# Trinity Gate — Phase 7 Operator Service Spec (Draft v0.1)

> Thin adapter between the Phase 6 Aether engine and the Phase 7 Trinity Gate Operator UI. This spec defines **service‑level contracts** (shapes + behaviours), not implementation details or framework.

---

## 1. Purpose & Scope

### 1.1 Purpose

The Operator Service is a long‑lived process that:

- Loads scenarios and run configs from the Phase 6 repo.
- Starts and supervises Gate runs.
- Tracks current run state, metrics, logs, and artefacts.
- Provides a clean, UI‑friendly API for the Trinity Gate Operator Surface.

It hides engine internals (`SessionConfigV1`, `SessionRunResult`, tick loop details) behind simple JSON‑like shapes.

### 1.2 In Scope (Phase 7)

- Read APIs for:
  - Current Gate run state and active scenario.
  - Scenario registry and scenario details.
  - Pillar status snapshots (derived from metrics + governance + introspection).
  - Governance snapshot (high‑level knobs only).
  - Run history and per‑run details.
  - Structured logs for a given run.
- Write APIs for:
  - Run controls: start, stop (pause/step/resume stubbed for future phases).
  - Scenario updates (where allowed).
  - Governance/budget updates (small, curated subset).

Out of scope for Phase 7:

- True interactive stepping (pause/step/resume) inside the tick loop.
- Multi‑user auth/permissions.
- Horizontal scaling or multi‑node orchestration.

---

## 2. Engine Dependencies (Phase 6 Repo)

The service is built over these core types and functions:

- **Configs & Scenarios**
  - `RunConfigV1` – run configuration (JSON‑backed).
  - `ScenarioRegistryV1` – registry of named scenarios.
  - Helpers: `load_scenario_registry`, `load_run_config`, `load_run_session_config`.

- **Runs & Results**
  - `SessionConfigV1` – in‑memory session config.
  - `run_session(config: SessionConfigV1) -> SessionRunResult`.
  - `GF01RunResult` / tick loop core.

- **Introspection**
  - `IntrospectionViewV1` – structured view over a run.
  - `build_introspection_view(run_result)`.

- **Metrics**
  - `MetricsConfigV1`, `MetricsSnapshotV1`.

- **Logging**
  - `LoggingConfigV1`, `StructuredLogEntryV1`, `StructuredLogger`.

- **Governance**
  - `GovernanceConfigV1`, `BudgetPolicyV1`, `TopologyPolicyV1`, `SafetyPolicyV1`.

- **Snapshots/Exports**
  - `write_snapshot`, `compare_snapshots`, `SnapshotDiff` (optional backing for History & Exports).

The Operator Service does **not** modify these types; it only instantiates and composes them.

---

## 3. UI‑Facing Data Models

These are the shapes exposed to the UI. They are derived from engine types but deliberately simpler.

> Naming is illustrative; real on‑wire names can follow your API conventions.

### 3.1 ScenarioSummary

Minimal info for listing scenarios.

- `id: string` – scenario ID.
- `name: string` – human‑friendly label (can mirror `id`).
- `description: string`
- `tags: string[]` – optional tags.
- `runtime_hint: string` – e.g., `"tiny"`, `"small"`, `"full"` (from registry metadata).
- `pillars: string[]` – names/IDs of pillars primarily involved.

### 3.2 ScenarioDetail

Full editable view for a scenario.

- All fields from `ScenarioSummary`.
- `run_config_id: string` – backing run config identifier/path.
- `core_params: object` – curated subset of `RunConfigV1` fields exposed in UI, e.g.:
  - `ticks_total`
  - `primary_window_id`
  - `metrics_enabled`
  - `logging_enabled`
- `governance_preset?: string` – mapped from governance section of run config.
- `advanced?: object` – optional blob for fields only shown in an expert view.

### 3.3 RunStatus

Live and historical view of a run.

