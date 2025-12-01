# UMX Pillar Coverage Matrix — v1 (Draft)

## Status

- **Pillar:** Universal Matrix (UMX)  
- **Doc:** Coverage of master UMX implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Show how the UMX master spec’s requirements are implemented and tested across phases/specs, and expose any obvious gaps.

This is a **first-pass coverage map**. It groups master-spec requirements into themes rather than listing every sentence individually, but it’s designed so we can refine it down to line-level later if needed.

## Phase 6 Coverage Crosswalk

- **CMP-0 + policy hooks delivered.** Causal radius, epsilon-cap, deterministic ordering, and kill-switch semantics implemented in `umx.engine` with regression coverage in `tests/unit/test_umx_engine.py` and lifecycle checks in `tests/unit/test_session_lifecycle.py`.
- **Cross-pillar run path validated.** Gate PFNA ingress, Loom persistence, Press streams, and U-Ledger checkpoints are exercised by `tests/gf01/test_run_gf01.py` and `tests/integration/test_full_system_demo.py`, with snapshots under `tests/snapshots/` confirming deterministic outputs.
- **Governance traceability complete.** Codex decisions and Gate governance envelopes feed U-Ledger checkpoints for UMX runs, validated via refreshed governance snapshots and `tests/unit/test_gate_governance.py`.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this coverage doc (we can later map these to exact line/section refs in `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`).  
- **Master Spec Theme** — Short label for the requirement group from the UMX master spec.  
- **Summary** — What the requirement actually demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it is primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level Requirements)

### 2.1 Core Types & Records

| Req ID | Master Spec Theme                 | Summary                                                                 | Primary Specs                              | Phase | Notes / Tests |
|--------|-----------------------------------|-------------------------------------------------------------------------|--------------------------------------------|-------|---------------|
| UMX-01 | UMXTickLedger core record        | Define `UMXTickLedger_v1` with all required fields (pre/post state, per-edge flux, invariants) as the canonical per-tick record. | SPEC-002, SPEC-005                        | P1–P2 | SPEC-002: GF-01 tick ledger parity vs paper tables; SPEC-005: generalises but keeps same contract. |
| UMX-02 | EdgeFlux / per-edge structures   | Define per-edge flux representation (e.g. `EdgeFlux_v1`) capturing `du`, `raw`, `f_e` and any IDs needed. | SPEC-002, SPEC-005                        | P1–P2 | GF-01 tables exercised in P1; P2 keeps type but generalises to arbitrary topologies. |
| UMX-03 | TopologyProfile definition       | Define `TopologyProfile_v1` for nodes/edges and associated parameters (`k`, `cap`, `SC`, etc.). | SPEC-002, SPEC-005                        | P1–P2 | P1: GF-01 hard-coded topology; P2: loader/validator, multiple profiles (line/ring/star). |
| UMX-04 | Profile (numeric) definition     | Define `Profile_CMP0_v1` (and future profiles) with all numeric parameters (`M`, `C0`, `SC`, rules, defaults). | SPEC-002, SPEC-005                        | P1–P2 | P1 locks CMP-0 for GF-01; P2 defines reusable profile type and allows more instances. |

### 2.2 Flux Rule & State Evolution

| Req ID | Master Spec Theme                 | Summary                                                                                      | Primary Specs        | Phase | Notes / Tests |
|--------|-----------------------------------|----------------------------------------------------------------------------------------------|----------------------|-------|---------------|
| UMX-10 | CMP-0 flux rule                  | Implement integer-only CMP-0 flux rule (`du`, `raw`, `f_e`) exactly as defined in UMX master spec. | SPEC-002, SPEC-005  | P1–P2 | GF-01 V0 tick tables in SPEC-002 are the reference; SPEC-005 generalises stepping across topologies. |
| UMX-11 | Conservation & invariants        | Per tick, total mass is conserved (`sum_pre_u == sum_post_u == z_check`) and checked.       | SPEC-002, SPEC-005  | P1–P2 | P1: GF-01 tests; P2: diagnostics mode and multi-topology conservation tests. |
| UMX-12 | Integer-only arithmetic          | All core UMX operations use integer math; no floats or FP rounding paths.                   | SPEC-002, SPEC-005  | P1–P2 | Enforced via implementation notes + tests; determinism/snapshot tests guard drift. |
| UMX-13 | Order of application             | Edges stepped in a defined order (`e_id` order) with well-defined accumulation semantics.   | SPEC-002, SPEC-005  | P1–P2 | P1 uses GF-01 edge tables; P2 codifies ordering in `TopologyProfile_v1` + `UMX.step`. |

