# Trinity Gate — Phase 7 Operator Surface UI Spec (Draft v0.1)

> This document treats the existing HTML mock (`aether_gate_operator_surface_mock_ui_2025_11_30.html`) as a **wireframe**, not a contract. Layout and visuals can change. The spec below captures the **information architecture, states, and behaviours** that Phase 7 must deliver.

---

## 1. Purpose & Scope

### 1.1 Purpose

The Trinity Gate Operator Surface is the **human control membrane** for the five pillars. It gives an operator a single place to:

- See **what the Gate is doing right now** (state, scenario, run progress, pillar health).
- **Start, pause, stop, and step** gate runs safely.
- **Configure scenarios** and store/load them.
- Inspect and nudge **pillars, budgets, and guardrails** at a high level.
- Inspect **history, exports, and logs** for a given run.

### 1.2 Phase 7 Scope

Phase 7 covers the first **usable operator surface** wired to the existing Gate/UMX implementation.

In scope:

- Navigation shell with tabs (Dashboard, Scenario & Config, Pillars, Governance & Budgets, History & Exports, Logs & Console).
- Live binding to the Gate state model (Idle/Running/Paused/Fault, active scenario, tick count, etc.).
- Run control actions: start, pause, step, stop, reset.
- Scenario selection, inspection, and editing at a **structured field** level.
- High‑level pillar overview (one card per pillar) with key metrics and statuses.
- Governance/budget summary and basic adjustments (where supported by the back end).
- Read‑only history of past runs with basic filtering.
- Read‑only logs/console stream with filtering and levels.

Out of scope for Phase 7 (can be later phases):

- Fine‑grained pillar internals editing.
- Rich analytics, charts, or multi-run comparisons beyond simple tables.
- Multi‑user authentication/permissions.

---

## 2. Users & Roles (Phase 7)

Phase 7 assumes a single generic **Operator** role.

- **Operator**
  - Starts and stops runs.
  - Chooses and configures scenarios.
  - Monitors pillars and budgets.
  - Reads history/logs.

Future roles (not implemented but good to keep in mind):

- **Overseer** – Can change global guardrails, approve risky runs.
- **Observer** – Read-only access for watching runs.

---

## 3. Core Concepts & State Model

### 3.1 Gate Run State

Canonical top‑level state exposed to the UI:

- **Idle** – No active run. A scenario may be selected but not running.
- **Running** – Active run in progress.
- **Paused** – Run is suspended; can resume or stop.
- **Fault** – Run halted due to a safety trip, error, or manual stop with error condition.

Each run has at minimum:

- Run ID.
- Scenario ID.
- Start time.
- Current tick / step index.
- Optional end condition (ticks, convergence, manual stop, fault reason).

### 3.2 Scenario

A Scenario is a bundle of parameters the Gate uses to drive a run.

Core fields in UI (names can map directly or via adapter to engine fields):

- Scenario ID / name.
- Description.
- Pillar weights or emphasis (e.g., Gate, Aether, UMX, Loom, Codex sliders or weight vector).
- Baseline intensity / volatility / time horizon (as applicable).
- Any safety profile or guardrail preset tagged to that scenario.

### 3.3 Pillar Snapshot

For each pillar (Aether, Astral Press, UMX, Aevum Loom, Codex Eterna), the Gate exposes:

- Status: Idle / Warming up / Running / Cooling / Fault.
- Core load metric (0–1 or similar scale).
- Signal or health indicator.
- Any pillar‑specific headline metric (e.g., coverage, variance, etc.).

The UI only needs a **read‑only snapshot** in Phase 7.

---

## 4. Navigation Model

Top‑level navigation is a single row of tabs, roughly based on the mock:

1. **Dashboard** – Live overview and run controls.
2. **Scenario & Config** – Select, view, and edit scenarios.
3. **Pillars** – Overview of all pillars and a more detailed view for Trinity Gate.
4. **Governance & Budgets** – Budgets, guardrails presets, and global toggles.
5. **History & Exports** – Past runs, basic filters, and export hooks.
6. **Logs & Console** – Raw log stream and filters.

Guardrail: At most **one tab is active** at a time. Tab selection never causes destructive side‑effects.

---

## 5. Dashboard Tab

### 5.1 Intent

Give the operator a **one‑glance view** of what’s happening right now plus direct access to run controls.

### 5.2 Content & Layout (from mock, as IA only)

- **Header row**
  - App title and short description.
  - Scenario label (e.g., `baseline_calm_start`).
  - Status pill indicating Gate state (Idle/Running/Paused/Fault).

- **Run controls block**
  - Primary buttons: Start/Resume, Pause, Stop/Reset, Step.
  - A simple run mode toggle, if supported (e.g., Live vs Dry‑run).

