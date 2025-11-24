# SPEC-002 — Phase 1 Closeout Report  
## GF-01 CMP-0 Baseline (Paper Parity)

**Status:** COMPLETE  
**Phase:** 1 — SPEC-002 GF-01 CMP-0 Baseline  
**Repo:** `aether-engine` (docs-first, implementation in `src/`, tests in `tests/`)

This document records **how Phase 1 (SPEC-002)** was implemented in the repo, and where the work
for each SPEC-002 issue actually lives in the tree (code + tests + docs).

It is meant as a **phase close document** and a starting point for Phase 2 (SPEC-005).

---

## 1. Phase 1 Goal (SPEC-002 Recap)

**SPEC-002 Name:** GF-01 CMP-0 Baseline Engine (Paper Parity)  
**Core objective:**

> Implement the minimal Aether engine that passes the **GF-01 V0 exam** under **CMP-0**:
>
> - Integer-only math (no floats),
> - Fixed GF-01 topology,
> - Ticks 1–8,
> - Exact match with paper tables and check values.

**Key references in the repo:**

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`  
  – the narrative spec for Phase 1.
- `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`  
  – the full-system plan that nests Phase 1.
- `docs/specs/spec_000_AETHER_Spec_Index_and_Roadmap.md`  
  – overall map of specs and phases.
- `docs/specs/spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md`  
  – the issue pack that was used to create the 7 Phase 1 GitHub issues.
- `docs/specs/Aether_CMP0_Physics_Core_and_Invariants_v1.md`  
  – CMP-0 physics and invariants.
- `docs/specs/GF01_V0_Exam_v1.md` and `docs/contracts/GF01_V0_Exam.md`  
  – what it means to “pass the GF-01 exam”.
- `docs/fixtures/gf01/`  
  – the PDFs and binders for GF-01 tick tables, APX sheets, envelopes.

Phase 1 is considered **complete** when:

- All 7 SPEC-002 issues have a concrete implementation in `src/`,  
- Corresponding tests live under `tests/`,  
- The GF-01 exam passes, including determinism + snapshot tests.

---

## 2. Implementation Summary by Issue

This section walks issue-by-issue through SPEC-002 and shows:

- **What the spec asked for**, and  
- **Where in the repo that work lives** now.

Each subsection maps 1:1 to a SPEC-002 GitHub issue.

---

### 2.1 Issue 1 — CMP-0 Topology & Profile (GF-01)

**Spec / Issue:**

- SPEC-002 Issue 1 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- GitHub Issue: `[SPEC-002][P1] Implement CMP-0 topology & profile (GF-01)`
- Issue pack entry: `docs/specs/spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md` (Issue 1)

**What it required:**

- Define `TopologyProfile_v1`, `NodeProfile_v1`, `EdgeProfile_v1` as per contract.
- Define `Profile_CMP0_v1` with:
  - `name = "CMP-0"`
  - `modulus_M = 1_000_000_007`
  - `C0 = 1234567`
  - `SC = 32`
  - `I_block_spacing_W = 8`
- Provide a concrete **GF-01** instance:
  - `gid = "GF01"`, `N = 6`, edges 1..8 with correct `(i, j, k, cap, SC, c)` from the GF-01 tables.
- Unit tests that construct/load the GF-01 profile deterministically and verify values.

**Where it lives (code):**

- `src/umx/topology_profile.py`
  - Implements `TopologyProfileV1`, `NodeProfileV1`, `EdgeProfileV1`.
  - Provides helpers to build a GF-01 topology profile.
- `src/umx/profile_cmp0.py`
  - Implements `ProfileCMP0V1` mirroring `Profile_CMP0_v1` contract.
  - Provides `gf01_profile_cmp0()` with CMP-0 constants and GF-01 metadata.

**Where it lives (tests):**

- `tests/unit/test_topology_profile.py`
  - Reconstructs GF-01 topology and CMP-0 profile.
  - Asserts node/edge counts, edge list, and CMP-0 constants match the spec.

**Status:** Implemented and tested. GF-01 topology and CMP-0 profile are available as reusable objects for later issues.

---

### 2.2 Issue 2 — UMX CMP-0 Engine & UMXTickLedger_v1

**Spec / Issue:**

- SPEC-002 Issue 2 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- GitHub Issue: `[SPEC-002][P1] Implement UMX CMP-0 engine and UMXTickLedger_v1`
- Contracts:
  - `docs/contracts/UMXTickLedger_v1.md`
  - `docs/contracts/TopologyProfile_v1.md`
  - `docs/contracts/Profile_CMP0_v1.md`

**What it required:**

- Implement `UMXTickLedger_v1` + `EdgeFlux_v1` types.
- Implement CMP-0 flux rule (integer-only):

  - `du = pre_u[i] - pre_u[j]`  
  - `raw = floor(k * abs(du) / SC)`  
  - `f_e = sign(du) * min(raw, cap, abs(du))`  
  - Conservation: `sum_pre_u == sum_post_u == z_check`.

- Implement `UMX.step(t, state, topo, profile)` → `UMXTickLedger_v1` for GF-01.
- Tests: ticks 1–8 from `u(0) = [3,1,0,0,0,0]`, matching the GF-01 tables.

**Where it lives (code):**

- `src/umx/tick_ledger.py`
  - Defines the Python representation of `UMXTickLedgerV1` and `EdgeFluxV1`.
- `src/umx/engine.py`
  - Implements the CMP-0 flux logic and per-tick stepping:
    - Applies the flux rule edge-by-edge in `e_id` order.
    - Produces `pre_u`, edge fluxes, `post_u`, and aggregate checks.

**Where it lives (tests):**

- `tests/unit/test_umx_engine.py`
  - Checks:
    - CMP-0 flux rule behaviour at the unit level.
    - Conservation (`sum_pre_u == sum_post_u`).
- `tests/gf01/test_run_gf01.py`
  - Uses the UMX engine inside the full `run_gf01()` loop (see Issue 6).
  - Asserts that tick-by-tick UMX behaviour is consistent and matches GF-01 expectations at an integration level.

**Status:** Implemented and tested. UMX CMP-0 is integer-only and integrated into the GF-01 run.

---

### 2.3 Issue 3 — Loom CMP-0 Chain & Blocks

**Spec / Issue:**

- SPEC-002 Issue 3 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- Contracts:
  - `docs/contracts/LoomBlocks_v1.md`
  - `docs/contracts/Profile_CMP0_v1.md`

**What it required:**

- Implement `LoomPBlock_v1` and `LoomIBlock_v1` types.
- Implement CMP-0 `s_t` and chain update:

  - GF-01: `s_t = 9` for all ticks.  
  - `C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M`.

- Emit a P-block each tick with UMX tick + chain data.
- Every `W` ticks (GF-01: `W = 8`), emit an I-block with topology snapshot and state.
- Tests:
  - Chain values `C_1..C_8` match the GF-01 chain:
    - `[20987847, 356793608, 65491504, 113355772, 927048329, 759821701, 916969047, 588473909]`
  - I-block at `t = 8` has correct chain, state, and topology snapshot.

**Where it lives (code):**

- `src/loom/loom.py`
  - Implements P-block and I-block structures.
  - Implements `compute_s_t` (GF-01 uses constant 9).
  - Implements the CMP-0 chain update.
  - Provides a stepping API that consumes UMX tick ledgers and emits Loom blocks.

**Where it lives (tests):**

- `tests/unit/test_loom.py`
  - Verifies per-tick chain updates for GF-01.
  - Verifies that I-block at `t = 8` matches expected chain and snapshot.
- `tests/gf01/test_run_gf01.py`
  - Confirms that the chain values emitted during `run_gf01()` exactly match the GF-01 sequence.

**Status:** Implemented and tested. Loom reproduces GF-01 chain and I-block under CMP-0.

---

### 2.4 Issue 4 — Press/APX CMP-0 (R-mode & Manifest)

**Spec / Issue:**

- SPEC-002 Issue 4 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- Contracts:
  - `docs/contracts/APXManifest_v1.md`

**What it required:**

- Implement `APXManifest_v1` and `APXStream_v1`.
- Implement minimal `"R"` scheme encoder (GF-01’s run-length-like scheme).
- Implement a Press module that:
  - Buffers GF-01 streams (post_u deltas, flux sequences).
  - Computes `L_model`, `L_residual`, `L_total` per stream.
  - Computes `manifest_check` exactly as per the spec.
- Tests:
  - Window ticks 1–8:
    - `manifest_check = 487809945`.
  - Window ticks 1–2:
    - `manifest_check = 869911338`.
  - Streams and MDL values match the APX sheets.

**Where it lives (code):**

- `src/press/press.py`
  - Implements `PressWindowContextV1` (minimal Phase 1 form).
  - Implements APX stream / manifest structures.
  - Implements the R-mode scheme and manifest calculation for GF-01.

**Where it lives (tests):**

- `tests/unit/test_press.py`
  - Reconstructs the 1–8 and 1–2 windows from GF-01 data.
  - Verifies `L_total` for the streams and the exact `manifest_check` values.
- `tests/gf01/test_run_gf01.py`
  - Confirms that the APX manifest produced inside `run_gf01()` matches GF-01 exam requirements.

**Status:** Implemented and tested. Press/APX reproduces GF-01 manifest checks for the required windows.

---

### 2.5 Issue 5 — NAPEnvelope_v1 & Minimal Gate/TBP Integration

**Spec / Issue:**

- SPEC-002 Issue 5 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- Contracts:
  - `docs/contracts/NAPEnvelope_v1.md`
  - `docs/contracts/SceneFrame_v1.md`
  - `docs/contracts/TickLoop_v1.md`

**What it required:**

- Implement `NAPEnvelope_v1` and `SceneFrame_v1` types.
- Implement minimal Gate module that, per tick:
  - Builds a scene frame from UMX + Loom + Press outputs.
  - Emits **one NAP envelope per tick** with:
    - `v = 1`
    - `gid = "GF01"`
    - `layer = "DATA"`
    - `mode = "P"`
    - `payload_ref = manifest_check`
    - `seq = tick`
    - `prev_chain = C_{t-1}` (with `C_0 = 1234567`).

**Where it lives (code):**

- `src/gate/gate.py`
  - Implements `SceneFrameV1` as the per-tick integration object.
  - Implements `NAPEnvelopeV1`.
  - Provides helper logic to build both from UMX tick ledger, Loom chain, and APX manifest data for GF-01.

**Where it lives (tests):**

- `tests/unit/test_gate.py`
  - Validates that envelopes produced for GF-01 ticks 1–8:
    - Have correct `gid`, `layer`, `mode`, `v`.
    - Use `payload_ref` equal to the manifest’s `manifest_check`.
    - Use `prev_chain` equal to `C_0` then `C_1..C_7` for ticks 1..8.
- `tests/gf01/test_run_gf01.py`
  - Confirms that the envelopes emitted during the full GF-01 run match expectations.

**Status:** Implemented and tested. Gate/NAP wiring is present and producing deterministic envelopes.

---

### 2.6 Issue 6 — TickLoop_v1 End-to-End Wiring (`run_gf01`)

**Spec / Issue:**

- SPEC-002 Issue 6 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- Contracts:
  - `docs/contracts/TickLoop_v1.md`
  - All pillar contracts (UMX, Loom, Press, NAP).

**What it required:**

- Implement an orchestrated GF-01 run function (`run_gf01()` or equivalent) that:
  - Constructs GF-01 topology + profile.
  - Sets initial state `u(0) = [3,1,0,0,0,0]` and chain `C_0 = 1234567`.
  - Steps through ticks `t = 1..8`:
    - UMX → Loom → Press → Gate/NAP.
  - Returns:
    - All UMX tick ledgers,
    - All Loom P-blocks and the final I-block at tick 8,
    - APX manifests (1–8, 1–2),
    - NAP envelopes.

**Where it lives (code):**

- `src/core/tick_loop.py`
  - Defines `GF01RunResult` (or equivalent) to bundle the artefacts.
  - Implements `run_gf01()`:
    - Wires together:
      - GF-01 topology/profile from Issue 1.
      - UMX engine from Issue 2.
      - Loom from Issue 3.
      - Press/APX from Issue 4.
      - Gate/NAP from Issue 5.

**Where it lives (tests):**

- `tests/gf01/test_run_gf01.py`
  - Calls `run_gf01()`.
  - Checks:
    - 8 UMX tick ledgers.
    - 8 Loom P-blocks, 1 I-block at t = 8.
    - Correct chain values `C_1..C_8` for GF-01.
    - Correct APX manifest properties and `manifest_check`.
    - Correct envelopes (counts and key fields).

**Status:** Implemented and tested. There is a single orchestrated GF-01 run that produces all required artefacts.

---

### 2.7 Issue 7 — Determinism Harness & Regression Snapshot

**Spec / Issue:**

- SPEC-002 Issue 7 in `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- Contracts:
  - `docs/contracts/UMXTickLedger_v1.md`
  - `docs/contracts/LoomBlocks_v1.md`
  - `docs/contracts/APXManifest_v1.md`
  - `docs/contracts/NAPEnvelope_v1.md`
  - `docs/contracts/ULedgerEntry_v1.md` (for Phase 2+, but determinism harness anticipates it)

