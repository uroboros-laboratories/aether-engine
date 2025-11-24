# SPEC-005 — Phase 2 Issue Pack (Pillar V1 Generalisation)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

It maps **SPEC-005** (Phase 2 — Pillar V1 Generalisation) into concrete GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 2 — SPEC-005 Pillar V1 Generalisation`

**Suggested labels:**

- `spec:SPEC-005`
- `phase:P2`
- `component:umx`
- `component:loom`
- `component:press`
- `component:gate`
- `component:nap`
- `component:u-ledger`
- `component:codex`
- `component:slp`
- `type:feature`
- `type:tests`
- `priority:medium`
- `priority:high`

You don’t have to use all labels on each issue; suggestions are given per-issue.

---

## EPIC P2.1 — UMX V1 (General Integer Engine)

### Issue P2.1.1 — TopologyProfile Loader & Validator

**Title:**  
`[SPEC-005][P2] TopologyProfile loader & validator (multi-topology support)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement a loader and validator for `TopologyProfile_v1` so the engine can support **multiple topologies**, not just GF-01.

This is the foundation for running arbitrary small/medium graphs under CMP-0.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.1, Issue P2.1.1
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- GF-01 topology fixture(s) in `docs/fixtures/gf01/`

## Goals

- Load topology profiles from JSON/YAML (or chosen format).
- Validate topologies against the contract and basic invariants.
- Provide a clean path to define non-GF-01 graphs (line, ring, star, etc.).

## Tasks

- [ ] Implement a loader for `TopologyProfile_v1` from config/fixture files.
- [ ] Implement validation:
  - [ ] Node IDs must be contiguous `[1..N]`.
  - [ ] Edge IDs must be contiguous `[1..E]`.
  - [ ] `edges` must be sorted by `e_id`.
  - [ ] Edge endpoints `i`, `j` must lie in `[1..N]`.
  - [ ] All integer parameters (`k`, `cap`, `SC`, `c`) are valid integers.
- [ ] Provide example profiles:
  - [ ] Loader for the existing GF-01 profile (regression).
  - [ ] At least one simple line graph.
  - [ ] At least one ring or star graph.
- [ ] Add tests:
  - [ ] Valid profiles load and pass validation.
  - [ ] Invalid profiles fail with clear, deterministic errors.

## Acceptance Criteria

- [ ] `TopologyProfile_v1` instances can be loaded for GF-01 and at least two other named topologies.
- [ ] Validation catches malformed profiles and surfaces clear error messages.
- [ ] No GF-01-specific hacks in the loader.
```

---

### Issue P2.1.2 — UMXRunContext (Multi-Run Support)

**Title:**  
`[SPEC-005][P2] UMXRunContext for multi-run UMX V1 engine`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:umx`, `type:feature`, `priority:high`

```markdown
## Summary

Introduce a reusable `UMXRunContext` abstraction that can manage **one UMX run**:

- Topology + profile,
- Current state and tick,
- Stepping and multi-tick runs,

without relying on global state or GF-01-specific assumptions.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.1, Issue P2.1.2
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- `docs/contracts/UMXTickLedger_v1.md`

## Goals

- Allow multiple UMX runs in one process.
- Keep each run self-contained and deterministic.

## Tasks

- [ ] Define a `UMXRunContext` with:
  - [ ] `topo: TopologyProfile_v1`
  - [ ] `profile: Profile_CMP0_v1`
  - [ ] `state: int[N]` (current `u(t)`)
  - [ ] `tick: int`
  - [ ] Run metadata (`gid`, `run_id`, etc.)
- [ ] Implement:
  - [ ] `init_state(u0)` — set initial state.
  - [ ] `step()` — perform one CMP-0 tick, returning a `UMXTickLedger_v1`.
  - [ ] `run_until(t_max)` — run multiple ticks, returning a sequence of ledgers.
- [ ] Ensure:
  - [ ] No global state; multiple contexts can exist concurrently.
  - [ ] `step()` uses only `TopologyProfile_v1` + `Profile_CMP0_v1` + `state` (no hard-coded GF-01 logic).
- [ ] Refactor GF-01 tests (from SPEC-002) to use `UMXRunContext` instead of any earlier ad hoc wiring.

## Acceptance Criteria

- [ ] `UMXRunContext` can be used to reproduce GF-01 UMX behaviour with all SPEC-002 tests passing.
- [ ] `UMXRunContext` also runs at least one non-GF-01 topology deterministically (line/ring/star).
- [ ] No global mutable state is required to run UMX.
```

