import re
from dataclasses import dataclass, field

from overflow.native import native_redact_emails

PHONE_PATTERN = re.compile(r"(?<!\d)\+\d[\d\s().-]{7,17}\d(?!\d)")
IBAN_PATTERN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")


@dataclass
class Finding:
    entity_type: str
    replacement: str


@dataclass
class RedactionReport:
    output: str
    findings: list[Finding] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def emails_found(self):
        return self.counts.get("EMAIL", 0)


def _apply_pattern(pattern, text, entity_type, replacement, findings, counts):
    def replace(_match):
        counts[entity_type] = counts.get(entity_type, 0) + 1
        findings.append(Finding(entity_type=entity_type, replacement=replacement))
        return replacement

    return pattern.sub(replace, text)


def redact_text(text, custom_patterns=None):
    findings = []
    counts = {}
    output = text

    output, email_count = native_redact_emails(output)

    if email_count > 0:
        counts["EMAIL"] = email_count
        findings.append(Finding(entity_type="EMAIL", replacement="[EMAIL_REDACTED]"))

    output = _apply_pattern(PHONE_PATTERN, output, "PHONE", "[PHONE_REDACTED]", findings, counts)
    output = _apply_pattern(IBAN_PATTERN, output, "IBAN", "[IBAN_REDACTED]", findings, counts)

    for rule in custom_patterns or []:
        name = str(rule.get("name", "CUSTOM")).upper()
        pattern = rule.get("pattern")

        if not pattern:
            continue

        replacement = rule.get("replacement", f"[CUSTOM_{name}_REDACTED]")
        compiled = re.compile(pattern)
        output = _apply_pattern(compiled, output, name, replacement, findings, counts)

    return RedactionReport(output=output, findings=findings, counts=counts)


def redact_emails(text):
    return redact_text(text)
