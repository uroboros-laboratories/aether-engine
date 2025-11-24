# SPEC-002 — GF-01 CMP-0 Baseline Build Plan

## Status

- **Spec ID:** SPEC-002
- **Name:** GF-01 CMP-0 Baseline Engine (Paper Parity)
- **Version:** v1
- **Scope:** UMX + Loom + Press/APX + NAP + Tick Loop + minimal Gate/TBP
- **Goal:** Digital engine matches the GF-01 V0 paper implementation exactly, under profile **CMP-0**

---

## 1. Purpose & Context

This spec defines the **first working digital implementation** of the Aether engine:

- Universal Matrix (UMX) integer engine,
- Aevum Loom (time chain and blocks),
- Astral Press / APX (compression + manifest),
- NAP (Normalised Aether Payload envelopes),
- Minimal Gate/TBP integration and tick loop.

The target is **strict paper parity** with the **GF-01 V0** example under **CMP-0**:

- Same tick-by-tick state evolution,
- Same edge fluxes,
- Same Loom chain values,
- Same APX bit counts and `manifest_check`,
- Same NAP envelopes.

This is *not* the final, general system. It’s the **golden baseline** for:

- Deterministic behaviour,
- Integer-only math,
- Correct cross-pillar handoffs.

All future profiles and features must preserve this baseline via tests.

---

## 2. Reference Documents

Place these under `docs/contracts/` and `docs/specs/`:

### Contracts (v1)

- `GF01_V0_Exam.md`
- `UMXTickLedger_v1.md`
- `LoomBlocks_v1.md`
- `APXManifest_v1.md`
- `NAPEnvelope_v1.md`
- `TopologyProfile_v1.md`
- `Profile_CMP0_v1.md`
- `TickLoop_v1.md`
- `SceneFrame_v1.md`
- `ULedgerEntry_v1.md`
- `CodexContracts_v1.md` (for later phases; Codex is observer-only at this stage)

### Pillar / System Specs

- Trinity Gate / TBP master spec  
- Astral Press master spec  
- Aevum Loom pillar master spec  
- Universal Matrix pillar master spec  
- Codex Eterna master spec  
- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (full build plan)

GF-01 PDFs (topology card, tick tables, APX prefilled sheets, envelopes) live in `docs/fixtures/gf01/`.

---

## 3. Repo Layout (target)

When created, the repo should roughly follow:

```text
aether-engine/
  docs/
    specs/
      spec_001_aether_full_system_build_plan_medium_agnostic.md
      spec_002_GF01_CMP0_Baseline_Build_Plan.md
      ...pillar master specs...
    contracts/
      GF01_V0_Exam.md
      UMXTickLedger_v1.md
      LoomBlocks_v1.md
      APXManifest_v1.md
      NAPEnvelope_v1.md
      TopologyProfile_v1.md
      Profile_CMP0_v1.md
      TickLoop_v1.md
      SceneFrame_v1.md
      ULedgerEntry_v1.md
      CodexContracts_v1.md
    fixtures/
      gf01/
        GF01_Ticks_1_8_Worked_Examples.pdf
        GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf
        GF01_Ticks_1_8_APX_Press_Prefilled.pdf
        GF01_Ticks_1_2_Worked_Examples.pdf
        GF01_Ticks_1_2_APX_Press_Prefilled.pdf
        ...csv/json mirrors...
  src/
    core/
    gate/
    umx/
    loom/
    press/
    codex/
    uledger/
  tests/
    gf01/
    integration/
```

The rest of this spec defines the **Phase 1** work: the GF-01 baseline.

---

## 4. Epic: GF-01 CMP-0 Baseline Engine (Paper Parity)

### 4.1 Epic Goal

Implement the minimal Aether engine that passes the **GF-01 V0 exam** defined in `GF01_V0_Exam.md`:

* Integer-only CMP-0 profile,
* Fixed GF-01 topology,
* Ticks 1–8,
* Exact match with paper tables and check values.

### 4.2 Success Criteria (summary)

An implementation passes SPEC-002 if:

