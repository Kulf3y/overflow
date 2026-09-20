import re
from dataclasses import dataclass, field

SECRET_PATTERNS = {
    "AWS_ACCESS_KEY": r"\bAKIA[0-9A-Z]{16}\b",
    "GITHUB_TOKEN": r"\bgh[pousr]_[A-Za-z0-9]{20,255}\b",
    "PRIVATE_KEY": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "JWT": r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",
    "BEARER_TOKEN": r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}\b",
    "CONNECTION_STRING": r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s]+\b",
    "GENERIC_API_KEY": r"(?i)\b(?:api[_-]?key|apikey|token)\b\s*[:=]\s*[A-Za-z0-9_\-]{16,}"
}

INJECTION_PATTERNS = [
    r"(?i)ignore (?:all |any )?previous instructions",
    r"(?i)disregard (?:all |any )?previous instructions",
    r"(?i)reveal (?:your |the )?system prompt",
    r"(?i)show (?:your |the )?system prompt",
    r"(?i)output (?:your |the )?system prompt",
    r"(?i)pretend you are (?:unrestricted|unfiltered|jailbroken)",
    r"(?i)act as (?:unrestricted|unfiltered|jailbroken)"
]


@dataclass
class SecurityReport:
    allowed: bool
    findings: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)


def scan_text(text, block_secrets=True, block_prompt_injection=True):
    findings = []
    counts = {}
    reasons = []

    for name, pattern in SECRET_PATTERNS.items():
        compiled = re.compile(pattern)
        matches = list(compiled.finditer(text))

        if matches:
            counts[name] = len(matches)
            findings.append(f"{name}:{len(matches)}")

    injection_matches = 0

    if block_prompt_injection:
        for pattern in INJECTION_PATTERNS:
            compiled = re.compile(pattern)
            matches = list(compiled.finditer(text))

            if matches:
                injection_matches += len(matches)

        if injection_matches > 0:
            counts["PROMPT_INJECTION"] = injection_matches
            findings.append(f"PROMPT_INJECTION:{injection_matches}")
            reasons.append("Possible prompt injection detected.")

    if block_secrets:
        secret_total = 0

        for name in SECRET_PATTERNS:
            secret_total += counts.get(name, 0)

        if secret_total > 0:
            reasons.append("Possible secrets detected.")

    allowed = len(reasons) == 0

    return SecurityReport(
        allowed=allowed,
        findings=findings,
        reasons=reasons,
        counts=counts
    )
