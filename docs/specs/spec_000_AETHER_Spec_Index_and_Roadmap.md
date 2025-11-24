# SPEC-000-AETHER — Spec Index & Roadmap

## Status

- **Spec ID:** SPEC-000-AETHER
- **Name:** Aether Spec Index & Roadmap
- **Version:** v1 (draft)
- **Scope:** Index and roadmap for all Aether implementation specs (SPEC-00X)
- **Intent:** Make it obvious how we get from “nothing” to **100% coverage** of the pillar master specs using a small, ordered set of implementation specs.

This doc is **bookkeeping + navigation**, not a new feature spec. It’s the map you keep open next to the others.

---

## 1. Spec Catalogue (current + planned)

This table names every spec and pins its purpose at a glance.

| Spec ID           | Name / Focus                                                | Phase | Status      |
|-------------------|-------------------------------------------------------------|-------|------------|
| SPEC-000-AETHER   | Spec Index & Roadmap (this doc)                            | P0    | Draft      |
| SPEC-001-AETHER   | Full System Build Plan (Medium-Agnostic)                   | P0    | Existing   |
| SPEC-002          | GF-01 CMP-0 Baseline Engine (Paper Parity)                 | P1    | Existing   |
| SPEC-003          | Gate/TBP & PFNA V0 — External Inputs & Layering            | P3    | Planned    |
| SPEC-004          | Press/APX AEON & APXi — Advanced Grammars & Windows        | P3    | Planned    |
| SPEC-005          | Pillar V1 Generalisation (UMX/Loom/Press/Gate/U-ledger/Codex) | P2 | Existing   |
| SPEC-006          | Multi-Graph & Dynamic Topology V1 (SLP, growth/prune)      | P4    | Planned    |
| SPEC-007          | Governance, Budgets & Codex Actioning V1                   | P5    | Planned    |

Notes:

- You already have full text for **SPEC-001**, **SPEC-002** and the **SPEC-005** plan in this repo planning work.
- SPEC-003/004/006/007 are **stubs with clear themes** so we can hang future detail off them without renumbering.

---

## 2. Phase Overview (0 → 5)

This is the “game board” view: what each phase is trying to unlock.

### Phase 0 — Foundations & Contracts

**Specs:**

- SPEC-000-AETHER — this index + roadmap.
- SPEC-001-AETHER — Full System Build Plan (medium-agnostic).

**Goal:**

- Repo created, docs/fixtures contracts mirrored.
- Contracts and master pillar specs live under `docs/` and are treated as the **source of truth**.
- No engine code required yet; this is scaffolding and paperwork.

---

### Phase 1 — SPEC-002 GF-01 CMP-0 Baseline

**Spec:**

- SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity).
- Plus its GitHub issue pack (`spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md`).

**Goal:**

- One graph (GF-01), one profile (CMP-0).
- Ticks 1–8, fully paper-parity with GF-01 PDFs.
- UMX, Loom, Press, NAP, Gate all wired **just enough** to pass the GF-01 exam.
- Strict determinism harness + snapshot in place.

This becomes the **golden baseline** that everything else must respect.

---

### Phase 2 — SPEC-005 Pillar V1 Generalisation

**Spec:**

- SPEC-005 — Phase 2 Pillar V1 Implementation Plan (Pillar generalisation).
- Plus its GitHub issue pack (`spec_005_Phase2_Pillar_V1_GitHub_Issues.md`).

**Goal:**

- Take the GF-01 one-off and turn it into a reusable **Pillar V1** engine:
  - UMX V1: general integer engine, multiple topologies.
  - Loom V1: proper time axis, replay, configurable spacing.
  - Press/APX V1: stream registry, multiple schemes (ID/R/GR), general manifests.
  - Gate/TBP V1: SceneFrame as the integration object, NAP layers/modes, PFNA placeholder.
  - U-ledger V1: canonical serialisation & hash chain for runs.
  - Codex V1: observer-only motif identification and proposal emission.

After Phase 2, the codebase is no longer “just GF-01”; it’s a **small general engine** that still exactly reproduces GF-01 when asked.

---

### Phase 3 — SPEC-003 & SPEC-004 (External Inputs & Advanced Press)

**Specs (planned):**

- SPEC-003 — Gate/TBP & PFNA V0 — External Inputs & Layering.
- SPEC-004 — Press/APX AEON & APXi — Advanced Grammars & Windows.

**High-level Goal:**

- Turn the engine from a closed demo into something that can **accept external integer streams** and **reason about more complex temporal structures** using Press/APX.

**Rough focus:**

- Gate/TBP / PFNA:
  - Move from PFNA placeholder to a **first real PFNA pipeline**.
  - Define how physical or external integer traces are normalised and injected.
  - Enrich NAP layer/mode semantics for multi-layer IO (INGRESS / DATA / CTRL / EGRESS).
