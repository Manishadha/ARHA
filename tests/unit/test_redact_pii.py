from backend.middleware.redact_pii import _redact


def test_email_redaction():
    s = "error for alice@example.com and bob.smith@bank.eu"
    r = _redact(s)
    assert "example.com" not in r and "bank.eu" not in r
    assert "[redacted_email]" in r
