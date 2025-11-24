# Aether Engine — Phase 3–5 Sprint Plan (SPEC-003/004/006/007)

This extends the previous sprint plans:

- **Phase 1** — SPEC-002: GF-01 CMP-0 baseline (paper parity).  
- **Phase 2** — SPEC-005: Pillar V1 generalisation (UMX/Loom/Press/Gate/U-ledger/Codex).  

Here we sketch sprints for:

- **Phase 3** — SPEC-003 & SPEC-004 (dynamic topology / SLP, richer AEON/APXi, runtime harness).  
- **Phase 4** — SPEC-006 (PFNA + hardware/data-plane integration).  
- **Phase 5** — SPEC-007 (governance, budgets, multi-run orchestration).  

This is deliberately high-level so we can refine against the actual SPEC-003/004/006/007
issue packs once the repo is live.

Assumption: Sprints 1–8 completed and the engine is stable as a general V1 system.

We continue sprint numbering from **Sprint 9**.

---

## Sprint 9 — Dynamic Topology Core (SLP Engine)

**Theme:** Give the engine a **living graph**: growth, prune, and simple rewiring
under well-defined rules.

**Phase:** 3 — SPEC-003

**Duration:** ~1–1.5 weeks.

### High-Level Goals

- Introduce a topology layer that can change over time (SLP = structure/locomotion pipeline).
- Keep changes explicit, logged, and reversible via the U-ledger.
- Make sure dynamic evolution is still deterministic under the same config + inputs.

### Suggested Breakdown

- [ ] SLP core contracts:
  - [ ] Implement types that represent **topology mutations**:
    - [ ] Add/remove node.
    - [ ] Add/remove edge.
    - [ ] Adjust edge parameters (k, cap, SC, c).
  - [ ] Define basic invariants (e.g. no orphaned edges, node ID continuity or mapping rules).
- [ ] SLP engine:
  - [ ] Maintain a versioned view of `TopologyProfile_v1` over time.
  - [ ] Apply batches of mutations at defined tick boundaries or windows.
  - [ ] Emit events/records that can be hashed into U-ledger entries.
- [ ] Integration with UMX / Loom:
  - [ ] On topology change, ensure:
    - [ ] UMX sees the updated topology from the next tick.
    - [ ] Loom includes structural info in blocks as required by specs.
- [ ] Determinism & rollback:
  - [ ] Given the same initial state + mutation sequence, runs must be reproducible.
  - [ ] Make it easy to re-run a segment of time with the same mutation set.

### Tests

- [ ] Toy scenarios:
  - [ ] Simple growth-only run (add edges/nodes, no removal).
  - [ ] Simple prune-only run (remove edges, shrink back).
- [ ] Determinism:
  - [ ] Same mutation log → same outputs, double-run checked.
- [ ] GF-01 compatibility:
  - [ ] Confirm that with “no mutations” configured, behaviour is identical to Phase 2 engine.

**Exit condition:** You can run a small scenario where the graph changes over time
and the engine remains deterministic and debuggable via SLP records.

---

## Sprint 10 — AEON/APXi & Structural Streams

**Theme:** Let Press/APX and Codex “see” **structure-level** change, not just
node/edge flux time-series.

**Phase:** 3 — SPEC-003 / SPEC-004

**Duration:** ~1–1.5 weeks.

### High-Level Goals

- Extend Press/APX to support **AEON/APXi-style streams** that encode structural events.
- Align SLP events with Press/APX manifests so chain/ledger capture structural history.

### Suggested Breakdown

- [ ] Structural streams:
  - [ ] Define one or more stream types for:
    - [ ] Node/edge creation and deletion.
    - [ ] Parameter tuning events (e.g. k/cap changes).
  - [ ] Register these as additional named streams in `PressWindowContext`.
- [ ] Basic AEON/APXi grammar:
  - [ ] Represent sequences of structural events in a more compact, grammar-like way.
  - [ ] Keep it simple (V1): a small codebook or token scheme is enough.
