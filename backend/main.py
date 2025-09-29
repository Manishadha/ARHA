from fastapi import FastAPI
from sqlalchemy import create_engine, text
from backend.utils.config import settings
from backend.utils.logging import append_audit


app = FastAPI(title="ARHA API", version="2025.9")

engine = create_engine(settings.database_url(), pool_pre_ping=True)


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.post("/audit/ping")
def audit_ping():
    append_audit(engine, actor="system", action="audit_ping", target="/audit/ping")
    return {"status": "logged"}
