# SPEC-006 — Phase 3 Governance, Config & Ops Implementation Plan

## Status

- **Spec ID:** SPEC-006
- **Name:** Phase 3 Governance, Config & Ops Implementation Plan
- **Version:** v1
- **Scope:** Configuration & profiles, CLI & run orchestration, logging & metrics, introspection, regression tooling & CI
- **Assumes:**
  - SPEC-002 (GF-01 CMP-0 Baseline Build Plan) is implemented and green.
  - SPEC-005 (Phase 2 Pillar V1 Implementation Plan) is implemented or in progress.
  - SPEC-004 (Dev Workflow & Codex Guide) is in force for all development.

---

## 1. Purpose & Context

SPEC-002 and SPEC-005 focus on **what the engine does**:

- SPEC-002: GF-01 CMP-0 baseline, strict paper parity.
- SPEC-005: Pillar V1 implementations (UMX, Loom, Press, Gate/TBP, U-ledger, Codex) for arbitrary configs.

SPEC-006 defines **how the engine is operated and governed**:

- How runs are configured and launched,
- How state, metrics, and logs are exposed,
- How regression and CI are enforced so the system doesn’t drift,
- How to keep everything reproducible and inspectable.

This is the “Governance / Config / Ops” layer that wraps the pillar implementations.

---

## 2. Reference Documents

