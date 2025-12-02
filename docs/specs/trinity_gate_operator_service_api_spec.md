# Trinity Gate — Operator Service API Spec (Draft v0.1)

> Thin adapter layer between the Phase 6 engine repo and the Phase 7 Gate UI. No framework assumed. Describes **shapes and behaviours**, not implementation details.

---

## 1. Purpose & Role

The **Operator Service** is a long‑lived process that:

- Loads scenarios and run configs from the existing engine repo.
- Starts and tracks Gate runs.
- Aggregates metrics, governance, introspection, and logs into **UI‑friendly objects**.
- Provides a small set of JSON endpoints (or equivalent) consumed by the Gate UI.

It does **not** re‑implement engine logic. It simply:

- Builds `SessionConfigV1` from config files and defaults.
- Calls `run_session(SessionConfigV1)` (or a future incremental runner).
- Persists minimal run metadata for history.

---

## 2. High‑Level Model

### 2.1 Layers

1. **Engine Core (existing)**
   - `RunConfigV1`, `ScenarioRegistryV1`, `SessionConfigV1`, `SessionRunResult`.
   - `MetricsConfigV1` / `MetricsSnapshotV1`.
   - `GovernanceConfigV1` and related policy types.
   - `IntrospectionViewV1` and snapshot helpers.
   - `StructuredLogger` / `StructuredLogEntryV1`.

2. **Operator Service (new)**
   - Keeps track of the **active scenario**.
   - Starts runs, maintains run handles, tracks state.
   - Surfaces `RunStatus`, `PillarStatus`, `HistoryEntry`, `GovernanceSnapshot`, `LogEntry` objects.

3. **Gate UI (Phase 7)**
   - Talks to Operator Service only.
   - Never calls engine core directly.

---

## 3. UI‑Facing Data Shapes

These are conceptual types. Actual JSON field names can be chosen to taste.

### 3.1 ScenarioSummary

Minimal info for lists and pickers.

- `id: string` – scenario identifier (matches registry ID).
- `name: string` – human‑friendly name.
- `description: string` – short description.
- `tags: string[]` – arbitrary tags (runtime hints, pillar emphasis, etc.).
- `runtime_hint?: string` – e.g. `tiny`, `small`, `demo`, etc.
- `pillars?: string[]` – list of pillar codes touched by this scenario.

**Backed by:** `ScenarioRegistryV1` entries.

---

### 3.2 ScenarioDetail

Full detail for editing and inspection.

- All fields from `ScenarioSummary`.
- `run_config_id: string` – identifier for the underlying run config.
- `run_config_path: string` – relative path in repo.
- `ticks_total?: number` – total ticks from the associated `RunConfigV1`.
- `logging_enabled?: boolean` – derived from `RunConfigV1.logging`.
- `metrics_enabled?: boolean` – derived from `RunConfigV1.metrics`.
- `governance_profile?: string` – name/id of governance preset if used.
- `parameters: Record<string, number | string | boolean>` – small editable subset of run config (e.g. tick budget, window choice, etc.).

**Backed by:** `ScenarioRegistryV1` + `RunConfigV1` fixtures.

---

### 3.3 RunState

Top‑level run lifecycle state as seen by the UI.

- `state: "IDLE" | "RUNNING" | "COMPLETED" | "FAULT" | "CANCELLED"`.
- `reason?: string` – human‑readable reason when in FAULT or CANCELLED.

**Backed by:** Operator service bookkeeping + Structured logs and/or errors.

---

### 3.4 RunStatus

Flattened snapshot used across Dashboard, History, and Run Details.

- `run_id: string` – unique within the Operator Service.
- `state: RunState` – as above.
- `scenario_id: string`.
- `started_at: string` – ISO timestamp.
- `ended_at?: string` – ISO, present when not RUNNING.
- `ticks_total?: number` – planned number of ticks.
- `ticks_completed?: number` – best estimate completed.
- `progress?: number` – 0–1, computed from `ticks_completed / ticks_total` when available.
- `result_summary?: string` – short text summary (optional).

**Backed by:**

- Operator service memory for live runs.
- `SessionRunResult` + `MetricsSnapshotV1` for completed runs.
- Structured logs (`tick_complete` events) for tick counts when metrics are disabled.

---

### 3.5 PillarStatus

High‑level pillar cards for Dashboard and Pillars tab.