1. **UMX parity**
   For ticks 1–8, `UMXTickLedger_v1` records match the paper GF-01 tables exactly:

   * `pre_u`, `post_u`,
   * `du`, `raw`, `f_e` per edge,
   * `sum_pre_u`, `sum_post_u`, `z_check`.

2. **Loom parity**
   For ticks 1–8, Loom produces:

   * `C_1..C_8` equal to GF-01 chain values,
   * An I-block at `t = 8` with correct `C_8`, `post_u`, and topology snapshot.

3. **Press/APX parity**
   For the 8-tick window and 2-tick window:

   * Streams, scheme choices, bit counts, and `manifest_check` equal GF-01:

     * Window 1–8: `manifest_check = 487809945`
     * Window 1–2: `manifest_check = 869911338`

4. **NAP parity**
   For ticks 1–8, `NAPEnvelope_v1` records are identical to the GF-01 envelopes:

   * Correct `gid`, `layer`, `mode`,
   * `payload_ref = 487809945`,
   * `prev_chain = C_{t-1}`.

5. **Determinism**
   Two runs with identical config produce **bitwise identical** outputs:

   * UMX ledgers,
   * Loom blocks,
   * APX manifests,
   * NAP envelopes.

The formal, detailed criteria are in `GF01_V0_Exam.md`.

---

## 5. Issues / Work Items

### Issue 1 — CMP-0 Topology & Profile Implementation

**Title:** Implement CMP-0 topology & profile (GF-01)  
**Goal:** Represent GF-01 topology and CMP-0 numeric profile as code objects matching the contracts.

**Depends on:**

* `TopologyProfile_v1.md`
* `Profile_CMP0_v1.md`

**Tasks:**

* [ ] Implement `TopologyProfile_v1` type as specified.
* [ ] Implement `NodeProfile_v1` and `EdgeProfile_v1` types.
* [ ] Implement `Profile_CMP0_v1` type with:

  * `name = "CMP-0"`
  * `modulus_M = 1_000_000_007`
  * `C0 = 1234567`
  * `SC = 32`
  * `I_block_spacing_W = 8`
  * Embedded `flux_rule`, `chain_rule`, `s_t_rule`, `nap_defaults`.
* [ ] Provide a concrete GF-01 instance:

  * [ ] `gid = "GF01"`, `N = 6`, edges 1..8 with correct `(i, j, k, cap, SC, c)`.
  * [ ] All values are integers; no floats.

**Acceptance Criteria:**

* [ ] Unit test can construct/load the GF-01 topology and profile deterministically.
* [ ] Topology and profile values match GF-01 documents.

---

### Issue 2 — UMX CMP-0 Engine and UMXTickLedger_v1

**Title:** Implement UMX CMP-0 engine and UMXTickLedger_v1  
**Goal:** Implement the integer flux engine that produces `UMXTickLedger_v1` records, matching GF-01.

**Depends on:**

* `UMXTickLedger_v1.md`
* `TopologyProfile_v1.md`
* `Profile_CMP0_v1.md`

**Tasks:**

* [ ] Implement `UMXTickLedger_v1` and `EdgeFlux_v1` types.
* [ ] Implement CMP-0 flux rule:

  * [ ] `du = pre_u[i] - pre_u[j]`
  * [ ] `raw = floor(k * abs(du) / SC)`
  * [ ] `f_e = sign(du) * min(raw, cap, abs(du))`
  * [ ] Conservation: `sum_pre_u == sum_post_u == z_check`.
* [ ] Implement `UMX.step(t, state, topo, profile) -> UMXTickLedger_v1`:

  * [ ] `pre_u` from input state,
  * [ ] `edges` populated in `e_id` order,
  * [ ] `post_u` computed from fluxes.
* [ ] GF-01 tests:

  * [ ] For initial `u(0) = [3,1,0,0,0,0]` and GF-01 topology/profile, ticks 1–8:

    * `pre_u`, `post_u`, `du`, `raw`, `f_e` match GF-01 tables.
    * `sum_pre_u == sum_post_u == z_check`.

**Acceptance Criteria:**

* [ ] All GF-01 UMX tests pass with exact equality.
* [ ] No floating-point arithmetic appears in UMX.