- `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`
- `docs/specs/spec_004_Dev_Workflow_and_Codex_Guide.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- Pillar master specs (Gate/TBP, UMX, Loom, Press, Codex)

Contracts used:

- `TopologyProfile_v1.md`
- `Profile_CMP0_v1.md` (and future profile contracts)
- `TickLoop_v1.md`
- `SceneFrame_v1.md`
- `ULedgerEntry_v1.md`
- `NAPEnvelope_v1.md`
- `APXManifest_v1.md`
- `CodexContracts_v1.md`
- `UMXTickLedger_v1.md`
- `LoomBlocks_v1.md`

---

## 3. Phase Scope

Phase 3 delivers:

- **Config & Profiles:** File-based configuration for runs, topologies, profiles, and windows.
- **CLI / Runner:** A small command-line tool to start runs, inspect results, and manage fixtures.
- **Logging & Metrics:** Structured, deterministic logs and basic metrics for understanding runs.
- **Introspection:** Tools to inspect internal artefacts (UMX, Loom, Press, Codex, U-ledger).
- **Regression & CI:** Expanded test suites and tooling to keep GF-01 and other reference scenarios stable.

This phase does **not** change core pillar semantics — it exposes and governs them.

---

## 4. EPIC P3.1 — Configuration & Profiles

### 4.1 Epic Goal

Introduce a robust, file-based configuration system so that:

- Runs can be defined without code changes,
- Topologies and profiles can be declared in config files,
- Window and layer settings are configurable per scenario,
- GF-01 and other scenarios are reproducible from config alone.

### 4.2 Dependencies

- SPEC-005 UMX V1, Loom V1, Press V1, Gate/TBP V1.
- Contracts: `TopologyProfile_v1`, `Profile_CMP0_v1`, `TickLoop_v1`.

### 4.3 Issues / Work Items

#### Issue P3.1.1 — Config Schema Definition

**Goal:** Define config schemas for topologies, profiles, and runs.

**Tasks:**

- [ ] Define a `RunConfig` schema with at least:
  - `gid`, `run_id`,
  - references to:
    - a `TopologyProfile` file,
    - a `Profile` file (numeric profile like CMP-0),
  - `ticks` (number of ticks to run),
  - `window_config` (APX windows, NAP layer routing),
  - flags for enabling Codex, diagnostics, etc.
- [ ] Define a `TopologyConfig` format (optionally identical to `TopologyProfile_v1` JSON/YAML).
- [ ] Define a `ProfileConfig` format that maps onto `Profile_CMP0_v1` and future profiles.

**Acceptance Criteria:**

- [ ] Schemas are documented (e.g. under `docs/specs` or `docs/contracts`).
- [ ] Example configs are provided:
  - GF-01,
  - at least two additional toy scenarios.

---

#### Issue P3.1.2 — Config Loader & Validator

**Goal:** Implement config loading and validation.

**Tasks:**

- [ ] Implement loaders for:
  - `RunConfig`,
  - `TopologyConfig`,
  - `ProfileConfig`.
- [ ] Implement validation rules:
  - Required fields present,
  - References to files exist,
  - Topologies and profiles are internally consistent.
- [ ] Integrate with UMX/Loom/Press/Gate contexts:
  - Run contexts can be constructed solely from a `RunConfig`.

**Acceptance Criteria:**

- [ ] GF-01 run can be launched from a `RunConfig` without code changes.
- [ ] Invalid configs produce clear, deterministic errors.

---

#### Issue P3.1.3 — Scenario Registry

**Goal:** Keep a catalogue of known scenarios.

**Tasks:**

- [ ] Implement a simple scenario registry (e.g. `scenarios/` directory with named config files).
- [ ] Provide metadata per scenario:
  - Description,
  - Pillars involved,
  - Expected runtime characteristics.
- [ ] Tests:
  - Registry can be enumerated,
  - Each scenario config can be validated and loaded.

**Acceptance Criteria:**

- [ ] GF-01 is registered as a scenario, along with at least two additional scenarios.
- [ ] Tools can list and select scenarios by name.

---

#### Issue P3.1.4 — Profile Extensions (Beyond CMP-0)

**Goal:** Prepare for multiple numeric profiles beyond CMP-0.

**Tasks:**

- [ ] Extend profile handling to allow:
  - Multiple profile definitions (e.g. CMP-1, CMP-2),
  - Profiles described in separate config files.
- [ ] Ensure profile selection is driven by `RunConfig`.

**Acceptance Criteria:**

- [ ] Engine can load a profile other than CMP-0 (even if identical to CMP-0 for now).
- [ ] Tests verify correct profile selection and use.

---

## 5. EPIC P3.2 — Logging, Metrics & Introspection

### 5.1 Epic Goal

Provide visibility into Aether runs via:

- Structured logs,
- Basic metrics,
- Introspection APIs and CLI commands.

### 5.2 Dependencies

- SPEC-005 pillar V1 implementations,
- SPEC-004 dev workflow.

### 5.3 Issues / Work Items

#### Issue P3.2.1 — Structured Logging

**Goal:** Define and implement structured logging for runs.

**Tasks:**

- [ ] Define log event types, e.g.:
  - `run_started`, `run_finished`,
  - `tick_summary`,
  - `window_closed`,
  - `codex_event`,
  - `error`.
- [ ] Implement a logging API that:
  - Emits JSON or key-value logs,
  - Is deterministic in order and content,
  - Can be filtered by run, tick, or component.
- [ ] Tests:
  - Logs generated for GF-01 match a reference snapshot (allowing for timestamps if used in a deterministic way).

**Acceptance Criteria:**

- [ ] Logs are structured, machine-parsable, and reproducible for deterministic runs.

---

#### Issue P3.2.2 — Metrics Collection

**Goal:** Provide basic, high-level metrics for runs.

**Tasks:**

- [ ] Identify core metrics, e.g.:
  - Total ticks, windows, envelopes emitted,
  - MDL totals per window/stream,
  - U-ledger length, last hash,
  - Codex motif counts.
- [ ] Implement a metrics collector that:
  - Aggregates per-run metrics,
  - Can dump metrics at end-of-run or on demand.
- [ ] Tests:
  - GF-01 metrics match expected values.

**Acceptance Criteria:**

- [ ] Metrics are available in a simple structured format (JSON, etc.) for GF-01 and other scenarios.

---

#### Issue P3.2.3 — Introspection APIs

**Goal:** Implement APIs to inspect internal artefacts programmatically.

**Tasks:**

- [ ] Provide functions to:
  - Fetch UMX tick ledgers by tick,
  - Fetch Loom blocks by tick/window,
  - Fetch APX manifests by window,
  - Fetch NAP envelopes by tick/layer,
  - Fetch U-ledger entries by tick.
- [ ] Ensure:
  - Results are read-only,
  - Access patterns are deterministic.

**Acceptance Criteria:**

- [ ] Introspection APIs return artefacts identical to those produced during a run.
- [ ] Tests exercise these APIs on GF-01 and one additional scenario.

---

#### Issue P3.2.4 — Introspection CLI Commands

**Goal:** Expose introspection via CLI.

**Tasks:**

- [ ] Implement commands such as:
  - `aether inspect <run-id> --summary`
  - `aether inspect <run-id> --tick 5`
  - `aether inspect <run-id> --window 1`
  - `aether show-ledger <run-id>`
- [ ] Integrate with introspection APIs.

**Acceptance Criteria:**

- [ ] CLI commands can be used to inspect GF-01 run artefacts without needing to write code.

---

## 6. EPIC P3.3 — Regression Harness & CI

### 6.1 Epic Goal

Scale the regression harness beyond GF-01 and formalise CI expectations:

- Multiple reference scenarios,
- Snapshot management tooling,
- CI configuration.

### 6.2 Dependencies

- SPEC-002 and SPEC-005 tests,
- Introspection APIs (EPIC P3.2).

### 6.3 Issues / Work Items

#### Issue P3.3.1 — Multi-Scenario Regression Suite

**Goal:** Add more reference scenarios for regression.

**Tasks:**

- [ ] Design at least 2–3 additional scenarios (topology + profile + run config).
- [ ] For each scenario:
  - [ ] Generate a canonical output snapshot (JSON).
  - [ ] Add tests that compare new runs to the snapshot.
- [ ] Maintain GF-01 as the primary “golden” regression.

**Acceptance Criteria:**

- [ ] Regression suite includes GF-01 + multiple additional scenarios.
- [ ] All regression tests must pass for CI to succeed.

---

#### Issue P3.3.2 — Snapshot Management Tooling

**Goal:** Provide tools to manage regression snapshots.

**Tasks:**

- [ ] Implement commands or scripts to:
  - Generate snapshots for a given scenario,
  - Compare two snapshots,
  - Show diffs (e.g. via JSON diff).
- [ ] Ensure:
  - Any snapshot update is intentional and reviewable.

**Acceptance Criteria:**

- [ ] Snapshot tooling is used to update GF-01 and other snapshots when specs change.
- [ ] Snapshots are stored in a clear directory structure (e.g. `tests/fixtures/snapshots/`).

---

#### Issue P3.3.3 — CI Configuration

**Goal:** Codify CI requirements.

**Tasks:**

- [ ] Configure CI to:
  - Run all unit tests,
  - Run all integration tests,
  - Run all regression & determinism tests.
- [ ] Ensure:
  - CI fails on any test failure,
  - Flaky tests are identified and stabilised.

**Implementation notes (Phase 3):**

- GitHub Actions workflow: `.github/workflows/ci.yml`.
- Runner: `ubuntu-latest` with Python 3.11.
- Commands:
  - `python -m pip install --upgrade pip`
  - `python -m pip install pytest`
  - `PYTHONPATH=src python -m pytest` (covers unit + integration + snapshot regressions for GF-01, line, ring, AEON/APXi demos).
- Triggered on every push and pull request; fails on any test or regression difference.
- Contributor guidance: documented in `docs/ops/ci.md`.

**Acceptance Criteria:**

- [ ] CI reliably enforces that main branch is always green for GF-01 and other reference scenarios.
- [ ] CI configuration is documented (e.g. in `docs/specs` or a `CONTRIBUTING.md`).

---

## 7. Out-of-Scope for SPEC-006

The following are explicitly **out of scope** for SPEC-006 and will be handled by later specs (e.g. SPEC-007):

- Advanced Press/APX features (full AEON/APXi, complex MDL placement),
- Dynamic topology (SLP growth/prune) and Codex-driven structure changes,
- Rich PFNA and hardware/quantum integration in Gate/TBP,
- Multi-graph, multi-engine coordination beyond simple separate runs.

SPEC-006 is about making the Phase 2 engine **operable, inspectable, and governable** without changing its fundamental behaviour.
