from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.models.audit_log import AuditLog
from app.schemas.analysis import AnalysisInfo
from app.api.deps import get_current_user, require_role

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

@router.get("/audit-logs")
def get_audit_trail(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """HIPAA Compliance: Review immutable clinical audit trail (Admin only)."""
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
