import json
import os
import urllib.request
from dataclasses import dataclass, field

PROVIDER_NAMES = ["mock", "openai_compatible"]


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
    name = "openai_compatible"

    def __init__(self, base_url=None, api_key=None, model=None):
        self.base_url = base_url or os.environ.get("OVERFLOW_PROVIDER_BASE_URL", "")
        self.api_key = api_key or os.environ.get("OVERFLOW_PROVIDER_API_KEY", "")
        self.model = model or os.environ.get("OVERFLOW_PROVIDER_MODEL", "")

    def complete(self, text):
        if not self.base_url or not self.model:
            raise ProviderError("OpenAI-compatible provider requires base_url and model.")

        url = self.base_url.rstrip("/") + "/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise ProviderError(f"Provider request failed: {exc}") from exc

        choices = body.get("choices", [])

        if not choices:
            raise ProviderError("Provider returned no choices.")

        message = choices[0].get("message", {})
        content = message.get("content", "")

        return ProviderResult(
            text=content,
            provider=self.name,
            model=self.model,
            metadata={
                "base_url": self.base_url
            }
        )


def get_provider(name):
    if name == "mock":
        return MockProvider()

    if name == "openai_compatible":
        return OpenAICompatibleProvider()

    raise ProviderError(f"Unknown provider: {name}")
