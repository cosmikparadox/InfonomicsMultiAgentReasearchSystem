"""Synthesizer Agent - integrates findings into coherent research output."""

from __future__ import annotations

import json
import logging

from src.core.agent import BaseAgent
from src.core.types import (
    AgentRole,
    Citation,
    Confidence,
    Finding,
    ResearchOutput,
    ResearchPhase,
    ResearchQuery,
)

logger = logging.getLogger(__name__)


class Synthesizer(BaseAgent):
    """Agent specialized in synthesizing research from multiple agents
    into a coherent, publication-quality research output."""

    role = AgentRole.SYNTHESIZER

    def system_prompt(self, query: ResearchQuery) -> str:
        return """You are a senior academic researcher specializing in producing \
publication-quality synthesis of multi-source research in infonomics and \
information economics.

Your task is to integrate findings from literature review, theoretical analysis, \
and critical review into a coherent, well-structured research output suitable for \
a PhD dissertation chapter or journal submission.

Your response MUST be structured as valid JSON with the following schema:
{
    "summary": "Abstract-quality summary of the synthesized research",
    "detailed_content": "Full synthesized research output, structured as an academic paper section",
    "findings": [
        {
            "claim": "Synthesized finding",
            "evidence": "Integrated evidence from multiple sources",
            "confidence": "high|medium|low|speculative",
            "methodology": "How the synthesis was achieved",
            "limitations": "Remaining limitations after synthesis"
        }
    ],
    "citations": [
        {
            "title": "Paper title",
            "authors": ["Author"],
            "year": 2024,
            "source": "Source",
            "summary": "Relevance"
        }
    ],
    "contribution": "What this research adds to the field",
    "future_directions": ["Direction 1", "Direction 2"],
    "practical_implications": ["Implication 1"]
}

Guidelines:
- Integrate, don't just concatenate -- find connections and tensions across inputs
- Resolve contradictions explicitly, explaining which position is better supported
- Maintain academic rigor while being accessible
- Clearly state the contribution to the field
- Distinguish established knowledge from novel synthesis
- Propose concrete future research directions
- Consider practical implications for information valuation and data economics"""

    def parse_response(self, raw_response: str, query: ResearchQuery) -> ResearchOutput:
        try:
            text = raw_response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            logger.warning("Could not parse structured JSON from synthesizer, using raw")
            return ResearchOutput(
                agent_role=self.role,
                phase=ResearchPhase.SYNTHESIS,
                summary="Synthesis completed (unstructured)",
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

        citations = [
            Citation(
                title=c.get("title", ""),
                authors=c.get("authors", []),
                year=c.get("year"),
                source=c.get("source", ""),
                summary=c.get("summary", ""),
            )
            for c in data.get("citations", [])
        ]

        return ResearchOutput(
            agent_role=self.role,
            phase=ResearchPhase.SYNTHESIS,
            summary=data.get("summary", ""),
            detailed_content=data.get("detailed_content", ""),
            findings=findings,
            citations=citations,
            metadata={
                "contribution": data.get("contribution", ""),
                "future_directions": data.get("future_directions", []),
                "practical_implications": data.get("practical_implications", []),
            },
        )
