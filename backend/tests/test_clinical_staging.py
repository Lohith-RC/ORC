import pytest
from app.services.clinical_staging import (
    evaluate_ajcc_staging,
    ClinicalTriageTier,
    ClinicalStagingReport
)

def test_tier_1_benign_evaluation():
    report = evaluate_ajcc_staging(
        prediction="non_cancer",
        confidence=0.92,
        lesion_site="buccal_mucosa",
        diameter_mm=8.5,
        clinical_risk_score=0.10,
        vital_stain_abnormal=False,
        border_irregularity=1.05
    )
    assert report.triage_tier == ClinicalTriageTier.TIER_1_LOW_RISK
    assert "cT1" in report.cTNM_estimate
    assert report.recommended_biopsy_type is None
    assert len(report.action_checklist) >= 3

def test_tier_2_intermediate_evaluation():
    # Triggered by uncertainty or moderate risk score
    report = evaluate_ajcc_staging(
        prediction="uncertain",
        confidence=0.55,
        lesion_site="buccal_mucosa",
        diameter_mm=14.0,
        clinical_risk_score=0.45,
        vital_stain_abnormal=False,
        border_irregularity=1.55
    )
    assert report.triage_tier == ClinicalTriageTier.TIER_2_INTERMEDIATE
    assert "14-Day" in report.triage_tier_display
    assert "cT1" in report.cTNM_estimate
    assert len(report.action_checklist) >= 3

def test_tier_3_high_suspicion_cancer_prediction():
    # Triggered by cancer prediction with confidence >= 0.70
    report = evaluate_ajcc_staging(
        prediction="cancer",
        confidence=0.88,
        lesion_site="lateral_tongue",
        diameter_mm=26.0,
        clinical_risk_score=0.70,
        vital_stain_abnormal=True,
        border_irregularity=1.85
    )
    assert report.triage_tier == ClinicalTriageTier.TIER_3_HIGH_SUSPICION
    assert "cT2" in report.cTNM_estimate
    assert report.recommended_biopsy_type is not None
    assert "HIGH ONCOLOGICAL RISK ZONE" in report.anatomical_risk_factor
    assert any("expedited referral" in item.lower() for item in report.action_checklist)

def test_ajcc_ct_staging_diameter_brackets():
    # cT1: <= 20mm
    rep_t1 = evaluate_ajcc_staging("non_cancer", 0.9, "buccal_mucosa", diameter_mm=19.5, clinical_risk_score=0.1)
    assert "cT1" in rep_t1.cTNM_estimate

    # cT2: 20 < d <= 40mm
    rep_t2 = evaluate_ajcc_staging("non_cancer", 0.9, "buccal_mucosa", diameter_mm=35.0, clinical_risk_score=0.1)
    assert "cT2" in rep_t2.cTNM_estimate

    # cT3: > 40mm
    rep_t3 = evaluate_ajcc_staging("non_cancer", 0.9, "buccal_mucosa", diameter_mm=45.0, clinical_risk_score=0.1)
    assert "cT3" in rep_t3.cTNM_estimate
