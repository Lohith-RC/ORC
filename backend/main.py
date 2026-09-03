import io
import datetime
import os
import hashlib
import hmac
import base64
import secrets
import logging
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, validator
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# ============================================================
#  LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================
#  CONFIGURATION  (read from env vars for production)
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "oralcancer.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

# SECURITY: Secret key should come from environment, never hardcoded in prod
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_USE_SECRETS_TOKEN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ML thresholds
UNCERTAINTY_THRESHOLD = 0.015       # σ² above this → uncertain
TTA_PASSES = 8                       # Test-Time Augmentation passes
MC_DROPOUT_PASSES = 15               # Monte Carlo Dropout passes
BLUR_THRESHOLD = 50.0                # Laplacian variance below → blurry
MAX_IMAGE_SIZE_MB = 10               # Reject images > 10 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

# ============================================================
#  DATABASE SETUP
# ============================================================
engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    analyses = relationship("Analysis", back_populates="owner")


class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(String)
    confidence = Column(Float)
    uncertainty = Column(Float, nullable=True)           # Fault 4
    risk_score = Column(Float, nullable=True)            # Fault 5
    image_quality_score = Column(Float, nullable=True)   # Fault 6
    tta_used = Column(Boolean, default=False)            # Fault 6
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    image_filename = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="analyses")


Base.metadata.create_all(bind=engine)


def _safe_migrate():
    """
    Add new columns to existing tables if they don't already exist.
    This avoids breaking existing databases when the schema evolves.
    Works for both SQLite and PostgreSQL.
    """
    from sqlalchemy import inspect, text
    inspector = inspect(engine)

    with engine.begin() as conn:
        # --- users table ---
        user_cols = {c["name"] for c in inspector.get_columns("users")}
        if "is_active" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"))
            logger.info("Migration: added 'is_active' column to users")
        if "created_at" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN created_at TEXT"))
            logger.info("Migration: added 'created_at' column to users")

        # --- analyses table ---
        analysis_cols = {c["name"] for c in inspector.get_columns("analyses")}
        if "uncertainty" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN uncertainty REAL"))
            logger.info("Migration: added 'uncertainty' column to analyses")
        if "risk_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN risk_score REAL"))
            logger.info("Migration: added 'risk_score' column to analyses")
        if "image_quality_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN image_quality_score REAL"))
            logger.info("Migration: added 'image_quality_score' column to analyses")
        if "tta_used" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN tta_used INTEGER DEFAULT 0"))
            logger.info("Migration: added 'tta_used' column to analyses")


_safe_migrate()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
#  PYDANTIC SCHEMAS
# ============================================================
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None

    @validator("username")
    def username_alphanumeric(cls, v):
        v = v.strip()
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return v

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @validator("email")
    def email_basic_check(cls, v):
        # v can be None/empty — only validate if provided
        if v and "@" not in v:
            raise ValueError("Invalid email address — must contain '@'")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class ClinicalRiskForm(BaseModel):
    """Fault 5: Structured clinical risk factors for multimodal fusion."""
    age: int
    tobacco_use: bool = False
    alcohol_use: bool = False
    betel_nut: bool = False
    prior_lesions: bool = False

    @validator("age")
    def age_range(cls, v):
        if not (5 <= v <= 110):
            raise ValueError("Age must be between 5 and 110")
        return v


class AnalysisInfo(BaseModel):
    id: int
    prediction: str
    confidence: float
    uncertainty: Optional[float] = None
    risk_score: Optional[float] = None
    image_quality_score: Optional[float] = None
    timestamp: datetime.datetime
    image_filename: str

    class Config:
        from_attributes = True


# ============================================================
#  PASSWORD & JWT UTILITIES
# ============================================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_password_hash(password: str) -> str:
    """PBKDF2-SHA256 hashing — stronger than plain bcrypt for this use case."""
    salt = secrets.token_bytes(16)
    iterations = 390000
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_b64, hash_b64 = hashed_password.split("$", 3)
            salt = base64.b64decode(salt_b64)
            expected = base64.b64decode(hash_b64)
            candidate = hashlib.pbkdf2_hmac(
                "sha256", plain_password.encode("utf-8"), salt, int(iterations)
            )
            return hmac.compare_digest(candidate, expected)
        except Exception:
            return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (
        expires_delta or datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
#  FASTAPI APP + RATE LIMITING
# ============================================================
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Oral Cancer AI Detection API",
    description="Secure, production-grade AI diagnostic backend.",
    version="2.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#  AUTHENTICATION HELPERS
# ============================================================
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str):
    # Try exact username match, then case-insensitive, then email
    user = get_user(db, username)
    if not user:
        user = db.query(User).filter(User.username.ilike(username)).first()
    if not user:
        user = get_user_by_email(db, username)
    if not user:
        return None
    # is_active can be NULL for old migrated rows — treat NULL as active
    if user.is_active is not None and not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: {username}")
        return None
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    # is_active can be NULL for old migrated rows — treat NULL as active
    if user is None or (user.is_active is not None and not user.is_active):
        raise credentials_exception
    return user