**What it required:**

- Canonical serialisation for core artefacts.
- Double-run determinism test:
  - Run GF-01 twice, serialise both outputs, compare byte-for-byte.
- Snapshot regression test:
  - Persist a known-good snapshot JSON for GF-01.
  - Future runs must match exactly, or tests fail.

**Where it lives (code):**

- `src/core/serialization.py`
  - Defines how GF-01 run results are serialised to canonical JSON.
  - Ensures stable ordering / formatting for determinism.

**Where it lives (tests):**

- `tests/gf01/test_determinism_snapshot.py`
  - Runs `run_gf01()` twice and compares both serialised outputs.
  - Loads `tests/snapshots/gf01_run_snapshot.json` and compares current output to that snapshot.

- `tests/snapshots/gf01_run_snapshot.json`
  - The canonical saved output for a known-good GF-01 run:
    - Contains ledgers, blocks, manifests, and envelopes.

**Status:** Implemented and tested. GF-01 behaviour is locked in via snapshot; any change will surface as a test failure.

---

## 3. How to Verify Phase 1 (for Humans / Agents)

Phase 1 verification = **all SPEC-002 tests passing**.

Typical checks (run by a dev or a coding agent):

- Run unit + GF-01 tests (e.g. with `pytest`):
  - `tests/unit/test_topology_profile.py`
  - `tests/unit/test_umx_engine.py`
  - `tests/unit/test_loom.py`
  - `tests/unit/test_press.py`
  - `tests/unit/test_gate.py`
  - `tests/gf01/test_run_gf01.py`
  - `tests/gf01/test_determinism_snapshot.py`

