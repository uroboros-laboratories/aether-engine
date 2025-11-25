# SPEC-006 — Phase 3 Governance, Config & Ops Issue Pack (v1)

This issue pack turns **SPEC-006 — Phase 3 Governance, Config & Ops Implementation Plan** into concrete
GitHub issues you can paste directly into your repo.

Suggested milestone name:

> `Phase 3 — SPEC-006 Governance, Config & Ops`

Suggested labels (create once in the repo):

- `spec:SPEC-006`
- `phase:P3`
- `component:config`
- `component:cli`
- `component:logging`
- `component:metrics`
- `component:introspection`
- `component:regression`
- `component:ci`
- `type:feature`
- `type:tests`
- `priority:high`
- `priority:medium`

You don’t need to use all labels on every issue; suggested labels for each issue are listed below.

---

## EPIC P3.1 — Configuration & Profiles

### Issue P3.1.1 — Config Schema Definition

**Title:**  
`[SPEC-006][P3] Define config schemas for runs, topologies, and profiles`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:config`, `type:feature`, `type:tests`, `priority:high`

**Body:**

```markdown
## Summary

Define file-based configuration schemas for **runs**, **topologies**, and **profiles** so Aether runs
can be launched and reproduced without touching code.

This implements **P3.1.1 — Config Schema Definition** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — EPIC P3.1
- Existing pillar contracts and Phase 2 specs (UMX, Loom, Press, Gate, U-ledger, Codex)

## Goals

- Define explicit config schemas for:
  - `RunConfig` (how to run the engine),
  - `TopologyConfig` / topology references,
  - `ProfileConfig` (numeric profile like CMP-0).
- Make these schemas the **single source of truth** for configuring runs, not ad hoc code.

## Tasks

- [ ] Define a `RunConfig` schema with at least:
  - [ ] `gid`, `run_id`.
  - [ ] References to:
    - [ ] A `TopologyProfile` file (e.g. JSON/YAML describing the graph).
    - [ ] A `Profile` file (numeric profile like CMP-0).
  - [ ] `ticks` (number of ticks to run).
  - [ ] `window_config` (APX windows, NAP layer routing).
  - [ ] Flags for enabling diagnostics, Codex, PFNA inputs, etc.
- [ ] Define schemas / types for:
  - [ ] `TopologyConfig` (or reuse `TopologyProfile_v1` fixtures consistently).
  - [ ] `ProfileConfig` (profile name/ID + parameters, e.g. CMP-0, CMP-1, etc.).
- [ ] Decide on canonical serialisation (JSON/YAML) and document it.
- [ ] Add schema docs under `docs/specs/` or `docs/contracts/` as appropriate.

## Acceptance Criteria

- [ ] Config schemas are defined in code and/or documented contracts.
- [ ] Example config files exist for:
  - [ ] GF-01 scenario.
  - [ ] At least two additional toy scenarios (e.g. line, ring).
- [ ] Later issues (loader, CLI) can rely on these schemas without modification.
```

---

### Issue P3.1.2 — Config Loader & Validator

**Title:**  
`[SPEC-006][P3] Implement config loader & validator (RunConfig, TopologyConfig, ProfileConfig)`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:config`, `type:feature`, `type:tests`, `priority:high`

**Body:**

```markdown
## Summary

Implement config loading and validation so that Aether runs can be launched purely from config files.

This implements **P3.1.2 — Config Loader & Validator** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.1.2
- Config schemas from P3.1.1
- Existing topology/profile loaders from Phase 2

## Goals

- Load `RunConfig`, `TopologyConfig`, and `ProfileConfig` from disk.
- Validate that configs are complete and self-consistent.
- Allow UMX/Loom/Press/Gate runs to be constructed **solely from a `RunConfig`**.

## Tasks

- [ ] Implement loaders for:
  - [ ] `RunConfig` (e.g. `load_run_config(path)`).
  - [ ] `TopologyConfig` / `TopologyProfile` (using or extending existing loaders).
  - [ ] `ProfileConfig` (numeric profiles like CMP-0, future profiles).
- [ ] Implement validation rules:
  - [ ] Required fields are present.
  - [ ] Referenced files (topology, profile, PFNA inputs, etc.) exist.
  - [ ] Topologies and profiles are internally consistent.
  - [ ] Window configuration is valid for Press/APX.
- [ ] Integrate with run contexts:
  - [ ] UMXRunContext, LoomRunContext, PressWindowContext, Gate/NAP, and Codex can be constructed from a `RunConfig`.
- [ ] Add unit tests for:
  - [ ] Successful loading/validation of valid configs (GF-01 + another scenario).
  - [ ] Clear, deterministic errors for invalid configs.

## Acceptance Criteria

- [ ] GF-01 run can be launched from a `RunConfig` **without code changes**.
- [ ] Invalid configs produce deterministic, human-readable error messages.
```