- `pillar_id: "AETHER" | "PRESS" | "UMX" | "LOOM" | "CODEX" | string`.
- `name: string`.
- `status: "IDLE" | "ACTIVE" | "COOLING" | "FAULT"` – derived label.
- `headline_metric_label: string` – e.g. "UMX ticks", "APX manifests", "ULedger entries".
- `headline_metric_value: number`.
- `secondary_metrics?: Array<{
    label: string,
    value: number | string
  }>` – optional extras.

**Backed by:**

- `MetricsSnapshotV1` counts (ticks, windows, manifests, ULedger entries).
- Optional `IntrospectionViewV1` counts.
- Governance state (for Codex/Guard rails) if needed.

---

### 3.6 GovernanceSnapshot

High‑level governance view for Governance & Budgets tab.

- `mode: string` – governance mode (e.g. `ENABLED`, `DISABLED`, etc.).
- `codex_action_mode: string` – e.g. `OFF`, `OBSERVE`, `ENFORCE`.
- `policy_set_hash: string` – hash of policy set for audit.
- `budget_controls: Array<{
    id: string,
    label: string,
    value: number,
    min?: number,
    max?: number,
    step?: number
  }>` – small set of numeric knobs exposed to UI.
- `meta?: Record<string, string>` – optional textual hints.

**Backed by:** `GovernanceConfigV1` and related policy types.

---

### 3.7 HistoryEntry

Minimal row for History list.

- `run_id: string`.
- `scenario_id: string`.
- `started_at: string`.
- `ended_at: string`.
- `state: "COMPLETED" | "FAULT" | "CANCELLED"`.
- `ticks_total?: number`.
- `ticks_completed?: number`.
- `duration_ms?: number`.

**Backed by:** Operator service run index written at end of each run.

---

### 3.8 LogEntry

Used by Logs & Console tab.

- `timestamp: string` – ISO.
- `level: "DEBUG" | "INFO" | "WARN" | "ERROR"`.
- `run_id?: string`.
- `event_type?: string` – e.g. `run_start`, `tick_complete`, `window_closed`.
- `message: string`.
- `payload?: Record<string, any>` – structured metadata.

**Backed by:** `StructuredLogEntryV1` and `StructuredLogger`.

---

## 4. API Surface by UI Tab

The spec is written as if using HTTP+JSON. Any RPC mechanism is acceptable if it preserves the same semantics.

### 4.1 Dashboard

#### GET `/state`

**Purpose:** Single call for Dashboard to see current situation.

**Returns:**

```json
{
  "current_run": RunStatus | null,
  "active_scenario": ScenarioSummary | null,
  "pillars": PillarStatus[] | [],
  "governance": GovernanceSnapshot | null
}
```

**Behaviour:**

- If no run is active, `current_run` is `null` and `pillars`/`governance` may show last known or default values.
- For a RUNNING run, `ticks_completed` and `progress` are updated based on logs/metrics.

---

#### POST `/runs`

**Purpose:** Start a new run.

**Body:**

```json
{
  "scenario_id": "string",
  "overrides": {
    "ticks_total"?: number,
    "logging_enabled"?: boolean,
    "metrics_enabled"?: boolean,
    "governance_profile"?: string
  }
}
```

**Returns:** `RunStatus` for the newly created run.

**Behaviour:**

- Service resolves `scenario_id` via `ScenarioRegistryV1` and underlying `RunConfigV1`.
- Builds a `SessionConfigV1` with applied overrides.
- Spawns a worker/thread/process to call `run_session(config)`.
- Immediately returns a `RunStatus` with `state = RUNNING` (or an error if creation fails).

---

#### POST `/runs/{run_id}/stop`

**Purpose:** Request that a run stop.

**Body:** empty or `{}`.

**Returns:** Updated `RunStatus`.

**Behaviour (Phase 7 floor):**

- If run has not started yet, mark as `CANCELLED`.
- If run is already running and the engine does not support cooperative cancellation, record the request and mark state as `CANCEL_REQUESTED` internally, but `RunStatus` remains `RUNNING` until natural completion.
- Future work may wire this into a cancellation flag checked within the tick loop.

---

#### (Optional Future) POST `/runs/{run_id}/pause` / `/resume` / `/step`

**Purpose:** True runtime control of the tick loop.

**Note:**

