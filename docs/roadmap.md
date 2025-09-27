# ARHA Roadmap (Build Order + Quality Gates)

This roadmap is locked to ARHA Blueprint v2. Update progress by checking boxes only; do not change the folder structure.

---

## 0) Ground Rules (Always On)
- [ ] Commit only passing code (no TODOs, no placeholder hints, no emojis).
- [ ] Secrets in `.env` only; never commit `.env`.
- [ ] Each change comes with tests, docs, and security review notes.
- [ ] Code formatted & linted (black/ruff for Python, eslint/prettier for React).
- [ ] Dependency updates reviewed for CVEs.

---

## 1) Environment & Scaffolding
- [ ] Create Python `venv` and install backend deps (`backend/requirements.txt`).
- [ ] Initialize frontend (React/Vite) and baseline deps (`frontend/package.json`).
- [ ] Initialize PostgreSQL locally (Docker or native).
- [ ] Copy `.env.example` → `.env` and fill local values.
- [ ] Verify `docker-compose.yml` starts DB + backend (+ frontend if used).

**Quality Gate A (pass all before proceeding)**
- [ ] `tools/setup_env.sh` provisions clean env on a fresh machine.
- [ ] `pytest -q` runs (even with placeholder tests) with 0 failures.
- [ ] `bandit` and `ruff` pass on backend; `eslint` passes on frontend.

---

## 2) Database Foundation
- [ ] Define minimal schema in `database/init.sql` and `database/models.sql` (users, roles, sessions, logs, alerts, honeytokens).
- [ ] Add migrations in `database/migrations/` (idempotent).
- [ ] Implement backup script `tools/backup_db.sh` and test restore.

**Quality Gate B**
- [ ] Schema review: primary keys, FKs, indexes for auth & audit tables.
- [ ] Encryption at rest strategy documented in `docs/compliance.md`.
- [ ] Backup/restore tested and documented in `docs/handover.md`.

---

## 3) Backend Core (APIs)
- [ ] `backend/api/auth.py`: login, MFA hooks, session issuance.
- [ ] `backend/api/users.py`: RBAC/ABAC endpoints (create/read/update roles).
- [ ] `backend/api/db_protection.py`: parameterized query proxy endpoints.
- [ ] `backend/api/alerts.py`: create/list/acknowledge alerts.
- [ ] `backend/main.py`: app factory, routers, health endpoint.

**Quality Gate C**
- [ ] Unit tests for all endpoints in `tests/unit/`.
- [ ] Integration tests with DB in `tests/integration/`.
- [ ] Negative tests for SQLi/XSS payloads in `tests/security/`.

---

## 4) Security Middleware & Logging
- [ ] `middleware/rate_limiter.py`: per-IP/per-user rate limits.
- [ ] `middleware/cors_headers.py`: strict origins & headers.
- [ ] `middleware/audit_trail.py`: immutable audit entries for all auth & data actions.
- [ ] `utils/logging.py`: structured JSON logs + tamper-evidence (hash chain).
- [ ] `utils/crypto.py`: hashing, AEAD encryption APIs.

**Quality Gate D**
- [ ] Tamper-evident logs validated in tests.
- [ ] Rate limit & CORS covered by tests.
- [ ] Log redaction verified (no secrets in logs).

---

## 5) Detection Services
- [ ] `services/deepfake_detector.py`: interface + deterministic test stub.
- [ ] `services/anomaly_detector.py`: behavior features + baseline model pipeline.
- [ ] `services/rasp.py`: runtime checks on dangerous ops.
- [ ] `services/honeytokens.py`: seeded decoys + alert wiring.

**Quality Gate E**
- [ ] Reproducible model artifacts/versioning documented.
- [ ] False-positive/negative test scenarios in `tests/security/`.
- [ ] Performance baseline tests in `tests/performance/`.

---

## 6) Alerts & Monitoring
- [ ] `api/alerts.py` wired to SMTP (and optional webhook).
- [ ] Alert policies defined (severity, throttle, escalation).
- [ ] Dashboards: counts, recent threats, unresolved alerts.

**Quality Gate F**
- [ ] Alert flood protection tests.
- [ ] End-to-end alert flow verified (trigger → store → notify → ack).

---

## 7) Admin Frontend (Optional but Recommended)
- [ ] Authenticated login page.
- [ ] Dashboard: system health, recent alerts, KPIs.
- [ ] Alerts page: filter, search, acknowledge.
- [ ] Users page: roles, least-privilege management.
- [ ] `frontend/src/i18n/` baseline (en, fr, nl, de) with keys only.

**Quality Gate G**
- [ ] Accessibility pass (basic a11y checks).
- [ ] API error handling and empty states covered.
- [ ] i18n toggles verified; no hard-coded strings.

---

## 8) Compliance & Docs
- [ ] `docs/api_docs.md` complete with request/response examples.
- [ ] `docs/architecture.png` updated from actual implementation.
- [ ] `docs/compliance.md`: GDPR, data retention, encryption, access logs.
- [ ] `security/threat_model.md`: STRIDE/MITRE mapping, mitigations.
- [ ] `security/audit.md`: checklist of what was reviewed and when.

**Quality Gate H**
- [ ] Handover dry-run on a clean machine using only docs & scripts.
- [ ] All scripts in `tools/` are executable and idempotent.
- [ ] CI/CD (in `ci_cd/`) builds, tests, scans, and packages artifacts.

---

## 9) Penetration & Performance
- [ ] `security/pentest_report.md`: internal pen test results and fixes.
- [ ] Load tests in `tests/performance/` with target throughput & latency.
- [ ] Dependency and container scans (SCA) attached to CI/CD.

**Quality Gate I**
- [ ] No HIGH/CRITICAL CVEs in final image.
- [ ] Meets performance SLOs documented in `docs/blueprint.md`.

---

## 10) Final Handover
- [ ] `docs/handover.md` finalized (install, operate, backup/restore, contacts).
- [ ] `.env.example` exhaustive; `.gitignore` verified.
- [ ] Docker images build reproducibly; image digests recorded.
- [ ] Archive created with source, docs, and reproducible build instructions.

**Definition of Done (DoD)**
- All Quality Gates A–I passed.
- Tests: unit, integration, security, performance all green.
- Docs complete and match the final implementation.
- One-time sale terms reiterated in `docs/handover.md`.

---

## Daily Log Template (paste once per day)