### 2.3 Topology Handling

| Req ID | Master Spec Theme                   | Summary                                                                                       | Primary Specs         | Phase | Notes / Tests |
|--------|-------------------------------------|-----------------------------------------------------------------------------------------------|-----------------------|-------|---------------|
| UMX-20 | Static single-graph topology       | Support static topology for a single graph per run (UMX baseline).                           | SPEC-002, SPEC-005   | P1–P2 | GF-01 baseline; additional simple graphs in P2. |
| UMX-21 | Multi-topology support (V1)        | Ability to load and validate multiple different topologies (GF-01, line, ring, star, etc.).  | SPEC-005             | P2    | P2.1.1 loader/validator epic. |
| UMX-22 | Multi-graph runtime (V1.5)         | Ability to run multiple graphs concurrently in a single run, each with its own topology/profile. | SPEC-006             | P4    | P4.1 multi-graph runtime & registry. |
| UMX-23 | Dynamic topology changes (SLP)     | Topology can change over time via SLP events (`ADD_NODE`, `ADD_EDGE`, etc.).                 | SPEC-006             | P4    | P4.2 SLP events & dynamic topology; replay via Loom/U-ledger. |

### 2.4 Run Context & Execution Model

| Req ID | Master Spec Theme                  | Summary                                                                                      | Primary Specs   | Phase | Notes / Tests |
|--------|------------------------------------|----------------------------------------------------------------------------------------------|-----------------|-------|---------------|
| UMX-30 | Single-run context abstraction     | Encapsulate a single UMX run’s state in a context object (`UMXRunContext`).                 | SPEC-005        | P2    | P2.1.2 epic; used by Loom, Gate, Codex, and TickLoop. |
| UMX-31 | Multi-run / multi-instance safety  | Allow multiple UMXRunContexts in one process without global mutable state.                  | SPEC-005, 006   | P2–P4 | P2 context design; P4 extends it to multi-graph registry. |
| UMX-32 | Deterministic stepping API         | Provide `step()` and `run_until()` APIs with fully deterministic semantics.                 | SPEC-005        | P2    | Tests: double-run determinism and snapshot comparisons. |
| UMX-33 | Integration with TickLoop          | TickLoop contract specifies how UMX integrates with Loom, Press, Gate.                      | SPEC-002, 005   | P1–P2 | P1: GF-01 `run_gf01`; P2: generalised TickLoop_v1 usage. |

### 2.5 Diagnostics, Invariants & Debug

| Req ID | Master Spec Theme             | Summary                                                                                       | Primary Specs | Phase | Notes / Tests |
|--------|-------------------------------|-----------------------------------------------------------------------------------------------|---------------|-------|---------------|
| UMX-40 | Optional diagnostic mode      | Ability to run with invariant checks and extra metrics (min/max, overflow flags, etc.).      | SPEC-005      | P2    | P2.1.4 diagnostics & invariant checks. |
| UMX-41 | Non-intrusive diagnostics     | Diagnostics must not change core state or outputs; they affect only logs/metadata.           | SPEC-005      | P2    | Tests compare outputs with/without diagnostics enabled. |
| UMX-42 | Error path clarity            | Invalid topologies/profiles produce deterministic, clear errors/logs.                        | SPEC-005      | P2    | Loader/validator tests for failure cases. |

### 2.6 Integration with Other Pillars