- Requires an incremental runner or cooperative pause points inside `run_cmp0_tick_loop`.
- For Phase 7, keep these out of scope or stubbed as not implemented.

---

### 4.2 Scenario & Config

#### GET `/scenarios`

**Purpose:** Populate Scenario list / pickers.

**Returns:** `ScenarioSummary[]`.

**Behaviour:**

- Built from `ScenarioRegistryV1`.
- May be cached and invalidated on changes.

---

#### GET `/scenarios/{id}`

**Purpose:** Show/edit details for a specific scenario.

**Returns:** `ScenarioDetail`.

**Behaviour:**

- Resolves scenario from registry.
- Loads associated `RunConfigV1` and maps fields into `ScenarioDetail.parameters` and flags.

---

#### POST `/scenarios/{id}`

**Purpose:** Update scenario’s underlying run configuration.

**Body:**

```json
ScenarioDetail
```

**Returns:** Updated `ScenarioDetail` or a minimal success object.

**Behaviour:**

- Applies allowed updates onto the underlying `RunConfigV1` representation.
- Writes JSON back to disk or to an appropriate config store.
- Invalidates cached registry/summary if relevant fields changed.

**Guardrails:**

- Service must validate that only whitelisted parameters are editable.

---

#### POST `/scenarios/{id}/activate`

**Purpose:** Mark a scenario as the active default for new runs.

**Body:** empty or `{}`.

**Returns:**

```json
{"active_scenario": ScenarioSummary}
```

**Behaviour:**

- Sets internal `active_scenario_id`.
- Does **not** start a run.
- `GET /state` reflects this in `active_scenario`.

---

### 4.3 Pillars

#### GET `/runs/{run_id}/pillars`

**Purpose:** Drive Pillars tab content.

**Returns:** `PillarStatus[]`.

**Behaviour:**

- For completed runs: built from final `MetricsSnapshotV1` and optional `IntrospectionViewV1`.
- For running runs: built from latest available metrics and governance snapshot.

**Note:**

- `GET /state` may include a shallow `pillars` array for current run to avoid extra round trips on Dashboard.

---

### 4.4 Governance & Budgets

#### GET `/governance`

**Purpose:** Show high‑level governance mode and budget knobs.

**Returns:** `GovernanceSnapshot`.

**Behaviour:**

- Reads configuration used as default for new `SessionConfigV1` instances.
- May be derived from a shared `RunConfigV1` template or a dedicated governance config file.

---

#### POST `/governance`

**Purpose:** Update governance defaults for future runs.

**Body:**

```json
{
  "mode"?: string,
  "codex_action_mode"?: string,
  "budget_controls"?: Array<{
    "id": string,
    "value": number
  }>
}
```

**Returns:** Updated `GovernanceSnapshot`.

**Behaviour:**

- Applies updates to the governance configuration used in `SessionConfigV1` construction.
- Optionally writes updated governance config back into disk config.

**Guardrails:**

- Only a small subset of policies is exposed as `budget_controls`.

---

### 4.5 History & Exports

#### GET `/history`

**Purpose:** Populate History tab list.

**Query Params:**

- `limit?: number` – max number of entries.
- `offset?: number` – pagination offset.

**Returns:**

```json
{
  "entries": HistoryEntry[],
  "total": number
}
```

**Behaviour:**

- Backed by a simple run index (e.g. JSONL or SQLite) written by the Operator Service when runs complete.

---

#### GET `/history/{run_id}`

**Purpose:** Detailed view for a specific completed run.

**Returns:**

```json
{
  "run": RunStatus,
  "pillars": PillarStatus[],
  "governance": GovernanceSnapshot,
  "metrics": Record<string, number | string>,
  "notes"?: string
}
```

**Behaviour:**

- Reads from run index + stored results/metrics snapshot.

---

#### GET `/history/{run_id}/export`

**Purpose:** Downloadable artefact for external analysis.

**Returns:** Binary/content representing a **run bundle**, e.g.:

- Serialized `SessionRunResult` + `IntrospectionViewV1`.
- Snapshot format from `ops.snapshots`.

**Behaviour:**

- Reads pre‑written snapshot if available.
- Otherwise builds a bundle from stored run artefacts.

---

### 4.6 Logs & Console

#### GET `/runs/{run_id}/logs`

**Purpose:** Drive Logs & Console tab.

