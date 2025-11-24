# Aether Engine — Phase 2 Sprint Plan (SPEC-005)

This is a sprint plan for **Phase 2 / SPEC-005 — Pillar V1 Generalisation**.

Scope: take the **GF-01 CMP-0 baseline engine** from Phase 1 and generalise it into
a reusable V1 engine:

- UMX V1 (multi-topology, multi-run),
- Loom V1 (time axis + replay),
- Press/APX V1 (streams + schemes),
- Gate/TBP V1 (SceneFrame-centric, layered NAP),
- U-ledger V1,
- Codex V1 (observer-only).

You can use this plan **before** the repo exists; once the repo is live, drop this
file into `docs/specs/` and wire sprints to a GitHub Project and SPEC-005 issues.

Phase 1 sprints ended at **Sprint 3**, so we continue numbering from Sprint 4.

---

## Sprint 4 — UMX V1 (Multi-Topology, Multi-Run)

**Theme:** Turn the GF-01-only UMX into a **general integer engine**.

**Duration:** ~1–1.5 weeks.

### SPEC-005 Issues in scope

- P2.1.1 — TopologyProfile loader & validator  
- P2.1.2 — UMXRunContext for multi-run UMX V1 engine  
- P2.1.3 — Generalise CMP-0 UMX tick stepping across topologies  
- P2.1.4 — UMX diagnostics & invariant checks (can slip to Sprint 5 if needed)

### Goals

- Load validated `TopologyProfile_v1` instances from config/fixtures.
- Run multiple UMX runs in one process via `UMXRunContext`.
- Confirm CMP-0 stepping is fully general and deterministic across several graphs.
- Add an optional diagnostics mode for safety checks.

### Suggested Breakdown

- [ ] Loader + validator:
  - [ ] Implement config-based loader for `TopologyProfile_v1` (JSON/YAML/…).
  - [ ] Enforce invariants:
    - [ ] Node IDs contiguous in `[1..N]`.
    - [ ] Edge IDs contiguous in `[1..E]`, sorted.
    - [ ] Edge endpoints within `[1..N]`.
    - [ ] All integer parameters valid (no floats).
- [ ] Example topologies:
  - [ ] Lift GF-01 into a loader fixture (for regression).
  - [ ] Add at least one **line** graph profile.
  - [ ] Add at least one **ring** or **star** profile.
- [ ] `UMXRunContext` implementation:
  - [ ] Holds `topo`, `profile`, `state`, `tick`, metadata.
  - [ ] `init_state(u0)` initialises `u(t)`.
  - [ ] `step()` runs a single CMP-0 tick and returns `UMXTickLedger_v1`.
  - [ ] `run_until(t_max)` runs multiple ticks, returning ledgers.
  - [ ] No global mutable state; multiple contexts can coexist.
- [ ] Generalised stepping:
  - [ ] Ensure `UMX.step` logic uses only `TopologyProfile_v1` + `Profile_CMP0_v1`.
  - [ ] No GF-01-specific branching or counts.
- [ ] Diagnostics (optional within this sprint):
  - [ ] Flag/option to enable extra checks:
    - [ ] Conservation per tick (`sum_pre_u == sum_post_u`).
    - [ ] Min/max node values tracking.
    - [ ] Optional warnings on negatives/overflow (if applicable).
  - [ ] Ensure diagnostics do not change the core outputs.

### Tests

- [ ] GF-01: refactor UMX tests to use `UMXRunContext`; all existing SPEC-002 tests still pass.
- [ ] Line, ring, star graphs:
  - [ ] Determinism: double-run checks on each topology.
  - [ ] Conservation: sums invariant across ticks.

**Exit condition:** UMX is a reusable V1 engine: you can spin up multiple runs, load
any valid topology profile, and get deterministic CMP-0 evolution with optional diagnostics.

---

## Sprint 5 — Loom V1 (Contexts, Config, Replay)

**Theme:** Generalise the **time axis** to work with any UMX run and add replay.

**Duration:** ~1 week.

