"""Enrich knowledge chunks with domain keywords using a language model.

Document frontmatter provides authoritative baseline keywords. This enricher
identifies section-specific banking concepts, terms, and synonyms to improve
downstream retrieval precision and pre-filtering.
"""

import json
import logging
from collections.abc import Sequence
from typing import Protocol

from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider, create_llm_provider
from app.core.config import Settings, get_settings
from app.modules.knowledge.models import KnowledgeChunk

logger = logging.getLogger(__name__)

ENRICHMENT_SYSTEM_PROMPT = """You are a specialized banking knowledge engineer.
Your task is to extract section-specific banking keywords, concepts, and synonyms for each given text chunk.

Rules:
1. Extract 2 to 4 concise, high-precision keywords or phrases specific to the content (e.g. "penalty waiver", "cash withdrawal limit", "KYC documents").
2. Focus on specific terms, products, conditions, or customer actions directly discussed in the text.
3. Do not invent fees, limits, or banking facts not present in the chunk.
4. Output a single JSON object mapping each chunk_id to its list of keywords:
   {
     "CHUNK_ID_1": ["keyword1", "keyword2", "keyword3"],
     "CHUNK_ID_2": ["keyword1", "keyword2"]
   }
5. Return JSON only, with no commentary or markdown fences.
"""


class ChunkEnricher(Protocol):
    """Enriches knowledge chunks with semantic keywords."""

    def enrich(self, chunks: Sequence[KnowledgeChunk]) -> list[KnowledgeChunk]:
        """Return chunks with additive semantic keywords."""


class NoOpChunkEnricher:
    """Pass-through enricher. Used when LLM enrichment is disabled or unconfigured."""

    def enrich(self, chunks: Sequence[KnowledgeChunk]) -> list[KnowledgeChunk]:
        return list(chunks)


class LLMChunkEnricher:
    """Enrich chunks using a language model in parallel batches."""

    def __init__(self, llm: LLMProvider, *, batch_size: int = 5, max_workers: int = 8) -> None:
        self._llm = llm
        self._batch_size = max(1, batch_size)
        self._max_workers = max(1, max_workers)

    def enrich(self, chunks: Sequence[KnowledgeChunk]) -> list[KnowledgeChunk]:
        if not chunks:
            return []

        batches = [
            list(chunks[i : i + self._batch_size])
            for i in range(0, len(chunks), self._batch_size)
        ]
        total_batches = len(batches)
        print(f"Enriching {len(chunks)} chunks with LLM metadata ({total_batches} batches, concurrency={self._max_workers})...", flush=True)

        from concurrent.futures import ThreadPoolExecutor, as_completed
        import sys

        enriched_results: list[tuple[int, list[KnowledgeChunk]]] = []
        completed_count = 0

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            future_to_idx = {
                executor.submit(self._enrich_batch, batch): idx
                for idx, batch in enumerate(batches)
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                batch_res = future.result()
                enriched_results.append((idx, batch_res))
                completed_count += 1
                percent = int((completed_count / total_batches) * 100)
                sys.stdout.write(f"\r  Progress: {completed_count}/{total_batches} batches completed ({percent}%)")
                sys.stdout.flush()

        sys.stdout.write("\n")
        sys.stdout.flush()

        enriched_results.sort(key=lambda item: item[0])
        flattened: list[KnowledgeChunk] = []
        for _, batch in enriched_results:
            flattened.extend(batch)
        return flattened

    def _enrich_batch(self, batch: list[KnowledgeChunk]) -> list[KnowledgeChunk]:
        user_prompt = _build_batch_prompt(batch)
        try:
            raw_response = self._llm.complete(system=ENRICHMENT_SYSTEM_PROMPT, user=user_prompt)
            keyword_map = _parse_enrichment_response(raw_response)
        except Exception as exc:
            logger.warning(
                "Chunk metadata enrichment failed for batch; using existing metadata",
                extra={"batch_size": len(batch), "error_type": type(exc).__name__},
            )
            return batch

        result: list[KnowledgeChunk] = []
        for chunk in batch:
            extracted = keyword_map.get(chunk.chunk_id, [])
            combined_keywords = _merge_keywords(chunk.keywords, extracted)
            # Reconstruct chunk with updated keywords
            updated = chunk.model_copy(update={"keywords": combined_keywords})
            result.append(updated)
        return result


def create_chunk_enricher(
    settings: Settings | None = None,
    llm: LLMProvider | None = None,
) -> ChunkEnricher:
    """Create a configured chunk enricher."""
    current = settings if settings is not None else get_settings()
    if not current.ENABLE_METADATA_ENRICHMENT:
        return NoOpChunkEnricher()

    if llm is None:
        if not current.OPENAI_API_KEY.strip():
            logger.info("OPENAI_API_KEY is not set; chunk metadata enrichment is disabled")
            return NoOpChunkEnricher()
        try:
            llm = create_llm_provider(current)
        except LLMNotConfiguredError:
            return NoOpChunkEnricher()

    max_workers = getattr(current, "ENRICHMENT_MAX_WORKERS", 8)
    return LLMChunkEnricher(llm, batch_size=current.ENRICHMENT_BATCH_SIZE, max_workers=max_workers)


def _build_batch_prompt(batch: list[KnowledgeChunk]) -> str:
    sections: list[str] = []
    for chunk in batch:
        path = " > ".join(chunk.heading_path) if chunk.heading_path else chunk.document_title
        snippet = chunk.content[:800].strip()
        sections.append(
            f"--- Chunk ID: {chunk.chunk_id} ---\n"
            f"Title: {chunk.document_title}\n"
            f"Heading: {path}\n"
            f"Content:\n{snippet}\n"
        )
    return "\n".join(sections)


def _parse_enrichment_response(raw_text: str) -> dict[str, list[str]]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Enrichment response is not valid JSON")
        return {}

    if not isinstance(parsed, dict):
        return {}

    result: dict[str, list[str]] = {}
    for chunk_id, keywords in parsed.items():
        if isinstance(keywords, list):
            cleaned = [str(kw).strip() for kw in keywords if str(kw).strip()]
            if cleaned:
                result[str(chunk_id)] = cleaned
    return result


def _merge_keywords(existing: Sequence[str], additive: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for kw in existing:
        cleaned = kw.strip()
        if cleaned and cleaned.casefold() not in seen:
            seen.add(cleaned.casefold())
            merged.append(cleaned)
    for kw in additive:
        cleaned = kw.strip()
        if cleaned and cleaned.casefold() not in seen:
            seen.add(cleaned.casefold())
            merged.append(cleaned)
    return merged