**Query Params:**

- `cursor?: string` – opaque token for incremental fetch.
- `level?: string` – min log level filter.
- `event_type?: string` – optional filter (e.g. `tick_complete`).

**Returns:**

```json
{
  "entries": LogEntry[],
  "cursor": string
}
```

**Behaviour:**

- If `cursor` is omitted, returns logs from the start or from a reasonable recent window.
- If `cursor` is provided, returns entries after that point.
- Filtering may be applied server‑side or client‑side; behaviour must be stable.

---

#### (Optional) WebSocket `/runs/{run_id}/logs/stream`

**Purpose:** Push log entries to UI in near real time.

**Behaviour:**

- On connect, may send recent entries then tail new ones.

---

## 5. Integration Notes

### 5.1 Engine entrypoints to wrap

Minimal set of engine‑side functions/types the Operator Service must use:

- Configuration & scenarios:
  - `ScenarioRegistryV1` and helpers to load it.
  - `RunConfigV1` loading from JSON.
  - `SessionConfigV1` construction from config mappings.

- Execution:
  - `run_session(config: SessionConfigV1) -> SessionRunResult`.
  - (Future) an incremental tick runner or a wrapper around `run_cmp0_tick_loop`.

- Metrics:
  - `MetricsConfigV1`, `MetricsSnapshotV1`.
  - Functions that build metrics snapshot for a run.

- Governance:
  - `GovernanceConfigV1` and associated policy types.

- Introspection & snapshots:
  - `IntrospectionViewV1` builders.
  - Snapshot helpers (e.g. in `ops.snapshots`).

- Logging:
  - `LoggingConfigV1`, `StructuredLogger`, `StructuredLogEntryV1`.

### 5.2 Run lifecycle inside Operator Service

For each run, the Operator Service should track:

1. **Creation**
   - Assign `run_id`.
   - Build `SessionConfigV1` (scenario + overrides + governance/defaults).
   - Attach a `StructuredLogger`.
   - Persist an initial `HistoryEntry` stub.

2. **Execution**
   - Invoke `run_session(config)` in a way that allows log capture.
   - Update live `RunStatus` based on tick events / metrics.

3. **Completion**
   - Map `SessionRunResult` + final metrics into:
     - final `RunStatus`,
     - `PillarStatus[]`,
     - history index row.
   - Persist any export bundles if desired.

4. **Faults**
   - Catch exceptions and mark run as `FAULT` with `reason`.
   - Log fault via `StructuredLogger`.

---

## 6. Phase 7 Definition of Done (Operator Service)

Operator Service is considered Phase 7‑complete when:

1. All endpoints in this spec are implemented (except explicitly marked "future"), with stable JSON contracts.
2. The service can:
   - List scenarios and activate one.
   - Start a run using the active scenario.
   - Provide live `RunStatus` including progress for runs with logging/metrics enabled.
   - Surface pillar cards for current and historical runs.
   - Show and update high‑level governance settings used for new runs.
   - Maintain a local run history index and serve it to the UI.
   - Stream or page through log entries per run.
3. The existing Gate UI (Phase 7 Operator Surface) can be fully wired using **only** this API surface, with no direct calls into engine internals.

This spec is intended as the **contract** between engine implementation work and UI implementation work. Visual layout and technology choices on the UI side remain flexible as long as these interactions and behaviours are preserved.


## 14. Diagnostics & Tests Flows

### 14.1 Intent

Provide a **one-click way** from the operator surface to:

- Verify that the engine + operator service + configs are wired correctly (smoke test).
- Run a slightly heavier **self-check** using curated scenarios.
- See the latest diagnostics status and results without dropping to CLI.

Diagnostics are for **operators**, not engine developers: the focus is "does this stack work as deployed?", not full unit test coverage.

---

### 14.2 Content & Layout

Diagnostics is exposed via existing tabs rather than a new tab, to keep navigation simple:

- **Dashboard**
  - A small **"Diagnostics" card** in the lower area (or sidebar) showing:
    - Last diagnostics status: `Not run`, `Passed`, `Failed`, `Running`.
    - Last run time.
    - Primary button: **"Run quick smoke test"**.
    - Secondary link: **"View detailed report"** → navigates to History & Exports diagnostics view.

