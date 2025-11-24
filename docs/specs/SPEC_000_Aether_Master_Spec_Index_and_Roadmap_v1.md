# SPEC-000 — Aether Master Spec Index & Roadmap

This document is the **top-level index** for the Aether engine specs and build plan.

It’s meant to live in `docs/specs/` as the “start here” file for humans and for GPT-based dev flows (e.g. GitHub Copilot / GPT 5.1 Codex working over the repo).

---

## 1. Purpose

This file answers three questions:

1. **What are the moving parts?** — pillars, subsystems, paper artefacts.
2. **What specs exist and how do they relate?** — SPEC-001 through SPEC-007.
3. **In what order do we build?** — phases, milestones, and dependency edges.

Everything else (pillar master specs, issue packs, PDFs) plug into this map.

---

## 2. Pillars & Subsystems at a Glance

Aether V0/V1 is organised into **pillars** plus one cross-cutting subsystem:

### 2.1 Core Pillars

1. **Universal Matrix (UMX)**  
   - Integer flux engine over graphs.  
   - Ticks, node states, edge fluxes, conservation.  
   - Owns: `UMXTickLedger_v1` records, edge fluxes, per-tick state evolution.

2. **Aevum Loom (Loom)**  
   - Time axis and chain.  
   - Per-tick `C_t` chain, P-blocks, periodic I-block checkpoints.  
   - Owns: `LoomPBlock_v1`, `LoomIBlock_v1`, replay API over ticks/state.

3. **Astral Press / APX / AEON / APXi (Press)**  
   - Compression + description of engine traces.  
   - APX: ID/R/GR schemes, bit counts, `APXManifest_v1`, `manifest_check`.  
   - AEON: window grammar and registry over time.  
   - APXi: higher-level descriptors and MDL accounting for sequences.

4. **Trinity Gate / TBP + NAP / PFNA (Gate)**  
   - Entry/exit of the engine and session orchestration.  
   - NAP: envelopes across layers (INGRESS/DATA/CTRL/EGRESS).  
   - PFNA: deterministic external integer inputs.  
   - TBP: decision loop wiring together Codex proposals, governance, and SLP.

5. **Codex Eterna (Codex)**  
   - Observer/analyst over engine traces and Press/AEON/APXi artefacts.  
   - Learns motifs, emits proposals (`CodexProposal_v1`).  
   - Observer-only up to Phase 4, then governed actioning in Phase 5.

### 2.2 Cross-Cutting Subsystem

6. **U-ledger Subsystem (not a pillar, but treated like one in planning)**  
   - Canonical serialisation + hashing for core records.  
   - `ULedgerEntry_v1` chains together UMX, Loom, Press, NAP, Codex, SLP.  
   - Used for determinism checks, replay, governance/audit.

---

## 3. Spec Catalogue

This section lists all the Aether specs and their roles.

> **Naming convention in the repo:**  
> Specs live under `docs/specs/` with filenames like `spec_00X_*.md`.  
> Contracts live under `docs/contracts/`.  
> PDFs and paper artefacts live under `docs/fixtures/`.

### 3.1 SPEC-001 — Full System Build Plan (Medium-Agnostic)

- **File (existing):**  
  `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
- **Status:** Baseline planning spec (already authored).  
- **Scope:**  
  - High-level description of pillars.  
  - Phase breakdown, profiles, behaviours.  
  - Medium-agnostic (paper or code).  
- **Role in roadmap:**  
  - Root conceptual spec for Aether.  
  - Everything else (SPEC-002…007) refines it into code-focused build stages.

### 3.2 SPEC-002 — GF-01 CMP-0 Baseline Engine (Paper Parity)

- **File (existing):**  
  `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- **Phase:** **Phase 1** — Baseline.  
- **Scope:**  
  - Implement integer-only CMP-0 profile.  
  - Reproduce GF-01 V0 run exactly (ticks 1–8).  
  - UMX, Loom, Press, NAP, minimal Gate/TBP wiring.  
- **Output:**  
  - First working digital engine with strict paper parity.  
  - Determinism harness + regression snapshot for GF-01.

### 3.3 SPEC-003 — Gate/TBP & PFNA V0 / IO (Phase 3)

- **File (this issue pack):**  
  `docs/specs/SPEC_003_Phase_3_Issue_Pack_v1.md`
- **Phase:** **Phase 3 (part 1)** — IO and session orchestration.  
- **Scope:**  
  - Gate/TBP session lifecycle and TickLoop integration.  
  - NAP layers & modes V1 (INGRESS/DATA/CTRL/EGRESS).  
  - PFNA V0 schema, loader, and PFNA → engine mapping.  
  - NAP IO wiring and Press configuration via Gate.  
  - Canonical PFNA demo scenario + regression snapshot.

### 3.4 SPEC-004 — Press AEON/APXi Views & Descriptors (Phase 3)

