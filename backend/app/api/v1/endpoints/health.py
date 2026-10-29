import time
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.db.session import get_db
from app.services.ml_engine import get_model, get_ort_session, device

router = APIRouter()
_BOOT_TIME = time.time()

@router.get("/health")
@router.head("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive Enterprise Liveness & Observability Probe:
      - Validates relational database connectivity (Supabase / SQLite)
      - Inspects AI model status (ONNX Runtime vs PyTorch MergedNet)
      - Telemetry: Uptime, inference device, thresholds, keep-alive state
    """
    db_status = "connected"
    try:
        db.execute(text("SELECT 1;"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    ort_session = get_ort_session()
    model_loaded = ort_session is not None or get_model() is not None
    engine_backend = "ONNX INT8 Runtime" if ort_session is not None else "PyTorch MergedNet"
    
    uptime_sec = int(time.time() - _BOOT_TIME)
    hours, remainder = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_human = f"{hours}h {minutes}m {seconds}s"

    return {
        "status": "ok" if db_status == "connected" and model_loaded else "degraded",
        "database": db_status,
        "model": "loaded" if model_loaded else "unloaded",
        "engine_backend": engine_backend,
        "device": str(device),
        "version": settings.VERSION,
        "uptime_seconds": uptime_sec,
        "uptime": uptime_human,
        "thresholds": {
            "uncertainty": settings.UNCERTAINTY_THRESHOLD,
            "blur_min_sharpness": settings.BLUR_THRESHOLD,
            "max_image_mb": settings.MAX_IMAGE_SIZE_MB
        },
        "keep_alive": "active"
    }
