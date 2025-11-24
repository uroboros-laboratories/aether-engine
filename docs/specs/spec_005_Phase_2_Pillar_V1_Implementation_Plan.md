# SPEC-005 — Phase 2 Pillar V1 Implementation Plan

## Status

- **Spec ID:** SPEC-005
- **Name:** Phase 2 Pillar V1 Implementation Plan
- **Version:** v1
- **Scope:** UMX V1, Loom V1, Press/APX V1, Gate/TBP V1, U-ledger V1, Codex V1 (observer-only)
- **Assumes:**
  - SPEC-002 (GF-01 CMP-0 Baseline Build Plan) is implemented and passing.
  - SPEC-003 (Aether v1 Full Pillar Implementation Roadmap) is accepted as the high-level roadmap.
  - SPEC-004 (Dev Workflow & Codex Guide) is in force for all development.

---

## 1. Purpose & Context

SPEC-002 delivered a **minimal working engine**:

- One topology (GF-01),
- One numeric profile (CMP-0),
- One scenario (ticks 1–8),
- Paper parity enforced by tests.

SPEC-005 defines **Phase 2**: upgrading the pillars from “GF-01-only” to **Pillar V1**:

- Multiple topologies (still CMP-0 for now),
- Reusable run contexts,
- Proper time axis & replay,
- Real APX stream registry & modes,
- A universal ledger tying everything together,
- Codex wired in as an observer-only learner.

This phase does **not** try to cover every advanced feature in the master specs. Instead, it delivers a robust, reusable V1 implementation of each pillar that:

- Still respects all GF-01 constraints,
- Is driven by the existing contracts in `docs/contracts/`,
- Matches the intent of the pillar master specs at a first usable level.

Phase 3 and 4 (SPEC-006, SPEC-007, etc.) will handle governance, ops, and advanced features.

---

## 2. Reference Documents

### 2.1 Specs

- `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`
- `docs/specs/spec_004_Dev_Workflow_and_Codex_Guide.md`
- `docs/specs/<pillar master specs>.md` for:
  - Trinity Gate / TBP
  - Astral Press
  - Aevum Loom
  - Universal Matrix
  - Codex Eterna

### 2.2 Contracts

Phase 2 builds directly on these contracts:

- `UMXTickLedger_v1.md`
- `LoomBlocks_v1.md`
- `APXManifest_v1.md`
- `NAPEnvelope_v1.md`
- `TopologyProfile_v1.md`
- `Profile_CMP0_v1.md`
- `TickLoop_v1.md`
- `SceneFrame_v1.md`
- `ULedgerEntry_v1.md`
- `CodexContracts_v1.md`

---

## 3. Phase Scope (What “Pillar V1” Means)

For each pillar, Phase 2 aims for:

- **UMX V1** — General integer engine for arbitrary small/medium graphs under CMP-0:
  - Multiple topologies via `TopologyProfile_v1`.
  - Reusable `UMXRunContext`.
  - Conservation and determinism across all runs.

- **Loom V1** — Time axis and replay:
  - `LoomRunContext` that tracks `C_t` and blocks.
  - Configurable I-block spacing.
  - Replay API to reconstruct state at arbitrary ticks.

- **Press/APX V1** — Stream registry and basic schemes:
  - Named streams per run/window.
  - ID/R/GR basic schemes.
  - Consistent `APXManifest_v1` for arbitrary windows.

- **Gate/TBP V1** — Scenes and layers:
  - `SceneFrame_v1` as the integration backbone.
  - NAP envelopes across basic layers (DATA, CTRL, INGRESS/EGRESS).
  - Simple PFNA placeholders for external inputs.

- **U-ledger V1** — Global commit chain:
  - `ULedgerEntry_v1` for each tick/window.
  - Canonical hash chain over pillars.

- **Codex V1** — Observer-only learner:
  - `CodexLibraryEntry_v1` and `CodexProposal_v1` populated from traces.
  - No structural changes applied yet.

---

## 4. EPIC P2.1 — UMX V1 (General Integer Engine)

### 4.1 Epic Goal

Generalise UMX from a “GF-01-only” engine into a reusable integer engine that can:

- Load arbitrary topologies via `TopologyProfile_v1`,
- Run one or more independent UMX runs in the same process,
- Maintain conservation and determinism for all runs,
- Still pass all GF-01 tests from SPEC-002.

### 4.2 Dependencies

- SPEC-002 (GF-01 UMX implementation and tests),
- `TopologyProfile_v1.md`,
- `Profile_CMP0_v1.md`,
- `UMXTickLedger_v1.md`.

