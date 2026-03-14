"""CLI viewer for browsing past research sessions."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.session import list_sessions, load_session

console = Console()


def show_session_list():
    """Display all saved research sessions."""
    sessions = list_sessions()
    if not sessions:
        console.print("[yellow]No research sessions found.[/yellow]")
        return

    table = Table(title="Research Sessions")
    table.add_column("#", style="dim")
    table.add_column("File")
    table.add_column("Question")
    table.add_column("Status")
    table.add_column("Outputs")

    for i, path in enumerate(sessions, 1):
        session = load_session(path)
        table.add_row(
            str(i),
            path.name,
            session.question[:60] + ("..." if len(session.question) > 60 else ""),
            session.status,
            str(len(session.outputs)),
        )

    console.print(table)


def show_session_detail(filepath: str):
    """Display details of a specific research session."""
    session = load_session(filepath)

    console.print(Panel(
        f"[bold]Question:[/bold] {session.question}\n"
        f"[bold]Domain:[/bold] {session.domain}\n"
        f"[bold]Started:[/bold] {session.started_at}\n"
        f"[bold]Status:[/bold] {session.status}\n"
        f"[bold]Refinement rounds:[/bold] {session.refinement_rounds}",
        title="Research Session",
        border_style="blue",
    ))

    for output in session.outputs:
        console.print(f"\n[bold]{output.agent_role.value} — {output.phase.value}[/bold]")
        console.print(f"  Summary: {output.summary[:200]}")
        if output.findings:
            console.print(f"  Findings: {len(output.findings)}")
            for f in output.findings[:3]:
                console.print(f"    [{f.confidence.value}] {f.claim[:100]}")
        if output.critiques:
            console.print(f"  Critiques: {len(output.critiques)}")
            for c in output.critiques[:3]:
                console.print(f"    [{c.severity}] {c.description[:100]}")


def main():
    if len(sys.argv) > 1:
        show_session_detail(sys.argv[1])
    else:
        show_session_list()


if __name__ == "__main__":
    main()
