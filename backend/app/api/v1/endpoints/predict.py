import io
import json
import logging
import datetime
import anyio
from PIL import Image

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Request, Form
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import limiter, get_client_ip
from app.db.session import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.schemas.clinical import ClinicalRiskForm
from app.api.deps import get_current_user, log_audit_action
from typing import Optional
from app.services.clinical_risk import compute_clinical_risk_score
from app.services.vision_pipeline import execute_dual_stage_pipeline
from app.services.clinical_staging import evaluate_ajcc_staging
from app.services.longitudinal_tracker import compute_longitudinal_delta

logger = logging.getLogger(__name__)

router = APIRouter()

ANATOMICAL_SITE_METADATA = {
    "buccal_mucosa": {"display": "Buccal Mucosa (Cheek Lining)", "risk_tier": "Standard", "metastatic_propensity": "Moderate"},
    "lateral_tongue": {"display": "Lateral Border of Tongue", "risk_tier": "High Risk", "metastatic_propensity": "High (Early Occult Nodal Spread)"},
    "floor_of_mouth": {"display": "Floor of Mouth", "risk_tier": "High Risk", "metastatic_propensity": "High (Early Lymphatic Drainage)"},
    "dorsal_tongue": {"display": "Dorsal Tongue", "risk_tier": "Standard", "metastatic_propensity": "Low"},
    "hard_palate": {"display": "Hard Palate", "risk_tier": "Standard", "metastatic_propensity": "Low"},
    "soft_palate": {"display": "Soft Palate / Oropharynx", "risk_tier": "High Risk (HPV Predilection)", "metastatic_propensity": "High"},
    "gingiva": {"display": "Gingiva / Retromolar Trigone", "risk_tier": "Elevated", "metastatic_propensity": "Moderate-High (Bone Infiltration Risk)"},
    "lip": {"display": "Labial Mucosa / Vermilion Border", "risk_tier": "Standard (UV-related)", "metastatic_propensity": "Low-Moderate"}
}

