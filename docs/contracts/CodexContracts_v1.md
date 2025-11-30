# Codex Contracts — CodexLibraryEntry_v1 and CodexProposal_v1 (Skeletons)

## Purpose

Codex Eterna is the **self-learning pillar** that builds and maintains libraries of reusable motifs and rules, and proposes structural changes to the engine.

For the initial implementation phases, we define **skeleton contracts**:

- `CodexLibraryEntry_v1` — describes a learned motif or pattern.
- `CodexProposal_v1` — describes a proposed placement or structural change.

Phase 3 extends these skeletons so Codex can **ingest AEON/APXi artefacts** in an
observer-only fashion. APXi descriptors and AEON windows are made visible to
Codex for motif learning while keeping engine behaviour unchanged.

These contracts are designed to be:

- Simple enough for early “observer-only” implementations,
- Rich enough to support full MDL-driven learning later.

---

## CodexLibraryEntry_v1

### High-Level Role

Represents one learned **motif** in the Codex library:

- Found via analysis of UMX/Loom/Press traces,
- Associated with a specific CMP profile (e.g. CMP-0),
- Carries MDL and reuse statistics.

### Record Shape

Logical record name: `CodexLibraryEntry_v1`

Top-level fields:

1. **library_id: string**  
   - Identifier for the Codex library (e.g. `"CE_MAIN"`).

2. **motif_id: string**  
   - Unique ID for this motif within the library.

3. **profile: string**  
   - Profile under which this motif is valid (e.g. `"CMP-0"`).

4. **source_gid: string**  
   - Graph/run ID from which this motif was originally extracted (e.g. `"GF01"`).

5. **source_window_id: string**  
   - Window identifier where this motif was first discovered (e.g. `"GF01_W1_ticks_1_8"`).

6. **pattern_descriptor: object**  
   - Abstract description of the motif (to be refined later).  
   - For early phases, may include:
     - Node/edge subsets,
     - Repeated flux patterns,
     - Simple time-local patterns.

7. **mdl_stats: object**  
   - Description length and savings statistics, e.g.:
     - `L_self`: bits to describe the motif itself.
     - `L_usage`: bits to describe all usages.
     - `L_total`: `L_self + L_usage`.
     - `delta_vs_baseline`: change in total description length vs not having this motif.

8. **usage_stats: object**  
   - How often and where this motif has been used:
     - `usage_count`: total number of placements.
     - Optional maps keyed by graph or window.

9. **created_at_tick: int**  
   - Tick at which this motif was first committed to the library.

10. **last_updated_tick: int**  
    - Most recent tick at which stats or descriptor changed.

11. **meta: object (optional)**  
    - Free-form metadata (labels, comments, tags).

Example (very rough, CMP-0 placeholder):

```jsonc
{
  "library_id": "CE_MAIN",
  "motif_id": "MOTIF_0001",
  "profile": "CMP-0",
  "source_gid": "GF01",
  "source_window_id": "GF01_W1_ticks_1_8",
  "pattern_descriptor": {
    "type": "edge_flux_pattern_v1",
    "edges": [1, 2, 3],
    "du_signature": [1, 1, -2]
  },
  "mdl_stats": {
    "L_self": 24,
    "L_usage": 16,
    "L_total": 40,
    "delta_vs_baseline": -8
  },
  "usage_stats": {
    "usage_count": 3
  },
  "created_at_tick": 8,
  "last_updated_tick": 8,
  "meta": {}
}
```

### APXi descriptor motifs (Phase 3 observer-only)

When APXi views are ingested, Codex may emit library entries with a
`pattern_descriptor` of type `apxi_descriptor_v1`:

```jsonc
{
  "type": "apxi_descriptor_v1",
  "descriptor": { /* APXiDescriptor_v1.to_dict() */ },
  "residual_scheme": "R",
  "stream_id": "S1_post_u_deltas",
  "apx_name": "LINE4_APX_W1_T1_6",
  "aeon_window_id": "AEON_LINE4_W_all"
}
```

`mdl_stats` for these entries mirror the APXi view breakdown:

- `L_self` ← descriptor model cost,
- `L_usage` ← residual cost for the view,
- `L_total` ← `L_self + L_usage`,
- `delta_vs_baseline` ← deterministic delta vs no descriptor (negative residuals).

---

## CodexProposal_v1

### High-Level Role

Represents a **proposal** made by Codex to change the engine’s structure or configuration, e.g.:

- Add a new motif,
- Place a motif at a certain location,
- Merge or retire a motif,
- Adjust thresholds/parameters.

The proposal is evaluated by the governance layer (UMX + Gate + profile barriers), which decides whether to accept it.

### Record Shape

Logical record name: `CodexProposal_v1`

Top-level fields:

1. **proposal_id: string**  
   - Unique ID for the proposal.

2. **library_id: string**  
   - Codex library this proposal is associated with.

3. **motif_id: string (optional)**  
   - ID of the motif involved, if applicable.

4. **gid: string**  
   - Graph/run ID the proposal targets.

5. **target_window_id: string (optional)**  
   - Window or tick range the proposal refers to.

6. **target_location: object**  
   - Location in the engine where the proposal would apply, e.g.:
     - Subset of nodes/edges,
     - Layer or profile segment.

7. **action: enum { "ADD", "PLACE", "MERGE", "RETIRE", "TUNE" }**  
   - Type of action:
     - `"ADD"`: add new motif to library.
     - `"PLACE"`: place an existing motif at a location.
     - `"MERGE"`: merge motifs.
     - `"RETIRE"`: retire motif.
     - `"TUNE"`: adjust parameters (e.g. MDL thresholds).

8. **expected_effect: object**  
   - Codex’s prediction of the proposal’s impact:
     - `delta_L_total`: expected change in total description length (bits).
     - `confidence`: optional confidence score.
     - `notes`: free-form rationale.

9. **budget_effect: object (optional)**  
   - Estimated effect on any resource budgets:
     - e.g. `delta_mu`, `delta_complexity`, etc.

10. **created_at_tick: int**  
    - Tick when the proposal was created.

11. **status: enum { "PENDING", "ACCEPTED", "REJECTED" }**
    - Proposal lifecycle status.

12. **governance_status: enum { "UNEVALUATED", "OK", "SOFT_FAIL", "HARD_FAIL" }**
    - Outcome of governance evaluation.

13. **violated_policies: array<string> (optional)**
    - Policy IDs that were not satisfied.

14. **governance_scores: object (optional)**
    - Structured evaluation scores (e.g. `topology_change_count`).

15. **governance_notes: object (optional)**
    - Notes from the evaluator (e.g. Gate/UMX/governance layer).

16. **evaluated_at_tick: int (optional)**
    - Tick when the proposal was evaluated.

Example (sketch):

```jsonc
{
  "proposal_id": "P0001",
  "library_id": "CE_MAIN",
  "motif_id": "MOTIF_0001",
  "gid": "GF01",
  "target_window_id": "GF01_W1_ticks_1_8",
  "target_location": {
    "nodes": [1, 2, 3],
    "edges": [1, 2, 3]
  },
  "action": "PLACE",
  "expected_effect": {
    "delta_L_total": -4,
    "confidence": 0.8,
    "notes": "Motif_0001 captures repeated flux pattern, reduces total description length."
  },
  "budget_effect": {
    "delta_mu": 0
  },
  "created_at_tick": 8,
  "status": "PENDING",
  "governance_notes": {}
}
```

---

## Early Implementation Guidance

For the **first codebase iterations**:

- Implement Codex as **observer-only**:
  - It reads UMX, Loom, APX artefacts.
  - It may emit `CodexLibraryEntry_v1` and `CodexProposal_v1` records.
  - It does **not** apply any changes to UMX or profiles yet.

- The governance layer (UMX + Gate + profile) can simply:
  - Mark all proposals as `status = "REJECTED"` or keep them `PENDING`.
  - Log them for inspection.

As the system matures, these contracts give you a clean way to:

- Turn proposals into structured NAP transactions,
- Update UMX / profiles / topologies in a governed, reversible way.
