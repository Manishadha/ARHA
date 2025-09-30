# backend/utils/crypto.py
from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.hash import bcrypt

from . import config as _cfg  # import the module; constants may live here

# Prefer environment, then optional constant on config, then a safe dev default
_JWT_SECRET = os.getenv("JWT_SECRET") or getattr(_cfg, "JWT_SECRET", "dev-secret")
_ALG = "HS256"


def _jsonable_sub(sub: Any) -> str | int:
    """Ensure 'sub' is JSON-serializable (e.g., UUID -> str)."""
    if isinstance(sub, (str, int)):
        return sub
    return str(sub)


def create_jwt(sub: Any, minutes: int = 60, ttl_minutes: int | None = None) -> str:
    """
    Create a signed JWT.
    - sub: subject (user id). UUIDs or other objects are coerced to str.
    - minutes: token lifetime (default 60).
    - ttl_minutes: optional alias for minutes (kept for tests/back-compat).
    """
    if ttl_minutes is not None:
        minutes = ttl_minutes

    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": _jsonable_sub(sub),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm=_ALG)


def decode_jwt(token: str) -> dict[str, Any]:
    """Decode and verify a JWT."""
    return jwt.decode(token, _JWT_SECRET, algorithms=[_ALG])


def hash_password(pwd: str) -> str:
    """Hash a password."""
    return bcrypt.hash(pwd)


def verify_password(pwd: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.verify(pwd, hashed)
