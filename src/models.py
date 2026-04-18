"""Data models for research outputs. Used by Claude Code to persist structured findings."""

from __future__ import annotations

import secrets
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    LITERATURE_REVIEWER = "literature_reviewer"
    THEORIST = "theorist"
    CRITIC = "critic"
    SYNTHESIZER = "synthesizer"


class ResearchPhase(str, Enum):
    LITERATURE_REVIEW = "literature_review"
    THEORETICAL_ANALYSIS = "theoretical_analysis"
    CRITIQUE = "critique"
    REFINEMENT = "refinement"
    SYNTHESIS = "synthesis"


class SessionStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class Citation(BaseModel):
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source: str = ""
    doi: str | None = None
    summary: str = ""


class Finding(BaseModel):
    claim: str
    evidence: str
    confidence: Confidence
    methodology: str = ""
    limitations: str = ""
    citations: list[Citation] = Field(default_factory=list)


class CritiquePoint(BaseModel):
    target: str
    issue_type: str  # methodological, logical, empirical, scope, assumption
    description: str
    severity: str  # major, minor, suggestion
    suggested_remedy: str = ""


class ResearchOutput(BaseModel):
    agent_role: AgentRole
    phase: ResearchPhase
    timestamp: datetime = Field(default_factory=datetime.now)
    summary: str
    detailed_content: str
    findings: list[Finding] = Field(default_factory=list)
    critiques: list[CritiquePoint] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionEvent(BaseModel):
    """Single observability event appended to the session JSONL log."""

    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: str
    event_type: str  # session_started, phase_started, phase_completed, checkpoint,
                     # refinement_triggered, session_paused, session_resumed,
                     # session_completed, session_failed, note
    phase: ResearchPhase | None = None
    role: AgentRole | None = None
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)


def _generate_session_id() -> str:
    """Stable, sortable session id — sess_<YYYYMMDD_HHMMSS>_<rand6>."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = secrets.token_hex(3)
    return f"sess_{stamp}_{suffix}"


class ResearchSession(BaseModel):
    # Identity
    session_id: str = Field(default_factory=_generate_session_id)
    question: str
    domain: str = "infonomics"
    depth: str = "phd"

    # Timing
    started_at: datetime = Field(default_factory=datetime.now)
    last_checkpoint_at: datetime | None = None
    completed_at: datetime | None = None

    # Progress
    outputs: list[ResearchOutput] = Field(default_factory=list)
    refinement_rounds: int = 0
    current_phase: ResearchPhase | None = None
    next_phase: ResearchPhase | None = ResearchPhase.LITERATURE_REVIEW

    # State
    status: SessionStatus = SessionStatus.IN_PROGRESS
    last_error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
