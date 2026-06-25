# Attribution

TraceHunt is a customized fork of the open-source **Sherlock** project
(https://github.com/sherlock-project/sherlock), used under the MIT License.
The original Sherlock copyright notice is preserved in `LICENSE`.

## What TraceHunt changes / adds on top of Sherlock
- Rebranded and repackaged as the `tracehunt` Python package / CLI.
- **New:** styled standalone **HTML report** generator (`tracehunt/report.py`).
- **New:** **digital-footprint score** and per-username summary.
- **New:** **YAML config file** support (`tracehunt/config.py`, `--config`).
- **Privacy:** the upstream "check for updates" call no longer runs automatically —
  it is opt-in via `--check-update`, so the tool does not phone home by default.
- Default site database is the **bundled offline** `data.json` (no network needed).
- Fresh, offline-friendly test suite for the new functionality.

The bundled site database (`tracehunt/resources/data.json`) is the curated list
from the Sherlock project and remains under the same MIT terms.