- [ ] Press/APX integration:
  - [ ] Ensure structural streams are included in window manifests.
  - [ ] Extend `manifest_check` input so it reflects structural and numeric content.
- [ ] Codex hooks:
  - [ ] Allow Codex to ingest structural streams for motif detection (e.g. recurring growth patterns).

### Tests

- [ ] Toy SLP + AEON/APXi scenario:
  - [ ] A short run where edges are added/removed with structural streams active.
  - [ ] Check manifest and U-ledger entries reflect those changes.
- [ ] Determinism:
  - [ ] Same structural event log → same structural streams and manifests.

**Exit condition:** Structural change is now a first-class part of the compression
and ledger story: you can point to “what the graph did” as well as “what the numbers did”.

---

## Sprint 11 — Runtime Harness & Scenario Layer

**Theme:** Build a **clean scenario API** so you can define and run experiments
without ad hoc wiring.

**Phase:** 3 — SPEC-004

**Duration:** ~1 week.

### High-Level Goals

- Introduce a runtime layer that understands:
  - A scenario config (topology + profile + inputs + SLP + Press config).
  - How to spin up UMX/Loom/Press/Gate/Codex/U-ledger contexts.
- Make it easy to express new experiments with config files instead of code edits.

### Suggested Breakdown

- [ ] Scenario contracts:
  - [ ] Define a scenario configuration structure that includes:
    - [ ] Topology and profile references.
    - [ ] Initial state / PFNA inputs (if relevant).
    - [ ] SLP script or mutation schedule.
    - [ ] Press/APX scheme hints and windowing.
    - [ ] Run duration and output options.
- [ ] Runtime harness:
  - [ ] Implement a “scenario runner” that:
    - [ ] Loads scenario config.
    - [ ] Constructs all necessary contexts (UMX, Loom, Press, Gate/NAP, Codex, U-ledger, SLP).
    - [ ] Iterates ticks/windows until completion.
  - [ ] Provide a single entrypoint like `run_scenario(config)`.
- [ ] Output packaging:
  - [ ] Bundle relevant artefacts per run (snapshots, manifests, ledger) in a consistent directory layout.

### Tests

- [ ] Re-express GF-01 as a scenario (no structural change, CMP-0 profile).
- [ ] A small dynamic-topology scenario via SLP.
- [ ] Confirm both can be run via the same harness API with deterministic outputs.

**Exit condition:** New experiments can be created by _writing scenario configs_;
no need to touch low-level wiring code to set up a new run.

---

## Sprint 12 — PFNA & Hardware / Data-Plane Integration

**Theme:** Connect the engine to **real or recorded external data** via PFNA-like
structures in a deterministic, replayable way.

**Phase:** 4 — SPEC-006

**Duration:** ~1–1.5 weeks.

### High-Level Goals

- Define PFNA-like contracts for external integer data streams.
- Implement adapters to bring external data into Gate → SceneFrame → UMX.
- Ensure runs are still fully replayable given recorded PFNA inputs.

### Suggested Breakdown

- [ ] PFNA contracts:
  - [ ] Encode external inputs as discrete, timestamped sequences with metadata.
  - [ ] Define channels (e.g. sensors, user actions) and mapping rules to engine parameters/state.
- [ ] Input adapters:
  - [ ] Implement deterministic adapters that map PFNA channels to:
    - [ ] Initial state on tick 0.
    - [ ] Per-tick perturbations (e.g. injection into certain nodes or edges).
- [ ] Integration with SceneFrame:
  - [ ] Ensure PFNA-derived data is visible in `SceneFrame_v1` for later analysis.
  - [ ] Optionally stream PFNA aggregates into Press/APX.
- [ ] Recording and replay:
  - [ ] Provide a way to record PFNA inputs for a run.
  - [ ] Ensure re-running with the same PFNA log reproduces the same behaviour.

