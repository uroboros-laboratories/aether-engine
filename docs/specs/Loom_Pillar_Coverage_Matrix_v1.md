# Aevum Loom Pillar Coverage Matrix — v1 (Draft)

## Status

- **Pillar:** Aevum Loom (Time Axis & Blocks)  
- **Doc:** Coverage of Loom master-spec implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Show how the Loom master spec’s requirements are implemented and tested across phases/specs, and surface obvious gaps.

This is a **first-pass coverage map**. Requirements are grouped into themes rather than every line individually; we can tighten it later to section/line-level once everything is in the repo.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this coverage doc (we can later link these to exact section refs in `Aevum Loom Pillar — Master spec.txt`).  
- **Master Spec Theme** — Short label for the requirement group from the Loom master spec.  
- **Summary** — What the requirement demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it’s primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level Requirements)

### 2.1 Core Types & Records

| Req ID  | Master Spec Theme          | Summary                                                                                                   | Primary Specs                              | Phase | Notes / Tests |
|---------|----------------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------|-------|---------------|
| LOOM-01 | LoomPBlock core record     | Define `LoomPBlock_v1` as the per-tick Loom record (chain update + linkage to UMX tick data).           | SPEC-002, SPEC-005                         | P1–P2 | P1: GF-01 P-blocks implicitly defined; P2: formal contract + implementation. |
| LOOM-02 | LoomIBlock checkpoint      | Define `LoomIBlock_v1` for periodic checkpoints (I-blocks) capturing chain, state snapshot, topology.   | SPEC-002, SPEC-005                         | P1–P2 | P1: GF-01 I-block at t=8; P2: general I-block spacing and structure. |
| LOOM-03 | Chain state representation | Define representation for chain value `C_t` and any related metadata (e.g. sequence index, flags).      | SPEC-002, SPEC-005                         | P1–P2 | Chain is integer `C_t`; spec-005 formalises context fields. |
| LOOM-04 | Profile binding            | Define how Loom uses profile parameters (e.g. modulus `M`, spacing `W`, chain tuning constants).        | SPEC-002, SPEC-005                         | P1–P2 | CMP-0 chain rule keyed off `Profile_CMP0_v1`; later profiles share shape. |

### 2.2 Chain Rule & s_t Rule

| Req ID  | Master Spec Theme            | Summary                                                                                             | Primary Specs      | Phase | Notes / Tests |
|---------|------------------------------|-----------------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| LOOM-10 | CMP-0 s_t rule               | Implement CMP-0 `s_t` computation (constant 9 for GF-01) as per Loom master spec.                  | SPEC-002, SPEC-005 | P1–P2 | P1: GF-01 uses implicit constant; P2: explicit `s_t` rule in profile. |
| LOOM-11 | CMP-0 chain update rule      | Implement CMP-0 chain update: `C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M`.                      | SPEC-002, SPEC-005 | P1–P2 | GF-01 chain sequence is canonical reference. |
| LOOM-12 | Integer-only chain arithmetic| All Loom chain operations are integer-only and deterministic.                                       | SPEC-002, SPEC-005 | P1–P2 | Enforced via tests + determinism harness. |
| LOOM-13 | Parameterised chain rules    | Structure Loom so other profiles can define different chain rules without breaking CMP-0.          | SPEC-005          | P2    | Profile-driven chain rule; future profiles plug into same interface. |

### 2.3 Time Axis, Blocks & Spacing

| Req ID  | Master Spec Theme        | Summary                                                                                          | Primary Specs      | Phase | Notes / Tests |
|---------|--------------------------|--------------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| LOOM-20 | Time axis per run        | Loom defines a single, monotonic tick index per run (`t = 1,2,...`) and binds blocks to ticks. | SPEC-002, SPEC-005 | P1–P2 | P1 GF-01 tick 1–8; P2 generalises to arbitrary run lengths. |
| LOOM-21 | P-block emission         | Emit a `LoomPBlock_v1` for each tick, containing `C_t` and relevant tick-level info.           | SPEC-002, SPEC-005 | P1–P2 | P1 implicit; P2 formal contract + tests. |
| LOOM-22 | I-block spacing          | Support configurable I-block spacing `W` (CMP-0 defaults to 8, but can vary for other profiles).| SPEC-005          | P2    | P2.2.2 configurable spacing; GF-01 uses W=8. |
| LOOM-23 | I-block content          | I-blocks must contain chain value, state snapshot, and topology snapshot for the period.        | SPEC-002, SPEC-005 | P1–P2 | P1 GF-01 I-block; P2 general I-block semantics tested on GF-01 + toy runs. |

### 2.4 Run Context & Replay

