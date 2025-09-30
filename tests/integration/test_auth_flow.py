from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_signup_login_me_and_errors():
    email = "cov@example.com"
    pwd = "S3curePass!"
    # signup (ok or already exists)
    r = client.post("/auth/signup", json={"email": email, "password": pwd})
    assert r.status_code in (200, 409)

    # bad login
    r = client.post("/auth/login", json={"email": email, "password": "wrong"})
    assert r.status_code == 401

    # good login
    r = client.post("/auth/login", json={"email": email, "password": pwd})
    assert r.status_code == 200
    token = r.json()["access_token"]

    # me with bad/missing token
    r = client.get("/auth/me")
    assert r.status_code == 401
    r = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401

    # me with valid token
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert "sub" in r.json()
