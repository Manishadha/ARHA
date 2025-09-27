# ARHA Daily Log

# Append a fresh daily block 26/09/2025 (Ubuntu)
Date: 2025-09-26
Progress:
- [x] Project folder tree created and placeholder files added
- [x] docs/roadmap.md created and committed
- [x] docs/daily_log.md created and initial entry appended
- [ ] backend/requirements.txt populated
- [ ] tools/setup_env.sh: draft started

Risks/Decisions:
- Risk: I am solo on the backend AI modules; consider hiring/partner for deepfake model later.
- Decision: Use GitHub Actions for CI initially; GitLab CI kept as backup.

Checks:
- Tests green?  no (no tests yet)
- Lint/format?  partial (black not run yet)
- CVE scan?     not run
Notes:
- Next: activate venv and install initial backend deps, add .env with local values (do not commit .env).

Date: 2025-09-26
Progress:
- [x] Generated fresh JWT and encryption keys into .env
- [x] Secured .env permissions
- [x] Created least-privilege DB user arha_app and arha_db
- [x] Applied initial schema

Checks:
- Tests green?  yes (sanity)
- Lint/format?  pending
- CVE scan?     pending

