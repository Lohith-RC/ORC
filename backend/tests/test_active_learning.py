"""
Unit and Integration Tests for Milestone 3:
Active Learning Data Flywheel & Clinician Ground Truth Verification.
"""

import uuid
import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.analysis import Analysis
from app.models.user import User
from app.services.active_learning import (
    compute_acquisition_priority,
    submit_clinician_verification,
    compute_flywheel_metrics
)
from app.schemas.analysis import ClinicianVerificationRequest
from app.db.session import SessionLocal

client = TestClient(app)


def test_acquisition_priority_uncertainty_weighting():
    # Synthetic analysis with high epistemic uncertainty (0.22)
    high_u = Analysis(
        confidence=0.85,
        uncertainty=0.22,
        risk_score=0.30,
        triage_tier="Tier 2 // Intermediate Risk"
    )
    score, reason = compute_acquisition_priority(high_u)
    assert score > 0.50
    assert "High Model Uncertainty" in reason


def test_acquisition_priority_discordance_weighting():
    # Discordant: 95% AI confidence for cancer, but 0.05 clinical risk (patient young, non-smoker)
    discordant = Analysis(
        confidence=0.95,
        uncertainty=0.04,
        risk_score=0.05,
        triage_tier="Tier 1 // Low Risk"
    )
    score, reason = compute_acquisition_priority(discordant)
    assert "Discordant Vision/Risk Profile" in reason


def test_acquisition_priority_tier3_urgency():
    # Tier 3 high suspicion case
    tier3 = Analysis(
        confidence=0.92,
        uncertainty=0.10,
        risk_score=0.85,
        triage_tier="Tier 3 // High Suspicion (Urgent Biopsy Referral)"
    )
    score, reason = compute_acquisition_priority(tier3)
    assert "Tier 3 High Oncology Suspicion" in reason


def test_active_learning_and_verification_api_flow():
    uid = uuid.uuid4().hex[:6]
    username = f"pathologist_{uid}"
    pwd = "PathoPassword123!"

    # 1. Register & Login Clinician
    reg = client.post("/register", json={"username": username, "password": pwd, "email": f"{username}@pathology.org"})
    assert reg.status_code == 201
    login = client.post("/login", data={"username": username, "password": pwd})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Insert test unverified analysis directly into DB
    db = SessionLocal()
    clinician = db.query(User).filter(User.username == username).first()
    assert clinician is not None
    
    test_analysis = Analysis(
        user_id=clinician.id,
        patient_identifier=f"PT-VERIFY-{uid}",
        prediction="cancer",
        confidence=0.91,
        uncertainty=0.19,
        risk_score=0.25,
        image_quality_score=150.0,
        lesion_site="lateral_tongue",
        triage_tier="Tier 3 // High Suspicion (Urgent Biopsy Referral)",
        image_filename="test_biopsy.jpg",
        biopsy_proven=False,
        ground_truth_dx=None
    )
    db.add(test_analysis)
    db.commit()
    db.refresh(test_analysis)
    analysis_id = test_analysis.id
    db.close()

    # 3. Query Active Learning Queue via API
    queue_res = client.get("/analyses/active-learning/queue", headers=headers)
    assert queue_res.status_code == 200
    queue = queue_res.json()
    assert isinstance(queue, list)
    target_items = [q for q in queue if q["analysis_id"] == analysis_id]
    assert len(target_items) == 1
    assert target_items[0]["priority_score"] > 0.40

    # 4. Submit Clinician Verification (Biopsy-Proven OSCC, Grade 2)
    verify_payload = {
        "ground_truth_dx": "OSCC_MALIGNANT",
        "biopsy_proven": True,
        "histology_grade": "MODERATELY_DIFFERENTIATED",
        "clinician_feedback_notes": "Histopathological confirmation received: Infiltrating squamous cell carcinoma with keratin pearls.",
        "annotated_contour": "[[10, 20], [15, 25], [20, 20]]"
    }
    verify_res = client.post(f"/analyses/{analysis_id}/verify", json=verify_payload, headers=headers)
    assert verify_res.status_code == 200
    vdata = verify_res.json()
    assert vdata["biopsy_proven"] is True
    assert vdata["ground_truth_dx"] == "OSCC_MALIGNANT"
    assert vdata["histology_grade"] == "MODERATELY_DIFFERENTIATED"
    assert "Infiltrating squamous cell carcinoma" in vdata["clinician_feedback_notes"]

    # 5. Verify Flywheel Metrics Endpoint
    metrics_res = client.get("/analyses/active-learning/metrics", headers=headers)
    assert metrics_res.status_code == 200
    mdata = metrics_res.json()
    assert mdata["verified_count"] >= 1
    assert mdata["biopsy_proven_count"] >= 1
    assert 0.0 <= mdata["concordance_rate"] <= 1.0
    assert 0.0 <= mdata["flywheel_maturation_pct"] <= 100.0
