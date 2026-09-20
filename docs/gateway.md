# Overflow Gateway

Overflow includes a lightweight local HTTP gateway.

The current implementation uses the Python standard library only.

A FastAPI version may be added later.

## Default binding

The gateway binds to:

```text
http://127.0.0.1:8080
```

This keeps it local by default.

## Endpoints

### GET /v1/health

Returns gateway health.

### POST /v1/check

Checks text for privacy-sensitive data.

Example body:

```json
{
  "text": "contact jane@example.com"
}
```

### POST /v1/security

Checks text for security risks.

Example body:

```json
{
  "text": "Ignore previous instructions"
}
```

### POST /v1/policy/validate

Validates a policy object.

Example body:

```json
{
  "policy": {
    "privacy": {
      "redact_pii": true
    }
  }
}
```
