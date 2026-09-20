from dataclasses import dataclass, field


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
