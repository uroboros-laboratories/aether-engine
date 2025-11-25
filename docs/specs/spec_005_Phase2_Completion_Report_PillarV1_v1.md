# SPEC-005 — Phase 2 Closeout Report  
## Pillar V1 Generalisation (UMX / Loom / Press / Gate / U-ledger / Codex)

**Status:** COMPLETE  
**Phase:** 2 — SPEC-005 Pillar V1 Generalisation  
**Repo:** `aether-engine`

This document records **how Phase 2 (SPEC-005)** was implemented in the repo and where the work
for each SPEC-005 issue actually lives (code + tests + docs).

It is the companion to:

- `docs/specs/spec_002_Phase1_Completion_Report_GF01_CMP0_v1.md`  
  (Phase 1 / SPEC-002 — GF-01 CMP-0 baseline)
- and it marks the formal close of **Phase 2 — Pillar V1 Generalisation**.

---

## 1. Phase 2 Goal (SPEC-005 Recap)

**SPEC-005 Name:** Phase 2 — Pillar V1 Generalisation  

Phase 1 (SPEC-002) delivered:

- A working, deterministic, **paper-parity GF-01 CMP-0 engine**,
- With UMX, Loom, Press, Gate/NAP wired end-to-end,
- And a determinism harness + snapshot for the GF-01 scenario.

Phase 2 (SPEC-005) lifts that into **reusable, generalised V1 pillars**:

- UMX V1: multiple topologies, reusable run context, diagnostics.
- Loom V1: time-axis context, configurable chain rules, replay API.
- Press/APX V1: stream registry, multiple schemes (ID/R/GR), generalised manifests.
- Gate/TBP V1: SceneFrame as the canonical integration object, richer NAP semantics, PFNA path.
- U-ledger V1: canonical serialisation + hash-chain entries.
- Codex V1: observer-only context, motif identification, proposal emission.

**Phase 2 is considered complete** when:

- All SPEC-005 issues (P2.1.1–P2.6.3) have concrete implementation in `src/`,  
- Corresponding tests live under `tests/`, and  
- The full test suite passes (including GF-01 determinism and new multi-topology runs).

---

## 2. Reference Documents

Key docs for Phase 2 in the repo:

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`  
  – The narrative implementation plan for Pillar V1 generalisation.
- `docs/specs/spec_005_Phase2_Pillar_V1_GitHub_Issues.md`  
  – The SPEC-005 issue pack used to create GitHub issues P2.1.1–P2.6.3.
- `docs/specs/Aether_Sprint_Plan_Phase2_v1.md`  
  – Phase 2 sprint planning and ordering guidance.
- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`  
  – Where Phase 2 sits in the broader roadmap.
- `docs/specs/spec_000_AETHER_Spec_Index_and_Roadmap.md`  
  – Index of specs and phases.
- `docs/specs/spec_002_Phase1_Completion_Report_GF01_CMP0_v1.md`  
  – Phase 1 closeout report (baseline context).

The rest of this doc maps **SPEC-005 issues** to actual implementation and tests.

---

## 3. EPIC P2.1 — UMX V1 (General Integer Engine)

### P2.1.1 — TopologyProfile Loader & Validator

**Spec:** TopologyProfile loader & validator (multi-topology support).  

**What it required:**

- Ability to load `TopologyProfile_v1` from fixtures/config, not just hard-coded GF-01.
- Strict validation:
  - Node IDs contiguous `[1..N]`,
  - Edge IDs contiguous `[1..E]`,
  - Edge endpoints within `[1..N]`,
  - Integer parameters with valid ranges.
- Example topologies: GF-01, plus at least line/ring/star graphs.

**Implementation:**

- `src/umx/topology_profile.py`
  - Defines `TopologyProfileV1`, `NodeProfileV1`, `EdgeProfileV1`.
  - Implements a **JSON-based loader**:
    - `load_topology_profile(path: Path) -> TopologyProfileV1`.
  - Performs strict validation as per the contract and SPEC-005.
  - Provides helpers for built-in fixtures (GF-01, line, ring, star).

**Tests:**

- `tests/unit/test_topology_profile.py`
  - Loads GF-01, line, ring, star fixture files.
  - Asserts node and edge ranges, contiguity, and endpoint correctness.
  - Checks malformed profiles raise clear `ValueError`s.

**Status:** COMPLETE. Topology profiles are now reusable and multi-topology ready.

---

### P2.1.2 — UMXRunContext (Multi-Run Support)

**Spec:** UMXRunContext for multi-run UMX V1 engine.

**What it required:**

- Reusable `UMXRunContext` abstraction:
  - Holds topology, profile, state, tick, run metadata.
- Methods for:
  - Initialising state from `u(0)`,
  - Stepping a single tick,
  - Running to a target tick.
- No global mutable state.

**Implementation:**

- `src/umx/run_context.py`
  - Defines `UMXRunContext` with:
    - `topology: TopologyProfileV1`
    - `profile: ProfileCMP0V1`
    - `state: list[int]` (current `u(t)`)
    - `tick: int`
    - `gid`, `run_id`, and optional diagnostics config.
  - Methods:
    - `init_state(u0: list[int])`
    - `step() -> UMXTickLedgerV1`
    - `run_until(t_max: int) -> list[UMXTickLedgerV1]`

- `src/umx/engine.py`
  - Exposes the underlying CMP-0 flux stepping used by `UMXRunContext`.

- `src/core/tick_loop.py`
  - Refactored GF-01 run to use `UMXRunContext` rather than hard-coded per-tick logic.

**Tests:**

- `tests/unit/test_umx_engine.py`
  - Validates per-tick UMX stepping for GF-01 (regression back to Phase 1).
- `tests/unit/test_umx_run_context.py`
  - Verifies init/step/run behaviour of `UMXRunContext`.
  - Includes non-GF-01 topologies (e.g., line topology).

**Status:** COMPLETE. UMX runs are now managed by a reusable, multi-topology run context.

---

### P2.1.3 — CMP-0 Generalised Tick Stepping

**Spec:** Generalise CMP-0 UMX tick stepping across topologies.

**What it required:**

- Ensure CMP-0 stepping uses topology/profile parameters, not GF-01 assumptions.
- Regression coverage on non-GF-01 graphs (line, ring, star).
- Conservation and determinism across all tested graphs.

**Implementation:**

- `src/umx/engine.py`
  - CMP-0 `step` now routes through:
    - Topology’s edge list (with shared scale constant),
    - Profile’s CMP-0 parameter set.
  - Ensures a shared scale constant is enforced across edges for a given topology/profile pair.

**Tests:**

- `tests/unit/test_umx_engine.py`
  - GF-01 conservation and correctness.
- `tests/unit/test_umx_run_context.py`
  - Line/ring/star stepping tests:
    - Conservation (`sum_pre_u == sum_post_u`).
    - Deterministic outputs via double-run parity.

**Status:** COMPLETE. CMP-0 stepping is generalised and tested beyond GF-01.

---

### P2.1.4 — UMX Diagnostics & Invariants

**Spec:** UMX diagnostics & invariant checks.

**What it required:**

- Optional diagnostics mode to record:
  - Conservation checks,
  - Min/max node values,
  - Negative value/overflow checks,
  - Violation flags or exceptions.
- Diagnostics must not change core state evolution.

**Implementation:**

- `src/umx/diagnostics.py`
  - Defines `UMXDiagnosticsConfig` (toggle behaviour, raise-or-log) and `UMXDiagnosticsRecord`.
  - Helpers to compute diagnostics for a tick ledger.

- `src/umx/run_context.py`
  - Accepts diagnostics config.
  - Records diagnostics records per tick when enabled.

**Tests:**

- `tests/unit/test_umx_diagnostics.py`
  - Verifies diagnostics-on/off parity (core outputs unchanged).
  - Validates that invariant violations are reported and/or raise when configured.

**Status:** COMPLETE. UMX diagnostics exist and are fully optional and deterministic.

---

## 4. EPIC P2.2 — Loom V1 (Time Axis & Replay)

### P2.2.1 — LoomRunContext

**Spec:** LoomRunContext for time axis & blocks.

**What it required:**

- `LoomRunContext` to manage:
  - Current chain value `C_t`,
  - P-/I-block sequences,
  - Tight coupling to UMX ticks (via tick ledgers).

**Implementation:**

- `src/loom/run_context.py`
  - Defines `LoomRunContext` with:
    - Reference to a tick ledger source / UMXRunContext.
    - Current `C_t`, configuration for `W`, `s_t` rule, `seq_t` rule.
    - Internal storage of P-blocks and I-blocks.
  - Methods:
    - `ingest_tick(ledger: UMXTickLedgerV1) -> LoomPBlockV1`
    - Optional I-block emission according to `W`.
    - `run_until(t_max)` to drive through a sequence of ticks.

- `src/loom/loom.py`
  - Contains the core chain update math and block dataclasses used by the run context.

**Tests:**

- `tests/unit/test_loom.py`
  - GF-01 reproduction using LoomRunContext.
  - Line-topology test to show non-GF-01 compatibility.

**Status:** COMPLETE. Loom has a dedicated run context that tracks chain + blocks.

---

### P2.2.2 — Configurable I-block Spacing & s_t Rule

**Spec:** Configurable Loom I-block spacing & s_t rule.

**What it required:**

- Ability to configure:
  - `W` (I-block spacing),
  - `s_t` rule (constant for GF-01, plus at least one derived rule).

**Implementation:**

- `src/loom/run_context.py` + `src/loom/loom.py`
  - `LoomRunContext` accepts spacing and s_t mode from profile/config.
  - CMP-0 s_t computation supports:
    - Constant `s_t = 9` for GF-01.
    - A simple derived `s_t` (e.g. sum of absolute fluxes) per spec.

**Tests:**

- `tests/unit/test_loom.py`
  - GF-01 regression with `s_t = 9`, `W = 8`.
  - A derived s_t rule scenario using a small topology.
  - Tests for non-default spacing `W` and deterministic outputs.

**Status:** COMPLETE. Loom supports configurable checkpoint spacing and s_t modes.

---

### P2.2.3 — Loom Replay API

**Spec:** Loom replay API (get_chain_at, replay_state_at).

**What it required:**

- APIs to query chain and replay state:
  - `get_chain_at(t) -> C_t`,
  - I-block lookup for a given tick,
  - `replay_state_at(t)` using nearest prior I-block + UMX replay.

**Implementation:**

- `src/loom/run_context.py`
  - Stores ingested ledgers alongside P-/I-blocks.
  - Provides:
    - `get_chain_at(t: int) -> int`,
    - `get_pblock(t: int) -> LoomPBlockV1`,
    - `get_iblock_for(t: int) -> LoomIBlockV1`,
    - `replay_state_at(t: int) -> list[int]`:
      - Finds nearest I-block,
      - Applies UMX stepping from checkpoint to target tick.

**Tests:**

- `tests/unit/test_loom.py`
  - GF-01 replay parity: replayed state at `t = 1..8` equals original `post_u` from UMX.
  - Line-topology scenario verifying replay correctness and determinism.

**Status:** COMPLETE. Loom supports deterministic replay for chain and state.

---

## 5. EPIC P2.3 — Press/APX V1 (Stream Registry & Modes)

### P2.3.1 — PressWindowContext & Stream Registry

**Spec:** PressWindowContext & stream registry.

**What it required:**

- Window-level context keyed by `(gid, window_id)`.
- Multiple named streams per window.
- Tick-aligned buffering and manifest generation at window close.

**Implementation:**

- `src/press/press.py`
  - `PressStreamBufferV1` and `PressWindowContextV1`:
    - `register_stream(name, scheme_hint, description)`.
    - `append(name, value)` with integer validation.
    - `close_window(apx_name, profile)`:
      - Validates that each stream has the right number of ticks.
      - Computes per-stream length stats.
      - Builds `APXManifestV1` and optionally resets buffers.

**Tests:**

- `tests/unit/test_press.py`
  - GF-01 windows (1–8, 1–2) using the context.
  - Tests for incomplete streams, width mismatches, invalid inputs.
  - Ensures GF-01 manifest outputs remain identical to Phase 1 expectations.

**Status:** COMPLETE. Press has a robust window context and stream registry.

---

### P2.3.2 — ID, R, and Basic GR Schemes

**Spec:** Implement ID, R, and basic GR schemes in Press/APX.

**What it required:**

- Scheme implementations:
  - ID (identity),
  - R (run-length-like),
  - GR (simple grouped R).
- Deterministic `L_model`, `L_residual`, `L_total` for integer sequences.

**Implementation:**

- `src/press/press.py`
  - Scheme dispatch integrated into `PressWindowContextV1`:
    - Validates `scheme` ∈ {`"ID"`, `"R"`, `"GR"`}.
    - Calls scheme-specific calculators for each stream:
      - ID: raw bit-count behaviour.
      - R: run-length behaviour (GF-01 default).
      - GR: grouped variant as per SPEC-005 heuristic.

**Tests:**

- `tests/unit/test_press.py`
  - Sequence-level tests for each scheme.
  - Guard tests for width mismatches and invalid scheme values.
  - Regression tests to ensure GF-01 R-mode behaviour is unchanged.

**Status:** COMPLETE. ID, R, and GR are all present and tested.

---

### P2.3.3 — Generalised APXManifest Generation

**Spec:** Generalised `APXManifest_v1` creation.

**What it required:**

- Manifests supporting:
  - Arbitrary number of streams,
  - Mixed schemes,
  - Deterministic `manifest_check` based on all relevant fields.

**Implementation:**

- `src/press/press.py`
  - `APXManifestV1` extended to carry:
    - Stream definitions (name, scheme, lengths).
    - Per-stream `L_model`, `L_residual`, `L_total`.
  - `compute_manifest_check` uses a deterministic hash over all manifest fields, including stream definitions and profile identifiers.

**Tests:**

- `tests/unit/test_press.py`
  - Multi-stream, mixed-scheme windows (ID+R+GR together).
  - Checks that `manifest_check` responds to stream/scheme changes.
  - Ensures GF-01 checks remain exactly as in Phase 1.

**Status:** COMPLETE. Manifests are generalised and stable.

---

## 6. EPIC P2.4 — Gate/TBP V1 (Scenes & Layers)

### P2.4.1 — SceneFrame_v1 as Primary Integration Object

**Spec:** SceneFrame_v1 as primary integration object.

**What it required:**

- Refactor tick loop so SceneFrame is the canonical per-tick bundle:
  - UMX state,
  - Loom chain values,
  - Press/APX window references,
  - NAP envelope metadata.

**Implementation:**

- `src/core/tick_loop.py`
  - CMP-0 tick loop refactored to build `SceneFrameV1` each tick.
  - Exposes helpers to run windows and attach manifest references.

- `src/gate/gate.py`
  - `SceneFrameV1` dataclass extended to carry:
    - P-block references,
    - APX manifest references,
    - PFNA metadata (Phase 2 addition).

**Tests:**

- `tests/gf01/test_run_gf01.py`
  - Updated to assert GF-01 scene frames contain expected fields and references.
- `tests/unit/test_gate.py`
  - SceneFrame-level checks outside the GF-01 specific run.

**Status:** COMPLETE. SceneFrame is now the canonical integration object in the tick loop.

---

### P2.4.2 — NAP Layers & Modes

**Spec:** NAP layers & modes (beyond DATA/P).

**What it required:**

- Layer semantics: INGRESS, DATA, CTRL, EGRESS.
- Mode semantics: at least P + one secondary type.
- Keep GF-01 still using DATA/P.

**Implementation:**

- `src/gate/gate.py`
  - Defines allowed NAP layers/modes as constants.
  - `emit_nap_envelope` validates requested layer/mode:
    - Defaults to profile’s `nap_defaults` (DATA/P for CMP-0).
    - Allows override for CTRL envelopes (and other layers) in configured scenarios.

**Tests:**

- `tests/unit/test_gate.py`
  - Ensures GF-01 remains DATA/P by default.
  - Adds cases for CTRL-layer envelopes and invalid layer/mode rejections.

**Status:** COMPLETE. NAP layers/modes exist and are enforced at construction time.

---

### P2.4.3 — PFNA Placeholder for External Inputs

**Spec:** PFNA placeholder for deterministic external inputs.

**What it required:**

- Minimal PFNA-like structure.
- Deterministic path:
  - External integer sequences → PFNA → Gate → Scene/UMX adjustment.

**Implementation:**

- `src/gate/gate.py`
  - Adds `PFNAInputV0` wrapper and helpers.
  - SceneFrame metadata extended with `pfna_refs`.

- `src/core/tick_loop.py`
  - CMP-0 tick loop optionally accepts PFNA inputs.
  - Applies deterministic state deltas to UMX initial state before each tick (or per window) according to PFNA configuration.

- `src/umx/run_context.py`
  - Provides helper to apply external input vectors safely.

**Tests:**

- `tests/unit/test_gate.py`
  - PFNA tests confirming that external inputs affect pre_u deterministically and are recorded on scenes.

**Status:** COMPLETE. PFNA placeholder path exists and is wired into the tick loop.

---

## 7. EPIC P2.5 — U-ledger V1

### P2.5.1 — Canonical Serialisation & Hashing

**Spec:** Canonical serialisation & hashing for U-ledger.

**What it required:**

- Canonical JSON rules (key ordering, numeric formats, whitespace).
- A fixed hash algorithm (SHA-256).
- `hash_record(record) -> hash_string` utility.

**Implementation:**

- `src/uledger/canonical.py`
  - Implements canonical JSON normalisation:
    - Dict key ordering,
    - Stable handling for dataclasses/tuples,
    - UTF-8 encoding.
  - Provides `hash_record(record)` using SHA-256 over canonical bytes.

**Tests:**

- `tests/unit/test_uledger_canonical.py`
  - Verifies that the same record always yields the same bytes and hash.
  - Ensures mutations change the hash.
  - Tests mixed input types (dicts, dataclasses, nested structures).

**Status:** COMPLETE. Canonical serialisation and hashing are stable and documented.

---

### P2.5.2 — ULedgerEntry Construction

**Spec:** Construct ULedgerEntry_v1 per tick/window.

**What it required:**

- U-ledger entry tying together:
  - UMX tick ledger hash,
  - Loom block hash,
  - APX manifest hash,
  - NAP envelope hash,
  - Chain value and manifest_check,
  - Previous entry hash.

**Implementation:**

- `src/uledger/entry.py`
  - Defines `ULedgerEntryV1` dataclass.
  - Builder functions:
    - Compute hashes of pillar artefacts via `hash_record`.
    - Enforce tick and window ordering.
    - Chain entries via `prev_entry_hash`.

- `src/core/tick_loop.py`
  - CMP-0 runner updated to:
    - Record `run_id`,
    - Emit per-tick U-ledger entries from scene + pillar outputs.

- `src/core/serialization.py`
  - Updated GF-01 serialisation to include U-ledger entries in the snapshot.

**Tests:**

- `tests/unit/test_uledger_entry.py`
  - Verifies U-ledger chain stability and mutation sensitivity.
- `tests/gf01/test_determinism_snapshot.py`
  - Ensures GF-01 snapshot includes ledger entries and that re-runs match exactly.

**Status:** COMPLETE. U-ledger entries and hash chain are implemented and tested.

---

## 8. EPIC P2.6 — Codex V1 (Observer-Only)

### P2.6.1 — CodexContext & Data Ingest

**Spec:** CodexContext & data ingest (observer mode).

**What it required:**

- `CodexContext` to ingest engine traces (UMX, Loom, Press, NAP).
- Observer-only behaviour (no structural changes).

**Implementation:**

- `src/codex/context.py`
  - Defines `CodexContext` and `CodexLibraryEntryV1` skeleton.
  - Ingest methods for:
    - UMX tick ledgers,
    - Loom P-/I-blocks,
    - APX manifests,
    - NAP envelopes (optional).
  - Gathers basic stats and alignment checks.

**Tests:**

- `tests/unit/test_codex_context.py`
  - GF-01 ingestion without errors.
  - Alignment validation and per-edge/ledger counting.

**Status:** COMPLETE. Codex can ingest data as an observer-only component.

---

### P2.6.2 — Motif Identification (Simple Heuristics)

**Spec:** Codex motif identification (simple heuristics).

**What it required:**

- Simple heuristic motif detection (e.g. repeated flux patterns).
- Generation of `CodexLibraryEntry_v1` with basic MDL/usage stats.
- Determinism across runs.

**Implementation:**

- `src/codex/context.py`
  - Motif learner that:
    - Builds tick-aligned signatures from flux patterns.
    - Creates deduplicated `edge_flux_pattern_v1` motifs.
    - Tracks MDL-like and usage statistics.

**Tests:**

- `tests/unit/test_codex_context.py`
  - GF-01 and synthetic scenarios:
    - Confirm motifs are discovered deterministically.
    - Confirm library content is stable across re-runs.

**Status:** COMPLETE. Codex identifies deterministic motifs from traces.

---

### P2.6.3 — Proposal Emission (Observer-Only)

**Spec:** Codex proposal emission (observer-only).

**What it required:**

- `CodexProposal_v1` records.
- Deterministic proposal emission from learned motifs.
- No engine behaviour changes yet (observer-only).

**Implementation:**

- `src/codex/context.py`
  - Defines `CodexProposalV1`.
  - `emit_proposals(...)` helper:
    - Emits PLACE/PENDING proposals based on motif thresholds.
    - Deduplicates by motif/window.

**Tests:**

- `tests/unit/test_codex_context.py`
  - GF-01 and synthetic runs:
    - Proposal creation, thresholds, repeatability.
    - Confirms proposals do not alter engine outputs.

**Status:** COMPLETE. Codex can emit deterministic proposals while remaining observer-only.

---

## 9. How to Verify Phase 2 (for Humans / Agents)

Phase 2 verification = **all SPEC-005 tests passing**.

Typical command (from repo root):

```bash
python -m pytest
```

This exercises:

- Phase-1 and Phase-2 unit tests under `tests/unit/`,
- GF-01 end-to-end runs and determinism under `tests/gf01/`,
- New multi-topology scenarios and Codex/U-ledger behaviour.

A green test run confirms that:

- UMX, Loom, Press, Gate/NAP, U-ledger, and Codex V1 features are all coherent.
- GF-01 behaviour is preserved (snapshot tests).
- New Phase 2 generalisation features behave deterministically.

---

## 10. Boundaries and Known Limitations (Post-Phase 2)

Even after Phase 2, the system is intentionally constrained:

- **Profile:** Only CMP-0 is implemented (no alternate physics profiles yet).
- **Scale:** Topologies are small/medium; large-scale performance is not tuned.
- **PFNA:** Placeholder only, not full external-signal grammar.
- **Codex:** Observer-only; proposals are emitted but not yet applied to topology or parameters.
- **Governance:** Rich governance/budget policies remain out of scope until later specs.

These constraints align with:

- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`

Later phases will:
- Introduce new profiles and richer Gate/TBP semantics.
- Extend Codex from observer to governed actor (with guardrails).
- Expand PFNA and external integration.

---

## 11. Phase 2 → Next Phase Handover

With Phase 2 complete:

- All major pillars now have **V1 generalised implementations**:
  - UMX V1 (multi-topology + diagnostics),
  - Loom V1 (context + replay),
  - Press/APX V1 (ID/R/GR + manifests),
  - Gate/TBP V1 (SceneFrame, NAP layers, PFNA placeholder),
  - U-ledger V1 (hash-chain),
  - Codex V1 (observer-only motifs + proposals).
- GF-01 CMP-0 remains the canonical baseline, but the engine is no longer GF-01-only.

The next phase (as outlined in the roadmap specs) is expected to focus on:

- Extending profiles, PFNA, and Gate/TBP for richer external input.
- Moving Codex from “observer-only” to governed participation (structural proposals applied under constraints).
- Strengthening governance and budgeting layers around U-ledger and Codex.

**Recommended docs to open when starting the next phase:**

- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`
- Any subsequent SPEC documents (e.g. Phase 3/4 plans) as they are added.

---

## 12. File Placement

Suggested location for this closeout report in the repo:

- `docs/specs/spec_005_Phase2_Completion_Report_PillarV1_v1.md`

You can rename it if you prefer a different naming scheme, but keeping the `spec_005_...` prefix and “Phase2_Completion” suffix makes it easy to discover alongside the other Phase 2 docs.

---

**Phase 2 (SPEC-005) is now considered CLOSED.**  
The repo is ready to proceed to the next planned phase in the Aether roadmap.
