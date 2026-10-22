"""In-process conversation state for agent sessions."""

from dataclasses import dataclass, field
from threading import Lock


@dataclass(slots=True)
class SessionState:
    """Conversation state for a single session."""

    history: list[tuple[str, str]] = field(default_factory=list)


class SessionStore:
    """Process-local session store."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._sessions: dict[str, SessionState] = {}

    def get(self, session_id: str) -> SessionState:
        with self._lock:
            return self._sessions.setdefault(session_id, SessionState())


def conversation_context(history: list[tuple[str, str]]) -> str:
    """Render prior conversation turns for the agent prompt."""
    if not history:
        return "No prior conversation."
    lines: list[str] = []
    for user_message, reply in history[-6:]:
        lines.append(f"Customer: {user_message}")
        lines.append(f"Concierge: {reply}")
    return "\n".join(lines)
