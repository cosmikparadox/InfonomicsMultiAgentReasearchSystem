"""Critic Agent - provides adversarial review and quality control."""

from __future__ import annotations

import json
import logging

from src.core.agent import BaseAgent
from src.core.types import (
    AgentRole,
    CritiquePoint,
    ResearchOutput,
    ResearchPhase,
    ResearchQuery,
)

logger = logging.getLogger(__name__)


class Critic(BaseAgent):
    """Agent specialized in adversarial critique, identifying weaknesses,
    logical gaps, methodological issues, and unstated assumptions."""

    role = AgentRole.CRITIC

    def system_prompt(self, query: ResearchQuery) -> str:
        return """You are a rigorous academic reviewer and devil's advocate specializing \
in infonomics and information economics.

Your task is to critically evaluate research findings, theoretical arguments, and \
methodological choices. You operate at the standard of a top-tier journal reviewer \
or PhD dissertation committee member.

Your response MUST be structured as valid JSON with the following schema:
{
    "summary": "Overall assessment of the research quality",
    "detailed_content": "Full critical analysis",
    "critiques": [
        {
            "target": "What specific claim/method/argument is being critiqued",
            "issue_type": "methodological|logical|empirical|scope|assumption|completeness",
            "description": "Detailed description of the issue",
            "severity": "major|minor|suggestion",
            "suggested_remedy": "How to address this issue"
        }
    ],
    "strengths": ["Strength 1", "Strength 2"],
    "overall_rigor_score": 0.0,
    "ready_for_synthesis": false,
    "required_revisions": ["What must be fixed before synthesis"]
}

Guidelines:
- Be constructive but unflinching -- identify real weaknesses
- Check for: logical fallacies, unstated assumptions, selection bias, \
  confounding factors, overgeneralization, circular reasoning
- Evaluate methodological soundness
- Assess whether claims are supported by the evidence presented
- Consider alternative explanations for findings
- Check for internal consistency across findings
- Evaluate the scope and boundaries of the analysis
- Flag speculative claims that are presented as established facts
- The rigor_score should be 0.0-1.0 where 1.0 is publishable quality"""

    def parse_response(self, raw_response: str, query: ResearchQuery) -> ResearchOutput:
        try:
            text = raw_response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            logger.warning("Could not parse structured JSON from critic, using raw")
            return ResearchOutput(
                agent_role=self.role,
                phase=ResearchPhase.CRITIQUE,
                summary="Critique completed (unstructured)",
                detailed_content=raw_response,
            )

        critiques = [
            CritiquePoint(
                target=c.get("target", ""),
                issue_type=c.get("issue_type", ""),
                description=c.get("description", ""),
                severity=c.get("severity", "minor"),
                suggested_remedy=c.get("suggested_remedy", ""),
            )
            for c in data.get("critiques", [])
        ]

        return ResearchOutput(
            agent_role=self.role,
            phase=ResearchPhase.CRITIQUE,
            summary=data.get("summary", ""),
            detailed_content=data.get("detailed_content", ""),
            critiques=critiques,
            metadata={
                "strengths": data.get("strengths", []),
                "overall_rigor_score": data.get("overall_rigor_score", 0.0),
                "ready_for_synthesis": data.get("ready_for_synthesis", False),
                "required_revisions": data.get("required_revisions", []),
            },
        )
