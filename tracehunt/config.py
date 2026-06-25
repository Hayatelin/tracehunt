"""TraceHunt Config Module.

Original TraceHunt feature (not present in upstream Sherlock).

Loads default option values from a YAML config file so users don't have to
retype common flags. Search order:

  1. --config <path> (handled by the CLI)
  2. ./tracehunt.yaml  (current directory)
  3. ~/.config/tracehunt/config.yaml

Any key present becomes a default for the matching CLI argument; explicit CLI
flags always win. Unknown keys are ignored.
"""

from __future__ import annotations

import os
from typing import Dict, Any, Optional

ALLOWED_KEYS = {
    "timeout", "output", "folderoutput", "proxy", "tor", "unique_tor",
    "csv", "xlsx", "html", "summary", "print_all", "print_found",
    "no_color", "nsfw", "site_list", "local",
}


def _candidate_paths() -> list:
    paths = ["tracehunt.yaml", "tracehunt.yml"]
    home = os.path.expanduser("~")
    paths.append(os.path.join(home, ".config", "tracehunt", "config.yaml"))
    return paths


def load_config(explicit_path: Optional[str] = None) -> Dict[str, Any]:
    """Return {dest: value} from the first config file found, else {}."""
    try:
        import yaml  # lazy import; optional dependency
    except Exception:
        return {}

    search = [explicit_path] if explicit_path else _candidate_paths()
    for path in search:
        if path and os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh) or {}
            except Exception:
                return {}
            if not isinstance(data, dict):
                return {}
            return {k: v for k, v in data.items() if k in ALLOWED_KEYS}
    return {}
