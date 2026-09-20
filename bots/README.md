# Overflow Bots

This folder contains automation bot foundations.

## Qwen bot

`qwen_bot.py` is a safe skeleton for Qwen-assisted automation.

It is designed to:

- read GitHub issues
- generate safe code suggestions
- open pull requests for human review

Important rules:

- No hardcoded secrets.
- No direct pushes to main.
- Human review is always required.
- No legal compliance guarantees.

## Environment variables

```text
OVERFLOW_QWEN_API_KEY
OVERFLOW_QWEN_BASE_URL
OVERFLOW_QWEN_MODEL
OVERFLOW_GITHUB_TOKEN
```
