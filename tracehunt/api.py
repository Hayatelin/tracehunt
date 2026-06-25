"""TraceHunt programmatic API.

A thin, import-and-call wrapper around the TraceHunt engine so other Python
code — and the MCP server — can run a hunt without going through the CLI.

    from tracehunt.api import hunt
    result = hunt("johndoe")                 # all 480+ sites
    result = hunt("johndoe", sites=["GitHub", "Reddit"])

Returns a JSON-serializable dict:
    {
      "username": str,
      "checked": int,
      "found_count": int,
      "footprint_score": int,        # 0-100
      "found": [{"site": str, "url": str}, ...]
    }
"""
from __future__ import annotations

import os
from typing import Optional, List, Dict, Any

from tracehunt.sites import SitesInformation
from tracehunt.notify import QueryNotify
from tracehunt.result import QueryStatus
from tracehunt.core import run_search
from tracehunt import report

_DATA = os.path.join(os.path.dirname(__file__), "resources", "data.json")


def hunt(username: str, sites: Optional[List[str]] = None,
         timeout: int = 30, proxy: Optional[str] = None,
         include_nsfw: bool = False) -> Dict[str, Any]:
    """Hunt a username across the bundled site database (offline DB by default)."""
    sites = sites or []
    info = SitesInformation(_DATA, honor_exclusions=False)
    if not include_nsfw:
        info.remove_nsfw_sites(do_not_remove=sites)

    all_sites = {s.name: s.information for s in info}
    if sites:
        wanted = {s.lower() for s in sites}
        site_data = {n: i for n, i in all_sites.items() if n.lower() in wanted}
    else:
        site_data = all_sites

    results = run_search(username, site_data, QueryNotify(), timeout=timeout, proxy=proxy)

    found = [
        {"site": name, "url": d["url_user"]}
        for name, d in results.items()
        if d["status"].status == QueryStatus.CLAIMED
    ]
    summary = report.summarize(username, results)
    return {
        "username": username,
        "checked": summary["checked"],
        "found_count": summary["found"],
        "footprint_score": summary["footprint_score"],
        "found": sorted(found, key=lambda x: x["site"]),
    }
