import io
import os
import uuid
import pytest

# Enforce local SQLite test database isolation before loading app or database engines
os.environ["DATABASE_URL"] = "sqlite:///oralcancer_test.db"
os.environ["SECRET_KEY"] = "ci_cd_test_secret_key_2026"
os.environ["CORS_ORIGINS"] = "http://localhost:3000,http://localhost:8000"

from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """Shared TestClient instance across the test suite."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def unique_username():
    """Generates a guaranteed-unique username for isolated tests."""
    return f"testuser_{uuid.uuid4().hex[:10]}"

@pytest.fixture
def auth_headers(client, unique_username):
    """Registers a user, logs in, and returns valid Authorization headers."""
    password = "StrongTestPassword123!"
    email = f"{unique_username}@hospital.test"
    client.post("/register", json={
        "username": unique_username,
        "password": password,
        "email": email
    })
    res = client.post("/login", data={"username": unique_username, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_oral_image():
    """Creates an in-memory 224x224 synthetic oral mucosa JPEG image."""
    img = Image.new("RGB", (224, 224), color=(180, 70, 70))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf
