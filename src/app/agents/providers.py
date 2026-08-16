from typing import Any

from app.models import WorkflowState


class DeterministicProvider:
    """Offline provider used for reproducible demos and tests."""

    async def complete(self, prompt: str, state: WorkflowState) -> str:
        del state
        return f"Deterministic response for: {prompt[:200]}"


class OpenAIProvider:
    """Optional provider boundary for integrating a hosted LLM."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key
        self.model = model

    async def complete(self, prompt: str, state: WorkflowState) -> str:
        del state
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError(
                "Install the optional 'openai' dependency to use OpenAIProvider"
            ) from exc
        client = AsyncOpenAI(api_key=self.api_key)
        response: Any = await client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""
