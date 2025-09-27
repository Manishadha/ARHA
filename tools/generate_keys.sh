#!/usr/bin/env bash
set -euo pipefail
echo "[ARHA] Generating fresh secrets…"
JWT_SECRET="$(python3 - <<'PY'
import secrets; print(secrets.token_urlsafe(48))
PY
)"
ENCRYPTION_KEY="$(python3 - <<'PY'
import os, base64; print(base64.b64encode(os.urandom(32)).decode())
PY
)"
FILE=".env"
touch "$FILE"
# Update-or-append, then show surrounding context
if grep -q '^JWT_SECRET=' "$FILE"; then
  sed -i "s|^JWT_SECRET=.*$|JWT_SECRET=${JWT_SECRET}|" "$FILE"
else
  echo "JWT_SECRET=${JWT_SECRET}" >> "$FILE"
fi
if grep -q '^ENCRYPTION_KEY=' "$FILE"; then
  sed -i "s|^ENCRYPTION_KEY=.*$|ENCRYPTION_KEY=${ENCRYPTION_KEY}|" "$FILE"
else
  echo "ENCRYPTION_KEY=${ENCRYPTION_KEY}" >> "$FILE"
fi
echo "[ARHA] Keys written. Showing matches:"
grep -nE '^(JWT_SECRET|ENCRYPTION_KEY)=' "$FILE"
echo "[ARHA] Tail of .env:"
tail -n 10 "$FILE"
