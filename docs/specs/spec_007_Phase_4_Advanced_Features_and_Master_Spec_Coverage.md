# SPEC-007 — Phase 4 Advanced Features & Master Spec Coverage

## Status

- **Spec ID:** SPEC-007
- **Name:** Phase 4 Advanced Features & Master Spec Coverage
- **Version:** v1
- **Scope:** Advanced Press/APX (AEON/APXi, MDL placement), dynamic topology & SLP, full Gate/TBP, Codex active mode, multi-graph/engine scaling
- **Assumes:**
  - SPEC-005 (Phase 2 Pillar V1 Implementation Plan) is implemented.
  - SPEC-006 (Governance, Config & Ops) is implemented.
  - All GF-01 and Phase 2/3 scenarios are green and stable.

---

## 1. Purpose & End-State

SPEC-007 describes **Phase 4**, whose goal is:

> Bring the codebase to full coverage of the *normative behaviours* described in the master pillar specs, within the Aether v1 scope.

That means:

- Press/APX implements the AEON/APXi grammars and placement/MDL constraints described in the Astral Press pillar spec.
- UMX supports dynamic topology via SLP operations, under conservation and MDL barriers.
- Gate/TBP supports the full range of ingress/egress and PFNA/TBP interactions required for v1.
- Codex moves from observer-only to **active mode**, able to propose and apply structural changes via governance.
- The engine can run and coordinate multiple graphs/engines in one universe, as per the system-level master spec.

This is the “100% coverage of master specs” phase at the conceptual level; further extensions would be v2+.

---

## 2. Reference Documents

- Pillar master specs:
  - Trinity Gate / TBP master spec
  - Astral Press pillar master spec
  - Aevum Loom pillar master spec
  - Universal Matrix pillar master spec
  - Codex Eterna pillar master spec
- System- or universe-level specs:
  - Full Aether system spec (if distinct from pillar specs)
- Contracts:
  - `APXManifest_v1.md` (may require extensions for AEON/APXi),
  - `CodexContracts_v1.md`,
  - `TopologyProfile_v1.md` (for SLP operations),
  - `ULedgerEntry_v1.md`,
  - `NAPEnvelope_v1.md`,
  - others as needed.

Any new contracts introduced in this phase should be added under `docs/contracts/` and referenced here.

---

## 3. EPIC P4.1 — Advanced Press/APX (AEON/APXi & MDL Placement)

### 3.1 Epic Goal

Implement the full Press/APX feature set required by the Astral Press pillar spec, including:

- AEON/APXi grammatical descriptions for streams,
- MDL-based placement and scheme selection across multiple pillars,
- Detailed accounting of model vs residual vs control bits,
- Tight integration with Codex and U-ledger.

### 3.2 Dependencies

- Press/APX V1 from SPEC-005,
- Config & metrics from SPEC-006,
- Astral Press pillar master spec.

### 3.3 Issues / Work Items

#### Issue P4.1.1 — AEON/APXi Grammar Representation

**Goal:** Represent AEON/APXi grammars in a concrete, machine-readable way.

**Tasks:**

- [ ] Define data structures/contracts for:
  - AEON grammar definitions,
  - APXi instances bound to specific streams or stream groups.
- [ ] Provide a way to:
  - Load grammars from spec-like config files,
  - Validate them.

**Acceptance Criteria:**

- [ ] At least one non-trivial AEON/APXi grammar from the Astral Press spec is represented faithfully in code.

---

#### Issue P4.1.2 — Grammar Interpreter & MDL Accounting

**Goal:** Implement an interpreter for AEON/APXi grammars that:

- Applies a grammar to streams,
- Computes MDL contributions as per the spec.

**Tasks:**

- [ ] Implement grammar evaluation over:
  - Single streams,
  - Groups of related streams (e.g. state deltas + fluxes).
- [ ] Compute:
  - `L_model`, `L_residual`, `L_control` (if defined),
  - MDL-based placement costs.
- [ ] Integrate results into `APXManifest_v1` (or a v2 contract if necessary).

**Acceptance Criteria:**

- [ ] For at least one worked example from the Astral Press spec, the implementation reproduces the described MDL breakdown.

---

#### Issue P4.1.3 — Placement Across Pillars

**Goal:** Implement a first pass at **placement** decisions across Press, UMX, Loom, Codex.

**Tasks:**

- [ ] Define how placement decisions are represented (e.g. as Codex proposals, APX hints).
- [ ] Implement logic that:
  - Uses MDL stats to suggest placement (e.g. in UMX vs Press),
  - Emits proposals without necessarily applying them (tie-in with Codex).
- [ ] Tests:
  - Confirm that placement suggestions are consistent for given scenarios.

**Acceptance Criteria:**

- [ ] Placement hints and MDL stats are produced deterministically and match pillar spec descriptions for at least one example.

---

## 4. EPIC P4.2 — Dynamic Topology & SLP in UMX

### 4.1 Epic Goal

Extend UMX from a fixed-topology engine to a dynamic one that supports:

- SLP (Structure Learning Process) operations,
- Topology growth and pruning,
- All under conservation and MDL barriers.

### 4.2 Dependencies

- UMX V1 from SPEC-005,
- Codex V1 (observer mode),
- Universal Matrix pillar master spec,
- Codex Eterna pillar spec (for SLP concepts).

### 4.3 Issues / Work Items

#### Issue P4.2.1 — SLP Representation & Operations

**Goal:** Represent SLP operations abstractly and implement primitives.

**Tasks:**

- [ ] Define SLP operation types (e.g. `ADD_EDGE`, `REMOVE_EDGE`, `MERGE_NODE`, `SPLIT_NODE`) in contracts.
- [ ] Implement functions to:
  - Apply these operations to `TopologyProfile_v1`,
  - Validate before/after topologies,
  - Maintain invariants (e.g. no orphan nodes, degree constraints if any).

**Acceptance Criteria:**

- [ ] SLP operations can be applied to a running topology in a test scenario without violating invariants.

---

#### Issue P4.2.2 — Conservation & MDL Constraints on SLP

**Goal:** Ensure SLP changes respect conservation and MDL constraints.

**Tasks:**

- [ ] Define constraints from pillar specs (e.g. energy/flux conservation, MDL improvement conditions).
- [ ] Implement checks so that:
  - SLP operations are only accepted if they improve or maintain required metrics.
  - Violating operations are rejected or only logged as hypothetical.

**Acceptance Criteria:**

- [ ] Test scenarios where:
  - Beneficial SLP operations are accepted,
  - Harmful ones are rejected,
  - Behaviour matches spec descriptions.

---

#### Issue P4.2.3 — Dynamic Run Support & Snapshots

**Goal:** Allow runs that change topology over time and still have reproducible snapshots.

**Tasks:**

- [ ] Extend run config to include SLP policies (when and how often changes are allowed).
- [ ] Ensure Loom, Press, Codex, and U-ledger can track and log topology changes.
- [ ] Provide snapshot/replay support for dynamic topologies.

**Acceptance Criteria:**

- [ ] At least one dynamic-topology scenario is fully reproducible, including SLP actions and resulting states.

---

## 5. EPIC P4.3 — Full Gate/TBP (PFNA & Time-Basis Bridge)

### 5.1 Epic Goal

Elevate Gate/TBP from a minimal V1 to the full v1 behaviour described in the Trinity Gate / TBP pillar spec, including:

- PFNA structures for external inputs,
- Time-basis bridges (classical/quantum if applicable),
- Rich NAP layering for scenes.

### 5.2 Dependencies

- Gate/TBP V1 from SPEC-005,
- PFNA/TBP definitions from the pillar spec,
- NAPEnvelope and SceneFrame contracts.

### 5.3 Issues / Work Items

#### Issue P4.3.1 — PFNA Schema & Handling

**Goal:** Define and implement PFNA representations for external inputs.

**Tasks:**

- [ ] Translate PFNA definitions from the pillar spec into contracts.
- [ ] Implement:
  - PFNA parsing from fixtures or live sources,
  - Mapping from PFNA to internal state changes (e.g. initial conditions, parameter tweaks).

**Acceptance Criteria:**

- [ ] At least one scenario that uses PFNA inputs to drive a run, in line with pillar spec.

---

#### Issue P4.3.2 — Time-Basis Bridge (TBP) Integration

**Goal:** Implement TBP behaviour for time-basis transformations.

**Tasks:**

- [ ] Represent TBP configuration and modes (classical/quantum views as per spec).
- [ ] Implement transformations that:
  - Respect deterministic constraints,
  - Link external time sources to Loom and Gate.

**Acceptance Criteria:**

- [ ] A test scenario demonstrates TBP effects on timing or sequencing in a controlled way.

---

#### Issue P4.3.3 — Rich Scene & NAP Layering

**Goal:** Enable complex scene definitions and multi-layer NAP flows.

**Tasks:**

- [ ] Extend `SceneFrame_v1` and/or related contracts (if needed) to support:
  - Multiple NAP streams per tick,
  - Layered semantics as per pillar spec.
- [ ] Implement Gate logic that:
  - Routes different data types to different layers/modes in NAP.
- [ ] Tests for:
  - Multi-layer envelope flows in a scenario resembling spec examples.

**Acceptance Criteria:**

- [ ] Rich scene/NAP behaviour in code matches at least one worked example from the Trinity Gate / TBP pillar spec.

---

## 6. EPIC P4.4 — Codex Active Mode (Governance & Structural Changes)

### 6.1 Epic Goal

Move Codex from observer-only to **active mode** where:

- Proposals can be submitted as NAP transactions,
- A governance module can accept or reject them,
- Accepted proposals can change UMX, Press, Loom configs (and possibly topology),
- All changes are recorded via U-ledger.

### 6.2 Dependencies

- Codex V1 from SPEC-005,
- U-ledger from SPEC-005,
- Governance/ops framework from SPEC-006,
- Codex pillar spec.

### 6.3 Issues / Work Items

#### Issue P4.4.1 — Proposal Transactions via NAP

