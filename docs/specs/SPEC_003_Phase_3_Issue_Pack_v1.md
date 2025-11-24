# SPEC-003 — Phase 3 Issue Pack (Gate/TBP + PFNA V0 / IO)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 3 — SPEC-003 Gate/TBP & PFNA V0 IO`

**Suggested labels:**

- `spec:SPEC-003`
- `phase:P3`
- `component:gate`
- `component:nap`
- `component:pfna`
- `component:umx`
- `component:loom`
- `component:press`
- `type:feature`
- `type:tests`
- `priority:medium`
- `priority:high`

You don’t have to use all labels on each issue; suggestions are given per-issue.

---

## Issue P3.1 — Session Lifecycle & TickLoop Integration

**Title:**  
`[SPEC-003][P3] Gate/TBP session lifecycle & TickLoop_v1 integration`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:gate`, `component:nap`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Define and implement the **Gate/TBP run/session lifecycle** and wire it cleanly into `TickLoop_v1`:

- Config → session initialisation,
- Start → tick loop orchestration,
- Stop/teardown,
- NAP signalling of lifecycle events.

This turns Gate/TBP into the canonical entrypoint for running Aether engine sessions in Phase 3.

## Spec References

- `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md` (this spec, when added)
- `docs/contracts/TickLoop_v1.md`
- `docs/contracts/SceneFrame_v1.md`
- `docs/contracts/NAPEnvelope_v1.md`

## Goals

- Gate/TBP owns the **session lifecycle**:
  - Load config and PFNA inputs (if any),
  - Initialise UMX/Loom/Press contexts,
  - Run the tick loop,
  - Emit NAP envelopes for lifecycle events.
- Make `TickLoop_v1` a clear, reusable contract callable by Gate.

## Tasks

- [ ] Define a `SessionConfig_v1` structure (or equivalent) that includes:
  - [ ] Topology/profile selection.
  - [ ] Press window/scheme settings.
  - [ ] PFNA input source(s) (if used).
  - [ ] Governance hooks placeholder (to be used in SPEC-007).
- [ ] Implement Gate/TBP entrypoint, e.g. `run_session(config: SessionConfig_v1)`:
  - [ ] Initialise:
    - [ ] UMXRunContext.
    - [ ] LoomRunContext.
    - [ ] PressWindowContext(s).
    - [ ] CodexContext (observer-only).
  - [ ] Emit NAP CTRL envelope for `SESSION_START`.
  - [ ] Run `TickLoop_v1` from `t = 1..T` (or until stop condition).
  - [ ] Emit NAP CTRL envelope for `SESSION_END`.
- [ ] Ensure `SceneFrame_v1` is constructed on every tick and passed to:
  - [ ] NAP envelope builder.
  - [ ] Codex (for ingest).
- [ ] Add tests:
  - [ ] Minimal GF-01-based session using this entrypoint.
  - [ ] A simple PFNA-driven session (see SPEC-003 PFNA issues).
  - [ ] Verify that lifecycle NAP CTRL envelopes appear in expected order.

## Acceptance Criteria

- [ ] Gate/TBP provides a stable `run_session`-style API over `TickLoop_v1`.
- [ ] Lifecycle is visible via NAP CTRL envelopes and replayable via logs/U-ledger.
- [ ] Existing GF-01 integration tests can be refactored to use this entrypoint without behaviour changes.
```

---

## Issue P3.2 — NAP Layers & Modes V1 (INGRESS/DATA/CTRL/EGRESS)

**Title:**  
`[SPEC-003][P3] NAP layers & modes V1 (INGRESS/DATA/CTRL/EGRESS)`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:nap`, `component:gate`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend `NAPEnvelope_v1` usage to support multiple layers and modes:

- Layers: INGRESS, DATA, CTRL, EGRESS,
- Modes: at least `P` (primary) + one secondary mode,

while keeping GF-01 behaviour (`layer = DATA`, `mode = P`) unchanged.

## Spec References

- Trinity Gate / TBP master spec (`trinity gate full spec.txt`)
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/SceneFrame_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (SceneFrame integration)
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`

## Goals

- Introduce layers and modes as **first-class, explicit fields** on NAP envelopes.
- Standardise how different envelope types are emitted in each layer.

## Tasks

- [ ] Update/confirm `NAPEnvelope_v1` fields for:
  - [ ] `layer` (enum: INGRESS, DATA, CTRL, EGRESS).
  - [ ] `mode` (enum including at least P + one secondary, e.g. S/AUX).
- [ ] Implement layer/mode mapping rules:
  - [ ] `DATA/P`: main data envelopes per tick (GF-01 compatible).
  - [ ] `CTRL/P`: lifecycle events (`SESSION_START`, `SESSION_END`), basic control messages.
  - [ ] `INGRESS/P`: PFNA ingress summary messages (see PFNA issues).
  - [ ] `EGRESS/P`: summary/export envelopes for external systems (V0 placeholder if needed).