- Press/APX AEON/APXi:
  - Add AEON-like window grammars (overlapping windows, multi-scale views).
  - Implement the first APXi-style “explanatory programs” / more expressive MDL descriptions.
  - Keep integer-only behaviour and determinism.

Phase 3 is all about **opening the engine to the outside world** while preserving the guarantees from Phases 1–2.

---

### Phase 4 — SPEC-006 Multi-Graph & Dynamic Topology V1

**Spec (planned):**

- SPEC-006 — Multi-Graph & Dynamic Topology V1 (SLP, growth/prune).

**High-level Goal:**

- Move from “one fixed graph per run” to a **dynamic space of graphs**:
  - Multiple UMX instances (graphs) per run.
  - SLP-like growth/prune of topology over time.
  - Loom and U-ledger updated to track this richer structure.

This is where Aether stops being “a single network experiment” and becomes a **living topological playground**.

---

### Phase 5 — SPEC-007 Governance, Budgets & Codex Actioning

**Spec (planned):**

- SPEC-007 — Governance, Budgets & Codex Actioning V1.

**High-level Goal:**

- Turn Codex from passive observer into an actor under **explicit governance**:

  - Codex proposals can be accepted/rejected under budget constraints.
  - Structural changes to graphs or parameters must pass governance checks.
  - U-ledger acts as the immutable record of decisions and changes.

After Phase 5, the system has:

- A governed way to change itself.
- Full traceability of why any structural change occurred.
- A clear “who approved what and when” story.

---

## 3. Pillar Coverage Matrix

This section answers: _“Which spec/phase covers which parts of each pillar master spec?”_

Think of it as a coverage map, not a strict one-to-one; some features may be touched in multiple specs.

### 3.1 Universal Matrix (UMX Pillar)

- **SPEC-002 / Phase 1**
  - CMP-0 flux rule for a single topology (GF-01).
  - UMXTickLedger_v1 for ticks 1–8.
- **SPEC-005 / Phase 2**
  - UMX V1 engine:
    - Multi-topology support (loader/validator).
    - UMXRunContext for multi-run.
    - Generalised CMP-0 stepping + diagnostics.
- **SPEC-006 / Phase 4 (planned)**
  - Multi-graph support (multiple UMX instances per run).
  - Dynamic topology: SLP growth/prune.
  - Integration with Loom and U-ledger for topological changes.
- **SPEC-007 / Phase 5 (planned)**
  - Governance-driven topology changes actioned via Codex proposals.

### 3.2 Aevum Loom Pillar

- **SPEC-002 / Phase 1**
  - CMP-0 Loom for GF-01:
    - Chain rule for C_t.
    - P-blocks, single I-block at t=8.
- **SPEC-005 / Phase 2**
  - LoomRunContext.
  - Configurable `W`, alternative s_t rules.
  - Replay API (`get_chain_at`, `replay_state_at`).
- **SPEC-006 / Phase 4 (planned)**
  - Multi-graph / multi-chain support.
  - More advanced block types for dynamic topology (SLP events).
- **SPEC-007 / Phase 5 (planned)**
  - Use Loom chain in governance decisions and budgets (e.g. time-weighted signals).

### 3.3 Astral Press / APX Pillar

- **SPEC-002 / Phase 1**
  - Minimal R-mode encoder for two GF-01 streams.
  - APXManifest_v1 and `manifest_check` for 8-tick and 2-tick windows.
- **SPEC-005 / Phase 2**
  - PressWindowContext and stream registry.
  - Three schemes: ID, R, basic GR.
  - Generalised manifest generation with multiple streams and mixed schemes.
- **SPEC-004 / Phase 3 (planned)**
  - AEON-like window grammars and multi-scale views.
  - APXi expressive descriptions / primitive “program-like” codes.
  - Richer MDL accounting where needed.

### 3.4 Trinity Gate / TBP Pillar (incl. PFNA & NAP)

- **SPEC-002 / Phase 1**
  - Minimal Gate/TBP wiring:
    - SceneFrame_v1 (basic) for GF-01.
    - NAPEnvelope_v1 in DATA/P mode.
- **SPEC-005 / Phase 2**
  - SceneFrame_v1 as canonical per-tick integration object.
  - Layer/mode framework for NAP (DATA/CTRL/etc.), still mostly used in simple form.
  - PFNA placeholder for external inputs, wired deterministically.
- **SPEC-003 / Phase 3 (planned)**
  - Full PFNA V0 path:
    - External integer traces → PFNA normalisation → Gate → SceneFrames.
  - Richer NAP layering across INGRESS, DATA, CTRL, EGRESS.
  - First genuine “external input” scenarios.
- **SPEC-007 / Phase 5 (planned)**
  - Governance messages through NAP CTRL layer.
  - Codex proposal acceptance/rejection via Gate/TBP paths.

### 3.5 Codex Eterna Pillar

