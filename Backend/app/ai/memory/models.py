"""Data models for conversation memory and session state."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ConversationMessage(BaseModel):
    """A single turn/message in a conversation session."""

    model_config = ConfigDict(extra="ignore")

    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=_utc_now)
    response_type: str | None = None
    reason_code: str | None = None
    chunk_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class ConversationSession(BaseModel):
    """A multi-turn conversation session containing sequential turns."""

    model_config = ConfigDict(extra="ignore")

    conversation_id: str
    messages: list[ConversationMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    def add_turn(
        self,
        user_content: str,
        assistant_content: str,
        *,
        response_type: str | None = None,
        reason_code: str | None = None,
        chunk_ids: list[str] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Append a user question and assistant answer to the session history."""
        now = _utc_now()
        self.messages.append(
            ConversationMessage(
                role="user",
                content=user_content,
                timestamp=now,
            )
        )
        self.messages.append(
            ConversationMessage(
                role="assistant",
                content=assistant_content,
                timestamp=now,
                response_type=response_type,
                reason_code=reason_code,
                chunk_ids=list(chunk_ids or []),
                metadata=metadata or {},
            )
        )
        self.updated_at = now

    def get_recent_messages(self, max_turns: int = 5) -> list[ConversationMessage]:
        """Return the most recent messages up to max_turns pairs (2 * max_turns messages)."""
        max_messages = max(1, max_turns) * 2
        return self.messages[-max_messages:]
