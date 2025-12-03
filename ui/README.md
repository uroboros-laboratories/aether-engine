# Trinity Gate Operator UI Shell

This folder contains a minimal offline shell for the Phase 7 Trinity Gate Operator Surface. It provides:

- A tabbed layout that mirrors the Phase 7 navigation (Dashboard, Scenario & Config, Pillars, Governance & Budgets, History & Exports, Logs & Console).
- A lightweight `GateClient` wrapper for calling the Operator Service with a configurable base URL.
- A connection status line that probes `/state` to confirm connectivity.

## Usage

### Quick start (manual)
Open `ui/index.html` in a browser (or serve the folder locally) and point the Operator Service URL to your running backend (default: `http://localhost:8000`). The client will store the endpoint in `localStorage` and re-use it on next load.

### Offline bundle
Bundle the UI into `dist/operator_ui` (and an optional zip) with:

```bash
python scripts/build_ui_bundle.py
```

### One-command launcher
Start the Operator Service and serve the bundled UI together:

```bash
python scripts/run_phase7_local.py
```

This launches the Operator Service on `127.0.0.1:8000` and the static UI server on `127.0.0.1:9000`, then opens the browser unless `--no-browser` is provided.