- `run_id: string`
- `state: "idle" | "running" | "completed" | "fault" | "cancelled"`
- `scenario_id: string`
- `started_at: ISO8601 string | null`
- `ended_at: ISO8601 string | null`
- `ticks_total: number | null`
- `ticks_completed: number | null`
- `progress: number | null` – 0..1, derived from logs or metrics.
- `fault_reason?: string`

### 3.4 PillarStatus

Card‑level snapshot for each pillar.

- `pillar_id: "aether" | "press" | "umx" | "loom" | "codex"`
- `name: string`
- `status: "idle" | "warming" | "running" | "cooling" | "fault" | "unknown"`
- `load?: number` – 0..1 or other normalized scale.
- `headline_metric?: string` – small human string like `"32 windows"`, `"1024 motifs"`.
- `secondary_metric?: string`
- `governance_mode?: string` – e.g., Codex action mode when relevant.

### 3.5 GovernanceSnapshot

High‑level governance view.

- `mode: string` – overall governance mode.
- `codex_action_mode: string`
- `budget_knobs: { [key: string]: number }` – small curated set (e.g., 1–3 budgets).
- `policy_set_hash: string`

### 3.6 HistoryEntry

List view for past runs.

- `run_id: string`
- `scenario_id: string`
- `started_at: ISO8601 string`
- `ended_at: ISO8601 string`
- `result: "completed" | "fault" | "cancelled"`
- `ticks_total: number`
- `summary_metrics?: object` – small subset (e.g., window_count, nap_count).

### 3.7 LogEntry

Structured log entry for Logs & Console tab.

- `timestamp: ISO8601 string`
- `level: "DEBUG" | "INFO" | "WARN" | "ERROR"`
- `event_type: string` – e.g., `"run_start"`, `"tick_complete"`, `"window_closed"`.
- `run_id: string`
- `message: string`
- `payload?: object` – payload from `StructuredLogEntryV1` when present.

---

## 4. API Surface by UI Tab

This section maps Trinity Gate UI tabs to Operator Service endpoints.

> All paths are illustrative; method+path+shape is what matters.

### 4.1 Dashboard

**Goal:** one‑glance view of current state + run controls.

#### 4.1.1 GET `/state`

Returns the current operator surface state.

- **Response**
  - `run: RunStatus | null`
  - `active_scenario: ScenarioSummary | null`
  - `pillars: PillarStatus[]`

- **Backed by**
  - In‑memory `RunHandle` (see Section 5).
  - Cached `ScenarioRegistryV1`.
  - Last `MetricsSnapshotV1` and/or `IntrospectionViewV1` (for pillar metrics).

#### 4.1.2 POST `/runs`

Start a new run.

- **Request body**
  - `scenario_id: string`
  - `overrides?: { ticks_total?: number; metrics_enabled?: boolean; logging_enabled?: boolean; governance_preset?: string; }`

- **Behaviour**
  - Resolve `ScenarioRegistryV1` entry → `RunConfigV1`.
  - Apply overrides → new `RunConfigV1` instance.
  - Build `SessionConfigV1` (using existing helpers).
  - Create a `RunHandle`, start `run_session(config)` in background.
  - Attach a `StructuredLogger` and metrics collection if configured.

- **Response**
  - Initial `RunStatus` for the new `run_id`.

#### 4.1.3 POST `/runs/{run_id}/stop`

Request that a run stop as soon as practical.

- **Phase 7 behaviour**
  - If run has not started: mark as `cancelled`.
  - If run is already in flight: best‑effort stop (Phase 7 may not support mid‑tick abort).
  - Mark status as `cancelled` or `fault` accordingly.

- **Future**
  - Integrate cooperative cancellation into `run_cmp0_tick_loop`.

#### 4.1.4 (Future) `/runs/{run_id}/pause`, `/resume`, `/step`

Defined in API but explicitly marked **not implemented** for Phase 7. UI can show disabled buttons where required.

