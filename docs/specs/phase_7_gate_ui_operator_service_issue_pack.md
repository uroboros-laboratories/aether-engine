# Phase 7 – Gate UI & Operator Service Issue Pack

> Goal: Offline local webpage UI (Gate Operator) that uses the existing Phase 6 engine repo, follows the Trinity Gate UI spec, and exposes the full stack (runs + diagnostics/tests) via the Operator Service API spec.
>
> This file is structured as GitHub‑style issues grouped by epic. Each issue includes scope, files/hints, and acceptance criteria.

---

## Epic A – Engine Adapter & Runtime

### A1 – Establish EngineRuntime wrapper

**Summary**  
Create a small `EngineRuntime` (or similarly named) wrapper that centralises access to scenarios, run configs, session configs, governance defaults, and logging/metrics defaults.

**Scope**
- Define an `EngineRuntime` object responsible for:
  - Loading `ScenarioRegistryV1` from the repo.
  - Loading `RunConfigV1` from JSON files.
  - Constructing `SessionConfigV1` from a `scenario_id` plus overrides (ticks, logging, metrics, governance presets).
- Ensure all logic for locating config files and fixtures is encapsulated here.

**Hints / likely files**
- `src/config/schemas.py`
- `src/config/__init__.py`
- `src/gate/gate.py`
- `docs/fixtures/scenarios/scenario_registry.json`
- `docs/fixtures/configs/*.json`

**Constraints**
- Do **not** change the public shape of `RunConfigV1`, `SessionConfigV1`, or the tick loop.
- `EngineRuntime` should be a thin orchestration layer, not a new engine.

**Acceptance Criteria**
- A single public method such as `build_session_config(scenario_id: str, overrides: Mapping) -> SessionConfigV1` exists.
- Scenario IDs from the registry can be resolved into valid `SessionConfigV1` objects using only the `EngineRuntime` API.
- All path logic and default governance/logging/metrics wiring live inside `EngineRuntime`, not scattered across the service.

---

### A2 – Canonical run_session entrypoint & helpers

**Summary**  
Confirm and document a single canonical entrypoint for executing a session (`run_session`) and provide helpers for post‑run artefacts.

**Scope**
- Ensure there is a clear function such as `run_session(config: SessionConfigV1) -> SessionRunResult` exposed at a stable import path.
- Provide helper functions:
  - `build_metrics_snapshot(result: SessionRunResult) -> MetricsSnapshotV1` (if not already exposed cleanly).
  - `build_introspection_view(result: SessionRunResult) -> IntrospectionViewV1`.

**Hints / likely files**
- `src/gate/gate.py`
- `src/ops/metrics.py`
- `src/ops/introspection.py`
- `docs/contracts/Metrics_v1.md`
- `docs/contracts/Introspection_v1.md`

**Acceptance Criteria**
- The Operator Service can import a single `run_session` entrypoint and call it with `SessionConfigV1`.
- There are clear helper functions to move from `SessionRunResult` to `MetricsSnapshotV1` and `IntrospectionViewV1` without duplicating logic.

---

### A3 – Structured logging configuration for runs

**Summary**  
Standardise how structured logging is configured for engine runs so the Operator Service can reliably stream and filter logs.

**Scope**
- Ensure `LoggingConfigV1` and `StructuredLogger` are wired consistently for all runs started via `EngineRuntime`.
- Decide and document the logging destination strategy (in‑memory, file, or both) to support the UI’s `/runs/{run_id}/logs` endpoint.

**Hints / likely files**
- `src/ops/structured_logging.py`
- `src/gate/gate.py`
- `src/config/schemas.py`
- `docs/contracts/StructuredLogging_v1.md`

**Acceptance Criteria**
- Every run started via `EngineRuntime` uses a `StructuredLogger` instance associated with that run.
- Log entries include enough metadata (timestamp, run_id, event_type) to support the Logs & Console tab.
- The chosen logging destination strategy is documented for use by the Operator Service.

---

### A4 – Metrics & governance defaults surface

**Summary**  
Define and document reasonable default metrics/governance configurations for runs launched from the UI.

**Scope**
- Decide default metrics configuration for UI‑launched runs (e.g., enable metrics by default where performance cost is acceptable).
- Decide default governance configuration for UI‑launched runs (e.g., conservative Codex action mode).
- Wire these defaults into `EngineRuntime` so they are applied unless the Operator Service explicitly overrides them.

