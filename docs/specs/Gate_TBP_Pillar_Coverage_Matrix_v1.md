# Trinity Gate / TBP / NAP / PFNA Pillar Coverage Matrix — v1 (Draft)

## Status

- **Pillar:** Trinity Gate / TBP + NAP envelopes + PFNA V0  
- **Doc:** Coverage of Gate/TBP master-spec implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Map the Gate/TBP + NAP/PFNA master spec requirements to SPEC-001–007 and phases, surfacing any obvious gaps on the path to 100% coverage.

This is a **first-pass coverage map**. Requirements are grouped into themes (types, lifecycle, NAP, PFNA, governance). Later, once the repo and tests exist, we can refine this to section/line-level coverage against `trinity gate full spec.txt` and related contracts.

## Phase 6 Coverage Crosswalk

- **PFNA ingress + scenes covered.** `tests/unit/test_gate_pfna_ingress.py` and `tests/unit/test_gate.py` exercise integerization, audit trails, and SceneFrame validation.
- **Governance enforcement complete.** `tests/unit/test_gate_governance.py` and `tests/integration/test_full_system_demo.py` confirm decision envelopes, per-tick caps, and deterministic filtering.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this coverage doc (we can later bind these to section refs in `trinity gate full spec.txt`, `NAPEnvelope_v1.md`, PFNA schema docs, etc.).  
- **Master Spec Theme** — Short label for the requirement group.  
- **Summary** — What the requirement demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it’s primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level Requirements)

### 2.1 Core Types & Records (Gate / NAP / SceneFrame / PFNA)

| Req ID     | Master Spec Theme          | Summary                                                                                                       | Primary Specs                                 | Phase | Notes / Tests |
|------------|----------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-------|---------------|
| GATE-01    | NAPEnvelope core record    | Define `NAPEnvelope_v1` as the canonical envelope for engine IO: fields for version, gid, layer, mode, payload_ref, chain, etc. | SPEC-002, SPEC-005, SPEC-003, SPEC-007        | P1–P5 | P1 minimal NAP for GF-01; P2 formal contract; P3 layering; P5 CTRL messages for governance. |
| GATE-02    | SceneFrame core record     | Define `SceneFrame_v1` as the per-tick integration bundle linking UMX, Loom, Press, Gate, NAP.               | SPEC-005, SPEC-003                             | P2–P3 | SPEC-005 promotes SceneFrame to primary integration object; SPEC-003 adds PFNA/session data. |
| GATE-03    | TickLoop contract          | Define `TickLoop_v1` describing how per-tick orchestration works (UMX → Loom → Press → Gate/NAP).            | SPEC-002, SPEC-005                             | P1–P2 | P1: GF-01 `run_gf01`; P2: generalised TickLoop_v1. |
| GATE-04    | PFNA placeholder record    | Define PFNA V0 schema (placeholder) for deterministic external integer inputs into Gate.                     | SPEC-003                                       | P3    | PFNA_V0_Schema_v1.md in SPEC-003. |

### 2.2 Gate/TBP Session & Lifecycle

| Req ID     | Master Spec Theme          | Summary                                                                                               | Primary Specs       | Phase | Notes / Tests |
|------------|----------------------------|-------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| GATE-10    | Session lifecycle          | Gate/TBP manages run/session lifecycle: init, start, tick loop, stop, teardown.                      | SPEC-003, SPEC-005  | P2–P3 | SPEC-005: TickLoop-level; SPEC-003: session semantics & NAP signalling. |
| GATE-11    | Run configuration          | Gate/TBP loads configuration for a run: topology/profile, Press config, PFNA config, governance hooks.| SPEC-003, SPEC-005, SPEC-006, SPEC-007 | P3–P5 | Config evolves as phases add multi-graph, governance. |
| GATE-12    | Deterministic runtime      | Given identical config, PFNA inputs, and specs, Gate/TBP must orchestrate deterministically.         | SPEC-002–007        | P1–P5 | Determinism harness and U-ledger snapshots act as tests. |
| GATE-13    | Error handling             | Misconfigurations should fail deterministically with clear errors (no partial hidden behaviour).     | SPEC-003, SPEC-005  | P2–P3 | Tests for invalid configs, missing PFNA, etc. |