- **Scenario & autopilot highlights**
  - Current scenario summary card.
  - Autopilot/automation toggles (e.g., allow automatic stop or guardrail priority).

- **Pillar summary grid**
  - One card per pillar: A (Aether), P (Astral Press), U (UMX), L (Aevum Loom), C (Codex Eterna).
  - Each card shows status, core load, key metric(s), and intensity/neutral label.

### 5.3 Behaviour

- Run control buttons are enabled/disabled according to Gate state.
  - Idle → Start enabled, Pause/Stop/Step disabled.
  - Running → Pause/Stop/Step enabled, Start/Resume disabled.
  - Paused → Resume and Stop enabled, Step optional.
  - Fault → Only Reset/Stop enabled.

- Scenario label and pillar cards update in near‑real time (polling or push; implementation detail, but UI assumes updates within a short interval).

### 5.4 Acceptance Criteria

- **D-AC-1**: When a run is **Idle**, the Dashboard shows state as “Idle” and only a **Start** action is available as primary.
- **D-AC-2**: When a run is **Running**, the Dashboard state pill changes to “Running” and the **Pause** and **Stop** buttons become enabled.
- **D-AC-3**: When the active scenario changes (via Scenario tab), the new scenario name appears in the Dashboard header within one refresh interval.
- **D-AC-4**: Each pillar card shows at least **status** and **one numeric or categorical metric** per pillar.
- **D-AC-5**: Attempting to use a run control that is disabled never triggers any action at the back end.

---

## 6. Scenario & Config Tab

### 6.1 Intent

Let the operator **select, inspect, and tune** a scenario before or between runs.

### 6.2 Content & Layout (IA)

- **Scenario picker**
  - List or table of available scenarios.
  - Ability to search or filter by name/tag.

- **Scenario details panel**
  - Name, description, tags.
  - Core numeric/intensity parameters.
  - Pillar weight sliders or inputs.
  - Safety/guardrail preset selection if available.

- **Actions**
  - Set as active scenario.
  - Save changes.
  - Save as new scenario (clone).

### 6.3 Behaviour

- Changing fields updates a **draft** until explicitly saved.
- Setting a scenario as active does **not** automatically start a run.
- UI should guard against starting a run with unsaved changes (either auto‑save or prompt).

### 6.4 Acceptance Criteria

- **S-AC-1**: The operator can select a scenario from a list and mark it as the active scenario.
- **S-AC-2**: Editing a scenario field marks the scenario as **dirty** until saved.
- **S-AC-3**: If the operator navigates away with unsaved scenario changes, the UI either **prompts to save/discard** or **persists the draft** in a predictable way.
- **S-AC-4**: After saving, the updated scenario fields are reflected on the Dashboard header within one refresh interval.

---

## 7. Pillars Tab

### 7.1 Intent

Provide a more detailed overview of all pillars, plus a slightly deeper view of the **Trinity Gate pillar** without overwhelming the operator.

### 7.2 Content & Layout (IA)

- **Pillar overview grid** (as per Dashboard but larger)
  - Aether, Astral Press, UMX, Aevum Loom, Codex Eterna cards.

- **Trinity Gate panel**
  - Gate state.
  - Internal headline metrics such as current tick, effective budgets, and any key safety counters.
  - Read‑only view of current guardrail profile applied.

- **Placeholder panels for other pillars**
  - Can remain mostly read‑only in Phase 7.

### 7.3 Behaviour

- Selecting a pillar highlights it and shows more metrics in a side panel.
- No destructive edits occur in Pillars tab in Phase 7; it is effectively read‑only.

### 7.4 Acceptance Criteria

- **P-AC-1**: The Pillars tab shows one card per pillar with status and at least one metric.
- **P-AC-2**: Selecting a pillar focuses it and shows additional details.
- **P-AC-3**: No control in the Pillars tab can change run state (start/pause/stop) in Phase 7.

---

## 8. Governance & Budgets Tab

### 8.1 Intent

Surface high‑level governance controls and budget settings that influence how aggressively the Gate and pillars operate.

### 8.2 Content & Layout (IA)

- **Budget overview**
  - Textual or numeric summaries of key budgets (e.g., exploration vs exploitation, safety vs performance).

- **Controls** (Phase 7 minimal set)
  - Sliders or numeric inputs to adjust one or two key global budgets.
  - Toggle(s) for strict safety mode vs relaxed mode, if exposed by the engine.

- **Presets**
  - Optional drop‑down to apply guardrail presets (e.g., "conservative", "balanced", "aggressive"), if defined.

### 8.3 Behaviour

- Changing a budget or guardrail preset sends a request to the back end **only on explicit apply/save**.
- When a preset is applied, visible values update to match the applied settings.

