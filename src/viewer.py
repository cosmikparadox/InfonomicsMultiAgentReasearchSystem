"""CLI viewer for browsing, tailing, and resuming research sessions.

Usage:
    research-viewer                       # list all sessions
    research-viewer list                  # list all sessions
    research-viewer resumable             # list in-progress / paused sessions
    research-viewer show <id|path>        # show one session in detail
    research-viewer tail <id|path> [-n]   # print the event log
"""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models import SessionStatus
from src.session import (
    event_log_path,
    find_resumable,
    list_sessions,
    load_session,
    read_events,
)

console = Console()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def show_session_list() -> None:
    sessions = list_sessions()
    if not sessions:
        console.print("[yellow]No research sessions found.[/yellow]")
        return

    table = Table(title="Research Sessions")
    table.add_column("#", style="dim")
    table.add_column("Session ID / File")
    table.add_column("Question")
    table.add_column("Status")
    table.add_column("Phase")
    table.add_column("Outputs", justify="right")
    table.add_column("Last checkpoint")

    for i, path in enumerate(sessions, 1):
        try:
            session = load_session(path)
        except Exception as exc:
            table.add_row(str(i), path.name, f"[red]unreadable: {exc}[/red]", "", "", "", "")
            continue

        status_color = {
            SessionStatus.COMPLETED: "green",
            SessionStatus.IN_PROGRESS: "yellow",
            SessionStatus.PAUSED: "magenta",
            SessionStatus.FAILED: "red",
        }.get(session.status, "white")
        phase = (
            session.current_phase.value
            if session.current_phase
            else (session.next_phase.value if session.next_phase else "-")
        )
        last_ckpt = (
            session.last_checkpoint_at.strftime("%Y-%m-%d %H:%M:%S")
            if session.last_checkpoint_at
            else "-"
        )
        ident = session.session_id if session.session_id else path.name
        table.add_row(
            str(i),
            ident,
            session.question[:60] + ("..." if len(session.question) > 60 else ""),
            f"[{status_color}]{session.status.value}[/{status_color}]",
            phase,
            str(len(session.outputs)),
            last_ckpt,
        )

    console.print(table)


def show_resumable() -> None:
    sessions = find_resumable()
    if not sessions:
        console.print("[green]No sessions waiting to resume.[/green]")
        return
    console.print(f"[bold]{len(sessions)} session(s) can be resumed:[/bold]")
    for s in sessions:
        next_phase = s.next_phase.value if s.next_phase else "-"
        console.print(
            f"  [yellow]{s.session_id}[/yellow] "
            f"({s.status.value}, next={next_phase}, outputs={len(s.outputs)}) "
            f"— {s.question[:80]}"
        )


def show_session_detail(ref: str) -> None:
    session = load_session(ref)

    next_phase = session.next_phase.value if session.next_phase else "-"
    current = session.current_phase.value if session.current_phase else "-"
    console.print(
        Panel(
            f"[bold]Session ID:[/bold] {session.session_id}\n"
            f"[bold]Question:[/bold] {session.question}\n"
            f"[bold]Domain:[/bold] {session.domain}\n"
            f"[bold]Started:[/bold] {session.started_at}\n"
            f"[bold]Status:[/bold] {session.status.value}\n"
            f"[bold]Current phase:[/bold] {current}\n"
            f"[bold]Next phase:[/bold] {next_phase}\n"
            f"[bold]Refinement rounds:[/bold] {session.refinement_rounds}\n"
            f"[bold]Last checkpoint:[/bold] {session.last_checkpoint_at}",
            title="Research Session",
            border_style="blue",
        )
    )

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


def tail_events(ref: str, n: int | None = None) -> None:
    # Accept either a session_id or a direct path to a snapshot.
    session_id = ref
    candidate = Path(ref)
    if candidate.exists() and candidate.suffix == ".json":
        session_id = load_session(candidate).session_id

    log_path = event_log_path(session_id)
    if not log_path.exists():
        console.print(f"[yellow]No event log for {session_id}[/yellow]")
        return

    events = read_events(session_id)
    if n is not None:
        events = events[-n:]
    for e in events:
        phase = e.phase.value if e.phase else "-"
        role = e.role.value if e.role else "-"
        console.print(
            f"[dim]{e.timestamp.strftime('%H:%M:%S')}[/dim] "
            f"[bold]{e.event_type}[/bold] "
            f"phase={phase} role={role} "
            f"{e.message[:120]}"
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "list":
        show_session_list()
        return

    cmd = args[0]
    if cmd == "resumable":
        show_resumable()
    elif cmd == "show" and len(args) >= 2:
        show_session_detail(args[1])
    elif cmd == "tail" and len(args) >= 2:
        n = None
        if len(args) >= 4 and args[2] in ("-n", "--lines"):
            n = int(args[3])
        tail_events(args[1], n)
    else:
        # Back-compat: single arg treated as a session path/id for detail view.
        show_session_detail(cmd)


if __name__ == "__main__":
    main()
