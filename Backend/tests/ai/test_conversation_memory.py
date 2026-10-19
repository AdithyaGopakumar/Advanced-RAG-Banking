"""Tests for multi-turn conversation memory, session state, and contextual query resolution."""

import pytest
from starlette.testclient import TestClient

from app.ai.graphs.workflow import AgentResources, run_agent
from app.ai.memory import (
    ConversationMessage,
    ConversationSession,
    InMemorySessionStore,
    format_history_for_prompt,
    resolve_contextual_query,
)
from app.ai.providers.llm import LLMProvider
from app.ai.rag.indexing.filters import ChunkMetadata
from app.ai.rag.indexing.models import RetrievalHit
from app.ai.rag.indexing.vector_store import InMemoryVectorStore, VectorRecord
from app.ai.rag.retrieval.reranker import CrossEncoderReranker
from main import create_app


from app.ai.embeddings.deterministic import DeterministicEmbeddingProvider
from app.ai.rag.retrieval.mqe import OriginalQueryExpander


class _MockLexical:
    def search(self, query: str, *, top_k: int, metadata_filter: object = None) -> list[RetrievalHit]:
        return []


class _ScriptedLLM(LLMProvider):
    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)

    def complete(self, *, system: str, user: str) -> str:
        if self._responses:
            return self._responses.pop(0)
        return "Grounded response."


def _build_test_resources(
    llm: LLMProvider,
    session_store: InMemorySessionStore | None = None,
) -> AgentResources:
    embedder = DeterministicEmbeddingProvider("deterministic", 8)
    store = InMemoryVectorStore()
    store.upsert(
        [
            VectorRecord(
                chunk_id="BSBDA#c0001",
                vector=embedder.embed_documents(["BSBDA requires zero minimum balance."]).embeddings[0].vector,
                metadata=ChunkMetadata(
                    chunk_id="BSBDA#c0001",
                    document_id="BSBDA",
                    document_version="1.0",
                    document_type="product",
                    document_title="BSBDA Account",
                    status="approved",
                    source_path="docs/bsbda.md",
                    content_hash="hash1",
                    heading_path=["BSBDA"],
                ),
                text="BSBDA requires zero minimum balance. Any resident individual can open BSBDA.",
            )
        ]
    )

    return AgentResources(
        embedder=embedder,
        vector_store=store,
        lexical_index=_MockLexical(),
        expander=OriginalQueryExpander(),
        reranker=CrossEncoderReranker("test", scorer=lambda query, texts: [0.9 for _ in texts]),
        llm=llm,
        session_store=session_store,
        max_memory_turns=5,
        top_k=5,
        evidence_top_k=3,
        token_budget=1000,
        input_max_chars=500,
    )


def test_session_store_lifecycle():
    store = InMemorySessionStore()
    session = ConversationSession(conversation_id="conv-101")
    session.add_turn(
        user_content="What is BSBDA?",
        assistant_content="BSBDA is a basic savings bank deposit account.",
        response_type="answer",
        reason_code="SUPPORTED",
    )

    store.save(session)
    fetched = store.get("conv-101")
    assert fetched is not None
    assert fetched.conversation_id == "conv-101"
    assert len(fetched.messages) == 2
    assert fetched.messages[0].role == "user"
    assert fetched.messages[0].content == "What is BSBDA?"
    assert fetched.messages[1].role == "assistant"
    assert fetched.messages[1].response_type == "answer"

    store.clear("conv-101")
    assert store.get("conv-101") is None


def test_session_max_turns_truncation():
    session = ConversationSession(conversation_id="conv-102")
    for i in range(1, 7):
        session.add_turn(f"User question {i}", f"Assistant answer {i}")

    # 6 turns = 12 messages. Requesting last 3 turns returns 6 messages
    recent = session.get_recent_messages(max_turns=3)
    assert len(recent) == 6
    assert recent[0].content == "User question 4"
    assert recent[-1].content == "Assistant answer 6"

    formatted = format_history_for_prompt(recent)
    assert len(formatted) == 6
    assert formatted[0] == {"role": "user", "content": "User question 4"}


def test_contextual_query_resolution_no_history():
    query = "What is the penalty for premature withdrawal?"
    resolved = resolve_contextual_query(query, [])
    assert resolved == query


def test_contextual_query_resolution_with_pronoun():
    history = [
        ConversationMessage(role="user", content="Tell me about the Premier Savings Account"),
        ConversationMessage(role="assistant", content="The Premier Savings Account is a premium savings variant."),
    ]

    # Follow-up with pronoun "it"
    follow_up = "What is the minimum balance for it?"
    resolved = resolve_contextual_query(follow_up, history)
    assert "Premier Savings Account" in resolved
    assert "minimum balance" in resolved


