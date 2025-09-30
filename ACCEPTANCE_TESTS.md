# ACCEPTANCE TESTS

1) Install
- python -m venv .venv && source .venv/bin/activate
- pip install -r backend/requirements.txt

2) Configure
- Copy .env.example → .env; set DB_* and JWT_SECRET/ENCRYPTION_KEY.

3) Start
- uvicorn backend.main:app --reload
- GET /health → {"status":"ok"}

4) Auth flow
- POST /auth/signup → 200/409
- POST /auth/login → 200 returns token
- GET /auth/me with Bearer token → 200 {"sub": ...}

5) Audit
- POST /audit/ping → 200 {"status":"logged"}
- Run: ./tools/verify_audit_chain.py "postgresql://user:pass@127.0.0.1:5432/arha_db" → OK

6) CI
- Push to main → Actions runs lint+tests; expect green.
