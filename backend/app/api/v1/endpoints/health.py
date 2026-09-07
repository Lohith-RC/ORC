from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.services.ml_engine import get_model, device

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive Liveness Probe:
      - Validates database connectivity
      - Validates AI inference model status
    """
    db_status = "connected"
    try:
        db.execute(text("SELECT 1;"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    model_loaded = get_model() is not None
    
    return {
        "status": "ok" if db_status == "connected" and model_loaded else "degraded",
        "database": db_status,
        "model": "loaded" if model_loaded else "unloaded",
        "device": str(device),
        "version": "2.0.0"
    }
