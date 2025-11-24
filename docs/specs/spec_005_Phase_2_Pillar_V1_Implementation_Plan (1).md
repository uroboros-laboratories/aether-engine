# SPEC-005 — Phase 2 Pillar V1 Implementation Plan

## Status

- **Spec ID:** SPEC-005  
- **Name:** Phase 2 — Pillar V1 Generalisation  
- **Version:** v1 (draft)  
- **Scope:** UMX V1, Loom V1, Press/APX V1, Gate/TBP V1, U-ledger V1, Codex V1 (observer-only)  
- **Predecessors:**  
  - SPEC-001-AETHER — Full System Build Plan (Medium-Agnostic)  
  - SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)  
- **Related Planning:**  
  - `docs/planning/spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md`  
  - `docs/planning/spec_005_Phase2_Pillar_V1_GitHub_Issues.md`  

---

## 1. Purpose & Context

Phase 1 (SPEC-002) delivered a **single, closed-form baseline**:

- One graph: **GF-01**  
- One profile: **CMP-0**  
- One run: **ticks 1–8**  
- Exact parity with the paper GF-01 V0 tables and APX sheets.  

That baseline proves the pillars can cooperate correctly in the simplest possible setting.

Phase 2 (SPEC-005) takes that baseline and turns it into a **small, reusable general engine**:

- Multiple topologies, not just GF-01.
- Clean “run contexts” per pillar instead of GF-01-specific wiring.
- Proper time axis and replay via Loom.
- Reusable Press/APX with a minimal set of schemes and a stream registry.
- A universal ledger (U-ledger) with canonical hashes and entries per tick/window.
- Codex Eterna wired in as a **read-only observer** that can learn motifs and emit proposals.

The non‑negotiable constraint:

> **Nothing in Phase 2 is allowed to break the GF-01 baseline.**  
> SPEC-002’s GF-01 exam remains green throughout.

This spec defines the **shape and boundaries** of Phase 2. Concrete work items and GitHub issues live in the Phase 2 issue pack.

---

## 2. Dependencies & References

### 2.1 Core Aether Specs

- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (SPEC-001-AETHER)  
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (SPEC-002)  
- `spec_000_AETHER_Spec_Index_and_Roadmap.md` (SPEC-000-AETHER, spec index & roadmap)  

### 2.2 Pillar Master Specs

UMX pillar:

- `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`  

Aevum Loom pillar:

- `Aevum Loom Pillar — Master spec.txt`  

Astral Press pillar:

- `astral_press_master_implementation_spec_combined_v1.md`  

Trinity Gate / TBP pillar (incl. PFNA & NAP):

- `trinity gate full spec.txt`  

Codex Eterna pillar:

- `Codex Eterna — Master spec.txt`  

### 2.3 Contracts & Run Specs

Contracts (v1) — expected under `docs/contracts/`:

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

Run / fixture docs:

- `GF01_V0_Exam.md`  
- GF-01 PDFs and mirrors under `docs/fixtures/gf01/`  

### 2.4 Planning Docs

- `docs/planning/spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md`  
- `docs/planning/spec_005_Phase2_Pillar_V1_GitHub_Issues.md` (Phase 2 issue pack)  

---

## 3. Scope & Non‑Goals

### 3.1 In Scope for Phase 2

UMX (Universal Matrix):

- Multi-topology support (loader & validator for `TopologyProfile_v1`).  
- `UMXRunContext` abstraction for clean multi-run, multi-topology operation.  
- CMP-0 stepping refactored to be fully general across topologies.  
- Optional diagnostics / invariant checks (e.g. conservation checks) that do not alter behaviour.

Loom (Aevum):

- `LoomRunContext` linked to UMX runs.  
- Configurable I-block spacing `W` and simple alternative `s_t` rules.  
- Replay API: `get_chain_at(t)`, `replay_state_at(t)` via I-block + re-run.

Press / APX (Astral Press):

- `PressWindowContext` & stream registry for multiple streams per window.  
- Three schemes: **ID**, **R**, and **basic GR**.  
- Generalised `APXManifest_v1` that supports mixed schemes and many streams.  

Gate / TBP (incl. NAP / PFNA placeholder):

- `SceneFrame_v1` as the canonical per-tick integration object.  
- NAP layers/modes extended beyond DATA/P (at least CTRL added in principle).  
- PFNA **placeholder** path for deterministic external integer inputs.

U-ledger:

