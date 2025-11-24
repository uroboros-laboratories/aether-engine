# SPEC-004 — Phase 3 Issue Pack (Press AEON/APXi Views & Descriptors)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 3 — SPEC-004 Press AEON/APXi`

**Suggested labels:**

- `spec:SPEC-004`
- `phase:P3`
- `component:press`
- `component:aeon`
- `component:apxi`
- `component:loom`
- `component:codex`
- `type:feature`
- `type:tests`
- `priority:medium`
- `priority:high`

You don’t have to use all labels on each issue; suggestions are given per-issue.

---

## Issue P4.1 — AEON Window Grammar Contracts

**Title:**  
`[SPEC-004][P3] Define AEON window grammar contracts`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:aeon`, `component:press`, `type:feature`, `priority:high`

```markdown
## Summary

Define the **AEON window grammar** contracts that describe how windows are organised over time:

- Base windows (tick ranges),
- Aggregated/derived windows,
- Hierarchical relationships between windows.

These contracts are the backbone for all AEON/APXi features.

## Spec References

- Astral Press / AEON master spec (AEON grammar sections)
- `docs/contracts/AEONWindowGrammar_v1.md` (to be added)
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/LoomBlocks_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`

## Goals

- Provide a clear, versioned contract for AEON windows.
- Make AEON windows compatible with existing Press windows and Loom tick axis.

## Tasks

- [ ] Define `AEONWindowDef_v1` type:
  - [ ] Base window definition (tick_start, tick_end).
  - [ ] Optional labels/tags.
- [ ] Define higher-level AEON grammar types:
  - [ ] Aggregated windows (compositions of base windows).
  - [ ] Hierarchical relations (parent/child, siblings).
- [ ] Ensure AEON windows can be linked to:
  - [ ] Loom chain/ticks.
  - [ ] Press windows / manifests.
- [ ] Add unit tests:
  - [ ] Construct simple AEON hierarchies and validate structure.
  - [ ] Round-trip serialisation tests (JSON or chosen format).

## Acceptance Criteria

- [ ] `AEONWindowGrammar_v1` contracts are defined and test-covered.
- [ ] AEON window definitions can represent at least:
  - [ ] GF-01-style fixed windows.
  - [ ] A simple hierarchical example (e.g. daily + weekly windows) for demos.
```

---

## Issue P4.2 — AEON Window Registry & Query API

**Title:**  
`[SPEC-004][P3] Implement AEON window registry & query API`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:aeon`, `component:press`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement an **AEON window registry** and a query API to:

- Register windows (base + derived),
- Look up windows by tick, id, or relationship,
- Provide AEON views over Press/APX data.

## Spec References

- Astral Press / AEON master spec
- `docs/contracts/AEONWindowGrammar_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/LoomBlocks_v1.md`

## Goals

- Make AEON windows addressable and queryable.
- Provide the foundation for AEON-based views and APXi descriptors.

## Tasks

- [ ] Implement `AEONWindowRegistry`:
  - [ ] Register base and derived windows.
  - [ ] Ensure IDs are unique and stable.
- [ ] Implement query functions:
  - [ ] `get_window(window_id)`.
  - [ ] `windows_covering_tick(t)`.
  - [ ] `children_of(window_id)`, `parent_of(window_id)`.
- [ ] Integrate with Loom and Press:
  - [ ] Map existing Press windows to AEON windows.
  - [ ] Store references from AEON windows to manifests (where applicable).
- [ ] Add tests:
  - [ ] Simple AEON hierarchies: lookups by tick and relationships.
  - [ ] GF-01-style windows represented in AEON registry.

## Acceptance Criteria

- [ ] AEON windows can be registered and queried deterministically.
- [ ] Press windows from earlier phases can be exposed via AEON window registry without behaviour changes.
```

---

## Issue P4.3 — APXiDescriptor_v1 Contracts & Primitive Types

**Title:**  
`[SPEC-004][P3] Define APXiDescriptor_v1 and primitive descriptor types`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:apxi`, `component:press`, `type:feature`, `priority:high`

```markdown
## Summary

Define `APXiDescriptor_v1` and a small set of **primitive descriptor types** to describe integer sequences over AEON windows:

- Constant segments,
- Repeats,
- Simple patterns/trends (V0).

These descriptors will be used by APXi for structured explanations and by Codex for motifs.

## Spec References

- Astral Press / APXi master spec (descriptor language section)
- `docs/contracts/APXiDescriptor_v1.md` (to be added)
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/AEONWindowGrammar_v1.md`

## Goals

- Provide a minimal but expressive descriptor contract for APXi V0.
- Ensure descriptors are composable and serialisable.

## Tasks

- [ ] Define `APXiDescriptor_v1` base type:
  - [ ] Fields: `id`, `type`, `window_id`, `params`, etc.
- [ ] Define primitive descriptor types:
  - [ ] `CONST_SEGMENT` (constant value over window or sub-window).
  - [ ] `RUN_SEGMENT` (repeat pattern / runs).
  - [ ] `LINEAR_TREND` (simple trend: slope + intercept).
- [ ] Define how descriptors refer to streams:
  - [ ] Stream IDs / names from Press manifests.
- [ ] Add tests:
  - [ ] Construct each primitive descriptor and serialise/deserialise.
  - [ ] Validate that they can be associated to AEON windows and streams.

## Acceptance Criteria

- [ ] APXi descriptor contracts exist and are stable.
- [ ] Primitive descriptors cover simple patterns and can be extended later.
```

---

## Issue P4.4 — APXi MDL Accounting & Residual Handling

**Title:**  
`[SPEC-004][P3] Implement APXi MDL accounting & residual handling`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:apxi`, `component:press`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Implement MDL accounting for APXi descriptors and their residuals:

- Description cost of descriptors,
- Cost of residual errors,
- Total cost comparable to existing ID/R/GR schemes.

## Spec References

- Astral Press / APXi master spec (MDL rules)
- `docs/contracts/APXiDescriptor_v1.md`
- `docs/contracts/APXManifest_v1.md`

## Goals

- Make APXi costs fully integer-only and deterministic.
- Allow apples-to-apples comparison of APXi vs ID/R/GR for a given stream/window.

## Tasks

- [ ] Implement MDL cost functions for each primitive descriptor type.
- [ ] Implement residual computation:
  - [ ] Apply descriptor to original sequence.
  - [ ] Compute residual sequence.
  - [ ] Compute cost of residual (e.g. via ID or R scheme).
- [ ] Integrate with Press/APX:
  - [ ] Allow APXi to produce `L_model`, `L_residual`, `L_total` for a stream/window.
- [ ] Add tests:
  - [ ] Simple synthetic sequences where APXi improvement is obvious.
  - [ ] Compare APXi vs ID/R/GR to ensure MDL arithmetic is consistent.
  - [ ] Determinism tests: same inputs/config → same APXi costs.

## Acceptance Criteria

- [ ] APXi MDL metrics are integer-only and reproducible.
- [ ] APXi outputs can be compared against existing schemes without ambiguity.
```

---

## Issue P4.5 — AEON/APXi Integration with PressWindowContext

**Title:**  
`[SPEC-004][P3] Integrate AEON/APXi with PressWindowContext`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:press`, `component:aeon`, `component:apxi`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Wire AEON and APXi into the existing PressWindowContext so that:

- Each AEON window can have associated streams and descriptors,
- APXi results are attached to or referenced by `APXManifest_v1` or an associated structure.

## Spec References

- Astral Press / AEON/APXi master spec
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/AEONWindowGrammar_v1.md`
- `docs/contracts/APXiDescriptor_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`

## Goals

- Make AEON/APXi feel like a natural extension of existing Press windows, not a separate subsystem.
- Ensure manifest_check remains deterministic when AEON/APXi are active or inactive.

## Tasks

- [ ] Extend `PressWindowContext` to:
  - [ ] Associate windows with AEON window IDs.
  - [ ] Store optional APXi descriptor sets per stream/window.
- [ ] Decide and implement how APXi is surfaced:
  - [ ] Inline in `APXManifest_v1`, or
  - [ ] Via a companion `APXiView_v1` structure referenced from the manifest.
- [ ] Ensure `manifest_check` includes or excludes APXi consistently per spec.
- [ ] Add tests:
  - [ ] Scenario with AEON/APXi disabled → behaviour identical to P2.
  - [ ] Scenario with AEON/APXi enabled on a small demo window/stream.

