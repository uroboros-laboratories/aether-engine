# SPEC-006 — Multi-Graph & Dynamic Topology V1 (SLP, Growth/Prune)

## Status

- **Spec ID:** SPEC-006  
- **Name:** Multi-Graph & Dynamic Topology V1 (SLP, Growth/Prune)  
- **Version:** v1 (skeleton)  
- **Phase:** Phase 4  
- **Scope:** UMX multi-graph runtime, dynamic topology events (SLP), Loom & U-ledger integration, Gate-level routing  
- **Predecessors:**  
  - SPEC-001-AETHER — Full System Build Plan (Medium-Agnostic)  
  - SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)  
  - SPEC-005 — Phase 2 Pillar V1 Implementation Plan  
  - SPEC-003 — Gate/TBP & PFNA V0 — External Inputs & Layering  
  - SPEC-004 — Press/APX AEON & APXi — Advanced Grammars & Windows  

---

## 1. Purpose & Context

By the end of Phase 3, the engine can:

- Run **one graph per run** with Pillar V1 (UMX, Loom, Press, Gate, Codex, U-ledger),  
- Accept external integer inputs via PFNA V0 (SPEC-003),  
- Describe behaviour across multiple time scales with AEON/APXi (SPEC-004).  

What it still does **not** do is treat topology itself as a first-class, evolving object. The graph is static during a run; structural changes require manual reconfig or out-of-band intervention.

Phase 4 (SPEC-006) changes that:

> Introduce a **multi-graph, dynamic topology runtime** where graphs can be created, grown, pruned, and related to each other in a governed, deterministic way (without yet enforcing budgets or governance policies — those come in SPEC-007).

This is the “SLP” layer: a space where:

- Multiple UMX instances (“graphs”) coexist,  
- Topology changes are expressed as **events** (add/remove nodes/edges, spawn/merge graphs),  
- Loom and U-ledger keep track of these events over time,  
- Gate/TBP can route inputs and outputs between graphs.

Non-negotiables:

- All topology changes are explicit **events**, not hidden side effects.  
- The system remains integer-only and deterministic.  
- GF-01 and other Phase 2/3 scenarios continue to work unmodified when run in “static topology mode”.  

---

## 2. Dependencies & References

### 2.1 Core Specs

- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (SPEC-001-AETHER)  
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (SPEC-002)  
- `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (SPEC-005)  
- `spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md` (SPEC-003)  
- `spec_004_Press_APX_AEON_APXi_Advanced_Grammars_and_Windows.md` (SPEC-004)  
- `spec_000_AETHER_Spec_Index_and_Roadmap.md` (SPEC-000-AETHER)  

### 2.2 Pillar Master Specs

- UMX pillar master spec: `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`  
- Aevum Loom pillar master spec: `Aevum Loom Pillar — Master spec.txt`  
- Trinity Gate pillar spec: `trinity gate full spec.txt`  
- Codex Eterna pillar spec: `Codex Eterna — Master spec.txt`  
- Any SLP / topology-evolution sections embedded in these pillars.  

### 2.3 Contracts & Types

Existing contracts from Phases 1–3:

- `TopologyProfile_v1.md`  
- `Profile_CMP0_v1.md`  
- `UMXTickLedger_v1.md`  
- `LoomBlocks_v1.md`  
- `APXManifest_v1.md`  
- `NAPEnvelope_v1.md`  
- `SceneFrame_v1.md`  
- `TickLoop_v1.md`  
- `ULedgerEntry_v1.md`  
- `CodexContracts_v1.md`  
- `AEONWindowGrammar_v1.md`  
- `APXiDescriptor_v1.md`  
- `PFNA_V0_Schema_v1.md` (from SPEC-003)  

New / extended contracts expected for SPEC-006:

- `SLPEvent_v1.md` — defines topology change events.  
- `GraphProfile_v1.md` — metadata for individual graphs / engines.  
- Possible extensions to `ULedgerEntry_v1` and `SceneFrame_v1` to carry multi-graph context.

---

## 3. Scope & Non-Goals

### 3.1 In Scope

- **Multi-graph runtime:**

  - Ability to keep multiple UMXRunContexts alive in one run.  
  - Basic registry of graphs (graph IDs, profiles, topology profiles).  

- **Dynamic topology (SLP events):**

  - Schema for structural events: create graph, delete graph, add/remove node, add/remove edge, adjust parameters.  
  - Deterministic application of events to graphs.  

- **Loom & U-ledger integration:**

  - Recording SLP events in Loom chains and U-ledger entries.  
  - Ability to replay runs including topology changes.  

- **Gate/TBP routing:**

  - SceneFrames and NAP envelopes extended to reference graph IDs.  
  - Gate can route PFNA inputs to specific graphs or SLP events based on configuration.

### 3.2 Out of Scope (Deferred)

- Governance and budgets over SLP events (which changes are *allowed* and how often) — handled by SPEC-007.  
- Complex cross-graph semantics (e.g. “physics” of interaction between graphs beyond simple data passing).  
- Any probabilistic topological changes — Phase 4 remains fully deterministic.

SPEC-006 is about **making dynamic topology possible and traceable**, but not yet “intelligent” or governed.

---

## 4. Phase 4 Objectives (Multi-Graph & SLP)

### 4.1 Primary Objectives

1. **Multi-graph UMX runtime**  
   - Multiple UMXRunContexts can exist and step in a coordinated tick loop.

2. **Topology-as-events (SLP)**  
   - All structural changes are captured as SLPEvent_v1 records and applied deterministically.

3. **Loom & U-ledger awareness**  
   - Time axis and ledger include topology change events; replay recovers both state and structure.

4. **Gate/TBP routing & addressing**  
   - Inputs and outputs can target specific graphs and events via graph IDs and routing rules.

### 4.2 Success Criteria (High Level)

- At least one Phase 4 demo scenario where:

  - A graph starts small and grows (adding nodes/edges) during the run.  
  - Another scenario where a graph is pruned or split.  
  - All changes are visible and reproducible via U-ledger and Loom replay.  

- GF-01 and earlier static scenarios run unchanged when no SLP events are configured (backwards compatibility).

---

## 5. Epics & Workstreams — Phase 4

We’ll use **P4.x** epic numbering for Phase 4.

### EPIC P4.1 — Multi-Graph Runtime & Registry

**Intent:** Support managing multiple UMX graphs in a single run with a central registry.

**Key outcomes:**

- A graph registry with unique graph IDs and metadata.  
- Tick loop capable of stepping multiple UMXRunContexts per tick.

Core themes:

- Design `GraphProfile_v1`:

  - Fields: `gid`, topology reference, profile reference (e.g. CMP-0), optional tags.  
  - Versioning / status (active, inactive, etc.).  

- Implement a **graph registry**:

  - Functions to add/remove graphs.  
  - Lookup by `gid`.  
  - Integration with existing run configs.

- Extend TickLoop:

  - For each tick, step all active graphs (or a configured subset).  
  - Collect per-graph UMX, Loom, Press outputs and wrap with multi-graph SceneFrames.

- Tests:

  - Simple multi-graph scenario (e.g. two static graphs running in parallel).  
  - Deterministic behaviour and ordering for stepping multiple graphs.

---

### EPIC P4.2 — SLP Events & Dynamic Topology

**Intent:** Represent and apply topology changes as explicit SLP events.

**Key outcomes:**

- `SLPEvent_v1` contract.  
- Deterministic application of events to topologies.

Core themes:

- Define `SLPEvent_v1`:

  - Event types: `CREATE_GRAPH`, `DELETE_GRAPH`, `ADD_NODE`, `REMOVE_NODE`, `ADD_EDGE`, `REMOVE_EDGE`, `UPDATE_PARAM`, etc.  
  - Fields for timestamps/ticks, graph IDs, and parameters.  

- Event application engine:

  - Given an SLPEvent sequence, apply changes to a graph registry and individual topologies.  
  - Ensure all invariants and validations from `TopologyProfile_v1` are re-checked after changes.

- Integration with UMX:

  - Rebuild or adjust TopologyProfile in UMXRunContext when events occur.  
  - Handle transitions cleanly between ticks (e.g. changes happen between ticks, not mid-step).

- Tests:

  - Add/remove nodes and edges in small graphs over time, verifying that:  
    - UMX stepping uses updated topologies.  
    - No illegal states (e.g. edges pointing to non-existent nodes) appear.

---

### EPIC P4.3 — Loom & U-ledger Integration for SLP

**Intent:** Extend Loom and U-ledger so topology events are part of the recorded and replayed history.

**Key outcomes:**

- Topology events appear in Loom chains / blocks.  
- U-ledger entries reference SLP events and graph profiles.

Core themes:

- Loom integration:

  - Decide how SLP events influence chain updates (e.g. special s_t contributions or flags).  
  - Ensure I-blocks capture snapshots of topology as well as state for affected graphs.

- U-ledger integration:

  - Extend ULedgerEntry fields to include references/hashes of SLPEvent_v1 sequences at or before each tick/window.  
  - Canonical serialisation of SLP events and graph profiles.

- Replay:

  - `replay_state_at(t)` extended to:  
    - Reconstruct active graphs and their topologies at t.  
    - Then replay UMX state from nearest chain/graph checkpoint.

- Tests:

  - Scenario with multiple SLP events; verify:  
    - Replay reconstructs both structure and state identically.  
    - Ledger chains are stable across runs.

---

### EPIC P4.4 — Cross-Graph Relationships & Routing

**Intent:** Allow simple relationships and routing between graphs (without full governance yet).

**Key outcomes:**

- Ability to express that one graph’s outputs feed another’s inputs.  
- Routing rules visible and deterministically applied.

Core themes:

- Relationship contracts:

  - Simple links like `GRAPH_A → GRAPH_B` with mapping rules (which states or fluxes are shared).  
  - Possibly a `GraphLink_v1` structure describing mapping of quantities.

- Gate/TBP routing extensions:

  - SceneFrames and NAP envelopes carry graph IDs and maybe link IDs.  
  - Gate configurations define which PFNA inputs go to which graph or link event.

- Tests:

  - A small scenario where one graph drives another via a simple mapping.  
  - Deterministic behaviour and full U-ledger trace of routing decisions.

---

## 6. Testing & Determinism (Multi-Graph & SLP)

SPEC-006 inherits all determinism requirements from previous specs and adds:

- **SLP ordering:** Event ordering must be completely deterministic and unambiguous.  
- **Multi-graph stepping order:** When multiple graphs are stepped per tick, the order must be fixed by configuration and documented.  
- **Snapshot coverage:** At least one multi-graph / SLP scenario must have a snapshot in tests for full replay verification.

Any changes to SLP or multi-graph logic must surface as ledger/snapshot changes, not invisible internal differences.

---

## 7. Repo Placement & Planning

When implemented:

- This spec lives at:  
  `docs/specs/spec_006_MultiGraph_Dynamic_Topology_V1.md`

- A corresponding planning file (GitHub issue pack) should live at:  
  `docs/planning/spec_006_MultiGraph_Dynamic_Topology_V1_Issues.md`

Planning for SPEC-006 will mirror SPEC-002/005: epics → issue stubs → GitHub issues.

---

## 8. Forward Relations

- **Upstream:** SPEC-006 depends on Pillar V1 (SPEC-005) and Phase 3 (SPEC-003/004) being stable.  
- **Downstream:** SPEC-007 (Governance, Budgets & Codex Actioning V1) will regulate SLP events and cross-graph changes, using the machinery introduced here.

SPEC-006’s job is to make topological change **possible, explicit, and replayable** — governance comes next.
