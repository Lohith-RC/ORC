from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.audit_log import AuditLog
from app.schemas.analysis import AnalysisInfo
from app.api.deps import get_current_user, require_role
from app.services.longitudinal_tracker import fetch_patient_serial_trajectory

router = APIRouter()

@router.get("/me/analyses", response_model=List[AnalysisInfo])
def get_my_analyses(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve patient screenings conducted by the authenticated clinician (paginated)."""
    # ponytail: cap at 100 max to prevent OOM
    safe_limit = min(max(1, limit), 100)
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.timestamp.desc())
        .offset(max(0, offset))
        .limit(safe_limit)
        .all()
    )

@router.get("/analyses/{analysis_id}", response_model=AnalysisInfo)
def get_analysis_by_id(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnostic record not found")
        
    # Only owner or admin can inspect this record
    if analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access to patient record")
        
    return analysis

@router.get("/analyses/longitudinal/{patient_identifier}")
def get_patient_longitudinal_history(
    patient_identifier: str,
    lesion_site: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve serial chronological trajectory & growth velocity metrics for a specific patient ID."""
    trajectory = fetch_patient_serial_trajectory(
        db=db,
        user_id=current_user.id,
        patient_identifier=patient_identifier,
        lesion_site=lesion_site
    )
    return {
        "patient_identifier": patient_identifier,
        "lesion_site": lesion_site,
        "total_encounters": len(trajectory),
        "timeline": trajectory
    }

@router.get("/audit-logs")
def get_audit_trail(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """HIPAA Compliance: Review immutable clinical audit trail (Admin only)."""
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()

