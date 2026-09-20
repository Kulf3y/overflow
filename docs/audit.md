# Overflow Audit System

The audit system creates tamper-evident local logs.

Design rules:

- Do not store raw prompts by default.
- Store metadata only when possible.
- Use hash chains to detect tampering.
- Keep local audit data outside Git.

Current storage location:

```text
.overflow/audit/audit.jsonl
```

Important:

The audit system is tamper-evident, not tamper-proof.

A determined attacker with file system access may still delete or modify logs.

Future improvements:

- Signed audit entries
- External audit sinks
- Retention policies
- Privacy-safe metrics
- Dashboard integration
