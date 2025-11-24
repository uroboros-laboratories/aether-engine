# SPEC-003 — Aether v1 Full Pillar Implementation Roadmap

## Status

- **Spec ID:** SPEC-003
- **Name:** Aether v1 Full Pillar Implementation
- **Version:** v1
- **Scope:** Gate/TBP, UMX, Loom, Press/APX, Codex, U-ledger
- **Assumes:** SPEC-002 (GF-01 CMP-0 Baseline Engine) is implemented and stable
- **Goal:** Reach a “v1 complete” implementation of all five pillars + ledger in code, consistent with the master pillar specs

---

## 1. Baseline Assumptions

Before this roadmap starts, the following are already true (from SPEC-002):

- GF-01 CMP-0 engine is implemented:
  - UMX CMP-0 engine produces correct `UMXTickLedger_v1` tick ledgers.
  - Loom CMP-0 produces correct chain and blocks.
  - Press/APX CMP-0 reproduces GF-01 manifests and `manifest_check`.
  - NAP produces correct `NAPEnvelope_v1` envelopes for GF-01.
  - Determinism + snapshot tests are in place.

- Contracts in `docs/contracts/` are the **source of truth** for data shapes:
  - `UMXTickLedger_v1`, `LoomBlocks_v1`, `APXManifest_v1`, `NAPEnvelope_v1`,
  - `TopologyProfile_v1`, `Profile_CMP0_v1`, `TickLoop_v1`, `SceneFrame_v1`,
  - `ULedgerEntry_v1`, `CodexContracts_v1`.

- Repo layout is roughly:
  - `src/core`, `src/gate`, `src/umx`, `src/loom`, `src/press`, `src/codex`, `src/uledger`,
  - `tests/gf01`, `tests/integration`.

---

## 2. Phase 2 — Pillar V1 Generalisation

### Overview

Phase 2 takes you from a **single toy graph & profile (GF-01 CMP-0)** to a **general, reusable v1** for each pillar, still within the constraints of the master specs but without all the fancy annexes.

This phase is where the engine becomes something you can actually *use*, not just a paper exam.

---

### EPIC P2.1 — UMX V1 (General Integer Engine)

**Goal**  
Generalise UMX from “hard-coded GF-01” to a reusable integer engine for arbitrary small to medium graphs under CMP-0.

**Key deltas vs SPEC-002**

- Arbitrary `TopologyProfile_v1` inputs (not just GF-01).
- Multiple runs/graphs in one process.
- Clean separation of config (profiles/topologies) and execution.

**Work items (high level)**

- [ ] Extend `TopologyProfile_v1` loading:
  - JSON/YAML loader for arbitrary topologies.
  - Validation of node/edge sets and parameters.

- [ ] Generalise `UMX.step` to:
  - Take any `TopologyProfile_v1` with CMP-0-compatible parameters.
  - Produce `UMXTickLedger_v1` for arbitrary N, E.

- [ ] Implement a `UMXRunContext` abstraction:
  - Holds `topo`, `profile`, current state, and tick counter.
  - Provides `step()` and `run_until(t_max)` APIs.

- [ ] New tests:
  - Small handcrafted graphs besides GF-01 (line, ring, star).
  - Conservation and determinism tests on those.

**Acceptance**

- UMX can run multiple graph configs under CMP-0 with:
  - Determinism,
  - Conservation,
  - Correct tick ledger structure.

---

### EPIC P2.2 — Loom V1 (Profiles, Replay, API)

**Goal**  
Turn Loom from a GF-01-specific chain into a proper time-axis service:

- Supports multiple runs,
- Supports replay queries,
- Supports varying I-block cadence.

**Work items**

- [ ] Generalise Loom to handle:
  - Any `UMXRunContext`,
  - Configurable `I_block_spacing_W`,
  - Configurable `s_t` rule (still restricted to integer, simple forms).

- [ ] Implement a `LoomRunContext`:
  - References a UMX run,
  - Maintains `C_t` sequence,
  - Stores `LoomPBlock_v1` and `LoomIBlock_v1` sequences.

- [ ] Implement replay API:
  - `get_chain_at(t) -> C_t`,
  - `get_state_at(t)` via I-block + re-run tick steps,
  - `get_window(t_start, t_end)` returning blocks.

