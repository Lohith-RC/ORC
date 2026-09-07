import pytest
from app.schemas.clinical import ClinicalRiskForm
from app.services.clinical_risk import compute_clinical_risk_score

def test_baseline_risk_score():
    form = ClinicalRiskForm(age=25, tobacco_use=False, alcohol_use=False, betel_nut=False, prior_lesions=False)
    assert compute_clinical_risk_score(form) == 0.0

def test_age_scaling():
    form_young = ClinicalRiskForm(age=35)
    form_middle = ClinicalRiskForm(age=45)
    form_elderly = ClinicalRiskForm(age=65)
    
    assert compute_clinical_risk_score(form_young) == 0.0
    assert compute_clinical_risk_score(form_middle) == 0.15
    assert compute_clinical_risk_score(form_elderly) == 0.30

def test_carcinogen_weighting():
    # Tobacco only
    form_tobacco = ClinicalRiskForm(age=25, tobacco_use=True)
    assert compute_clinical_risk_score(form_tobacco) == 0.35

    # Betel nut only
    form_betel = ClinicalRiskForm(age=25, betel_nut=True)
    assert compute_clinical_risk_score(form_betel) == 0.30

    # Tobacco + Alcohol co-carcinogenesis
    form_combo = ClinicalRiskForm(age=25, tobacco_use=True, alcohol_use=True)
    assert compute_clinical_risk_score(form_combo) == 0.55

def test_maximum_risk_score_capped_at_one():
    # Extreme risk profile exceeds 1.0 sum, must clamp to 1.0
    form_extreme = ClinicalRiskForm(
        age=65,             # +0.30
        tobacco_use=True,   # +0.35
        alcohol_use=True,   # +0.20
        betel_nut=True,     # +0.30
        prior_lesions=True  # +0.25
    )
    score = compute_clinical_risk_score(form_extreme)
    assert score == 1.0

def test_invalid_age_validation():
    with pytest.raises(ValueError):
        ClinicalRiskForm(age=3)  # Below min 5
    with pytest.raises(ValueError):
        ClinicalRiskForm(age=125)  # Above max 110
