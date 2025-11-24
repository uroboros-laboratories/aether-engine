# SPEC-002 — Phase 1 Issue Pack (GF-01 CMP-0 Baseline)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

It maps **SPEC-002** (GF-01 CMP-0 Baseline Build Plan) into concrete GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 1 — SPEC-002 GF-01 CMP-0 Baseline`

**Suggested labels:**

- `spec:SPEC-002`
- `phase:P1`
- `component:umx`
- `component:loom`
- `component:press`
- `component:gate`
- `component:nap`
- `component:u-ledger`
- `type:feature`
- `type:tests`
- `priority:high`
- `priority:medium`

Use the per-issue suggestions below; you don’t have to apply every label to every issue.

---

## Issue 1 — CMP-0 Topology & Profile

**Title:**  
`[SPEC-002][P1] Implement CMP-0 topology & profile (GF-01)`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement the **GF-01 CMP-0 topology and numeric profile** as first-class code objects, matching the contracts and values from the docs.

This is the foundation for the rest of the Phase 1 work.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 1
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- GF-01 fixtures under `docs/fixtures/gf01/`

## Goals

- Represent the GF-01 graph structure and CMP-0 numeric parameters exactly.
- Provide a deterministic, reusable way to construct/load the GF-01 profile.

## Tasks

- [ ] Implement `TopologyProfile_v1` type as specified in the contract.
- [ ] Implement `NodeProfile_v1` and `EdgeProfile_v1` types.
- [ ] Implement `Profile_CMP0_v1` type with:
  - [ ] `name = "CMP-0"`
  - [ ] `modulus_M = 1_000_000_007`
  - [ ] `C0 = 1234567`
  - [ ] `SC = 32`
  - [ ] `I_block_spacing_W = 8`
  - [ ] Embedded `flux_rule`, `chain_rule`, `s_t_rule`, `nap_defaults` (even if as structured metadata / comments for now).
- [ ] Provide a concrete **GF-01** instance:
  - [ ] `gid = "GF01"`
  - [ ] `N = 6`
  - [ ] Edges 1..8 with correct `(i, j, k, cap, SC, c)` from the GF-01 tables.
  - [ ] All values are integers; no floats.
- [ ] Add unit tests that:
  - [ ] Construct/load the GF-01 topology and profile deterministically.
  - [ ] Assert that all topology and profile values match the GF-01 docs.

## Acceptance Criteria

- [ ] A `TopologyProfile_v1` + `Profile_CMP-0_v1` pair exists for GF-01.
- [ ] Tests verify the GF-01 profile against the docs; any mismatch fails.
- [ ] No floating-point arithmetic is introduced in the profile/topology logic.
```

---

## Issue 2 — UMX CMP-0 Engine & Tick Ledger

**Title:**  
`[SPEC-002][P1] Implement UMX CMP-0 engine and UMXTickLedger_v1`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement the **UMX integer flux engine** for CMP-0 that produces `UMXTickLedger_v1` records and matches the GF-01 paper tables tick-by-tick.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 2
- `docs/contracts/UMXTickLedger_v1.md`
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- GF-01 worked examples in `docs/fixtures/gf01/`

## Goals

- Implement CMP-0 flux rule in integer-only math.
- Produce `UMXTickLedger_v1` records for ticks 1–8 that match GF-01 exactly.

## Tasks

- [ ] Implement `UMXTickLedger_v1` type as per the contract.
- [ ] Implement `EdgeFlux_v1` type as per the contract.
- [ ] Implement CMP-0 flux rule:
  - [ ] `du = pre_u[i] - pre_u[j]`
  - [ ] `raw = floor(k * abs(du) / SC)`
  - [ ] `f_e = sign(du) * min(raw, cap, abs(du))`
  - [ ] Conservation: `sum_pre_u == sum_post_u == z_check`.
- [ ] Implement `UMX.step(t, state, topo, profile) -> UMXTickLedger_v1`:
  - [ ] `pre_u` from input state.
  - [ ] Edges processed in `e_id` order from `TopologyProfile_v1`.
  - [ ] `post_u` computed by applying all `f_e`.