---

### Issue 3 — Loom CMP-0 Chain and Blocks

**Title:** Implement Loom CMP-0 chain and blocks  
**Goal:** Implement Loom chain, P-blocks, and I-block checkpoints per contracts, matching GF-01.

**Depends on:**

* `LoomBlocks_v1.md`
* `Profile_CMP0_v1.md`
* UMX engine (Issue 2)

**Tasks:**

* [ ] Implement `LoomPBlock_v1` and `LoomIBlock_v1`.
* [ ] Implement CMP-0 `s_t` computation:

  * [ ] For GF-01, `s_t = 9` for all ticks.
* [ ] Implement CMP-0 chain update:

  * [ ] `C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M`
* [ ] Implement Loom module:

  * [ ] Takes `UMXTickLedger_v1`, `C_prev`, `seq_t`, `profile`.
  * [ ] Outputs `LoomPBlock_v1` and updated `C_t`.
  * [ ] Every `W` ticks (GF-01: W=8), emit `LoomIBlock_v1` with topology snapshot.
* [ ] GF-01 tests:

  * [ ] `C_1..C_8` exactly `[20987847, 356793608, 65491504, 113355772, 927048329, 759821701, 916969047, 588473909]`.
  * [ ] I-block at t = 8:

    * `C_t = 588473909`,
    * `post_u` = UMX post_u at tick 8,
    * topology snapshot = GF-01 topology.

**Acceptance Criteria:**

* [ ] All Loom GF-01 tests pass with bitwise equality.
* [ ] Loom computation uses integer arithmetic only.

---

### Issue 4 — Press/APX CMP-0 (R-mode, APXManifest_v1 & manifest_check)

**Title:** Implement Press/APX CMP-0 (R-mode, manifest & manifest_check)  
**Goal:** Implement minimal Press/APX functionality to reproduce GF-01 APX manifests and `manifest_check` values.

**Depends on:**

* `APXManifest_v1.md`
* `Profile_CMP0_v1.md`
* Loom (Issue 3) / UMX (Issue 2) for stream inputs

**Tasks:**

* [ ] Implement `APXManifest_v1` and `APXStream_v1`.
* [ ] Implement minimal `"R"` scheme encoder sufficient for GF-01 examples.
* [ ] Implement Press module that:

  * [ ] Accepts window slices of:

    * `S1_post_u_deltas` (per-tick state deltas),
    * `S2_fluxes` (per-tick edge flux sequences).
  * [ ] Computes `L_model`, `L_residual`, `L_total` per stream.
  * [ ] Computes `manifest_check` from stream data and scheme choices.
* [ ] GF-01 tests:

  * [ ] Window ticks 1–8:

    * `apx_name = "GF01_APX_v0_full_window"`,
    * `profile = "CMP-0"`,
    * `L_total(S1) = 7`, `L_total(S2) = 8`,
    * `manifest_check = 487809945`.
  * [ ] Window ticks 1–2:

    * `apx_name = "GF01_APX_v0_ticks_1_2"`,
    * `manifest_check = 869911338`,
    * bit counts as per GF-01 APX sheet.

**Acceptance Criteria:**

* [ ] Both the 8-tick and 2-tick APX fixtures match exactly (bit counts + manifest_check).

---

### Issue 5 — NAPEnvelope_v1 and Minimal Gate/TBP Integration

**Title:** Implement NAPEnvelope_v1 and minimal Gate/TBP tick integration  
**Goal:** Implement `NAPEnvelope_v1` and a simple Gate/TBP that emits one envelope per tick based on Loom/Press outputs.

**Depends on:**

* `NAPEnvelope_v1.md`
* `SceneFrame_v1.md`
* `TickLoop_v1.md`
* Loom & Press modules

**Tasks:**

