# Overflow Providers

Overflow supports provider abstraction.

Current providers:

- `mock`
- `openai_compatible`

The `mock` provider is used for testing and does not call an external API.

The `openai_compatible` provider can connect to an OpenAI-compatible API.

Environment variables for `openai_compatible`:

```text
OVERFLOW_PROVIDER_BASE_URL
OVERFLOW_PROVIDER_API_KEY
OVERFLOW_PROVIDER_MODEL
```

Important:

External providers are blocked unless a policy explicitly allows them.

Example policy setting:

```json
{
  "routing": {
    "allow_external_providers": true
  }
```