# ============================================================
#  ML MODEL SETUP
# ============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using compute device: {device}")


class MergedNet(nn.Module):
    def __init__(self, num_classes):
        super(MergedNet, self).__init__()
        self.vgg16 = models.vgg16(weights=None).features
        self.resnet = nn.Sequential(*list(models.resnet50(weights=None).children())[:-2])
        self.efficientnet = models.efficientnet_b0(weights=None).features
        self.mobilenet = models.mobilenet_v2(weights=None).features
        for m in [self.vgg16, self.resnet, self.efficientnet, self.mobilenet]:
            for param in m.parameters():
                param.requires_grad = False
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(512 + 2048 + 1280 + 1280, 512),
            nn.ReLU(),
            nn.Dropout(0.5),   # Dropout retained — enables MC Dropout at inference
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        f1 = self.pool(self.vgg16(x)).view(x.size(0), -1)
        f2 = self.pool(self.resnet(x)).view(x.size(0), -1)
        f3 = self.pool(self.efficientnet(x)).view(x.size(0), -1)
        f4 = self.pool(self.mobilenet(x)).view(x.size(0), -1)
        merged = torch.cat([f1, f2, f3, f4], dim=1)
        return self.classifier(merged)


# Standard inference transform
inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# Fault 6 — Test-Time Augmentation (TTA) transforms for domain robustness
tta_transforms = [
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomHorizontalFlip(p=1.0), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomVerticalFlip(p=1.0), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.ColorJitter(brightness=0.2), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.ColorJitter(contrast=0.2), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((256, 256)), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomRotation(15), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    transforms.Compose([transforms.Resize((224, 224)), transforms.RandomGrayscale(p=0.5), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
    inference_transform,  # Original transform included as one pass
]

class_names = ["cancer", "non_cancer"]
ai_model = MergedNet(num_classes=2)
model_path = BASE_DIR / "merged_model.pth"
if not model_path.exists():
    raise RuntimeError(f"Model file not found at: {model_path}")
ai_model.load_state_dict(torch.load(model_path, map_location=device))
ai_model.eval()
ai_model.to(device)
logger.info("AI model loaded successfully.")


# ============================================================
#  UTILITY FUNCTIONS
# ============================================================
def compute_image_quality(img_array: np.ndarray) -> float:
    """
    Fault 6 — Image Quality Gating.
    Computes sharpness via Laplacian variance. Values < BLUR_THRESHOLD indicate blur.
    """
    gray = np.mean(img_array, axis=2) if img_array.ndim == 3 else img_array
    gray = gray.astype(np.float32)
    # Approximate Laplacian via finite differences
    laplacian = (
        np.roll(gray, -1, 0) + np.roll(gray, 1, 0) +
        np.roll(gray, -1, 1) + np.roll(gray, 1, 1) - 4 * gray
    )
    return float(np.var(laplacian))


def compute_clinical_risk_score(form: ClinicalRiskForm) -> float:
    """
    Fault 5 — Clinical Risk Factor Scoring.
    Generates a weighted risk score (0.0–1.0) from structured patient metadata.
    Based on established OSCC epidemiological risk weights.
    """
    score = 0.0
    # Age risk: peaks sharply after 40
    if form.age >= 60:
        score += 0.30
    elif form.age >= 40:
        score += 0.15
    # Tobacco is the highest single risk factor for OSCC
    if form.tobacco_use:
        score += 0.35
    # Alcohol amplifies tobacco risk (co-carcinogen)
    if form.alcohol_use:
        score += 0.20
    # Betel nut is the primary risk factor in South Asian populations
    if form.betel_nut:
        score += 0.30
    # Prior lesions indicate a history of dysplasia
    if form.prior_lesions:
        score += 0.25
    return min(score, 1.0)


def run_inference_with_tta_and_mcd(image: Image.Image):
    """
    Full inference pipeline:
      1. Image quality gate (Fault 6)
      2. Test-Time Augmentation — 8 passes (Fault 6)
      3. Monte Carlo Dropout — 15 passes (Fault 4)
      4. Aggregate mean + variance for uncertainty
    """
    img_array = np.array(image)
    quality_score = compute_image_quality(img_array)

    # --- TTA: collect predictions across augmented versions ---
    tta_probs = []
    with torch.no_grad():
        for t in tta_transforms:
            tensor = t(image).unsqueeze(0).to(device)
            out = ai_model(tensor)
            tta_probs.append(torch.nn.functional.softmax(out, dim=1))
    tta_mean = torch.stack(tta_probs).mean(dim=0)  # [1, num_classes]

    # --- MC Dropout: stochastic passes with dropout ON ---
    ai_model.train()  # Enable dropout layers
    mcd_preds = []
    with torch.no_grad():
        base_tensor = inference_transform(image).unsqueeze(0).to(device)
        for _ in range(MC_DROPOUT_PASSES):
            out = ai_model(base_tensor)
            mcd_preds.append(torch.nn.functional.softmax(out, dim=1))
    ai_model.eval()  # Restore eval mode

    mcd_stack = torch.stack(mcd_preds)
    mcd_mean = mcd_stack.mean(dim=0)       # [1, num_classes]
    mcd_var = mcd_stack.var(dim=0)

    # Fuse TTA mean and MCD mean (equal weighting)
    final_probs = 0.5 * tta_mean + 0.5 * mcd_mean
    confidence, pred_idx = torch.max(final_probs, 1)
    pred_class = class_names[pred_idx.item()]
    confidence_score = confidence.item()
    uncertainty = mcd_var.max().item()

    return pred_class, confidence_score, uncertainty, quality_score


# ============================================================
#  API ENDPOINTS
# ============================================================

@app.post("/register", status_code=201)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user. Rate-limited to prevent brute-force account creation."""
    try:
        if get_user(db, user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if user.email and get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        new_user = User(
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name,
            email=user.email,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"New user registered: {user.username}")
        return {"message": "User registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during registration")


@app.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user. Rate-limited to prevent brute-force attacks."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/predict")
@limiter.limit("20/minute")
async def predict(
    request: Request,
    file: UploadFile = File(...),
    age: int = 30,
    tobacco_use: bool = False,
    alcohol_use: bool = False,
    betel_nut: bool = False,
    prior_lesions: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Full AI inference endpoint with:
    - Input validation & size limits (Security)
    - Image quality gating (Fault 6)
    - Test-Time Augmentation for domain robustness (Fault 6)
    - MC Dropout for uncertainty quantification (Fault 4)
    - Clinical risk factor scoring (Fault 5)
    """
    # --- Security: Validate file type ---
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only JPEG, PNG, and WEBP images are accepted.",
        )

    image_bytes = await file.read()

    # --- Security: Validate file size ---
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({size_mb:.1f} MB). Maximum allowed is {MAX_IMAGE_SIZE_MB} MB.",
        )

    # --- Validate image can be opened ---
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.")

    # --- Fault 5: Build clinical risk form ---
    try:
        risk_form = ClinicalRiskForm(
            age=age,
            tobacco_use=tobacco_use,
            alcohol_use=alcohol_use,
            betel_nut=betel_nut,
            prior_lesions=prior_lesions,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    clinical_risk_score = compute_clinical_risk_score(risk_form)

    # --- Full inference pipeline (TTA + MC Dropout) ---
    try:
        pred_class, confidence_score, uncertainty, quality_score = run_inference_with_tta_and_mcd(image)
    except Exception as e:
        logger.error(f"Inference error for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="AI inference failed. Please try again.")

    # --- Fault 6: Image quality gate ---
    image_quality_flag = None
    if quality_score < BLUR_THRESHOLD:
        image_quality_flag = "low_quality"
        logger.warning(f"Low quality image from user {current_user.username} (blur score: {quality_score:.2f})")

    # --- Fault 4: Override prediction if uncertain ---
    final_prediction = pred_class
    if uncertainty > UNCERTAINTY_THRESHOLD:
        final_prediction = "uncertain"

    # --- Fault 5: Boost confidence flag if clinical risk is high ---
    clinical_alert = clinical_risk_score >= 0.6

    # --- Persist analysis to DB ---
    new_analysis = Analysis(
        user_id=current_user.id,
        prediction=final_prediction,
        confidence=confidence_score,
        uncertainty=round(uncertainty, 5),
        risk_score=round(clinical_risk_score, 3),
        image_quality_score=round(quality_score, 2),
        tta_used=True,
        image_filename=file.filename,
    )
    db.add(new_analysis)
    db.commit()
    logger.info(
        f"Prediction for {current_user.username}: {final_prediction} "
        f"(conf={confidence_score:.3f}, unc={uncertainty:.5f}, risk={clinical_risk_score:.3f})"
    )

    return {
        "prediction": final_prediction,
        "confidence": round(confidence_score, 4),
        "uncertainty": round(uncertainty, 5),
        "clinical_risk_score": round(clinical_risk_score, 3),
        "clinical_alert": clinical_alert,
        "image_quality": image_quality_flag or "acceptable",
        "tta_passes": TTA_PASSES,
        "mc_dropout_passes": MC_DROPOUT_PASSES,
    }


@app.get("/me", response_model=UserInfo)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/me/analyses", response_model=List[AnalysisInfo])
def get_user_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.timestamp.desc())
        .all()
    )


@app.post("/me/update", response_model=UserInfo)
def update_me(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if update_data.email and update_data.email != current_user.email:
        if "@" not in update_data.email:
            raise HTTPException(status_code=422, detail="Invalid email address")
        if get_user_by_email(db, update_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = update_data.email
    if update_data.full_name is not None:
        fn = update_data.full_name.strip()
        if len(fn) > 100:
            raise HTTPException(status_code=422, detail="Full name too long")
        current_user.full_name = fn
    db.commit()
    db.refresh(current_user)
    return current_user


@app.get("/health")
def health_check():
    """Lightweight health check endpoint for monitoring."""
    return {"status": "ok", "model": "loaded", "device": str(device)}