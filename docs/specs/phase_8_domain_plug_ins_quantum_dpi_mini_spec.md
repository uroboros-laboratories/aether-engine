# Phase 8 — Domain Plug-ins (DPI) & Quantum DPI Mini-Spec

## 1. Scope & Goals

**Phase 7** delivers the core Trinity Gate operator surface and operator service on top of the Aether engine.

**Phase 8** introduces a **Domain Plug-ins (DPI)** layer that:
- Sits **on top of** the existing Aether stack (Gate → UMX → Loom → Press → Codex).
- Exposes domain-specific workflows (e.g. quantum ingestion/simulation/emulation) without modifying core physics.
- Wires into the engine via the existing Operator Service, not by bypassing or patching UMX/Loom directly.

The first concrete DPI is the **Quantum DPI**, providing:
- Quantum data **ingestion** (from files / external sources).
- Quantum **simulation** (classical/emulated circuits).
- Quantum **emulation / experiments** (e.g. the H1 spin-chain law-finder experiment).

Phase 8 is additive and non-breaking with respect to Phase 7.

---

## 2. Architecture Placement

### 2.1 Layering

Layers after Phase 8:

- **Engine Core (Phase 6)**
  - Aether pillars: Gate, UMX, Loom, Press, Codex, NAP, etc.
- **Operator Service (Phase 7)**
  - REST API over engine: scenarios, runs, governance, history, logs, diagnostics.
- **Operator UI (Phase 7)**
  - Tabs: Dashboard, Scenario & Config, Pillars, Governance & Budgets, History & Exports, Logs & Console.
- **Domain Plug-ins (Phase 8)**
  - Logical DPI registry and API in the Operator Service.
  - New **Domain Plug-ins** tab in the Operator UI.
  - Quantum DPI as the first concrete domain plug-in.

### 2.2 Non-goals

- No changes to core Aether pillar semantics (UMX, Loom, Press, Codex remain as-is).
- No direct DPI writes into UMX state; DPIs must go through Gate/Operator Service scenarios.
- No new scheduling layer; DPI jobs are just **annotated Gate runs**.

---

## 3. Operator UI — Domain Plug-ins Tab

### 3.1 New top-level tab

Add a 7th main tab to the existing Gate operator surface:

> `Dashboard | Scenario & Config | Pillars | Governance & Budgets | History & Exports | Logs & Console | Domain Plug-ins`

The tab is feature-flagged and considered Phase 8.

### 3.2 Layout Pattern

The **Domain Plug-ins** tab reuses established UI patterns:

- **Left column**: DPI list.
  - Each row/card:
    - `name` (e.g. Quantum DPI)
    - `type` (Quantum / Thermo / Social / etc.)
    - `status` (Idle / Active / Fault / Disabled)
    - `tags` (e.g. `ingestion`, `simulation`, `emulation`)
- **Right column**: DPI detail view.
  - Header with name + status + short description.
  - Sub-tabs (or segmented controls) specific to that DPI.

### 3.3 DPI List Behaviours

- Click a DPI row → load that DPI’s detail view and its sub-tabs.
- Selection has **no destructive side effects**; it’s purely read + control surface.
- Status is driven by Operator Service DPI metadata (see API section).

---

## 4. Quantum DPI v0.1 — UI Sub-tabs

For the **Quantum DPI**, define the following sub-tabs in the right-hand detail view:

1. **Overview** (optional but recommended)
   - High-level description (what the DPI does).
   - Quick metrics: number of jobs, last run status, last MDL gain.

2. **Ingestion**
   - Purpose: define and run jobs that ingest real or recorded quantum data into Aether.
   - UI elements:
     - **Source selector**:
       - Options (v0.1): `File upload`, `Manual JSON`, `Test fixture`.
       - Future options (vNext): `IBMQ`, `Other provider`.
     - **Schema hint** box:
       - Shows expected input schema (e.g. measurement counts, bitstrings, metadata fields).
     - **Jobs table**:
       - Columns: `Job ID`, `Source`, `Size/Shots`, `Status`, `Created at`, `Run link`.
   - Actions:
     - **Create ingestion job** button:
       - Opens side panel/modal.
       - Allows the user to select source, attach file or paste JSON, and submit.
       - On submit, UI calls `POST /dpis/{id}/jobs` with `kind=INGESTION`.

