import json
import datetime
import pytest
from app.models.analysis import Analysis
from app.services.longitudinal_tracker import (
    compute_longitudinal_delta,
    TrajectoryStatus
)

def test_baseline_initial_when_no_prior():
    current_time = datetime.datetime.utcnow()
    delta = compute_longitudinal_delta(
        current_area_mm2=125.0,
        current_diameter_mm=12.6,
        current_irregularity=1.12,
        current_contour=[(50.0, 50.0), (55.0, 55.0)],
        current_timestamp=current_time,
        prior_analysis=None
    )

    assert delta.has_prior is False
    assert delta.trajectory_status == TrajectoryStatus.BASELINE_INITIAL
    assert delta.elapsed_days == 0.0
    assert delta.delta_surface_area_mm2 is None
    assert delta.growth_velocity_mm2_per_day is None

def test_rapid_expansion_critical_trajectory():
    prior_time = datetime.datetime.utcnow() - datetime.timedelta(days=14)
    current_time = datetime.datetime.utcnow()
    
    prior = Analysis(
        id=101,
        timestamp=prior_time,
        telemetry_data=json.dumps({
            "surface_area_mm2": 100.0,
            "diameter_mm": 11.3,
            "border_irregularity_score": 1.10,
            "contour_points": [(50.0, 50.0)]
        })
    )

    # Current has expanded to 135.0 mm² (+35% expansion in 14 days)
    delta = compute_longitudinal_delta(
        current_area_mm2=135.0,
        current_diameter_mm=13.1,
        current_irregularity=1.48,
        current_contour=[(50.0, 50.0), (60.0, 60.0)],
        current_timestamp=current_time,
        prior_analysis=prior
    )

    assert delta.has_prior is True
    assert delta.trajectory_status == TrajectoryStatus.RAPID_EXPANSION_CRITICAL
    assert delta.delta_surface_area_mm2 == 35.0
    assert delta.percentage_change_area == 35.0
    assert delta.growth_velocity_mm2_per_day >= 2.0
    assert "CRITICAL" in delta.trajectory_status_display

def test_regression_resolving_trajectory():
    prior_time = datetime.datetime.utcnow() - datetime.timedelta(days=20)
    current_time = datetime.datetime.utcnow()
    
    prior = Analysis(
        id=102,
        timestamp=prior_time,
        telemetry_data=json.dumps({
            "surface_area_mm2": 120.0,
            "diameter_mm": 12.4,
            "border_irregularity_score": 1.20,
            "contour_points": []
        })
    )

    # Current contracted to 80.0 mm² (-33.3% reduction)
    delta = compute_longitudinal_delta(
        current_area_mm2=80.0,
        current_diameter_mm=10.1,
        current_irregularity=1.08,
        current_contour=[],
        current_timestamp=current_time,
        prior_analysis=prior
    )

    assert delta.has_prior is True
    assert delta.trajectory_status == TrajectoryStatus.REGRESSION_RESOLVING
    assert delta.delta_surface_area_mm2 < 0
    assert delta.percentage_change_area <= -10.0

def test_stable_persistence_trajectory():
    prior_time = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    current_time = datetime.datetime.utcnow()
    
    prior = Analysis(
        id=103,
        timestamp=prior_time,
        telemetry_data=json.dumps({
            "surface_area_mm2": 100.0,
            "diameter_mm": 11.3,
            "border_irregularity_score": 1.15,
            "contour_points": []
        })
    )

    # Current varies by only +1% (101.0 mm²)
    delta = compute_longitudinal_delta(
        current_area_mm2=101.0,
        current_diameter_mm=11.3,
        current_irregularity=1.16,
        current_contour=[],
        current_timestamp=current_time,
        prior_analysis=prior
    )

    assert delta.has_prior is True
    assert delta.trajectory_status == TrajectoryStatus.STABLE_PERSISTENCE
    assert -5.0 <= delta.percentage_change_area <= 5.0

def test_indolent_expansion_trajectory():
    prior_time = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    current_time = datetime.datetime.utcnow()
    
    prior = Analysis(
        id=104,
        timestamp=prior_time,
        telemetry_data=json.dumps({
            "surface_area_mm2": 100.0,
            "diameter_mm": 11.3,
            "border_irregularity_score": 1.15,
            "contour_points": []
        })
    )

    # Current expanded by +10% (110.0 mm²) over 30 days (velocity ~0.33 mm²/day < 0.40)
    delta = compute_longitudinal_delta(
        current_area_mm2=110.0,
        current_diameter_mm=11.8,
        current_irregularity=1.20,
        current_contour=[],
        current_timestamp=current_time,
        prior_analysis=prior
    )

    assert delta.has_prior is True
    assert delta.trajectory_status == TrajectoryStatus.INDOLENT_EXPANSION

def test_predict_longitudinal_endpoint_flow():
    from fastapi.testclient import TestClient
    from main import app
    import io
    import uuid
    from PIL import Image

    client = TestClient(app)
    uid = uuid.uuid4().hex[:6]
    username = f"long_doc_{uid}"
    pwd = "DocPassword123!"

    # 1. Register & Login
    reg = client.post("/register", json={"username": username, "password": pwd, "email": f"{username}@test.org"})
    assert reg.status_code == 201
    login = client.post("/login", data={"username": username, "password": pwd})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    patient_id = f"PT-{uuid.uuid4().hex[:4].upper()}"

    # 2. Visit 1 (Baseline)
    img1 = Image.new("RGB", (224, 224), color=(130, 90, 90))
    buf1 = io.BytesIO()
    img1.save(buf1, format="JPEG")
    buf1.seek(0)

    res1 = client.post(
        "/predict",
        headers=headers,
        files={"file": ("v1.jpg", buf1, "image/jpeg")},
        data={
            "patient_identifier": patient_id,
            "lesion_site": "lateral_tongue",
            "age": "48"
        }
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["patient_identifier"] == patient_id
    assert data1["longitudinal_trajectory"]["has_prior"] is False
    assert data1["longitudinal_trajectory"]["trajectory_status"] == "BASELINE_INITIAL"

    # 3. Visit 2 (Serial follow-up)
    img2 = Image.new("RGB", (224, 224), color=(170, 60, 60))
    buf2 = io.BytesIO()
    img2.save(buf2, format="JPEG")
    buf2.seek(0)

    res2 = client.post(
        "/predict",
        headers=headers,
        files={"file": ("v2.jpg", buf2, "image/jpeg")},
        data={
            "patient_identifier": patient_id,
            "lesion_site": "lateral_tongue",
            "age": "48"
        }
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["patient_identifier"] == patient_id
    assert data2["longitudinal_trajectory"]["has_prior"] is True
    assert data2["longitudinal_trajectory"]["prior_analysis_id"] == data1["id"]

    # 4. Query Serial History Route
    hist = client.get(f"/analyses/longitudinal/{patient_id}", headers=headers)
    assert hist.status_code == 200
    hdata = hist.json()
    assert hdata["patient_identifier"] == patient_id
    assert hdata["total_encounters"] == 2
    assert len(hdata["timeline"]) == 2