- **SPEC-002 / Phase 1**
  - No Codex behaviour yet; Codex is concept-only.
- **SPEC-005 / Phase 2**
  - CodexContext as observer-only.
  - Motif identification (simple heuristics) → CodexLibraryEntry_v1.
  - Proposal emission (`CodexProposal_v1`) without actioning.
- **SPEC-007 / Phase 5 (planned)**
  - Codex proposals can be accepted under budget/governance rules.
  - Codex can drive structural changes (e.g. place/add motifs) recorded in U-ledger.
  - Clear boundaries so Codex never silently changes the engine outside governance.

### 3.6 Universal Ledger (U-ledger) Pillar

- **SPEC-002 / Phase 1**
  - Determinism harness & regression snapshot for GF-01.
  - Ad hoc serialisation sufficient for the exam, but not yet the final ledger spec.
- **SPEC-005 / Phase 2**
  - Canonical JSON serialisation for all core artefacts.
  - Hashing rules and utilities.
  - ULedgerEntry_v1 per tick/window with hash chain.
- **SPEC-006 / Phase 4 (planned)**
  - Multi-graph and SLP event logging.
  - Explicit recording of topology changes and cross-graph relationships.
- **SPEC-007 / Phase 5 (planned)**
  - Governance decisions and Codex actions recorded as first-class ledger entries.
  - Complete “who/what/when/why” trail for all structural changes.

---

## 4. “100% Coverage” Definition

When we say **“100% coverage of the master specs”**, we mean:

1. **Every normative requirement** in the pillar master specs is:
   - Mapped to at least one SPEC-00X document, and
   - Backed by at least one test or ledgered check in the implementation.

2. For each pillar, we can answer:
   - “Which spec(s) implement this requirement?”
   - “Which tests prove it works?”
   - “Where in U-ledger do we see it in action?”

3. No “mystery features”:
   - If the code does something meaningful, it is either:
     - Described in a SPEC-00X doc, or
     - Marked as experimental and destined for a future SPEC or deletion.

In practice, this means:

- **SPEC-001** defines the big-picture build logic.
- **SPEC-002, 005, 003, 004, 006, 007** collectively enumerate all concrete capabilities needed to make the pillar specs real.
- The GitHub issue packs (like the ones you already have for SPEC-002 and SPEC-005) form the **implementation spine**.

When the last phase (Phase 5) is green and every master-spec requirement is mapped and tested, we can legitimately say “Aether V1 fully implements the master specs.”

---

## 5. Where to Put Things in the Repo

When you create the repo, a simple layout that fits this roadmap is:

```text
aether-engine/
  docs/
    specs/
      spec_000_AETHER_Spec_Index_and_Roadmap.md
      spec_001_aether_full_system_build_plan_medium_agnostic.md
      spec_002_GF01_CMP0_Baseline_Build_Plan.md
      spec_005_Phase_2_Pillar_V1_Implementation_Plan.md
      # Later:
      spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md
      spec_004_Press_APX_AEON_APXi_Advanced_Grammars.md
      spec_006_MultiGraph_Dynamic_Topology_V1.md
      spec_007_Governance_Budgets_Codex_Actioning_V1.md

    planning/
      spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md
      spec_005_Phase2_Pillar_V1_GitHub_Issues.md

    contracts/
      # Pillar contracts + run contracts
      # (TopologyProfile_v1, UMXTickLedger_v1, LoomBlocks_v1, APXManifest_v1, NAPEnvelope_v1, ULedgerEntry_v1, etc.)

    fixtures/
      gf01/
        # All GF-01 PDFs and any CSV/JSON mirrors

  src/
    # Engine implementation by component (umx, loom, press, gate, codex, uledger, etc.)

  tests/
    gf01/
    integration/
    regression/
```

This keeps:

- **Specs** (design-time) in `docs/specs/`,
- **Issue packs / GitHub-ready text** in `docs/planning/`,
- **Contracts** in `docs/contracts/`,
- **Fixtures** in `docs/fixtures/`,
- And leaves `src/` and `tests/` clean for GPT-5.1 Codex to fill out later.

---

## 6. Next Concrete Documents to Draft

With this roadmap in place, the next natural drafting targets are:

1. **SPEC-005 proper spec doc**  
   (You already have the issue pack; we can turn the earlier Phase 2 description into a full narrative spec like SPEC-002.)

2. **SPEC-003 and SPEC-004 skeleton specs**  
   - Each with:
     - Purpose & scope,
     - Coverage vs pillars,
     - Epics & high-level issues (to be later expanded into GitHub issue packs).

From here, we can proceed spec-by-spec:

- For each SPEC-00X:
  - Draft the narrative spec (`docs/specs/...`),
  - Draft the GitHub issue pack (`docs/planning/...`),
  - Keep updating this SPEC-000 index if anything moves.

This keeps the path to **100% coverage** visible at all times.