3. **Simulation**
   - Purpose: run classical simulations of quantum circuits using the Aether engine as the execution substrate.
   - UI elements:
     - **Circuit picker**:
       - Preset circuits (e.g. Bell pair, GHZ-4, QFT-4, random Clifford).
     - **Parameter form**:
       - Qubit count (bounded by engine profile).
       - Depth / number of layers.
       - Optional noise profile (none / simple / stub).
     - **Runs list**:
       - Last N simulation jobs with `job_id`, `run_id`, `status`, `qubits`, `depth`.
   - Actions:
     - **Run simulation** button:
       - Calls `POST /dpis/{id}/jobs` with `kind=SIMULATION` and circuit parameters.

4. **Emulation / Experiments**
   - Purpose: host domain-level experiments (e.g. Stage 2 H1 spin-chain law-finder).
   - UI elements:
     - **Experiment library** list:
       - `H1_spin_chain_law_finder` (core Stage 2 hero experiment).
       - Future experiments can be added similarly.
     - **Experiment detail** pane:
       - Description, parameters (qubits, ticks, episodes), and expected runtime hints.
     - **Experiment runs** table:
       - `job_id`, `run_id`, `status`, key metrics (e.g. MDL gain, motifs discovered).
   - Actions:
     - **Run experiment** button:
       - Calls `POST /dpis/{id}/jobs` with `kind=EXPERIMENT` and experiment config.
     - **View in History** link:
       - Jumps to `History & Exports` tab filtered to this `run_id`.

5. **Results**
   - Purpose: provide domain-aware summaries over DPI jobs, backed by normal history.
   - UI elements:
     - **Results list**:
       - All completed DPI jobs with headline metrics.
     - **Result detail**:
       - Summaries such as:
         - MDL baseline vs CE.
         - Number of CE motifs used.
         - Basic chart of MDL over ticks.
     - **Export buttons**:
       - Export summary report (e.g. JSON/CSV/Markdown snippet).
       - Link to full history export for the underlying run.

---

## 5. Operator Service — DPI Extensions

### 5.1 Entities

Introduce DPI-specific representations in the Operator Service domain model:

- `DpiSummary`
  - `id: string`
  - `name: string`
  - `type: string` (e.g. `quantum`, `thermo`, `social`)
  - `description: string`
  - `status: enum` (`IDLE`, `ACTIVE`, `FAULT`, `DISABLED`)
  - `tags: string[]` (e.g. `ingestion`, `simulation`, `emulation`)

- `DpiDetail`
  - Extends `DpiSummary` with:
  - `capabilities: { supports_ingestion: bool; supports_simulation: bool; supports_experiments: bool }`
  - `config_schema: object` (opaque schema hints for the UI, per capability)

