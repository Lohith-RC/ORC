from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class ClinicalTriageTier(str, Enum):
    TIER_1_LOW_RISK = "TIER_1_LOW_RISK_OBSERVE"
    TIER_2_INTERMEDIATE = "TIER_2_INTERMEDIATE_14_DAY_RECHECK"
    TIER_3_HIGH_SUSPICION = "TIER_3_HIGH_SUSPICION_URGENT_BIOPSY"

class ClinicalStagingReport(BaseModel):
    triage_tier: ClinicalTriageTier
    triage_tier_display: str
    triage_summary: str
    estimated_diameter_mm: float
    cTNM_estimate: str
    action_checklist: List[str]
    anatomical_risk_factor: str
    recommended_biopsy_type: Optional[str] = None

# High-risk anatomical zones with elevated propensity for occult cervical metastasis
HIGH_RISK_SITES = {"lateral_tongue", "floor_of_mouth", "soft_palate"}

def evaluate_ajcc_staging(
    prediction: str,
    confidence: float,
    lesion_site: str,
    diameter_mm: float,
    clinical_risk_score: float,
    vital_stain_abnormal: bool = False,
    is_cross_polarized: bool = False,
    border_irregularity: float = 1.0
) -> ClinicalStagingReport:
    """
    Evaluates clinical risk using AJCC 8th Edition & WHO Oral Premalignant Lesion criteria.
    Transitions from black-box prediction to actionable clinical decision support.
    """
    is_high_risk_site = lesion_site in HIGH_RISK_SITES
    
    # 1. Estimate Clinical T (cT) staging based on estimated diameter (AJCC 8th Edition)
    if diameter_mm <= 20.0:
        cT_stage = "cT1"
    elif diameter_mm <= 40.0:
        cT_stage = "cT2"
    else:
        cT_stage = "cT3"
        
    cTNM = f"{cT_stage} cN0 cM0 (Presumptive Clinical Stage)"

    # 2. Tier Classification Logic
    # Tier 3 Trigger: High AI suspicion OR high-risk site with elevated habits OR abnormal vital stain
    if (prediction == "cancer" and confidence >= 0.70) or \
       (vital_stain_abnormal and is_high_risk_site) or \
       (is_high_risk_site and clinical_risk_score >= 0.65 and diameter_mm > 15.0):
        tier = ClinicalTriageTier.TIER_3_HIGH_SUSPICION
        display = "Tier 3 // High Suspicion (Immediate Specialist Referral)"
        summary = (
            "Clinical presentation and imaging biomarkers indicate high suspicion for invasive squamous cell carcinoma "
            "or severe epithelial dysplasia. Immediate histopathological biopsy is mandatory."
        )
        checklist = [
            "Issue immediate expedited referral to Oral & Maxillofacial Surgery / Head & Neck Oncology.",
            f"Schedule diagnostic punch or incisional scalpel biopsy targeting the primary lesion margin.",
            "Palpate Level I-III cervical lymph nodes for lymphadenopathy.",
            "Advise immediate, complete cessation of tobacco, alcohol, and areca nut."
        ]
        biopsy_type = "Incisional scalpel or punch biopsy including junctional normal margin"

    # Tier 2 Trigger: Moderate confidence, habit risk factors, intermediate diameter, or uncertain inference
    elif prediction == "uncertain" or \
         (clinical_risk_score >= 0.40) or \
         (is_high_risk_site and diameter_mm > 10.0) or \
         (border_irregularity > 1.4):
        tier = ClinicalTriageTier.TIER_2_INTERMEDIATE
        display = "Tier 2 // Intermediate Risk (14-Day Elimination & Re-check)"
        summary = (
            "Indeterminate mucosal atypical presentation. Potential frictional keratosis, lichenoid reaction, "
            "or early low-grade dysplasia. 14-day observation post-trauma elimination is indicated."
        )
        checklist = [
            "Eliminate local mechanical trauma (sharp cusps, defective restorations, ill-fitting prostheses).",
            "Prescribe topical protective mucosal emollients; avoid spicy or acidic dietary irritants.",
            "Enforce strict 14-day digital photographic re-examination to confirm regression.",
            "If lesion fails to resolve or expands after 14 days, escalate immediately to biopsy."
        ]
        biopsy_type = "Re-evaluation indicated; biopsy if non-resolving at Day 14"

    # Tier 1 Trigger: Low risk, benign appearance, standard anatomical site
    else:
        tier = ClinicalTriageTier.TIER_1_LOW_RISK
        display = "Tier 1 // Low Clinical Risk (Routine Monitoring)"
        summary = (
            "Mucosal architecture exhibits low likelihood of high-grade dysplasia. Consistent with benign reactionary "
            "tissue or physiological pigmentation."
        )
        checklist = [
            "Maintain standard 6-month routine dental and oral mucosal screening interval.",
            "Educate patient on self-examination for oral mucosal changes or non-healing ulcers.",
            "Document baseline oral photographs in patient record."
        ]
        biopsy_type = None

    site_risk_note = "HIGH ONCOLOGICAL RISK ZONE (Rapid occult lymphatic drainage)" if is_high_risk_site else "STANDARD MUCOSAL RISK ZONE"

    return ClinicalStagingReport(
        triage_tier=tier,
        triage_tier_display=display,
        triage_summary=summary,
        estimated_diameter_mm=round(diameter_mm, 1),
        cTNM_estimate=cTNM,
        action_checklist=checklist,
        anatomical_risk_factor=site_risk_note,
        recommended_biopsy_type=biopsy_type
    )