---

### 4.2 Scenario & Config Tab

**Goal:** list scenarios, inspect one, edit, set active.

#### 4.2.1 GET `/scenarios`

- **Response**: `ScenarioSummary[]`
- **Backed by**: `ScenarioRegistryV1` loaded from repo fixtures.

#### 4.2.2 GET `/scenarios/{id}`

- **Response**: `ScenarioDetail`
- **Backed by**:
  - `ScenarioRegistryV1` for metadata.
  - `RunConfigV1` loaded from the referenced run config file.

#### 4.2.3 POST `/scenarios/{id}`

Update editable fields of a scenario.

- **Request**: `ScenarioDetail` (or patch) with only allowed fields populated.
- **Behaviour**:
  - Validate changes.
  - Write updated `RunConfigV1` back to disk or a configured config store.
  - Optionally refresh `ScenarioRegistryV1` cache.

#### 4.2.4 POST `/scenarios/{id}/activate`

Set active scenario for future runs.

- **Behaviour**:
  - Operator Service records `active_scenario_id` in memory (and optionally on disk).
  - `GET /state` starts returning the new active scenario.

---

### 4.3 Pillars Tab

**Goal:** overview of all pillars + focused Gate panel (read‑only).

#### 4.3.1 GET `/runs/{run_id}/pillars`

- **Response**: `PillarStatus[]`
- **Backed by**:
  - `SessionRunResult.metrics: MetricsSnapshotV1`.
  - Selected values from `IntrospectionViewV1`.
  - `GovernanceConfigV1` for governance‑related modes.

Example mapping (illustrative only):

- Aether → tick/nap coverage metrics.
- Press → APX manifests & APXi counts.
- UMX → ledger length, motif counts.
- Loom → block counts / window structure.
- Codex → action proposals evaluated/applied.

Phase 7: cards are read‑only; no pillar mutations via this endpoint.

---

### 4.4 Governance & Budgets Tab

**Goal:** show and adjust high‑level governance knobs.

#### 4.4.1 GET `/governance`

- **Response**: `GovernanceSnapshot`
- **Backed by**:
  - A "base" `GovernanceConfigV1` template used when building `SessionConfigV1`.

#### 4.4.2 POST `/governance`

- **Request**: partial `GovernanceSnapshot` with editable fields (e.g., action mode and 1–3 budgets).
- **Behaviour**:
  - Validate and update the base `GovernanceConfigV1` the service uses.
  - Persist to disk if desired (e.g., a `governance_base.json` file).

**Note:** governance changes affect *future* runs built from the updated base config; they do not retroactively change already‑running sessions in Phase 7.

---

### 4.5 History & Exports Tab

**Goal:** browse past runs and export artefacts.

#### 4.5.1 GET `/history`

- **Response**: `HistoryEntry[]` (e.g., last N runs).
- **Backed by**:
  - An Operator Service run index (JSON/SQLite) updated when runs finish.

#### 4.5.2 GET `/history/{run_id}`

- **Response**:
  - `run: RunStatus`
  - `summary_metrics: object` – subset of `MetricsSnapshotV1`.

#### 4.5.3 GET `/history/{run_id}/export`

- **Response**: file download or presigned path to a bundle containing:
  - Serialized `SessionRunResult`.
  - `IntrospectionViewV1`.
  - Optional snapshot written with `write_snapshot`.

---

### 4.6 Logs & Console Tab

**Goal:** show structured logs for the current or past run.

#### 4.6.1 GET `/runs/{run_id}/logs`

- **Query params**:
  - `since?: string` – cursor or timestamp.
  - `level?: string` – log level filter.
  - `event_type?: string` – event filter.

- **Response**:
  - `entries: LogEntry[]`
  - `next_cursor: string`

- **Backed by**:
  - In‑memory `StructuredLogger` attached to the `RunHandle`, or
  - Tail over log file produced by the logger.

