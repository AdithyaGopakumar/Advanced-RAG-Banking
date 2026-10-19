"""Context assembly and query understanding for multi-turn conversations."""

from __future__ import annotations

import logging
import re

from app.ai.memory.models import ConversationMessage
from app.ai.providers.llm import LLMNotConfiguredError, LLMProvider

logger = logging.getLogger(__name__)

# Pronouns and anaphoric cues that indicate the current query depends on previous turns
_ANAPHORA_PATTERN = re.compile(
    r"\b(it|its|that account|this account|this card|that card|this deposit|that deposit|the same|same account)\b",
    re.IGNORECASE,
)

_FOLLOW_UP_PATTERN = re.compile(
    r"^(what about|how about|what of|tell me about|and what|and how|and the)\b",
    re.IGNORECASE,
)

# Common banking domain product/subject terms to extract when resolving references deterministically
_BANKING_ENTITIES = [
    re.compile(r"\b(BSBDA\s+Small(?:\s+Account)?)\b", re.IGNORECASE),
    re.compile(r"\b(BSBDA|Basic\s+Savings\s+Bank\s+Deposit\s+Account)\b", re.IGNORECASE),
    re.compile(r"\b(Premier\s+Savings(?:\s+Account)?)\b", re.IGNORECASE),
    re.compile(r"\b(Savings\s+Account|Savings\s+Bank)\b", re.IGNORECASE),
    re.compile(r"\b(Salary\s+Account)\b", re.IGNORECASE),
    re.compile(r"\b(Current\s+Account)\b", re.IGNORECASE),
    re.compile(r"\b(Fixed\s+Deposit|FD|Term\s+Deposit)\b", re.IGNORECASE),
    re.compile(r"\b(Recurring\s+Deposit|RD)\b", re.IGNORECASE),
    re.compile(r"\b(Senior\s+Citizen(?:\s+FD|\s+Deposit|\s+Account)?)\b", re.IGNORECASE),
    re.compile(r"\b(NRE|NRO|FCNR)\b", re.IGNORECASE),
    re.compile(r"\b(Debit\s+Card|Credit\s+Card|ATM\s+Card)\b", re.IGNORECASE),
    re.compile(r"\b(Gold\s+Loan|Home\s+Loan|Personal\s+Loan|Education\s+Loan|Car\s+Loan|Vehicle\s+Loan|Loan)\b", re.IGNORECASE),
    re.compile(r"\b(Locker|Safe\s+Deposit\s+Locker)\b", re.IGNORECASE),
    re.compile(r"\b(Overdraft|OD)\b", re.IGNORECASE),
    re.compile(r"\b(PPF|Public\s+Provident\s+Fund)\b", re.IGNORECASE),
]

_CONTEXTUALIZE_PROMPT = """You are a banking query understanding assistant.
Given a conversation history and a follow-up question, rewrite the follow-up question into a clear, standalone banking question.

Rules:
- Resolve pronouns ("it", "that account", "those fees", "this card") using the previous turns.
- Keep the user's intent unchanged.
- Do NOT answer the question.
- Do NOT add new banking facts, terms, or conditions that were not mentioned.
- If the question is already standalone, return it exactly as is.
- Return ONLY the rewritten question text without preamble, explanations, or quotes.
"""


def format_history_for_prompt(messages: list[ConversationMessage]) -> list[dict[str, str]]:
    """Format conversation messages into a list of role/content dictionaries."""
    return [{"role": msg.role, "content": msg.content} for msg in messages]


def extract_recent_entity(messages: list[ConversationMessage]) -> str | None:
    """Extract the most recently discussed banking product/entity from history."""
    for msg in reversed(messages):
        text = msg.content
        for pattern in _BANKING_ENTITIES:
            match = pattern.search(text)
            if match:
                raw_entity = match.group(1).strip()
                if raw_entity.isupper():
                    return raw_entity
                return raw_entity.title()
    return None


def resolve_contextual_query(
    query: str,
    history: list[ConversationMessage],
    *,
    llm: LLMProvider | None = None,
) -> str:
    """Reformulate a follow-up query into a standalone question using conversation history.

    If history is empty or query has no anaphoric references, returns the original query.
    If an LLM is available, uses the model to resolve references; otherwise falls back
    to deterministic entity inheritance from the preceding turns.
    """
    clean_query = query.strip()
    if not history or not clean_query:
        return clean_query

    # If the query does not contain anaphoric references and is sufficiently detailed, keep it
    has_anaphora = bool(_ANAPHORA_PATTERN.search(clean_query))
    is_follow_up = bool(_FOLLOW_UP_PATTERN.search(clean_query))
    is_short = len(clean_query.split()) <= 6 and not any(p.search(clean_query) for p in _BANKING_ENTITIES)

    if not has_anaphora and not is_follow_up and not is_short:
        return clean_query

    # 1. Deterministic fast resolution: extract antecedent banking entity and resolve pronouns
    entity = extract_recent_entity(history)
    if entity and entity.lower() not in clean_query.lower():
        if has_anaphora:
            return _ANAPHORA_PATTERN.sub(entity, clean_query, count=1)
        if is_follow_up or is_short:
            return f"{clean_query} for {entity}"

    # 2. Model-based contextualization fallback: for nuanced queries where entity extraction failed
    if llm is not None:
        try:
            recent_turns = history[-6:]  # Last 3 turns (user + assistant)
            conversation_text = "\n".join(
                f"{msg.role.capitalize()}: {msg.content}" for msg in recent_turns
            )
            user_prompt = f"Conversation History:\n{conversation_text}\n\nFollow-up question:\n{clean_query}"
            rewritten = llm.complete(system=_CONTEXTUALIZE_PROMPT, user=user_prompt).strip()
            # Clean any model artifacts (quotes or preamble)
            rewritten = rewritten.strip('"\'`')
            if rewritten and len(rewritten) > 5 and not rewritten.lower().startswith("conversation"):
                return rewritten
        except (LLMNotConfiguredError, Exception) as exc:
            logger.debug("Model-based query contextualization failed (%s); returning original query", exc)

    return clean_query
