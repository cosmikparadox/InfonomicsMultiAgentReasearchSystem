"""Theorist Agent - develops and analyzes theoretical frameworks."""

from __future__ import annotations

import json
import logging

from src.core.agent import BaseAgent
from src.core.types import (
    AgentRole,
    Confidence,
    Finding,
    ResearchOutput,
    ResearchPhase,
    ResearchQuery,
)

logger = logging.getLogger(__name__)


class Theorist(BaseAgent):
    """Agent specialized in theoretical analysis, model building, and
    framework development for infonomics research."""

    role = AgentRole.THEORIST

    def system_prompt(self, query: ResearchQuery) -> str:
        return """You are a PhD-level theoretical economist specializing in infonomics \
and information economics.

Your task is to develop rigorous theoretical analysis, propose models, and build \
conceptual frameworks relevant to the research question. You think at the level of \
a doctoral dissertation's theoretical contribution.

Your response MUST be structured as valid JSON with the following schema:
{
    "summary": "Executive summary of theoretical analysis",
    "detailed_content": "Full theoretical analysis with formal reasoning",
    "findings": [
        {
            "claim": "Theoretical proposition or model prediction",
            "evidence": "Logical reasoning or formal derivation supporting this",
            "confidence": "high|medium|low|speculative",
            "methodology": "Theoretical approach used (game theory, mechanism design, etc.)",
            "limitations": "Assumptions and boundary conditions"
        }
    ],
    "proposed_frameworks": [
        {
            "name": "Framework name",
            "description": "What it explains",
            "key_assumptions": ["Assumption 1"],
            "testable_predictions": ["Prediction 1"],
            "relationship_to_existing_theory": "How it extends/challenges current thinking"
        }
    ],
    "formal_models": [
        {
            "name": "Model name",
            "variables": {"var": "description"},
            "relationships": "Formal or semi-formal description",
            "equilibrium_conditions": "If applicable"
        }
    ]
}

Guidelines:
- Build on established economic theory (information economics, mechanism design, etc.)
- Be explicit about assumptions and their implications
- Propose testable predictions where possible
- Consider both micro and macro perspectives on information value
- Reference relevant formal models (Stiglitz-Grossman, Akerlof, Shapley value, etc.)
- Distinguish between normative and positive analysis
- Consider behavioral and institutional dimensions"""

    def parse_response(self, raw_response: str, query: ResearchQuery) -> ResearchOutput:
        try:
            text = raw_response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            logger.warning("Could not parse structured JSON from theorist, using raw")
            return ResearchOutput(
                agent_role=self.role,
                phase=ResearchPhase.THEORETICAL_ANALYSIS,
                summary="Theoretical analysis completed (unstructured)",
                detailed_content=raw_response,
            )

        findings = [
            Finding(
                claim=f.get("claim", ""),
                evidence=f.get("evidence", ""),
                confidence=Confidence(f.get("confidence", "medium")),
                methodology=f.get("methodology", ""),
                limitations=f.get("limitations", ""),
            )
            for f in data.get("findings", [])
        ]

        return ResearchOutput(
            agent_role=self.role,
            phase=ResearchPhase.THEORETICAL_ANALYSIS,
            summary=data.get("summary", ""),
            detailed_content=data.get("detailed_content", ""),
            findings=findings,
            metadata={
                "proposed_frameworks": data.get("proposed_frameworks", []),
                "formal_models": data.get("formal_models", []),
            },
        )
