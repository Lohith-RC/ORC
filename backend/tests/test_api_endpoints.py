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
