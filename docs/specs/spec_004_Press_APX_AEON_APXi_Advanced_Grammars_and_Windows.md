# SPEC-004 — Press/APX AEON & APXi — Advanced Grammars & Windows

## Status

- **Spec ID:** SPEC-004  
- **Name:** Press/APX AEON & APXi — Advanced Grammars & Windows  
- **Version:** v1 (skeleton)  
- **Phase:** Phase 3  
- **Scope:** Astral Press AEON windows, APXi descriptive codes, multi-scale views  
- **Predecessors:**  
  - SPEC-001-AETHER — Full System Build Plan (Medium-Agnostic)  
  - SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)  
  - SPEC-005 — Phase 2 Pillar V1 Implementation Plan  
- **Related Phase:**  
  - Phase 3 — External Inputs & Advanced Press (with SPEC-003)  

---

## 1. Purpose & Context

By the end of Phase 2 (SPEC-005), Press/APX can:

- Manage multiple named streams via `PressWindowContext`,
- Use a small set of schemes (ID, R, basic GR),
- Produce `APXManifest_v1` records with deterministic `manifest_check`,
- Reproduce GF-01 APX manifests exactly.

What it *doesn’t* do yet is “look up” and “explain” engine behaviour across **multiple time scales** or with richer **window grammars**. Right now it is mostly “compression per window”.

Phase 3’s Press/APX work (SPEC-004) adds the AEON/APXi capabilities:

> Move from “per-window compression” to **multi-scale temporal views and simple explanatory programs** over streams, while staying integer-only and deterministic.

SPEC-004 is the Press side of Phase 3. SPEC-003 handles Gate/TBP & PFNA V0 (external inputs and layering). Together they make Phase 3 “external-aware and time-smart”.

Non-negotiables:

- AEON/APXi are **built on top of** Pillar V1 Press/APX, not a rewrite.  
- GF-01 manifests remain untouched unless a specific AEON/APXi mode is invoked.  
- No probabilistic or floating-point reasoning; MDL-style reasoning is still expressed in integer bit counts.

---

## 2. Dependencies & References

### 2.1 Core & Pillar Specs