### Tests

- [ ] Synthetic PFNA scenario:
  - [ ] A simple external signal (e.g. step function) that shapes the run.
  - [ ] Check replay correctness.
- [ ] Edge cases:
  - [ ] Missing / truncated PFNA streams produce clear, handled errors.

**Exit condition:** You can plug a deterministic external data feed into the engine,
record it, and replay runs exactly, with PFNA visible end-to-end.

---

## Sprint 13 — Governance, Budgets & Multi-Run Orchestration

**Theme:** Put a **governance shell** around the engine so multiple runs,
resources, and proposals can be managed coherently.

**Phase:** 5 — SPEC-007

**Duration:** ~1–1.5 weeks.

### High-Level Goals

- Introduce basic governance structures: budgets, run classes, prioritisation.
- Use U-ledger + Codex proposals as inputs to governance decisions (observer-only at first).
- Add orchestration over _batches_ of runs.

### Suggested Breakdown

- [ ] Governance contracts:
  - [ ] Represent budgets (compute/time/whatever unit you choose).
  - [ ] Represent runs as governance objects with status and class (e.g. test, baseline, experiment).
- [ ] Orchestrator:
  - [ ] Accepts a set of scenario configs.
  - [ ] Schedules them according to governance rules (e.g. budget, dependencies).
  - [ ] Registers results and snapshots in a high-level index.
- [ ] Codex & U-ledger integration:
  - [ ] Allow governance layer to read:
    - [ ] Ledger health (hash chain intact, snapshot deltas).
    - [ ] Codex proposals and motif summaries.
  - [ ] Still treat proposals as advisory, not auto-applied changes.
- [ ] Reporting:
  - [ ] Provide basic aggregated reports per “campaign” of runs (e.g. metrics, motif counts).

### Tests

- [ ] Tiny “campaign” with several small scenarios:
  - [ ] Check they run in order respecting simple governance constraints.
- [ ] Fault injection:
  - [ ] Simulate a bad scenario or mismatch and ensure governance reports/flags it via U-ledger signals.

**Exit condition:** You have a thin governance/orchestration layer that can run
and track multiple scenarios and surface Codex/U-ledger information without taking
over actual structural control yet.

---

## Sprint 14 — Polishing, Docs & Reference Scenarios

**Theme:** Stabilise, document, and demonstrate.

**Phase:** 5 — SPEC-007 (and general wrap-up)

**Duration:** ~1 week (or ongoing background).

### High-Level Goals

- Clean up docs & examples for all phases.
- Provide a small set of reference scenarios that exercise different capabilities.
- Make it easy for “future you” to spin this up after a break.

### Suggested Breakdown

- [ ] Documentation:
  - [ ] High-level “How the engine fits together” doc.
  - [ ] Updated READMEs in `docs/`, `src/`, `tests/`.
  - [ ] Link SPEC-000 index to actual code paths and modules.
- [ ] Reference scenarios:
  - [ ] A GF-01 regression scenario.
  - [ ] A dynamic-topology scenario (Phase 3 features).
  - [ ] A PFNA-driven scenario (Phase 4 features).
  - [ ] A small governance/orchestration campaign (Phase 5).
- [ ] Developer ergonomics:
  - [ ] One or two “quickstart” scripts/notebooks/configs to run a scenario and inspect outputs.

**Exit condition:** Someone with the docs + repo can pull, configure a run, and
get meaningful outputs without reading the entire codebase.

---

## Big Picture

With Sprints 1–14 laid out across Phases 1–5, you now have:

- A baseline → general engine → dynamic topology → PFNA → governance arc.
- A natural place to pause after any phase while still having a coherent, working system.
- Enough structure to create GitHub milestones, labels, Projects boards, and sprints
  without guessing later.

Once the repo is live, we can tighten this plan against the exact SPEC-003/004/006/007
issue packs and adjust sprint boundaries if you want finer granularity.
