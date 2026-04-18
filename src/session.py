"""Session management — persistent, checkpointable, resumable research sessions.

Design:
- Every session has a stable ``session_id`` and writes to a stable file
  (``data/outputs/sessions/<session_id>.json``), overwritten on each checkpoint.
  A crash loses at most the work since the last checkpoint.
- Alongside the snapshot, a JSONL event log (``<session_id>.events.jsonl``)
  records every phase transition, refinement, and error for observability.
- ``resume_session`` rehydrates a session from disk and returns it alongside
  the next phase to run, so Claude Code can pick up mid-pipeline.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from src.models import (
    AgentRole,
    ResearchOutput,
    ResearchPhase,
    ResearchSession,
    SessionEvent,
    SessionStatus,
)

OUTPUTS_DIR = Path("data/outputs")
SESSIONS_DIR = OUTPUTS_DIR / "sessions"
KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def session_path(session_id: str) -> Path:
    """Stable snapshot path for a session. Overwritten on each checkpoint."""
    return SESSIONS_DIR / f"{session_id}.json"


def event_log_path(session_id: str) -> Path:
    """JSONL observability log path for a session."""
    return SESSIONS_DIR / f"{session_id}.events.jsonl"


def _ensure_dirs() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Atomic writes
# ---------------------------------------------------------------------------


def _atomic_write(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` atomically via a temp file + rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# Event log
# ---------------------------------------------------------------------------


def log_event(
    session: ResearchSession,
    event_type: str,
    *,
    phase: ResearchPhase | None = None,
    role: AgentRole | None = None,
    message: str = "",
    data: dict[str, Any] | None = None,
) -> SessionEvent:
    """Append a single observability event to the session's JSONL log."""
    _ensure_dirs()
    event = SessionEvent(
        session_id=session.session_id,
        event_type=event_type,
        phase=phase,
        role=role,
        message=message,
        data=data or {},
    )
    line = event.model_dump_json() + "\n"
    with event_log_path(session.session_id).open("a", encoding="utf-8") as fh:
        fh.write(line)
    return event


def read_events(session_id: str) -> list[SessionEvent]:
    """Read all events for a session from its JSONL log."""
    path = event_log_path(session_id)
    if not path.exists():
        return []
    events: list[SessionEvent] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        events.append(SessionEvent.model_validate_json(raw))
    return events


# ---------------------------------------------------------------------------
# Session lifecycle
# ---------------------------------------------------------------------------


def new_session(
    question: str,
    *,
    domain: str = "infonomics",
    depth: str = "phd",
    metadata: dict[str, Any] | None = None,
) -> ResearchSession:
    """Create a fresh session, persist the initial snapshot, log the start."""
    _ensure_dirs()
    session = ResearchSession(
        question=question,
        domain=domain,
        depth=depth,
        metadata=metadata or {},
    )
    checkpoint(session, reason="session_started")
    log_event(
        session,
        "session_started",
        message=question,
        data={"domain": domain, "depth": depth},
    )
    return session


def checkpoint(session: ResearchSession, *, reason: str = "checkpoint") -> Path:
    """Persist the current session state to disk atomically.

    Call this after every role switch — the session file is the single
    source of truth used on resume.
    """
    session.last_checkpoint_at = datetime.now()
    path = session_path(session.session_id)
    _atomic_write(path, session.model_dump_json(indent=2))
    if reason != "session_started":
        log_event(session, "checkpoint", phase=session.current_phase, message=reason)
    return path


def record_output(
    session: ResearchSession,
    output: ResearchOutput,
    *,
    next_phase: ResearchPhase | None = None,
) -> Path:
    """Append a role's output, advance phase tracking, and checkpoint."""
    session.outputs.append(output)
    log_event(
        session,
        "phase_completed",
        phase=output.phase,
        role=output.agent_role,
        message=output.summary[:200],
        data={
            "findings": len(output.findings),
            "critiques": len(output.critiques),
            "citations": len(output.citations),
        },
    )
    session.current_phase = None
    session.next_phase = next_phase
    return checkpoint(session, reason=f"after_{output.phase.value}")


def start_phase(
    session: ResearchSession,
    phase: ResearchPhase,
    role: AgentRole,
) -> Path:
    """Mark a phase as started and checkpoint so a crash is debuggable."""
    session.current_phase = phase
    session.next_phase = None
    log_event(session, "phase_started", phase=phase, role=role)
    return checkpoint(session, reason=f"start_{phase.value}")


