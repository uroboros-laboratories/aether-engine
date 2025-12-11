# Aether Engine

This repo is the **docs‑first implementation home** for the Aether engine.

The basic idea:

- All the **behaviour** lives in the docs under `docs/`.
- The **code** in `src/` is just an implementation that has to obey those docs.
- The **tests** in `tests/` keep everything honest (GF‑01 paper parity first, then generalised features).

If you’re a human or a coding agent landing here, read this in order:

 1. `docs/specs/spec_000_AETHER_Spec_Index_and_Roadmap.md`
    High‑level map of all specs and phases (SPEC‑000 .. SPEC‑007).
 2. `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`  
    The overall build plan and architecture for the full Aether system.
 3. `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
    Defines the **Phase 1** “GF‑01 CMP‑0 Baseline” engine and exactly what must be built and tested.
 4. `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
    Defines **Phase 2** “Pillar V1” generalisation work (UMX / Loom / Press / Gate / Codex / U‑ledger).

 For a novice-friendly Phase 9 CLI run sheet (commands, meanings, and a one-line "run everything" command), see `docs/phase9_novice_runsheet.md`.

 After that, use `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md` and the per‑phase issue packs
 (`SPEC_002_…Issue_Pack_v1.md` etc.) as your guide for day‑to‑day work.

 ---

 ## Layout

 ```text
 aether-engine-full/
   README.md                ← this file (root overview)
   .gitignore

   docs/                    ← all behaviour / design lives here
     README.md              ← docs overview
     Aether_Coding_Agent_Roles_v1.md
     specs/                 ← specs, roadmaps, issue packs, pillar master specs
     contracts/             ← cross‑pillar contracts (types / records / invariants)
     fixtures/              ← PDFs and paper references

   src/                     ← code implementation skeleton
     README.md              ← how to treat this tree
     core/
     umx/
     loom/
     press/
     gate/
     codex/
     uledger/

   tests/                   ← tests skeleton
     README.md
     gf01/                  ← GF‑01 CMP‑0 exam tests (Phase 1)
     integration/           ← cross‑pillar tests
     snapshots/             ← regression snapshots
     unit/                  ← low‑level unit tests
 ```

 At the moment, `src/` and `tests/` are mostly empty shells. That’s deliberate. The docs are the
 source of truth; implementation and tests are expected to *follow* them, not improvise.

 ---

 ## Pillars

 Aether is organised around five primary pillars plus one supporting subsystem:

 - **UMX** — Universal Matrix integer engine (graph + flux)
 - **Loom** — Aevum Loom time axis (chain, P‑blocks, I‑blocks, replay)
 - **Press/APX** — Astral Press compression, APX manifests, AEON/APXi
 - **Gate / TBP** — Trinity Gate, tick‑binding, NAP envelopes, PFNA inputs
 - **Codex Eterna** — observer / motif library / proposal engine
 - **U‑ledger** — universal ledger subsystem that ties pillars together (hash chain)

 The pillar master specs live here:

 - `docs/specs/UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`
 - `docs/specs/astral_press_master_implementation_spec_combined_v1.md`
 - `docs/specs/Aevum Loom Pillar — Master spec.txt`
 - `docs/specs/trinity gate full spec.txt`
 - `docs/specs/Codex Eterna — Master spec.txt`

 Coverage matrices for each pillar live under `docs/specs/*Coverage_Matrix_v1.md` and define what
 “100% of the master spec” means in practice.

 ---

 ## Phases

 The build is split into phases, each with:

 - A SPEC document (e.g. `spec_002_…`, `spec_005_…`),
 - A `SPEC_00X_…Issue_Pack_v1.md` file to map work into GitHub issues,
 - Readiness and sprint docs.

 The high‑level phase flow is:

 1. **SPEC‑002 — Phase 1: GF‑01 CMP‑0 Baseline**
    - Exact digital match of the GF‑01 V0 paper run.
    - Builds the integer physics, tick loop, and cross‑pillar wiring.
 2. **SPEC‑005 — Phase 2: Pillar V1 Generalisation**
    - UMX / Loom / Press / Gate / Codex / U‑ledger generalised beyond GF‑01.
 3. **SPEC‑006 — Phase 3: Governance, Config & Ops**
 4. **SPEC‑007 — Phase 4/5: Advanced features & full master spec coverage**

 See:

 - `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`
 - `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`
 - `docs/specs/spec_007_Governance_Budgets_Codex_Actioning_V1.md`
 - `docs/specs/spec_007_Phase_4_Advanced_Features_and_Master_Spec_Coverage.md`

 for the long‑range view.

 ---

## Where to start (for coding)

 If you are a coding agent or a dev:

 1. Read:
    - `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
    - `docs/specs/spec_002_GF01_CMP0_Baseline_Phase1_GitHub_Issues.md`
    - `docs/specs/Aether_Start_Coding_Gate_v1.md`
    - `docs/Aether_Coding_Agent_Roles_v1.md`

 2. Then focus on **Phase 1** only:
    - Implement UMX CMP‑0 + Loom + Press/APX + Gate/NAP + U‑ledger *only* to the extent needed
      to pass the GF‑01 exam.
    - Put code into `src/` and tests into `tests/gf01/` and `tests/snapshots/`.

 3. Use the issue pack to drive work:
    - Each section in `SPEC_002_…Issue_Pack_v1.md` maps cleanly to a GitHub Issue.

 Past that, move to `SPEC_005_…` for Phase 2 work.

---

## Phase 7 (Gate Operator) local dev snapshot
- Bundle the offline UI: `python scripts/build_ui_bundle.py` (honours `OPERATOR_UI_SRC`, `OPERATOR_UI_DIST`, `OPERATOR_UI_ZIP`).
- Run the Operator Service + UI together: `python scripts/run_phase7_local.py` (defaults to `127.0.0.1:8000` and `127.0.0.1:9000`; override with `OPERATOR_SERVICE_HOST`/`OPERATOR_SERVICE_PORT`/`OPERATOR_UI_HOST`/`OPERATOR_UI_PORT` or CLI flags).
- See `docs/phase7_runbook.md` for prerequisites, workflows, and troubleshooting the Phase 7 offline stack.
- See `docs/phase7_completion_report.md` for a concise Phase 7 deliverable summary and offline run instructions.
