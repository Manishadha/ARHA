# DB SCHEMA

users
- id UUID PK
- email TEXT UNIQUE NOT NULL
- password_hash TEXT NOT NULL
- role TEXT NOT NULL
- created_at TIMESTAMPTZ DEFAULT now()

audit_logs
- id BIGSERIAL PK
- ts TIMESTAMPTZ NOT NULL DEFAULT now()
- actor TEXT NOT NULL
- action TEXT NOT NULL
- target TEXT
- hash_chain BYTEA  # sha256(prev|ts(UTC ISO)|actor|action|target) hex→BYTEA

Indexes
- users_email_key on users(email)
