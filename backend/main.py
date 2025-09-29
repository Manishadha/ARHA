from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy import create_engine, text

from backend.middleware.audit_trail import RequestContextMiddleware
from backend.utils.config import settings
from backend.utils.logging import configure_logging, append_audit

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

engine = create_engine(settings.database_url(), pool_pre_ping=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure minimal schema before serving any requests
    with engine.begin() as conn:
        conn.execute(text(DDL_AUDIT))
    yield


configure_logging()
app = FastAPI(title="ARHA API", version="2025.9", lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.post("/audit/ping")
def audit_ping():
    append_audit(engine, actor="system", action="audit_ping", target="/audit/ping")
    return {"status": "logged"}


@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception")
    return JSONResponse(status_code=500, content={"detail": "internal_error"})