---

### Issue P2.1.3 — CMP-0 Generalised Tick Stepping

**Title:**  
`[SPEC-005][P2] Generalise CMP-0 UMX tick stepping across topologies`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:umx`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Refine `UMX.step` so CMP-0 stepping is **fully general**:

- Works for any topology loaded via `TopologyProfile_v1`,
- Preserves conservation and determinism across all tested graphs.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.1.3
- `docs/contracts/UMXTickLedger_v1.md`
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`

## Goals

- Ensure CMP-0 implementation makes no hidden assumptions about GF-01.
- Confirm conservation and determinism for multiple graph types.

## Tasks

- [ ] Refactor `UMX.step` (if needed) to:
  - [ ] Use only `topo.edges` (with `e_id` order) and `profile` parameters.
  - [ ] Avoid any hard-coded node/edge counts or GF-01-specific logic.
- [ ] Add tests for:
  - [ ] A small line graph scenario.
  - [ ] A small ring graph scenario.
  - [ ] A small star graph scenario.
- [ ] In each case:
  - [ ] Check conservation (`sum_pre_u == sum_post_u`) per tick.
  - [ ] Assert determinism via double-run comparison.

## Acceptance Criteria

- [ ] All new graph tests pass (conservation + determinism).
- [ ] All GF-01 tests still pass unchanged.
- [ ] No topology-specific hacks remain in CMP-0 stepping logic.
```

---

### Issue P2.1.4 — UMX Diagnostics & Invariants

**Title:**  
`[SPEC-005][P2] UMX diagnostics & invariant checks`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:umx`, `type:feature`, `type:tests`, `priority:low`

```markdown
## Summary

Add optional UMX diagnostics and invariant checks that:

- Verify conservation per tick,
- Track simple stats (min/max values),
- Flag unexpected conditions,

without changing core behaviour.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.1.4
- `docs/contracts/UMXTickLedger_v1.md`

## Goals

- Provide an optional “diagnostic mode” for UMX runs.
- Ensure diagnostics do not break determinism.

## Tasks

- [ ] Add a diagnostic flag/config for UMX runs.
- [ ] When enabled, diagnostics should:
  - [ ] Verify conservation (`sum_pre_u == sum_post_u`) per tick.
  - [ ] Track min/max node values.
  - [ ] Optionally flag overflow or disallowed negatives (if applicable).
- [ ] Ensure:
  - [ ] Diagnostics only affect logs/metadata, not core state evolution.
- [ ] Add tests:
  - [ ] Run with diagnostics on and off; compare core outputs (they must match).
  - [ ] Confirm that conservation violations (if injected in tests) are detected and surfaced.

## Acceptance Criteria

- [ ] UMX diagnostics can be toggled without affecting outputs.
- [ ] Violations/invariants are clearly reported when enabled.
```

---

## EPIC P2.2 — Loom V1 (Time Axis & Replay)

### Issue P2.2.1 — LoomRunContext

**Title:**  
`[SPEC-005][P2] LoomRunContext for time axis & blocks`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:loom`, `type:feature`, `priority:high`

```markdown
## Summary

Introduce a `LoomRunContext` to manage the **time axis** for a run:

- Tracks `C_t`,
- Produces P- and I-blocks,
- Connects tightly with `UMXRunContext`.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.2, Issue P2.2.1
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`

## Goals

- Encapsulate Loom behaviour in a reusable context.
- Keep GF-01 Loom behaviour working via this new context.

## Tasks

- [ ] Define `LoomRunContext` with:
  - [ ] Reference to `UMXRunContext` (or an abstract tick-ledger source).
  - [ ] Current chain value `C_t`.
  - [ ] Config:
    - [ ] `W` (I-block spacing),
    - [ ] `s_t` rule,
    - [ ] `seq_t` rule.
  - [ ] Storage for `LoomPBlock_v1` and `LoomIBlock_v1` sequences.
- [ ] Implement:
  - [ ] `ingest_tick(ledger: UMXTickLedger_v1)` → `LoomPBlock_v1` (+ optional `LoomIBlock_v1`).
  - [ ] `run_until(t_max)` to step UMX and Loom together, or to ingest from an external UMX source.
- [ ] Refactor GF-01 Loom code to use `LoomRunContext`.

## Acceptance Criteria

- [ ] GF-01 chain `C_1..C_8` and I-block at `t = 8` can be reproduced using `LoomRunContext`.
- [ ] LoomRunContext can also run on at least one non-GF-01 scenario.
```

---

### Issue P2.2.2 — Configurable I-Block Spacing & s_t Rule

**Title:**  
`[SPEC-005][P2] Configurable Loom I-block spacing & s_t rule`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:loom`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend Loom to support:

- Configurable I-block spacing `W`,
- Alternative simple `s_t` rules,

while keeping CMP-0 / GF-01 behaviour as the default.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.2.2
- `docs/contracts/Profile_CMP0_v1.md`
- `docs/contracts/LoomBlocks_v1.md`

## Goals

- Allow different checkpoint cadences for different scenarios.
- Try at least one alternative `s_t` rule beyond constant 9.

## Tasks

- [ ] Use `Profile_CMP0_v1.I_block_spacing_W` as CMP-0 default.
- [ ] Allow run configs to override `W` (e.g. smaller window for tests).
- [ ] Implement:
  - [ ] Constant `s_t = 9` for GF-01.
  - [ ] At least one simple derived `s_t` (e.g. from flux magnitudes).
- [ ] Tests:
  - [ ] GF-01 still uses `s_t = 9` and `W = 8`.
  - [ ] A toy scenario using a different `W` and alternate `s_t` yields deterministic chain values.

## Acceptance Criteria

- [ ] Loom’s behaviour is parameterised by profile/config (no hard-coded `W` or `s_t`).
- [ ] All Loom tests (GF-01 + new ones) remain deterministic and reproducible.
```

---

### Issue P2.2.3 — Replay API

**Title:**  
`[SPEC-005][P2] Loom replay API (get_chain_at, replay_state_at)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:loom`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement **replay** APIs for Aevum Loom so that:

- Chain values can be queried at arbitrary ticks,
- System state can be reconstructed at any tick via I-block + re-run.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.2.3
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/UMXTickLedger_v1.md`

## Goals

- Support `get_chain_at(t)` and `replay_state_at(t)` APIs.
- Ensure replayed state matches the original run exactly.

## Tasks

- [ ] Implement functions:
  - [ ] `get_chain_at(t) -> C_t`.
  - [ ] `get_pblock(t) -> LoomPBlock_v1`.
  - [ ] `get_iblock_for(t) -> LoomIBlock_v1`.
  - [ ] `replay_state_at(t)`:
    - [ ] Find nearest prior I-block.
    - [ ] Re-run UMX ticks from checkpoint to target `t`.
- [ ] Tests:
  - [ ] For GF-01: replay `state_t` for `t = 1..8` matches original `post_u`.
  - [ ] For at least one non-GF-01 scenario: direct run vs replay produce identical states.

## Acceptance Criteria

- [ ] Replay APIs return states that exactly match original run results.
- [ ] Replay is deterministic and uses the same UMX logic as the forward run.
```

