"""Core types for the multi-agent research system."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """Roles that agents can play in the research pipeline."""

    ORCHESTRATOR = "orchestrator"
    LITERATURE_REVIEWER = "literature_reviewer"
    DATA_ANALYST = "data_analyst"
    THEORIST = "theorist"
    CRITIC = "critic"
    SYNTHESIZER = "synthesizer"


class ResearchPhase(str, Enum):
    """Phases of the research pipeline."""

    QUESTION_FORMULATION = "question_formulation"
    LITERATURE_REVIEW = "literature_review"
    THEORETICAL_ANALYSIS = "theoretical_analysis"
    DATA_ANALYSIS = "data_analysis"
    CRITIQUE = "critique"
    SYNTHESIS = "synthesis"
    REFINEMENT = "refinement"


class Confidence(str, Enum):
    """Confidence level for claims and findings."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class Citation(BaseModel):
    """A reference to a source."""

    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source: str = ""  # journal, conference, url, etc.
    doi: str | None = None
    summary: str = ""


class Finding(BaseModel):
    """A single research finding or claim."""

    claim: str
    evidence: str
    confidence: Confidence
    citations: list[Citation] = Field(default_factory=list)
    methodology: str = ""
    limitations: str = ""


class CritiquePoint(BaseModel):
    """A critique of a finding or argument."""

    target: str  # what is being critiqued
    issue_type: str  # e.g., "methodological", "logical", "empirical", "scope"
    description: str
    severity: str  # "major", "minor", "suggestion"
    suggested_remedy: str = ""


class ResearchOutput(BaseModel):
    """Output from any research agent."""

    agent_role: AgentRole
    phase: ResearchPhase
    timestamp: datetime = Field(default_factory=datetime.now)
    summary: str
    detailed_content: str
    findings: list[Finding] = Field(default_factory=list)
    critiques: list[CritiquePoint] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_response: str = ""


class ResearchQuery(BaseModel):
    """A research question or task to investigate."""

    question: str
    context: str = ""
    scope: str = ""  # constraints on the investigation
    prior_findings: list[Finding] = Field(default_factory=list)
    phase: ResearchPhase = ResearchPhase.QUESTION_FORMULATION
    depth: str = "phd"  # "survey", "detailed", "phd"
    domain_focus: str = "infonomics"


class ConversationMessage(BaseModel):
    """A message in the agent conversation history."""

    role: str  # "user", "assistant"
    content: str
    agent_role: AgentRole | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
