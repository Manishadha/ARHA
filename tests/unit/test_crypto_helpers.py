from backend.utils.crypto import create_jwt, decode_jwt, hash_password, verify_password


def test_password_hash_and_verify():
    h = hash_password("Secret123!")
    assert h and "$2b$" in h
    assert verify_password("Secret123!", h)
    assert not verify_password("nope", h)


def test_jwt_create_and_decode():
    tok = create_jwt("user-123", ttl_minutes=2)
    claims = decode_jwt(tok)
    assert claims["sub"] == "user-123"
    assert "exp" in claims and "iat" in claims
