from sqlalchemy import create_engine, text

from backend.utils.config import settings
from backend.utils.logging import append_audit


def test_append_audit_builds_valid_chain():
    engine = create_engine(settings.database_url(), pool_pre_ping=True)
    # write two linked events
    append_audit(engine, actor="t-user", action="t-action-1", target="t1")
    append_audit(engine, actor="t-user", action="t-action-2", target="t2")

    # verify last two rows form a valid chain link
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
            SELECT id, ts, actor, action, target, encode(hash_chain,'hex') AS hx
            FROM audit_logs ORDER BY id DESC LIMIT 2
        """
            )
        ).fetchall()
    assert len(rows) >= 2
    # recompute the expected hash of the newest row using the previous row's hash
    (id_new, ts_new, a_new, act_new, tgt_new, hx_new) = rows[0]
    (id_prev, ts_prev, a_prev, act_prev, tgt_prev, hx_prev) = rows[1]
    from hashlib import sha256

    ts_iso = ts_new.astimezone(__import__("datetime").timezone.utc).isoformat()
    payload = f"{hx_prev}|{ts_iso}|{a_new}|{act_new}|{tgt_new or ''}".encode()
    expect = sha256(payload).hexdigest()
    assert expect == hx_new