* [ ] Implement `NAPEnvelope_v1` type.
* [ ] Implement `SceneFrame_v1` type.
* [ ] Implement minimalist Gate module that, per tick:

  * [ ] Builds a `SceneFrame_v1` from:

    * `gid`, `run_id`, `tick`, `nid`,
    * `pre_u`, `post_u` from UMX,
    * `C_prev`, `C_t` from Loom,
    * window info and `manifest_check`.
  * [ ] Produces `NAPEnvelope_v1`:

    * `v = 1` (from `Profile_CMP0_v1.nap_defaults.v`),
    * `gid = "GF01"`,
    * `layer = "DATA"`, `mode = "P"`,
    * `payload_ref = manifest_check`,
    * `seq = tick`,
    * `prev_chain = C_prev`,
    * `sig = ""` (placeholder).
* [ ] GF-01 tests:

  * [ ] For ticks 1–8:

    * `payload_ref = 487809945`,
    * `prev_chain(1) = 1234567`,
    * `prev_chain(2..8)` equal `C_1..C_7`.

**Acceptance Criteria:**

* [ ] All NAP envelopes match the GF-01 envelope sheet exactly.

---

### Issue 6 — TickLoop_v1 End-to-End Wiring (run_gf01)

**Title:** Wire up TickLoop_v1 (end-to-end GF-01)  
**Goal:** Implement a single orchestrator that runs the GF-01 scenario and produces all artefacts.

**Depends on:**

* `TickLoop_v1.md`
* Issues 1–5

**Tasks:**

* [ ] Implement `run_gf01()` (or equivalent) that:

  * [ ] Constructs GF-01 `TopologyProfile_v1` and `Profile_CMP0_v1`.
  * [ ] Initialises:

    * `state = u(0) = [3,1,0,0,0,0]`,
    * `C_prev = C_0 = 1234567`,
    * Press window buffers.
  * [ ] For ticks `t = 1..8`:

    * [ ] Call UMX → get `UMXTickLedger_v1`.
    * [ ] Call Loom → get `LoomPBlock_v1`, updated `C_t`.
    * [ ] Update Press window; at t = 8, produce `APXManifest_v1`.
    * [ ] Build `SceneFrame_v1` and emit `NAPEnvelope_v1`.
  * [ ] Collect and return:

    * UMX tick ledgers,
    * Loom blocks (P-blocks + I-block at t = 8),
    * APX manifests (8-tick + 2-tick if implemented),
    * NAP envelopes.

* [ ] Implement an integration test:

  * [ ] Calls `run_gf01()`,
  * [ ] Validates all conditions in `GF01_V0_Exam.md`.

**Acceptance Criteria:**

* [ ] `run_gf01()` passes the GF-01 exam tests with no deviations.

---

### Issue 7 — Determinism Harness & Regression Snapshot

**Title:** Determinism harness & regression test scaffold  
**Goal:** Ensure the entire GF-01 pipeline is bitwise deterministic and future changes can’t silently break parity.

**Depends on:**

* `GF01_V0_Exam.md`
* All previous issues

**Tasks:**

* [ ] Implement canonical JSON serialisation for:

  * `UMXTickLedger_v1`,
  * `LoomPBlock_v1`, `LoomIBlock_v1`,
  * `APXManifest_v1`,
  * `NAPEnvelope_v1`.
* [ ] Implement a double-run test:

  * [ ] Run `run_gf01()` twice,
  * [ ] Serialise both output sets,
  * [ ] Assert equality byte-for-byte.
* [ ] Implement a snapshot test:

  * [ ] Persist a known-good JSON snapshot of GF-01 outputs,
  * [ ] Compare new runs against snapshot,
  * [ ] Fail test on any difference.

**Acceptance Criteria:**

* [ ] Double-run test passes (strict determinism).
* [ ] Snapshot test passes and acts as a guardrail for future changes.

---

## 6. Out-of-Scope for SPEC-002

The following are explicitly **out of scope** for this spec and will be addressed in later specs/epics:

* Dynamic topology (SLP growth/prune),
* Multiple graphs/engines in parallel,
* Full AEON/APXi grammars and advanced Press modes,
* Codex-driven structural changes (beyond logging proposals),
* Real external inputs via Gate/TBP (PFNA from hardware, etc.),
* Rich governance policies and budgets.

SPEC-002 is “just”: **prove the digital engine can exactly emulate the paper V0 GF-01 run under CMP-0.**

---