def test_contextual_query_resolution_with_short_followup():
    history = [
        ConversationMessage(role="user", content="What are the Fixed Deposit rates?"),
        ConversationMessage(role="assistant", content="Fixed deposit rates range up to 7.25% p.a."),
    ]

    follow_up = "What about premature closure?"
    resolved = resolve_contextual_query(follow_up, history)
    assert "Fixed Deposit" in resolved


def test_agent_workflow_multi_turn_persistence():
    session_store = InMemorySessionStore()
    llm = _ScriptedLLM(
        [
            # Turn 1: Grounding assessment & Answer
            '{"claims": [{"text": "what is BSBDA", "support": "supported"}]}',
            "BSBDA is a basic savings bank deposit account.",
            # Turn 2: Grounding assessment & Answer for follow-up
            '{"claims": [{"text": "minimum balance", "support": "supported"}]}',
            "BSBDA has zero minimum balance requirement.",
        ]
    )
    resources = _build_test_resources(llm, session_store=session_store)

    cid = "sess-turn-test"

    # Turn 1
    turn1 = run_agent("What is BSBDA?", resources, conversation_id=cid)
    assert turn1.response_type == "answer"
    assert "BSBDA" in turn1.response

    # Verify session store recorded turn 1
    session = session_store.get(cid)
    assert session is not None
    assert len(session.messages) == 2

    # Turn 2: Follow-up question with pronoun
    turn2 = run_agent("What is the minimum balance for it?", resources, conversation_id=cid, full_trace=True)
    assert turn2.response_type == "answer"
    assert "minimum balance" in turn2.response
    assert turn2.resolved_query is not None
    assert "BSBDA" in turn2.resolved_query

    # Verify session store recorded both turns (4 messages total)
    updated_session = session_store.get(cid)
    assert len(updated_session.messages) == 4


def test_knowledge_primacy_with_memory():
    """Verify that conversation memory does NOT bypass retrieval grounding."""
    session_store = InMemorySessionStore()
    # LLM simulates grounding check finding NO evidence for gold loan in BSBDA chunk
    llm = _ScriptedLLM(
        [
            # Grounding says unsupported
            '{"claims": [{"text": "gold loan interest rate", "support": "unsupported"}]}',
        ]
    )
    resources = _build_test_resources(llm, session_store=session_store)

    cid = "sess-primacy-test"
    # Seed session mentioning gold loan in dialogue
    session = ConversationSession(conversation_id=cid)
    session.add_turn("Can I get a gold loan?", "Let me check our gold loan policies.")
    session_store.save(session)

    # Follow up asking for the gold loan interest rate
    turn = run_agent("What is the interest rate for it?", resources, conversation_id=cid)
    # Must return unavailable, NOT fabricate or assume truth from memory
    assert turn.response_type == "unavailable"


@pytest.mark.asyncio
async def test_chat_api_conversation_id_continuity(client):
    from app.modules.chat.dependencies import get_agent_resources
    from main import app

    session_store = InMemorySessionStore()
    llm = _ScriptedLLM(
        [
            '{"claims": [{"text": "BSBDA", "support": "supported", "evidence_ids": ["BSBDA#c0001"]}]}',
            "BSBDA is a basic savings bank deposit account.",
            '{"claims": [{"text": "minimum balance", "support": "supported", "evidence_ids": ["BSBDA#c0001"]}]}',
            "BSBDA has zero minimum balance requirement.",
        ]
    )
    resources = _build_test_resources(llm, session_store=session_store)
    app.dependency_overrides[get_agent_resources] = lambda: resources

    try:
        # Turn 1: without conversationId -> backend generates one
        res1 = await client.post("/api/v1/chat", json={"query": "What is BSBDA?"})
        assert res1.status_code == 200
        data1 = res1.json()["data"]
        cid = data1.get("conversation_id") or data1.get("conversationId")
        assert cid is not None
        assert len(cid) > 0

        # Turn 2: pass conversationId
        res2 = await client.post(
            "/api/v1/chat",
            json={"query": "What is the minimum balance for it?", "conversationId": cid, "fullTrace": True},
        )
        assert res2.status_code == 200
        data2 = res2.json()["data"]
        assert (data2.get("conversation_id") or data2.get("conversationId")) == cid
        assert data2["trace"] is not None
        assert data2["trace"]["conversation"]["conversation_id"] == cid
        assert "BSBDA" in data2["trace"]["conversation"]["resolved_query"]
    finally:
        app.dependency_overrides.clear()
