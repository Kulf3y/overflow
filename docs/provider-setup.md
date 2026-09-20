# Connecting Your Own AI Model

Overflow lets each user connect their own AI model securely via API key.

## Setup

1. Copy the example config:

```powershell
copy .env.example .env
```

2. Edit `.env` and set your provider and API key.

## Examples

### OpenAI
```
OVERFLOW_PROVIDER=openai
OVERFLOW_PROVIDER_API_KEY=sk-your-key-here
OVERFLOW_PROVIDER_MODEL=gpt-4o-mini
```

### Mistral
```
OVERFLOW_PROVIDER=mistral
OVERFLOW_PROVIDER_API_KEY=your-mistral-key
OVERFLOW_PROVIDER_MODEL=mistral-small-latest
```

### Ollama (local, no key needed)
```
OVERFLOW_PROVIDER=ollama
OVERFLOW_PROVIDER_MODEL=llama3.2
```

### Any OpenAI-compatible API
```
OVERFLOW_PROVIDER=openai_compatible
OVERFLOW_PROVIDER_BASE_URL=https://your-api.example.com/v1
OVERFLOW_PROVIDER_API_KEY=your-key
OVERFLOW_PROVIDER_MODEL=your-model
```

## Security rules

- API keys are read from environment variables only.
- The `.env` file is ignored by Git.
- Keys are never logged (they are masked in errors).
- Never hardcode keys in source code.
