# SPEC-007 — Governance, Budgets & Codex Actioning V1

## Status

- **Spec ID:** SPEC-007  
- **Name:** Governance, Budgets & Codex Actioning V1  
- **Version:** v1 (skeleton)  
- **Phase:** Phase 5  
- **Scope:** Governance configuration, budget engine, Codex proposal lifecycle, governance IO & ledgering  
- **Predecessors:**  
  - SPEC-001-AETHER — Full System Build Plan (Medium-Agnostic)  
  - SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)  
  - SPEC-005 — Phase 2 Pillar V1 Implementation Plan  
  - SPEC-003 — Gate/TBP & PFNA V0 — External Inputs & Layering  
  - SPEC-004 — Press/APX AEON & APXi — Advanced Grammars & Windows  
  - SPEC-006 — Multi-Graph & Dynamic Topology V1 (SLP, Growth/Prune)  

---

## 1. Purpose & Context

By the end of Phase 4, the engine can:

- Run multiple graphs with dynamic topology (SLP events),  
- Accept external inputs (PFNA V0) and layer them via NAP,  
- Describe behaviour in time using AEON/APXi,  
- Learn motifs & emit proposals via Codex (observer-only),  
- Record everything in a hash-linked U-ledger.

What it **does not** yet have is a way to **decide** which proposed changes are allowed, when, and under what constraints. There is no concept of budgets, policies, or approvals beyond “whatever inputs and SLP events we feed it.”

Phase 5 (SPEC-007) introduces:

> A **governance layer** that controls how Codex proposals and SLP/PFNA actions are accepted, rejected, or delayed, under explicit budget and policy constraints, fully recorded in the U-ledger.

Non-negotiables:

- Governance decisions are **explicit** and **ledgered**.  
- Codex still cannot “silently” act; it can only propose. Governance decides.  
- Budgets and policies are configuration-driven; no hidden hard-coded rules.  
- Determinism holds: given the same inputs and governance config, the same decisions and outcomes must result.

---

## 2. Dependencies & References

### 2.1 Core Specs

- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (SPEC-001-AETHER)  
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (SPEC-002)  
- `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (SPEC-005)  
- `spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md` (SPEC-003)  
- `spec_004_Press_APX_AEON_APXi_Advanced_Grammars_and_Windows.md` (SPEC-004)  
- `spec_006_MultiGraph_Dynamic_Topology_V1.md` (SPEC-006)  
- `spec_000_AETHER_Spec_Index_and_Roadmap.md` (SPEC-000-AETHER)  

### 2.2 Pillar Master Specs

- Trinity Gate pillar: `trinity gate full spec.txt` (governance / policy sections).  
- Codex Eterna pillar: `Codex Eterna — Master spec.txt` (motifs & proposals).  
- Any governance/budget references scattered across pillar masters.  

### 2.3 Contracts & Types

Existing contracts from earlier phases:

- `NAPEnvelope_v1.md` (CTRL layer for governance messages).  
- `SceneFrame_v1.md`  
- `ULedgerEntry_v1.md`  
- `CodexContracts_v1.md` (library entries, proposals).  
- `SLPEvent_v1.md` (from SPEC-006).  
- `GraphProfile_v1.md` (from SPEC-006).  

New / extended contracts for SPEC-007:

- `GovernancePolicy_v1.md` — configuration of rules/policies.  
- `BudgetProfile_v1.md` — limits, quotas, and expiry rules.  
- `GovernanceDecision_v1.md` — records of decisions (accept/reject/defer).  

---

## 3. Scope & Non-Goals

### 3.1 In Scope

- **Governance configuration:**

  - A declarative way to state what Codex and SLP/PFNA actions are allowed.  
  - Policy rules that map proposals/actions → decisions (accept/reject/defer).  

- **Budgets:**

  - Define “budgets” as integer-limited resources (e.g. number of topology changes per period, allowed cost, etc.).  
  - Track budget consumption over time.  

- **Codex proposal lifecycle:**

  - A pipeline from `CodexProposal_v1` → governance evaluation → decision → (if accepted) action.  

- **Governance IO & ledgering:**

  - NAP CTRL messages representing governance events.  
  - U-ledger entries tying proposals, decisions, and actions together.

### 3.2 Out of Scope (Deferred / Future Work)

- Any human UI or external decision tooling (we assume configs + machine-executable policies).  
- Complex game-theoretic or multi-agent governance logic (Phase 5 aims for deterministic, rule-based policies).  
- Automatic policy learning; governance rules are configured, not learned.

SPEC-007 is about **explicit, rule-based control** over changes, not emergent political systems.

---

## 4. Phase 5 Objectives (Governance & Actioning)

### 4.1 Primary Objectives

1. **Governance policies as config**  
   - Express governance rules in declarative configurations that are applied deterministically.

2. **Budgets as integer resources**  
   - Quantify allowed change (e.g. SLP events, PFNA mappings, Codex actions) in integer budgets, enforced over time.

3. **Proposal lifecycle & actioning**  
   - Codex proposals are evaluated under policy and budgets to yield decisions.  
   - Accepted proposals are transformed into SLP events or config changes, with full traceability.

4. **Full governance traceability**  
   - Every decision (accept/reject/defer) is visible in NAP CTRL layer and U-ledger, with links to inputs and outputs.

### 4.2 Success Criteria (High Level)

- At least one Phase 5 demo scenario where:

  - Codex proposes multiple changes.  
  - Governance accepts some, rejects others, and defers or blocks some based on budgets/policies.  
  - The resulting SLP changes and system behaviour are fully traceable.

- Deterministic: given the same run, PFNA inputs, Codex outputs, and governance config, the same decisions and resulting run occur every time.

---

## 5. Epics & Workstreams — Phase 5

We’ll use **P5.x** epic numbering for Phase 5.

### EPIC P5.1 — Governance Model & Policy Config

**Intent:** Define governance policies as clear, declarative configurations.

**Key outcomes:**

- `GovernancePolicy_v1` contract.  
- Policy evaluation engine.

Core themes:

- Design `GovernancePolicy_v1`:

  - Policy scopes: per-graph, per-run, global.  
  - Rules keyed by: proposal type, graph ID, SLP event type, budget class, etc.  
  - Actions: allow, deny, require manual override flag, etc.  

- Implement policy evaluation:

  - Given a proposal or requested action, determine the preliminary decision **before** budgets and other considerations.  
  - Ensure no ambiguity: conflicts resolved by explicit priority rules.

- Tests:

  - Synthetic policies applied to test proposals, verifying decisions are deterministic and match expectations.

---

### EPIC P5.2 — Budget Engine

**Intent:** Introduce and enforce integer-based budgets over time.

**Key outcomes:**

- `BudgetProfile_v1` contract.  
- Budget tracking and enforcement engine.

Core themes:

- Design `BudgetProfile_v1`:

  - Budget classes (e.g. topology_change_budget, motif_place_budget).  
  - Limits per period (e.g. per run, per 100 ticks, etc.).  
  - Refill / decay rules if applicable (still integer-only).  

- Implement budget tracking:

  - Counters updated when actions are accepted and executed.  
  - Time-based windows using Loom or tick counts to know when budgets reset or change.

- Integrate with policy evaluation:

  - After policy says “allowed in principle”, budgets decide whether it is allowed **now** or must be deferred/rejected.

- Tests:

  - Scenarios where budgets are exhausted, partially used, and refilled.  
  - Deterministic budget evolution given the same sequence of decisions.

---

### EPIC P5.3 — Codex Proposal Lifecycle & Actioning

**Intent:** Wire Codex proposals through governance into actual system changes (or rejections).

**Key outcomes:**

- End-to-end pipeline from `CodexProposal_v1` → decision → SLP events / config changes.  
- Clear status updates for proposals.

Core themes:

- Proposal ingestion:

  - Collect proposals per run, per graph, etc. from CodexContext.  
  - Identify which proposals are actionable (according to type).  

- Governance evaluation:

  - For each proposal, apply policies and budgets.  
  - Produce `GovernanceDecision_v1` records with reasons (which rule/budget triggered decision).  

- Actioning accepted proposals:

  - Transform accepted proposals into SLP events, configuration changes, or other discrete actions.  
  - Ensure actions follow the same deterministic rules as manually configured SLP events / inputs.

- Status updates:

  - Proposals carry statuses: PENDING → ACCEPTED / REJECTED / DEFERRED.  
  - Status changes recorded via NAP CTRL messages and ledger entries.

- Tests:

  - Test runs where Codex proposes various changes and governance filters them.  
  - Verify only accepted proposals trigger SLP events and structural changes.

---

### EPIC P5.4 — Governance IO & U-ledger Traceability

**Intent:** Ensure governance decisions and effects are fully observable and reconstructable.

**Key outcomes:**

- Governance messages in NAP CTRL layer.  
- U-ledger entries linking proposals, decisions, and actions.

Core themes:

- NAP CTRL integration:

  - Define NAP CTRL message types for governance events (policy load, decision, budget updates).  
  - Use SceneFrames to capture governance events alongside “normal” ticks.

- Ledger integration:

  - Extend ULedgerEntry or add companion governance records:  
    - Hashes/IDs for proposals, decisions, applied SLP events.  
    - Budget snapshots if needed (to reconstruct budget state over time).  

- Replay and audit:

  - Given ledger and configs, reconstruct:  
    - Why a proposal was accepted or rejected.  
    - What budgets were at the moment of decision.  
    - What structural or parameter changes resulted.

- Tests:

  - Simple audit scenarios: “show me why graph X has this structure” and verify the engine can reconstruct a minimal proof trail.

---

## 6. Testing & Determinism (Governance)

SPEC-007 continues the determinism theme:

- Policies and budgets must be evaluated in a fixed, documented order.  
- No random tie-breaking; all tie-breaking rules are explicit and deterministic.  
- Governance decisions are reproducible from configs and logs alone.

Snapshot tests:

- At least one full governance-driven scenario must have a snapshot capturing proposals, decisions, actions, and resulting structure.  
- Re-running with the same inputs and configs must match the snapshot byte-for-byte.

---

## 7. Repo Placement & Planning

When implemented:

- This spec lives at:  
  `docs/specs/spec_007_Governance_Budgets_Codex_Actioning_V1.md`

- A corresponding planning file (GitHub issue pack) should live at:  
  `docs/planning/spec_007_Governance_Budgets_Codex_Actioning_V1_Issues.md`

The planning pack will mirror the pattern of SPEC-002 and SPEC-005: epics → issue stubs → GitHub issues.

---

## 8. End-State & Forward Relations

Once SPEC-007 is implemented and tested, the system reaches its first **governed, self-modifying** stage:

- Pillars implement their master specs (UMX, Loom, Press, Gate/TBP, Codex, U-ledger).  
- External inputs and dynamic topology are possible but constrained by governance and budgets.  
- Codex can propose, but only governance can approve and enact changes.  
- Every decision and change is recorded in the ledger, with enough information to reconstruct “who/what/when/why”.

Beyond SPEC-007, future work can focus on:

- Richer governance models (e.g. multiple policy layers, human-in-the-loop overrides).  
- More advanced Codex modelling and learning.  
- Performance and scaling work, given that the behavioural foundations and safety rails are already in place.
