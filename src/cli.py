"""CLI entry point for the research system."""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console

from src.agents.orchestrator import Orchestrator
from src.config.settings import Settings
from src.core.types import ResearchQuery

console = Console()


def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def save_session(session, output_dir: str):
    """Save research session outputs to JSON."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_path / f"session_{timestamp}.json"

    data = {
        "query": session.query.model_dump(mode="json"),
        "started_at": session.started_at.isoformat(),
        "refinement_rounds": session.refinement_round,
        "outputs": [o.model_dump(mode="json") for o in session.outputs],
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

    console.print(f"\nSession saved to: {filename}")
    return filename


async def run_research(question: str, context: str = "", domain: str = "infonomics"):
    """Run a research session."""
    settings = Settings()
    setup_logging(settings.log_level)

    query = ResearchQuery(
        question=question,
        context=context,
        domain_focus=domain,
        depth="phd",
    )

    orchestrator = Orchestrator(settings)
    session = await orchestrator.run(query)
    save_session(session, settings.output_dir)

    # Print final synthesis
    final = session.outputs[-1]
    console.print("\n[bold]===== FINAL SYNTHESIS =====[/bold]\n")
    console.print(final.summary)
    console.print("\n[bold]Key Findings:[/bold]")
    for i, finding in enumerate(final.findings, 1):
        console.print(f"  {i}. [{finding.confidence.value}] {finding.claim}")

    return session


def main():
    if len(sys.argv) < 2:
        console.print("[bold]Usage:[/bold] research \"Your research question here\"")
        console.print("\n[bold]Example:[/bold]")
        console.print('  research "How should organizations value their data assets using infonomics frameworks?"')
        sys.exit(1)

    question = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else ""

    asyncio.run(run_research(question, context))


if __name__ == "__main__":
    main()