- [ ] Ensure GF-01 NAP behaviour is preserved:
  - [ ] Default layer/mode remain DATA/P unless overridden by config.
- [ ] Add tests:
  - [ ] Scenario with lifecycle CTRL envelopes.
  - [ ] Scenario with INGRESS envelopes when PFNA is present.
  - [ ] Optional EGRESS test (even if placeholder) to validate plumbing.

## Acceptance Criteria

- [ ] NAP envelopes support multiple layers/modes without breaking GF-01.
- [ ] At least CTRL and INGRESS layers are exercised in tests.
- [ ] Layer/mode choices are deterministic and driven by config + event type.
```

---

## Issue P3.3 — PFNA V0 Schema & Loader

**Title:**  
`[SPEC-003][P3] PFNA V0 schema & deterministic loader`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:pfna`, `component:gate`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Define PFNA V0 as a **deterministic encoding for external integer inputs** and implement a loader that:

- Parses PFNA V0 files/configs,
- Validates them,
- Makes them available to Gate/TBP for use during runs.

## Spec References

- Trinity Gate/TBP master spec (PFNA sections)
- `docs/contracts/PFNA_V0_Schema_v1.md` (to be added)
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`

## Goals

- Provide a minimal but well-structured PFNA V0 format.
- Ensure PFNA ingest is deterministic and validated.

## Tasks

- [ ] Define PFNA V0 schema:
  - [ ] Represent integer sequences (e.g. time series or parameter sequences).
  - [ ] Identify target (graph/run, parameter names, etc.).
  - [ ] Include basic metadata (`gid`, `pfna_id`, version, etc.).
- [ ] Implement PFNA loader:
  - [ ] Accepts PFNA V0 JSON/YAML/other agreed format.
  - [ ] Validates schema and value ranges.
  - [ ] Produces an in-memory structure for Gate to consume.
- [ ] Add tests:
  - [ ] Valid PFNA files load successfully and reproducibly.
  - [ ] Invalid PFNA files (missing fields, bad types) fail with clear errors.
  - [ ] Round-trip tests: serialise → parse → serialise yields identical bytes (if applicable).

## Acceptance Criteria

- [ ] PFNA V0 schema and loader exist and are documented.
- [ ] PFNA inputs can be loaded deterministically for later mapping into runs.
```

---

## Issue P3.4 — PFNA → Engine Mapping (Initial State & Parameters)

**Title:**  
`[SPEC-003][P3] PFNA V0 → engine mapping (initial state & parameters)`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:pfna`, `component:gate`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Define and implement **how PFNA V0 inputs affect engine behaviour**, in a deterministic and configurable way:

- Initial UMX state,
- Profile/parameter tweaks,
- Optional run-level tags.

## Spec References

- Trinity Gate/TBP pillar spec (PFNA → engine mapping)
- `docs/contracts/PFNA_V0_Schema_v1.md`
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- `docs/contracts/UMXTickLedger_v1.md`
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`

## Goals

- Provide a minimal, clear set of mapping rules from PFNA fields to engine config/state.
- Ensure mapping is deterministic and reversible (at least conceptually).

## Tasks

- [ ] Define mapping rules for PFNA V0:
  - [ ] Mapping to initial UMX state `u(0)` for one or more graphs.
  - [ ] Optional mapping to profile parameters (within safe constraints).
  - [ ] Optional mapping to run/session tags (for logging/inspection).
- [ ] Implement Gate logic that:
  - [ ] Applies PFNA mappings during session initialisation.
  - [ ] Logs PFNA usage via NAP INGRESS and/or U-ledger (if available).
- [ ] Add tests:
  - [ ] Scenario: PFNA changes `u(0)` but nothing else; outputs differ deterministically from a non-PFNA run.
  - [ ] Scenario: PFNA includes invalid target (e.g. unknown graph ID) → clear deterministic error.
  - [ ] Double-run: same PFNA + config → identical outputs.

## Acceptance Criteria

- [ ] PFNA can be used to configure initial state and minor parameters in a deterministic way.
- [ ] Mapping is clearly documented and tested for at least one concrete example scenario.
```

---

## Issue P3.5 — NAP IO: INGRESS / CTRL / EGRESS Wiring

**Title:**  
`[SPEC-003][P3] NAP IO wiring for INGRESS, DATA, CTRL, EGRESS`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:nap`, `component:gate`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Implement the **NAP IO wiring** across layers for Phase 3:

- INGRESS (PFNA summaries),
- DATA (per-tick scene frames → envelopes),
- CTRL (session lifecycle and simple control events),
- EGRESS (summary/export envelopes).

## Spec References

