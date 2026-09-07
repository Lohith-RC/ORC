from app.schemas.clinical import ClinicalRiskForm

def compute_clinical_risk_score(form: ClinicalRiskForm) -> float:
    """
    Weighted Epidemiological Clinical Risk Scoring for Oral Squamous Cell Carcinoma (OSCC).
    Scores range from 0.0 (baseline) to 1.0 (maximum clinical risk).
    """
    score = 0.0
    
    # Age factor
    if form.age >= 60:
        score += 0.30
    elif form.age >= 40:
        score += 0.15
        
    # Tobacco is the primary carcinogen for oral mucosal dysplasia
    if form.tobacco_use:
        score += 0.35
        
    # Alcohol acts as a co-carcinogen and permeability enhancer
    if form.alcohol_use:
        score += 0.20
        
    # Betel nut (Areca catechu) with slaked lime is a Grade 1 human carcinogen
    if form.betel_nut:
        score += 0.30
        
    # Prior oral lesions (e.g. leukoplakia, erythroplakia) indicate pre-malignant history
    if form.prior_lesions:
        score += 0.25
        
    return min(round(score, 4), 1.0)
