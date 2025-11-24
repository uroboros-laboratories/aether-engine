# SPEC-006 — Phase 4 Issue Pack (Multi-Graph & SLP / Dynamic Topology V1)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 4 — SPEC-006 Multi-graph & SLP V1`

**Suggested labels:**

- `spec:SPEC-006`
- `phase:P4`
- `component:umx`
- `component:loom`
- `component:press`
- `component:gate`
- `component:nap`
- `component:codex`
- `component:slp`
- `component:u-ledger`
- `type:feature`
- `type:tests`
- `priority:medium`
- `priority:high`

You don’t have to use all labels on each issue; suggestions are given per-issue.

---

## Issue P4.6.1 — MultiGraphRunConfig & Topology Registry

**Title:**  
`[SPEC-006][P4] MultiGraphRunConfig & topology registry`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:umx`, `component:gate`, `component:slp`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Introduce a **multi-graph configuration and topology registry** so a single session can manage:

- Multiple graphs (each with its own topology/profile),
- Shared or distinct profiles (CMP-0 and beyond),
- Unique graph IDs (`gid`) and metadata.

This is the foundation for multi-graph runs and SLP (dynamic topology) in Phase 4.

## Spec References

- Universal Matrix pillar master spec
- Trinity Gate/TBP pillar spec (multi-graph sections)
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md` (and successors)
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` (UMXRunContext)
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`
- `docs/specs/spec_006_Phase_4_MultiGraph_SLP_Plan.md` (this spec, when added)

## Goals

- Allow Gate/TBP to define sessions involving one or more graphs.
- Provide a registry to manage topology/profile definitions keyed by `gid`.

## Tasks

- [ ] Extend or define `MultiGraphRunConfig_v1` including:
  - [ ] List of graph configs (each with `gid`, topology/profile refs, initial state source).
  - [ ] Optional inter-graph metadata (labels, grouping).
- [ ] Implement a topology registry:
  - [ ] Load one or more `TopologyProfile_v1` instances from config/fixtures.
  - [ ] Index by `gid` and version.
  - [ ] Validate uniqueness and consistency (no duplicated `gid` within a run).
- [ ] Integrate with Gate/TBP:
  - [ ] Gate creates one `UMXRunContext` per graph based on registry + config.
- [ ] Add tests:
  - [ ] Multi-graph config with 2–3 graphs loads successfully.
  - [ ] Invalid configs (duplicate `gid`, missing topology) fail with clear errors.

## Acceptance Criteria

- [ ] Multi-graph session config is defined and can be parsed/validated.
- [ ] Topology registry can supply per-graph topology/profile data deterministically.
```

---

## Issue P4.6.2 — MultiGraphRunContext (UMX & Loom Across Graphs)

**Title:**  
`[SPEC-006][P4] MultiGraphRunContext for UMX & Loom`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:umx`, `component:loom`, `component:gate`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Create a `MultiGraphRunContext` to orchestrate:
- Multiple `UMXRunContext` instances,
- Multiple `LoomRunContext` instances,
- Shared tick axis (session tick `t`) across graphs.

This enables multi-graph runs driven by a single Gate/TBP tick loop.

## Spec References

- UMX pillar master spec
- Loom pillar master spec
- `docs/contracts/UMXTickLedger_v1.md`
- `docs/contracts/LoomBlocks_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`

## Goals

- Step all graphs in lockstep per session tick (unless configured otherwise).
- Keep each graph’s state and chain values isolated but coordinated.

## Tasks

- [ ] Define `MultiGraphRunContext` holding:
  - [ ] Map `gid -> UMXRunContext`.
  - [ ] Map `gid -> LoomRunContext`.
  - [ ] Session-level tick counter.
  - [ ] Global config (e.g. list of active graphs, scheduling flags).
- [ ] Implement stepping API:
  - [ ] `step_all()` — advance all graphs one tick:
    - [ ] For each `gid`, call UMX `step()` then Loom ingest.
  - [ ] Optional: scheduling hooks for skipping certain graphs per tick if needed.
- [ ] Ensure integration with `SceneFrame_v1`:
  - [ ] Each tick and `gid` combination yields a scene frame keyed by `gid`.
- [ ] Add tests:
  - [ ] Multi-graph run with 2 simple graphs (line + ring) advances deterministically.
  - [ ] GF-01 alone can still be run via MultiGraphRunContext as a special case.

## Acceptance Criteria

- [ ] MultiGraphRunContext can coordinate multiple graphs’ UMX & Loom contexts under a shared tick axis.
- [ ] Tests confirm deterministic behaviour across multi-graph runs.
```

---

## Issue P4.6.3 — SLPEvent_v1 Contracts & Operation Types

**Title:**  
`[SPEC-006][P4] Define SLPEvent_v1 & topology operation types`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:slp`, `component:umx`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Define `SLPEvent_v1` and a minimal set of **topology operation types** for dynamic topology:

- Add/remove/adjust nodes,
- Add/remove/adjust edges,
- Graph-level ops (e.g. enable/disable a graph in a session).

These events will be applied between ticks to modify graph structure.

## Spec References

- Universal Matrix pillar master spec (SLP / dynamic topology sections)
- Trinity Gate/TBP pillar spec (graph lifecycle)
- `docs/contracts/SLPEvent_v1.md` (to be added)
- `docs/contracts/TopologyProfile_v1.md`

## Goals

- Provide a precise, serialisable representation of topology changes.
- Make SLP operations deterministic and replayable.

## Tasks

- [ ] Define `SLPEvent_v1` base fields:
  - [ ] `event_id`, `gid`, `tick_effective`, `op_type`, `payload`, etc.
- [ ] Define minimal operation types, e.g.:
  - [ ] `ADD_NODE`, `REMOVE_NODE`, `UPDATE_NODE`.
  - [ ] `ADD_EDGE`, `REMOVE_EDGE`, `UPDATE_EDGE`.
  - [ ] `GRAPH_ENABLE`, `GRAPH_DISABLE`.
- [ ] Define invariants:
  - [ ] No orphan edges, no duplicate node IDs, etc.
- [ ] Add tests:
  - [ ] Construct events of each type and serialise/deserialise.
  - [ ] Validate invariants at the event level.

## Acceptance Criteria

- [ ] SLPEvent_v1 is defined with a small but expressive operation set.
- [ ] Operation types cover basic dynamic topology needs for Phase 4.
```

---

## Issue P4.6.4 — Applying SLP Events to Topology (Between Ticks)

**Title:**  
`[SPEC-006][P4] Apply SLPEvent_v1 to live topology between ticks`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:slp`, `component:umx`, `component:loom`, `component:gate`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement logic to **apply SLPEvent_v1 operations** to live topologies safely and deterministically between ticks in a run.

## Spec References

- Universal Matrix pillar master spec (dynamic topology application rules)
- `docs/contracts/SLPEvent_v1.md`
- `docs/contracts/TopologyProfile_v1.md`
- `docs/specs/spec_006_Phase_4_MultiGraph_SLP_Plan.md`

## Goals

- Allow graph structure to change at well-defined tick boundaries.
- Preserve invariants and avoid mid-tick inconsistencies.

## Tasks

- [ ] Define when SLP events are applied:
  - [ ] e.g. between ticks `t` and `t+1` for each `gid`.
- [ ] Implement application logic:
  - [ ] Take `TopologyProfile_v1` and a list of SLP events for `gid`.
  - [ ] Apply operations in a deterministic order.
- [ ] On each event application:
  - [ ] Validate resulting topology (no orphan edges, etc.).
  - [ ] If invalid, fail with a clear error and/or mark run as aborted.
- [ ] Integration with MultiGraphRunContext:
  - [ ] Maintain per-graph SLP event queues keyed by tick.
  - [ ] On each tick boundary, apply relevant SLP events before the next `step_all()`.
- [ ] Add tests:
  - [ ] Simple scenarios of edge/node add/remove during a run.
  - [ ] Event ordering tests, including conflicting events.

## Acceptance Criteria

- [ ] SLP events can be applied deterministically between ticks.
- [ ] Topology remains valid after each batch of SLP events.
```

---

## Issue P4.6.5 — Loom, NAP & Press Integration with Multi-Graph & SLP

**Title:**  
`[SPEC-006][P4] Integrate Loom, NAP & Press with multi-graph & SLP`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:loom`, `component:nap`, `component:press`, `component:slp`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend Loom, NAP and Press so they remain consistent in the face of:

- Multi-graph runs,
- Dynamic topology changes via SLP.

## Spec References

- Loom pillar master spec
- Trinity Gate/TBP pillar spec
- Astral Press/APX pillar spec
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/SLPEvent_v1.md`

## Goals

- Ensure that chain values, blocks, NAP envelopes and manifests reflect the correct topology and graph context at each tick/window.

## Tasks

- [ ] Loom:
  - [ ] Ensure I-block snapshots include topology at blocks that cross SLP boundaries.
  - [ ] Include `gid` and any dynamic topology metadata in blocks where appropriate.
- [ ] NAP:
  - [ ] Include `gid` in envelopes for multi-graph runs.
  - [ ] Optionally include SLP-related metadata (e.g. SLP event IDs) in CTRL envelopes.
- [ ] Press:
  - [ ] Ensure streams are tagged by `gid` and respect topology changes (e.g. new edges impact flux streams).
- [ ] Add tests:
  - [ ] Scenario: graph where a new edge is added mid-run; verify Loom snapshots, NAP envelopes and Press outputs remain consistent.
  - [ ] Multi-graph scenario where only one graph receives SLP events.

## Acceptance Criteria

- [ ] Loom, NAP and Press correctly reflect graph identity and topology changes.
- [ ] No ambiguity about which graph or topology version an artefact belongs to.
```

