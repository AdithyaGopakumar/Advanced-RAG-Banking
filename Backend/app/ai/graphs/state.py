"""State carried between agent nodes.

Conversation history is not loaded here. Memory is context for a later
phase and is not a source of banking facts.
"""

from typing import TypedDict


class AgentState(TypedDict, total=False):
    """Fields the workflow reads and writes. Nodes return only what they change."""

    user_message: str
    normalized_query: str
    evidence: dict[str, object]
    decision: dict[str, object]
    support_level: str
    response: str
    response_type: str
    reason_code: str
    chunk_ids: list[str]
    errors: list[str]
    output_ok: bool
