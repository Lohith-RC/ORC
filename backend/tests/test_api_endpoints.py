import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model"] == "loaded"
    assert "version" in data

def test_security_headers_present():
    response = client.get("/health")
    assert response.status_code == 200
    headers = response.headers
    assert "x-request-id" in headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"

def test_registration_validation_and_flow():
    unique_user = f"test_{uuid.uuid4().hex[:8]}"
    
    # 1. Reject weak password (<6 chars)
    bad_payload = {
        "username": unique_user,
        "password": "123",
        "email": f"{unique_user}@hospital.org"
    }
    res_bad = client.post("/register", json=bad_payload)
    assert res_bad.status_code == 422

    # 2. Accept valid user
    good_payload = {
        "username": unique_user,
        "password": "StrongPassword!2026",
        "email": f"{unique_user}@hospital.org"
    }
    res_good = client.post("/register", json=good_payload)
    assert res_good.status_code == 201

    # 3. Reject duplicate username
    res_dup = client.post("/register", json=good_payload)
    assert res_dup.status_code == 400
    assert "already registered" in res_dup.json()["detail"]

def test_login_flow():
    unique_user = f"login_{uuid.uuid4().hex[:8]}"
    client.post("/register", json={
        "username": unique_user,
        "password": "ValidPassword123",
        "email": f"{unique_user}@test.com"
    })

    # Correct login
    res_login = client.post("/login", data={"username": unique_user, "password": "ValidPassword123"})
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Wrong password login
    res_fail = client.post("/login", data={"username": unique_user, "password": "WrongPassword"})
    assert res_fail.status_code == 401

def test_predict_multipart_form_data_flow():
    unique_user = f"clinician_{uuid.uuid4().hex[:8]}"
    client.post("/register", json={
        "username": unique_user,
        "password": "ClinicianPassword123!",
        "email": f"{unique_user}@hospital.org"
    })
    token = client.post("/login", data={"username": unique_user, "password": "ClinicianPassword123!"}).json()["access_token"]
    
    # Synthetic test image
    import io
    from PIL import Image
    img = Image.new("RGB", (224, 224), color=(120, 80, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    
    response = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("specimen.jpg", buf, "image/jpeg")},
        data={
            "age": "55",
            "tobacco_use": "true",
            "alcohol_use": "true",
            "betel_nut": "false",
            "prior_lesions": "true"
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "confidence" in result
    assert "clinical_risk_score" in result
    assert result["clinical_risk_score"] > 0.6  # High risk due to age+tobacco+alcohol+lesions
    assert "uncertainty" in result
