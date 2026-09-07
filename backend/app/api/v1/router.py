from fastapi import APIRouter
from app.api.v1.endpoints import auth, predict, history, health, active_learning

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(predict.router, tags=["AI Diagnostic Inference"])
api_router.include_router(history.router, tags=["Patient Screening History"])
api_router.include_router(active_learning.router, tags=["Active Learning & Pathology Ground Truth"])
api_router.include_router(health.router, tags=["Health & Observability"])
