"""TraceHunt Report Module.

Original TraceHunt feature (not present in upstream Sherlock).

Generates a self-contained, styled HTML report from a search result set and
computes a simple "digital footprint" summary so an investigator can grasp the
scope of a username's online presence at a glance.

Standard-library only, so it works even in minimal installs.
"""

from __future__ import annotations

import html
import math
import datetime
from typing import Dict, Any

from tracehunt.result import QueryStatus


def summarize(username: str, results: Dict[str, Any]) -> Dict[str, Any]:
    """Reduce a raw results dict into a compact summary with a 0-100 score."""
    found = []
    response_times = []
    for site, data in results.items():
        status = data["status"].status
        if status == QueryStatus.CLAIMED:
            found.append(site)
            qt = data["status"].query_time
            if qt is not None:
                response_times.append(qt)

    total = len(results)
    hit_count = len(found)
    # Saturating curve: first hits matter most. 0->0, 1->~15, 6->~63, 15+->~92.
    score = 0 if hit_count == 0 else min(100, round(100 * (1 - math.exp(-hit_count / 6.0))))
    avg_rt = round(sum(response_times) / len(response_times), 2) if response_times else None

    return {
        "username": username,
        "checked": total,
        "found": hit_count,
        "found_sites": sorted(found),
        "footprint_score": score,
        "avg_response_time_s": avg_rt,
    }


def print_summary(summary: Dict[str, Any]) -> None:
    """Print a human-readable summary block to stdout."""
    print("\n" + "=" * 48)
    print(f"  Digital footprint summary for: {summary['username']}")
    print("=" * 48)
    print(f"  Platforms checked : {summary['checked']}")
    print(f"  Accounts found    : {summary['found']}")
    print(f"  Footprint score   : {summary['footprint_score']}/100")
    if summary["avg_response_time_s"] is not None:
        print(f"  Avg response time : {summary['avg_response_time_s']}s")
    if summary["found_sites"]:
        preview = ", ".join(summary["found_sites"][:12])
        more = "" if summary["found"] <= 12 else f"  (+{summary['found'] - 12} more)"
        print(f"  Found on          : {preview}{more}")
    print("=" * 48 + "\n")


def write_html(username: str, results: Dict[str, Any], path: str, only_found: bool = True) -> str:
    """Write a standalone HTML report to ``path`` and return that path."""
    summary = summarize(username, results)
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []
    for site, data in sorted(results.items()):
        claimed = data["status"].status == QueryStatus.CLAIMED
        if only_found and not claimed:
            continue
        qt = data["status"].query_time
        qt_txt = f"{qt:.2f}s" if isinstance(qt, (int, float)) else "-"
        badge = '<span class="ok">FOUND</span>' if claimed else '<span class="no">-</span>'
        url = html.escape(str(data.get("url_user", "")))
        rows.append(
            f"<tr><td>{html.escape(site)}</td><td>{badge}</td>"
            f'<td><a href="{url}" target="_blank" rel="noopener">{url}</a></td>'
            f"<td>{qt_txt}</td></tr>"
        )
    if not rows:
        rows.append('<tr><td colspan="4" class="empty">No accounts found.</td></tr>')

    score = summary["footprint_score"]
    score_color = "#16a34a" if score < 34 else "#d97706" if score < 67 else "#dc2626"

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TraceHunt report - {html.escape(username)}</title>
<style>
:root {{ color-scheme: light dark; }}
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  margin: 0; padding: 2rem; background: #0f172a; color: #e2e8f0; }}
.wrap {{ max-width: 920px; margin: 0 auto; }}
h1 {{ font-size: 1.6rem; margin: 0 0 .25rem; }}
.sub {{ color: #94a3b8; margin: 0 0 1.5rem; font-size: .9rem; }}
.cards {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }}
.card {{ flex: 1 1 150px; background: #1e293b; border-radius: 12px; padding: 1rem 1.2rem; }}
.card .n {{ font-size: 1.8rem; font-weight: 700; }}
.card .l {{ color: #94a3b8; font-size: .8rem; text-transform: uppercase; letter-spacing: .04em; }}
.score .n {{ color: {score_color}; }}
table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; }}
th, td {{ text-align: left; padding: .6rem .9rem; border-bottom: 1px solid #334155; font-size: .9rem; }}
th {{ background: #334155; text-transform: uppercase; font-size: .72rem; letter-spacing: .04em; }}
a {{ color: #38bdf8; text-decoration: none; word-break: break-all; }}
.ok {{ color: #22c55e; font-weight: 700; }}
.no {{ color: #64748b; }}
.empty {{ text-align: center; color: #94a3b8; padding: 1.5rem; }}
footer {{ margin-top: 1.5rem; color: #64748b; font-size: .78rem; }}
</style></head>
<body><div class="wrap">
<h1>TraceHunt report - {html.escape(username)}</h1>
<p class="sub">Generated {generated} - for authorized OSINT / security research only</p>
<div class="cards">
  <div class="card"><div class="n">{summary['checked']}</div><div class="l">Checked</div></div>
  <div class="card"><div class="n">{summary['found']}</div><div class="l">Found</div></div>
  <div class="card score"><div class="n">{score}</div><div class="l">Footprint score</div></div>
</div>
<table><thead><tr><th>Platform</th><th>Status</th><th>URL</th><th>Time</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table>
<footer>TraceHunt - MIT licensed - based on the open-source Sherlock project.</footer>
</div></body></html>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path
