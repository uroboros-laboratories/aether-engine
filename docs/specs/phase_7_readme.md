# Phase 7 – Trinity Gate Offline Operator UI

## 1. What Phase 7 Is

Phase 7 adds an **offline Gate Operator UI** and a thin **Operator Service** on top of the existing Phase 6 engine.

When Phase 7 is complete, you should be able to:

- Start a **local service + web UI** on `localhost`.
- Use the UI (based on the Trinity Gate mock) to:
  - Select scenarios and run the **full engine stack** (Gate + pillars + governance),
  - Monitor state, metrics, pillars, and logs in real time,
  - Browse run history and exports,
  - Run **diagnostics/self-checks** from the UI (smoke tests, etc.),
- All without any internet connection.

The Phase 6 engine remains the **source of truth** for behaviour. Phase 7 does **not** change core physics/algorithms; it exposes them cleanly and safely via a service + UI.

---

## 2. Key Documents (Phase 7)

All Phase 7 design docs live under `docs/phase7/`:

- `gate_ui_spec_phase7.md`  
  **Trinity Gate — Phase 7 Operator Surface Spec**  
  Describes the operator UI: tabs, layouts, behaviours, and acceptance criteria for each part of the interface (Dashboard, Scenario & Config, Pillars, Governance & Budgets, History & Exports, Logs & Console, Diagnostics flows).

- `operator_service_api_spec_phase7.md`  
  **Trinity Gate — Operator Service API Spec**  
  Defines the Operator Service that sits between the Phase 6 engine and the UI. Specifies the JSON shapes and endpoints for runs, scenarios, governance, history, logs, pillars, and diagnostics.

- `phase7_issue_pack.md`  
  **Phase 7 – Gate UI & Operator Service Issue Pack**  
  GitHub-style issue backlog for implementing Phase 7. Grouped into epics:
  - Engine adapter/runtime,
  - Operator Service core,
  - Diagnostics & tests,
  - Gate UI (offline webpage),
  - Packaging & developer experience.

- `gate_operator_surface_mock_2025_11_30.html`  
  Static HTML mockup of the Gate UI that inspired the Phase 7 spec. Treat this as a **wireframe**, not a pixel-perfect contract.

These docs are the **normative reference** for Phase 7 work. Code changes should be aligned with them unless there is a documented reason to diverge.

---

## 3. High-Level Architecture

Phase 7 introduces a three-layer structure:

1. **Engine Core** (existing, under `src/`)
   - Phase 6 implementation: Gate, UMX, Loom, Astral Press, Codex, governance, metrics, structured logging, introspection, etc.
   - Key types: `RunConfigV1`, `ScenarioRegistryV1`, `SessionConfigV1`, `SessionRunResult`, `MetricsSnapshotV1`, `GovernanceConfigV1`, `IntrospectionViewV1`, `StructuredLogEntryV1`, etc.

2. **Operator Service** (new)
   - Long-lived process that:
     - Wraps engine entrypoints (via an `EngineRuntime` adapter),
     - Starts and tracks runs,
     - Aggregates metrics/governance/introspection/logs into UI-friendly objects,
     - Exposes a small JSON API described in `operator_service_api_spec_phase7.md`.

3. **Gate Operator UI** (new)
   - Local web application that:
     - Follows the Trinity Gate UI spec,
     - Talks only to the Operator Service (never directly to engine internals),
     - Provides operators with a clean control surface for runs, history, logs, and diagnostics.

All components are intended to run **offline** on a single machine (localhost only).

---

## 4. Phase 7 Implementation Plan

Actual development work should follow the issues in `docs/phase7/phase7_issue_pack.md`.

### 4.1 Recommended Order of Work

**Step 1 – Engine adapter/runtime (Epic A)**
- Implement `EngineRuntime` wrapper for scenarios, configs, and session configs.
- Confirm a canonical `run_session(SessionConfigV1) -> SessionRunResult` entrypoint.
- Standardise structured logging and metrics/governance defaults for UI-launched runs.

**Step 2 – Operator Service core (Epic B)**
- Bootstrap a small HTTP service with a health endpoint.
- Add run lifecycle + registry, `/state`, `/runs`, `/scenarios`, `/governance`, `/history`, `/runs/{id}/logs`, and `/runs/{id}/pillars` following the API spec.

**Step 3 – Diagnostics & tests (Epic C)**
- Implement diagnostics runner profiles (starting with `SMOKE`).
- Expose `/diagnostics` endpoints.
- Integrate with history and logs.

**Step 4 – Gate UI (Epic D)**
- Build the UI shell with tabs and layout.
- Wire each tab to the Operator Service API (Dashboard, Scenario & Config, Pillars, Governance, History & Exports, Logs & Console, Diagnostics).
- Ensure all assets are bundled for offline use.

**Step 5 – Packaging & DX (Epic E)**
- Provide scripts/commands for local dev and testing.
- Add a single entrypoint command or launcher that starts the Operator Service, serves the UI bundle, and opens the browser.
- Update documentation and run book.

---

## 5. How to Work With This Repo (for AI / Codex)

When using an AI coding assistant (e.g., GitHub Copilot / Codex / GPT) on this repo, follow these rules:

1. **Engine is source of truth**  
   Do not rewrite or radically restructure core engine modules unless an issue in `phase7_issue_pack.md` explicitly calls for it.

2. **Specs are normative**  
   The following documents define intended behaviour and interfaces:
   - `docs/phase7/gate_ui_spec_phase7.md`
   - `docs/phase7/operator_service_api_spec_phase7.md`
   - `docs/phase7/phase7_issue_pack.md`

3. **Work issue-by-issue**  
   Implement one issue at a time from `phase7_issue_pack.md`. For each issue:
   - Read the issue description and acceptance criteria.
   - Identify the suggested files and types to touch.
   - Make the minimal necessary changes to satisfy the acceptance criteria.

4. **Keep everything offline-safe**  
   Do not introduce dependencies on external network resources (APIs, CDNs, etc.) as part of Phase 7.

---

## 6. Quickstart (Once Phase 7 Is Implemented)

> **Note:** This section describes the intended experience. Exact commands/paths may differ depending on the final implementation. See the final run book for authoritative instructions.

1. Build or install dependencies as described in the main `README.md`.
2. Start the Operator Service + UI (single command):

```bash
python scripts/run_phase7_local.py
```

3. Open the Gate Operator UI in a browser:

```text
http://localhost:<PORT>
```

4. From the UI you can:
   - Pick a scenario and start a run.
   - Watch state/metrics/pillars on the Dashboard.
   - Inspect history and exports.
   - Run a **smoke diagnostics** and see the results.

For detailed operator workflows, refer to:

- `docs/phase7/gate_ui_spec_phase7.md` (behaviour & acceptance criteria),
- `docs/phase7_runbook.md` (operator run book and troubleshooting).


## 7. Developer experience snapshot (Phase 7)
- Bundle the offline UI: `python scripts/build_ui_bundle.py` (outputs `dist/operator_ui` and a zip archive). Override defaults with `OPERATOR_UI_SRC`, `OPERATOR_UI_DIST`, `OPERATOR_UI_ZIP`, or CLI flags.
- Run the full stack locally: `python scripts/run_phase7_local.py` (Operator Service on `127.0.0.1:8000`, UI on `127.0.0.1:9000`). Defaults can be adjusted via CLI flags or `OPERATOR_SERVICE_HOST` / `OPERATOR_SERVICE_PORT` / `OPERATOR_UI_HOST` / `OPERATOR_UI_PORT`.
- See `docs/phase7_runbook.md` for prerequisites, workflow, and troubleshooting, including the full environment variable matrix.