---

## EPIC P2.3 — Press/APX V1 (Stream Registry & Modes)

### Issue P2.3.1 — Stream Registry & Window Context

**Title:**  
`[SPEC-005][P2] PressWindowContext & stream registry`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:press`, `type:feature`, `priority:high`

```markdown
## Summary

Create a `PressWindowContext` and stream registry so Press/APX can:

- Manage multiple named streams per window,
- Buffer data per tick,
- Produce `APXManifest_v1` at window close.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.3, Issue P2.3.1
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`

## Goals

- Generalise Press beyond GF-01’s two hard-coded streams.
- Provide a clean API for registering and appending streams.

## Tasks

- [ ] Define `PressWindowContext` keyed by `(gid, window_id)` that:
  - [ ] Holds multiple named streams.
  - [ ] Buffers data per tick.
- [ ] Implement API:
  - [ ] `register_stream(name, scheme_hint)`.
  - [ ] `append(name, value_or_tuple)` per tick.
  - [ ] `close_window()` to:
    - [ ] Compute `APXManifest_v1`.
    - [ ] Clear/roll buffers as needed.
- [ ] Adapt GF-01 logic to use `PressWindowContext`.

## Acceptance Criteria

- [ ] GF-01 windows (ticks 1–8, 1–2) can be expressed via `PressWindowContext` and still reproduce existing manifests.
- [ ] New scenarios can declare additional streams without code changes in the core.
```

---

### Issue P2.3.2 — ID, R, and Basic GR Schemes

**Title:**  
`[SPEC-005][P2] Implement ID, R, and basic GR schemes in Press/APX`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:press`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend Press/APX to support three schemes:

- ID (identity),
- R (run-length-like),
- GR (grouped R, basic version),

with deterministic MDL accounting.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.3.2
- `docs/contracts/APXManifest_v1.md`

## Goals

- Represent and apply three core schemes for integer sequences.
- Provide consistent `L_model`, `L_residual`, `L_total` accounting per scheme.

## Tasks

- [ ] Implement scheme handlers:
  - [ ] ID scheme for raw/identity encoding.
  - [ ] R scheme as currently used for GF-01.
  - [ ] Basic GR scheme (grouped R), even if simple.
- [ ] Each scheme must:
  - [ ] Accept integer sequences.
  - [ ] Return `L_model`, `L_residual`, `L_total`.
  - [ ] Be deterministic.
- [ ] Integrate with `PressWindowContext`:
  - [ ] On `close_window()`, apply scheme per stream using `scheme_hint` or profile defaults.
- [ ] Add tests:
  - [ ] Simple sequences (constant, sparse, etc.) per scheme.
  - [ ] GF-01 still matches its known `L_total` and `manifest_check`.

## Acceptance Criteria

- [ ] All three schemes behave deterministically and produce consistent MDL stats.
- [ ] GF-01 APX results remain unchanged for its streams.
```

---

### Issue P2.3.3 — Generalised APXManifest Generation

**Title:**  
`[SPEC-005][P2] Generalised APXManifest_v1 generation`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:press`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Generalise `APXManifest_v1` creation to support:

- Arbitrary numbers of streams,
- Mixed schemes,
- Deterministic `manifest_check`.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.3.3
- `docs/contracts/APXManifest_v1.md`

## Goals

- Make APX manifests independent of GF-01-specific assumptions.
- Still preserve exact GF-01 behaviour.

## Tasks

- [ ] Ensure manifests include:
  - [ ] Stream definitions (name, scheme, lengths).
  - [ ] `L_model`, `L_residual`, `L_total` per stream.
  - [ ] `manifest_check` derived from all relevant fields (as per contract).
- [ ] Tests:
  - [ ] Multi-stream windows (more than two streams).
  - [ ] Mixed schemes (ID on one stream, R on another, GR on a third).
  - [ ] GF-01 regressions remain green.

## Acceptance Criteria

- [ ] Manifests for non-GF-01 windows are generated and deterministic.
- [ ] GF-01 manifests match their original values exactly.
```