- [ ] Tests:
  - Replay correctness on GF-01 and small extra graphs.
  - Deterministic reproduction of states via Loom replay, not just raw UMX re-run.

**Acceptance**

- Loom can reconstruct any state from checkpoints + P-blocks.
- Chain values are deterministic and consistent with `Profile_CMP0_v1`.

---

### EPIC P2.3 — Press/APX V1 (Stream Registry & Basic Modes)

**Goal**  
Generalise Press from “just enough to pass GF-01” to a **v1 APX service** that can:

- Handle multiple named streams per run/window,
- Choose between ID/R/GR schemes based on config,
- Produce consistent `APXManifest_v1` outputs.

**Work items**

- [ ] Implement a stream registry:
  - Register streams like `S_post_u_deltas`, `S_fluxes`, `S_s_t`, etc.
  - Allow different windows to compress different subsets.

- [ ] Implement ID, R, and basic GR modes:
  - Encode/decode frameworks for integer sequences.
  - MDL bit accounting for each scheme.

- [ ] Press context:
  - `PressWindowContext` keyed by `(gid, window_id)`,
  - Accepts appended data per stream each tick,
  - Produces `APXManifest_v1` at window close.

- [ ] Tests:
  - GF-01 regressions still pass,
  - Extra toy windows (short ranges) use the specified scheme and yield consistent `L_total` and `manifest_check`.

**Acceptance**

- Press can compress arbitrary integer sequences in a small set of streams,
- GF-01 manifests remain unchanged,
- Mode selection & bit accounting are deterministic and testable.

---

### EPIC P2.4 — Gate/TBP V1 (Basic I/O / Scene Frames)

**Goal**  
Upgrade Gate/TBP from a “GF-01 stub” to a minimal but real:

- Scene abstraction (`SceneFrame_v1`),
- Ingress/egress layers (INGRESS, DATA, CTRL),
- Basic PFNA placeholder where needed.

**Work items**

- [ ] Solidify `SceneFrame_v1` usage:
  - For each tick, capture engine state + chain + manifest + envelope references.

- [ ] Introduce simple ING/EG/CTRL layering:
  - `layer` field in NAP envelope reflects data type (INGRESS, EGRESS, CTRL, DATA).
  - For now, still mostly DATA + some CTRL (e.g. start/stop markers).

- [ ] Optional: PFNA placeholder:
  - Simple deterministic integer encodings for “external inputs” even if synthetic.

- [ ] Tests:
  - End-to-end tick loop still works when scene frames are the primary integration mechanism.
  - NAP envelopes match expectations for scenes that have basic ingress/egress annotations.

**Acceptance**

- Gate can support multiple scenario types beyond GF-01,
- NAP envelopes and scene frames remain deterministic and consistent.

---

### EPIC P2.5 — U-ledger V1 (ULedgerEntry_v1)

**Goal**  
Introduce a universal ledger commit record that stitches all pillars together per tick or window.

**Work items**

- [ ] Implement `ULedgerEntry_v1` type and canonical JSON.
- [ ] Choose and implement hash algorithm (e.g. SHA-256) and canonical serialisation.
- [ ] Implement a `ULedgerContext`:
  - For each tick, compute hashes of:
    - `UMXTickLedger_v1`,
    - `LoomPBlock_v1`,
    - `APXManifest_v1` for the window,
    - `NAPEnvelope_v1`.
  - Build `ULedgerEntry_v1` with:
    - `C_t`, `manifest_check`,
    - hash chain (`prev_entry_hash`).

- [ ] Tests:
  - GF-01 run yields a stable U-ledger chain.
  - Any change in pillar outputs breaks the hash chain (as expected).

**Acceptance**

- U-ledger provides a single, immutable record per tick/window,
- Re-running GF-01 yields identical U-ledger entries.

---

### EPIC P2.6 — Codex V1 (Observer-Only)

**Goal**  
Implement Codex as an **observer-only** component:

- Reads traces,
- Builds `CodexLibraryEntry_v1`,
- Emits `CodexProposal_v1` as logs only (no structural changes yet).

**Work items**

- [ ] Implement `CodexLibraryEntry_v1` and `CodexProposal_v1` data structures fully.
- [ ] Implement a `CodexContext` that:
  - Consumes sequences of UMX/Loom/APX artefacts.
  - Extracts simple motifs (e.g. repeated patterns in du/f_e or state).
  - Calculates simple MDL stats (even crude/heuristic to start).

