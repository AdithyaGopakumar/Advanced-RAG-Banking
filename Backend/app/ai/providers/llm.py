"""Chat completions used for query expansion and grounded answers."""

from typing import Protocol

from app.core.config import Settings, get_settings


class LLMProvider(Protocol):
    """One completion from a chat model."""

    def complete(self, *, system: str, user: str) -> str:
        """Return the model text for a system prompt and a user message."""


class LLMNotConfiguredError(Exception):
    """A language model was requested without the settings it needs."""


class OpenAIChatProvider:
    """GPT-4o-mini chat completions. The OpenAI client is created on first use."""

    def __init__(self, *, api_key: str, model: str) -> None:
        if not api_key.strip():
            raise LLMNotConfiguredError("Set OPENAI_API_KEY before using the OpenAI chat provider.")
        if not model.strip():
            raise LLMNotConfiguredError("Set LLM_MODEL before using the OpenAI chat provider.")
        self._api_key = api_key.strip()
        self._model = model.strip()
        self._client: object | None = None

    def complete(self, *, system: str, user: str) -> str:
        client = self._openai()
        response = client.chat.completions.create(  # type: ignore[attr-defined]
            model=self._model,
            temperature=0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        content = response.choices[0].message.content
        return content or ""

    def _openai(self) -> object:
        if self._client is not None:
            return self._client
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMNotConfiguredError("openai is not installed") from exc
        self._client = OpenAI(api_key=self._api_key)
        return self._client


def create_llm_provider(settings: Settings | None = None) -> OpenAIChatProvider:
    """Build the development chat model from settings."""
    current = settings if settings is not None else get_settings()
    return OpenAIChatProvider(api_key=current.OPENAI_API_KEY, model=current.LLM_MODEL)
