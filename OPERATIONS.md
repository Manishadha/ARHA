# OPERATIONS

Prereqs
- Python 3.11+, PostgreSQL 15+, OpenSSL.
- .env file present (see .env.example).

Local Run
  python -m venv .venv && source .venv/bin/activate
  pip install -r backend/requirements.txt
  uvicorn backend.main:app --reload
  curl -s http://127.0.0.1:8000/health  # {"status":"ok"}

Database
- App self-creates minimal schema at startup (users, audit_logs).
- Postgres least-privilege user recommended.

CI/CD
- GitHub Actions: spins Postgres service, applies schema, runs lint+security+tests.

Logs
- JSON structured to stdout (request_id included).

Environments
- ENV=production|test (affects logging/behavior if extended).
