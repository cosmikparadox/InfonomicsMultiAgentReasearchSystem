"""Data models for research outputs. Used by Claude Code to persist structured findings."""

from __future__ import annotations

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


class ResearchSession(BaseModel):
    question: str
    domain: str = "infonomics"
    depth: str = "phd"
    started_at: datetime = Field(default_factory=datetime.now)
    outputs: list[ResearchOutput] = Field(default_factory=list)
    refinement_rounds: int = 0
    status: str = "in_progress"  # in_progress, completed
