import os
import json
import asyncio
import logging
import urllib.request
import anyio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
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


async def _keep_alive_worker():
    """
    Self-ping background worker to keep the Render container active.
    Fires an HTTP ping every 8 minutes, resetting Render's 15-minute idle spin-down timer.
    """
    raw_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("KEEP_ALIVE_URL")
    if not raw_url and os.getenv("ENVIRONMENT") != "development":
        raw_url = "https://oral-cancer-backend-fiwu.onrender.com"
        
    if not raw_url:
        logger.info("Keep-alive self-ping worker disabled in local environment.")
        return

    health_url = f"{raw_url.rstrip('/')}/health"
    logger.info(f"Keep-alive worker activated targeting: {health_url}")
    
    # Wait 2 minutes after startup before initial ping
    await asyncio.sleep(120)
    
    while True:
        try:
            req = urllib.request.Request(
                health_url,
                headers={"User-Agent": "OSCC-AI-Heartbeat/2.1.0"}
            )
            def _send_ping():
                with urllib.request.urlopen(req, timeout=20) as resp:
                    return resp.getcode()
                    
            status_code = await anyio.to_thread.run_sync(_send_ping)
            logger.info(f"Keep-alive heartbeat succeeded: HTTP {status_code}")
        except Exception as err:
            logger.warning(f"Keep-alive heartbeat notice: {err}")
            
        # Ping every 8 minutes (480s) to safely prevent Render's 15-minute idle shutdown
        await asyncio.sleep(480)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.validate()
    logger.info(f"Initializing relational database on {settings.DATABASE_URL.split('@')[-1]}...")
    Base.metadata.create_all(bind=engine)
    run_safe_migrations()
    logger.info("Database schema synchronized successfully.")
    if settings.WARMUP_ON_STARTUP:
        warmup_model()
    else:
        logger.info("Startup model warmup skipped (lazy loading enabled to conserve container memory).")

    # Start automated keep-alive worker in the background
    keep_alive_task = asyncio.create_task(_keep_alive_worker())
    
    yield
    
    keep_alive_task.cancel()
    try:
        await keep_alive_task
    except asyncio.CancelledError:
        pass

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

    # 3. Enterprise CORS Lockdown (Supports Whitelist & Vercel Preview/Production Domains)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_origin_regex=r"^https://.*\.vercel\.app$",
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

    # 5. Interactive Root Liveness Gateway
    @application.get("/", include_in_schema=False)
    @application.head("/", include_in_schema=False)
    async def root_status(request: Request):
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OSCC AI Engine | Operational</title>
  <style>
    :root { color-scheme: dark; }
    body {
      margin: 0; padding: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center;
      background: #080B10; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #F1F5F9;
    }
    .card {
      background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(51, 65, 85, 0.5);
      border-radius: 16px; padding: 36px 40px; max-width: 520px; width: 90%;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); backdrop-filter: blur(12px);
    }
    .badge {
      display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.15);
      color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 5px 14px; border-radius: 9999px;
      font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .pulse {
      width: 8px; height: 8px; background: #34D399; border-radius: 50%;
      box-shadow: 0 0 10px #34D399; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    h1 { margin: 18px 0 8px 0; font-size: 24px; font-weight: 700; color: #FFFFFF; }
    p { margin: 0 0 24px 0; color: #94A3B8; font-size: 14px; line-height: 1.5; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }
    .stat {
      background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(51, 65, 85, 0.4);
      padding: 12px 14px; border-radius: 10px;
    }
    .stat-label { font-size: 11px; text-transform: uppercase; color: #64748B; font-weight: 600; }
    .stat-val { font-size: 14px; font-weight: 600; color: #E2E8F0; margin-top: 4px; }
    .actions { display: flex; gap: 12px; }
    .btn {
      flex: 1; text-align: center; text-decoration: none; padding: 12px 16px; border-radius: 10px;
      font-size: 14px; font-weight: 600; transition: all 0.2s ease;
    }
    .btn-primary { background: #0D9488; color: white; }
    .btn-primary:hover { background: #0F766E; }
    .btn-secondary { background: #1E293B; color: #CBD5E1; border: 1px solid #334155; }
    .btn-secondary:hover { background: #334155; color: white; }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge"><div class="pulse"></div> Backend Operational</div>
    <h1>Oral Cancer AI Engine</h1>
    <p>FastAPI Deep Learning Diagnostic & Multimodal Triage API running on Uvicorn.</p>
    <div class="grid">
      <div class="stat"><div class="stat-label">Model Architecture</div><div class="stat-val">4-Backbone Ensemble</div></div>
      <div class="stat"><div class="stat-label">Platform Version</div><div class="stat-val">v2.1.0 Enterprise</div></div>
      <div class="stat"><div class="stat-label">Epistemic Variance</div><div class="stat-val">15-Pass MC Dropout</div></div>
      <div class="stat"><div class="stat-label">Container State</div><div class="stat-val">Keep-Alive Active</div></div>
    </div>
    <div class="actions">
      <a href="/docs" class="btn btn-primary">Swagger API Docs</a>
      <a href="/health" class="btn btn-secondary">System Health</a>
    </div>
  </div>
</body>
</html>"""
            return HTMLResponse(content=html_content, status_code=200)

        return JSONResponse(
            status_code=200,
            content={
                "status": "online",
                "system": settings.PROJECT_NAME,
                "version": settings.VERSION,
                "docs": "/docs",
                "health": "/health",
                "endpoints": {
                    "predict": f"{settings.API_V1_STR}/predict",
                    "auth": f"{settings.API_V1_STR}/auth",
                    "history": f"{settings.API_V1_STR}/history",
                    "interoperability": f"{settings.API_V1_STR}/interoperability"
                }
            }
        )

    return application

app = create_application()
