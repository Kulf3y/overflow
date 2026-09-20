# Overflow Pipeline

The Overflow pipeline connects the main guardrail modules.

Current flow:

```text
Input text
    |
    v
Privacy redaction
    |
    v
Security scan
    |
    v
Policy validation
    |
    v
Token optimization
    |
    v
Provider
    |
    v
Response
```

Current provider:

- MockProvider

The MockProvider allows testing without external API keys.

Future providers:

- Local models
- OpenAI-compatible APIs
- European-hosted providers
- Self-hosted inference servers
