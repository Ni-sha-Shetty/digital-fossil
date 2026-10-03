import pytest
from app.auth.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing_and_verification():
    pw = "SecretForensicPassword123"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_flow():
    payload = {"sub": "investigator@digitalfossil.local", "role": "investigator"}
    token = create_access_token(payload)
    assert isinstance(token, str)
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "investigator@digitalfossil.local"
    assert decoded["role"] == "investigator"

def test_jwt_invalid_token():
    assert decode_access_token("corrupted.jwt.token") is None