Success means:

- UMX, Loom, Press, Gate/NAP all behave exactly as paper GF-01 says they should.
- `run_gf01()` is deterministic.
- Outputs match the saved snapshot.

If any behaviour legitimately changes in future:

1. Update the relevant specs/contracts under `docs/`.
2. Update implementation under `src/`.
3. Update expected values and snapshots under `tests/` and `tests/snapshots/`.

---

## 4. Boundaries and Known Limitations (Phase 1 Only)

Phase 1 deliberately keeps scope tight:

- **Single topology only:** GF-01 is hard-coded as the only scenario.
- **Single profile only:** CMP-0 is the only profile implemented.
- **Press/APX:** Only the minimal “R” mode required for GF-01 is implemented.
- **Gate/TBP:** Only per-tick DATA/P envelopes for GF-01.
- **Codex:** Not active in Phase 1; Codex Eterna remains observer-only and is introduced in Phase 2.
- **U-ledger:** Determinism harness uses canonical serialisation, but full U-ledger hash chain is Phase 2+.

These limitations are intentional and match the design in:

- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`

---

## 5. Phase 1 → Phase 2 Handover

With Phase 1 complete:

- We have a **working, deterministic, paper-parity engine** for GF-01 under CMP-0.
- All cross-pillar handoffs (UMX → Loom → Press → Gate/NAP) are proven in at least one concrete scenario.
- The determinism harness + snapshot provide a strong guardrail for future change.

This is the required foundation for **SPEC-005 — Phase 2: Pillar V1 Generalisation**, where we:

- Generalise UMX to multiple topologies and broader usage.
- Generalise Loom (configurable I-block spacing, replay API).
- Generalise Press/APX (stream registry, additional schemes, manifest generalisation).
- Promote `SceneFrame_v1` to the primary integration object.
- Introduce U-ledger entries and Codex Eterna in observer-only mode.

**Recommended next doc to open when starting Phase 2:**

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/spec_005_Phase2_Pillar_V1_GitHub_Issues.md`

---

## 6. File Placement

Suggested location for this closeout report in the repo:

- `docs/specs/spec_002_Phase1_Completion_Report_GF01_CMP0_v1.md`

You can rename it if you prefer a different naming style, but keeping the `spec_002_...` prefix makes it easy to discover alongside the other Phase 1 docs.

---

**Phase 1 (SPEC-002) is now considered CLOSED.**  
The repo is ready to proceed to Phase 2 work under SPEC-005.
