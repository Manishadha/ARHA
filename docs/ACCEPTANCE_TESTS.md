1) Setup .env (new keys/password).
2) Start API; /health returns ok.
3) POST /auth/signup + /auth/login + /auth/me works.
4) POST /audit/ping creates a row; verify with SELECT.
5) Run pytest; all green.