- [ ] Emit library entries & proposals:
  - `status = "PENDING"` or `"REJECTED"` by default.
  - No direct side effects on UMX or profiles.

- [ ] Tests:
  - GF-01 run produces at least one stable `CodexLibraryEntry_v1` and some `CodexProposal_v1` records.
  - Re-running GF-01 yields identical Codex outputs.

**Acceptance**

- Codex is wired into the system as a read-only analysis layer,
- Library and proposal records are deterministic and correctly formed,
- No behaviour change in the core engine yet.

---

## 3. Phase 3 — Governance, Config, and Ops

Once all pillars have a V1 implementation, Phase 3 makes the system **operable and configurable**.

### EPIC P3.1 — Configuration & Profiles

**Goal**  
Allow the engine to be configured from files/CLI without code changes.

**Work items**

- [ ] Config loader for:
  - Topology profiles (`TopologyProfile_v1`),
  - Numeric profiles (`Profile_CMP0_v1` and future profiles),
  - Run definitions (which graph, how many ticks, window sizes).

- [ ] CLI commands:
  - `aether run <config>` — run a scenario.
  - `aether inspect <run-id>` — inspect stored artefacts.

**Acceptance**

- You can run non-GF-01 scenarios by editing config files, not code.

---

### EPIC P3.2 — Logging, Metrics, and Introspection

**Goal**  
Make it easy to see what’s happening in a run.

**Work items**

- [ ] Structured logs:
  - Per-tick summary (state ranges, chain, manifest_check).
- [ ] Basic metrics:
  - MDL stats per window,
  - NAP envelope counts per layer,
  - U-ledger chain stats (length, last hash).

**Acceptance**

- Operators can understand runs from logs + metrics without stepping into code.

---

### EPIC P3.3 — Developer Tooling & Regression Harness

**Goal**  
Ensure future changes don’t break GF-01 or other reference runs.

**Work items**

- [ ] Expand regression test suite:
  - Multiple fixture runs besides GF-01.
- [ ] Provide a “generate fixtures” tool:
  - Packs outputs for a run into a snapshot folder (JSON).

**Acceptance**

- CI can catch any behavioural change in core pillars quickly.

---

## 4. Phase 4 — Advanced Features & Spec Completeness

This phase is about aligning as closely as possible with the **full master pillar specs** and annexes.

### EPIC P4.1 — Advanced Press/APX (AEON/APXi, Placement MDL)

- Full AEON/APXi grammar support.
- Rich MDL placement spec across Press + UMX + Codex.
- Smarter encoding choices beyond fixed R/GR.

### EPIC P4.2 — Dynamic Topology & SLP in UMX

- Implement SLP growth/prune operations.
- Integrate Codex proposals into topology changes.
- Enforce conservation & MDL barriers during topology changes.

### EPIC P4.3 — Full Gate/TBP (PFNA, Quantum/Classic Bridge)

- PFNA generalised beyond toy encodings.
- TBP bridging for time-basis and external hardware/time sources.
- Scene-level multi-layer NAP streams.

### EPIC P4.4 — Codex Active Mode (Accepted Proposals)

- Let Codex proposals be submitted as NAP transactions.
- Implement governance logic to accept/reject proposals.
- Apply accepted proposals to UMX/Press/Loom configurations in a reversible way.

### EPIC P4.5 — Multi-Graph, Multi-Engine Scaling

- Support multiple UMX engines in a single run.
- Cross-graph interactions via Gate/TBP + U-ledger.

These epics will each need their own detailed specs, but SPEC-003 defines **where they sit in the overall journey**.

---

## 5. How to Use This Roadmap with GitHub

When you create the repo:

1. Add this file as:  
   `docs/specs/spec_003_Aether_v1_Full_Pillar_Roadmap.md`

2. Create GitHub Epics/Projects:
   - `Phase 2 — Pillar V1 Generalisation`
   - `Phase 3 — Governance & Ops`
   - `Phase 4 — Advanced Features & Spec Completeness`

3. For each EPIC above, spawn issues whose titles and checklists mirror the bullets here.

This keeps the repo implementation work tightly coupled to the master specs and the contracts we’ve already defined.