- **History & Exports tab**
  - A dedicated **"Diagnostics" section** above or alongside regular run history:
    - Table of diagnostics runs (latest first):
      - Diagnostic ID.
      - Profile: `SMOKE`, `SELF_CHECK`, `FULL_SUITE` (or similar).
      - Started/finished times.
      - Result: `PASSED`, `FAILED`, `ABORTED`.
    - Row click or "View" action opens a **Diagnostics details panel** with:
      - Overall result + summary message.
      - List of individual checks: name, status, short message.
      - Link to associated logs (e.g., opens Logs & Console filtered to that diagnostics run).

The visuals are flexible; the behaviours below are the contract.

---

### 14.3 Behaviour

Diagnostics runs are **separate from normal Gate runs** but share the same engine and logging infrastructure.

- **Profiles**
  - `SMOKE` – Very fast check (target seconds, not minutes):
    - Load scenario registry and at least one known-good run config.
    - Run a tiny run through the full stack (Gate → pillars → governance) with logging and metrics enabled.
    - Confirm no exceptions and basic metrics/logs are produced.
  - `SELF_CHECK` – Heavier but still reasonable for an operator to run ad hoc:
    - Run a small set of curated scenarios (e.g., baseline GF01, governance demo, Codex-off vs Codex-on).
    - Validate a handful of key invariants / metrics thresholds.
  - `FULL_SUITE` – Optional; may trigger a longer-running internal test harness or snapshot comparison. Can be hidden or clearly marked as "slow".

- **Concurrency rules**
  - Phase 7 floor: **no overlapping diagnostics and Gate runs.**
    - If a Gate run is `Running`, diagnostics controls are disabled in the UI.
    - If a diagnostics run is `Running`, run controls for normal scenarios are disabled.
  - Operator always sees a clear reason when a button is disabled (tooltip or label).

- **Lifecycle**
  - When the operator clicks **"Run quick smoke test"**:
    - UI calls the Operator Service diagnostics endpoint with profile `SMOKE`.
    - A new diagnostics run is created with its own ID and status `RUNNING`.
    - Dashboard Diagnostics card switches to a **running** state (spinner or similar).
    - When done, status flips to `PASSED` or `FAILED` with a timestamp.
  - If diagnostics **fail**:
    - The card shows `FAILED` plus a short human-readable summary (e.g. "Engine error while running GF01 scenario", "Snapshot mismatch for governance demo").
    - History & Exports diagnostics details show the breakdown with failing check(s).

---

### 14.4 Acceptance Criteria

- **DIA-AC-1**: From the Dashboard, the operator can trigger a **quick smoke test** and see the result (`PASSED` or `FAILED`) without leaving the page.
- **DIA-AC-2**: While a normal Gate run is in state `Running`, diagnostics controls are clearly disabled and attempting to start diagnostics via the UI does not create a diagnostics run.
- **DIA-AC-3**: While a diagnostics run is `Running`, the main run controls (Start/Resume) are disabled and the operator is informed that diagnostics are in progress.
- **DIA-AC-4**: Each diagnostics run appears in the **History & Exports** diagnostics section with:
  - Profile name,
  - Start/end times,
  - Final result (`PASSED`, `FAILED`, or `ABORTED`).
- **DIA-AC-5**: For a **FAILED** diagnostics run, the details view shows at least:
  - A short overall failure reason, and
  - At least one individual failing check with a name and message.
- **DIA-AC-6**: Diagnostics flows do not require internet access and run using the same offline configs and engine binaries as normal Gate runs.


## 7. Diagnostics & Tests API

### 7.1 Data Shapes

#### 7.1.1 DiagnosticProfile

Represents the **kind of diagnostics run** requested.

- `id: string` – stable identifier, e.g. `SMOKE`, `SELF_CHECK`, `FULL_SUITE`.
- `label: string` – human-friendly label.
- `description: string` – short description of what the profile does.

Profiles are defined/configured inside the Operator Service, not by the UI.

---

#### 7.1.2 DiagnosticStatus

Lifecycle state of a diagnostics run.

- `diagnostic_id: string` – unique within the Operator Service.
- `profile_id: string` – one of the configured profiles (e.g. `SMOKE`).
- `state: "PENDING" | "RUNNING" | "PASSED" | "FAILED" | "ABORTED"`.
- `created_at: string` – ISO timestamp.
- `started_at?: string` – ISO, present once execution begins.
- `finished_at?: string` – ISO, present once terminal.
- `summary?: string` – short human-readable summary.
- `checks_passed?: number` – optional number of passing checks.
- `checks_failed?: number` – optional number of failing checks.

