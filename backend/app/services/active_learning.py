"""
Active Learning Data Flywheel & Clinician-in-the-Loop Weak Supervision Service.
Computes acquisition priorities using Bayesian uncertainty sampling and clinical discordance.
"""

import datetime
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import (
    ClinicianVerificationRequest,
    ActiveLearningQueueItem,
    FlywheelMetricsResponse
)

# Standardized Ground Truth Diagnoses
GROUND_TRUTH_DIAGNOSES = {
    "OSCC_MALIGNANT": "Oral Squamous Cell Carcinoma (Malignant)",
    "HIGH_GRADE_DYSPLASIA": "High-Grade Epithelial Dysplasia (Pre-cancerous)",
    "MILD_MOD_DYSPLASIA": "Mild / Moderate Epithelial Dysplasia",
    "LICHEN_PLANUS": "Oral Lichen Planus / Keratotic Lesion",
    "TRAUMATIC_ULCER": "Traumatic / Aphthous Reactive Ulcer",
    "BENIGN_HYPERKERATOSIS": "Frictional Hyperkeratosis (Benign)",
    "NORMAL_MUCOSA": "Normal Healthy Oral Mucosa",
}

HISTOLOGY_GRADES = {
    "WELL_DIFFERENTIATED": "Well Differentiated (G1)",
    "MODERATELY_DIFFERENTIATED": "Moderately Differentiated (G2)",
    "POORLY_DIFFERENTIATED": "Poorly Differentiated / Anaplastic (G3)",
    "NOT_APPLICABLE": "Not Applicable / Non-Carcinoma",
}


def compute_acquisition_priority(analysis: Analysis) -> Tuple[float, str]:
    """
    Computes Active Learning acquisition score combining:
    1. Epistemic Uncertainty (Bayesian MC Dropout variance)
    2. Deep Model Confidence vs Epidemiological Risk Score Discordance
    3. AJCC Triage Tier Urgency
    """
    uncertainty = float(analysis.uncertainty or 0.0)
    conf = float(analysis.confidence or 0.5)
    risk = float(analysis.risk_score or 0.0)
    tier = analysis.triage_tier or ""

    # 1. Normalized Uncertainty (typical MC dropout variance range 0.00 - 0.20)
    norm_uncertainty = min(1.0, max(0.0, uncertainty / 0.18))

    # 2. Model-Clinical Discordance
    # E.g. Model confidence is 90% cancer but clinical risk is 10% (discordance 0.80)
    discordance = abs(conf - risk)

    # 3. Triage Tier Urgency weight
    tier_weight = 0.0
    if "Tier 3" in tier or "TIER_3" in tier:
        tier_weight = 1.0
    elif "Tier 2" in tier or "TIER_2" in tier:
        tier_weight = 0.5

    priority_score = (
        0.45 * norm_uncertainty +
        0.35 * discordance +
        0.20 * tier_weight
    )

    reasons = []
    if norm_uncertainty >= 0.65:
        reasons.append(f"High Model Uncertainty (σ²={uncertainty:.3f})")
    if discordance >= 0.50:
        reasons.append(f"Discordant Vision/Risk Profile (Δ={discordance:.2f})")
    if tier_weight == 1.0:
        reasons.append("Tier 3 High Oncology Suspicion")

    if not reasons:
        reasons.append("Standard Active Learning Sampling")

    return round(priority_score, 4), " • ".join(reasons)


def get_prioritized_active_learning_queue(
    db: Session,
    user_id: int,
    limit: int = 40
) -> List[ActiveLearningQueueItem]:
    """
    Retrieves unverified or unconfirmed analyses, ranks them by acquisition priority,
    and returns a queue for clinician verification.
    """
    unverified = db.query(Analysis).filter(
        (Analysis.ground_truth_dx.is_(None)) | (Analysis.biopsy_proven == False)
    ).order_by(Analysis.timestamp.desc()).limit(150).all()

    scored_items: List[Tuple[float, ActiveLearningQueueItem]] = []

    for item in unverified:
        priority_score, priority_reason = compute_acquisition_priority(item)
        queue_item = ActiveLearningQueueItem(
            analysis_id=item.id,
            patient_identifier=item.patient_identifier or "ANON-001",
            lesion_site=item.lesion_site or "buccal_mucosa",
            prediction=item.prediction,
            confidence=round(item.confidence, 4),
            uncertainty=round(float(item.uncertainty or 0.0), 4),
            risk_score=round(float(item.risk_score or 0.0), 3),
            triage_tier=item.triage_tier,
            timestamp=item.timestamp,
            priority_score=priority_score,
            priority_reason=priority_reason
        )
        scored_items.append((priority_score, queue_item))

    # Sort descending by priority score
    scored_items.sort(key=lambda x: x[0], reverse=True)

    return [item[1] for item in scored_items[:limit]]


def submit_clinician_verification(
    db: Session,
    analysis_id: int,
    user_id: int,
    payload: ClinicianVerificationRequest
) -> Analysis:
    """
    Applies ground truth verification from an authenticated clinician or pathologist.
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise ValueError(f"Analysis record #{analysis_id} not found.")

    analysis.ground_truth_dx = payload.ground_truth_dx
    analysis.biopsy_proven = payload.biopsy_proven
    analysis.histology_grade = payload.histology_grade
    analysis.clinician_feedback_notes = payload.clinician_feedback_notes
    if payload.annotated_contour:
        analysis.annotated_contour = payload.annotated_contour
    analysis.verified_at = datetime.datetime.utcnow()
    analysis.verified_by_user_id = user_id

    db.commit()
    db.refresh(analysis)
    return analysis


def compute_flywheel_metrics(db: Session) -> FlywheelMetricsResponse:
    """
    Calculates operational health and active learning flywheel statistics.
    """
    total = db.query(Analysis).count()
    verified = db.query(Analysis).filter(Analysis.ground_truth_dx.isnot(None)).count()
    biopsy_proven = db.query(Analysis).filter(Analysis.biopsy_proven == True).count()
    unverified_queue = total - verified

    # Calculate concordance rate on verified specimens
    verified_records = db.query(Analysis).filter(Analysis.ground_truth_dx.isnot(None)).all()
    concordant = 0
    for rec in verified_records:
        ai_is_cancer = (rec.prediction.lower() == "cancer")
        gt_is_cancer = (rec.ground_truth_dx in ("OSCC_MALIGNANT", "HIGH_GRADE_DYSPLASIA"))
        if ai_is_cancer == gt_is_cancer:
            concordant += 1

    concordance_rate = (concordant / max(verified, 1)) if verified > 0 else 1.0
    maturation_pct = min(100.0, (verified / max(total, 1)) * 100.0) if total > 0 else 0.0

    return FlywheelMetricsResponse(
        total_screenings=total,
        verified_count=verified,
        biopsy_proven_count=biopsy_proven,
        unverified_queue_count=unverified_queue,
        concordance_rate=round(concordance_rate, 4),
        flywheel_maturation_pct=round(maturation_pct, 1)
    )
