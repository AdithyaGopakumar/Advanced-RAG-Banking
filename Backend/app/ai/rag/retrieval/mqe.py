"""Multi-query expansion.

The original question is always first. Additional formulations come from the
language model. A missing model, or a response that is not a JSON list,
leaves retrieval with the original question only.
"""

import json
import logging
from typing import Protocol

from app.ai.prompts import MQE_SYSTEM_PROMPT
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider, create_llm_provider
from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


class QueryExpander(Protocol):
    """Produce the search strings for one user question."""

    def expand(self, query: str) -> list[str]:
        """Return the original query, then any extra formulations."""


class OriginalQueryExpander:
    """Search the question as written. Used when no expansion model is configured."""

    def expand(self, query: str) -> list[str]:
        return [query.strip()]


class LLMQueryExpander:
    """Ask the configured chat model for a bounded set of rephrasings."""

    def __init__(self, llm: LLMProvider, *, max_queries: int) -> None:
        self._llm = llm
        self._max_queries = max(1, max_queries)

    def expand(self, query: str) -> list[str]:
        original = query.strip()
        if self._max_queries == 1:
            return [original]
        try:
            raw = self._llm.complete(system=MQE_SYSTEM_PROMPT, user=original)
        except Exception:
            logger.warning("Query expansion failed; searching the original question only")
            return [original]
        return normalize_queries(original, raw, max_queries=self._max_queries)


def create_query_expander(settings: Settings | None = None) -> QueryExpander:
    """Use the chat model when an API key is set, otherwise the original question."""
    current = settings if settings is not None else get_settings()
    if not current.OPENAI_API_KEY.strip():
        return OriginalQueryExpander()
    try:
        llm = create_llm_provider(current)
    except LLMNotConfiguredError:
        logger.warning("Query expansion model is not configured; searching the original question only")
        return OriginalQueryExpander()
    return LLMQueryExpander(llm, max_queries=current.MQE_MAX_QUERIES)


def normalize_queries(original: str, model_output: str, *, max_queries: int) -> list[str]:
    """Keep the original question first, then unique rephrasings up to the cap."""
    first = original.strip()
    queries = [first]
    seen = {first.casefold()}
    for variant in _parse_variants(model_output):
        if len(queries) >= max_queries:
            break
        key = variant.casefold()
        if key in seen:
            continue
        seen.add(key)
        queries.append(variant)
    return queries


def _parse_variants(model_output: str) -> list[str]:
    text = model_output.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Query expansion did not return JSON; searching the original question only")
        return []
    if not isinstance(parsed, list):
        return []
    variants: list[str] = []
    for item in parsed:
        if not isinstance(item, str):
            continue
        cleaned = " ".join(item.split())
        if cleaned:
            variants.append(cleaned)
    return variants
