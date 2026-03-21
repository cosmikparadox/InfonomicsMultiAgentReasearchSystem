#!/usr/bin/env python3
"""
publish.py — CLI for the Infonomics Research Dashboard.

Usage:
    python publish.py                # Open dashboard + report in browser, list outputs
    python publish.py --open         # Open dashboard.html in default browser
    python publish.py --list         # List all session outputs in data/outputs/
    python publish.py --serve        # Start local HTTP server on port 8080

No dependencies beyond Python 3.8+ stdlib.
"""

import argparse
import http.server
import functools
import json
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "outputs"
DASHBOARD_FILE = BASE_DIR / "dashboard.html"
REPORT_FILE = BASE_DIR / "Ottoman_report.html"
DEFAULT_PORT = 8080


def list_outputs() -> list[dict]:
    """List all files in data/outputs/ with metadata."""
    if not OUTPUT_DIR.exists():
        print(f"  Output directory not found: {OUTPUT_DIR}")
        return []

    entries = []
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_dir():
            continue
        stat = f.stat()
        entries.append({
            "name": f.name,
            "path": str(f),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "suffix": f.suffix.lower(),
        })
    return entries


def print_outputs(entries: list[dict]) -> None:
    """Print a formatted table of output files."""
    if not entries:
        print("  No output files found.")
        return

    # Column widths
    name_width = max(len(e["name"]) for e in entries)
    name_width = max(name_width, 4)  # minimum "Name" header

    print(f"\n  {'Name':<{name_width}}   {'Type':>5}   {'Size':>10}   {'Modified'}")
    print(f"  {'-' * name_width}   -----   ----------   -------------------")

    for e in entries:
        size_str = format_size(e["size"])
        mod_str = e["modified"].strftime("%Y-%m-%d %H:%M:%S")
        suffix = e["suffix"].lstrip(".").upper() or "—"
        print(f"  {e['name']:<{name_width}}   {suffix:>5}   {size_str:>10}   {mod_str}")

    print(f"\n  {len(entries)} file(s) in {OUTPUT_DIR}\n")


def format_size(size_bytes: int) -> str:
    """Format byte count as human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def view_file_cli(entries: list[dict]) -> None:
    """Simple interactive CLI to view research output files."""
    if not entries:
        return

    while True:
        print("\nEnter file number to view (or 'q' to quit):")
        for i, e in enumerate(entries, 1):
            size_str = format_size(e["size"])
            print(f"  [{i}] {e['name']} ({size_str})")

        try:
            choice = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice.lower() in ("q", "quit", "exit", ""):
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(entries):
                entry = entries[idx]
                print(f"\n{'=' * 60}")
                print(f"  {entry['name']}")
                print(f"{'=' * 60}\n")

                path = Path(entry["path"])
                content = path.read_text(encoding="utf-8", errors="replace")

                # For JSON files, pretty-print
                if entry["suffix"] == ".json":
                    try:
                        parsed = json.loads(content)
                        content = json.dumps(parsed, indent=2)
                    except json.JSONDecodeError:
                        pass

                # Truncate very large files in CLI view
                lines = content.splitlines()
                if len(lines) > 200:
                    print("\n".join(lines[:200]))
                    print(f"\n  ... ({len(lines) - 200} more lines, "
                          f"open in browser for full view)")
                else:
                    print(content)

                print(f"\n{'=' * 60}")
            else:
                print(f"  Invalid selection. Choose 1-{len(entries)}.")
        except ValueError:
            print("  Invalid input. Enter a number or 'q' to quit.")


def open_dashboard() -> None:
    """Open dashboard.html in the default browser."""
    if not DASHBOARD_FILE.exists():
        print(f"  Error: {DASHBOARD_FILE} not found.")
        sys.exit(1)
    url = DASHBOARD_FILE.as_uri()
    print(f"  Opening dashboard: {url}")
    webbrowser.open(url)


def open_report() -> None:
    """Open Ottoman_report.html in the default browser."""
    if not REPORT_FILE.exists():
        print(f"  Warning: {REPORT_FILE} not found, skipping.")
        return
    url = REPORT_FILE.as_uri()
    print(f"  Opening report: {url}")
    webbrowser.open(url)


def serve(port: int = DEFAULT_PORT) -> None:
    """Start a local HTTP server to serve HTML files and data/outputs/."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(BASE_DIR))

    print(f"\n  Infonomics Research Dashboard Server")
    print(f"  {'=' * 40}")
    print(f"  Dashboard:  http://localhost:{port}/dashboard.html")
    print(f"  Report:     http://localhost:{port}/Ottoman_report.html")
    print(f"  Outputs:    http://localhost:{port}/data/outputs/")
    print(f"  {'=' * 40}")
    print(f"  Serving from: {BASE_DIR}")
    print(f"  Press Ctrl+C to stop.\n")

    try:
        with http.server.HTTPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"  Error: Port {port} is already in use. Try a different port.")
        else:
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Infonomics Research Dashboard CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  python publish.py              Interactive mode: list outputs, view files
  python publish.py --open       Open dashboard in default browser
  python publish.py --list       List all research outputs
  python publish.py --serve      Start HTTP server on port 8080
  python publish.py --serve 9000 Start HTTP server on port 9000
""",
    )
    parser.add_argument(
        "--open", action="store_true",
        help="Open dashboard.html in default browser",
    )
    parser.add_argument(
        "--list", action="store_true", dest="list_files",
        help="List all session outputs in data/outputs/",
    )
    parser.add_argument(
        "--serve", nargs="?", const=DEFAULT_PORT, type=int, metavar="PORT",
        help=f"Start local HTTP server (default port: {DEFAULT_PORT})",
    )

    args = parser.parse_args()

    print("\n  Infonomics Multi-Agent Research System")
    print(f"  {'=' * 40}\n")

    # If a specific flag is given, run that action and exit
    if args.serve is not None:
        serve(args.serve)
        return

    if args.open:
        open_dashboard()
        open_report()
        return

    if args.list_files:
        entries = list_outputs()
        print_outputs(entries)
        return

    # Default: list outputs and launch interactive viewer
    entries = list_outputs()
    print_outputs(entries)

    # Also show available HTML assets
    html_files = [f for f in [DASHBOARD_FILE, REPORT_FILE] if f.exists()]
    if html_files:
        print("  HTML assets:")
        for hf in html_files:
            print(f"    - {hf.name}")
        print()
        print("  Tip: Use --open to launch in browser, --serve to start HTTP server.\n")

    # Interactive file viewer
    if entries:
        view_file_cli(entries)


if __name__ == "__main__":
    main()
