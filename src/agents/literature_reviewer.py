"""Literature Review Agent - surveys and synthesizes existing research."""

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


class LiteratureReviewer(BaseAgent):
    """Agent specialized in surveying existing literature and identifying key theories,
    findings, gaps, and debates in the infonomics domain."""

    role = AgentRole.LITERATURE_REVIEWER

    def system_prompt(self, query: ResearchQuery) -> str:
        return """You are a PhD-level research assistant specializing in literature review \
for infonomics and information economics.

Your task is to provide a comprehensive, rigorous survey of relevant literature on the \
given research question. You operate at the level expected of a doctoral dissertation \
literature review.

Your response MUST be structured as valid JSON with the following schema:
{
    "summary": "Executive summary of the literature landscape",
    "detailed_content": "Full narrative literature review with proper academic structure",
    "findings": [
        {
            "claim": "Key finding or consensus from the literature",
            "evidence": "Supporting evidence and key papers",
            "confidence": "high|medium|low|speculative",
            "methodology": "How this finding was established in the literature",
            "limitations": "Known limitations or caveats"
        }
    ],
    "citations": [
        {
            "title": "Paper title",
            "authors": ["Author 1", "Author 2"],
            "year": 2024,
            "source": "Journal or conference name",
            "summary": "Brief summary of the paper's relevance"
        }
    ],
    "research_gaps": ["Gap 1", "Gap 2"],
    "key_debates": ["Debate 1", "Debate 2"],
    "theoretical_frameworks": ["Framework 1", "Framework 2"]
}

Guidelines:
- Prioritize seminal works and recent developments
- Identify competing theoretical frameworks
- Highlight methodological approaches used in the field
- Note research gaps that the current question might address
- Be explicit about the boundaries of your knowledge
- Distinguish between well-established findings and emerging/contested ideas
- Use proper academic language and reasoning"""

    def parse_response(self, raw_response: str, query: ResearchQuery) -> ResearchOutput:
        try:
            # Try to extract JSON from the response
            text = raw_response.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            logger.warning("Could not parse structured JSON from literature reviewer, using raw")
            return ResearchOutput(
                agent_role=self.role,
                phase=ResearchPhase.LITERATURE_REVIEW,
                summary="Literature review completed (unstructured)",
                detailed_content=raw_response,
            )

        findings = []
        for f in data.get("findings", []):
            findings.append(
                Finding(
                    claim=f.get("claim", ""),
                    evidence=f.get("evidence", ""),
                    confidence=Confidence(f.get("confidence", "medium")),
                    methodology=f.get("methodology", ""),
                    limitations=f.get("limitations", ""),
                )
            )

        citations = []
        for c in data.get("citations", []):
            citations.append(
                Citation(
                    title=c.get("title", ""),
                    authors=c.get("authors", []),
                    year=c.get("year"),
                    source=c.get("source", ""),
                    summary=c.get("summary", ""),
                )
            )

        return ResearchOutput(
            agent_role=self.role,
            phase=ResearchPhase.LITERATURE_REVIEW,
            summary=data.get("summary", ""),
            detailed_content=data.get("detailed_content", ""),
            findings=findings,
            citations=citations,
            metadata={
                "research_gaps": data.get("research_gaps", []),
                "key_debates": data.get("key_debates", []),
                "theoretical_frameworks": data.get("theoretical_frameworks", []),
            },
        )
