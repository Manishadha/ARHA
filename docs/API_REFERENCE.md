# API REFERENCE

GET /health
- 200 {"status":"ok"}

POST /audit/ping
- 200 {"status":"logged"}

POST /auth/signup
- Body: { "email": "user@example.com", "password": "..." }
- 200 { "id": "<uuid>", "email": "..." } or 409 email_exists

POST /auth/login
- Body: { "email": "user@example.com", "password": "..." }
- 200 { "access_token": "<jwt>", "token_type": "bearer" }
- 401 invalid_credentials

GET /auth/me
- Header: Authorization: Bearer <token>
- 200 { "sub": "<user_id>" } | 401 missing_token|invalid_token
