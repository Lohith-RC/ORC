import os
from pathlib import Path
from typing import Set
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "Oral Cancer AI Detection Platform (OSCC AI)"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Base paths
    BASE_DIR: Path = BASE_DIR
    DEFAULT_DB_PATH: Path = BASE_DIR / "oralcancer.db"
    MODEL_PATH: Path = BASE_DIR / "merged_model.pth"
    
    # Database
    _raw_db_url = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL: str = _raw_db_url
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "oral_cancer_detection_super_secret_jwt_key_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Machine Learning & Clinical Thresholds
    UNCERTAINTY_THRESHOLD: float = 0.015       # Variance above which result is flagged uncertain
    TTA_PASSES: int = 8                        # Test-Time Augmentation passes
    MC_DROPOUT_PASSES: int = 15                # Monte Carlo Dropout stochastic passes
    BLUR_THRESHOLD: float = 50.0               # Laplacian variance threshold
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_CONTENT_TYPES: Set[str] = {"image/jpeg", "image/jpg", "image/png", "image/webp"}

settings = Settings()