- **File (this issue pack):**  
  `docs/specs/SPEC_004_Phase_3_Issue_Pack_v1.md`
- **Phase:** **Phase 3 (part 2)** — Views & descriptors on top of Press.  
- **Scope:**  
  - AEON window grammar and registry.  
  - APXi descriptor contracts and primitive types.  
  - APXi MDL accounting and residual handling.  
  - AEON/APXi integration with PressWindowContext and manifests.  
  - AEON/APXi demo scenario, snapshots, and Codex ingest (observer-only).

### 3.5 SPEC-005 — Pillar V1 Generalisation (UMX/Loom/Press/Gate/Codex)

- **File (issue pack):**  
  `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`  
  *(plus its issue-pack companion if you keep them separate)*
- **Phase:** **Phase 2** — Generalise beyond GF-01.  
- **Scope:**  
  - UMX V1 (TopologyProfile loader, UMXRunContext, diagnostics).  
  - Loom V1 (LoomRunContext, configurable I-block spacing and s_t, replay).  
  - Press V1 (stream registry, ID/R/GR schemes, generalised manifests).  
  - Gate/TBP V1 integration via SceneFrame.  
  - NAP V1 layers/modes and PFNA placeholder wiring.  
  - U-ledger V1 (canonical serialisation + hashing, ULedgerEntry construction).  
  - Codex V1 observer mode (motifs + proposals, no actioning).

### 3.6 SPEC-006 — Multi-Graph & SLP / Dynamic Topology V1 (Phase 4)

- **File (this issue pack):**  
  `docs/specs/SPEC_006_Phase_4_Issue_Pack_v1.md`
- **Phase:** **Phase 4** — Multi-graph + dynamic topology.  
- **Scope:**  
  - MultiGraphRunConfig, topology registry, MultiGraphRunContext.  
  - SLPEvent_v1 contracts and topology operations.  
  - Application of SLP events between ticks.  
  - Loom, NAP, Press integration with multi-graph + SLP.  
  - Codex motifs for multi-graph and SLP (observer-only).  
  - U-ledger integration and multi-graph + SLP demo snapshot.

### 3.7 SPEC-007 — Governance, Budgets & Codex Actioning V1 (Phase 5)

- **File (this issue pack):**  
  `docs/specs/SPEC_007_Phase_5_Issue_Pack_v1.md`
- **Phase:** **Phase 5** — Governance + Codex actioning.  
- **Scope:**  
  - GovernanceConfig_v1 and policy contracts.  
  - Evaluation of CodexProposal_v1 against policies.  
  - TBP decision loop and governed action queue.  
  - Budget tracking and exhaustion behaviour.  
  - Governance-aware NAP IO (CTRL/GOV signalling).  
  - Governance + Codex actioning demo scenario.  
  - Governance introspection and dry-run mode.

---

## 4. Phases & Milestones

This section is the **time axis of the build**. Each phase has a recommended GitHub milestone name and its main spec(s).

### Phase 0 — Foundations (Paper & Master Specs)

- Pillar master specs (UMX, Loom, Press, Gate/TBP, Codex).  
- Paper artefacts (GF-01 PDFs, AETHER V0 booklets, templates).  
- SPEC-001 full system build plan.

> **Milestone name:** `Phase 0 — Foundations`  
> **Primary docs:** pillar master specs + SPEC-001.

### Phase 1 — SPEC-002 GF-01 CMP-0 Baseline

- **Goal:** Digital engine matches GF-01 paper under CMP-0 exactly.  
- **Core spec:** `spec_002_GF01_CMP0_Baseline_Build_Plan.md`  
- **Key outcomes:**  
  - UMX, Loom, Press, NAP, Gate minimal wiring for a single graph.  
  - GF-01 exam passes.  
  - Determinism harness + snapshot.

> **Milestone name:** `Phase 1 — SPEC-002 GF-01 CMP-0 Baseline`

### Phase 2 — SPEC-005 Pillar V1 Generalisation

- **Goal:** Generalise pillars beyond GF-01, still single-graph.  
- **Core spec:** `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`  
- **Key outcomes:**  
  - UMXRunContext, LoomRunContext, PressWindowContext.  
  - Multiple topologies, diagnostics, replay.  
  - U-ledger V1.  
  - Codex observer-only V1.

> **Milestone name:** `Phase 2 — SPEC-005 Pillar V1 Generalisation`

### Phase 3 — SPEC-003 + SPEC-004 (Gate IO & AEON/APXi)

Split into two tightly-coupled milestones, or one combined:

- **SPEC-003:** Gate/TBP sessions + PFNA V0 / IO  
  - Session lifecycle, NAP layers/modes, PFNA V0.  
  - Gate-driven Press window/stream config.  
  - PFNA demo scenario.