**Goal:** Represent Codex proposals as NAP transactions.

**Tasks:**

- [ ] Define NAP payload schema for proposals (referencing `CodexProposal_v1`).
- [ ] Implement Gate/TBP logic to:
  - Accept proposal envelopes,
  - Route them to a governance module.

**Acceptance Criteria:**

- [ ] Proposals emitted by Codex can be re-ingested as NAP envelopes and recognised as such.

---

#### Issue P4.4.2 — Governance Module

**Goal:** Implement governance logic to accept/reject proposals.

**Tasks:**

- [ ] Define a governance policy mechanism drawing from:
  - MDL gains,
  - Safety constraints (e.g. conservation, stability),
  - Human override if desired.
- [ ] Implement a governance engine that:
  - Consumes proposals,
  - Decides `accept` / `reject` / `defer`,
  - Logs decisions via U-ledger and logs.

**Acceptance Criteria:**

- [ ] Test scenarios where:
  - Some proposals are accepted and applied,
  - Others are rejected or deferred,
  - Decisions match spec/policy configuration.

---

#### Issue P4.4.3 — Applying Structural Changes Safely

**Goal:** Apply accepted proposals to live configs/topologies.

**Tasks:**

- [ ] Implement mechanisms to:
  - Apply UMX topology changes (via SLP ops),
  - Adjust Press/APX configs or schemes,
  - Tune Loom or Gate parameters,
  - All under deterministic rules.
- [ ] Provide roll-back or checkpoint mechanisms, if required by pillar spec.

**Acceptance Criteria:**

- [ ] A scenario shows Codex proposing, governance accepting, and the engine updating its structure/config without breaking determinism or conservation.

---

## 7. EPIC P4.5 — Multi-Graph & Multi-Engine Scaling

### 7.1 Epic Goal

Support multiple UMX engines (graphs) and potentially multiple universes/runs interacting in a coordinated way, as per the system-level master spec.

### 7.2 Dependencies

- UMX V1 + SLP (EPIC P4.2),
- Loom, Press, Gate, Codex, U-ledger V1,
- System-level/master specs for multi-graph behaviour.

### 7.3 Issues / Work Items

#### Issue P4.5.1 — Multi-Engine Orchestrator

**Goal:** Implement an orchestrator for multiple engines.

**Tasks:**

- [ ] Define a structure representing:
  - Multiple `UMXRunContext`s,
  - Shared or separate Loom/Press contexts,
  - Interactions (if any) between graphs.
- [ ] Implement a scheduler that:
  - Steps multiple engines in a defined order,
  - Maintains determinism.

**Acceptance Criteria:**

- [ ] Test scenario with at least two independent graphs being run in one process, with reproducible results.

---

#### Issue P4.5.2 — Cross-Graph Interactions

**Goal:** Implement basic cross-graph interactions if described in the master spec.

**Tasks:**

- [ ] Define mechanisms (possibly via Gate/TBP and NAP) to:
  - Pass signals or envelopes between graphs,
  - Maintain causality and determinism.
- [ ] Tests:
  - Scenarios where one graph influences another through defined channels.

**Acceptance Criteria:**

- [ ] Cross-graph interactions behave as described in the system-level spec and remain reproducible.

---

#### Issue P4.5.3 — U-ledger Integration for Multi-Graph

**Goal:** Extend U-ledger to handle multiple graphs/universes.

**Tasks:**

- [ ] Decide whether:
  - A single unified ledger is used,
  - Or one ledger per graph with an overarching meta-ledger.
- [ ] Implement ledger extensions accordingly.
- [ ] Tests:
  - Verify consistent hash chaining and referencing across multiple graphs.

**Acceptance Criteria:**

- [ ] Multi-graph ledger behaviour is well-defined and deterministic.

---

## 8. Completion Criteria for SPEC-007

SPEC-007 is considered **complete** when:

1. Each EPIC (P4.1–P4.5) has been implemented, with:
   - Issues closed,
   - Tests passing,
   - Metrics/logs confirming behaviour.

2. For each pillar:
   - The implementation can demonstrate the key behaviours required in its master pillar spec (within v1 scope),
   - Representative worked examples from the specs are reproducible in code.

3. For the system as a whole:
   - There exist one or more scenarios that:
     - Use advanced Press/APX,
     - Exercise dynamic topology (SLP),
     - Use PFNA/TBP for external input and time,
     - Allow Codex to propose and apply structural changes under governance,
     - Potentially involve multi-graph runs,
   - And all of the above remain deterministic and inspectable via logs, metrics, introspection, and U-ledger.

At that point, Aether v1 is “feature-complete” relative to the current master specs. Further work would be framed as v2+ or separate research projects.

---

## 9. Out-of-Scope for SPEC-007

- Any fundamentally new pillar or subsystem not present in the current master specs.
- Hardware-specific optimisations or deployments (GPU/FPGA, etc.).
- Full-blown distributed or networked deployments (beyond multi-engine in a single process/universe).

SPEC-007’s role is to bridge the gap between the **Pillar V1 implementations** and **full v1 spec coverage** for the existing Aether design.
