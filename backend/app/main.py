import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.security import SecurityHeadersMiddleware
from app.core.rate_limit import limiter, rate_limit_handler
from app.db.session import engine, Base
from app.db.migrations import run_safe_migrations
from app.services.ml_engine import warmup_model
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.validate()
    logger.info(f"Initializing relational database on {settings.DATABASE_URL.split('@')[-1]}...")
    Base.metadata.create_all(bind=engine)
    run_safe_migrations()
    logger.info("Database schema synchronized successfully.")
    warmup_model()
    yield

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-grade AI diagnostic platform with epistemic uncertainty and multimodal triage.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # 1. Attach Rate Limiter
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    # 2. Security Headers & Request Correlation Middleware
    application.add_middleware(SecurityHeadersMiddleware)

    # 3. Enterprise CORS Lockdown
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
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

    return application

app = create_application()
