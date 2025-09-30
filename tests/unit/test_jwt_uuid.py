from uuid import uuid4

from backend.utils.crypto import create_jwt, decode_jwt


def test_jwt_with_uuid_subject_roundtrip():
    sub = uuid4()
    tok = create_jwt(sub=sub, minutes=1)
    claims = decode_jwt(tok)
    assert claims["sub"] == str(sub)
    assert "exp" in claims and "iat" in claims