---

#### 7.1.3 DiagnosticResult

Detailed outcome of a diagnostics run.

- `status: DiagnosticStatus` – top-level summary.
- `checks: Array<{
    id: string,
    name: string,
    description?: string,
    state: "PASSED" | "FAILED" | "SKIPPED",
    message?: string
  }>` – individual checks.
- `related_run_ids?: string[]` – optional list of normal Gate `run_id`s created as part of diagnostics.

**Backed by:**

- A small diagnostics runner inside the Operator Service that internally uses:
  - `EngineRuntime` / `SessionConfigV1` / `run_session` to run small scenarios.
  - Existing snapshot/metrics helpers where appropriate.

---

### 7.2 Endpoints

Diagnostics endpoints give the UI a simple interface for running self-checks and seeing results.

#### 7.2.1 GET `/diagnostics/profiles`

**Purpose:** Discover available diagnostics profiles.

**Returns:**

```json
DiagnosticProfile[]
```

**Behaviour:**

- Allows UI to populate dropdowns or labels without hardcoding profile IDs.

---

#### 7.2.2 POST `/diagnostics`

**Purpose:** Start a new diagnostics run.

**Body:**

```json
{
  "profile_id": "SMOKE" | "SELF_CHECK" | "FULL_SUITE",
  "notes"?: string
}
```

**Returns:**

```json
DiagnosticStatus
```

**Behaviour:**

- If a normal Gate run is currently `RUNNING`, the service **rejects** the request with a clear error (e.g. HTTP 409 with message "Gate run in progress").
- If another diagnostics run is `RUNNING`, the service also rejects the request.
- On success, creates a new diagnostics run record with `state = PENDING` and schedules execution in a worker.
- Execution will:
  - Run one or more engine scenarios or internal checks depending on `profile_id`.
  - Aggregate results and set `state = PASSED` or `FAILED`.

---

#### 7.2.3 GET `/diagnostics`

**Purpose:** List diagnostics runs for display in History & Exports.

**Query Params:**

- `limit?: number` – max number of entries to return.
- `offset?: number` – pagination.

**Returns:**

```json
{
  "entries": DiagnosticStatus[],
  "total": number
}
```

**Behaviour:**

- Returns diagnostics runs ordered by `created_at` descending.

---

#### 7.2.4 GET `/diagnostics/{diagnostic_id}`

**Purpose:** Detailed view of a diagnostics run.

**Returns:** `DiagnosticResult`.

**Behaviour:**

- Includes top-level status and full list of checks.
- May include links to related normal Gate run IDs to allow drilling into logs/metrics via existing endpoints.

---

### 7.3 Behaviour & Implementation Notes

- Diagnostics runs must:
  - Use the **same offline engine** and configs as normal Gate runs.
  - Avoid reaching out to any external network resources.
- Profiles are intentionally **implementation-defined**:
  - `SMOKE` should be tuned to complete quickly (seconds) and focus on wiring issues.
  - `SELF_CHECK` can include more thorough checks but should remain operator-friendly in duration.
  - `FULL_SUITE` is optional and may represent a slower, more exhaustive test set.
- The Operator Service should record diagnostics runs in the **same history store** as normal runs or a parallel diagnostics index, so that UI can list them reliably.

---

### 7.4 Phase 7 Diagnostics Definition of Done

Diagnostics support is considered Phase 7-complete when:

1. `GET /diagnostics/profiles` returns at least one profile (`SMOKE`) and optionally others.
2. `POST /diagnostics` with `profile_id = "SMOKE"` starts a diagnostics run that:
   - Executes at least one real engine scenario end-to-end, and
   - Surfaces `PASSED`/`FAILED` appropriately based on engine success.
3. `GET /diagnostics` lists past diagnostics runs with their final states.
4. `GET /diagnostics/{diagnostic_id}` returns a breakdown of checks, including at least one named check.
5. Diagnostics endpoints respect the **no-concurrency** rule with normal Gate runs (attempting to start diagnostics during a run yields a clear error and no diagnostics run is created).
6. All diagnostics functionality operates correctly in a **fully offline** environment.