| Req ID  | Master Spec Theme        | Summary                                                                                                  | Primary Specs      | Phase | Notes / Tests |
|---------|--------------------------|----------------------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| LOOM-30 | LoomRunContext           | Encapsulate Loom state per run: current `C_t`, spacing, `s_t` rule, block storage.                     | SPEC-005           | P2    | P2.2.1 LoomRunContext epic. |
| LOOM-31 | Ingest from UMX          | Loom must ingest `UMXTickLedger_v1` per tick as its main input.                                         | SPEC-002, SPEC-005 | P1–P2 | GF-01 integration in P1; P2 formalises Loom’s API. |
| LOOM-32 | Replay chain & state     | Provide replay APIs: `get_chain_at(t)`, `get_pblock(t)`, `get_iblock_for(t)`, `replay_state_at(t)`.     | SPEC-005, SPEC-006 | P2–P4 | P2.2.3 defines replay; P4 extends to multi-graph replay. |
| LOOM-33 | Deterministic replay     | Replay of state and chain must match the original run exactly.                                          | SPEC-005, SPEC-006 | P2–P4 | Determinism + snapshot tests enforce matching states. |

### 2.5 Multi-Graph & Dynamic Topology

| Req ID  | Master Spec Theme         | Summary                                                                                   | Primary Specs      | Phase | Notes / Tests |
|---------|---------------------------|-------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| LOOM-40 | Multi-graph awareness     | Loom must track chains for multiple graphs in multi-graph runs.                          | SPEC-006           | P4    | P4.1 & P4.3 integrate Loom with graph registry. |
| LOOM-41 | Topology change visibility| SLP topology events must be visible to Loom so checkpoints reflect correct topology.      | SPEC-006           | P4    | I-blocks capture updated topology; SLP events included in Loom/U-ledger context. |
| LOOM-42 | Replay with SLP events    | Replay must reconstruct both topology and state, applying SLP events in correct order.    | SPEC-006           | P4    | Replay tests for dynamic topology scenarios. |

### 2.6 Integration with Other Pillars

| Req ID  | Master Spec Theme             | Summary                                                                                             | Primary Specs           | Phase | Notes / Tests |
|---------|-------------------------------|-----------------------------------------------------------------------------------------------------|-------------------------|-------|---------------|
| LOOM-50 | UMX integration               | Loom consumes `UMXTickLedger_v1` and uses its state to compute/attach chain evolution.              | SPEC-002, SPEC-005, 006 | P1–P4 | Rooted in SPEC-002 GF-01; extended in SPEC-005; multi-graph in SPEC-006. |
| LOOM-51 | Press/APX integration        | Loom’s `C_t` and block metadata can be used as part of Press streams or conditioning information.   | SPEC-002, SPEC-005, 004 | P1–P3 | Initially just chain values; AEON/APXi may use chain as additional stream or context. |
| LOOM-52 | Gate/TBP & SceneFrame usage  | Loom chain values and block info appear in `SceneFrame_v1` and influence NAP envelopes.            | SPEC-002, SPEC-005, 003 | P1–P3 | GF-01 NAP uses `C_prev`/`C_t`; P2 makes SceneFrame central; P3 extends layering/CTRL semantics. |
| LOOM-53 | Codex ingest                  | Loom P/I-blocks are part of Codex’s trace inputs for motif identification and proposals.           | SPEC-005, SPEC-006, 007 | P2–P5 | CodexContext ingests chain and blocks; proposals about temporal motifs may depend on Loom data. |
| LOOM-54 | U-ledger inclusion            | Loom blocks and/or chain snapshots must be serialised & hashed into ULedgerEntry records.          | SPEC-002, SPEC-005, 006, 007 | P1–P5 | SPEC-002 determinism harness; SPEC-005 canonical serialisation; SPEC-006/7 add SLP/governance linkage. |

### 2.7 Governance & Policy (Loom-Relevant)

| Req ID  | Master Spec Theme           | Summary                                                                                             | Primary Specs      | Phase | Notes / Tests |
|---------|-----------------------------|-----------------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| LOOM-60 | Governance over chain params| Changes to Loom profile parameters (e.g. `W`, chain rule constants) must be governed.             | SPEC-007           | P5    | Treated as configuration/parameter changes; budgets/policies control changes. |
| LOOM-61 | Governance over SLP timing  | Rules about when topology changes (SLP events) may occur can be enforced by governance.            | SPEC-006, SPEC-007 | P4–P5 | SLP events in P4; P5 introduces budgets/policies on when/how often they occur. |
| LOOM-62 | Traceable decisions         | All governance decisions affecting Loom behaviour must be visible in NAP CTRL and U-ledger trail.  | SPEC-007           | P5    | GovernanceDecision_v1 and ledger entries link decisions to chain/blocks. |

---

## 3. Phase-by-Phase View (Loom Only)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

Loom focus:

- Implement basic chain rule for CMP-0 over GF-01 (LOOM-10, LOOM-11, LOOM-12).  
- Implicit P-block concept: chain-per-tick attached to UMX ticks (LOOM-01, partially).  
- Produce a single I-block at `t=8` for GF-01, containing chain, state, topology snapshot (LOOM-02, LOOM-23).  
- Integrate with GF-01 Press and NAP by exposing `C_t` and relevant fields (LOOM-50–52 minimally).  
- Determinism: GF-01 chain sequence is part of the overall snapshot test (LOOM-32, LOOM-33 indirectly).

