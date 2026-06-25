#!/usr/bin/env python3
"""TraceHunt MCP server.

Exposes TraceHunt's OSINT username search to any MCP client (Claude Code,
Cursor, Codex, Gemini CLI, ...) as callable tools.

Run:
    pip install "mcp[cli]" requests requests-futures
    python mcp/tracehunt_mcp.py

Then register it with your agent (see mcp/README.md).
"""
import os
import sys

# Make the `tracehunt` package importable when run as a standalone file.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from tracehunt.api import hunt  # noqa: E402

mcp = FastMCP("tracehunt")


@mcp.tool()
def hunt_username(username: str, sites: list[str] | None = None, timeout: int = 30) -> dict:
    """Search for a username across 480+ platforms (OSINT).

    Args:
        username: the handle to investigate.
        sites: optional list of site names to limit the search (e.g. ["GitHub", "Reddit"]).
        timeout: per-request timeout in seconds.

    Returns a dict with the platforms where the handle exists, the number of
    sites checked, and a 0-100 digital-footprint score. For authorized security
    research / OSINT only.
    """
    return hunt(username, sites=sites, timeout=timeout)


@mcp.tool()
def footprint_score(username: str, timeout: int = 30) -> dict:
    """Return just the digital-footprint summary for a username (no per-site list)."""
    r = hunt(username, timeout=timeout)
    return {
        "username": r["username"],
        "checked": r["checked"],
        "found": r["found_count"],
        "footprint_score": r["footprint_score"],
    }


if __name__ == "__main__":
    mcp.run()
