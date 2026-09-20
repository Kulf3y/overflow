import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


PROVIDER_DEFAULTS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini"
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "model": "mistral-small-latest"
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2"
    }
}


@dataclass
class ProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str


def get_provider_config(provider_name=None):
    name = provider_name or os.environ.get("OVERFLOW_PROVIDER", "mock")
    defaults = PROVIDER_DEFAULTS.get(name, {})

    return ProviderConfig(
        name=name,
        api_key=os.environ.get("OVERFLOW_PROVIDER_API_KEY", ""),
        base_url=os.environ.get(
            "OVERFLOW_PROVIDER_BASE_URL",
            defaults.get("base_url", "")
        ),
        model=os.environ.get(
            "OVERFLOW_PROVIDER_MODEL",
            defaults.get("model", "")
        )
    )


def mask_secret(value):
    if not value or len(value) < 8:
        return "***"
    return value[:4] + "..." + value[-4:]
