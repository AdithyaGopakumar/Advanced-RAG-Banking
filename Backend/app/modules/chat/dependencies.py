"""Dependency injection for the chat module."""

import logging
from functools import lru_cache

from app.ai.embeddings.factory import create_embedding_provider
from app.ai.graphs.workflow import AgentResources
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider, create_llm_provider
from app.ai.rag.indexing.lexical import LexicalIndexError, create_lexical_index
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.indexing.vector_store import create_vector_store
from app.ai.rag.retrieval.mqe import create_query_expander
from app.ai.rag.retrieval.reranker import create_reranker
from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


class EmptyLexicalSearcher:
    """Fallback when Elasticsearch is not running or unconfigured."""

    def search(self, query: str, *, top_k: int, metadata_filter: object = None) -> list[RetrievalHit]:
        return []


class UnconfiguredLLMProvider:
    """Fallback when OPENAI_API_KEY is not configured."""

    def complete(self, *, system: str, user: str) -> str:
        raise LLMNotConfiguredError("Set OPENAI_API_KEY before calling the chat model.")


from fastapi import Depends

_agent_resources_cache: AgentResources | None = None


def _build_agent_resources(settings: Settings) -> AgentResources:
    embedder = create_embedding_provider(settings)
    vector_store = create_vector_store(settings)
    try:
        lexical_index = create_lexical_index(settings)
    except (LexicalIndexError, Exception) as exc:
        logger.warning("Lexical index unavailable (%s); using in-memory empty lexical fallback", exc)
        lexical_index = EmptyLexicalSearcher()

    expander = create_query_expander(settings)
    reranker = create_reranker(settings)
    try:
        llm: LLMProvider = create_llm_provider(settings)
    except (LLMNotConfiguredError, Exception) as exc:
        logger.warning("LLM provider unavailable (%s); using unconfigured LLM fallback", exc)
        llm = UnconfiguredLLMProvider()

    from app.ai.memory import get_session_store

    session_store = get_session_store() if settings.ENABLE_CONVERSATION_MEMORY else None

    return AgentResources(
        embedder=embedder,
        vector_store=vector_store,
        lexical_index=lexical_index,
        expander=expander,
        reranker=reranker,
        llm=llm,
        session_store=session_store,
        max_memory_turns=settings.MAX_MEMORY_TURNS,
        top_k=settings.RETRIEVAL_TOP_K,
        candidates_per_query=settings.RETRIEVAL_CANDIDATES_PER_QUERY,
        rrf_k=settings.RETRIEVAL_RRF_K,
        evidence_top_k=settings.EVIDENCE_TOP_K,
        token_budget=settings.CONTEXT_TOKEN_BUDGET,
        min_score=settings.RERANKER_MIN_SCORE,
        input_max_chars=settings.INPUT_MAX_CHARS,
    )


def get_agent_resources(settings: Settings = Depends(get_settings)) -> AgentResources:
    """Build or retrieve cached AgentResources singleton."""
    global _agent_resources_cache
    if _agent_resources_cache is None:
        actual_settings = settings if isinstance(settings, Settings) else get_settings()
        _agent_resources_cache = _build_agent_resources(actual_settings)
    return _agent_resources_cache


def reset_agent_resources_cache() -> None:
    """Reset cached resources (primarily for testing)."""
    global _agent_resources_cache
    _agent_resources_cache = None