**Hints / likely files**
- `src/ops/metrics.py`
- `src/governance/config.py`
- governance‑related specs in `docs/specs/*Governance*`

**Acceptance Criteria**
- UI‑launched runs have metrics enabled by default (unless overridden) and produce a `MetricsSnapshotV1`.
- UI‑launched runs have a consistent default governance profile that aligns with the Phase 7 Governance tab expectations.

---

## Epic B – Operator Service Core

### B1 – Bootstrap Operator Service skeleton

**Summary**  
Create the basic Operator Service application: process startup, config loading, and a minimal health endpoint.

**Scope**
- Set up a small HTTP server (framework choice is flexible) with:
  - Configuration for bind host/port.
  - Wiring to `EngineRuntime`.
  - A basic `GET /health` endpoint returning service status.
- Provide a single CLI entrypoint to start the service.

**Acceptance Criteria**
- Running a single command starts the Operator Service on `localhost` and `GET /health` returns a simple JSON health document.

---

### B2 – Implement run lifecycle & run registry

**Summary**  
Introduce a `RunHandle` concept and a registry to track runs and their states.

**Scope**
- Define `RunHandle` containing at least:
  - `run_id`
  - `RunStatus`
  - handle to the worker/task running `run_session`
  - access to logs and artefacts
- Implement a `RunRegistry` or similar to:
  - Track the current run (Phase 7 floor: one concurrent run).
  - Track completed runs with references to persistent artefacts.

**Acceptance Criteria**
- The service can start a run, track its state transitions (RUNNING → COMPLETED/FAULT), and look up `RunStatus` by `run_id`.
- The service enforces the one‑run‑at‑a‑time constraint for normal runs.

---

### B3 – Implement /state and /runs endpoints

**Summary**  
Implement the core endpoints driving the Dashboard run controls and status display.

**Scope**
- `GET /state` returning:
  - `current_run: RunStatus | null`
  - `active_scenario: ScenarioSummary | null`
  - `pillars: PillarStatus[] | []` (shallow view)
  - `governance: GovernanceSnapshot | null`
- `POST /runs` to start a new run from `scenario_id` plus overrides, mapping to `EngineRuntime.build_session_config` and `run_session`.
- `POST /runs/{run_id}/stop` to request stopping a run (Phase 7 floor: best effort, with clear semantics if hard cancellation is not yet supported).

**Acceptance Criteria**
- Dashboard can call `GET /state` and receive a valid picture of current run, active scenario, and pillars.
- `POST /runs` starts a run and returns a populated `RunStatus` with `state = RUNNING`.
- `POST /runs/{run_id}/stop` is accepted only when appropriate, and RunStatus reflects the requested stop or the limitation clearly.

---

### B4 – Implement /scenarios endpoints

**Summary**  
Expose scenario list and detail for the Scenario & Config tab.

**Scope**
- `GET /scenarios` → `ScenarioSummary[]`.
- `GET /scenarios/{id}` → `ScenarioDetail`.
- `POST /scenarios/{id}` → update whitelisted config parameters.
- `POST /scenarios/{id}/activate` → set the active scenario for future runs.

**Acceptance Criteria**
- UI can list scenarios, inspect details, save edits to allowed parameters, and mark a scenario active.
- Scenario edits are persisted in a way that affects subsequent runs.

---

### B5 – Implement /governance endpoints

**Summary**  
Surface a manageable slice of governance configuration for the Governance & Budgets tab.

**Scope**
- `GET /governance` → `GovernanceSnapshot` built from the defaults used for UI‑launched runs.
- `POST /governance` → update selected governance knobs (mode, Codex action mode, a small set of numeric budgets).

**Acceptance Criteria**
- Governance tab can show and edit the configured subset of governance fields.
- Changes are applied to subsequent runs and reflected via `GET /governance` and `GET /state`.

---

### B6 – Implement /history endpoints

**Summary**  
Provide run history and details for the History & Exports tab.

**Scope**
- Introduce a simple persistent store (SQLite/JSONL) for `HistoryEntry` rows.
- `GET /history` → `{ entries: HistoryEntry[], total: number }`.
- `GET /history/{run_id}` → `{ run: RunStatus, pillars: PillarStatus[], governance: GovernanceSnapshot, metrics: Record<string, number | string> }`.