### 2.3 NAP Layers & Modes

| Req ID     | Master Spec Theme          | Summary                                                                                                          | Primary Specs        | Phase | Notes / Tests |
|------------|----------------------------|------------------------------------------------------------------------------------------------------------------|----------------------|-------|---------------|
| GATE-20    | Layer semantics            | Support multiple NAP layers: at minimum INGRESS, DATA, CTRL, EGRESS (as per pillar spec).                        | SPEC-003, SPEC-005, SPEC-007 | P3–P5 | P3 introduces full layering; P5 uses CTRL for governance signals. |
| GATE-21    | Mode semantics             | Support NAP modes: at minimum P (primary) plus at least one secondary (e.g. S or AUX), even if rarely used early. | SPEC-005, SPEC-003   | P2–P3 | GF-01 uses DATA/P; other modes introduced as options in later phases. |
| GATE-22    | DATA layer envelopes       | Implement data-carrying envelopes linking SceneFrame/Press outputs to downstream consumers.                      | SPEC-002, SPEC-005, SPEC-003 | P1–P3 | GF-01 NAP; SceneFrame-derived NAP envelopes in P2; PFNA-based runs in P3. |
| GATE-23    | CTRL layer envelopes       | Implement control/governance envelopes (config loads, decisions, budgets, policy changes).                       | SPEC-003, SPEC-007   | P3–P5 | P3: simple session start/stop; P5: full governance messaging. |
| GATE-24    | EGRESS layer envelopes     | Implement egress semantics for shipping outputs externally in a deterministic, logged way (even if V0 is simple).| SPEC-003, SPEC-007   | P3–P5 | Likely minimal at first; grows with external tooling requirements. |

### 2.4 PFNA V0 (Deterministic External Inputs)

| Req ID     | Master Spec Theme         | Summary                                                                                                  | Primary Specs | Phase | Notes / Tests |
|------------|---------------------------|----------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| GATE-30    | PFNA schema V0            | Define PFNA V0 as a deterministic encoding for external integer sequences and small config tweaks.      | SPEC-003      | P3    | PFNA_V0_Schema_v1.md; minimal but structurally sound. |
| GATE-31    | PFNA ingest               | Gate must be able to load PFNA inputs deterministically (from file/config) and bind them to a run.      | SPEC-003      | P3    | Tests: same PFNA → same initial state/config; broken PFNA → clear error. |
| GATE-32    | PFNA → state mapping      | Provide a clear mapping from PFNA data to UMX initial state, parameters, or config handles.             | SPEC-003      | P3    | Tests: PFNA-coded small scenarios that change UMX initial conditions. |
| GATE-33    | PFNA determinism          | No randomness or ambiguity in how PFNA affects runs (no side channels or time-of-day dependence).       | SPEC-003, SPEC-007 | P3–P5 | Determinism harness + governance for PFNA-based structural changes later. |

### 2.5 SceneFrame as Integration Object

| Req ID     | Master Spec Theme           | Summary                                                                                                                | Primary Specs | Phase | Notes / Tests |
|------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| GATE-40    | SceneFrame aggregation      | For each tick, Gate builds `SceneFrame_v1` gathering: UMX state, Loom chain, relevant Press/APX outputs, NAP metadata.| SPEC-005      | P2    | P2.4.1 epic. |
| GATE-41    | SceneFrame → NAP            | NAP envelopes are derived from SceneFrames (not ad-hoc wiring) to remain consistent and predictable.                  | SPEC-005, 003 | P2–P3 | Tests check SceneFrame fields map correctly to NAP envelopes. |
| GATE-42    | SceneFrame extensibility    | SceneFrame can evolve (add fields, flags) without breaking core invariants or determinism.                            | SPEC-005, 004, 006, 007 | P2–P5 | AEON/APXi and SLP/governance may add new metadata; versioning handled via contracts. |

### 2.6 Multi-Graph & Routing

