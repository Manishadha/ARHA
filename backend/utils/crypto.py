from passlib.context import CryptContext
import jwt
import os
import datetime

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
_ALG = "HS256"


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _pwd.verify(password, password_hash)


def create_jwt(sub: str, ttl_minutes: int = 60) -> str:
    now = datetime.datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=ttl_minutes),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm=_ALG)


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, _JWT_SECRET, algorithms=[_ALG])
