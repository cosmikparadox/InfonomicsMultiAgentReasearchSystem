#!/usr/bin/env python3
"""
publish.py — Generate a self-contained research dashboard from data/outputs/.

Usage:
    python publish.py              # generates dashboard.html
    python publish.py --open       # generates and opens in browser

No dependencies beyond Python 3.8+ stdlib.
"""

import csv
import html
import io
import json
import os
import sys
import webbrowser
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "data" / "outputs"
DASHBOARD_FILE = Path(__file__).parent / "dashboard.html"


def read_outputs(output_dir: Path) -> list[dict]:
    """Read all files from the output directory."""
    entries = []
    for f in sorted(output_dir.iterdir()):
        if f.is_dir():
            continue
        ext = f.suffix.lower()
        if ext not in (".md", ".csv", ".json", ".txt"):
            continue
        content = f.read_text(encoding="utf-8", errors="replace")
        entries.append({
            "name": f.name,
            "type": ext.lstrip("."),
            "content": content,
            "size": f.stat().st_size,
        })
    return entries


def csv_to_html_table(raw_csv: str) -> str:
    """Convert CSV text to an HTML table string."""
    reader = csv.reader(io.StringIO(raw_csv))
    rows = list(reader)
    if not rows:
        return "<p>Empty CSV</p>"
    header, body = rows[0], rows[1:]
    ths = "".join(f"<th>{html.escape(h)}</th>" for h in header)
    trs = []
    for row in body:
        tds = "".join(f"<td>{html.escape(c)}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return f"<table><thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody></table>"


def build_dashboard(entries: list[dict]) -> str:
    """Build the full HTML dashboard."""

    # Prepare entries JSON for JS consumption (markdown files)
    # and pre-render CSV tables
    nav_items = []
    content_sections = []

    for i, entry in enumerate(entries):
        eid = f"entry-{i}"
        label = entry["name"]
        size_kb = entry["size"] / 1024
        badge = entry["type"].upper()

        nav_items.append(
            f'<li data-target="{eid}" data-name="{html.escape(label.lower())}" '
            f'class="nav-item" onclick="showEntry(\'{eid}\')">'
            f'<span class="badge badge-{entry["type"]}">{badge}</span>'
            f'<span class="nav-label">{html.escape(label)}</span>'
            f'<span class="nav-size">{size_kb:.0f} KB</span></li>'
        )

        if entry["type"] == "csv":
            table_html = csv_to_html_table(entry["content"])
            inner = f'<div class="csv-wrapper">{table_html}</div>'
        elif entry["type"] == "json":
            try:
                parsed = json.loads(entry["content"])
                pretty = json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                pretty = entry["content"]
            inner = f'<pre class="json-block"><code>{html.escape(pretty)}</code></pre>'
        else:
            # Markdown / text — rendered client-side by marked.js
            inner = (
                f'<div class="md-content" id="md-{eid}">'
                f'<pre class="md-raw" style="display:none">{html.escape(entry["content"])}</pre>'
                f'<div class="md-rendered"></div></div>'
            )

        content_sections.append(
            f'<section id="{eid}" class="entry-section" style="display:none;">'
            f'<h2 class="entry-title">{html.escape(label)}</h2>'
            f'{inner}</section>'
        )

    nav_html = "\n".join(nav_items)
    content_html = "\n".join(content_sections)
    count = len(entries)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Infonomics Research Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root {{
  --bg: #0d1117; --bg2: #161b22; --bg3: #21262d;
  --fg: #c9d1d9; --fg2: #8b949e; --accent: #58a6ff;
  --accent2: #388bfd; --border: #30363d; --green: #3fb950;
  --orange: #d29922; --red: #f85149; --purple: #bc8cff;
}}
[data-theme="light"] {{
  --bg: #ffffff; --bg2: #f6f8fa; --bg3: #e8eaed;
  --fg: #1f2328; --fg2: #656d76; --accent: #0969da;
  --accent2: #0550ae; --border: #d0d7de; --green: #1a7f37;
  --orange: #9a6700; --red: #cf222e; --purple: #8250df;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg); color: var(--fg); display: flex; height: 100vh; overflow: hidden;
}}
/* Sidebar */
.sidebar {{
  width: 320px; min-width: 260px; background: var(--bg2); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; overflow: hidden;
}}
.sidebar-header {{
  padding: 20px; border-bottom: 1px solid var(--border);
}}
.sidebar-header h1 {{
  font-size: 16px; font-weight: 600; margin-bottom: 4px;
}}
.sidebar-header .subtitle {{
  font-size: 12px; color: var(--fg2);
}}
.search-box {{
  margin: 12px 16px; padding: 8px 12px; background: var(--bg3); border: 1px solid var(--border);
  border-radius: 6px; color: var(--fg); font-size: 14px; width: calc(100% - 32px); outline: none;
}}
.search-box:focus {{ border-color: var(--accent); }}
.search-box::placeholder {{ color: var(--fg2); }}
.nav-list {{
  list-style: none; overflow-y: auto; flex: 1; padding: 8px 0;
}}
.nav-item {{
  display: flex; align-items: center; gap: 8px; padding: 10px 16px;
  cursor: pointer; font-size: 13px; transition: background 0.15s;
}}
.nav-item:hover {{ background: var(--bg3); }}
.nav-item.active {{ background: var(--bg3); border-left: 3px solid var(--accent); }}
.nav-label {{ flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.nav-size {{ font-size: 11px; color: var(--fg2); white-space: nowrap; }}
.badge {{
  font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;
  text-transform: uppercase; white-space: nowrap;
}}
.badge-md {{ background: var(--accent); color: #fff; }}
.badge-csv {{ background: var(--green); color: #fff; }}
.badge-json {{ background: var(--purple); color: #fff; }}
.badge-txt {{ background: var(--orange); color: #fff; }}
.sidebar-footer {{
  padding: 12px 16px; border-top: 1px solid var(--border); font-size: 12px;
  color: var(--fg2); display: flex; justify-content: space-between; align-items: center;
}}
.theme-toggle {{
  background: var(--bg3); border: 1px solid var(--border); color: var(--fg);
  padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;
}}
/* Main content */
.main {{
  flex: 1; overflow-y: auto; padding: 40px 60px;
}}
.welcome {{
  text-align: center; margin-top: 15vh;
}}
.welcome h2 {{ font-size: 24px; margin-bottom: 8px; }}
.welcome p {{ color: var(--fg2); font-size: 15px; }}
.entry-section {{ max-width: 960px; margin: 0 auto; }}
.entry-title {{
  font-size: 20px; margin-bottom: 24px; padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}}
/* Markdown rendered content */
.md-rendered {{
  line-height: 1.7; font-size: 15px;
}}
.md-rendered h1 {{ font-size: 24px; margin: 32px 0 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
.md-rendered h2 {{ font-size: 20px; margin: 28px 0 12px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }}
.md-rendered h3 {{ font-size: 16px; margin: 24px 0 8px; }}
.md-rendered p {{ margin: 12px 0; }}
.md-rendered ul, .md-rendered ol {{ margin: 12px 0 12px 24px; }}
.md-rendered li {{ margin: 4px 0; }}
.md-rendered code {{
  background: var(--bg3); padding: 2px 6px; border-radius: 4px; font-size: 13px;
}}
.md-rendered pre {{
  background: var(--bg3); padding: 16px; border-radius: 8px; overflow-x: auto;
  margin: 16px 0; border: 1px solid var(--border);
}}
.md-rendered pre code {{ background: none; padding: 0; }}
.md-rendered blockquote {{
  border-left: 4px solid var(--accent); padding: 8px 16px; margin: 16px 0;
  background: var(--bg2); border-radius: 0 6px 6px 0;
}}
.md-rendered table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
.md-rendered th, .md-rendered td {{
  border: 1px solid var(--border); padding: 8px 12px; text-align: left; font-size: 13px;
}}
.md-rendered th {{ background: var(--bg3); font-weight: 600; }}
.md-rendered strong {{ color: var(--accent); }}
/* CSV tables */
.csv-wrapper {{ overflow-x: auto; }}
.csv-wrapper table {{
  border-collapse: collapse; width: 100%; font-size: 13px;
}}
.csv-wrapper th, .csv-wrapper td {{
  border: 1px solid var(--border); padding: 8px 12px; text-align: left;
  white-space: nowrap;
}}
.csv-wrapper th {{
  background: var(--bg3); font-weight: 600; position: sticky; top: 0;
}}
.csv-wrapper tr:nth-child(even) {{ background: var(--bg2); }}
.csv-wrapper tr:hover {{ background: var(--bg3); }}
/* JSON */
.json-block {{
  background: var(--bg3); padding: 20px; border-radius: 8px; overflow-x: auto;
  font-size: 13px; line-height: 1.5; border: 1px solid var(--border);
}}
/* Responsive */
@media (max-width: 768px) {{
  .sidebar {{ width: 100%; max-height: 40vh; border-right: none; border-bottom: 1px solid var(--border); }}
  body {{ flex-direction: column; }}
  .main {{ padding: 20px; }}
}}
</style>
</head>
<body>
<nav class="sidebar">
  <div class="sidebar-header">
    <h1>Infonomics Research</h1>
    <div class="subtitle">{count} outputs &middot; Ottoman Pilot</div>
  </div>
  <input type="text" class="search-box" placeholder="Search files..." oninput="filterNav(this.value)">
  <ul class="nav-list">
    {nav_html}
  </ul>
  <div class="sidebar-footer">
    <span>Generated by publish.py</span>
    <button class="theme-toggle" onclick="toggleTheme()">Toggle Theme</button>
  </div>
</nav>
<main class="main">
  <div class="welcome" id="welcome">
    <h2>Research Dashboard</h2>
    <p>Select a document from the sidebar to view.</p>
    <p style="margin-top: 24px; font-size: 13px; color: var(--fg2);">
      {count} files &middot; Markdown reports, CSV datasets, JSON sessions
    </p>
  </div>
  {content_html}
</main>
<script>
// Render markdown sections
document.querySelectorAll('.md-content').forEach(el => {{
  const raw = el.querySelector('.md-raw');
  const rendered = el.querySelector('.md-rendered');
  if (raw && rendered && typeof marked !== 'undefined') {{
    rendered.innerHTML = marked.parse(raw.textContent);
  }} else if (raw && rendered) {{
    rendered.innerHTML = '<pre>' + raw.textContent + '</pre>';
  }}
}});

let activeItem = null;

function showEntry(id) {{
  document.getElementById('welcome').style.display = 'none';
  document.querySelectorAll('.entry-section').forEach(s => s.style.display = 'none');
  const target = document.getElementById(id);
  if (target) target.style.display = 'block';
  // Update nav active state
  document.querySelectorAll('.nav-item').forEach(li => li.classList.remove('active'));
  const navItem = document.querySelector(`.nav-item[data-target="${{id}}"]`);
  if (navItem) navItem.classList.add('active');
}}

function filterNav(query) {{
  const q = query.toLowerCase();
  document.querySelectorAll('.nav-item').forEach(li => {{
    li.style.display = li.dataset.name.includes(q) ? '' : 'none';
  }});
}}

function toggleTheme() {{
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === 'dark' ? 'light' : 'dark';
}}

// Keyboard nav
document.addEventListener('keydown', e => {{
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
    e.preventDefault();
    document.querySelector('.search-box').focus();
  }}
}});
</script>
</body>
</html>"""


def main():
    if not OUTPUT_DIR.exists():
        print(f"Error: {OUTPUT_DIR} not found.")
        sys.exit(1)

    entries = read_outputs(OUTPUT_DIR)
    if not entries:
        print(f"No outputs found in {OUTPUT_DIR}")
        sys.exit(1)

    dashboard = build_dashboard(entries)
    DASHBOARD_FILE.write_text(dashboard, encoding="utf-8")
    print(f"Dashboard generated: {DASHBOARD_FILE}")
    print(f"  {len(entries)} files included")

    if "--open" in sys.argv:
        webbrowser.open(DASHBOARD_FILE.as_uri())


if __name__ == "__main__":
    main()
