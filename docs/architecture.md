# Overflow Architecture

Overflow is planned as a middleware layer between applications and AI providers.

```text
Application
    |
    v
Overflow Gateway
    |
    +--> Privacy
    +--> Security
    +--> Policy
    +--> Optimization
    +--> Routing
    +--> Audit
    |
    v
AI Provider / Local Model
```

## Planned components

### Rust core

- PII redaction
- Secret scanning
- Policy evaluation
- Token counting
- Audit hash chain

### Python gateway

- API server
- CLI
- Provider adapters
- Configuration

### Policies

- YAML policy files
- Privacy rules
- Security rules
- Routing rules
- Audit rules
