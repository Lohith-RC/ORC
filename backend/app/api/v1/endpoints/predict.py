import io
import logging
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
from app.services.clinical_risk import compute_clinical_risk_score
from app.services.ml_engine import run_inference_pipeline

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
    lesion_site: str = Form("buccal_mucosa"),
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

    # 5. ASYNCHRONOUS INFERENCE (Unblocks Event Loop!)
    try:
        pred_class, confidence_score, uncertainty, quality_score = await anyio.to_thread.run_sync(
            run_inference_pipeline, image
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

    # 7. Clinical alert logic
    clinical_alert = None
    if pred_class == "cancer" and clinical_risk_score > 0.60:
        clinical_alert = "CRITICAL: High AI confidence for malignant lesion combined with high clinical risk profile. Urgent specialist referral strongly recommended."
    elif pred_class == "uncertain":
        clinical_alert = "WARNING: AI model epistemic uncertainty is elevated. Second opinion or clinical biopsy recommended."

    # Resolve anatomical metadata
    site_info = ANATOMICAL_SITE_METADATA.get(lesion_site, ANATOMICAL_SITE_METADATA["buccal_mucosa"])

    # 8. Persist to Relational Database
    new_analysis = Analysis(
        user_id=current_user.id,
        prediction=pred_class,
        confidence=confidence_score,
        uncertainty=round(uncertainty, 5),
        risk_score=round(clinical_risk_score, 3),
        image_quality_score=round(quality_score, 2),
        tta_used=True,
        lesion_site=lesion_site,
        image_filename=file.filename or "upload.jpg",
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # 9. Audit Trail
    log_audit_action(
        db,
        action="RUN_PREDICTION",
        user_id=current_user.id,
        ip_address=get_client_ip(request),
        details=f"Analysis #{new_analysis.id}: {pred_class} (site={lesion_site}, conf={confidence_score:.3f}, risk={clinical_risk_score:.3f})"
    )

    return {
        "id": new_analysis.id,
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
    }