---

### Issue P3.1.3 — Scenario Registry

**Title:**  
`[SPEC-006][P3] Implement scenario registry for named runs`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:config`, `component:ops`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Implement a **scenario registry** that keeps a catalogue of known Aether scenarios, each defined by config.

This implements **P3.1.3 — Scenario Registry** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.1.3
- Config schemas and loader from P3.1.1 / P3.1.2

## Goals

- Provide a simple way to list and select named scenarios.
- Make GF-01 and at least two other scenarios first-class, named entries.

## Tasks

- [ ] Introduce a registry structure (e.g. `scenarios/` directory) containing named config files.
- [ ] Each scenario should include metadata:
  - [ ] Scenario name/ID.
  - [ ] Description.
  - [ ] Pillars involved.
  - [ ] Expected runtime characteristics (rough).
- [ ] Implement helpers/APIs to:
  - [ ] Enumerate available scenarios.
  - [ ] Load a scenario by name (returns `RunConfig` + references).
- [ ] Add tests:
  - [ ] Registry can be enumerated.
  - [ ] Each scenario config passes validation and can be loaded via the loader.
  - [ ] GF-01 and at least two additional scenarios (e.g. line, ring) are registered.

## Acceptance Criteria

- [ ] GF-01 is registered as a scenario along with **at least two** additional scenarios.
- [ ] Tools/CLI can list and select scenarios by name via this registry.
```

---

### Issue P3.1.4 — Profile Extensions (Beyond CMP-0)

**Title:**  
`[SPEC-006][P3] Prepare profile handling for multiple numeric profiles (beyond CMP-0)`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:config`, `component:umx`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Extend profile handling so the engine can support **multiple numeric profiles** (CMP-0, CMP-1, etc.),
even if non-CMP-0 profiles initially mirror CMP-0 behaviour.

This implements **P3.1.4 — Profile Extensions (Beyond CMP-0)** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.1.4
- Existing CMP-0 profile implementation from Phase 2

## Goals

- Allow profile definitions to be stored in separate config files.
- Allow `RunConfig` to select between multiple profiles by name/ID.
- Keep behaviour identical for CMP-0 while enabling future profiles.

## Tasks

- [ ] Extend profile handling so that:
  - [ ] Multiple profiles can be defined (e.g. CMP-0, CMP-1, CMP-2).
  - [ ] Profiles live in separate config files (per P3.1.1 / P3.1.2).
- [ ] Ensure profile selection is driven by `RunConfig` (not hard-coded in code).
- [ ] Provide at least one non-CMP-0 profile file, even if it shares CMP-0 parameters as a placeholder.
- [ ] Add tests:
  - [ ] Engine can load a profile other than CMP-0.
  - [ ] Correct profile is selected and used based on `RunConfig`.
  - [ ] GF-01 still uses CMP-0 by default.

## Acceptance Criteria

- [ ] Engine can load and use a profile other than CMP-0 (even as a clone for now).
- [ ] Tests verify correct profile selection and profile-driven behaviour.
```

---

## EPIC P3.2 — Logging, Metrics & Introspection

### Issue P3.2.1 — Structured Logging