**Acceptance Criteria**
- Completed runs are written to the history store with basic metadata.
- UI can list runs and inspect a run’s details using these endpoints.

---

### B7 – Implement /runs/{run_id}/logs endpoint

**Summary**  
Expose structured log entries to drive the Logs & Console tab.

**Scope**
- `GET /runs/{run_id}/logs?cursor=&level=&event_type=` → returns `LogEntry[]` plus a new cursor.
- Decide and implement how logs are stored and fetched (in‑memory or file‑backed).

**Acceptance Criteria**
- UI can fetch logs incrementally for a run via cursor.
- Level and event type filters work as expected.

---

### B8 – Implement /runs/{run_id}/pillars endpoint

**Summary**  
Provide pillar‑level metrics and statuses for the Pillars tab and run details.

**Scope**
- `GET /runs/{run_id}/pillars` → `PillarStatus[]`.
- Map metrics/introspection/governance into a simple, stable `PillarStatus` model.

**Acceptance Criteria**
- Pillars tab can render a card per pillar, powered by this endpoint.
- Run details view can show pillars context for historical runs.

---

## Epic C – Diagnostics & Tests

### C1 – Implement diagnostics runner & profiles

**Summary**  
Add a diagnostics runner that executes small, curated engine scenarios and reports results.

**Scope**
- Define `DiagnosticProfile`, `DiagnosticStatus`, and `DiagnosticResult` in the service.
- Implement at least the `SMOKE` profile using real engine runs.
- Optionally stub `SELF_CHECK` and `FULL_SUITE` with clear TODOs.

**Acceptance Criteria**
- Internal diagnostics runner can execute a `SMOKE` profile and produce a `DiagnosticResult` with at least one check.
- Failures are captured with a clear summary and check‑level messages.

---

### C2 – Expose diagnostics via /diagnostics API

**Summary**  
Implement diagnostics endpoints for the UI as per the Operator Service API Spec.

**Scope**
- `GET /diagnostics/profiles` → list profiles.
- `POST /diagnostics` → start a diagnostics run.
- `GET /diagnostics` → list diagnostics runs.
- `GET /diagnostics/{diagnostic_id}` → detailed result.
- Enforce concurrency rules: no diagnostics while normal run is RUNNING; no overlapping diagnostics.

**Acceptance Criteria**
- UI can discover profiles, start `SMOKE` diagnostics, and see results and history.
- Concurrency constraints are respected and errors are clearly reported.

---

### C3 – Integrate diagnostics with history & logs

**Summary**  
Ensure diagnostics runs show up in history and can be inspected via logs.

**Scope**
- Record diagnostics runs in either the same history store or a dedicated diagnostics index.
- Link diagnostics runs to any normal Gate `run_id`s created as part of diagnostics.
- Ensure logs from diagnostics runs are accessible via `/runs/{run_id}/logs`.

**Acceptance Criteria**
- Diagnostics runs appear in the diagnostics section of History & Exports.
- From diagnostics details, it is possible to navigate to logs for any related run.

---

## Epic D – Gate Operator UI (Offline Webpage)

> Implementation technology is flexible (e.g., React + local bundler). All assets must be served locally with no CDN dependence.

### D1 – UI shell & navigation

**Summary**  
Implement the UI shell that mirrors the Phase 7 Gate UI spec: top‑level tabs and base layout.

**Scope**
- Tabs: Dashboard, Scenario & Config, Pillars, Governance & Budgets, History & Exports, Logs & Console.
- Base layout: header, main content, consistent spacing and typography roughly aligned with the original mock.
- A small client‑side `GateClient` for calling Operator Service endpoints.

**Acceptance Criteria**
- User can switch between tabs without losing state unnecessarily.
- All network calls are routed through a single client module with base URL configurable (e.g. `http://localhost:PORT`).

---

### D2 – Dashboard tab wiring

**Summary**  
Implement Dashboard widgets and run controls on top of `/state`, `/runs`, and diagnostics APIs.

**Scope**
- Poll `GET /state` (or subscribe) to display:
  - current run status,
  - active scenario summary,
  - shallow pillar cards,
  - governance mode.
- Implement run controls wired to:
  - `POST /runs` (start),
  - `POST /runs/{run_id}/stop` (stop/reset semantics per spec).
- Implement Diagnostics card wired to diagnostics endpoints.