- Trinity Gate/TBP pillar spec
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/SceneFrame_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`

## Goals

- Make NAP IO behaviour explicit and deterministic.
- Ensure each layer has clear sources and triggers.

## Tasks

- [ ] INGRESS:
  - [ ] Emit NAP INGRESS envelopes when PFNA inputs are loaded/applied.
  - [ ] Include references to PFNA IDs and key summary fields.
- [ ] DATA:
  - [ ] Continue emitting per-tick DATA/P envelopes from SceneFrame (as in SPEC-005).
  - [ ] Confirm no regressions vs GF-01 baseline.
- [ ] CTRL:
  - [ ] Emit CTRL/P envelopes for `SESSION_START`, `SESSION_END`, and any simple control events defined in SPEC-003.
- [ ] EGRESS (V0):
  - [ ] Emit basic EGRESS/P envelopes at session end summarising key outputs (e.g. manifest IDs, snapshot hashes).
- [ ] Add tests:
  - [ ] Verify envelopes appear in the expected order and layers.
  - [ ] Verify that with no PFNA, INGRESS remains silent and behaviour matches earlier phases.

## Acceptance Criteria

- [ ] All four NAP layers are wired up and test-covered for P3 features.
- [ ] GF-01 behaviour is preserved as a special case (DATA/P-only scenario).
```

---

## Issue P3.6 — Gate/TBP + Press Integration Config (Windowing & Streams)

**Title:**  
`[SPEC-003][P3] Gate/TBP + Press configuration for windows & streams`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:gate`, `component:press`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend Gate/TBP so that **windowing and stream configuration** for Press/APX is driven by Gate config and SceneFrames, not hard-coded logic.

## Spec References

- Astral Press/APX pillar master spec
- `docs/contracts/APXManifest_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`

## Goals

- Let Gate/TBP decide:
  - Which windows to run (tick ranges, AEON windows in P4),
  - Which streams are active per window,
  - Which schemes are used (within the limits of SPEC-005 and later SPEC-004).

## Tasks

- [ ] Extend `SessionConfig_v1` with Press configuration:
  - [ ] Window definitions for V0/V1 (tick-based).
  - [ ] Stream definitions (sources, names, scheme hints).
- [ ] Update Press integration so:
  - [ ] `PressWindowContext` instances are created based on Gate config.
  - [ ] SceneFrames provide the data slices per tick to appropriate streams.
  - [ ] Windows close and manifests are emitted as per config.
- [ ] Add tests:
  - [ ] Scenario matching GF-01 windows (1–8, 1–2) using config only.
  - [ ] Scenario with an additional toy window or stream (e.g. chain-derived stream).

## Acceptance Criteria

- [ ] Press windows and streams are fully controlled by Gate/TBP config for Phase 3 scenarios.
- [ ] GF-01 can be reproduced using the config-driven path (no hard-coded windowing in code).
```

---

## Issue P3.7 — End-to-End PFNA Scenario & Regression Snapshot

**Title:**  
`[SPEC-003][P3] End-to-end PFNA V0 scenario & regression snapshot`

**Labels:**  
`spec:SPEC-003`, `phase:P3`, `component:gate`, `component:pfna`, `component:umx`, `component:loom`, `component:press`, `component:nap`, `type:tests`, `priority:high`

```markdown
## Summary

Define and implement **one canonical PFNA V0 scenario** that exercises:

- PFNA ingest,
- PFNA→engine mapping,
- NAP INGRESS/DATA/CTRL/EGRESS,
- Press configuration via Gate,

and snapshot its outputs for regression.

## Spec References

- Trinity Gate/TBP pillar spec (example scenarios)
- `docs/contracts/PFNA_V0_Schema_v1.md`
- `docs/contracts/ULedgerEntry_v1.md` (if U-ledger is present by P3)
- All relevant pillar contracts (UMX, Loom, Press, NAP)

## Goals

- Provide a small, well-defined PFNA scenario that can be used as a “hello world” end-to-end test for Phase 3.
- Lock in deterministic outputs as a regression anchor.

## Tasks

- [ ] Design a PFNA V0 example:
  - [ ] Small graph (could reuse GF-01 or a variant).
  - [ ] Simple PFNA sequence that changes `u(0)` or a small parameter.
- [ ] Implement a test harness that:
  - [ ] Loads PFNA + config via Gate.
  - [ ] Runs a short session (e.g. 4–8 ticks).
  - [ ] Collects UMX, Loom, Press, NAP (and U-ledger if available).
- [ ] Snapshot outputs:
  - [ ] Store canonical JSON snapshots under `tests/fixtures/snapshots/pfna_v0_demo/`.
  - [ ] Add regression tests comparing new runs against the snapshot.
- [ ] Ensure scenario does not conflict with GF-01 regressions.

## Acceptance Criteria

- [ ] A named PFNA V0 demo scenario exists and is documented.
- [ ] Running the scenario twice yields identical outputs across all pillars.
- [ ] Snapshot-based regression tests pass and guard against accidental changes.
```

---

## Notes

- Once you stand up the repo, you can create a **GitHub Project** for `Phase 3 — SPEC-003` and drop these issues straight in.
- When SPEC-004 (AEON/APXi) and SPEC-006 (multi-graph/SLP) come online, Gate/TBP will gain additional issues that build on this foundation rather than replacing it.
