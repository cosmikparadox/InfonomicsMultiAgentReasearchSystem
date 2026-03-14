"""Session management — save and load research sessions to/from JSON files."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.models import ResearchSession

OUTPUTS_DIR = Path("data/outputs")
KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")


def save_session(session: ResearchSession) -> Path:
    """Save a research session to a JSON file."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUTS_DIR / f"session_{timestamp}.json"
    filepath.write_text(
        session.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return filepath


def load_session(filepath: str | Path) -> ResearchSession:
    """Load a research session from a JSON file."""
    path = Path(filepath)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ResearchSession.model_validate(data)


def list_sessions() -> list[Path]:
    """List all saved research sessions."""
    if not OUTPUTS_DIR.exists():
        return []
    return sorted(OUTPUTS_DIR.glob("session_*.json"), reverse=True)


def save_to_knowledge_base(topic: str, content: str) -> Path:
    """Save a piece of knowledge for cross-session reference."""
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.lower().replace(" ", "_")[:50]
    filepath = KNOWLEDGE_BASE_DIR / f"{safe_topic}_{timestamp}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath
