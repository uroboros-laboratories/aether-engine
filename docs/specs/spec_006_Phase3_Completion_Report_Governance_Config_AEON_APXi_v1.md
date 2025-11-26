# SPEC-006 — Phase 3 Closeout Report  
## Governance / Config / Ops, Gate/PFNA Layering, and AEON/APXi Integration

**Status:** COMPLETE  
**Phase:** 3 — Governance / Config / Ops + Advanced Windows  
**Repo:** `aether-engine`

This document records **how Phase 3** was implemented in the repo and where the work
for each Phase 3 issue actually lives (code + tests + docs).

It is the companion to:

- `docs/specs/spec_002_Phase1_Completion_Report_GF01_CMP0_v1.md`  
  (Phase 1 / SPEC-002 — GF-01 CMP-0 baseline)
- `docs/specs/spec_005_Phase2_Completion_Report_PillarV1_v1.md`  
  (Phase 2 / SPEC-005 — Pillar V1 generalisation)

and it marks the formal close of **Phase 3**, which spans:

- **SPEC-003** — Gate / PFNA V0 external inputs and NAP layering,  
- **SPEC-004** — Press / APX extended with **AEON** windows and **APXi** descriptors,  
- **SPEC-006** — Governance, config, observability, regression, and CI.

All Phase 3 work sits *on top* of the stable Phase 1–2 engine; it does not replace the
core physics or GF‑01 paper-parity guarantees.

---

## 1. Phase 3 Goal (Recap)

Phase 3 had three intertwined goals:

1. **Gate / PFNA / NAP layering (SPEC-003)**  
   - Make external inputs first-class (PFNA V0),  
   - Formalise NAP layers (INGRESS / DATA / CTRL / EGRESS),  
   - Drive the engine through well-defined Gate/TBP session lifecycles.

2. **Press / AEON / APXi advanced windows (SPEC-004)**  
   - Introduce AEON window grammars and a registry over Press windows,  
   - Add APXi descriptors and MDL accounting,  
   - Make AEON/APXi views observable and Codex-ingestable.

3. **Governance / Config / Ops (SPEC-006, Phase 3)**  
   - Move the engine to **config‑driven runs** (RunConfig, ScenarioRegistry),  
   - Add **structured logging**, **metrics**, and **introspection APIs/CLI**,  
   - Establish **multi‑scenario regression** and **CI**.

By the end of Phase 3, you should be able to:

- Configure and run scenarios purely from **JSON configs**,
- Feed deterministic PFNA inputs and watch them appear in **INGRESS**/CTRL/EGRESS envelopes,
- See **AEON windows** and **APXi views** in manifests and Codex,
- Inspect runs via **CLI introspection**, **metrics snapshots**, and **snapshots/CI**.

---

## 2. Reference Documents

Key Phase 3 docs in the repo:

- Gate / PFNA / NAP (SPEC‑003)
  - `docs/specs/spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md`
  - `docs/specs/SPEC_003_Phase_3_Issue_Pack_v1.md`

- Press / AEON / APXi (SPEC‑004)
  - `docs/specs/spec_004_Press_APX_AEON_APXi_Advanced_Grammars_and_Windows.md`
  - `docs/specs/SPEC_004_Phase_3_Issue_Pack_v1.md` (P4.1–P4.7, implemented in Phase 3)

- Governance / Config / Ops (SPEC‑006)
  - `docs/specs/spec_006_Phase_3_Governance_Config_Ops_Implementation_Plan.md`
  - `docs/specs/SPEC_006_Phase_3_Issue_Pack_v1.md`  (P3.1.1–P3.3.3)

Supporting sprint / index docs:

- `docs/specs/SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`  
- `docs/specs/Aether_Sprint_Plan_Phase3_5_v1.md`  

---

## 3. Issue Coverage Summary

Phase 3 work was organised as:

### 3.1 SPEC‑003 (Gate / PFNA / NAP) — Issues P3.1–P3.7

Implemented issues:

- **P3.1 — Session lifecycle & TickLoop_v1 integration**

  **What:**  
  - Added `SessionConfigV1`, `SessionRunResult`, and `run_session` helpers to drive TickLoop runs from Gate/TBP with a clear session lifecycle.
  - Lifecycle emits CTRL envelopes for start/stop and aggregates per‑tick NAP envelopes.

  **Where:**  
  - Code: `src/gate/gate.py`, `src/core/tick_loop.py`, `src/core/__init__.py`  
  - Tests: `tests/unit/test_session_lifecycle.py`, `tests/unit/test_gate.py`

- **P3.2 — NAP layers & modes V1**

  **What:**  
  - Defined NAP layer/mode semantics: `INGRESS`, `DATA`, `CTRL`, `EGRESS`.  
  - Preserved existing GF‑01 default (`DATA`/`P`), added validation and helpers.  
  - Wired PFNA ingress to emit **INGRESS** envelopes per tick when inputs are applied.

  **Where:**  
  - Code: `src/gate/gate.py`, `src/core/tick_loop.py`  
  - Contracts: `docs/contracts/NAPEnvelope_v1.md` (extended with Phase 3 layer usage)  
  - Tests: `tests/unit/test_gate.py`, `tests/unit/test_session_lifecycle.py`

- **P3.3 — PFNA V0 schema & loader**

  **What:**  
  - Introduced PFNA V0 schema and loader/dumper utilities:
    - Bundle metadata, entry structure, deterministic integer sequences.  
  - Added validation for GID, tick ranges, and shape.

  **Where:**  
  - Contracts: `docs/contracts/PFNA_V0_Schema_v1.md`  
  - Code: `src/gate/gate.py` (PFNA utilities exported via `gate` package)  
  - Fixtures: `docs/fixtures/pfna/pfna_v0_demo.json`  
  - Tests: `tests/unit/test_pfna_loader.py`

- **P3.4 — PFNA→engine mapping (tick‑0 + per‑tick)**

  **What:**  
  - Reserved **tick 0** PFNA entries for initial state / parameter mapping.  
  - Applied tick‑0 PFNA vectors to the initial UMX state while preserving per‑tick ingress application.  
  - Tightened validation for mismatched GIDs and malformed tick 0 bundles.

  **Where:**  
  - Code: `src/gate/gate.py`, `src/core/tick_loop.py`  
  - Tests: `tests/unit/test_pfna_loader.py`, `tests/unit/test_session_lifecycle.py`

- **P3.5 — NAP IO wiring (EGRESS)**

  **What:**  
  - Added explicit **EGRESS** envelope generation at session end, so run results include ingress, data, control, and egress NAP traffic.  
  - Gate session aggregation preserves lifecycle ordering and chain references.

  **Where:**  
  - Code: `src/core/tick_loop.py`, `src/gate/gate.py`  
  - Tests: `tests/unit/test_gate.py`, `tests/unit/test_session_lifecycle.py`

- **P3.6 — Gate/TBP + Press window/stream config**

  **What:**  
  - Introduced `PressStreamSpecV1` and `SessionConfigV1` wiring so window/stream selection is config‑driven instead of hard‑coded.  
  - Taught TickLoop to:
    - Resolve window/stream configs,
    - Register streams with `PressWindowContextV1`,
    - Route deltas, fluxes, states, and chain‑derived streams according to config.

  **Where:**  
  - Code: `src/core/tick_loop.py`, `src/press/press.py`  
  - Contracts: `docs/contracts/PressWindowContext_v1.md` (stream spec references)  
  - Tests: `tests/unit/test_press.py`, `tests/unit/test_session_lifecycle.py`

- **P3.7 — PFNA end‑to‑end scenario & snapshot**

  **What:**  
  - Added a PFNA V0 demo scenario wiring PFNA inputs into a full session, including ingress/egress layers and deterministic artefacts.  
  - Implemented JSON dump helpers for sessions and captured a canonical PFNA snapshot.

  **Where:**  
  - Code: `src/core/tick_loop.py`, `src/ops/snapshots.py`, `src/ops/metrics.py`  
  - Fixtures: `tests/snapshots/pfna_v0_demo_snapshot.json`  
  - Tests: `tests/integration/test_pfna_v0_demo_snapshot.py`

---

### 3.2 SPEC‑004 (AEON / APXi) — Issues P4.1–P4.7

Although numbered `P4.*` in the issue pack, these were implemented **in Phase 3** as planned.

- **P4.1 — AEON window grammar contracts**

  **Where:**  
  - Contracts: `docs/contracts/AEONWindowGrammar_v1.md`  
  - Code: `src/press/aeon.py`  
  - Tests: `tests/unit/test_aeon_window_grammar.py`

- **P4.2 — AEON window registry & query API**

  **Where:**  
  - Code: `src/press/aeon.py`  
  - Tests: `tests/unit/test_aeon_registry.py`

- **P4.3 — APXiDescriptor_v1 contracts**

  **Where:**  
  - Contracts: `docs/contracts/APXiDescriptor_v1.md`  
  - Code: `src/press/apxi.py`  
  - Tests: `tests/unit/test_apxi_descriptor.py`

- **P4.4 — APXi MDL accounting & residual handling**

  **Where:**  
  - Code: `src/press/apxi.py`  
  - Tests: `tests/unit/test_apxi_mdl.py`

- **P4.5 — AEON/APXi integration with PressWindowContext**

  **Where:**  
  - Code: `src/press/press.py`, `src/core/tick_loop.py`  
  - Contracts: `docs/contracts/APXManifest_v1.md` (APXi view references)  
  - Tests: `tests/unit/test_press.py`, `tests/integration/test_aeon_apxi_demo_snapshot.py`

- **P4.6 — AEON/APXi demo & snapshot**

  **Where:**  
  - Fixtures: `tests/snapshots/aeon_apxi_demo/aeon_apxi_demo_snapshot.json`  
  - Tests: `tests/integration/test_aeon_apxi_demo_snapshot.py`

- **P4.7 — Codex ingest of AEON/APXi artefacts**

  **Where:**  
  - Code: `src/codex/context.py`  
  - Tests: `tests/unit/test_codex_context.py`

---

### 3.3 SPEC‑006 (Governance / Config / Ops / CI) — Issues P3.1.1–P3.3.3

#### Config & profiles (P3.1.1–P3.1.4)

- **RunConfig & profile schema (P3.1.1, P3.1.2)**  
  - Contracts: `docs/contracts/RunConfig_v1.md`  
  - Code: `src/config/schemas.py`, `src/config/__init__.py`  
  - Fixtures: `docs/fixtures/configs/*.json`, `docs/fixtures/profiles/*.json`  
  - Tests: `tests/unit/test_run_config_schema.py`, `tests/unit/test_config_loader.py`

- **Scenario registry (P3.1.3)**  
  - Contracts: `docs/contracts/ScenarioRegistry_v1.md`  
  - Fixtures: `docs/fixtures/scenarios/scenario_registry.json`  
  - Code: `src/config/schemas.py`  
  - Tests: `tests/unit/test_scenario_registry.py`

- **Multi‑profile support (P3.1.4)**  
  - Fixtures: `profile_cmp1.json`, `profile_cmp2.json`, and matching run configs  
  - Code: `src/umx/profile_cmp0.py`, `src/config/schemas.py`  
  - Tests: `tests/unit/test_config_loader.py`, `tests/unit/test_run_config_schema.py`

#### Observability (P3.2.1–P3.2.4)

- **Structured logging (P3.2.1)**  
  - Contracts: `docs/contracts/StructuredLogging_v1.md`  
  - Code: `src/ops/structured_logging.py`, logging config wiring in `src/core/tick_loop.py` and `src/gate/gate.py`  
  - Fixtures: `docs/fixtures/configs/gf01_run_config_logging.json`  
  - Tests: `tests/unit/test_structured_logging.py`

- **Metrics (P3.2.2)**  
  - Contracts: `docs/contracts/Metrics_v1.md`  
  - Code: `src/ops/metrics.py`  
  - Fixtures: `docs/fixtures/configs/gf01_run_config_metrics.json`  
  - Tests: `tests/unit/test_metrics.py`

- **Introspection APIs (P3.2.3)**  
  - Contracts: `docs/contracts/Introspection_v1.md`  
  - Code: `src/ops/introspection.py`  
  - Tests: `tests/unit/test_introspection.py`

- **Introspection CLI (P3.2.4)**  
  - Code: `src/cli.py`  
  - Docs: `docs/ops/introspection_cli.md`  
  - Tests: `tests/unit/test_cli.py`

#### Regression & CI (P3.3.1–P3.3.3)

- **Multi‑scenario regression suite (P3.3.1)**  
  - Fixtures:  
    - `tests/snapshots/line_4_run_snapshot.json`  
    - `tests/snapshots/ring_5_run_snapshot.json`  
  - Tests: `tests/integration/test_multi_scenario_regressions.py`

- **Snapshot management tooling (P3.3.2)**  
  - Code: `src/ops/snapshots.py`  
  - Docs: `docs/ops/snapshot_tooling.md`  
  - Tests: `tests/unit/test_snapshot_tooling.py`

- **CI configuration (P3.3.3)**  
  - Workflow: `.github/workflows/ci.yml`  
  - Docs: `docs/ops/ci.md`  

---

## 4. Determinism, Invariants, and CI

Throughout Phase 3:

- The **integer‑only physics core** (UMX / Loom / Press) remains consistent with Phase 1–2.  
- All new PFNA, AEON, APXi, config, metrics, and logging features are **deterministic**:
  - Snapshot tests verify that repeated runs with the same config produce bytewise‑identical artefacts.
- The CI workflow `.github/workflows/ci.yml` runs the full `pytest` suite on pushes and PRs, enforcing:
  - GF‑01 baseline parity,
  - Multi‑topology regressions,
  - PFNA and AEON/APXi snapshots,
  - Config/ops tests.

---

## 5. How to Use the Phase 3 Engine

Common operations now look like:

- **Run a scenario from the registry (no coding):**  
  - Via Python: load a `ScenarioRegistry_v1`, resolve a `RunConfig_v1`, and call the corresponding run helper.  
  - Via CLI: use the scenario/run‑config options exported from `src/cli.py` (see `docs/ops/introspection_cli.md`).

- **Inspect a run:**  
  - Use the **introspection CLI** or `IntrospectionViewV1` APIs to fetch:  
    - UMX ledgers and Loom blocks,  
    - NAP envelopes (by layer),  
    - AEON windows and APXi views,  
    - U‑ledger entries.

- **Manage snapshots:**  
  - Use snapshot tooling to generate/compare JSON snapshots for new scenarios.  
  - Store them under `tests/snapshots/` to extend regression coverage.

- **Observe behaviour:**  
  - Enable logging and metrics via RunConfig fields; outputs are included in session serialisation.

---

## 6. Phase 3 Status

- All planned Phase 3 issues from:
  - `SPEC_003_Phase_3_Issue_Pack_v1.md` (P3.1–P3.7),  
  - `SPEC_004_Phase_3_Issue_Pack_v1.md` (P4.1–P4.7, implemented as part of Phase 3),  
  - `SPEC_006_Phase_3_Issue_Pack_v1.md` (P3.1.1–P3.3.3),

  are **implemented in code, covered by tests, and green under CI.**

This document is the Phase 3 close marker.  
From here, work moves into **Phase 4 / SPEC‑007** (budgets, Codex‑driven actioning, and deeper topology/governance features) using this repo state as the stable base.