| Req ID | Master Spec Theme                 | Summary                                                                                         | Primary Specs           | Phase | Notes / Tests |
|--------|-----------------------------------|-------------------------------------------------------------------------------------------------|-------------------------|-------|---------------|
| UMX-50 | Loom integration (time axis)     | UMX must emit tick-level records consumable by Loom to build chains and blocks.                | SPEC-002, 005, 006      | P1–P4 | Loom uses `UMXTickLedger_v1` as input; P4 adds multi-graph integration. |
| UMX-51 | Press/APX integration            | UMX outputs (state deltas, fluxes) must be usable as Press streams for compression/MDL.       | SPEC-002, 005, 004      | P1–P3 | GF-01 streams S1/S2 in P1; P2 generalises; P3 AEON/APXi use these streams as raw material. |
| UMX-52 | Gate/TBP & SceneFrame integration| UMX state (`pre_u`, `post_u`) participates in `SceneFrame_v1` and NAP payloads.               | SPEC-002, 005, 003      | P1–P3 | P1 minimal scene; P2 makes SceneFrame primary; P3 extends with PFNA & layering. |
| UMX-53 | Codex ingest                     | UMX tick ledgers are one of the main trace sources for Codex motif learning.                  | SPEC-005, 006, 007      | P2–P5 | CodexContext uses UMXTickLedger sequences as input; actioning gated by SPEC-007. |
| UMX-54 | U-ledger inclusion               | UMX outputs must be serialised & hashed into U-ledger entries.                                 | SPEC-002, 005, 006, 007 | P1–P5 | SPEC-002 determinism harness; SPEC-005 canonical serialisation & hashes; SPEC-006/7 add SLP/governance links. |

### 2.7 Governance & Policy (UMX-Relevant)

| Req ID | Master Spec Theme                    | Summary                                                                                     | Primary Specs      | Phase | Notes / Tests |
|--------|--------------------------------------|---------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| UMX-60 | Governance over topology change      | Structural changes to UMX graphs must be governed by policies & budgets.                   | SPEC-006, 007      | P4–P5 | SLP events in P4; governance policies & budgets applied in P5. |
| UMX-61 | Governance over parameter change     | Changes to profiles/params (e.g. caps, gains) must pass governance rules.                  | SPEC-007           | P5    | Mapped to proposal types & budget classes. |
| UMX-62 | Traceable decisions                  | All governed UMX changes must be visible in NAP CTRL and U-ledger (who/what/when/why).     | SPEC-007           | P5    | GovernanceDecision_v1 + ledger entries; replay reconstructs decision trail. |

---

## 3. Phase-by-Phase View (UMX Only)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

UMX focus:

- Implement CMP-0 flux rule for GF-01 only (UMX-10, UMX-11, UMX-12).  
- Define UMXTickLedger and EdgeFlux in practice for GF-01 (UMX-01, UMX-02).  
- Hard-code GF-01 topology & profile (UMX-03, UMX-04) — no general loader yet.  
- Integrate UMX with Loom, Press, NAP in a minimal way to pass GF-01 exam (UMX-33, UMX-50, UMX-51, UMX-52).  
- Determinism harness & snapshot focused on GF-01 (UMX-32, UMX-54 for that scenario).

Coverage notes:

- P1 is intentionally **narrow** but deep: one graph, one profile, full parity.  
- Many generality requirements (multi-topology, multi-graph, governance) are not yet covered here by design.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

UMX upgrades:

- Introduce `TopologyProfile_v1` loader & validator (UMX-03, UMX-21, UMX-42).  
- Introduce `UMXRunContext` with clean run abstraction (UMX-30, UMX-31, UMX-32).  
- Generalise CMP-0 stepping across arbitrary topologies (UMX-10, UMX-11, UMX-13 extended).  
- Add diagnostics & invariant checks (UMX-40, UMX-41).  
- Solidify integration contracts with Loom, Press, Gate, Codex, and U-ledger (UMX-50–UMX-54).

Coverage notes:

- P2 is where UMX becomes a **proper general engine** instead of a special GF-01 runner.  
- Still single-graph-per-run; multi-graph and SLP are deferred to P4.  

---

### Phase 3 — SPEC-003 & SPEC-004 (UMX Touchpoints)

UMX remains the same numerically; changes are about IO & analysis:

- SPEC-003 (Gate/PFNA V0) affects **how inputs get into UMX**:  
  - PFNA V0 pipeline can set initial states and parameters (UMX-21/UMX-31 integration with PFNA).  
  - NAP layers & Session lifecycle wrap UMX runs more richly (UMX-52).

- SPEC-004 (Press AEON/APXi) affects **how UMX outputs are analysed/described**:  
  - UMXTickLedgers feed AEON/APXi hierarchies & descriptors via streams (UMX-51).  

Coverage notes:

- No new UMX core math here; it’s stabilisation at the IO and description layers.  

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

UMX responsibilities extend to topology and multi-graph:

- Multi-graph runtime & registry (UMX-22, UMX-31 via graph registry).  
- Dynamic topology via SLPEvent_v1 (UMX-23).  
- Integration with Loom and U-ledger so both state *and* topology can be replayed (UMX-50, UMX-54 extended).  
- Gate/TBP routing across graphs (UMX-52, cross-graph relations).

Coverage notes:

- P4 is where “UMX as a single graph” becomes **UMX as a population of graphs** with time-varying structures.  
- Governance is not yet applied; SLP events are assumed allowed by config.  

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

UMX is governed rather than free-running:

- Governance policies and budgets applied to UMX-related proposals:  
  - Topology events (UMX-60).  
  - Parameter/profile changes (UMX-61).  

- Codex proposals that touch UMX (e.g. place motif, add edge) must pass policy/budget checks before becoming SLP events.  
- All accepted/rejected UMX-related decisions are recorded in NAP CTRL and U-ledger (UMX-62).

Coverage notes:

- P5 doesn’t change UMX math; it constrains *who gets to ask UMX to change* and how often.  
- This is where “governed, self-modifying UMX” becomes possible but bounded.

---

## 4. Known / Likely Gaps (to be Refined)

This is a **draft** coverage map. Areas to refine once we take a finer-grained pass over the UMX master spec:

1. **Exact field-level mapping**  
   - For each field in UMXTickLedger_v1 and TopologyProfile_v1 (as defined in the master spec), we should:  
     - Confirm which SPEC-00X introduces it,  
     - Confirm which tests exercise it,  
     - Add row-level coverage entries if needed.

2. **Profile extension beyond CMP-0**  
   - Master spec may define additional profiles or hooks for future profiles beyond CMP-0.  
   - Coverage needs to specify whether these are:  
     - Not yet implemented (explicit TODO at Phase 2+), or  
     - Covered by generic profile machinery without concrete numeric definitions.

3. **Advanced invariants**  
   - If the master spec defines invariants beyond simple conservation (e.g. bounds, monotonicity in some dimensions), we should add UMX-4x entries and map them to diagnostics/tests.

4. **Performance / complexity notes**  
   - If UMX master spec includes performance-related constraints or guidelines, we may want coverage rows noting where those are to be addressed (likely in a later “performance optimisation” spec, not in SPEC-001–007).

5. **Codex-specific hooks**  
   - If UMX is expected to expose specific hooks or summarised statistics for Codex beyond raw tick ledgers, we should add requirements (UMX-5x) and map them to SPEC-005/007 work.

These gaps aren’t blockers for starting implementation, but they’re flags for a **second-pass, line-level coverage** once all pillar master specs are ingested more mechanically.

---

## 5. Next Steps

For UMX pillar coverage, next steps could be:

1. **Tighten mapping to master spec references**  
   - Add a column for “Master Spec Ref” with section/paragraph IDs from `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`.  
   - Fill at least for the most critical requirements (UMX-01, 10, 11, 20, 22, 23, 50, 54, 60–62).

2. **Add explicit test references**  
   - Once the repo exists, link each requirement to specific test files / fixtures (e.g. `tests/gf01/test_umx_gf01.py`).

3. **Repeat this exercise for the other pillars**  
   - Loom, Press/APX, Gate/TBP, Codex, U-ledger — each gets a similar coverage matrix, then we can aggregate into a single global “coverage dashboard”.

This doc is ready to drop into `docs/specs/` as part of the design set and can be iterated as the implementation and tests firm up.