### 4.3 Issues / Work Items

#### Issue P2.1.1 — TopologyProfile Loader & Validator

**Goal:** Load arbitrary topologies from file and validate them against the contract.

**Tasks:**

- [ ] Implement a loader for `TopologyProfile_v1` (e.g. from JSON/YAML).
- [ ] Validate:
  - [ ] Node IDs are contiguous `[1..N]`.
  - [ ] Edge IDs are contiguous `[1..E]`.
  - [ ] `edges` sorted by `e_id`.
  - [ ] All edge endpoints `i`, `j` are in `[1..N]`.
  - [ ] All integer parameters (`k`, `cap`, `SC`, `c`) are valid integers.
- [ ] Provide at least:
  - [ ] A loader for the existing GF-01 profile (for regression),
  - [ ] One or more example profiles (line graph, ring graph, star).

**Acceptance Criteria:**

- [ ] Test verifies that valid profiles load and validate cleanly.
- [ ] Test verifies that invalid profiles are rejected with clear errors.

---

#### Issue P2.1.2 — UMXRunContext (Multi-Run Support)

**Goal:** Introduce a reusable context object to manage a UMX run.

**Tasks:**

- [ ] Define a `UMXRunContext` with:
  - `topo: TopologyProfile_v1`,
  - `profile: Profile_CMP0_v1`,
  - `state: int[N]` (current `u(t)`),
  - `tick: int` (current tick index),
  - any run metadata (`gid`, `run_id`).
- [ ] Implement methods:
  - [ ] `init_state(u0)` — set initial state.
  - [ ] `step()` — perform one CMP-0 tick, returning `UMXTickLedger_v1`.
  - [ ] `run_until(t_max)` — run multiple ticks, returning a sequence of ledgers.
- [ ] Ensure:
  - [ ] No global state; multiple contexts can run independently.
  - [ ] `step()` uses `TopologyProfile_v1` rather than GF-01 hard-coding.

**Acceptance Criteria:**

- [ ] GF-01 tests use `UMXRunContext` and still pass unchanged.
- [ ] New tests use `UMXRunContext` with other topologies and verify conservation + determinism.

---

#### Issue P2.1.3 — CMP-0 Generalised Tick Stepping

**Goal:** Ensure CMP-0 tick stepping is fully generalised across topologies.

**Tasks:**

- [ ] Refactor `UMX.step` logic (if needed) to use only:
  - `TopologyProfile_v1`,
  - `Profile_CMP0_v1`,
  - current `state`.
- [ ] Confirm:
  - [ ] Flux computation uses edge list from `topo.edges` in `e_id` order.
  - [ ] Conservation holds for all test graphs.
- [ ] Add tests for:
  - [ ] Line graph (e.g. 4 nodes in a chain),
  - [ ] Ring graph,
  - [ ] Star graph.

**Acceptance Criteria:**

- [ ] All new tests pass, plus all GF-01 tests.

---

#### Issue P2.1.4 — UMX Diagnostics & Invariants

**Goal:** Provide basic diagnostics for UMX runs.

**Tasks:**

- [ ] Implement optional checks or logging that can:
  - [ ] Verify conservation per tick,
  - [ ] Track min/max node values over time,
  - [ ] Detect any overflow or unexpected negative values (if disallowed).
- [ ] Tests:
  - [ ] Ensure diagnostics don’t change core behaviour (only logs/flags).

**Acceptance Criteria:**

- [ ] UMX can be run in “diagnostic mode” without affecting determinism.

---

## 5. EPIC P2.2 — Loom V1 (Time Axis & Replay)

### 5.1 Epic Goal

Upgrade Loom into a full time-axis service that:

- Tracks chain values and blocks for arbitrary runs,
- Supports configurable I-block spacing,
- Allows replay: reconstructing state at a desired tick.

### 5.2 Dependencies

- SPEC-002 Loom CMP-0 implementation,
- `LoomBlocks_v1.md`,
- `Profile_CMP0_v1.md`,
- UMXRunContext.

### 5.3 Issues / Work Items

#### Issue P2.2.1 — LoomRunContext

**Goal:** Create a run context for Loom similar to UMX.

**Tasks:**

- [ ] Define `LoomRunContext` with:
  - Reference to a `UMXRunContext` (or an abstract source of tick ledgers),
  - Current chain value `C_t`,
  - Configuration:
    - `W` (I-block spacing),
    - `s_t` rule,
    - sequence rule (`seq_t`).
  - Storage for:
    - List of `LoomPBlock_v1`,
    - List of `LoomIBlock_v1`.
- [ ] Implement:
  - [ ] `ingest_tick(ledger: UMXTickLedger_v1)` → `LoomPBlock_v1` (+ optional I-block).
  - [ ] `run_until(t_max)` to step UMX and Loom together (or ingest externally produced ledgers).

**Acceptance Criteria:**

- [ ] GF-01 Loom behaviour implemented through `LoomRunContext` still matches SPEC-002 tests.

---

#### Issue P2.2.2 — Configurable I-Block Spacing & s_t Rule

**Goal:** Support different checkpoint spacing and simple alternative `s_t` rules.

**Tasks:**

- [ ] Use `Profile_CMP0_v1.I_block_spacing_W` as default `W` for CMP-0,
- [ ] Allow override via run config (e.g. a smaller window for testing).
- [ ] Support:
  - [ ] Constant `s_t = 9` (GF-01),
  - [ ] At least one simple derived rule (e.g. sum of absolute fluxes modulo some small integer).
- [ ] Tests:
  - [ ] Confirm chain values match expectations for different `W` and `s_t` rules on small sample runs (non-GF-01).

**Acceptance Criteria:**

- [ ] Loom chain construction is robust to changes in `W` and `s_t` rule, and remains deterministic.

---

#### Issue P2.2.3 — Replay API

**Goal:** Implement APIs to reconstruct state at arbitrary ticks from P-blocks + I-blocks.

**Tasks:**

- [ ] Provide functions/methods, e.g.:
  - `get_chain_at(t) -> C_t`,
  - `get_pblock(t) -> LoomPBlock_v1`,
  - `get_iblock_for(t) -> LoomIBlock_v1`,
  - `replay_state_at(t)`:
    - Find nearest prior I-block,
    - Re-run UMX ticks from that checkpoint to t.
- [ ] Ensure:
  - [ ] Replay uses the same UMX logic and is deterministic.
- [ ] Tests:
  - [ ] For multiple topologies and initial states:
    - Direct run `state_t` matches `replay_state_at(t)` for a range of t.
  - [ ] For GF-01, replay produces exact `post_u` seen in SPEC-002.

**Acceptance Criteria:**

- [ ] Replay is correct and deterministic for all tested runs.

---

## 6. EPIC P2.3 — Press/APX V1 (Stream Registry & Basic Modes)

### 6.1 Epic Goal

Turn the minimal Press/APX implementation into a reusable V1 service that can:

- Track multiple named streams per window,
- Apply ID/R/GR schemes,
- Produce `APXManifest_v1` for arbitrary windows.

### 6.2 Dependencies

- SPEC-002 Press/APX implementation,
- `APXManifest_v1.md`,
- UMX and Loom contexts for stream inputs.

### 6.3 Issues / Work Items

#### Issue P2.3.1 — Stream Registry & Window Context

**Goal:** Introduce a registry and context for APX streams.

**Tasks:**

- [ ] Define a `PressWindowContext` that:
  - Is keyed by `(gid, window_id)`,
  - Holds multiple named streams (`S_post_u_deltas`, `S_fluxes`, etc.),
  - Buffers data per tick.
- [ ] Implement:
  - [ ] `register_stream(name, scheme_hint)` to declare streams and preferred schemes.
  - [ ] `append(name, value_or_tuple)` to add data for a given tick.
  - [ ] `close_window()` to compute `APXManifest_v1` and clear or roll buffers.

**Acceptance Criteria:**

- [ ] GF-01 windows can be expressed via `PressWindowContext` and still reproduce existing manifests.

---

#### Issue P2.3.2 — Implement ID, R, and Basic GR Schemes

**Goal:** Support three schemes at a basic level, with consistent MDL accounting.

**Tasks:**

- [ ] Implement scheme handlers:
  - ID: identity/raw encoding.
  - R: simple run-length / residue scheme as per current GF-01 usage.
  - GR: basic grouped R scheme (even if simple).
- [ ] Each scheme must:
  - [ ] Accept integer sequences,
  - [ ] Return encoded length contributions (`L_model`, `L_residual`, `L_total`),
  - [ ] Be deterministic.
- [ ] Integrate schemes with `PressWindowContext`:
  - [ ] On `close_window()`, apply scheme per stream based on `scheme_hint` or default profile.

**Acceptance Criteria:**

- [ ] Tests cover each scheme on simple sequences (constant, random-ish, sparse).
- [ ] GF-01 usage continues to work exactly as before.

---

#### Issue P2.3.3 — Generalised APXManifest_v1 Generation

