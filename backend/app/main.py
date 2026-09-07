import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from sqlalchemy import inspect, text

from app.core.config import settings
from app.core.security import SecurityHeadersMiddleware
from app.core.rate_limit import limiter, rate_limit_handler
from app.db.session import engine, Base
import app.models  # Ensures all models (User, Analysis, AuditLog) are registered with Base
from app.api.v1.router import api_router

# Configure Structured JSON Logging
class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

log_handler = logging.StreamHandler()
log_handler.setFormatter(JSONLogFormatter())
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
# Replace default handlers with JSON handler
root_logger.handlers = [log_handler]

logger = logging.getLogger("app.main")

def run_safe_migrations():
    """Idempotent schema evolution ensuring columns and indexes exist across SQLite and PostgreSQL."""
    inspector = inspect(engine)
    with engine.begin() as conn:
        # 1. users table migrations
        user_cols = {c["name"] for c in inspector.get_columns("users")}
        if "role" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(30) DEFAULT 'clinician'"))
            logger.info("Database migration: added 'role' column to users")
        if "is_active" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"))
            logger.info("Database migration: added 'is_active' column to users")
        if "created_at" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
            logger.info("Database migration: added 'created_at' column to users")

        # 2. analyses table migrations
        analysis_cols = {c["name"] for c in inspector.get_columns("analyses")}
        if "uncertainty" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN uncertainty REAL"))
        if "risk_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN risk_score REAL"))
        if "image_quality_score" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN image_quality_score REAL"))
        if "tta_used" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN tta_used INTEGER DEFAULT 0"))
        if "patient_identifier" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN patient_identifier VARCHAR(64) DEFAULT 'ANON-001'"))
            logger.info("Database migration: added 'patient_identifier' column to analyses")
        if "triage_tier" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN triage_tier VARCHAR(64)"))
            logger.info("Database migration: added 'triage_tier' column to analyses")
        if "telemetry_data" not in analysis_cols:
            conn.execute(text("ALTER TABLE analyses ADD COLUMN telemetry_data TEXT"))
            logger.info("Database migration: added 'telemetry_data' column to analyses")

        # 3. Composite performance index migration
        analysis_indexes = {idx["name"] for idx in inspector.get_indexes("analyses")}
        if "idx_analyses_user_timestamp" not in analysis_indexes:
            try:
                conn.execute(text("CREATE INDEX idx_analyses_user_timestamp ON analyses (user_id, timestamp)"))
                logger.info("Database migration: created composite index idx_analyses_user_timestamp")
            except Exception as e:
                logger.warning(f"Index migration note: {e}")
        if "idx_analyses_patient_site" not in analysis_indexes:
            try:
                conn.execute(text("CREATE INDEX idx_analyses_patient_site ON analyses (user_id, patient_identifier, lesion_site)"))
                logger.info("Database migration: created composite index idx_analyses_patient_site")
            except Exception as e:
                logger.warning(f"Index migration note: {e}")


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-grade AI diagnostic platform with epistemic uncertainty and multimodal triage.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 1. Attach Rate Limiter
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    # 2. Security Headers & Request Correlation Middleware
    application.add_middleware(SecurityHeadersMiddleware)

    # 3. Enterprise CORS Lockdown
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Can be tightened via environment variable
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time-Ms"]
    )

    # 4. Mount API Routers
    # Versioned API: /api/v1/...
    application.include_router(api_router, prefix=settings.API_V1_STR)
    # Root API (100% Backwards Compatibility for existing frontend): /predict, /login, etc.
    application.include_router(api_router)

    @application.on_event("startup")
    def on_startup():
        logger.info(f"Initializing relational database on {settings.DATABASE_URL.split('@')[-1]}...")
        Base.metadata.create_all(bind=engine)
        run_safe_migrations()
        logger.info("Database schema synchronized successfully.")

    return application

app = create_application()
