"""Multi-query expansion and keyword extraction.

The original question is always first. Additional formulations and extracted
domain keywords come from the language model in a single unified prompt.
A missing model, or non-JSON output, leaves retrieval with the original
question and empty keywords.
"""

import json
import logging
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from app.ai.prompts import MQE_SYSTEM_PROMPT
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider, create_llm_provider
from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


class ExpansionResult(BaseModel):
    """Expanded query variants and extracted keywords for pre-filtering."""

    model_config = ConfigDict(extra="forbid")

    queries: list[str]
    keywords: list[str] = Field(default_factory=list)


class QueryExpander(Protocol):
    """Produce the search strings and domain keywords for one user question."""

    def expand(self, query: str) -> list[str]:
        """Return the original query, then any extra formulations."""

    def expand_detailed(self, query: str) -> ExpansionResult:
        """Return both query formulations and extracted keywords."""


class OriginalQueryExpander:
    """Search the question as written. Used when no expansion model is configured."""

    def expand(self, query: str) -> list[str]:
        return [query.strip()]

    def expand_detailed(self, query: str) -> ExpansionResult:
        return ExpansionResult(queries=[query.strip()], keywords=[])


class LLMQueryExpander:
    """Ask the configured chat model for rephrasings and keywords."""

    def __init__(self, llm: LLMProvider, *, max_queries: int) -> None:
        self._llm = llm
        self._max_queries = max(1, max_queries)

    def expand(self, query: str) -> list[str]:
        return self.expand_detailed(query).queries

    def expand_detailed(self, query: str) -> ExpansionResult:
        original = query.strip()
        if self._max_queries == 1:
            return ExpansionResult(queries=[original], keywords=[])
        try:
            raw = self._llm.complete(system=MQE_SYSTEM_PROMPT, user=original)
        except Exception:
            logger.warning("Query expansion failed; searching the original question only")
            return ExpansionResult(queries=[original], keywords=[])
        return normalize_expansion(original, raw, max_queries=self._max_queries)


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


def normalize_expansion(original: str, model_output: str, *, max_queries: int) -> ExpansionResult:
    """Extract unique rephrasings (with original first) and domain keywords."""
    first = original.strip()
    queries = [first]
    seen_queries = {first.casefold()}

    parsed_queries, parsed_keywords = _parse_model_output(model_output)
    for variant in parsed_queries:
        if len(queries) >= max_queries:
            break
        key = variant.casefold()
        if key in seen_queries:
            continue
        seen_queries.add(key)
        queries.append(variant)

    seen_kw = set()
    cleaned_keywords: list[str] = []
    for kw in parsed_keywords:
        cleaned = kw.strip()
        if cleaned and cleaned.casefold() not in seen_kw:
            seen_kw.add(cleaned.casefold())
            cleaned_keywords.append(cleaned)

    return ExpansionResult(queries=queries, keywords=cleaned_keywords)


def normalize_queries(original: str, model_output: str, *, max_queries: int) -> list[str]:
    """Backward-compatible helper returning query strings only."""
    return normalize_expansion(original, model_output, max_queries=max_queries).queries


def _parse_model_output(model_output: str) -> tuple[list[str], list[str]]:
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
        return [], []

    # Handle object format: {"queries": [...], "keywords": [...]}
    if isinstance(parsed, dict):
        raw_queries = parsed.get("queries") or parsed.get("variants") or []
        raw_keywords = parsed.get("keywords") or parsed.get("tags") or []
        queries = [
            " ".join(item.split())
            for item in raw_queries
            if isinstance(item, str) and item.strip()
        ]
        keywords = [
            " ".join(item.split())
            for item in raw_keywords
            if isinstance(item, str) and item.strip()
        ]
        return queries, keywords

    # Handle array format (legacy fallback): ["variant1", "variant2"]
    if isinstance(parsed, list):
        queries = [
            " ".join(item.split())
            for item in parsed
            if isinstance(item, str) and item.strip()
        ]
        return queries, []

    return [], []
