# SPEC-003 — Gate/TBP & PFNA V0 — External Inputs & Layering

## Status

- **Spec ID:** SPEC-003  
- **Name:** Gate/TBP & PFNA V0 — External Inputs & Layering  
- **Version:** v1 (skeleton)  
- **Phase:** Phase 3  
- **Scope:** Trinity Gate / TBP, NAP layers/modes, PFNA V0 path for external integer inputs  
- **Predecessors:**  
  - SPEC-001-AETHER — Full System Build Plan (Medium-Agnostic)  
  - SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)  
  - SPEC-005 — Phase 2 Pillar V1 Implementation Plan  
- **Related Phase:**  
  - Phase 3 — External Inputs & Advanced Press (with SPEC-004)  

---

## 1. Purpose & Context

By the end of Phase 2 (SPEC-005), the engine can:

- Run internal simulations (GF-01 and other small topologies),
- Replay runs via Loom,
- Compress streams with Press/APX V1,
- Ledger and observe via U-ledger and Codex V1 (observer-only),
- Accept a **PFNA placeholder** input path that is deterministic but minimal.

What it *cannot* yet do is act as a **first-class interface to the outside world**. External integer traces, sensor data, or higher-level “inputs” are not yet formalised or governed.

Phase 3’s Gate/TBP & PFNA V0 work (SPEC-003) changes that:

> Define the first real, deterministic path from **external integer sequences** → **PFNA-normalised representations** → **Gate/TBP** → **NAP envelopes & SceneFrames** → **UMX / Loom / Press**.

This spec focuses on the **Gate/TBP side** of Phase 3. The Press/APX side (AEON windows, APXi, etc.) is handled by SPEC-004, but both specs are part of the same Phase 3 milestone.

The non-negotiables:

- Everything remains **integer-only** and **deterministic**.
- GF-01 baseline behaviour is untouched unless PFNA explicitly changes initial conditions or config.  
- No governance / budgets yet — PFNA V0 is **data ingress**, not policy.

---

## 2. Dependencies & References

### 2.1 Core & Pillar Specs

- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (SPEC-001-AETHER)  
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (SPEC-002)  
- `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (SPEC-005)  
- `spec_000_AETHER_Spec_Index_and_Roadmap.md` (SPEC-000-AETHER)  

Pillar master specs:

- Trinity Gate pillar: `trinity gate full spec.txt`  
- NAP and PFNA sections in Gate/TBP and any adjunct docs  
- Astral Press master spec (for manifest-layer interactions): `astral_press_master_implementation_spec_combined_v1.md`  

### 2.2 Contracts & Types

Expected under `docs/contracts/`:

- `SceneFrame_v1.md`  
- `NAPEnvelope_v1.md`  
- `TickLoop_v1.md`  
- `ULedgerEntry_v1.md`  
- `APXManifest_v1.md`  
- `LoomBlocks_v1.md`  
- `UMXTickLedger_v1.md`  
- `CodexContracts_v1.md`  

New / extended contracts to be defined or refined during SPEC-003:

- `PFNA_V0_Schema_v1.md` (or equivalent)  
- Gate/TBP configuration & IO contracts (if not already present).  

### 2.3 Relationship to Other Phase 3 Work

- SPEC-004 — Press/APX AEON & APXi — handles **advanced window grammars & explanation codes**, not PFNA itself.  
- SPEC-003 — this spec — focuses on **how external data enters and leaves** the engine via Gate/TBP, NAP, and PFNA V0.

---

## 3. Scope & Non-Goals

### 3.1 In Scope

- Design and implement **PFNA V0**:

  - Minimal but complete schema for inputs: integer traces + metadata.  
  - Deterministic mapping from raw external streams to PFNA V0 structures.  
  - Configurable mapping from PFNA V0 → initial UMX state and/or run parameters.

- Extend **Gate/TBP**:

  - Define a **session lifecycle** (start, run, stop) with clear control messages.  
  - Route PFNA-derived inputs into `SceneFrame_v1` and NAP envelopes.  
  - Introduce and test **NAP layers & modes** for INGRESS / DATA / CTRL / EGRESS.

- Establish **IO paths**:

  - Well-defined ingress and egress semantics using NAP envelopes.  
  - Ensure IO is fully recorded in U-ledger (no “invisible inputs”).

### 3.2 Out of Scope (Deferred)

- Full PFNA grammar for complex signals or high-dimensional series (V0 is intentionally minimal and integer-focused).  
- Governance around which PFNA inputs are allowed (SPEC-007).  
- Rich APXi or AEON-level semantics (SPEC-004).  
- Multi-graph / SLP-specific input routing (SPEC-006).  

SPEC-003 aims to provide a **thin but solid V0 bridge** between outside data and the existing engine.

---

## 4. Phase 3 Gate/TBP Objectives

### 4.1 Primary Objectives

1. **Deterministic PFNA V0 pipeline**  
   - Raw integer sequences (files, fixtures, streams) can be transformed into PFNA V0 structures in a deterministic, reversible way.

2. **Session-level Gate/TBP IO**  
   - Gate/TBP can start, control, and end runs using NAP CTRL envelopes.  
   - External inputs are injected via PFNA and recorded in SceneFrames and NAP.

3. **Layered NAP semantics**  
   - NAP envelopes can be categorised into at least four layers (INGRESS, DATA, CTRL, EGRESS) with clear semantics.

4. **Ledgered IO**  
   - Every PFNA-derived input that affects the run must be visible in U-ledger via NAP / SceneFrame / ULedgerEntry references.

### 4.2 Success Criteria (High Level)

- At least one **Phase 3 demo scenario** where:

  - External integer fixture (PFNA V0) modifies initial state or parameters.  
  - The run’s behaviour differs from the baseline in a deterministic and explainable way.  
  - All input effects are visible in U-ledger and in NAP envelopes.  

- GF-01 baseline is preserved when PFNA is not in play (Gate/TBP default config reproduces SPEC-002 behaviour).

---

## 5. Epics & Workstreams — Phase 3 (Gate/TBP Side)

For Phase 3 we re-use the **P3.x** numbering for epics across SPEC-003 and SPEC-004. SPEC-003 holds **EPIC P3.1–P3.3** on the Gate/TBP & PFNA side.

### EPIC P3.1 — PFNA V0 Pipeline (Ingress Normalisation)

**Intent:** Define and implement the V0 PFNA pipeline that turns external integer data into engine-ready structures.

**Key outcomes:**

- A minimal but precise PFNA V0 schema.  
- Deterministic ingest from fixtures into PFNA V0 objects.  
- Configurable mapping into run configs.

Core themes for issues (to be detailed in the planning pack later):

- Design `PFNA_V0_Schema_v1` (contract):

  - Basic unit type (e.g. a timestamped integer vector or scalar).  
  - Metadata fields (source id, channel id, sampling notes).  
  - Batching/windowing rules.

- Implement PFNA V0 loader:

  - Load from JSON/CSV/other simple formats.  
  - Validate structures and provide clear error reporting.  

- Define mapping rules:

  - **Initial state mapping:** subset of PFNA sequences mapped into initial `u(0)` or other UMX state fields.  
  - **Parameter mapping:** PFNA sequences mapped into profile or run parameters (e.g. flux caps, scaling coefficients).  

- Tests:

  - Deterministic round-trip: fixture → PFNA V0 → config → ledger.  
  - Multiple PFNA fixtures produce distinct but deterministic configs.

---

### EPIC P3.2 — Gate/TBP Session & NAP Layering

**Intent:** Upgrade Gate/TBP from a minimal GF-01 helper to a **session-aware IO controller** using NAP layers and CTRL messages.

**Key outcomes:**

- Explicit run/session lifecycle via NAP CTRL envelopes.  
- Clear semantics for NAP layers: INGRESS, DATA, CTRL, EGRESS.  
- GF-01 defined as a simple DATA-only scenario by default.

Core themes:

- Formalise Gate/TBP session lifecycle:

  - Start-of-run CTRL messages.  
  - Tick-level DATA messages (scene frames, envelopes).  
  - End-of-run CTRL + EGRESS messages.

- Extend `NAPEnvelope_v1` usage:

  - Add enumerations / constants for layers: INGRESS, DATA, CTRL, EGRESS.  
  - Add modes beyond P if needed for PFNA.  
  - Ensure GF-01 remains DATA/P only.

- Integrate with `SceneFrame_v1`:

  - For each tick, ensure NAP envelope content is derivable from SceneFrame.  
  - PFNA-related transitions (e.g. “config loaded”, “input batch applied”) show up in CTRL-layer SceneFrames and envelopes.

- Tests:

  - One or more scenarios with non-trivial session lifecycle (start, patch input, end).  
  - GF-01 tests prove backwards-compat: when Gate is configured in “GF01 mode”, behaviour is unchanged.

---

### EPIC P3.3 — IO Paths & U-ledger Traceability

**Intent:** Ensure all external inputs and Gate/TBP IO flows are **fully traceable** in U-ledger.

**Key outcomes:**

- Direct references from `ULedgerEntry_v1` to PFNA-derived artefacts.  
- Ability to answer: “Which inputs drove this tick/window?”

Core themes:

- Extend ULedgerEntry fields (if needed) to include:

  - Hashes or IDs of PFNA batches used at or before a tick/window.  
  - NAP layer/mode summaries for the tick/window.  

- Establish canonical ordering:

  - For each tick/window, define the order in which inputs, state updates, and ledger entries occur.  
  - Ensure determinism by fixing this order in TickLoop / Gate logic.

- Tests:

  - For a PFNA-driven scenario, query ledger and reconstruct:  
    - Which PFNA batches were used.  
    - Which changes they induced (e.g. initial state shift).  

  - Validate double-run determinism: ledger traces must match byte-for-byte for identical PFNA fixtures.

---

## 6. Testing & Determinism (Gate/TBP & PFNA V0)

SPEC-003 inherits and builds on the determinism guardrails of SPEC-002 and SPEC-005:

- **No nondeterministic sources:** No randomness, current time, or environment-specific differences in PFNA V0 processing.  
- **Canonical serialisation:** PFNA V0 objects, NAP envelopes, and related U-ledger references must use canonical JSON serialisation from SPEC-005.  
- **Snapshot tests:** At least one PFNA-driven scenario must have a stored snapshot that integration tests compare against.

Any deviation in PFNA or Gate/TBP behaviour must show up as a test failure, not a silent drift.

---

## 7. Repo Placement & Planning Docs

When implemented:

- This spec lives at:  
  `docs/specs/spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md`

- A corresponding planning file (GitHub issue pack) should live at:  
  `docs/planning/spec_003_Gate_PFNA_V0_External_Inputs_and_Layering_Issues.md`

This keeps SPEC-003 aligned with SPEC-002 and SPEC-005 as the engine grows.

---

## 8. Forward Relations

- **Upstream:** SPEC-003 assumes Pillar V1 engine from SPEC-005 and baseline from SPEC-002.  
- **Peer:** SPEC-004 (Press/APX AEON & APXi) completes the Phase 3 story by adding richer time-window grammars and explanatory descriptions.  
- **Downstream:** SPEC-007 (Governance & Codex actioning) will later govern what PFNA inputs are allowed and how they may influence structure and policy.

SPEC-003’s job is to ensure that by the time we reach governance, the path for external data is already clean, deterministic, and fully observable.
