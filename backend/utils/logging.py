from loguru import logger
import sys
import uuid
from contextvars import ContextVar
import hashlib
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ProgrammingError

_request_id: ContextVar[str] = ContextVar("request_id", default="-")


def request_id() -> str:
    return _request_id.get()


def set_request_id(value: str | None = None) -> str:
    rid = value or uuid.uuid4().hex
    _request_id.set(rid)
    return rid


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=False,
        diagnose=False,
        format=lambda r: (
            f'{{"ts":"{r["time"].isoformat()}","level":"{r["level"].name}",'
            f'"msg":{r["message"]!r},"request_id":"{request_id()}"}}'
        ),
    )


DDL_AUDIT = """
CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actor TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT,
  hash_chain BYTEA
);
"""


def _hex_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def ensure_audit_table(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(DDL_AUDIT))


def append_audit(
    engine: Engine, *, actor: str, action: str, target: str | None = None
) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    # Fetch previous hash (create table if missing)
    try:
        with engine.begin() as conn:
            prev = conn.execute(
                text("SELECT hash_chain FROM audit_logs ORDER BY id DESC LIMIT 1")
            ).scalar()
    except ProgrammingError:
        ensure_audit_table(engine)
        with engine.begin() as conn:
            prev = conn.execute(
                text("SELECT hash_chain FROM audit_logs ORDER BY id DESC LIMIT 1")
            ).scalar()

    if prev is None:
        prev_hex = ""
    else:
        try:
            prev_hex = prev.tobytes().hex()  # psycopg2 Binary
        except AttributeError:
            try:
                prev_hex = prev.hex()  # memoryview
            except AttributeError:
                prev_hex = str(prev)

    payload = f"{prev_hex}|{ts}|{actor}|{action}|{target or ''}".encode()
    new_hex = _hex_sha256(payload)

    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO audit_logs (ts, actor, action, target, hash_chain) "
                "VALUES (:ts, :actor, :action, :target, decode(:hash_hex,'hex'))"
            ),
            {
                "ts": ts,
                "actor": actor,
                "action": action,
                "target": target,
                "hash_hex": new_hex,
            },
        )