- Canonical serialisation (JSON) for core records.  
- Fixed hash function (e.g. SHA-256) and hash utilities.  
- `ULedgerEntry_v1` construction per tick/window with a hash chain.

Codex Eterna:

- `CodexContext` as a **read-only** observer.  
- Simple deterministic motif identification heuristics.  
- Proposal emission as `CodexProposal_v1` records, not yet actioned.

### 3.2 Explicit Non‑Goals (Deferred to Later Specs)

The following are explicitly out of scope for SPEC-005 and will be handled by later specs:

- Full PFNA design, grammars, and hardware‑level integration (SPEC-003).  
- AEON window grammars and APXi advanced description systems (SPEC-004).  
- Multi-graph runtime and dynamic topology (SLP, growth/prune) (SPEC-006).  
- Governance, budgets, and Codex‑driven structural changes (SPEC-007).  

Phase 2 is about turning the **GF-01 demo engine** into a **small but real engine**, not about opening the whole outer world or letting Codex make changes on its own.

---

## 4. Phase 2 Objectives & Success Criteria

### 4.1 Primary Objectives

1. **Generalise the pillars**  
   The UMX, Loom, Press, Gate/TBP, U-ledger and Codex components must each have a clear “V1” implementation that:

   - Works for GF-01 (as now), and  
   - Works for at least one other small topology or scenario.

2. **Keep GF-01 as golden baseline**  
   All SPEC-002 GF-01 tests must stay green.  
   Phase 2 code should increase flexibility **without** introducing special cases that only work for new graphs.

3. **Introduce stable run contexts**  
   Each pillar gets a minimal run context abstraction (UMXRunContext, LoomRunContext, PressWindowContext, CodexContext, etc.) so that:

   - Multiple runs can coexist in one process.  
   - There is no reliance on global state.  
   - Replay and inspection are easy.

4. **Lift determinism & regression guarantees up to pillar V1 level**  
   SPEC-002 introduced determinism and snapshot tests for GF-01.  
   Phase 2 reuses and extends those patterns so that V1 pillars can be updated safely.

### 4.2 Success Criteria (High-Level)

Phase 2 is considered done when:

1. **UMX V1 general engine**  
   - UMX can run GF-01 and at least two additional topologies (e.g. line, ring, star) under CMP-0.  
   - All runs are deterministic & conserve total mass per tick.  

2. **Loom V1 time axis & replay**  
   - Loom can track chains for GF-01 and non-GF-01 runs with configurable `W` and one alternative `s_t` rule.  
   - `replay_state_at(t)` yields states that match the original run exactly.

3. **Press / APX V1**  
   - The original GF-01 APX manifests (8-tick and 2-tick) still match **exactly**.  
   - New scenarios can define extra streams and mix ID/R/GR schemes without code changes in core logic.

4. **Gate / NAP V1**  
   - `SceneFrame_v1` is the single integration object driving NAP envelope creation.  
   - NAP layer/mode semantics can be extended to include at least one CTRL example in tests, while GF-01 remains DATA/P only.

5. **U-ledger V1**  
   - All core artefacts (UMX, Loom, APX, NAP) can be canonically serialised and hashed.  
   - `ULedgerEntry_v1` chains form stable, reproducible histories for at least GF-01 and one additional scenario.

6. **Codex V1 (observer-only)**  
   - Codex can ingest traces, learn at least one motif for GF-01, and emit stable proposals.  
   - Engine behaviour is unchanged by Codex; proposals are advisory only.

---

## 5. Pillar-by-Pillar Phase 2 Goals

### 5.1 Universal Matrix — UMX V1

Goals:

- Lift CMP-0 flux logic into a **topology-agnostic engine**.  
- Embed it into `UMXRunContext` so any scenario can be expressed consistently.

Key outcomes:

- Loader & validator for `TopologyProfile_v1`, including GF-01 and at least two new small examples.  
- UMXRunContext that holds topology, profile, state, tick, and metadata.  
- `step()` and `run_until()` APIs that operate solely on context + contract types.  
- Optional diagnostics that confirm conservation and capture basic invariants.

UMX V1 remains integer-only and absolutely deterministic.

---

### 5.2 Aevum Loom — Loom V1

Goals:

- Treat Loom as the **time axis engine** for any UMX run.  
- Support:

  - Parameterised I-block spacing `W`.  
  - Simple variations of `s_t`.  
  - Replay from I-block checkpoints.

Key outcomes:

- `LoomRunContext` driven either by UMXRunContext or a tick-ledger source.  
- Replay APIs:

  - `get_chain_at(t)`  
  - `replay_state_at(t)`  

- Confirmed chain parity and state parity for GF-01 and at least one non-GF-01 scenario.

---

### 5.3 Astral Press — Press / APX V1

Goals:

- Generalise Press from “two hard-coded GF-01 streams” to a reusable **windowed compression engine**.

Key outcomes:

- `PressWindowContext` for each `(gid, window_id)`, managing multiple named streams.  
- Scheme handlers for ID, R, and basic GR.  
- Generalised `APXManifest_v1` supporting:

  - Many streams,  
  - Mixed schemes,  
  - Deterministic `manifest_check`.

GF-01 remains the hard test: its 8-tick and 2-tick manifests must remain verbatim.

---

### 5.4 Trinity Gate / TBP — Gate & NAP V1

Goals:

- Make `SceneFrame_v1` the **canonical per-tick bundle** and hook NAP envelopes and PFNA placeholder into it.

Key outcomes:

- Tick loop refactored so that:

  - UMX, Loom, Press outputs are assembled into a `SceneFrame_v1` per tick.  
  - NAP envelopes are derived from scene frames, not hand-wired fragments.  

- NAP:

  - DATA/P remains the GF-01 config.  
  - Layers/modes extended so at least one CTRL-example scenario exists.  

- PFNA placeholder:

  - A deterministic path from external integer sequences → PFNA-like structure → Gate → scene state changes.

Full PFNA grammar and hardware integration wait for SPEC-003; Phase 2 just establishes the slot and stub behaviour.

---

### 5.5 Universal Ledger — U-ledger V1

Goals:

- Provide a unified, hash‑linked ledger for runs.

Key outcomes:

- Canonical JSON serialisation rules and helpers.  
- Hash utilities for all core records.  
- `ULedgerEntry_v1` construction logic that:

  - Binds together UMX, Loom, APX, NAP outputs.  
  - Includes `prev_entry_hash` to form a chain.  

The ledger becomes the main place to verify that a run is intact and untouched.

---

### 5.6 Codex Eterna — Codex V1 (Observer-Only)

Goals:

- Attach Codex as an **observer** with:

  - Data ingest,  
  - Motif learning,  
  - Proposal emission,  

but no direct ability to alter the engine.

Key outcomes:

- `CodexContext` that can ingest runs from UMX, Loom, APX, and (optionally) NAP.  
- Motif detection that is deterministic and yields stable `CodexLibraryEntry_v1` records.  
- `CodexProposal_v1` messages generated based on motif usage, with default status `"PENDING"` or `"REJECTED"`.

These proposals will be used later by governance (SPEC-007); Phase 2 only produces them.

---

## 6. Epics & Workstreams (P2.1–P2.6)

This section summarises the Phase 2 epics. Detailed issue lists live in the Phase 2 GitHub issue pack.

### EPIC P2.1 — UMX V1 (General Integer Engine)

**Intent:** Turn the CMP-0 engine into a reusable, multi-topology, multi-run UMX V1.

Main work:

- **P2.1.1** — TopologyProfile loader & validator (multi-topology support).  
- **P2.1.2** — `UMXRunContext` for multi-run support.  
- **P2.1.3** — Generalised CMP-0 tick stepping across topologies.  
- **P2.1.4** — Diagnostics & invariant checks (optional).

Deliverable: A UMX engine that can be pointed at any `TopologyProfile_v1` + `Profile_CMP0_v1` pair and run deterministically.

---

### EPIC P2.2 — Loom V1 (Time Axis & Replay)

**Intent:** Turn Loom into a general time-axis engine with replay.

Main work:

- **P2.2.1** — `LoomRunContext` for time axis & blocks.  
- **P2.2.2** — Configurable I-block spacing & `s_t` rule.  
- **P2.2.3** — Replay API (`get_chain_at`, `replay_state_at`).

Deliverable: Loom that can drive, checkpoint, and replay runs for GF-01 and new scenarios.

---

### EPIC P2.3 — Press/APX V1 (Stream Registry & Modes)

**Intent:** Make Press/APX a reusable compression & description engine.

Main work:

- **P2.3.1** — `PressWindowContext` & stream registry.  
- **P2.3.2** — ID, R, and basic GR schemes.  
- **P2.3.3** — Generalised `APXManifest_v1` generation.