---

## EPIC P2.4 — Gate/TBP V1 (Scenes & Layers)

### Issue P2.4.1 — SceneFrame as Primary Integration Object

**Title:**  
`[SPEC-005][P2] SceneFrame_v1 as primary integration object`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:gate`, `component:nap`, `type:feature`, `priority:high`

```markdown
## Summary

Refactor the tick loop so that **SceneFrame_v1** becomes the core per-tick integration bundle, capturing:

- UMX state,
- Loom chain data,
- Press/APX manifest references,
- NAP envelope metadata.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.4, Issue P2.4.1
- `docs/contracts/SceneFrame_v1.md`
- `docs/contracts/TickLoop_v1.md`

## Goals

- Standardise per-tick data flow around `SceneFrame_v1`.
- Make Gate/TBP integration cleaner and easier to extend.

## Tasks

- [ ] Refactor tick loop to build a `SceneFrame_v1` for each tick:
  - [ ] Populate fields from UMX, Loom, Press, NAP as specified in the contract.
- [ ] Ensure `SceneFrame_v1` includes:
  - [ ] `gid`, `run_id`, `tick`, `nid`.
  - [ ] `pre_u`, `post_u`.
  - [ ] `C_prev`, `C_t`.
  - [ ] Window/manifest metadata (`window_id`, `manifest_check`, references).
- [ ] Adapt NAP envelope creation to use `SceneFrame_v1` as its source.
- [ ] Add tests:
  - [ ] GF-01: scene frames match expectations.
  - [ ] At least one non-GF-01 scenario: scene frames are built consistently.

## Acceptance Criteria

- [ ] Scene frames are the canonical integration object in the tick loop.
- [ ] NAP envelopes and other outputs are derived from scene frames, not ad hoc wiring.
```

---

### Issue P2.4.2 — NAP Layers & Modes

**Title:**  
`[SPEC-005][P2] NAP layers & modes (beyond DATA/P)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:gate`, `component:nap`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend NAP handling to support multiple layers and modes:

- Layers: INGRESS, DATA, CTRL, EGRESS.
- Modes: at least P (primary) + one secondary type.

GF-01 can remain `layer = DATA`, `mode = P`.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.4.2
- `docs/contracts/NAPEnvelope_v1.md`
- Trinity Gate/TBP pillar spec.

## Goals

- Add richer layering semantics for NAP envelopes.
- Preserve GF-01 behaviour as a simple special case.

## Tasks

- [ ] Define a minimal layering/mode scheme based on the pillar spec.
- [ ] Extend envelope creation so:
  - [ ] GF-01 remains DATA/P.
  - [ ] Other scenarios can declare CTRL envelopes (e.g. run start/end, governance messages).
- [ ] Add tests:
  - [ ] Scenario with CTRL envelopes (e.g. run start/end).
  - [ ] Layer/mode usage matches configuration.

## Acceptance Criteria

- [ ] NAP envelopes can carry multiple layer/mode types.
- [ ] GF-01 outputs remain unchanged.
```

---

### Issue P2.4.3 — PFNA Placeholder for External Inputs

**Title:**  
`[SPEC-005][P2] PFNA placeholder for deterministic external inputs`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:gate`, `type:feature`, `type:tests`, `priority:low`

```markdown
## Summary

Establish a deterministic PFNA-like placeholder for external inputs so that:

- External integer sequences can be brought into the engine via Gate,
- These inputs can affect initial state or parameters in a controlled way.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.4.3
- Trinity Gate/TBP pillar spec (PFNA sections).

## Goals

- Create a basic, deterministic path: external data → PFNA-ish structure → Gate → scene frame → UMX.

## Tasks

