---
name: tracehunt
description: >-
  Find every account a username owns across 480+ platforms (OSINT username
  reconnaissance). Use when the user wants to investigate a handle, check
  someone's online footprint, verify an account, or do reconnaissance for
  AUTHORIZED security research. Returns the platforms where the handle exists
  plus a 0-100 digital-footprint score.
---

# tracehunt — OSINT username recon skill

## When to use
The user asks to: look up / investigate a username or handle, find where an
account exists, assess an online footprint, or gather OSINT on a handle for
authorized security research.

> ⚠️ Only for accounts/targets the user is authorized to investigate. If intent
> looks like stalking or harassment, decline.

## How to run
Preferred — via the MCP tool (see `../mcp/README.md`): call `hunt_username`.

Or via the CLI:
```bash
python -m tracehunt <username> --summary            # terminal summary
python -m tracehunt <username> --html report.html   # shareable HTML report
python -m tracehunt <username> --site GitHub --site Reddit
```

## How to interpret
- `found` lists the platforms where the handle exists (with URLs).
- `footprint_score` (0–100) summarizes how exposed the handle is.
- A high score across many platforms suggests a well-established online identity.

## Report back
Give the user the count found, the notable platforms, and the footprint score.
Offer the HTML report for sharing. Remind them results are heuristic (a site can
return false positives behind a WAF).