Deliverable: A Press/APX module that can handle multiple streams and schemes in a generic way, while preserving all GF-01 results.

---

### EPIC P2.4 — Gate/TBP V1 (Scenes & Layers)

**Intent:** Standardise per-tick integration using `SceneFrame_v1` and extend NAP & PFNA placeholder.

Main work:

- **P2.4.1** — `SceneFrame_v1` as primary integration object.  
- **P2.4.2** — NAP layers & modes beyond DATA/P.  
- **P2.4.3** — PFNA placeholder for deterministic external inputs.

Deliverable: A Gate/TBP path that clearly separates scene assembly, NAP envelopes, and PFNA handling.

---

### EPIC P2.5 — U-ledger V1

**Intent:** Introduce a stable ledger chain for runs.

Main work:

- **P2.5.1** — Canonical serialisation & hashing.  
- **P2.5.2** — `ULedgerEntry_v1` construction per tick/window.

Deliverable: A reproducible ledger for each run, with hashes chaining entries and capturing all major artefacts.

---

### EPIC P2.6 — Codex V1 (Observer-Only)

**Intent:** Turn Codex into a read-only observer that can learn motifs and propose changes.

Main work:

- **P2.6.1** — `CodexContext` & data ingest.  
- **P2.6.2** — Motif identification (simple heuristics).  
- **P2.6.3** — Proposal emission (observer-only).

Deliverable: Codex that can watch runs, learn repeatable structures, and make deterministic proposals, without yet changing the engine.

---

## 7. Testing & Determinism Guardrails

Phase 2 must carry forward, and extend, the testing and determinism guarantees from SPEC-002.

### 7.1 GF-01 Regression

- All SPEC-002 GF-01 UMX, Loom, Press, NAP, and TickLoop tests must remain unchanged and green.  
- GF-01 snapshot tests remain authoritative; any change requires an explicit snapshot update and review.

### 7.2 New Scenario Tests

Each EPIC must add at least one non-GF-01 scenario:

- UMX: new topologies (line, ring, star).  
- Loom: replay checks for at least one non-GF-01 run.  
- Press: simple synthetic sequences for each scheme.  
- Gate/NAP: at least one scenario using CTRL layers/modes.  
- U-ledger: ledger chains for at least one extra run.  
- Codex: motifs and proposals stable across re-runs.

### 7.3 Determinism Harness Extension

- The determinism harness from SPEC-002 is extended to cover V1 pillars:  
  - Serialisation + hashing must be canonically defined.  
  - Double-run comparison must hold for GF-01 and designated test scenarios.  

Any non-determinism is treated as a defect unless explicitly documented (and even then, should be avoided at this phase).

---

## 8. Implementation & Repo Guidelines

When Phase 2 is implemented in the repository:

- **Docs:**  
  - This file lives at:  
    `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`  
  - Phase 2 issue pack lives at:  
    `docs/planning/spec_005_Phase2_Pillar_V1_GitHub_Issues.md`

- **Structure:**  
  - Each pillar should have a clear place under `src/` (e.g. `src/umx`, `src/loom`, etc.).  
  - Run contexts should live close to their pillar, not as global singletons.  

- **Contracts First:**  
  - Implementations should use the contract documents (`*_v1.md`) as their primary reference.  
  - Any disagreement between code and contract must be resolved by updating one or the other deliberately, not by silent drift.

- **No “hidden” behaviour:**  
  - If a meaningful behaviour emerges that isn’t covered by a spec, either:  
    - Document it and map it to a SPEC-00X, or  
    - Mark it as experimental and plan for removal or formalisation.

---

## 9. Forward Links (Beyond Phase 2)

SPEC-005 ends with:

- A generalised, tested V1 engine for each pillar.  
- Codex wired in as an observer with proposals.  
- U-ledger acting as the canonical record for runs.

Next steps (future specs, not part of this spec):

- **SPEC-003** — Turn PFNA placeholder into PFNA V0 and open the door to real external inputs.  
- **SPEC-004** — Expand Press/APX into AEON/APXi with richer grammars and description capabilities.  
- **SPEC-006** — Enable multi-graph and dynamic topology (SLP) on top of the V1 pillars.  
- **SPEC-007** — Add governance, budgets, and Codex actioning to control and track structural change.

At that point, Aether has a clear line of sight from **paper parity baseline** through **generalised pillars** to **governed, self‑modifying systems**, with every step spelled out by SPEC‑00X documents and guarded by tests and the U-ledger.