**Goal:** Generalise APX manifest creation beyond GF-01.

**Tasks:**

- [ ] Ensure manifest includes:
  - Stream definitions,
  - Scheme choice per stream,
  - Length contributions,
  - `manifest_check` computed from all relevant fields.
- [ ] Add tests for:
  - [ ] Multi-stream windows (more than the original two),
  - [ ] Different scheme mixes (ID on one stream, R on another, etc.).

**Acceptance Criteria:**

- [ ] Manifests are deterministic and reproducible for all tested windows.

---

## 7. EPIC P2.4 — Gate/TBP V1 (Scenes & Layers)

### 7.1 Epic Goal

Move from a minimal GF-01 Gate stub to a Gate/TBP V1 that:

- Uses `SceneFrame_v1` as its core unit,
- Properly sets NAP layers and modes,
- Has a basic pattern for handling external inputs and outputs.

### 7.2 Dependencies

- SPEC-002 minimal Gate implementation,
- `SceneFrame_v1.md`,
- `NAPEnvelope_v1.md`,
- `TickLoop_v1.md`,
- Trinity Gate / TBP master spec.

### 7.3 Issues / Work Items

#### Issue P2.4.1 — SceneFrame_v1 as Primary Integration Object

**Goal:** Standardise on `SceneFrame_v1` as the per-tick integration bundle.

**Tasks:**

- [ ] Refactor tick loop so that:
  - UMX + Loom + Press outputs are collected into a `SceneFrame_v1` per tick.
- [ ] Ensure `SceneFrame_v1` includes:
  - Pre/post state,
  - `C_prev`, `C_t`,
  - Window ID & `manifest_check`,
  - References to underlying artefacts (ledger, P-block, manifest, envelope).
- [ ] Tests:
  - [ ] For GF-01 and at least one non-GF-01 scenario, scene frames are produced consistently.

**Acceptance Criteria:**

- [ ] Tick loop logic is framed around `SceneFrame_v1`, not ad hoc parameter passing.

---

#### Issue P2.4.2 — NAP Layers & Modes

**Goal:** Expand NAP layer usage beyond a single DATA mode.

**Tasks:**

- [ ] Define a minimal layer/mode scheme:
  - `layer`: INGRESS, DATA, CTRL, EGRESS.
  - `mode`: P (primary), S (secondary), etc. (initially keep it minimal).
- [ ] Adjust NAP generation so that:
  - GF-01 remains `layer = DATA`, `mode = P`.
  - Additional test scenarios can emit CTRL envelopes (e.g. “start run”, “end run”).
- [ ] Tests:
  - [ ] Verify correct layering in envelopes for designed scenarios.

**Acceptance Criteria:**

- [ ] NAP handling supports multiple layers/modes without breaking GF-01.

---

#### Issue P2.4.3 — PFNA Placeholder for External Inputs

**Goal:** Establish a deterministic placeholder for external inputs through Gate.

**Tasks:**

- [ ] Define a minimal mapping from “external integer sequences” to PFNA-like structures, even if:
  - They are synthetic or read from fixtures.
- [ ] Ensure that:
  - Any such inputs are passed through scene frames and can be referenced in NAP if needed.
- [ ] Tests:
  - [ ] A small scenario where external inputs influence UMX initial state or parameters.

**Acceptance Criteria:**

- [ ] There is a clear, deterministic path from “external data” → Gate → scene frame → UMX state.

---

## 8. EPIC P2.5 — U-ledger V1 (Universal Ledger Entry)

### 8.1 Epic Goal

Introduce a U-ledger that ties together:

- UMX ledgers,
- Loom blocks,
- APX manifests,
- NAP envelopes,
- Optional Codex state.

using `ULedgerEntry_v1` as the commit unit.

### 8.2 Dependencies

- SPEC-002 core loop,
- `ULedgerEntry_v1.md`,
- `NAPEnvelope_v1.md`,
- `APXManifest_v1.md`,
- Canonical JSON & hashing rules (from dev guide or new contract).

### 8.3 Issues / Work Items

#### Issue P2.5.1 — Canonical Serialisation & Hashing

**Goal:** Fix a canonical serialisation and hash algorithm for U-ledger use.

**Tasks:**

- [ ] Define canonical JSON rules (key order, whitespace, integer/string formats).
- [ ] Fix a hash algorithm (e.g. SHA-256).
- [ ] Implement utilities:
  - [ ] `hash_record(record) -> hash_string`.
- [ ] Tests:
  - [ ] Serialisation of the same record in different code paths yields identical bytes and hash.

