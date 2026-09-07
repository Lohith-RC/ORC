from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.rate_limit import limiter, get_client_ip
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, Token
from app.api.deps import get_current_user, log_audit_action

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account. Rate-limited to 5/minute to prevent credential stuffing."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    if user.email:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_pw,
        full_name=user.full_name,
        email=user.email,
        role=user.role or "clinician",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_audit_action(
        db, action="REGISTER_USER", user_id=new_user.id,
        ip_address=get_client_ip(request), details=f"Registered username: {new_user.username}"
    )
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate clinician or patient and issue cryptographically signed JWT token."""
    username = form_data.username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = db.query(User).filter(User.username.ilike(username)).first()
    if not user:
        user = db.query(User).filter(User.email == username).first()
        
    if not user or not verify_password(form_data.password, user.hashed_password):
        log_audit_action(
            db, action="FAILED_LOGIN",
            ip_address=get_client_ip(request), details=f"Failed login attempt for: {username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if user.is_active is not None and not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    log_audit_action(
        db, action="SUCCESSFUL_LOGIN", user_id=user.id,
        ip_address=get_client_ip(request), details=f"Login successful for user: {user.username}"
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/me/update", response_model=UserResponse)
def update_me(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if update_data.email and update_data.email != current_user.email:
        if "@" not in update_data.email:
            raise HTTPException(status_code=422, detail="Invalid email address")
        if db.query(User).filter(User.email == update_data.email).first():
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
