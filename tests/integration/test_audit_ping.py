from fastapi.testclient import TestClient
from backend.main import app


def test_audit_ping_writes_row():
    client = TestClient(app)
    r = client.post("/audit/ping")
    assert r.status_code == 200
    assert r.json().get("status") == "logged"
