"""
Active Learning & Clinician Annotation REST Endpoints.
Provides uncertainty-ranked verification queues and pathology ground-truth submission.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.analysis import (
    ClinicianVerificationRequest,
    AnalysisInfo,
    ActiveLearningQueueItem,
    FlywheelMetricsResponse,
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.active_learning import (
    get_prioritized_active_learning_queue,
    submit_clinician_verification,
    compute_flywheel_metrics
)

router = APIRouter()


@router.get("/analyses/active-learning/queue", response_model=List[ActiveLearningQueueItem])
def get_active_learning_queue(
    limit: int = 40,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns high-uncertainty and clinically discordant cases prioritized for specialist review.
    """
    return get_prioritized_active_learning_queue(db, current_user.id, limit=limit)


@router.post("/analyses/{analysis_id}/verify", response_model=AnalysisInfo)
def verify_analysis_ground_truth(
    analysis_id: int,
    payload: ClinicianVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submits definitive pathology diagnosis, biopsy confirmation, and clinician annotations.
    """
    try:
        updated = submit_clinician_verification(db, analysis_id, current_user.id, payload)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record clinician verification: {str(e)}"
        )


@router.get("/analyses/active-learning/metrics", response_model=FlywheelMetricsResponse)
def get_active_learning_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns active learning flywheel operational metrics and concordance statistics.
    """
    return compute_flywheel_metrics(db)
