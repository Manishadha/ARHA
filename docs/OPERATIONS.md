Prereqs: Python 3.11+, PostgreSQL 15+, OpenSSL.
Env vars: see .env.example.

Local run:
  python -m venv .venv && source .venv/bin/activate
  pip install -r backend/requirements.txt
  uvicorn backend.main:app --reload

DB:
  create role/database (least privilege).
  app auto-creates core tables at startup (users, audit_logs).

CI:
  GitHub Actions spins Postgres service, runs lint/tests, applies schema.

Health:
  GET /health → {"status":"ok"}

Logs: JSON structured to stdout.
