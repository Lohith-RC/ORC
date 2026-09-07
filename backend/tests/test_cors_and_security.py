import pytest
from app.core.config import settings

def test_security_headers_enforced(client):
    response = client.get("/health")
    assert response.status_code == 200
    headers = response.headers

    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-xss-protection") == "1; mode=block"
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert "content-security-policy" in headers
    assert "frame-ancestors 'none'" in headers["content-security-policy"]

def test_cache_control_headers_on_sensitive_endpoints(client, auth_headers):
    response = client.get("/api/v1/history", headers=auth_headers)
    assert "no-store" in response.headers.get("cache-control", "")

def test_cors_preflight_allowed_origin(client):
    allowed = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost:3000"
    headers = {
        "Origin": allowed,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type,Authorization"
    }
    response = client.options("/predict", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == allowed

def test_cors_disallowed_origin(client):
    headers = {
        "Origin": "https://malicious-phishing-site.example.com",
        "Access-Control-Request-Method": "POST",
    }
    response = client.options("/predict", headers=headers)
    # Disallowed origin should NOT be echoed back as access-control-allow-origin
    assert response.headers.get("access-control-allow-origin") != "https://malicious-phishing-site.example.com"