**Acceptance Criteria:**

- [ ] Hashing is deterministic and documented.

---

#### Issue P2.5.2 — ULedgerEntry_v1 Construction

**Goal:** Implement construction of `ULedgerEntry_v1` per tick/window.

**Tasks:**

- [ ] For each tick:
  - [ ] Hash:
    - UMX ledger,
    - Loom P-block,
    - NAP envelope.
  - [ ] Look up:
    - `C_t`,
    - `manifest_check` for the window.
  - [ ] Build `ULedgerEntry_v1` with:
    - `gid`, `run_id`, `tick`, `window_id`,
    - `C_t`, `manifest_check`,
    - `nap_envelope_hash`, `umx_ledger_hash`, `loom_block_hash`,
    - `apx_manifest_hash` for the relevant window,
    - `prev_entry_hash`.
- [ ] Tests:
  - [ ] GF-01 run produces a stable U-ledger chain.
  - [ ] Re-running GF-01 yields identical entries.

**Acceptance Criteria:**

- [ ] U-ledger is stable and fully reproducible.

---

## 9. EPIC P2.6 — Codex V1 (Observer-Only)

### 9.1 Epic Goal

Wire Codex into the engine as an observer-only learner:

- Build motif definitions (`CodexLibraryEntry_v1`),
- Emit proposals (`CodexProposal_v1`),
- Do **not** modify engine structure yet.

### 9.2 Dependencies

- `CodexContracts_v1.md`,
- UMX, Loom, Press contexts (as data sources),
- Codex Eterna pillar master spec (for conceptual backing).

### 9.3 Issues / Work Items

#### Issue P2.6.1 — CodexContext & Data Ingest

**Goal:** Provide a context to ingest traces and produce Codex artefacts.

**Tasks:**

- [ ] Define `CodexContext` holding:
  - A library ID (`library_id`),
  - Collection of `CodexLibraryEntry_v1`,
  - Any runtime stats.
- [ ] Implement ingestion:
  - [ ] Accept sequences of:
    - UMX tick ledgers,
    - Loom P/I blocks,
    - APX manifests,
    - NAP envelopes (optional).
  - [ ] Maintain basic counts of patterns (e.g. repeated du/f_e patterns over edges).

**Acceptance Criteria:**

- [ ] CodexContext can consume GF-01 run data without error.

---

#### Issue P2.6.2 — Motif Identification (Simple Heuristics)

**Goal:** Implement a simple first pass at finding motifs.

**Tasks:**

- [ ] Define at least one motif type, e.g.:
  - `edge_flux_pattern_v1` (as sketched in `CodexContracts_v1.md`).
- [ ] Implement a heuristic that:
  - [ ] Scans sequences of flux patterns across ticks,
  - [ ] Identifies repeating patterns,
  - [ ] Constructs `CodexLibraryEntry_v1` entries with simple `mdl_stats` and `usage_stats`.
- [ ] Tests:
  - [ ] On GF-01 and one or two synthetic runs, Codex learns at least one motif in a deterministic way.

**Acceptance Criteria:**

- [ ] Library entries are stable and repeatable across runs.

---

#### Issue P2.6.3 — Proposal Emission (Observer-Only)

**Goal:** Emit `CodexProposal_v1` records for learned motifs, without applying them.

**Tasks:**

- [ ] For each motif meeting some threshold (e.g. use count), emit:
  - A `CodexProposal_v1` of type `PLACE` or `ADD`.
  - `status = "PENDING"` by default.
- [ ] Integrate with U-ledger:
  - [ ] Optionally hash and reference Codex library/proposal snapshots in `ULedgerEntry_v1`.
- [ ] Tests:
  - [ ] GF-01 run emits at least one proposal.
  - [ ] Re-running yields identical proposals.

**Acceptance Criteria:**

- [ ] Codex proposals are produced deterministically and do not affect core engine behaviour.

---

## 10. Out-of-Scope for SPEC-005

The following remain out of scope for Phase 2 and will be covered by later specs (e.g. SPEC-006, SPEC-007):

- Dynamic topology (SLP growth/prune) and Codex-driven structure changes,
- Full AEON/APXi grammar implementation in Press/APX,
- Rich PFNA and hardware-facing Gate/TBP integration,
- Complex governance policies and budgets,
- Multi-graph, multi-engine interoperation beyond simple parallel runs.

SPEC-005’s job is to move Aether from a **single exam fixture** to a **general V1 engine** for each pillar, while keeping all GF-01 guarantees intact.