---

## Issue P4.6.6 — Codex Motifs for SLP & Multi-Graph Structures (Observer-Only)

**Title:**  
`[SPEC-006][P4] Codex motifs for SLP & multi-graph structures (observer-only)`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:codex`, `component:slp`, `component:umx`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend Codex ingest and motifs to cover:

- SLP events,
- Multi-graph structural patterns,

while remaining strictly observer-only (no actioning yet).

## Spec References

- Codex Eterna master spec
- `docs/contracts/CodexContracts_v1.md`
- `docs/contracts/SLPEvent_v1.md`
- `docs/contracts/TopologyProfile_v1.md`

## Goals

- Allow Codex to learn motifs from structural evolution and multi-graph patterns.
- Keep Codex read-only in Phase 4.

## Tasks

- [ ] Extend Codex ingest to accept:
  - [ ] SLPEvent_v1 sequences per `gid`.
  - [ ] Topology snapshots (from Loom I-blocks or direct dumps).
- [ ] Define at least one SLP/multi-graph motif type (e.g. repeated growth pattern, common structural subgraph).
- [ ] Implement motif extraction:
  - [ ] Find repeated SLP event sequences or structural configurations.
  - [ ] Produce `CodexLibraryEntry_v1` with MDL/usage stats.
- [ ] Add tests:
  - [ ] Multi-graph scenario with repeated SLP patterns yields deterministic motifs.
  - [ ] Re-running scenario yields identical Codex entries.

## Acceptance Criteria

- [ ] Codex can learn motifs involving dynamic topology and multi-graph structure.
- [ ] Codex outputs are stable and do not influence engine behaviour in Phase 4.
```

---

## Issue P4.6.7 — U-ledger Integration for SLP & Multi-Graph + Demo Snapshot

**Title:**  
`[SPEC-006][P4] U-ledger integration for SLP & multi-graph + demo snapshot`

**Labels:**  
`spec:SPEC-006`, `phase:P4`, `component:u-ledger`, `component:slp`, `component:umx`, `component:loom`, `component:press`, `component:nap`, `component:codex`, `type:tests`, `type:feature`, `priority:high`

```markdown
## Summary

Extend U-ledger so that:

- Multi-graph runs and SLP events are fully represented,
- A canonical multi-graph + SLP demo scenario is snapshotted for regression.

## Spec References

- U-ledger subsystem coverage matrix
- `docs/contracts/ULedgerEntry_v1.md`
- `docs/contracts/SLPEvent_v1.md`
- All core pillar contracts (UMX, Loom, Press, NAP, Codex)

## Goals

- Make the ledger the complete, replayable history for multi-graph + SLP scenarios.
- Provide at least one stable scenario as a reference snapshot.

## Tasks

- [ ] Extend ULedgerEntry_v1 to include:
  - [ ] `gid` / graph identifiers where not already present.
  - [ ] Optional references/hashes to SLP events applied at or before a tick.
- [ ] Design a multi-graph + SLP demo scenario:
  - [ ] Two or more graphs with simple dynamics.
  - [ ] A small set of SLP events (e.g. adding/removing edges) during the run.
- [ ] Implement test harness:
  - [ ] Run scenario and collect U-ledger chain + pillar outputs.
  - [ ] Persist canonical JSON snapshot under `tests/fixtures/snapshots/multigraph_slp_demo/`.
- [ ] Add regression tests:
  - [ ] New runs must match the ledger snapshot (and any associated snapshots).
- [ ] Verify replay:
  - [ ] From snapshot, replay topology + state using pillar replay APIs and check consistency.

## Acceptance Criteria

- [ ] Multi-graph + SLP demo scenario is documented and deterministic.
- [ ] U-ledger entries form a coherent chain including SLP and multi-graph context.
- [ ] Snapshot-based tests catch behavioural drift in Phase 4 features.
```

---

## Notes

- SPEC-006 builds directly on:
  - SPEC-002 (baseline deterministic engine),
  - SPEC-005 (Pillar V1 generalisation),
  - SPEC-003 (Gate/PFNA IO),
  - SPEC-004 (AEON/APXi),
  - plus the U-ledger subsystem coverage.
- Phase 4 is still **observer-only** for Codex and governance: SLP and multi-graph patterns are learned and recorded, not acted upon yet. Engine-structural decisions remain manual or config-driven until SPEC-007 (Phase 5).