Coverage notes:

- P1 is deliberately narrow: single graph, no replay API, no multi-graph, minimal explicit context.  
- It proves Loom’s **mathematical chain rule** and single-window checkpointing are correct.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

Loom upgrades:

- Introduce `LoomRunContext` as the main time-axis state holder (LOOM-30).  
- Explicit `LoomPBlock_v1` and `LoomIBlock_v1` contracts implemented (LOOM-01, LOOM-02).  
- Configurable I-block spacing `W` via profile and/or run config (LOOM-22).  
- Explicit `s_t` rule defined and parameterised (still constant 9 for CMP-0) (LOOM-10, LOOM-13).  
- Replay APIs: chain and state replayable from I-blocks (LOOM-32, LOOM-33).  
- Clear integration points for UMX, Press, Gate, Codex, and U-ledger (LOOM-50–54).

Coverage notes:

- P2 turns Loom from a **hard-coded helper** into a general time-axis engine.  
- Still single-graph-per-run; multi-graph awareness comes later in P4.

---

### Phase 3 — SPEC-003 & SPEC-004 (Loom Touchpoints)

Loom’s core math stays the same; its role in IO/analysis expands:

- SPEC-003 (Gate/PFNA V0) ties Loom into richer session and NAP semantics:  
  - Session lifecycle (start/stop) anchored in time via Loom (LOOM-52).  
  - PFNA-driven scenarios recorded along the Loom chain for later replay.  

- SPEC-004 (AEON/APXi) uses time-axis semantics as part of AEON window grammars:  
  - AEON window definitions reference ticks, ranges, and possibly Loom chain properties (LOOM-51).  

Coverage notes:

- Phase 3 leverages Loom as **canonical time** for external inputs and advanced temporal views, without changing core chain rules.

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

Loom responsibilities grow to support SLP & multi-graph:

- Multi-graph awareness: track chains per graph (LOOM-40).  
- Visibility of SLP topology events: I-blocks and chains must reflect structural changes (LOOM-41).  
- Replay extended to reconstruct both **which graphs exist** and **their state** at any tick (LOOM-42).  
- U-ledger entries capture chain evolution + SLP events (LOOM-54 plus SLP integration).

Coverage notes:

- P4 is where Loom becomes the **global timeline** for multiple evolving graphs, not just “one graph’s chain”.  
- It works tightly with UMX multi-graph registry and SLP events.

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

Loom becomes part of the governance surface:

- Changes to chain parameters and I-block spacing (profiles) become governed (LOOM-60).  
- Timing and frequency of SLP events can be constrained by policies and budgets (LOOM-61).  
- Governance decisions related to time axis and topology changes must be visible in CTRL layer and U-ledger (LOOM-62).  

Coverage notes:

- P5 doesn’t change Loom’s math; it **wraps** Loom in governance so time and topology evolution are budgeted and policy-controlled.

---

## 4. Known / Likely Gaps (to Refine)

This matrix is a first pass; once we do a closer read of the Loom master spec we should refine:

1. **Exact s_t variants**  
   - If Loom master spec describes more advanced or profile-specific `s_t` rules (e.g. derived from UMX flux stats), we should:  
     - Add specific LOOM-1x requirements,  
     - Map them to a spec/phase (likely optional in SPEC-005, or future profile specs).

2. **I-block detailed content**  
   - Master spec may require specific fields or indexing for I-blocks (e.g. block IDs, proof-of-order metadata).  
   - Add LOOM-2x rows for those and point them at SPEC-005/006.

3. **Chain invariants beyond modulus**  
   - If chain invariants include specific behaviours (e.g. no trivial cycles under some conditions), we may need additional diagnostics or tests.  

4. **AEON/APXi-specific Loom hooks**  
   - AEON grammar may rely on particular Loom semantics (e.g. mapping block IDs to AEON windows).  
   - Once `AEONWindowGrammar_v1` is final, we can add LOOM-5x requirements linking Loom to AEON more explicitly.

5. **Performance / scaling notes**  
   - If Loom master spec calls out bounds (e.g. block storage strategy, checkpoint frequency), we should reflect that either here or in a separate performance-focused spec.

These gaps don’t block implementation but mark areas for deepening the coverage later.

---

## 5. Next Steps

For Loom pillar coverage, immediate follow-ups could be:

1. **Add master-spec references**  
   - Add a “Master Spec Ref” column with section names/anchors from `Aevum Loom Pillar — Master spec.txt`.  
   - Start with core items: LOOM-01, 02, 10–13, 20–23, 32–33, 40–42, 50–54, 60–62.

2. **Bind tests once the repo is live**  
   - For each requirement, note specific test modules / fixtures (e.g. `tests/loom/test_loom_gf01.py`).

3. **Produce equivalent coverage matrices for the remaining pillars**  
   - Press/APX, Gate/TBP, Codex, U-ledger — each gets a similar table, so we can see global coverage at a glance and be confident we’re on track for 100% of the master specs.
