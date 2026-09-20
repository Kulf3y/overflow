import re

try:
    from overflow_py import redact_emails as _rust_redact_emails
    NATIVE_AVAILABLE = True
except Exception:
    _rust_redact_emails = None
    NATIVE_AVAILABLE = False

_FALLBACK = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def native_available():
    return NATIVE_AVAILABLE


def native_redact_emails(text):
    if NATIVE_AVAILABLE:
        output, count = _rust_redact_emails(text)
        return output, int(count)

    count = 0

    def repl(_match):
        nonlocal count
        count += 1
        return "[EMAIL_REDACTED]"

    return _FALLBACK.sub(repl, text), count