### SPEC-005 Issues in scope

- P2.2.1 — LoomRunContext for time axis & blocks  
- P2.2.2 — Configurable Loom I-block spacing & s_t rule  
- P2.2.3 — Loom replay API (get_chain_at, replay_state_at)

### Goals

- Encapsulate Loom behaviour in `LoomRunContext`.
- Make I-block spacing and `s_t` rule configurable.
- Provide replay APIs for chain and state reconstruction at arbitrary ticks.

### Suggested Breakdown

- [ ] `LoomRunContext`:
  - [ ] Holds:
    - [ ] Reference to `UMXRunContext` (or generic tick-ledger source).
    - [ ] Current `C_t`.
    - [ ] Config: `W`, `s_t` rule, `seq_t` rule.
    - [ ] Collections of P-blocks and I-blocks.
  - [ ] Methods:
    - [ ] `ingest_tick(ledger)` → `LoomPBlock_v1` (+ optional `LoomIBlock_v1`).
    - [ ] `run_until(t_max)` to drive UMX + Loom together (or replay from stored ledgers).
- [ ] Configurable behaviour:
  - [ ] Use profile default (`W = 8`, `s_t = 9` for CMP-0/GF-01).
  - [ ] Allow run-time overrides of `W` for testing (e.g. `W = 4`).
  - [ ] Implement at least one derived `s_t` rule (e.g. from flux magnitudes).
- [ ] Replay API:
  - [ ] `get_chain_at(t) -> C_t`.
  - [ ] `get_pblock(t) -> LoomPBlock_v1`.
  - [ ] `get_iblock_for(t) -> LoomIBlock_v1` (nearest checkpoint).
  - [ ] `replay_state_at(t)`:
    - [ ] Find nearest I-block checkpoint.
    - [ ] Re-run UMX ticks from checkpoint to `t`, using original inputs.

### Tests

- [ ] GF-01:
  - [ ] `LoomRunContext` reproduces `C_1..C_8` and I-block at `t=8` exactly.
  - [ ] `replay_state_at(t)` equals original `post_u` for `t=1..8`.
- [ ] Non-GF-01 scenario:
  - [ ] Use a line/ring graph for a short run.
  - [ ] Confirm replayed states match direct run states exactly.

**Exit condition:** Loom is a V1 time-axis service: it can sit on top of any UMX run,
parameterised by profile/config, and reconstruct past states reliably.

---

## Sprint 6 — Press/APX V1 (Stream Registry & Schemes)

**Theme:** Generalise **Press/APX** from “two hard-coded GF-01 streams” to a
proper stream registry with multiple schemes.

**Duration:** ~1–1.5 weeks.

### SPEC-005 Issues in scope

- P2.3.1 — PressWindowContext & stream registry  
- P2.3.2 — Implement ID, R, and basic GR schemes in Press/APX  
- P2.3.3 — Generalised APXManifest_v1 generation

### Goals

- Create `PressWindowContext` for multiple named streams per window.
- Support three schemes: ID, R, GR (basic).
- Generalise APX manifests to arbitrary stream sets and mixed schemes.

### Suggested Breakdown

- [ ] `PressWindowContext`:
  - [ ] Keyed by `(gid, window_id)`.
  - [ ] Holds multiple named streams.
  - [ ] API:
    - [ ] `register_stream(name, scheme_hint)`.
    - [ ] `append(name, value_or_tuple)` per tick.
    - [ ] `close_window()` → `APXManifest_v1` (+ internal cleanup/rollover).
- [ ] Scheme implementations:
  - [ ] ID scheme: identity/raw encoding + MDL accounting.
  - [ ] R scheme: as per GF-01, formalised as a scheme handler.
  - [ ] Basic GR scheme: grouped R (simple implementation is fine at V1).
  - [ ] Each scheme returns `L_model`, `L_residual`, `L_total` deterministically.
- [ ] Manifest generation:
  - [ ] Streams section: name, scheme, lengths.
  - [ ] Per-stream MDL stats.
  - [ ] `manifest_check` computed from manifest contents (as per contract).
