from starlette.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_me_without_token_is_unauthorized():
    r = client.get("/auth/me")  # no Authorization header
    assert r.status_code == 401


def test_me_with_bad_token_is_unauthorized():
    r = client.get("/auth/me", headers={"Authorization": "Bearer not.a.jwt"})
    assert r.status_code == 401