| Req ID     | Master Spec Theme           | Summary                                                                                                         | Primary Specs  | Phase | Notes / Tests |
|------------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|----------------|-------|---------------|
| GATE-50    | Graph addressing            | NAP envelopes and SceneFrames must include graph IDs (gid) for multi-graph runs.                               | SPEC-006       | P4    | P4.4 cross-graph relationships & routing. |
| GATE-51    | Routing configuration       | Gate configurations specify which PFNA inputs and NAP envelopes route to which graph(s).                        | SPEC-006, 003  | P3–P4 | PFNA-based mapping in P3; multi-graph routing in P4. |
| GATE-52    | Cross-graph communication   | Allow simple patterns where outputs from one graph become inputs/signals for another, via Gate/NAP.             | SPEC-006       | P4    | `GraphLink_v1`/equivalent used; tests for simple driver/follower setups. |
| GATE-53    | Routing determinism         | Routing decisions must be deterministic functions of config, tick, and inputs; no opaque randomness.           | SPEC-006, 007  | P4–P5 | Verified by replay and snapshot tests. |

### 2.7 Governance & Policy (Gate-Relevant)

| Req ID     | Master Spec Theme               | Summary                                                                                                           | Primary Specs | Phase | Notes / Tests |
|------------|---------------------------------|-------------------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| GATE-60    | Governance IO via NAP CTRL      | Governance messages (policies, budgets, decisions) are carried via NAP CTRL envelopes and logged in U-ledger.   | SPEC-007      | P5    | CTRL layer is the main governance IO path. |
| GATE-61    | Policy application in Gate/TBP  | Gate is responsible for applying governance policies and budgets to proposals and actions before they affect engine. | SPEC-007  | P5    | Gate/TBP is where “accept/reject/defer” decisions are actually enforced. |
| GATE-62    | Governance determinism          | Same inputs + same governance config must yield same decisions and NAP CTRL traffic.                             | SPEC-007      | P5    | Determinism tests that replay governance behaviour from ledger. |
| GATE-63    | Traceable decisions             | For each structural/config change, there must be a clear governance trail: proposal → decision → action (or not).| SPEC-007      | P5    | Linked through GovernanceDecision_v1, NAP CTRL messages, and U-ledger entries. |

---

## 3. Phase-by-Phase View (Gate/TBP + NAP + PFNA)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

Gate/TBP focus (minimal, just enough to pass GF-01):

- Very thin Gate: just enough logic to wrap UMX/Loom/Press outputs into simple NAP DATA/P envelopes (GATE-01, GATE-22).  
- Implicit per-tick “scene” concept (pre/post state, chain, manifest_check) used to build envelopes (GATE-40, partially).  
- GF-01 integration test uses `run_gf01()` as an end-to-end tick loop, mostly binding pillars together with minimal Gate semantics (GATE-03, GATE-12).  

Coverage notes:

- No PFNA, no layering beyond basic DATA/P, no governance.  
- Phase 1 Gate is a **wiring harness** for the GF-01 run, not yet a full pillar implementation.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

Gate/TBP upgrades:

- Formalise `SceneFrame_v1` as the primary per-tick integration object (GATE-02, GATE-40).  
- Refactor tick loop to use SceneFrames and a documented `TickLoop_v1` contract (GATE-03, GATE-10).  
- NAP envelopes become standardised outputs derived from SceneFrames (GATE-01, GATE-22, GATE-41).  
- Still single-graph-per-run; multi-graph addressing is not yet required.  

Coverage notes:

- P2 makes Gate/TBP a **proper integration pillar** rather than an ad-hoc GF-01 harness.  
- PFNA and layering/CTRL are still not fully implemented; they arrive in Phase 3.

---

### Phase 3 — SPEC-003 & SPEC-004 (PFNA V0 + AEON/APXi IO)

Gate/TBP expands in two directions:

- SPEC-003 (Gate/TBP & PFNA V0):  
  - Introduces PFNA V0 schema and deterministic ingest (GATE-04, GATE-30–GATE-33).  
  - Extends session lifecycle: start/stop messages, basic CTRL envelopes (GATE-10, GATE-23).  
  - Adds layering semantics for NAP (at least INGRESS/DATA/CTRL/EGRESS) (GATE-20, GATE-24).  
  - Connects PFNA inputs to UMX initial state/parameters and run config (GATE-11, GATE-32).  