- **SPEC-004:** Press AEON/APXi views & descriptors  
  - AEON window grammar & registry.  
  - APXi descriptors + MDL.  
  - AEON/APXi demo scenario + snapshots.

> **Milestone names (suggested):**  
> - `Phase 3 — SPEC-003 Gate/TBP & PFNA V0 IO`  
> - `Phase 3 — SPEC-004 Press AEON/APXi`

### Phase 4 — SPEC-006 Multi-Graph & SLP / Dynamic Topology

- **Goal:** Run multiple graphs and evolve topology over time.  
- **Core spec:** `SPEC_006_Phase_4_Issue_Pack_v1.md`  
- **Key outcomes:**  
  - MultiGraphRunContext.  
  - SLPEvent_v1 and safe topology mutation between ticks.  
  - Loom/NAP/Press/U-ledger adapted to multi-graph + SLP.  
  - Multi-graph + SLP demo snapshots.  
  - Codex motifs for dynamic structure (observer-only).

> **Milestone name:** `Phase 4 — SPEC-006 Multi-graph & SLP V1`

### Phase 5 — SPEC-007 Governance & Codex Actioning

- **Goal:** Turn Codex from observer-only into a governed actor.  
- **Core spec:** `SPEC_007_Phase_5_Issue_Pack_v1.md`  
- **Key outcomes:**  
  - GovernanceConfig_v1, budgets, policies.  
  - Proposal evaluation engine.  
  - TBP decision loop + governed action queue.  
  - Governance-aware NAP IO and U-ledger audit hooks.  
  - Governance + Codex demo & dry-run mode.

> **Milestone name:** `Phase 5 — SPEC-007 Governance & Codex Actioning V1`

---

## 5. Dependency Graph (High-Level)

You can think of the build plan as this DAG:

- **Foundations**  
  → SPEC-002 (Phase 1)  
  → SPEC-005 (Phase 2)  
  → Phase 3 (SPEC-003 & SPEC-004 in parallel)  
  → SPEC-006 (Phase 4)  
  → SPEC-007 (Phase 5).

More explicitly:

- SPEC-002 depends on:  
  - Pillar master specs, GF-01 paper artefacts.

- SPEC-005 depends on:  
  - SPEC-002 (UMX/Loom/Press/NAP/Gate working + GF-01 parity).

- SPEC-003 depends on:  
  - SPEC-005 contexts (UMXRunContext, LoomRunContext, PressWindowContext).

- SPEC-004 depends on:  
  - SPEC-005 Press V1 and Loom (time axis).  
  - Integrates with Codex observer mode from SPEC-005.

- SPEC-006 depends on:  
  - SPEC-005 (pillars V1), SPEC-003 (Gate sessions), SPEC-004 (AEON/APXi) for richer views, plus U-ledger V1.

- SPEC-007 depends on:  
  - SPEC-006 (multi-graph + SLP),  
  - SPEC-005/003/004 (pillars, Gate, AEON/APXi),  
  - Codex motifs and proposals from prior phases.

---

## 6. How to Use This Index in the Repo

### 6.1 For Humans

When you open the repo:

1. Start here: `docs/specs/SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`.  
2. Jump from here to:
   - `spec_001_*` for conceptual overview,
   - Pillar master specs when you need detailed semantics,
   - Phase-specific specs (SPEC-002…007) when you’re working on a particular milestone,
   - Issue packs (SPEC-002, 003, 004, 006, 007 Markdown files) when you’re wiring GitHub issues.

### 6.2 For GitHub Issues

- Each SPEC-* issue pack already contains:
  - Milestone name,
  - Suggested labels,
  - Issue titles + body text.

The typical flow for a new repo is:

1. Create milestones for each phase (names above).  
2. Create labels from the packs (`spec:*`, `phase:*`, `component:*`, `type:*`, `priority:*`).  
3. For each SPEC’s issue pack, paste issues into GitHub.  
4. Optionally create GitHub Projects for each phase to track progress visually.

### 6.3 For GPT-Based Codegen (GPT 5.1 Codex etc.)

When using GPT-based tools over the repo:

- Point them at:
  - This file (SPEC-000) for global context,  
  - The relevant SPEC-* for the phase you’re working in,  
  - Pillar master specs for contract details,  
  - Contracts in `docs/contracts/` for exact types.

Keep SPEC-000 as the canonical “map” so GPT tools don’t have to rediscover structure every time.

---

## 7. Status & Versioning

- **This file:** `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`  
- **Version:** v1  
- **Owner:** Aether system architecture (Bj + Aster).  
- **Change policy:**  
  - When adding new SPECs or phases, update this file.  
  - When a SPEC’s scope changes materially, bump its version and summarise the change here.  
  - Keep this file stable enough that downstream tools can rely on it as a long-lived index.

---

End of SPEC-000.
