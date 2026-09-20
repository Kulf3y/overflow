import re

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


class RedactionReport:
    def __init__(self, output, emails_found):
        self.output = output
        self.emails_found = emails_found


def redact_emails(text):
    count = 0

    def replace(match):
        nonlocal count
        count += 1
        return "[EMAIL_REDACTED]"

    output = EMAIL_PATTERN.sub(replace, text)
    return RedactionReport(output, count)
