"""Integration tests for the evaluation runner and report generation."""

import tempfile
from pathlib import Path
from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.graphs.workflow import AgentResources
from app.ai.rag.indexing.filters import ChunkMetadata
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.indexing.vector_store import InMemoryVectorStore, VectorRecord
from app.ai.rag.retrieval.mqe import OriginalQueryExpander
from app.ai.rag.retrieval.reranker import CrossEncoderReranker
from evaluation.datasets import load_dataset
from evaluation.runners import EvaluationRunner, render_markdown_report, save_report
from evaluation.schemas.models import (
    EvalCategory,
    EvaluationCase,
    ExpectedBehavior,
)


class _MockLLM:
    def complete(self, *, system: str, user: str) -> str:
        if "claim" in system.lower() or "ground" in system.lower():
            return '{"claims": [{"text": "BSBDA is a zero-balance account", "support": "supported", "evidence_ids": ["BSBDA#c0001"]}]}'
        return "BSBDA is a zero-balance account for financial inclusion."


class _MockLexical:
    def search(self, query: str, *, top_k: int, metadata_filter: object = None) -> list[RetrievalHit]:
        return [
            RetrievalHit(
                chunk_id="BSBDA#c0001",
                document_id="BSBDA",
                score=10.0,
                source="bm25",
                text="BSBDA is an RBI-mandated zero-balance account.",

                metadata=ChunkMetadata(
                    chunk_id="BSBDA#c0001",
                    document_id="BSBDA",
                    document_version="1.0",
                    document_type="product",
                    document_title="BSBDA",
                    status="approved",
                    source_path="accounts/bsbda.md",
                    content_hash="hash",
                ),
            )
        ]


def _build_mock_resources() -> AgentResources:
    embedder = DeterministicEmbeddingProvider("test", 8)
    store = InMemoryVectorStore()
    store.upsert(
        [
            VectorRecord(
                chunk_id="BSBDA#c0001",
                vector=embedder.embed_documents(["BSBDA is a zero-balance account."]).embeddings[0].vector,
                metadata=ChunkMetadata(
                    chunk_id="BSBDA#c0001",
                    document_id="BSBDA",
                    document_version="1.0",
                    document_type="product",
                    document_title="BSBDA",
                    status="approved",
                    source_path="accounts/bsbda.md",
                    content_hash="hash",
                ),
                text="BSBDA is an RBI-mandated zero-balance account.",
            )
        ]
    )
    return AgentResources(
        embedder=embedder,
        vector_store=store,
        lexical_index=_MockLexical(),
        expander=OriginalQueryExpander(),
        reranker=CrossEncoderReranker("test", scorer=lambda q, texts: [0.95 for _ in texts]),
        llm=_MockLLM(),
        input_max_chars=2000,
    )


def test_load_dataset():
    cases = load_dataset()
    assert len(cases) >= 10
    categories = {c.category for c in cases}
    assert EvalCategory.FULLY_SUPPORTED in categories
    assert EvalCategory.PARTIALLY_SUPPORTED in categories
    assert EvalCategory.UNSUPPORTED in categories
    assert EvalCategory.ADVERSARIAL in categories


def test_runner_evaluates_suite():
    resources = _build_mock_resources()
    runner = EvaluationRunner(resources)

    test_case = EvaluationCase(
        id="test_suite_01",
        category=EvalCategory.FULLY_SUPPORTED,
        query="What is BSBDA?",
        expected_behavior=ExpectedBehavior.ANSWER,
        required_chunk_ids=["BSBDA#c0001"],
    )

    report = runner.run_suite([test_case])
    assert report.total_cases == 1
    assert report.passed_cases == 1
    assert report.pass_rate == 1.0
    assert "mean_hit_rate" in report.retrieval_aggregates
    assert report.retrieval_aggregates["mean_hit_rate"] == 1.0

    # Test report formatting and saving
    md = render_markdown_report(report)
    assert "# Benchmark Evaluation Report" in md
    assert "BSBDA#c0001" not in md  # table shows case IDs

    with tempfile.TemporaryDirectory() as tmp_dir:
        json_path, md_path = save_report(report, output_dir=tmp_dir)
        assert Path(json_path).exists()
        assert Path(md_path).exists()