- [ ] Add GF-01 tests:
  - [ ] Use `u(0) = [3,1,0,0,0,0]` with GF-01 topology/profile.
  - [ ] For ticks `t = 1..8`, assert:
    - [ ] `pre_u`, `post_u` per tick match the GF-01 tables.
    - [ ] `du`, `raw`, `f_e` per edge match the GF-01 tables.
    - [ ] `sum_pre_u == sum_post_u == z_check` each tick.

## Acceptance Criteria

- [ ] All GF-01 UMX tests pass with exact equality (no tolerance, integers only).
- [ ] No floating-point arithmetic is used in the UMX core.
- [ ] The UMX engine can be reused by later phases without GF-01-specific hacks.
```

---

## Issue 3 — Loom CMP-0 Chain & Blocks

**Title:**  
`[SPEC-002][P1] Implement Loom CMP-0 chain and blocks`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:loom`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement the **Aevum Loom** for CMP-0:

- Per-tick chain updates `C_t`,
- P-blocks (`LoomPBlock_v1`),
- I-block checkpoint (`LoomIBlock_v1`),

and match the GF-01 chain exactly.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 3
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- `docs/contracts/UMXTickLedger_v1.md`
- GF-01 chain values and docs in `docs/fixtures/gf01/`

## Goals

- Implement CMP-0 chain rule and block structures.
- Reproduce the GF-01 chain values `C_1..C_8` and the I-block at `t = 8`.

## Tasks

- [ ] Implement `LoomPBlock_v1` and `LoomIBlock_v1` types as per the contract.
- [ ] Implement CMP-0 `s_t` computation:
  - [ ] For GF-01, `s_t = 9` for all ticks.
- [ ] Implement CMP-0 chain update:
  - [ ] `C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M`
    - `M` from `Profile_CMP0_v1`.
- [ ] Implement Loom module:
  - [ ] Input: `UMXTickLedger_v1`, `C_prev`, `seq_t`, `profile`.
  - [ ] Output: `LoomPBlock_v1` + updated `C_t`.
  - [ ] Every `W` ticks (GF-01: `W = 8`), emit `LoomIBlock_v1` with topology snapshot.
- [ ] Add GF-01 tests:
  - [ ] `C_1..C_8` exactly `[20987847, 356793608, 65491504, 113355772, 927048329, 759821701, 916969047, 588473909]`.
  - [ ] At `t = 8`, I-block:
    - [ ] `C_t = 588473909`.
    - [ ] `post_u` equals UMX `post_u` at tick 8.
    - [ ] Topology snapshot equals GF-01 topology.

## Acceptance Criteria

- [ ] All Loom GF-01 tests pass with bitwise equality.
- [ ] Loom uses integer-only arithmetic.
- [ ] Implementation is compatible with later Loom V1 generalisation (SPEC-005).
```

---

## Issue 4 — Press/APX CMP-0 (R-mode & Manifest)

**Title:**  
`[SPEC-002][P1] Implement Press/APX CMP-0 (R-mode, APXManifest_v1 & manifest_check)`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:press`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement the minimal **Press/APX** functionality needed to:

