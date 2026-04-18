"""Claude Code hook entry points for the research session harness.

Invoked from ``.claude/settings.json``. Two commands:

- ``pause_running``   (Stop / SubagentStop hook): any session still marked
  ``in_progress`` is flipped to ``paused`` and gets a ``session_paused`` event,
  so we always know when the harness died mid-pipeline.
- ``announce_resumable`` (SessionStart hook): prints resumable sessions so the
  agent sees them in the transcript and can offer to continue.

Both commands are safe no-ops when there are no sessions.
"""

from __future__ import annotations

import sys
from datetime import datetime

from src.session import find_resumable, mark_paused


def pause_running() -> int:
    sessions = find_resumable()
    if not sessions:
        return 0
    for s in sessions:
        # Only flip true IN_PROGRESS sessions — leave PAUSED ones alone.
        if s.status.value == "in_progress":
            mark_paused(s, reason="harness_stop_hook")
            print(
                f"[research-harness] paused session {s.session_id} "
                f"(next_phase={s.next_phase.value if s.next_phase else '-'})",
                file=sys.stderr,
            )
    return 0


def announce_resumable() -> int:
    sessions = find_resumable()
    if not sessions:
        return 0
    print(
        f"\n[research-harness] {len(sessions)} resumable session(s) "
        f"as of {datetime.now().isoformat(timespec='seconds')}:"
    )
    for s in sessions:
        next_phase = s.next_phase.value if s.next_phase else "-"
        print(
            f"  - {s.session_id}  status={s.status.value}  "
            f"next={next_phase}  outputs={len(s.outputs)}  "
            f"Q={s.question[:80]}"
        )
    print(
        "To continue one, call resume_session(<id>) from src.session "
        "or ask the user which to resume.\n"
    )
    return 0


COMMANDS = {
    "pause_running": pause_running,
    "announce_resumable": announce_resumable,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: python -m src.hooks {{{'|'.join(COMMANDS)}}}", file=sys.stderr)
        return 2
    return COMMANDS[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
