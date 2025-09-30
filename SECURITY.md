# SECURITY

Auth
- Passwords hashed with bcrypt (passlib).
- JWT (HS256) with exp/iat; secret in env/secret store.

Data
- Parameterized queries only; least privilege DB role.

Audit
- Tamper-evident chain: sha256(prev|ts(UTC ISO)|actor|action|target) stored as BYTEA.
- Verifier tool recomputes and asserts continuity.

Hardening (Buyer)
- Rotate all secrets on Day 1.
- Enforce SCRAM on Postgres; restrict network.
- WAF / rate limiting in front of the API.
- Centralize logs to SIEM; define retention.

Secrets
- No secrets in repo. .env is git-ignored.
