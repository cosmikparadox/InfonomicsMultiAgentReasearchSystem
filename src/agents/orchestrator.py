"""Orchestrator - coordinates the multi-agent research pipeline."""

from __future__ import annotations

import logging
from datetime import datetime

import anthropic
from rich.console import Console
from rich.panel import Panel

from src.agents.critic import Critic
from src.agents.literature_reviewer import LiteratureReviewer
from src.agents.synthesizer import Synthesizer
from src.agents.theorist import Theorist
from src.config.settings import Settings
from src.core.types import (
    Finding,
    ResearchOutput,
    ResearchPhase,
    ResearchQuery,
)

logger = logging.getLogger(__name__)
console = Console()


class ResearchSession:
    """Tracks the state and outputs of a single research session."""

    def __init__(self, query: ResearchQuery):
        self.query = query
        self.started_at = datetime.now()
        self.outputs: list[ResearchOutput] = []
        self.refinement_round = 0

    def add_output(self, output: ResearchOutput):
        self.outputs.append(output)

    def get_all_findings(self) -> list[Finding]:
        findings = []
        for output in self.outputs:
            findings.extend(output.findings)
        return findings

    def get_latest_by_phase(self, phase: ResearchPhase) -> ResearchOutput | None:
        for output in reversed(self.outputs):
            if output.phase == phase:
                return output
        return None


class Orchestrator:
    """Coordinates specialist agents through the research pipeline.

    Pipeline flow:
    1. Literature Review  -- survey existing knowledge
    2. Theoretical Analysis -- develop frameworks and models
    3. Critique -- adversarial review of findings
    4. (If critique score < threshold) Refinement loop back to step 2
    5. Synthesis -- integrate into coherent output
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)

        self.literature_reviewer = LiteratureReviewer(
            client=self.client,
            model=self.settings.default_model,
            max_tokens=self.settings.max_tokens_per_request,
        )
        self.theorist = Theorist(
            client=self.client,
            model=self.settings.default_model,
            max_tokens=self.settings.max_tokens_per_request,
        )
        self.critic = Critic(
            client=self.client,
            model=self.settings.critic_model,
            max_tokens=self.settings.max_tokens_per_request,
        )
        self.synthesizer = Synthesizer(
            client=self.client,
            model=self.settings.default_model,
            max_tokens=self.settings.max_tokens_per_request,
        )

    async def run(self, query: ResearchQuery) -> ResearchSession:
        """Execute the full research pipeline."""
        session = ResearchSession(query)

        console.print(Panel(
            f"[bold]Research Question:[/bold] {query.question}\n"
            f"[bold]Domain:[/bold] {query.domain_focus}\n"
            f"[bold]Depth:[/bold] {query.depth}",
            title="Starting Research Session",
            border_style="blue",
        ))

        # Phase 1: Literature Review
        console.print("\n[bold blue]Phase 1: Literature Review[/bold blue]")
        lit_output = await self.literature_reviewer.run(query)
        session.add_output(lit_output)
        console.print(f"  Found {len(lit_output.findings)} findings, {len(lit_output.citations)} citations")

        # Phase 2: Theoretical Analysis (informed by literature)
        console.print("\n[bold blue]Phase 2: Theoretical Analysis[/bold blue]")
        theory_query = ResearchQuery(
            question=query.question,
            context=query.context + f"\n\nLiterature Review Summary:\n{lit_output.summary}",
            scope=query.scope,
            prior_findings=lit_output.findings,
            phase=ResearchPhase.THEORETICAL_ANALYSIS,
            depth=query.depth,
            domain_focus=query.domain_focus,
        )
        theory_output = await self.theorist.run(theory_query)
        session.add_output(theory_output)
        console.print(f"  Developed {len(theory_output.findings)} theoretical propositions")

        # Phase 3+: Critique and refinement loop
        all_findings = session.get_all_findings()
        for round_num in range(self.settings.max_refinement_rounds):
            session.refinement_round = round_num + 1
            console.print(f"\n[bold yellow]Critique Round {round_num + 1}[/bold yellow]")

            critique_query = ResearchQuery(
                question=query.question,
                context=self._build_critique_context(session),
                prior_findings=all_findings,
                phase=ResearchPhase.CRITIQUE,
                depth=query.depth,
                domain_focus=query.domain_focus,
            )
            critique_output = await self.critic.run(critique_query)
            session.add_output(critique_output)

            rigor_score = critique_output.metadata.get("overall_rigor_score", 0.0)
            ready = critique_output.metadata.get("ready_for_synthesis", False)
            major_issues = sum(
                1 for c in critique_output.critiques if c.severity == "major"
            )

            console.print(
                f"  Rigor score: {rigor_score:.2f} | "
                f"Major issues: {major_issues} | "
                f"Ready for synthesis: {ready}"
            )

            if ready or rigor_score >= self.settings.critique_threshold:
                console.print("  [green]Passing critique threshold -- proceeding to synthesis[/green]")
                break

            if round_num < self.settings.max_refinement_rounds - 1:
                console.print("  [yellow]Refining theoretical analysis based on critique...[/yellow]")
                refinement_query = ResearchQuery(
                    question=query.question,
                    context=(
                        f"Previous analysis was critiqued. Address these issues:\n"
                        + "\n".join(
                            f"- [{c.severity}] {c.description} -> {c.suggested_remedy}"
                            for c in critique_output.critiques
                        )
                    ),
                    prior_findings=all_findings,
                    phase=ResearchPhase.THEORETICAL_ANALYSIS,
                    depth=query.depth,
                    domain_focus=query.domain_focus,
                )
                refined = await self.theorist.run(refinement_query)
                session.add_output(refined)
                all_findings = session.get_all_findings()

        # Final Phase: Synthesis
        console.print("\n[bold green]Final Phase: Synthesis[/bold green]")
        synthesis_query = ResearchQuery(
            question=query.question,
            context=self._build_synthesis_context(session),
            prior_findings=session.get_all_findings(),
            phase=ResearchPhase.SYNTHESIS,
            depth=query.depth,
            domain_focus=query.domain_focus,
        )
        synthesis_output = await self.synthesizer.run(synthesis_query)
        session.add_output(synthesis_output)

        console.print(Panel(
            f"[bold]Synthesized {len(synthesis_output.findings)} findings[/bold]\n"
            f"Session duration: {datetime.now() - session.started_at}\n"
            f"Refinement rounds: {session.refinement_round}\n"
            f"Total agent calls: {len(session.outputs)}",
            title="Research Session Complete",
            border_style="green",
        ))

        return session

    def _build_critique_context(self, session: ResearchSession) -> str:
        parts = []
        lit = session.get_latest_by_phase(ResearchPhase.LITERATURE_REVIEW)
        if lit:
            parts.append(f"=== LITERATURE REVIEW ===\n{lit.summary}\n{lit.detailed_content[:2000]}")

        theory = session.get_latest_by_phase(ResearchPhase.THEORETICAL_ANALYSIS)
        if theory:
            parts.append(f"=== THEORETICAL ANALYSIS ===\n{theory.summary}\n{theory.detailed_content[:2000]}")

        return "\n\n".join(parts)

    def _build_synthesis_context(self, session: ResearchSession) -> str:
        parts = []
        for output in session.outputs:
            parts.append(
                f"=== {output.agent_role.value.upper()} ({output.phase.value}) ===\n"
                f"Summary: {output.summary}\n"
                f"Findings: {len(output.findings)}\n"
                f"Content preview: {output.detailed_content[:1500]}"
            )
        return "\n\n".join(parts)