#### 4.6.2 (Optional) WebSocket `/runs/{run_id}/logs/stream`

- **Behaviour**:
  - Push `LogEntry` objects to connected clients in real time.

---

## 5. Internal Service Model

### 5.1 RunHandle

Internal in‑memory representation of a run under supervision.

- `run_id: string`
- `session_config: SessionConfigV1`
- `status: RunStatus`
- `logger: StructuredLogger`
- `metrics_snapshot?: MetricsSnapshotV1`
- `introspection_view?: IntrospectionViewV1`
- `thread_or_task: handle` – reference to background job.

The Operator Service maintains:

- `current_run?: RunHandle`
- `runs_by_id: Map<string, RunHandle | CompletedRunRecord>`

`CompletedRunRecord` is a persisted, compact version / pointer used by History.

### 5.2 Lifecycle

1. **Startup**
   - Load `ScenarioRegistryV1`.
   - Optionally load base governance config.
   - Initialise empty run index.

2. **Starting a run**
   - Validate that no conflicting run is active (Phase 7 may enforce single active run).
   - Build `SessionConfigV1`.
   - Create `RunHandle` with attached logger.
   - Start `run_session(config)` in background.

3. **During a run**
   - Structured logs flow into `RunHandle.logger`.
   - Metrics snapshot built at the end (Phase 7 floor) or periodically (future).
   - `RunStatus` is updated as the run progresses.

4. **Completion**
   - Build `MetricsSnapshotV1` + optional `IntrospectionViewV1`.
   - Persist summary into run index (for History).
   - Optionally write a full snapshot file.

5. **Shutdown**
   - Cleanly mark any active run as cancelled or incomplete.
   - Flush run index and logs.

---

## 6. Phase 7 Acceptance Criteria (Operator Service)

The Operator Service is considered Phase 7 complete when:

1. **State API**
   - `GET /state` returns:
     - `run` matching current run status (or `null` when idle),
     - `active_scenario` matching last activated scenario,
     - `pillars` containing one entry per pillar with non‑empty `status`.

2. **Run Control**
   - `POST /runs` can start a run from any scenario in `ScenarioRegistryV1`.
   - `POST /runs/{id}/stop` marks a run as `cancelled` or `fault` and the status is reflected in both `GET /state` and `GET /history/{id}`.

3. **Scenarios**
   - `GET /scenarios` lists all registry entries.
   - `GET /scenarios/{id}` returns a detailed view including core run config parameters.
   - `POST /scenarios/{id}/activate` updates `active_scenario` for `GET /state`.

4. **Governance**
   - `GET /governance` returns a non‑empty `GovernanceSnapshot`.
   - `POST /governance` updates at least one editable governance parameter, which is reflected in newly started runs.

5. **History**
   - `GET /history` lists at least the last N runs with accurate status.
   - `GET /history/{id}` returns `RunStatus` and summary metrics for that run.

6. **Logs**
   - `GET /runs/{id}/logs` returns structured log entries for a run when logging is enabled.
   - Filtering by level works as expected.

7. **Resilience**
   - Service startup and shutdown do not corrupt scenario registry or run index.
   - If the underlying engine throws an error, the Operator Service surfaces a `fault` status and an explanatory message through its APIs.

---

## 7. Notes & Future Extensions

- **Pause/Resume/Step**
  - Requires cooperative cancellation and stepping support in the tick loop. API is reserved but not implemented in Phase 7.

- **Multi‑run and multi‑tenant**
  - Phase 7 assumes a single operator and at most one active run. Future versions may allow concurrent runs and session scoping.

- **Security**
  - Phase 7 can run on a trusted local network. Future phases can add authentication and role separation (Operator vs Overseer vs Observer).

This spec is intentionally framework‑agnostic so it can be implemented as a CLI‑spawned HTTP server, a lightweight web service, or integrated into a larger control plane without changing the Gate UI contract.