**Title:**  
`[SPEC-006][P3] Implement structured logging for Aether runs`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:logging`, `component:ops`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Introduce structured logging for Aether runs so execution can be inspected and debugged systematically.

This implements **P3.2.1 — Structured Logging** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.2.1
- Phase 2 determinism and snapshot harness

## Goals

- Provide structured, machine-readable logs per run.
- Capture key events: run start/end, tick outcomes, window closures, errors.

## Tasks

- [ ] Introduce a logging module or adapter that:
  - [ ] Emits structured log entries (JSON or similar).
  - [ ] Includes run identifiers (gid, run_id) and timestamps.
  - [ ] Logs key lifecycle events (start/end, tick progress, window closures).
- [ ] Ensure logs do **not** affect core deterministic behaviour.
- [ ] Add configuration to control log verbosity and destination (stdout/file).
- [ ] Add tests:
  - [ ] Running GF-01 produces structured logs.
  - [ ] Two runs with the same config produce compatible log structures (content may differ by timestamp, but keys/shape are stable).

## Acceptance Criteria

- [ ] Structured logs exist for GF-01 and other scenarios.
- [ ] Logging can be turned on/off or adjusted via config.
```

---

### Issue P3.2.2 — Metrics Collection

**Title:**  
`[SPEC-006][P3] Implement basic metrics collection for Aether runs`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:metrics`, `component:ops`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Implement a simple metrics collection layer that tracks basic per-run metrics for Aether.

This implements **P3.2.2 — Metrics Collection** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.2.2
- U-ledger, Codex, and run contexts from Phase 2

## Goals

- Track basic metrics such as:
  - Number of ticks, windows, envelopes,
  - U-ledger length, last hash,
  - Codex motif counts (if Codex enabled).

## Tasks

- [ ] Implement a metrics collector that can:
  - [ ] Aggregate per-run metrics while the run executes.
  - [ ] Export metrics at the end of the run (JSON or similar).
  - [ ] Optionally expose metrics on demand (e.g. via an API).
- [ ] Decide minimal metric set for Phase 3 (keep it simple but useful).
- [ ] Add tests:
  - [ ] GF-01 metrics match expected values (ticks, windows, envelopes, ledger entries).
  - [ ] Additional scenarios produce consistent metrics.

## Acceptance Criteria

- [ ] Metrics are available in a simple structured format for GF-01 and other scenarios.
- [ ] Metrics collection does not alter core behaviour or determinism.
```

---

### Issue P3.2.3 — Introspection APIs

**Title:**  
`[SPEC-006][P3] Implement introspection APIs for internal artefacts`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:introspection`, `component:ops`, `type:feature`, `type:tests`, `priority:high`

**Body:**

```markdown
## Summary

Provide programmatic APIs to inspect internal Aether artefacts from code, without digging through raw files.

This implements **P3.2.3 — Introspection APIs** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.2.3
- Existing serialisation and GF-01 snapshot tooling

## Goals

- Allow callers to query:
  - UMX tick ledgers,
  - Loom P-/I-blocks,
  - APX manifests,
  - NAP envelopes,
  - U-ledger entries,
  - Codex motifs/proposals (if present).

## Tasks

- [ ] Implement introspection functions/APIs to:
  - [ ] Fetch UMX tick ledgers by tick.
  - [ ] Fetch Loom blocks by tick/window.
  - [ ] Fetch APX manifests by window.
  - [ ] Fetch NAP envelopes by tick and/or layer.
  - [ ] Fetch U-ledger entries by tick or index.
- [ ] Ensure these APIs are:
  - [ ] Read-only.
  - [ ] Deterministic and side-effect free.
- [ ] Add tests:
  - [ ] GF-01 runs can be introspected programmatically to recover known artefacts.
  - [ ] Non-GF-01 scenarios work with the same APIs.

## Acceptance Criteria

- [ ] Introspection APIs exist and are covered by tests.
- [ ] APIs are documented so future tooling (CLI, UI) can rely on them.
```

---

### Issue P3.2.4 — Introspection CLI Commands

**Title:**  
`[SPEC-006][P3] Add CLI commands for run introspection`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:cli`, `component:introspection`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Expose introspection capabilities through a simple CLI so runs can be inspected without writing code.

This implements **P3.2.4 — Introspection CLI Commands** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.2.4
- Introspection APIs from P3.2.3
- Any existing CLI/run launcher from earlier work

## Goals

- Provide user-friendly CLI commands for run inspection:
  - Summaries,
  - Per-tick views,
  - Per-window views,
  - Viewing the U-ledger.

## Tasks

- [ ] Implement CLI commands such as:
  - [ ] `aether inspect <run-id> --summary`
  - [ ] `aether inspect <run-id> --tick 5`
  - [ ] `aether inspect <run-id> --window 1`
  - [ ] `aether show-ledger <run-id>`