- `spec_001_aether_full_system_build_plan_medium_agnostic.md` (SPEC-001-AETHER)  
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (SPEC-002)  
- `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (SPEC-005)  
- `spec_000_AETHER_Spec_Index_and_Roadmap.md` (SPEC-000-AETHER)  
- `spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md` (SPEC-003; Phase 3 peer)  

Astral Press pillar master spec:

- `astral_press_master_implementation_spec_combined_v1.md`  

### 2.2 Contracts & Types

Existing contracts from Phase 2:

- `APXManifest_v1.md`  
- `Profile_CMP0_v1.md`  
- Any scheme descriptors used by ID/R/GR implementations  

New / extended contracts for AEON/APXi:

- `AEONWindowGrammar_v1.md` — defines hierarchical window structures & relationships.  
- `APXiDescriptor_v1.md` — defines APXi program/descriptor format and fields.  
- Possible update or extension to `APXManifest_v1` for AEON/APXi metadata.

### 2.3 Relationship to Other Phase 3 Work

- SPEC-003 — Gate/TBP & PFNA V0 — External Inputs & Layering:  
  - Provides richer NAP layering and external feeds that AEON/APXi may consume or describe.  
- SPEC-004 — this spec — leaves PFNA & Gate semantics alone and focuses on **how Press/APX represents and compresses behaviour over time**.

---

## 3. Scope & Non-Goals

### 3.1 In Scope

- **AEON Window Grammar**:

  - Representing multi-scale window structures (e.g. ticks → small windows → large windows).  
  - Defining relationships between windows (e.g. parent/child, overlapping, derived).  

- **APXi Descriptors**:

  - Simple, deterministic “programs” or summaries that describe patterns in streams and their windows.  
  - Integration with MDL accounting: APXi code length + residual costs.  

- **AEON/APXi Integration with Press V1**:

  - AEON views constructed on top of existing window outputs.  
  - APXi descriptors recorded as part of manifests or companion records.  

- **Multi-stream, multi-scale explanations**:

  - Ability to describe relationships between streams (e.g. S1 and S2 correlations) across windows.

### 3.2 Out of Scope (Deferred)

- Any non-integer MDL or probabilistic/information-theoretic approximations (stick to integer bit counts).  
- Codex-driven advanced modelling that duplicates APXi’s job (Codex remains observer-only in Phase 3).  
- Governance over which AEON/APXi models are allowed (SPEC-007).  

SPEC-004 is about upgrading Press/APX’s **expressive power over time and structure**, not about changing how external data flows in (that’s SPEC-003).

---

## 4. Phase 3 Press/APX Objectives

### 4.1 Primary Objectives

1. **AEON Window Grammar**  
   - Define a formal way to build and query multi-scale windows over one or more streams.

2. **APXi Descriptive Codes**  
   - Implement a small, deterministic “language” of descriptors over streams/windows whose lengths contribute to MDL.

3. **Integrate AEON/APXi with APXManifest**  
   - Make sure advanced descriptions are properly accounted for in manifests (or companion records) without breaking existing R-mode and other V1 schemes.

4. **Demonstrate Multi-Scale Explanations**  
   - At least one Phase 3 demo scenario where AEON/APXi yields a clear multi-scale explanation of behaviour that plain per-window compression does not show as cleanly.

### 4.2 Success Criteria (High Level)

- AEON windows can be defined for GF-01-like runs and at least one more complex test scenario.  
- APXi descriptors can represent simple patterns (e.g. repeated motifs, trend segments) with deterministic code lengths.  
- Manifests (or companion AEON/APXi records) remain deterministic and compatible with existing Press V1.  
- The engine can answer queries like “show me the AEON/APXi view for this run” without ambiguity.

---

## 5. Epics & Workstreams — Phase 3 (Press/APX Side)

For Phase 3, SPEC-004 owns **EPIC P3.4–P3.6** on the Press/APX side, complementing SPEC-003’s P3.1–P3.3.

### EPIC P3.4 — AEON Window Grammar

**Intent:** Add a general, deterministic representation for hierarchical windows over streams.

**Key outcomes:**

- A contract specifying AEON window types and relationships.  
- An implementation that can define AEON structures for runs.  
- Query APIs to navigate these window hierarchies.

Core themes:

- Design `AEONWindowGrammar_v1`:

  - Types of windows (base window, aggregate window, sliding window, etc.).  
  - Relationships: contains, overlaps, parent/child.  
  - Identifiers and naming scheme for windows.

- Build AEON construction:

  - Given Press V1 windows (e.g. fixed tick ranges), define how AEON builds larger windows (e.g. unions, rolling subsets).  
  - Support multiple streams sharing AEON windows.

- Add AEON query API(s):

  - `get_window(id)` → window definition.  
  - `list_child_windows(parent_id)` → list of subwindows.  
  - Possibly `windows_covering_tick(t)` or `windows_intersecting_range(start, end)`.

- Tests:

  - AEON windows over GF-01 and at least one synthetic scenario.  
  - Deterministic AEON hierarchies for identical runs.

---

### EPIC P3.5 — APXi Descriptor Language

**Intent:** Implement APXi — a simple language of descriptive codes over streams and windows — and integrate it with MDL accounting.

**Key outcomes:**

- APXi descriptor contract.  
- Basic set of APXi primitives that can encode common patterns.  
- MDL accounting rules for APXi code length and residuals.

Core themes:

- Design `APXiDescriptor_v1` contract:

  - Fields for: target streams, window ids, descriptor type, parameters.  
  - Optional references to motifs (e.g. from Codex, but still deterministic).

- Define APXi primitive types (examples only, actual set to be derived from pillar spec):

  - Constant segment over a window.  
  - Repetition of a short pattern.  
  - Simple linear trend in integer sequences.  
  - Piecewise combinations of the above.

- Implement APXi MDL accounting:

  - Define how APXi code length is computed (integer bit lengths, no floats).  
  - Define how residuals (differences between descriptor and actual stream) are encoded and counted.  
  - Ensure APXi is compatible with and/or layered on top of ID/R/GR.

- Tests:

  - Simple synthetic sequences for each APXi primitive.  
  - Scenarios where APXi gives a lower total description length than raw ID/R, in a deterministic, explainable way.

---

### EPIC P3.6 — AEON/APXi Integration & Views

**Intent:** Integrate AEON and APXi with APXManifest and provide API-level visibility into advanced temporal descriptions.

**Key outcomes:**

- AEON/APXi outputs attached to manifests or companion structures.  
- A simple API to retrieve multi-scale explanations for a run.

Core themes:

- Manifest integration:

  - Decide whether AEON/APXi live inside `APXManifest_v1` or in companion records referenced by it.  
  - Ensure `manifest_check` remains deterministic and unambiguous in presence of AEON/APXi.

- View APIs:

  - `get_aeon_view(run_id)` → AEON window hierarchy plus stream mapping.  
  - `get_apxi_view(run_id)` → APXi descriptors and their MDL contributions.  
  - Optionally combine them for “explanation dashboards” (still just data/API at this stage).

- Tests:

  - For GF-01 and at least one more complex scenario, generate AEON/APXi views and confirm they are deterministic and consistent with manifests.  
  - Regression snapshots for AEON/APXi outputs, similar to GF-01 snapshot harness.

---

## 6. Testing & Determinism (AEON/APXi)

SPEC-004 inherits the determinism constraints from earlier specs and adds:

- **AEON determinism:** Window hierarchies must be uniquely determined by run configuration and basic AEON rules.  
- **APXi determinism:** Given the same run and configuration, APXi must select the same descriptors with the same parameters.  
- **Snapshot tests:** At least one AEON/APXi scenario is snapshotted and compared byte-for-byte on re-run.

No stochastic modelling, no heuristic randomness. Any tie-breaking in APXi selection must be explicitly defined and deterministic.

---

## 7. Repo Placement & Planning

When implemented:

- This spec lives at:  
  `docs/specs/spec_004_Press_APX_AEON_APXi_Advanced_Grammars_and_Windows.md`

- A corresponding planning file (GitHub issue pack) should live at:  
  `docs/planning/spec_004_Press_APX_AEON_APXi_Advanced_Grammars_and_Windows_Issues.md`

AEON/APXi planning will mirror the structure already used for SPEC-002 and SPEC-005: epics → issue stubs → GitHub issues.

---

## 8. Forward Relations

- **Upstream:** SPEC-004 assumes Press/APX V1 from SPEC-005 and baseline GF-01 from SPEC-002.  
- **Peer:** SPEC-003 provides PFNA V0 and richer NAP layers that AEON/APXi may use as additional streams or annotations.  
- **Downstream:** Later specs (especially SPEC-007) may use AEON/APXi outputs as inputs to governance and Codex actioning.

SPEC-004’s job is to ensure that by the time governance and Codex actioning arrive, the engine already has a **rich, deterministic temporal description layer** over its behaviour.
