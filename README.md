# Overflow

Overflow is an open-source AI governance and optimization middleware.

It sits between applications and AI providers to help control privacy,
security, cost, routing, and auditability.

## Core capabilities

- Privacy-first request handling
- PII and secret redaction
- Prompt injection detection
- Policy-driven governance
- Token and cost optimization
- Provider abstraction and routing
- Tamper-evident audit logging
- Local HTTP gateway and dashboard
- Docker deployment

## Quick start

Run the gateway and dashboard:

```powershell
powershell -File scripts\open_dashboard.ps1
```

Then open:

```text
http://127.0.0.1:8080/dashboard
```

## Documentation

- [Architecture](docs/architecture.md)
- [Pipeline](docs/pipeline.md)
- [Privacy engine](docs/privacy.md)
- [Security engine](docs/security-engine.md)
- [Audit system](docs/audit.md)
- [Providers](docs/providers.md)
- [Dashboard](docs/dashboard.md)
- [Deployment](docs/deployment.md)
- [Automation](docs/automation.md)
- [Project status](docs/project-status.md)

## Status

Early development.

## Security

See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Legal disclaimer

Overflow is a technical tool and does not provide legal advice.

See [LEGAL.md](LEGAL.md).