- SPEC-004 (Press AEON/APXi) interacts mainly via configuration:  
  - Gate config and SceneFrames decide which windows Press runs and which streams are compressed or described (GATE-42).  

Coverage notes:

- P3 is where Gate/TBP becomes the **bridge to the outside world** (PFNA) and a richer NAP layer system.  
- Governance still not active; decisions are mostly based on static config.

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

Gate/TBP responsibilities grow with SLP & multi-graph:

- Multi-graph addressing: SceneFrames and NAP envelopes carry graph IDs; PFNA can target different graphs (GATE-50, GATE-51).  
- Cross-graph routing: Gate can send outputs from graph A to graph B as inputs or signals (GATE-52).  
- Routing determinism: given config, tick, and PFNA inputs, routing choices are deterministic, logged and replayable (GATE-53).  
- Integration with SLP events: some NAP CTRL/Data envelopes may trigger or describe SLP events for graphs (GATE-51, GATE-52).  

Coverage notes:

- P4 makes Gate/TBP the **traffic controller** for a population of graphs and their topology changes.  
- Governance still not fully engaged, but SLP events exist and Gate can route them.

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

Gate/TBP becomes the enforcement surface for governance:

- Governance policies & budgets loaded as part of run config (GATE-11, GATE-60).  
- Gate/TBP evaluates Codex proposals and SLP/PFNA actions under policy & budget constraints (GATE-61).  
- Governance decisions transmitted via NAP CTRL envelopes and recorded in U-ledger (GATE-60, GATE-62, GATE-63).  
- Determinism extends to governance: same proposals + same config → same NAP CTRL history and structural outcomes (GATE-62).  

Coverage notes:

- P5 doesn’t change Gate’s basic job (orchestration & IO); it **binds it under rule and budget** so that the system cannot self-modify without an explicit, traceable decision trail.

---

## 4. Known / Likely Gaps (to Refine)

Areas to tighten once we do a line-level pass on the Gate/TBP + NAP/PFNA parts of the master specs:

1. **NAP field-level requirements**  
   - Exact required fields, allowed modes/layers, and encode/decode behaviour for NAP envelopes.  
   - Add GATE-0x/2x rows mapping each field to specific tests.

2. **PFNA richness beyond V0**  
   - Master spec may define PFNA beyond V0 (e.g. PFNA profiles, more complex external encodings).  
   - These might require a future SPEC (Phase 4/5+) or an extension to SPEC-003.

3. **TBP (Trinity Behaviour Protocol) details**  
   - If TBP defines more detailed behavioural states, gating rules, or handshake semantics, we should:  
     - Add coverage rows (GATE-7x),  
     - Map them to relevant specs (likely SPEC-003 and SPEC-007).

4. **External EGRESS semantics**  
   - How exactly NAP EGRESS envelopes are consumed by external systems, including format guarantees and buffering.  
   - May warrant a future IO-focused spec if not fully covered by SPEC-003/007.

5. **Performance/throughput constraints**  
   - If the pillar spec calls out throughput or latency requirements for Gate/NAP, we’ll need either:  
     - A performance-focused spec, or  
     - A cluster of tests/benchmarks referenced in this matrix.

---

## 5. Next Steps

For Gate/TBP + NAP/PFNA coverage, next steps once the repo exists:

1. **Add master-spec references**  
   - Add a “Master Spec Ref” column with section/anchor IDs from `trinity gate full spec.txt`, `NAPEnvelope_v1.md`, PFNA schema docs.

2. **Bind tests/fixtures**  
   - Attach each requirement to concrete test modules and fixtures once they exist (e.g. `tests/gate/test_pfna_ingest.py`, `tests/nap/test_layers_ctrl.py`).

3. **Mirror this for remaining pillars**  
   - Codex Eterna and U-ledger pillars need their own coverage matrices, then we can create a global “pillar coverage index” that shows 100% mapping from master specs → SPEC-00X → phases → tests.
