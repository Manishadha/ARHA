Auth: bcrypt password hashes, JWT (HS256).
RBAC: minimal (role stored on users).
Audit: tamper-evident hash chain (sha256(prev|ts|actor|action|target)).

Hardening (buyer to enforce):
  - Change all secrets on day 1.
  - Run DB with SCRAM, local socket or restricted network.
  - mTLS between services (if microservices).
  - WAF in front of API.
  - Fail2ban / rate limiting (middleware included).

Secrets in Git: none. .env ignored.
