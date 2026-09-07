"""
Clinical Interoperability & HL7 FHIR r4 Export Endpoints.
Produces FHIR Release 4 JSON Bundles and formal Oncological Referral Letters.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.rate_limit import get_client_ip
from app.api.deps import log_audit_action
from app.services.fhir_exporter import build_fhir_bundle, generate_specialist_referral_letter

router = APIRouter()


@router.get("/analyses/{analysis_id}/fhir")
def export_analysis_fhir_bundle(
    analysis_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Exports an analysis encounter as an official HL7 FHIR Release 4 compliant JSON Bundle.
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis #{analysis_id} not found.")

    if analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access to patient screening record.")

    # High-Assurance Audit Logging
    log_audit_action(
        db,
        action="EXPORT_FHIR_BUNDLE",
        user_id=current_user.id,
        ip_address=get_client_ip(request),
        details=f"Exported HL7 FHIR r4 Bundle for Specimen #{analysis_id} (Patient MRN: {analysis.patient_identifier})"
    )

    return build_fhir_bundle(analysis, current_user)


@router.get("/analyses/{analysis_id}/referral")
def get_analysis_specialist_referral(
    analysis_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generates structured Maxillofacial & Head & Neck Oncology specialist referral letter metadata.
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis #{analysis_id} not found.")

    if analysis.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access to patient screening record.")

    # High-Assurance Audit Logging
    log_audit_action(
        db,
        action="GENERATE_REFERRAL_LETTER",
        user_id=current_user.id,
        ip_address=get_client_ip(request),
        details=f"Generated specialist oncology referral letter for Specimen #{analysis_id} (Patient MRN: {analysis.patient_identifier})"
    )

    return generate_specialist_referral_letter(analysis, current_user)