### 8.4 Acceptance Criteria

- **G-AC-1**: Governance tab displays the current value of each budget parameter exposed by the back end for Phase 7.
- **G-AC-2**: Changing a budget value and saving triggers an update, which is reflected on the Trinity Gate panel within one refresh interval.
- **G-AC-3**: If a budget update fails, the UI shows a clear non‑blocking error state (no silent failure).

---

## 9. History & Exports Tab

### 9.1 Intent

Let the operator browse past Gate runs and export data for deeper analysis outside the UI.

### 9.2 Content & Layout (IA)

- **Run history list**
  - Table or list of runs, each with:
    - Run ID.
    - Scenario ID.
    - Start/end time.
    - Result (Completed, Stopped, Fault, etc.).
    - Tick count or duration.

- **Run details panel**
  - For the selected run: summary, key metrics, and notes.

- **Export actions**
  - Buttons to export run artefacts (e.g., JSON, CSV, bundle) if available from Gate.

### 9.3 Behaviour

- Selecting a run updates the details panel.
- Export buttons call back‑end export endpoints or trigger file generation if supported; otherwise can remain stubbed for Phase 7.

### 9.4 Acceptance Criteria

- **H-AC-1**: History tab lists at least the last N runs (N definable per configuration; default can be modest).
- **H-AC-2**: Selecting a run updates the details pane with that run’s data.
- **H-AC-3**: If exports are wired, triggering an export returns a file or clear success indication; on failure, UI shows a clear error message.

---

## 10. Logs & Console Tab

### 10.1 Intent

Expose a readable stream of logs from the Gate and pillars for debugging, without requiring the operator to drop to raw console.

### 10.2 Content & Layout (IA)

- **Log stream area**
  - Scrollable area where log entries appear.

- **Filters**
  - Level filters (Info, Warning, Error, Debug as supported).
  - Optional text search.

- **Run scope selector**
  - Option to view logs for the current run only vs all system logs.

### 10.3 Behaviour

- New log entries append to the bottom in real time while the tab is open.
- Filters apply client‑side or server‑side; behaviour must be consistent.
- Optional auto‑scroll toggle.

### 10.4 Acceptance Criteria

- **L-AC-1**: With a run in progress, the Logs tab shows new entries arriving without requiring a manual refresh.
- **L-AC-2**: Toggling log level filters changes which entries are visible.
- **L-AC-3**: Selecting "current run only" limits entries to logs tagged with that run ID.

---

## 11. Non‑Functional Requirements

These are **Phase 7 floor requirements**, not long‑term ceilings.

- **NFR-1 – Responsiveness**
  - UI must remain usable at common desktop resolutions; mobile layout is nice‑to‑have but not a blocker.

- **NFR-2 – Clarity**
  - All destructive actions (stop, reset, applying governance changes) must be clearly labelled and visually distinct from passive actions.

- **NFR-3 – Safety feedback**
  - Fault or safety‑halt states must be visually obvious on the Dashboard and, where relevant, in other tabs.

- **NFR-4 – Accessibility**
  - Basic keyboard navigation between tabs and primary actions is supported.

---

## 12. Integration Boundaries (High Level)

Phase 7 UI talks to the existing Gate/UMX implementation via an adapter layer that exposes:

- Read APIs for:
  - Current Gate run state.
  - Active scenario and its parameters.
  - Pillar snapshots.
  - Governance/budget values.
  - Run history.
  - Logs (stream or batched).

- Write APIs for:
  - Run controls (start, pause, stop, reset, step).
  - Scenario create/update.
  - Governance/budget updates.

Implementation details and exact payload shapes live in the engine/repo; this spec focuses on **what the operator surface must be able to see and do**.

---

## 13. Phase 7 Definition of Done (UI Layer)

To call Phase 7 complete from a **Gate UI** point of view:

1. Navigation with all 6 tabs is live and wired to content.
2. Dashboard shows live Gate state and pillar cards, and fully supports start/pause/stop (with state‑driven enable/disable behaviour).
3. Scenario & Config tab can:
   - List scenarios,
   - Edit a scenario,
   - Save changes,
   - Mark a scenario as active.
4. Pillars tab shows all pillars with at least the agreed minimum metrics and a focused Trinity Gate panel.
5. Governance & Budgets tab shows current values and can apply at least one global budget change successfully.
6. History & Exports tab lists past runs and shows details for the selected run.
7. Logs & Console tab shows live logs for the current run.
8. All acceptance criteria per section are satisfied in tests or a manual checklist.

This spec is intentionally **layout‑agnostic**: it takes cues from the HTML mock for structure, but any visual design that preserves the above behaviours and flows is acceptable for Phase 7.

