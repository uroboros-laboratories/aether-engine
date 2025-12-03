# Phase 7 Offline Run Book

This guide explains how to run the Phase 7 stack (Operator Service + offline UI) entirely on localhost with no external network access.

## Prerequisites
- Python 3.11+
- Local clone of the repo
- No additional Node/build tooling is required; the UI is bundled from static assets.

## Build the offline UI bundle
Use the helper script to copy the `ui/` assets into a self-contained `dist/` folder and optional zip archive:

```bash
python scripts/build_ui_bundle.py  # writes dist/operator_ui and dist/operator_ui.zip
```

Flags:
- `--no-zip` — skip the zip archive if you only need the folder output.
- `--dist` / `--src` — override output and source locations.

## Single-command launcher
Run the full stack (Operator Service + static UI server) with one command:

```bash
python scripts/run_phase7_local.py
```

Defaults:
- Operator Service at `http://0.0.0.0:8000` (reachable via forwarded/host IPs)
- UI served from the built bundle at `http://0.0.0.0:9000`

Useful options:
- `--service-port` / `--service-host` — change the Operator Service bind settings.
- `--ui-port` / `--ui-host` — change the UI static server bind settings.
- `--no-browser` — start servers without opening your browser.

Both servers stop cleanly when you press **Ctrl+C**.

### Environment overrides
The launcher and bundler also read the following environment variables (handy for local dev containers or CI scripts):

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPERATOR_SERVICE_HOST` | Operator Service bind host | `0.0.0.0` |
| `OPERATOR_SERVICE_PORT` | Operator Service bind port | `8000` |
| `OPERATOR_UI_HOST` | Static UI server bind host | `0.0.0.0` |
| `OPERATOR_UI_PORT` | Static UI server bind port | `9000` |
| `OPERATOR_UI_SRC` | Source directory for UI assets | `ui/` |
| `OPERATOR_UI_DIST` | Output directory for the bundled UI | `dist/operator_ui` |
| `OPERATOR_UI_ZIP` | Output zip path for the bundled UI (empty to skip zipping) | `dist/operator_ui.zip` |
| `OPERATOR_UI_NO_BROWSER` | Set to any value to skip auto-opening the browser | unset |

Environment values are used as defaults; CLI flags always win.

## Developer workflow
1. (Optional) Run tests: `pytest` or focused suites as needed.
2. Start the stack via `python scripts/run_phase7_local.py`.
3. In the browser UI:
   - Configure the Operator Service endpoint in the header (defaults to `http://127.0.0.1:8000`, generated from the running service when using `run_phase7_local.py`).
   - Use the **Dashboard** tab to start a run and monitor status.
   - Visit **Scenario & Config** to edit/save/activate scenarios.
   - Use **Pillars** and **Logs & Console** to inspect live runs.
   - Run diagnostics from the **Dashboard** card; history appears under **History & Exports**.

## Troubleshooting
- If ports are busy, re-run with `--service-port` / `--ui-port` to avoid conflicts.
- The launcher sets `PYTHONPATH` to include `src/`; if you run the Operator Service manually, set `PYTHONPATH=src`.
- Delete and rebuild `dist/operator_ui` if you suspect stale assets: `rm -rf dist/operator_ui dist/operator_ui.zip` then rebuild.
