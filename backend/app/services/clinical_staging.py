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
        cT_stage = "cT1 (Small spot ≤20mm)"
    elif diameter_mm <= 40.0:
        cT_stage = "cT2 (Medium spot 20-40mm)"
    else:
        cT_stage = "cT3 (Large spot >40mm)"
        
    cTNM = f"{cT_stage} - No spread detected"

    # 2. Tier Classification Logic
    # Tier 3 Trigger: High AI suspicion OR high-risk site with elevated habits OR abnormal vital stain
    if (prediction == "cancer" and confidence >= 0.70) or \
       (vital_stain_abnormal and is_high_risk_site) or \
       (is_high_risk_site and clinical_risk_score >= 0.65 and diameter_mm > 15.0):
        tier = ClinicalTriageTier.TIER_3_HIGH_SUSPICION
        display = "Tier 3: High Risk (See an Oral Specialist Promptly)"
        summary = (
            "The scan detected visual signs that require professional medical evaluation. "
            "Please schedule an in-person appointment with an oral surgeon or specialist doctor promptly."
        )
        checklist = [
            "Schedule an appointment with an oral surgeon or ear, nose & throat (ENT) specialist.",
            "Avoid all tobacco, smoking, betel nut, and alcohol immediately.",
            "Have a doctor perform an in-person clinical examination and biopsy if recommended.",
            "Bring this screening summary to your appointment."
        ]
        biopsy_type = "Specialist examination & biopsy recommended"

    # Tier 2 Trigger: Moderate confidence, habit risk factors, intermediate diameter, or uncertain inference
    elif prediction == "uncertain" or \
         (clinical_risk_score >= 0.40) or \
         (is_high_risk_site and diameter_mm > 10.0) or \
         (border_irregularity > 1.4):
        tier = ClinicalTriageTier.TIER_2_INTERMEDIATE
        display = "Tier 2: Medium Risk (Follow-up Check in 14 Days)"
        summary = (
            "Mild surface changes or irritation detected (such as a sore, friction, or inflammation). "
            "A follow-up dental checkup in 14 days is recommended to confirm it is healing."
        )
        checklist = [
            "Avoid spicy, acidic, or sharp foods that could irritate the spot.",
            "Avoid smoking, tobacco, and alcohol to allow tissue to heal.",
            "Schedule a re-check with your dentist in 14 days to see if the area resolved.",
            "If the spot does not heal or grows larger after 14 days, see a doctor for further evaluation."
        ]
        biopsy_type = "Dental follow-up check in 14 days; biopsy if not resolved"

    # Tier 1 Trigger: Low risk, benign appearance, standard anatomical site
    else:
        tier = ClinicalTriageTier.TIER_1_LOW_RISK
        display = "Tier 1: Low Risk (Healthy Tissue / Routine Care)"
        summary = (
            "The oral tissue appears healthy and normal with low risk of concern. "
            "Continue your regular dental visits every 6 months."
        )
        checklist = [
            "Continue regular dental checkups every 6 months.",
            "Maintain daily oral brushing and cleaning habits.",
            "Check your mouth monthly and see a dentist if any sore lasts longer than 2 weeks."
        ]
        biopsy_type = None

    site_risk_note = "High attention area" if is_high_risk_site else "Standard area"

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
