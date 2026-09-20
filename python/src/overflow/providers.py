import json
import urllib.request
from dataclasses import dataclass, field

from overflow.config import get_provider_config, mask_secret

PROVIDER_NAMES = ["mock", "openai", "mistral", "ollama", "openai_compatible"]


class ProviderError(Exception):
    pass


@dataclass
class ProviderResult:
    text: str
    provider: str
    model: str
    metadata: dict = field(default_factory=dict)


class MockProvider:
    name = "mock"
    model = "mock-echo"

    def complete(self, text):
        preview = text.strip().replace("\n", " ")
        if len(preview) > 80:
            preview = preview[:80]

        return ProviderResult(
            text=f"mock:{preview}",
            provider=self.name,
            model=self.model,
            metadata={}
        )


class OpenAICompatibleProvider:
    def __init__(self, provider_name="openai_compatible"):
        self.config = get_provider_config(provider_name)
        self.name = self.config.name
        self.model = self.config.model

    def complete(self, text):
        if not self.config.base_url or not self.config.model:
            raise ProviderError(
                f"Provider {self.name} requires base_url and model. "
                "Set OVERFLOW_PROVIDER_BASE_URL and OVERFLOW_PROVIDER_MODEL."
            )

        url = self.config.base_url.rstrip("/") + "/chat/completions"

        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "user", "content": text}
            ]
        }

        headers = {"Content-Type": "application/json"}

        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url, data=data, headers=headers, method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            safe_key = mask_secret(self.config.api_key)
            raise ProviderError(
                f"Provider request failed (key={safe_key}): {exc}"
            ) from exc

        choices = body.get("choices", [])
        if not choices:
            raise ProviderError("Provider returned no choices.")

        message = choices[0].get("message", {})
        content = message.get("content", "")

        return ProviderResult(
            text=content,
            provider=self.name,
            model=self.config.model,
            metadata={"base_url": self.config.base_url}
        )


def get_provider(name):
    if name == "mock":
        return MockProvider()

    if name in ("openai", "mistral", "ollama", "openai_compatible"):
        return OpenAICompatibleProvider(provider_name=name)

    raise ProviderError(f"Unknown provider: {name}")