- [ ] Define a minimal PFNA placeholder schema (in contracts if needed).
- [ ] Implement parsing or loading of external integer sequences into PFNA placeholder structures.
- [ ] Wire Gate logic so PFNA inputs can:
  - [ ] Modify initial UMX state, or
  - [ ] Adjust parameters, according to config.
- [ ] Add tests:
  - [ ] A small scenario where PFNA-coded external input changes run behaviour in a deterministic way.

## Acceptance Criteria

- [ ] External inputs can be represented and used deterministically through Gate.
- [ ] Implementation is compatible with later full PFNA support in Phase 4 (SPEC-007).
```

---

## EPIC P2.5 — U-ledger V1

### Issue P2.5.1 — Canonical Serialisation & Hashing

**Title:**  
`[SPEC-005][P2] Canonical serialisation & hashing for U-ledger`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:u-ledger`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Define and implement:

- A canonical serialisation (JSON) for core records,
- A fixed hash algorithm (e.g. SHA-256),

to be used by the universal ledger (`ULedgerEntry_v1`).

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.5, Issue P2.5.1
- `docs/contracts/ULedgerEntry_v1.md`

## Goals

- Ensure the same record always yields the same bytes and hash.
- Provide utilities for hashing records across pillars.

## Tasks

- [ ] Decide canonical JSON rules:
  - [ ] Key order,
  - [ ] Whitespace, encoding, numeric formats.
- [ ] Select and implement hash algorithm (e.g. SHA-256).
- [ ] Implement utility:
  - [ ] `hash_record(record) -> hash_string`.
- [ ] Add tests:
  - [ ] Serialising the same record from different code paths yields identical bytes and hash.
  - [ ] Hashes change when records change (sanity checks).

## Acceptance Criteria

- [ ] Canonical serialisation and hashing are documented and stable.
- [ ] All future U-ledger work can rely on these utilities.
```

---

### Issue P2.5.2 — ULedgerEntry Construction

**Title:**  
`[SPEC-005][P2] Construct ULedgerEntry_v1 per tick/window`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:u-ledger`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement construction of `ULedgerEntry_v1` that ties together:

- UMX tick ledger,
- Loom block,
- APX manifest,
- NAP envelope,

plus the previous U-ledger hash, per tick or window.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.5.2
- `docs/contracts/ULedgerEntry_v1.md`
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/UMXTickLedger_v1.md`

## Goals

- Build a stable, reproducible ledger chain for each run.
- Detect any change in pillar outputs via hash chain breakage.

## Tasks

- [ ] For each tick (or window, as defined):
  - [ ] Compute hashes of:
    - [ ] UMX tick ledger,
    - [ ] Loom P-block,
    - [ ] NAP envelope,
    - [ ] APX manifest (for the relevant window).
  - [ ] Gather:
    - [ ] `C_t` (chain),
    - [ ] `manifest_check` (window).
  - [ ] Construct `ULedgerEntry_v1` with:
    - [ ] `gid`, `run_id`, `tick`, `window_id`.
    - [ ] `C_t`, `manifest_check`.
    - [ ] `umx_ledger_hash`, `loom_block_hash`, `nap_envelope_hash`, `apx_manifest_hash`.
    - [ ] `prev_entry_hash`.
- [ ] Add tests:
  - [ ] GF-01 run yields a stable U-ledger chain.
  - [ ] Re-running GF-01 produces identical entries.
  - [ ] Any change to pillar outputs causes a hash mismatch (as expected).

## Acceptance Criteria

- [ ] U-ledger entries form a consistent hash chain for GF-01 and other scenarios.
- [ ] Re-running a scenario yields bit-identical ledger outputs.
```

---

## EPIC P2.6 — Codex V1 (Observer-Only)

### Issue P2.6.1 — CodexContext & Data Ingest

**Title:**  
`[SPEC-005][P2] CodexContext & data ingest (observer mode)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:codex`, `type:feature`, `priority:high`

