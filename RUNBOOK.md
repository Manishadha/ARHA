# RUNBOOK

Rotate Secrets
- JWT_SECRET / ENCRYPTION_KEY: update secret store and .env; restart API.

DB Password Reset
- sudo -u postgres psql -c "ALTER ROLE <user> WITH PASSWORD '<new>'"
- Update .env DB_PASSWORD; restart API.

Incidents
- 500 errors: check structured logs; verify DB reachability; run /health.
- Audit integrity: run tools/verify_audit_chain.py with DB URL; expect "OK".

Backups
- pg_dump -Fc arha_db > backup.dump
- pg_restore -d arha_db backup.dump

Smoke Checks
- /health 200 OK
- /auth/signup, /auth/login, /auth/me flow works
- /audit/ping inserts row; audit verifier says OK
