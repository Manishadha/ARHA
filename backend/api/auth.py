from uuid import uuid4

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from backend.utils.config import settings
from backend.utils.crypto import create_jwt, hash_password, verify_password
from backend.utils.logging import append_audit

__all__ = ["router"]

router = APIRouter(prefix="/auth", tags=["auth"])
engine: Engine = create_engine(settings.database_url(), pool_pre_ping=True)


class SignupIn(BaseModel):
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(payload: SignupIn):
    uid = str(uuid4())
    ph = hash_password(payload.password)
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO users (id, email, password_hash, role) VALUES (:id, :email, :ph, :role)"
                ),
                {"id": uid, "email": payload.email, "ph": ph, "role": "user"},
            )
        append_audit(engine, actor=payload.email, action="signup", target="users")
        return {"id": uid, "email": payload.email}
    except Exception:
        # duplicate email or other constraint
        raise HTTPException(status_code=409, detail="email_exists") from None


@router.post("/login")
def login(payload: LoginIn):
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT id, password_hash FROM users WHERE email=:e"),
            {"e": payload.email},
        ).fetchone()
    if not row or not verify_password(payload.password, row[1]):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    token = create_jwt(sub=row[0])
    append_audit(engine, actor=payload.email, action="login", target=row[0])
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(authorization: str = Header(default="")):
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing_token")
    token = authorization.split(" ", 1)[1]
    from backend.utils.crypto import decode_jwt

    try:
        claims = decode_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid_token") from None
    return {"sub": claims["sub"]}