```markdown
## Summary

Create a `CodexContext` to ingest engine traces and hold:

- Codex library entries,
- Basic stats needed for motif identification.

Codex remains **observer-only** at this phase (no structural changes).

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — EPIC P2.6, Issue P2.6.1
- `docs/contracts/CodexContracts_v1.md`

## Goals

- Wire Codex into the pipeline as a consumer of UMX/Loom/Press/NAP artefacts.
- Prepare for motif detection in later issues.

## Tasks

- [ ] Define `CodexContext` with:
  - [ ] `library_id` / metadata.
  - [ ] Collection of `CodexLibraryEntry_v1`.
  - [ ] Any runtime counters.
- [ ] Implement ingest pipeline that can consume:
  - [ ] Sequences of `UMXTickLedger_v1`.
  - [ ] Loom P/I blocks.
  - [ ] APX manifests.
  - [ ] (Optionally) NAP envelopes.
- [ ] Add tests:
  - [ ] GF-01 run can be ingested without errors.

## Acceptance Criteria

- [ ] CodexContext exists and can ingest data from at least GF-01 plus one non-GF-01 scenario.
- [ ] No changes are made to engine behaviour; Codex is read-only.
```

---

### Issue P2.6.2 — Motif Identification (Simple Heuristics)

**Title:**  
`[SPEC-005][P2] Codex motif identification (simple heuristics)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:codex`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Implement a first-pass motif identification for Codex:

- Use simple heuristics (e.g. repeated flux patterns),
- Produce `CodexLibraryEntry_v1` with basic MDL and usage stats.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.6.2
- `docs/contracts/CodexContracts_v1.md`

## Goals

- Have Codex learn **at least one motif** from GF-01 or other scenarios in a deterministic way.

## Tasks

- [ ] Define at least one motif type (e.g. `edge_flux_pattern_v1`) as per Codex contracts.
- [ ] Implement heuristic motif detection that:
  - [ ] Scans flux/state sequences for repeated patterns.
  - [ ] Builds `CodexLibraryEntry_v1` records.
  - [ ] Populates `mdl_stats` and `usage_stats` with simple but consistent metrics.
- [ ] Add tests:
  - [ ] GF-01 run leads to at least one stable motif in the library.
  - [ ] Re-running yields identical motifs.

## Acceptance Criteria

- [ ] Motif learning is deterministic.
- [ ] Library entries are stable across runs for the same scenario.
```

---

### Issue P2.6.3 — Proposal Emission (Observer-Only)

**Title:**  
`[SPEC-005][P2] Codex proposal emission (observer-only)`

**Labels:**  
`spec:SPEC-005`, `phase:P2`, `component:codex`, `component:u-ledger`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Have Codex emit **proposals** based on learned motifs as `CodexProposal_v1` records, without applying them yet.

Optionally, integrate with U-ledger for traceability.

## Spec References

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` — Issue P2.6.3
- `docs/contracts/CodexContracts_v1.md`
- `docs/contracts/ULedgerEntry_v1.md`

## Goals

- Produce deterministic proposals given the same run.
- Keep Codex in observer-only mode (no structural changes yet).

## Tasks

- [ ] For each motif meeting a configured threshold (e.g. usage count):
  - [ ] Emit `CodexProposal_v1` of appropriate type (e.g. `PLACE`, `ADD`).
  - [ ] Set `status = "PENDING"` or `"REJECTED"` by default.
- [ ] Optionally:
  - [ ] Hash and reference Codex library/proposal snapshots from `ULedgerEntry_v1`.
- [ ] Add tests:
  - [ ] GF-01 run produces at least one proposal.
  - [ ] Re-running produces identical proposal sets.

## Acceptance Criteria

- [ ] Proposals are generated deterministically and observed via Codex logs / data.
- [ ] No engine behaviour is changed by proposals at this phase.
```

---

End of SPEC-005 Phase 2 Issue Pack.