## Acceptance Criteria

- [ ] AEON/APXi can be toggled via config without changing baseline P2 behaviour.
- [ ] AEON windows and APXi descriptors are accessible via PressWindowContext and manifests.
```

---

## Issue P4.6 — AEON/APXi Demo Scenario & Snapshot

**Title:**  
`[SPEC-004][P3] AEON/APXi demo scenario & regression snapshot`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:press`, `component:aeon`, `component:apxi`, `component:codex`, `type:tests`, `priority:high`

```markdown
## Summary

Create a **small, canonical AEON/APXi demo scenario** that:

- Uses AEON windows over a short run,
- Applies APXi descriptors to at least one stream,
- Captures outputs in snapshots for regression,
- Optionally feeds Codex with AEON/APXi motifs.

## Spec References

- Astral Press / AEON/APXi master spec (examples section)
- `docs/contracts/AEONWindowGrammar_v1.md`
- `docs/contracts/APXiDescriptor_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/CodexContracts_v1.md` (optional for motif ingest)

## Goals

- Provide a concrete example of AEON/APXi in action.
- Lock in deterministic outputs as a test anchor for future changes.

## Tasks

- [ ] Design an AEON/APXi demo:
  - [ ] Small run (e.g. 8–16 ticks) with 1–2 streams.
  - [ ] Simple but non-trivial temporal patterns.
- [ ] Implement test harness:
  - [ ] Create AEON windows.
  - [ ] Apply APXi descriptors.
  - [ ] Generate APX manifests (and APXi views if separate).
- [ ] Snapshot outputs under `tests/fixtures/snapshots/aeon_apxi_demo/`.
- [ ] Add regression tests:
  - [ ] New runs must match the snapshot.
  - [ ] Ensure enabling/disabling AEON/APXi has predictable effects.
- [ ] (Optional) Feed AEON/APXi outputs into Codex ingest and confirm deterministic motifs.

## Acceptance Criteria

- [ ] AEON/APXi demo scenario is documented and deterministic.
- [ ] Snapshot tests guard against accidental changes to AEON/APXi behaviour.
```

---

## Issue P4.7 — Codex Ingest of AEON/APXi Artefacts (Observer-Only)

**Title:**  
`[SPEC-004][P3] Codex ingest of AEON/APXi artefacts (observer-only)`

**Labels:**  
`spec:SPEC-004`, `phase:P3`, `component:codex`, `component:press`, `component:aeon`, `component:apxi`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Wire AEON/APXi outputs into Codex ingest so that:

- AEON windows and APXi descriptors are visible to Codex,
- Codex can learn motifs over these structures,
- Codex remains observer-only (no actioning yet).

## Spec References

- Codex Eterna master spec
- Astral Press / AEON/APXi master spec
- `docs/contracts/CodexContracts_v1.md`
- `docs/contracts/AEONWindowGrammar_v1.md`
- `docs/contracts/APXiDescriptor_v1.md`

## Goals

- Give Codex richer, higher-level views of system behaviour via AEON/APXi.
- Preserve determinism and non-invasiveness (Codex reads only).

## Tasks

- [ ] Extend Codex ingest pipeline to accept:
  - [ ] AEON window definitions.
  - [ ] APXi descriptors and their MDL stats.
- [ ] Define at least one AEON/APXi-specific motif type.
- [ ] Add tests:
  - [ ] Run AEON/APXi demo scenario and ingest into Codex.
  - [ ] Ensure same run → same AEON/APXi motifs and proposals.
  - [ ] Confirm that Codex outputs do not change engine behaviour.

## Acceptance Criteria

- [ ] Codex can see and learn from AEON/APXi artefacts.
- [ ] Ingested data is deterministic and read-only.
```

---

## Notes

- SPEC-004 builds **on top of SPEC-005 (Press V1)** and SPEC-003 (Gate IO): AEON/APXi should feel like a natural extension, not a separate system.
- Once SPEC-006 and SPEC-007 are online, AEON/APXi will interact with multi-graph runs and governance, but this issue pack keeps Codex and AEON/APXi in **observer-only & configurational mode** for Phase 3.
