# Overflow Automation

Overflow is designed to support safe automation.

## Planned automation model

```text
GitHub Issue
    |
    v
Qwen bot generates a suggestion
    |
    v
Bot opens a pull request
    |
    v
CI runs tests
    |
    v
Human reviews and merges
```

## Safety rules

- No direct pushes to main.
- No hardcoded secrets.
- All credentials come from environment variables.
- Human review is always required.
- Automation assists developers; it does not replace them.
