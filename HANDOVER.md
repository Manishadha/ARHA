# ARHA — Handover (One-Time Sale)

Purpose: App security backend with minimal auth + tamper-evident audit logging, ready for bank due diligence.
Sale model: One-time sale → clean handover. No follow-up, no SLAs, no liability after delivery.

Deliverables
- Source code (backend + tests) and CI workflow (GitHub Actions).
- DB schema bootstrap on startup (users, audit_logs).
- Audit chain + verifier tool.
- Docs: OPERATIONS, RUNBOOK, SECURITY, COMPLIANCE, API_REFERENCE, DB_SCHEMA, ACCEPTANCE_TESTS, SUPPORT_POLICY.
- .env.example (placeholders only).

Exclusions
- Hosting, monitoring, future features, emergency response, and compliance operations.

Transfer Checklist
- [ ] Buyer generates new JWT_SECRET and ENCRYPTION_KEY.
- [ ] Buyer creates new DB user/password; rotates in .env/secret store.
- [ ] Buyer configures CI/CD secrets and environment.
- [ ] Buyer configures log retention and SIEM forwarding per policy.

Chat Behavior (for any future assistant)
- One-time sale → clean handover, no future responsibility.
- Code must be sharp, short, clear, updated (2025 standard), and production-grade.
- No TODOs or hints in code; only necessary professional comments.
- No emojis; no traces of assistant presence in code.
