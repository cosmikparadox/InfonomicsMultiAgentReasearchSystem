"""Base agent class for all research agents."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import anthropic

from src.core.types import (
    AgentRole,
    ConversationMessage,
    ResearchOutput,
    ResearchQuery,
)

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all research agents.

    Each agent wraps a Claude API call with a specialized system prompt
    and structured output parsing. Agents maintain conversation history
    for multi-turn reasoning within a research session.
    """

    role: AgentRole
    model: str = "claude-sonnet-4-6"

    def __init__(
        self,
        client: anthropic.Anthropic,
        model: str | None = None,
        max_tokens: int = 8192,
    ):
        self.client = client
        if model:
            self.model = model
        self.max_tokens = max_tokens
        self.conversation_history: list[ConversationMessage] = []

    @abstractmethod
    def system_prompt(self, query: ResearchQuery) -> str:
        """Build the system prompt for this agent's role."""
        ...

    @abstractmethod
    def parse_response(self, raw_response: str, query: ResearchQuery) -> ResearchOutput:
        """Parse the raw LLM response into structured output."""
        ...

    async def run(self, query: ResearchQuery) -> ResearchOutput:
        """Execute this agent's research task."""
        system = self.system_prompt(query)
        user_message = self._build_user_message(query)

        self.conversation_history.append(
            ConversationMessage(role="user", content=user_message, agent_role=self.role)
        )

        messages = [{"role": m.role, "content": m.content} for m in self.conversation_history]

        logger.info(f"[{self.role.value}] Sending request to {self.model}")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=messages,
        )

        raw_text = response.content[0].text

        self.conversation_history.append(
            ConversationMessage(role="assistant", content=raw_text, agent_role=self.role)
        )

        logger.info(f"[{self.role.value}] Received response ({len(raw_text)} chars)")

        output = self.parse_response(raw_text, query)
        output.raw_response = raw_text
        return output

    def _build_user_message(self, query: ResearchQuery) -> str:
        """Build the user message from a research query."""
        parts = [f"Research Question: {query.question}"]

        if query.context:
            parts.append(f"\nContext: {query.context}")
        if query.scope:
            parts.append(f"\nScope/Constraints: {query.scope}")
        if query.prior_findings:
            findings_text = "\n".join(
                f"- [{f.confidence.value}] {f.claim}" for f in query.prior_findings
            )
            parts.append(f"\nPrior Findings:\n{findings_text}")

        parts.append(f"\nDepth: {query.depth}")
        parts.append(f"\nDomain Focus: {query.domain_focus}")

        return "\n".join(parts)

    def reset_history(self):
        """Clear conversation history for a fresh session."""
        self.conversation_history.clear()
