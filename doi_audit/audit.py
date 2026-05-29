#!/usr/bin/env python3
"""DOI audit for LayerA0 v1.3 section 24 references.
Resolves each DOI via doi.org (CSL JSON), applies a title-match guard,
and proposes Crossref corrections for BROKEN / WRONG-PAPER? entries.
Proposes only -- edits no reference. Output: doi_audit_report.md
"""
import json, re, time, sys, urllib.request, urllib.parse, urllib.error

REF_FILE = "LayerA0_v1.3_section24_references.md"
OUT_FILE = "doi_audit_report.md"
MAILTO = "abhineet.asthana@gmail.com"
UA = f"doi-audit (mailto:{MAILTO})"
WRONG_PAPER_THRESHOLD = 0.6

STOP = {"a","an","the","of","on","in","to","for","and","with","as","is","at","by","from"}

def tokens(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return {t for t in s.split() if t and t not in STOP and len(t) > 1}

def overlap(ref_title, resolved_title):
    a, b = tokens(ref_title), tokens(resolved_title)
    if not a:
        return 0.0
    return len(a & b) / len(a)

def http_get(url, accept=None, timeout=40):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    if accept:
        req.add_header("Accept", accept)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")

def resolve_doi(doi):
    """Return (status_code, title, container) or (None, None, None) on failure."""
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/.:")
    try:
        code, body = http_get(url, "application/vnd.citationstyles.csl+json")
    except urllib.error.HTTPError as e:
        return e.code, None, None
    except Exception as e:
        return f"ERR:{type(e).__name__}", None, None
    try:
        j = json.loads(body)
    except Exception:
        return code, None, None
    title = j.get("title")
    if isinstance(title, list):
        title = " ".join(title)
    cont = j.get("container-title")
    if isinstance(cont, list):
        cont = "; ".join(cont)
    return code, title or "", cont or ""

def crossref_candidates(title, rows=3):
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": rows})
    url = "https://api.crossref.org/works?" + q + f"&mailto={MAILTO}"
    try:
        code, body = http_get(url)
        j = json.loads(body)
        items = j.get("message", {}).get("items", [])
    except Exception as e:
        return [f"(crossref query failed: {type(e).__name__})"]
    out = []
    for it in items[:rows]:
        d = it.get("DOI", "?")
        t = it.get("title", [""])
        t = (t[0] if isinstance(t, list) and t else (t or ""))
        yr = ""
        for k in ("published-print", "published-online", "published", "issued", "created"):
            dp = it.get(k, {}).get("date-parts", [[None]])
            if dp and dp[0] and dp[0][0]:
                yr = str(dp[0][0]); break
        cont = it.get("container-title", [""])
        cont = (cont[0] if isinstance(cont, list) and cont else (cont or ""))
        sc = it.get("score", 0)
        out.append(f"`{d}` — {t} — {yr} — {cont} (score {sc:.0f})")
    return out or ["(no candidates returned)"]

def parse_refs(text):
    """Return list of dicts for paragraphs containing a DOI."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    refs = []
    for p in paras:
        m = re.search(r"\bdoi:\s*(10\.\S+)", p, re.I)
        if not m:
            continue
        doi = m.group(1).rstrip(". ]")
        # author + year label
        ym = re.search(r"\(((?:1|2)\d{3}[a-z]?)\)", p)
        year = ym.group(1) if ym else "?"
        author = p.split("(")[0].strip().rstrip(".,")
        # title: text after "(year). " up to next ". "
        title = ""
        if ym:
            after = p[ym.end():].lstrip(". ").strip()
            # cut at first ". " (sentence end) -- keep '?' titles whole-ish
            cut = re.split(r"\.\s", after, maxsplit=1)
            title = cut[0].strip().rstrip(".")
        refs.append({"author": author, "year": year, "title": title, "doi": doi, "raw": p})
    return refs

def main():
    text = open(REF_FILE, encoding="utf-8").read()
    if "# 24. References" not in text:
        print("FATAL: '# 24. References' heading not found in input.", file=sys.stderr)
        sys.exit(2)
    refs = parse_refs(text)
    print(f"Parsed {len(refs)} references carrying DOIs.", file=sys.stderr)

    rows = []
    for i, r in enumerate(refs, 1):
        code, rtitle, rcont = resolve_doi(r["doi"])
        status = "OK"
        ov = None
        if code == 200 and rtitle is not None:
            ov = overlap(r["title"], rtitle)
            if ov < WRONG_PAPER_THRESHOLD:
                status = "WRONG-PAPER?"
        elif code == 200 and rtitle is None:
            status = "OK"  # resolved but no CSL title (e.g. some books)
        else:
            status = "BROKEN"
        cands = []
        if status in ("BROKEN", "WRONG-PAPER?"):
            time.sleep(1.0)
            cands = crossref_candidates(r["title"] or r["raw"][:120])
        r.update(code=code, rtitle=rtitle, rcont=rcont, status=status, ov=ov, cands=cands)
        rows.append(r)
        print(f"[{i:2}/{len(refs)}] {status:12} ov={ov if ov is None else round(ov,2)} "
              f"{r['author']} ({r['year']}) doi:{r['doi']} -> HTTP {code}", file=sys.stderr)
        time.sleep(1.0)

    n = len(rows)
    ok = sum(1 for r in rows if r["status"] == "OK")
    broken = sum(1 for r in rows if r["status"] == "BROKEN")
    wrong = sum(1 for r in rows if r["status"] == "WRONG-PAPER?")

    # flagged first, then OK; stable within group
    order = {"BROKEN": 0, "WRONG-PAPER?": 1, "OK": 2}
    rows_sorted = sorted(enumerate(rows), key=lambda x: (order[x[1]["status"]], x[0]))

    def esc(s):
        return (s or "").replace("|", "\\|").replace("\n", " ")

    lines = []
    lines.append("# DOI Audit Report — LayerA0 v1.3 §24 References\n")
    lines.append(f"**93 references in source, {n} with DOIs audited, "
                 f"{ok} OK, {broken} broken, {wrong} possible-wrong-paper.**\n")
    lines.append("Generated by resolving each DOI against doi.org (CSL JSON) with a "
                 "title-match guard (token overlap < 0.6 → `WRONG-PAPER?`). "
                 "Candidate corrections are Crossref suggestions for a human to approve — "
                 "**none applied**.\n")
    lines.append("| # | Reference (author, year) | Original DOI | Status | Resolved title | Candidate corrections (DOI — title — year — container) |")
    lines.append("|---|---|---|---|---|---|")
    for orig_i, r in rows_sorted:
        cand = "<br>".join(esc(c) for c in r["cands"]) if r["cands"] else ""
        rtitle = esc(r["rtitle"]) if r["rtitle"] else (f"(HTTP {r['code']})" if r["status"]=="BROKEN" else "")
        lines.append(f"| {orig_i+1} | {esc(r['author'])} ({r['year']}) | `{esc(r['doi'])}` | "
                     f"{r['status']} | {rtitle} | {cand} |")

    lines.append("\n## Observations\n")
    lines.append("- Off-spec items noticed but **not touched** (per brief scope fence):")
    lines.append("  - The Marsan/Conte/Balbo (1984) GSPN entry carries an inline editorial note "
                 "`[DOI string verified short; confirm on resolver before submission.]` in the source "
                 "references file. Left verbatim; its DOI is audited in the table above.")
    lines.append("  - Token-overlap thresholding can flag legitimate entries whose CSL title differs "
                 "stylistically from the reference text (e.g. books, subtitle/case differences). Treat "
                 "`WRONG-PAPER?` rows as *review prompts*, not verdicts.")
    open(OUT_FILE, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"\nWrote {OUT_FILE}: {n} audited / {ok} OK / {broken} broken / {wrong} wrong-paper?", file=sys.stderr)

if __name__ == "__main__":
    main()