def mark_refinement(session: ResearchSession, *, reason: str = "") -> Path:
    """Increment the refinement counter, log, and checkpoint."""
    session.refinement_rounds += 1
    session.next_phase = ResearchPhase.REFINEMENT
    log_event(
        session,
        "refinement_triggered",
        message=reason,
        data={"round": session.refinement_rounds},
    )
    return checkpoint(session, reason=f"refinement_round_{session.refinement_rounds}")


def finalize(session: ResearchSession) -> Path:
    """Mark the session completed and checkpoint."""
    session.status = SessionStatus.COMPLETED
    session.completed_at = datetime.now()
    session.current_phase = None
    session.next_phase = None
    log_event(session, "session_completed")
    return checkpoint(session, reason="session_completed")


def mark_failed(session: ResearchSession, error: str) -> Path:
    """Mark the session failed with an error message and checkpoint."""
    session.status = SessionStatus.FAILED
    session.last_error = error
    log_event(session, "session_failed", message=error)
    return checkpoint(session, reason="session_failed")


def mark_paused(session: ResearchSession, reason: str = "") -> Path:
    """Mark a still-active session as paused (e.g., harness stopped)."""
    session.status = SessionStatus.PAUSED
    log_event(session, "session_paused", message=reason)
    return checkpoint(session, reason="session_paused")


# ---------------------------------------------------------------------------
# Load / resume / list
# ---------------------------------------------------------------------------


def load_session(ref: str | Path) -> ResearchSession:
    """Load a session by id, path, or legacy timestamped filename."""
    path = _resolve_session_path(ref)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ResearchSession.model_validate(data)


def _resolve_session_path(ref: str | Path) -> Path:
    """Accept a session_id, a bare filename, or a full path."""
    p = Path(ref)
    if p.exists():
        return p
    candidate = session_path(str(ref))
    if candidate.exists():
        return candidate
    # Legacy session_YYYYMMDD_HHMMSS.json files live directly in OUTPUTS_DIR
    legacy = OUTPUTS_DIR / str(ref)
    if legacy.exists():
        return legacy
    raise FileNotFoundError(f"No session found for: {ref}")


def resume_session(ref: str | Path) -> tuple[ResearchSession, ResearchPhase | None]:
    """Load a session and return it with its next phase to run.

    Transitions status back to ``IN_PROGRESS`` if it was ``PAUSED``.
    If the session is already completed, the caller should not continue.
    """
    session = load_session(ref)
    if session.status == SessionStatus.PAUSED:
        session.status = SessionStatus.IN_PROGRESS
    log_event(
        session,
        "session_resumed",
        phase=session.current_phase,
        data={
            "prior_status": session.status.value,
            "outputs_so_far": len(session.outputs),
            "refinement_rounds": session.refinement_rounds,
        },
    )
    checkpoint(session, reason="session_resumed")
    next_phase = session.next_phase or session.current_phase
    return session, next_phase


def list_sessions() -> list[Path]:
    """List snapshot files for all sessions, newest first.

    Includes both the new ``sessions/<id>.json`` layout and any legacy
    ``session_*.json`` files directly under ``data/outputs/``.
    """
    snapshots: list[Path] = []
    if SESSIONS_DIR.exists():
        snapshots.extend(SESSIONS_DIR.glob("sess_*.json"))
    if OUTPUTS_DIR.exists():
        snapshots.extend(OUTPUTS_DIR.glob("session_*.json"))
    snapshots.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return snapshots


def find_resumable() -> list[ResearchSession]:
    """Return sessions that are not yet completed or failed — candidates for resume."""
    resumable: list[ResearchSession] = []
    for path in list_sessions():
        try:
            s = load_session(path)
        except Exception:
            continue
        if s.status in (SessionStatus.IN_PROGRESS, SessionStatus.PAUSED):
            resumable.append(s)
    return resumable


# ---------------------------------------------------------------------------
# Backwards-compatible helpers
# ---------------------------------------------------------------------------


def save_session(session: ResearchSession) -> Path:
    """Back-compat alias — snapshot the session. Prefer ``checkpoint``."""
    return checkpoint(session, reason="save_session")


def save_to_knowledge_base(topic: str, content: str) -> Path:
    """Save a piece of knowledge for cross-session reference."""
    KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.lower().replace(" ", "_")[:50]
    filepath = KNOWLEDGE_BASE_DIR / f"{safe_topic}_{timestamp}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath
