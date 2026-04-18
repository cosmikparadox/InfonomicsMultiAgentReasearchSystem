"""Tests for checkpointable session lifecycle."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from src import session as session_mod
from src.models import (
    AgentRole,
    ResearchOutput,
    ResearchPhase,
    SessionStatus,
)


@pytest.fixture(autouse=True)
def isolated_outputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect every persistence path into a per-test tmp dir."""
    outputs = tmp_path / "outputs"
    sessions = outputs / "sessions"
    kb = tmp_path / "kb"
    monkeypatch.setattr(session_mod, "OUTPUTS_DIR", outputs)
    monkeypatch.setattr(session_mod, "SESSIONS_DIR", sessions)
    monkeypatch.setattr(session_mod, "KNOWLEDGE_BASE_DIR", kb)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _make_output(phase: ResearchPhase, role: AgentRole) -> ResearchOutput:
    return ResearchOutput(
        agent_role=role,
        phase=phase,
        summary="ok",
        detailed_content="x",
    )


def test_new_session_writes_stable_snapshot_and_event_log() -> None:
    s = session_mod.new_session("Why does data have decreasing marginal value?")

    snapshot = session_mod.session_path(s.session_id)
    log = session_mod.event_log_path(s.session_id)
    assert snapshot.exists()
    assert log.exists()

    events = session_mod.read_events(s.session_id)
    types = [e.event_type for e in events]
    assert "session_started" in types


def test_checkpoint_overwrites_same_file_and_appends_event() -> None:
    s = session_mod.new_session("Q")
    snapshot = session_mod.session_path(s.session_id)
    first_size = snapshot.stat().st_size
    first_mtime_ns = snapshot.stat().st_mtime_ns

    s.refinement_rounds = 2
    # Bump mtime deterministically so the assertion does not depend on filesystem clock.
    os.utime(snapshot, ns=(first_mtime_ns - 1_000_000_000, first_mtime_ns - 1_000_000_000))
    session_mod.checkpoint(s, reason="manual")

    # Same file path, new content.
    assert snapshot.exists()
    data = json.loads(snapshot.read_text())
    assert data["refinement_rounds"] == 2
    assert snapshot.stat().st_mtime_ns > first_mtime_ns - 1_000_000_000
    assert snapshot.stat().st_size != first_size or data["last_checkpoint_at"] is not None

    events = session_mod.read_events(s.session_id)
    assert any(e.event_type == "checkpoint" and e.message == "manual" for e in events)


def test_phase_lifecycle_advances_and_persists() -> None:
    s = session_mod.new_session("Q")

    session_mod.start_phase(s, ResearchPhase.LITERATURE_REVIEW, AgentRole.LITERATURE_REVIEWER)
    reloaded = session_mod.load_session(s.session_id)
    assert reloaded.current_phase == ResearchPhase.LITERATURE_REVIEW
    assert reloaded.next_phase is None

    out = _make_output(ResearchPhase.LITERATURE_REVIEW, AgentRole.LITERATURE_REVIEWER)
    session_mod.record_output(s, out, next_phase=ResearchPhase.THEORETICAL_ANALYSIS)
    reloaded = session_mod.load_session(s.session_id)
    assert reloaded.current_phase is None
    assert reloaded.next_phase == ResearchPhase.THEORETICAL_ANALYSIS
    assert len(reloaded.outputs) == 1

    events = [e.event_type for e in session_mod.read_events(s.session_id)]
    assert "phase_started" in events
    assert "phase_completed" in events


def test_resume_session_returns_next_phase_and_logs_resume() -> None:
    s = session_mod.new_session("Q")
    session_mod.record_output(
        s,
        _make_output(ResearchPhase.LITERATURE_REVIEW, AgentRole.LITERATURE_REVIEWER),
        next_phase=ResearchPhase.THEORETICAL_ANALYSIS,
    )
    session_mod.mark_paused(s, reason="harness died")

    resumed, next_phase = session_mod.resume_session(s.session_id)
    assert next_phase == ResearchPhase.THEORETICAL_ANALYSIS
    assert resumed.status == SessionStatus.IN_PROGRESS

    types = [e.event_type for e in session_mod.read_events(s.session_id)]
    assert "session_paused" in types
    assert "session_resumed" in types


def test_find_resumable_excludes_completed_and_failed() -> None:
    in_prog = session_mod.new_session("active")
    done = session_mod.new_session("done")
    session_mod.finalize(done)
    failed = session_mod.new_session("broken")
    session_mod.mark_failed(failed, "boom")

    ids = {s.session_id for s in session_mod.find_resumable()}
    assert in_prog.session_id in ids
    assert done.session_id not in ids
    assert failed.session_id not in ids


def test_refinement_increments_and_is_tracked() -> None:
    s = session_mod.new_session("Q")
    session_mod.mark_refinement(s, reason="critic flagged 3 majors")
    session_mod.mark_refinement(s, reason="still has gaps")
    reloaded = session_mod.load_session(s.session_id)
    assert reloaded.refinement_rounds == 2
    assert reloaded.next_phase == ResearchPhase.REFINEMENT
    rounds = [
        e.data["round"]
        for e in session_mod.read_events(s.session_id)
        if e.event_type == "refinement_triggered"
    ]
    assert rounds == [1, 2]


def test_atomic_write_does_not_leave_temp_files_on_success() -> None:
    s = session_mod.new_session("Q")
    session_mod.checkpoint(s, reason="x")
    leftover = list(session_mod.SESSIONS_DIR.glob("*.tmp*"))
    leftover += list(session_mod.SESSIONS_DIR.glob("tmp*"))
    assert leftover == []