- [ ] GF-01 lift:
  - [ ] Express the GF-01 windows (1–8 and 1–2) through `PressWindowContext`
        using the R scheme on the same logical streams.
  - [ ] Ensure all previous GF-01 APX numbers remain unchanged.

### Tests

- [ ] Unit tests for ID, R, GR schemes on simple synthetic sequences:
  - [ ] Constant, alternating, sparse, etc.
- [ ] Multi-stream windows:
  - [ ] Mixed schemes (e.g. ID on one stream, R on another, GR on a third).
  - [ ] Deterministic manifests + `manifest_check`.
- [ ] GF-01 regressions:
  - [ ] `L_total` per stream and `manifest_check` for windows 1–8 and 1–2
        match SPEC-002 values exactly.

**Exit condition:** Press/APX is a general V1 subsystem: given arbitrary named
streams and scheme hints, it can produce deterministic manifests, with GF-01 still
acting as the regression gold standard.

---

## Sprint 7 — Gate/TBP V1 (SceneFrames, NAP Layers, PFNA Stub)

**Theme:** Clean, general **integration surface** around `SceneFrame_v1`
and a richer NAP layer/mode model, with PFNA stubbed in for deterministic inputs.

**Duration:** ~1–1.5 weeks.

### SPEC-005 Issues in scope

- P2.4.1 — SceneFrame_v1 as primary integration object  
- P2.4.2 — NAP layers & modes (beyond DATA/P)  
- P2.4.3 — PFNA placeholder for deterministic external inputs

### Goals

- Make `SceneFrame_v1` the canonical per-tick integration bundle.
- Support NAP layers (INGRESS/DATA/CTRL/EGRESS) and multiple modes (P + at least one more).
- Introduce a PFNA-style placeholder path for external integer inputs.

### Suggested Breakdown

- [ ] SceneFrame-centric tick loop:
  - [ ] Refactor existing tick loop (from Phase 1) so each tick builds a `SceneFrame_v1`:
    - [ ] UMX fields: `pre_u`, `post_u`, node IDs, etc.
    - [ ] Loom fields: `C_prev`, `C_t`, block references.
    - [ ] Press/APX: window IDs, manifest IDs/checks.
    - [ ] Metadata: `gid`, `run_id`, `tick`, `nid`.
  - [ ] NAP envelope creation becomes a simple transformation of `SceneFrame_v1`.
- [ ] NAP layers & modes:
  - [ ] Define an enum/constant set for layers: INGRESS, DATA, CTRL, EGRESS.
  - [ ] Define at least one extra mode beyond P (e.g. `M` for metadata/control).
  - [ ] Keep GF-01 as `layer = DATA`, `mode = P`.
  - [ ] Add a toy scenario using CTRL envelopes (e.g. run start/end messages).
- [ ] PFNA placeholder:
  - [ ] Minimal schema for PFNA-like external input bundles (integer sequences + metadata).
  - [ ] Gate logic that can ingest PFNA placeholders and:
    - [ ] Set initial UMX state, or
    - [ ] Adjust parameters, as configured.
  - [ ] Keep behaviour deterministic (no hidden randomness).

### Tests

- [ ] GF-01:
  - [ ] Scene frames produce the same NAP envelopes as before.
  - [ ] Layer/mode for GF-01 remains DATA/P.
- [ ] NAP layering scenario:
  - [ ] A short run where CTRL envelopes appear at start/end.
  - [ ] Correct layer/mode classification.
- [ ] PFNA scenario:
  - [ ] Small example where an external integer sequence (via PFNA placeholder)
        alters the initial state or parameters in a deterministic way.

**Exit condition:** Gate/TBP V1 defines a clean, reusable scene-centric API with
NAP layers/modes and an initial PFNA path, without breaking GF-01 behaviour.

---

## Sprint 8 — U-ledger V1 & Codex V1 (Observer-Only)