- Compress the two GF-01 streams (post_u deltas and fluxes),
- Produce `APXManifest_v1` records,
- Reproduce the exact `L_total` per stream and `manifest_check` for:
  - Ticks 1–8 window,
  - Ticks 1–2 window.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 4
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/Profile_CMP0_v1.md`
- GF-01 APX prefilled sheets in `docs/fixtures/gf01/`

## Goals

- Implement R-mode encoding for the GF-01 streams.
- Match `L_total` and `manifest_check` for the specified windows exactly.

## Tasks

- [ ] Implement `APXManifest_v1` and `APXStream_v1` types per the contract.
- [ ] Implement minimal `"R"` scheme encoder sufficient to reproduce GF-01 examples.
- [ ] Implement a Press module that:
  - [ ] Takes window slices of GF-01 streams:
    - `S1_post_u_deltas` (per-tick state deltas),
    - `S2_fluxes` (per-tick edge flux sequences).
  - [ ] Computes `L_model`, `L_residual`, `L_total` per stream.
  - [ ] Computes `manifest_check` exactly as defined in the contract/spec.
- [ ] Add GF-01 tests:
  - [ ] Window ticks 1–8:
    - [ ] `apx_name = "GF01_APX_v0_full_window"`.
    - [ ] `profile = "CMP-0"`.
    - [ ] `L_total(S1) = 7`, `L_total(S2) = 8`.
    - [ ] `manifest_check = 487809945`.
  - [ ] Window ticks 1–2:
    - [ ] `apx_name = "GF01_APX_v0_ticks_1_2"`.
    - [ ] `manifest_check = 869911338`.
    - [ ] Bit counts match the GF-01 APX sheet.

## Acceptance Criteria

- [ ] Both 8-tick and 2-tick GF-01 APX manifests match the paper values exactly.
- [ ] No floating-point arithmetic in core Press/APX logic.
- [ ] Implementation is compatible with later Press V1 generalisation (SPEC-005).
```

---

## Issue 5 — NAPEnvelope & Minimal Gate/TBP Integration

**Title:**  
`[SPEC-002][P1] Implement NAPEnvelope_v1 and minimal Gate/TBP integration`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:gate`, `component:nap`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Implement `NAPEnvelope_v1` and a minimal Gate/TBP layer that:

- Builds `SceneFrame_v1` per tick,
- Emits one NAP envelope per tick for GF-01,
- Uses manifest and chain values from Loom/Press.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 5
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/SceneFrame_v1.md`
- `docs/contracts/TickLoop_v1.md`
- GF-01 envelope fixtures in `docs/fixtures/gf01/`

## Goals

- Build per-tick scene frames for GF-01.
- Emit NAP envelopes whose fields match the GF-01 envelopes exactly.

## Tasks

- [ ] Implement `NAPEnvelope_v1` type per the contract.
- [ ] Implement `SceneFrame_v1` type per the contract.
- [ ] Implement a minimal Gate module that, for each tick:
  - [ ] Builds a `SceneFrame_v1` from:
    - `gid`, `run_id`, `tick`, `nid`,
    - `pre_u`, `post_u` from UMX,
    - `C_prev`, `C_t` from Loom,
    - Window info and `manifest_check` from Press.
  - [ ] Produces `NAPEnvelope_v1`:
    - [ ] `v = 1` (from `Profile_CMP0_v1.nap_defaults.v`).
    - [ ] `gid = "GF01"`.
    - [ ] `layer = "DATA"`, `mode = "P"`.
    - [ ] `payload_ref = manifest_check`.
    - [ ] `seq = tick`.
    - [ ] `prev_chain = C_prev`.
    - [ ] `sig = ""` (placeholder for now).
- [ ] Add GF-01 tests:
  - [ ] For ticks 1–8:
    - [ ] `payload_ref = 487809945`.
    - [ ] `prev_chain(1) = 1234567`.
    - [ ] `prev_chain(2..8)` equals `C_1..C_7`.

## Acceptance Criteria

- [ ] All GF-01 NAP envelopes match the envelope sheet exactly.
- [ ] NAP/Gate logic is deterministic and ready for Gate/TBP V1 expansion (SPEC-005).
```

---

## Issue 6 — TickLoop Wiring (`run_gf01`)

**Title:**  
`[SPEC-002][P1] Wire up TickLoop_v1 (end-to-end GF-01 run_gf01)`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:umx`, `component:loom`, `component:press`, `component:gate`, `component:nap`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Wire together UMX, Loom, Press, Gate/NAP into a single **per-tick pipeline** as described in `TickLoop_v1.md`, and implement `run_gf01()` that:

