"""Session persistence and retrieval for conversation memory."""

from __future__ import annotations

import logging
import threading
from functools import lru_cache
from typing import Protocol

from app.ai.memory.models import ConversationSession

logger = logging.getLogger(__name__)


class SessionStore(Protocol):
    """Protocol for conversation session storage."""

    def get(self, conversation_id: str) -> ConversationSession | None:
        """Retrieve a session by its conversation ID."""
        ...

    def save(self, session: ConversationSession) -> None:
        """Persist or update a conversation session."""
        ...

    def clear(self, conversation_id: str) -> None:
        """Remove a session from the store."""
        ...


class InMemorySessionStore:
    """Thread-safe in-memory session store suitable for development and testing."""

    def __init__(self, *, max_sessions: int = 5000) -> None:
        self._lock = threading.Lock()
        self._sessions: dict[str, ConversationSession] = {}
        self._max_sessions = max_sessions

    def get(self, conversation_id: str) -> ConversationSession | None:
        """Retrieve a session by ID."""
        if not conversation_id:
            return None
        with self._lock:
            return self._sessions.get(conversation_id)

    def save(self, session: ConversationSession) -> None:
        """Save or update a conversation session, pruning oldest if capacity reached."""
        if not session or not session.conversation_id:
            return
        with self._lock:
            if len(self._sessions) >= self._max_sessions and session.conversation_id not in self._sessions:
                # Evict the oldest updated session to maintain bounded memory
                oldest_id = min(self._sessions, key=lambda cid: self._sessions[cid].updated_at)
                del self._sessions[oldest_id]
            self._sessions[session.conversation_id] = session

    def clear(self, conversation_id: str) -> None:
        """Delete a conversation session."""
        with self._lock:
            self._sessions.pop(conversation_id, None)

    def count(self) -> int:
        """Return total active sessions count."""
        with self._lock:
            return len(self._sessions)


@lru_cache()
def get_session_store() -> SessionStore:
    """Cached singleton provider for the session store."""
    return InMemorySessionStore()