**Acceptance Criteria**
- Dashboard UI reflects run state transitions correctly.
- Start/Stop buttons enable/disable according to RunState.
- Triggering a smoke test diagnostics run updates the Diagnostics card and shows final result.

---

### D3 – Scenario & Config tab wiring

**Summary**  
Implement scenario list and detail views, wired to `/scenarios` endpoints.

**Scope**
- List view from `GET /scenarios`.
- Detail panel from `GET /scenarios/{id}` with editable subset of config fields.
- Save flow via `POST /scenarios/{id}`.
- Activate scenario via `POST /scenarios/{id}/activate`.

**Acceptance Criteria**
- Operator can select a scenario, edit allowed parameters, save, and activate it.
- Edits are reflected in Dashboard active scenario label after save.

---

### D4 – Pillars tab wiring

**Summary**  
Implement Pillars tab overview using `/runs/{run_id}/pillars` and/or `/state`.

**Scope**
- Render one card per pillar (Aether, Press, UMX, Loom, Codex) with status and key metrics.
- Optional details panel for the selected pillar.

**Acceptance Criteria**
- Pillars tab shows up‑to‑date pillar statuses for the current or selected run.
- Selecting a pillar shows additional metrics where available.

---

### D5 – Governance & Budgets tab wiring

**Summary**  
Implement governance UI on top of `/governance` endpoints.

**Scope**
- Display current governance mode, Codex action mode, and selected numeric budgets.
- Allow editing and saving via `POST /governance`.

**Acceptance Criteria**
- Changes via the UI are reflected in `/governance` and affect subsequent runs.
- Errors from governance updates are surfaced clearly (non‑blocking banners/toasts).

---

### D6 – History & Exports tab wiring

**Summary**  
Implement history list and run details, including diagnostics section.

**Scope**
- History list from `GET /history`.
- Run details from `GET /history/{run_id}`.
- Diagnostics section from `GET /diagnostics` and `GET /diagnostics/{diagnostic_id}`.
- Export actions from `/history/{run_id}/export` (when implemented).

**Acceptance Criteria**
- Operator can see a list of past runs and open details for any run.
- Diagnostics runs are clearly distinguishable from normal runs and show their check breakdown.

---

### D7 – Logs & Console tab wiring

**Summary**  
Implement log viewer wired to `/runs/{run_id}/logs`.

**Scope**
- Log list for selected run, with level and text filtering.
- Incremental loading using cursor.

**Acceptance Criteria**
- Logs appear and update while runs are in progress (within the limits of the backend strategy).
- Filters behave consistently and do not require a full page reload.

---

### D8 – Offline bundling & assets

**Summary**  
Ensure the Gate UI can be built into a static bundle that works offline and is served locally.

**Scope**
- Configure build tooling (e.g. Vite/Webpack) to produce static assets.
- Ensure no fonts, CSS, or scripts are loaded from external CDNs.

**Acceptance Criteria**
- With network disabled, the UI still loads and functions fully when served from the local Operator Service.

---

## Epic E – Packaging & Developer Experience

### E1 – Local dev and config

**Summary**  
Provide a simple developer workflow for running engine, service, and UI locally.

**Scope**
- Document environment variables (ports, paths to configs, etc.).
- Provide scripts/commands for:
  - running tests,
  - starting the Operator Service,
  - running the UI in dev mode.

**Acceptance Criteria**
- A new dev can follow a short README section to get a working Phase 7 stack locally.

---

### E2 – Single entrypoint for offline Phase 7

**Summary**  
Create a single command or launcher that starts the full Phase 7 stack and opens the UI.

**Scope**
- A script or executable that:
  - starts the Operator Service,
  - serves the built UI,
  - optionally opens the browser to `http://localhost:PORT`.

**Acceptance Criteria**
- On the target machine, running one documented command results in the offline Gate UI being available in a browser and fully wired to the engine.

---

### E3 – Phase 7 run book / README

**Summary**  
Write a user‑facing doc describing how to run and use the Phase 7 Gate UI offline.

**Scope**
- Sections:
  - Prerequisites (runtime, OS assumptions).
  - Install or build steps.
  - How to start the stack.
  - Basic workflows: run a scenario, check history, run diagnostics.
  - Troubleshooting basics.

**Acceptance Criteria**
- A technically literate operator can follow the README and successfully:
  - start the stack,
  - run a scenario,
  - run a diagnostics smoke test,
  - inspect logs and history – all offline.