- Runs ticks 1–8 for GF-01,
- Produces all required artefacts,
- Passes the GF-01 exam.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 6
- `docs/contracts/TickLoop_v1.md`
- All Phase 1 pillar contracts (UMX, Loom, Press, NAP)
- `GF01_V0_Exam.md`

## Goals

- Create a single function (or equivalent API) that:
  - Loads GF-01 topology/profile,
  - Runs ticks 1–8,
  - Returns all relevant artefacts in a structured way.

## Tasks

- [ ] Implement `run_gf01()` (or equivalent entrypoint) that:
  - [ ] Constructs GF-01 `TopologyProfile_v1` and `Profile_CMP0_v1`.
  - [ ] Initialises:
    - [ ] `state = u(0) = [3,1,0,0,0,0]`.
    - [ ] `C_prev = C_0 = 1234567`.
    - [ ] Press window buffers as needed.
  - [ ] For each tick `t = 1..8`:
    - [ ] Call UMX → get `UMXTickLedger_v1`.
    - [ ] Call Loom → get `LoomPBlock_v1`, updated `C_t`.
    - [ ] Update Press window; at t = 8, produce `APXManifest_v1`.
    - [ ] Build `SceneFrame_v1` and emit `NAPEnvelope_v1`.
  - [ ] Collect and return:
    - [ ] All `UMXTickLedger_v1` records.
    - [ ] All `LoomPBlock_v1` and the final `LoomIBlock_v1` at t = 8.
    - [ ] All APX manifests (1–8, and 1–2 if implemented).
    - [ ] All NAP envelopes for ticks 1–8.
- [ ] Add an integration test:
  - [ ] Calls `run_gf01()`.
  - [ ] Asserts all GF-01 exam conditions in `GF01_V0_Exam.md`.

## Acceptance Criteria

- [ ] `run_gf01()` passes the GF-01 exam tests with no deviations.
- [ ] The wiring matches `TickLoop_v1` and is suitable for generalisation in later phases.
```

---

## Issue 7 — Determinism Harness & Regression Snapshot

**Title:**  
`[SPEC-002][P1] Determinism harness and GF-01 regression snapshot`

**Suggested labels:**  
`spec:SPEC-002`, `phase:P1`, `component:umx`, `component:loom`, `component:press`, `component:gate`, `component:nap`, `component:u-ledger`, `type:tests`, `priority:high`

```markdown
## Summary

Implement a **determinism harness** and a **regression snapshot** for the GF-01 scenario:

- Ensure two runs with the same config produce bit-identical outputs.
- Persist a canonical snapshot for GF-01.
- Fail tests if behaviour drifts.

## Spec References

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md` — Issue 7
- `docs/contracts/UMXTickLedger_v1.md`
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/NAPEnvelope_v1.md`
- `GF01_V0_Exam.md`

## Goals

- Canonical JSON serialisation for core artefacts.
- Double-run determinism test.
- Snapshot-based regression test for GF-01.

## Tasks

- [ ] Implement canonical JSON serialisation for:
  - [ ] `UMXTickLedger_v1`.
  - [ ] `LoomPBlock_v1` and `LoomIBlock_v1`.
  - [ ] `APXManifest_v1`.
  - [ ] `NAPEnvelope_v1`.
- [ ] Implement a **double-run determinism** test:
  - [ ] Run `run_gf01()` twice.
  - [ ] Serialise both output sets.
  - [ ] Assert equality byte-for-byte.
- [ ] Implement a **snapshot regression** test:
  - [ ] Persist a known-good JSON snapshot for GF-01 outputs (e.g. under `tests/fixtures/snapshots/gf01/`).
  - [ ] On test run, compare new outputs to the snapshot.
  - [ ] Fail tests on any difference unless snapshot is intentionally updated.

## Acceptance Criteria

- [ ] Double-run determinism test passes (strict bitwise equality).
- [ ] Regression snapshot test passes for GF-01.
- [ ] Any future behavioural change in GF-01 must explicitly update the snapshot and be reviewed.
```
