import re
from dataclasses import dataclass

WHITESPACE_PATTERN = re.compile(r"\s+")


def estimate_tokens(text):
    if not text:
        return 0

    return max(1, len(text) // 4)


def compact_lines(text):
    lines = []

    for line in text.splitlines():
        compact = WHITESPACE_PATTERN.sub(" ", line).strip()

        if compact:
            lines.append(compact)

    return "\n".join(lines)


def remove_duplicate_lines(text):
    seen = set()
    lines = []

    for line in text.splitlines():
        key = line.strip().lower()

        if key and key in seen:
            continue

        if key:
            seen.add(key)

        lines.append(line.strip())

    return "\n".join(lines)


@dataclass
class OptimizationReport:
    output: str
    original_tokens: int
    optimized_tokens: int
    reduction_percent: float


def optimize_text(text, remove_duplicates=True, max_chars=None):
    original_tokens = estimate_tokens(text)
    output = text

    output = compact_lines(output)

    if remove_duplicates:
        output = remove_duplicate_lines(output)

    if max_chars is not None and len(output) > max_chars:
        output = output[:max_chars]

    optimized_tokens = estimate_tokens(output)

    if original_tokens == 0:
        reduction_percent = 0.0
    else:
        reduction_percent = round((1 - optimized_tokens / original_tokens) * 100, 2)

    return OptimizationReport(
        output=output,
        original_tokens=original_tokens,
        optimized_tokens=optimized_tokens,
        reduction_percent=reduction_percent
    )
