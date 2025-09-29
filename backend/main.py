from fastapi import FastAPI
from sqlalchemy import create_engine, text
from backend.utils.config import settings
from backend.utils.logging import append_audit


app = FastAPI(title="ARHA API", version="2025.9")
from contextlib import asynccontextmanager

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
    # ensure minimal schema before serving
    with engine.begin() as conn:
        conn.execute(text(DDL_AUDIT))
    yield


# pass lifespan to FastAPI
configure_logging()
app = FastAPI(title="ARHA API", version="2025.9", lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)


@app.on_event("startup")
def ensure_min_schema():
    ddl = """
    CREATE TABLE IF NOT EXISTS audit_logs (
      id BIGSERIAL PRIMARY KEY,
      ts TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      actor TEXT NOT NULL,
      action TEXT NOT NULL,
      target TEXT,
      hash_chain BYTEA
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.post("/audit/ping")
def audit_ping():
    append_audit(engine, actor="system", action="audit_ping", target="/audit/ping")
    return {"status": "logged"}