- `DpiJob`
  - `job_id: string`
  - `dpi_id: string`
  - `kind: enum` (`INGESTION`, `SIMULATION`, `EXPERIMENT`)
  - `status: enum` (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`)
  - `created_at: timestamp`
  - `updated_at: timestamp`
  - `run_id?: string` (optional link to the underlying Gate run)
  - `request_payload: object` (opaque domain params)
  - `result_summary?: object` (small domain-specific summary)

### 5.2 DPI REST Endpoints (Phase 8)

- `GET /dpis`
  - Returns `DpiSummary[]`.
  - Used by UI to populate the left-hand DPI list.

- `GET /dpis/{dpi_id}`
  - Returns `DpiDetail`.
  - Used for the DPI header and to drive which sub-tabs are enabled.

- `GET /dpis/{dpi_id}/jobs`
  - Query params for pagination and optional `kind` filter.
  - Returns `DpiJob[]`.

- `POST /dpis/{dpi_id}/jobs`
  - Body includes:
    - `kind: "INGESTION" | "SIMULATION" | "EXPERIMENT"`
    - `params: object` (domain-specific configuration)
  - Behaviour:
    - Validates DPI capabilities.
    - Internally composes a **Scenario/RunConfig** for the engine using existing Operator Service flows.
    - Starts a **regular Gate run** and obtains `run_id`.
    - Creates a `DpiJob` record tagged with `dpi_id`, `kind`, `run_id`.
    - Returns the created `DpiJob`.

- `GET /dpis/{dpi_id}/jobs/{job_id}`
  - Returns a single `DpiJob` with current status and `result_summary` if available.

No new engine-side API is required: DPIs orchestrate standard scenarios and runs through the Operator Service.

---

## 6. Quantum DPI v0.1 Behaviour (Backend)

### 6.1 Ingestion Jobs

- `kind = INGESTION`
- v0.1 sources:
  - `file_upload`: user-provided JSON/CSV with counts or statevectors.
  - `manual_json`: payload pasted into the UI.
  - `fixture`: built-in example payloads for testing.
- Behaviour:
  - Validate payload shape and schema.
  - Use Trinity Gate + PFNA/TBP to integerize and inject data as initial states or input streams into the engine.
  - Run a short Gate scenario (e.g. single tick or small number of ticks) to record into Loom.
  - Generate a `result_summary` including basic stats (number of samples, qubits, any fidelity metrics computed).

### 6.2 Simulation Jobs

- `kind = SIMULATION`
- Parameters:
  - `circuit_id` (preset ID like `bell_pair`, `ghz_4`, `qft_4`).
  - `qubits` (bounded by profile).
  - `depth` or `layers`.
- Behaviour:
  - Construct a scenario that:
    - Builds an initial state for the selected circuit.
    - Applies gate layers via UMX update rules.
    - Logs the trajectory via Loom.
  - Optionally, compute TBP fidelity metrics if both original and reconstructed states are available in the pipeline.
  - Summarise key stats (qubits, depth, run length, MDL baseline) into `result_summary`.

### 6.3 Experiment Jobs (H1 Spin Chain Law-Finder)

- `kind = EXPERIMENT`
- v0.1 implements **H1_spin_chain_law_finder** from the Stage 2 hero experiment spec:
  - Qubit count (default 8, configurable up to profile limit).
  - Number of ticks T.
  - Number of episodes (e.g. 100).
- Behaviour:
  - Compose a multi-episode scenario:
    - Generate different initial states per episode.
    - Apply the predefined spin-chain gate pattern each tick.
    - Log via Loom; allow CE to run and propose structural changes.
  - After completion, compute:
    - MDL baseline vs MDL with CE library engaged.
    - Number of CE motifs spawned and reused.
  - Attach a compact `result_summary` for the job and provide a link to full history.

---

## 7. History & Exports Integration

- All DPI jobs correspond to **standard Gate runs** with `run_id`.
- History tab remains the canonical place to:
  - Inspect logs, Loom streams, metrics.
  - Export full run bundles.
- DPI layer adds:
  - A filter/tag in history views for `dpi_id`.
  - Quick-links from DPI Results to the relevant history entries.

Acceptance criteria:
- Every Quantum DPI job appears in History with clear `dpi_id` and `kind` metadata.
- From History, user can trace back to the originating DPI job.

---

## 8. Phase 8 Acceptance Criteria (High-Level)

1. **DPI framework available**
   - `Domain Plug-ins` tab visible when Phase 8 feature flag is enabled.
   - `GET /dpis` returns at least the Quantum DPI in `ACTIVE` or `IDLE` state.

2. **Quantum DPI v0.1 wired**
   - Ingestion, Simulation, and Experiment sub-tabs render and can create jobs.
   - Each job creates a corresponding Gate run and job record.

3. **History integration**
   - DPI-tagged runs visible in History with stable `run_id` and `dpi_id`.
   - "View in History" from DPI UI navigates correctly.

4. **Non-breaking**
   - Phase 7 flows (tabs, Operator Service endpoints) behave exactly as before when the DPI feature flag is off.

5. **Basic observability**
   - DPI jobs logged in Operator Service logs.
   - Minimal metrics exposed (job counts per DPI, failure rates).

This mini-spec is intended as the basis for a Phase 8 issue pack and further detailed design where needed.

