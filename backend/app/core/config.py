import os
import sys
import logging
from pathlib import Path
from typing import Set, List
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
_is_testing = (
    "pytest" in sys.modules
    or any("pytest" in arg for arg in sys.argv)
    or os.getenv("TESTING") == "1"
    or os.getenv("PYTEST_CURRENT_TEST") is not None
)

if not _is_testing:
    load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger(__name__)

# Default secret key for local development ONLY — rejected in production
_DEFAULT_SECRET_KEY = "LOCAL_DEV_ONLY_change_me_in_production"

class Settings:
    PROJECT_NAME: str = "Oral Cancer AI Detection Platform (OSCC AI)"
    VERSION: str = "2.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Base paths
    BASE_DIR: Path = BASE_DIR
    DEFAULT_DB_PATH: Path = BASE_DIR / "oralcancer.db"
    MODEL_PATH: Path = BASE_DIR / "merged_model.pth"
    
    # Database — automatic test isolation
    if _is_testing:
        _raw_db_url = os.getenv("TEST_DATABASE_URL", f"sqlite:///{BASE_DIR / 'oralcancer_test.db'}")
    else:
        _raw_db_url = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL: str = _raw_db_url
    
    # Security — reject insecure defaults in production
    SECRET_KEY: str = os.getenv("SECRET_KEY", _DEFAULT_SECRET_KEY)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS — environment-controlled whitelist (comma-separated origins)
    _cors_raw: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    CORS_ORIGINS: List[str] = [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]
    
    # Machine Learning & Clinical Thresholds
    UNCERTAINTY_THRESHOLD: float = 0.015       # Variance above which result is flagged uncertain
    TTA_PASSES: int = 8                        # Test-Time Augmentation passes
    MC_DROPOUT_PASSES: int = 15                # Monte Carlo Dropout stochastic passes
    BLUR_THRESHOLD: float = 50.0               # Laplacian variance threshold
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_CONTENT_TYPES: Set[str] = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    WARMUP_ON_STARTUP: bool = os.getenv("WARMUP_ON_STARTUP", "false").lower() in ("true", "1", "yes")

    def validate(self) -> None:
        """Validate critical configuration. Called on startup."""
        is_production = (
            "render" in self.DATABASE_URL.lower()
            or "supabase" in self.DATABASE_URL.lower()
            or os.getenv("RENDER") is not None
            or os.getenv("PRODUCTION") == "1"
        )
        
        if is_production and self.SECRET_KEY == _DEFAULT_SECRET_KEY:
            logger.critical(
                "SECURITY: SECRET_KEY is set to the default development value in a production environment. "
                "Set the SECRET_KEY environment variable to a strong random value."
            )
            raise RuntimeError(
                "Refusing to start: SECRET_KEY must be configured in production. "
                "Set SECRET_KEY as an environment variable."
            )
        
        if self.SECRET_KEY == _DEFAULT_SECRET_KEY:
            logger.warning(
                "SECURITY WARNING: Using default SECRET_KEY. "
                "This is acceptable for local development only."
            )

settings = Settings()
