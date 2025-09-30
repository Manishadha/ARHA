# Release Notes — v1.0.0

- FastAPI backend with /health, /auth/*, /audit/ping
- Tamper-evident audit chain + verifier tool
- CI: ruff, black, bandit, pytest with Postgres service
- Startup lifespan creates users + audit_logs if missing