- [ ] Wire these commands to the introspection APIs from P3.2.3.
- [ ] Add tests (unit or integration) to cover at least:
  - [ ] Successful inspection of a GF-01 run.
  - [ ] Graceful handling of unknown/invalid run IDs.

## Acceptance Criteria

- [ ] CLI commands can inspect GF-01 run artefacts without writing code.
- [ ] CLI behaviour is documented (help text, README, or spec comments).
```

---

## EPIC P3.3 — Regression Harness & CI

### Issue P3.3.1 — Multi-Scenario Regression Suite

**Title:**  
`[SPEC-006][P3] Extend regression suite to multiple reference scenarios`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:regression`, `type:tests`, `priority:high`

**Body:**

```markdown
## Summary

Scale the regression harness beyond GF-01 to include **multiple reference scenarios**.

This implements **P3.3.1 — Multi-Scenario Regression Suite** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.3.1
- Existing GF-01 regression and snapshot tests from Phase 2

## Goals

- Treat more than one scenario as a first-class regression target.
- Run all reference scenarios in CI by default.

## Tasks

- [ ] Identify at least two additional reference scenarios besides GF-01 (e.g. line, ring).
- [ ] Add regression tests that:
  - [ ] Run each scenario from config (P3.1.x).
  - [ ] Assert determinism and basic invariants (conservation, chain stability, etc.).
- [ ] Ensure regression suite can be run via a single command (e.g. `pytest` or a specific test group).

## Acceptance Criteria

- [ ] Multiple scenarios are included in the regression suite.
- [ ] Running the regression suite validates GF-01 and the additional scenarios.
```

---

### Issue P3.3.2 — Snapshot Management Tooling

**Title:**  
`[SPEC-006][P3] Implement snapshot management tooling for regression data`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:regression`, `component:ops`, `type:feature`, `type:tests`, `priority:medium`

**Body:**

```markdown
## Summary

Introduce tools for managing regression snapshots (create, update, compare) across multiple scenarios.

This implements **P3.3.2 — Snapshot Management Tooling** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.3.2
- Existing GF-01 snapshot tooling

## Goals

- Make it easy to manage snapshots as the engine evolves.
- Avoid manual, error-prone snapshot updates.

## Tasks

- [ ] Implement snapshot tooling to:
  - [ ] Generate snapshots for a given scenario (GF-01 + others).
  - [ ] Compare current outputs to stored snapshots.
  - [ ] Flag differences clearly (for CI and local use).
- [ ] Define where snapshots live in the repo (e.g. `tests/fixtures/snapshots/`).
- [ ] Add tests or self-checks to validate snapshot tools themselves.

## Acceptance Criteria

- [ ] Snapshots can be regenerated and compared for GF-01 and other scenarios.
- [ ] Snapshot differences are clearly reported and easy to interpret.
```

---

### Issue P3.3.3 — CI Configuration

**Title:**  
`[SPEC-006][P3] Configure CI to enforce regression, determinism, and test suite`

**Suggested labels:**  
`spec:SPEC-006`, `phase:P3`, `component:ci`, `component:regression`, `type:feature`, `type:tests`, `priority:high`

**Body:**

```markdown
## Summary

Set up continuous integration so all tests and regression checks run automatically on pushes/PRs.

This implements **P3.3.3 — CI Configuration** from `spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`.

## Spec References

- `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` — P3.3.3
- Regression harness and snapshots from P3.3.1 / P3.3.2

## Goals

- Ensure that:
  - All unit, integration, and regression tests run in CI.
  - Main branch is always green for GF-01 and other reference scenarios.

## Tasks

- [ ] Add CI configuration (e.g. GitHub Actions workflow) to:
  - [ ] Install dependencies.
  - [ ] Run `python -m pytest` (or equivalent test command).
  - [ ] Run regression/snapshot checks.
- [ ] Ensure CI fails on:
  - [ ] Any failing test.
  - [ ] Any snapshot or determinism regression.
- [ ] Document CI expectations in:
  - [ ] `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md` (if needed), and/or
  - [ ] A `CONTRIBUTING.md` or similar.

## Acceptance Criteria

- [ ] CI reliably enforces that main branch is green for GF-01 and other reference scenarios.
- [ ] CI configuration is checked into the repo and documented for contributors.
```
