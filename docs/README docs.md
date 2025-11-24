# Aether Engine Docs (`docs/`)

This folder is the **source of truth** for how the engine is meant to behave.

Nothing in `src/` is allowed to contradict what’s written here. If code and docs disagree,
the docs win and the code is wrong.

---

## Layout

```text
docs/
  README.md                             ← this file
  Aether_Coding_Agent_Roles_v1.md       ← how coding agents should behave
  specs/                                ← specs, roadmaps, issue packs, pillar masters
  contracts/                            ← cross‑pillar type / record contracts
  fixtures/                             ← PDFs and paper references (GF‑01, Aether V0)
```

### `docs/specs/`

This is where all the **SPEC documents** and **pillar masters** live, including:

- `spec_000_AETHER_Spec_Index_and_Roadmap.md`
- `spec_001_aether_full_system_build_plan_medium_agnostic.md`
- `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `spec_003_Aether_v1_Full_Pillar_Roadmap.md`
- `spec_004_Dev_Workflow_and_Codex_Guide.md`
- `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `spec_006_MultiGraph_Dynamic_Topology_V1.md`
- `spec_007_Governance_Budgets_Codex_Actioning_V1.md`
- `spec_007_Phase_4_Advanced_Features_and_Master_Spec_Coverage.md`

plus:

- Pillar master specs (`UNIVERSAL_MATRIX_PILLAR_…`, `astral_press_…`, Loom, Gate, Codex).
- Coverage matrices (`*_Pillar_Coverage_Matrix_v1.md`, `ULedger_Subsystem_Coverage_Matrix_v1.md`).
- Physics and exams:
  - `Aether_CMP0_Physics_Core_and_Invariants_v1.md`
  - `GF01_V0_Exam_v1.md`
- Readiness and workflows:
  - `Aether_Paper_vs_Code_Readiness_Checklist_v1.md`
  - `Aether_PartA_Readiness_Status_v1.md`
  - `Aether_PartB_C_D_Readiness_Status_v1.md`
  - `Aether_Sprint_Plan_Phase1_v1.md`
  - `Aether_Sprint_Plan_Phase2_v1.md`
  - `Aether_Sprint_Plan_Phase3_5_v1.md`
  - `Aether_Repo_Bootstrap_Guide_v1.md`
  - `Aether_Toy_Topologies_v1.md`

There are two naming families:

- `spec_00X_*.md` — narrative specs / plans.
- `SPEC_00X_…Issue_Pack_v1.md` — concrete issue‑pack mapping for GitHub.

Use `spec_000_AETHER_Spec_Index_and_Roadmap.md` and
`SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md` as the entry points.

---

### `docs/contracts/`

This is where cross‑pillar contracts live. Each file defines a canonical record type or small
group of related types, including fields and invariants.

Examples:

- `TopologyProfile_v1.md` — graph / topology description (nodes, edges, parameters).
- `Profile_CMP0_v1.md` — numeric profile for CMP‑0 (modulus, SC, I‑block spacing, rules).
- `UMXTickLedger_v1.md` — per‑tick UMX flux ledger and edge flux records.
- `LoomBlocks_v1.md` — P‑blocks and I‑blocks for Aevum Loom.
- `APXManifest_v1.md` — APX manifests and stream descriptors.
- `PressWindowContext_v1.md` — window‑level compression context.
- `NAPEnvelope_v1.md` — NAP envelopes (Gate/TBP outputs).
- `SceneFrame_v1.md` — per‑tick integration object for Gate/TBP.
- `TickLoop_v1.md` — shape of the tick loop orchestration.
- `ULedgerEntry_v1.md` — universal ledger entries and hash linking.
- `CodexContracts_v1.md` — Codex library entries, motifs, proposals.

Helper docs:

- `Aether_Contracts_Explainer_v1.md` — how to read and use the contracts.
- `Aether_Existing_Contracts_Index_v1.md` — index of all contracts and where they’re used.
- `GF01_V0_Exam.md` — what it means to pass the GF‑01 baseline exam.

Implementation code should **not** redefine these structures. It should import/reflect them
and build types/classes around them.

---

### `docs/fixtures/`

Reference PDFs for paper parity and manual checking:

- `fixtures/gf01/` — all GF‑01 V0 binders, tick tables, APX sheets, envelope references.
- `fixtures/aether_v0/` — Aether V0 lookup booklet and paper templates.

Tests under `tests/gf01/` and `tests/snapshots/` should be written to match these fixtures.
