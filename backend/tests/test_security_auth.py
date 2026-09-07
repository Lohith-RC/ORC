import datetime
from jose import jwt
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

def test_password_hashing_and_verification():
    raw = "StrongClinicalPassword#2026"
    hashed = get_password_hash(raw)
    
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False

def test_password_salt_uniqueness():
    raw = "SamePassword"
    hash1 = get_password_hash(raw)
    hash2 = get_password_hash(raw)
    # Even with identical inputs, cryptographic salts must differ
    assert hash1 != hash2
    assert verify_password(raw, hash1) is True
    assert verify_password(raw, hash2) is True

def test_jwt_token_issuance_and_decoding():
    token = create_access_token(data={"sub": "dr_smith", "role": "clinician"})
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert payload["sub"] == "dr_smith"
    assert payload["role"] == "clinician"
    assert "exp" in payload

def test_expired_jwt_token_fails():
    # Issue a token that expired 10 minutes ago
    past_delta = datetime.timedelta(minutes=-10)
    token = create_access_token(data={"sub": "expired_user"}, expires_delta=past_delta)
    
    import pytest
    from jose import JWTError
    with pytest.raises(JWTError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