@router.post("/predict")
@limiter.limit("20/minute")
async def predict(
    request: Request,
    file: UploadFile = File(...),
    vital_stain_file: Optional[UploadFile] = File(None),
    patient_identifier: str = Form("ANON-001"),
    lesion_site: str = Form("buccal_mucosa"),
    cross_polarized: bool = Form(False),
    distance_mm: float = Form(50.0),
    age: int = Form(30),
    tobacco_use: bool = Form(False),
    alcohol_use: bool = Form(False),
    betel_nut: bool = Form(False),
    prior_lesions: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    """
    Production AI Diagnostic Screening Endpoint:
      - Accepts clinical risk factors in multipart FormData body (Zero PHI URL Query Leakage)
      - Validates MIME type
      - Enforces streaming 64KB chunk early-exit memory guard against payload exhaustion (<= 10MB)
      - Executes forward passes asynchronously via anyio.to_thread.run_sync (Zero Event-Loop Blocking)
      - Computes epistemic uncertainty via Monte Carlo Dropout
      - Calculates multimodal epidemiological risk score
      - Records clinical audit trail in PostgreSQL
    """
    # 1. MIME Validation
    if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported: JPEG, PNG, WEBP."
        )

    # 2. File size boundary validation with 64KB chunk-based early exit (prevents OOM on large payloads)
    max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    image_bytes = bytearray()
    
    while chunk := await file.read(65536):
        image_bytes.extend(chunk)
        if len(image_bytes) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum limit of {settings.MAX_IMAGE_SIZE_MB}MB."
            )

    # 3. Decode image
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or corrupt image payload.")

    # 3b. Decode optional vital stain / autofluorescence specimen
    vital_img = None
    if vital_stain_file and vital_stain_file.filename:
        if vital_stain_file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid vital stain file type '{vital_stain_file.content_type}'. Supported: JPEG, PNG, WEBP."
            )
        vital_bytes = bytearray()
        while chunk := await vital_stain_file.read(65536):
            vital_bytes.extend(chunk)
            if len(vital_bytes) > max_bytes:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Vital stain file exceeds maximum limit of {settings.MAX_IMAGE_SIZE_MB}MB."
                )
        try:
            vital_img = Image.open(io.BytesIO(vital_bytes)).convert("RGB")
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or corrupt vital stain image.")

    # 4. Clinical risk factors
    try:
        risk_form = ClinicalRiskForm(
            age=age,
            tobacco_use=tobacco_use,
            alcohol_use=alcohol_use,
            betel_nut=betel_nut,
            prior_lesions=prior_lesions,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    clinical_risk_score = compute_clinical_risk_score(risk_form)

    # 5. ASYNCHRONOUS DUAL-STAGE INFERENCE (Unblocks Event Loop!)
    try:
        pred_class, confidence_score, uncertainty, quality_score, telemetry = await anyio.to_thread.run_sync(
            execute_dual_stage_pipeline, image, vital_img, distance_mm, cross_polarized
        )
    except Exception as e:
        logger.error(f"Inference failure for clinician {current_user.username}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI diagnostic engine encountered an error during inference."
        )

    # 6. Quality flag
    image_quality_flag = None
    if quality_score < settings.BLUR_THRESHOLD:
        image_quality_flag = (
            f"Image may be blurry (sharpness score {quality_score:.1f} < {settings.BLUR_THRESHOLD}). "
            "Please review carefully or recapture."
        )

    # 7. AJCC 8th Edition Clinical Staging & Triage Evaluation
    staging_report = evaluate_ajcc_staging(
        prediction=pred_class,
        confidence=confidence_score,
        lesion_site=lesion_site,
        diameter_mm=telemetry.diameter_mm,
        clinical_risk_score=clinical_risk_score,
        vital_stain_abnormal=telemetry.vital_stain_abnormal,
        is_cross_polarized=cross_polarized,
        border_irregularity=telemetry.border_irregularity_score
    )

    # Clinical alert logic
    clinical_alert = None
    if pred_class == "cancer" and clinical_risk_score > 0.60:
        clinical_alert = "CRITICAL: High AI confidence for malignant lesion combined with high clinical risk profile. Urgent specialist referral strongly recommended."
    elif pred_class == "uncertain":
        clinical_alert = "WARNING: AI model epistemic uncertainty is elevated. Second opinion or clinical biopsy recommended."

    # Resolve anatomical metadata
    site_info = ANATOMICAL_SITE_METADATA.get(lesion_site, ANATOMICAL_SITE_METADATA["buccal_mucosa"])

    # 8. Longitudinal Patient Tracking & Delta Calibration
    prior_analysis = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.patient_identifier == patient_identifier,
        Analysis.lesion_site == lesion_site
    ).order_by(Analysis.timestamp.desc()).first()

    current_timestamp = datetime.datetime.now(datetime.timezone.utc)
    longitudinal_delta = compute_longitudinal_delta(
        current_area_mm2=telemetry.surface_area_mm2,
        current_diameter_mm=telemetry.diameter_mm,
        current_irregularity=telemetry.border_irregularity_score,
        current_contour=telemetry.contour_points,
        current_timestamp=current_timestamp,
        prior_analysis=prior_analysis
    )

    telemetry_dict = {
        "mask_detected": telemetry.mask_detected,
        "center_pct": telemetry.center_pct,
        "diameter_mm": telemetry.diameter_mm,
        "surface_area_mm2": telemetry.surface_area_mm2,
        "border_irregularity_score": telemetry.border_irregularity_score,
        "contour_points": telemetry.contour_points,
        "optical_cross_polarized": telemetry.optical_cross_polarized,
        "vital_stain_present": telemetry.vital_stain_present,
        "vital_stain_abnormal": telemetry.vital_stain_abnormal,
    }

    # 9. Persist to Relational Database
    new_analysis = Analysis(
        user_id=current_user.id,
        patient_identifier=patient_identifier,
        prediction=pred_class,
        confidence=confidence_score,
        uncertainty=round(uncertainty, 5),
        risk_score=round(clinical_risk_score, 3),
        image_quality_score=round(quality_score, 2),
        tta_used=True,
        lesion_site=lesion_site,
        triage_tier=staging_report.triage_tier.value,
        telemetry_data=json.dumps(telemetry_dict),
        image_filename=file.filename or "upload.jpg",
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # 10. Audit Trail
    log_audit_action(
        db,
        action="RUN_PREDICTION",
        user_id=current_user.id,
        ip_address=get_client_ip(request),
        details=f"Analysis #{new_analysis.id}: {pred_class} (patient={patient_identifier}, site={lesion_site}, conf={confidence_score:.3f}, risk={clinical_risk_score:.3f})"
    )

    staging_dict = staging_report.model_dump() if hasattr(staging_report, "model_dump") else staging_report.dict()
    trajectory_dict = longitudinal_delta.model_dump() if hasattr(longitudinal_delta, "model_dump") else longitudinal_delta.dict()

    return {
        "id": new_analysis.id,
        "patient_identifier": patient_identifier,
        "prediction": pred_class,
        "confidence": round(confidence_score, 4),
        "uncertainty": round(uncertainty, 5),
        "clinical_risk_score": round(clinical_risk_score, 3),
        "lesion_site": lesion_site,
        "lesion_site_display": site_info["display"],
        "lesion_site_risk": site_info["risk_tier"],
        "metastatic_propensity": site_info["metastatic_propensity"],
        "clinical_alert": clinical_alert,
        "image_quality": image_quality_flag or "acceptable",
        "tta_passes": settings.TTA_PASSES,
        "mc_dropout_passes": settings.MC_DROPOUT_PASSES,
        "timestamp": new_analysis.timestamp,
        "telemetry": telemetry_dict,
        "clinical_staging": staging_dict,
        "longitudinal_trajectory": trajectory_dict,
    }

