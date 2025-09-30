#!/usr/bin/env python3
import hashlib, sys, psycopg2


def h(s: bytes) -> str:
    return hashlib.sha256(s).hexdigest()


def main(dsn):
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, ts, actor, action, target, encode(hash_chain,'hex') FROM audit_logs ORDER BY id ASC"
    )
    rows = cur.fetchall()
    prev_hex = ""
    ok = True
    for id_, ts, actor, action, target, hex_hash in rows:
        payload = f"{prev_hex}|{ts.isoformat()}|{actor}|{action}|{target or ''}".encode()
        expect = h(payload)
        if expect != hex_hash:
            print(f"FAIL id={id_}: expected {expect}, got {hex_hash}")
            ok = False
            break
        prev_hex = hex_hash
    print("OK" if ok else "FAIL")
    cur.close()
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: verify_audit_chain.py postgresql://user:pass@host:5432/db")
        sys.exit(2)
    main(sys.argv[1])