**Theme:** Add **traceability** (U-ledger) and **learning** (Codex) on top of
the now-general engine, staying strictly observer-only for Codex.

**Duration:** ~1–1.5 weeks.

### SPEC-005 Issues in scope

- P2.5.1 — Canonical serialisation & hashing for U-ledger  
- P2.5.2 — Construct ULedgerEntry_v1 per tick/window  
- P2.6.1 — CodexContext & data ingest (observer mode)  
- P2.6.2 — Codex motif identification (simple heuristics)  
- P2.6.3 — Codex proposal emission (observer-only)

### Goals

- Define stable, canonical serialisation + hashing for all core records.
- Build a per-tick (or per-window) U-ledger chain that ties pillars together.
- Ingest runs into Codex, learn simple motifs, and emit proposals without affecting behaviour.

### Suggested Breakdown

- [ ] Canonical serialisation & hashing:
  - [ ] Decide JSON canon rules (key order, whitespace, number formatting).
  - [ ] Implement utilities to serialise:
    - [ ] `UMXTickLedger_v1`
    - [ ] `LoomPBlock_v1`, `LoomIBlock_v1`
    - [ ] `APXManifest_v1`
    - [ ] `NAPEnvelope_v1`
    - [ ] `SceneFrame_v1`
  - [ ] Choose hash (e.g. SHA-256) and implement `hash_record(record)`.
- [ ] `ULedgerEntry_v1` construction:
  - [ ] For each tick/window:
    - [ ] Hash pillar artefacts.
    - [ ] Include `C_t`, `manifest_check`, tick/window IDs.
    - [ ] Chain via `prev_entry_hash`.
  - [ ] Store entries per run in a U-ledger log.
- [ ] CodexContext:
  - [ ] Holds Codex library entries + metadata.
  - [ ] Ingest pipeline from:
    - [ ] UMX ledgers,
    - [ ] Loom blocks,
    - [ ] APX manifests,
    - [ ] (Optional) NAP envelopes / SceneFrames.
- [ ] Motif identification (simple):
  - [ ] Implement at least one motif type (e.g. `edge_flux_pattern_v1`).
  - [ ] Scan for repeated patterns in flux or state sequences.
  - [ ] Emit `CodexLibraryEntry_v1` with basic MDL + usage stats.
- [ ] Proposal emission (observer-only):
  - [ ] For motifs meeting thresholds, emit `CodexProposal_v1` records.
  - [ ] Mark proposals as PENDING/REJECTED by default (no application).
  - [ ] Optionally tie proposals/library snapshots into U-ledger entries by hash.

### Tests

- [ ] U-ledger:
  - [ ] GF-01 run produces a stable hash chain.
  - [ ] Re-running GF-01 yields identical ledger entries.
  - [ ] Any intentional change to pillar outputs changes the hash chain as expected.
- [ ] Codex:
  - [ ] GF-01 + at least one non-GF-01 scenario ingest without errors.
  - [ ] Stable motifs learned across repeats of the same run.
  - [ ] Proposals generated deterministically from motifs.
  - [ ] No change to engine behaviour when Codex is active.

**Exit condition:**

- U-ledger V1 exists as a cross-pillar hash chain for runs.
- Codex V1 can ingest data, learn simple motifs, and produce proposals,
  all without changing how the engine itself behaves.

---

## After Phase 2

With Phase 2 sprints complete, you’ll have:

- A **general engine** that can run multiple topologies and scenarios.
- A clean time axis with replay, configurable chaining, and snapshots.
- A generalised Press/APX with multiple schemes and arbitrary streams.
- A structured Gate/TBP + NAP layer/mode model.
- A U-ledger for traceability and a Codex observer that can start learning structure.

From here, Phase 3+ (SPEC-003/004/006/007) can focus on:
- SLP growth/prune,
- richer AEON/APXi grammars,
- governance and budgets,
- more advanced Codex-guided structural changes.

This plan is intentionally high-level so we can adjust sprint durations and issue
groupings based on your actual coding time once the repo is live.
