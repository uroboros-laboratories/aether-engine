# Astral Press / APX Pillar Coverage Matrix — v1 (Draft)

## Status

- **Pillar:** Astral Press / APX  
- **Doc:** Coverage of Press/APX master-spec implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Map the Press/APX master spec requirements to SPEC-001–007 and phases, and surface obvious gaps on the road to 100% coverage.

This is a **first-pass coverage map**: we group master-spec requirements into themes. Later, we can refine this to line/section-level coverage once the repo and tests exist.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this coverage doc (we can later bind these to exact section refs in `astral_press_master_implementation_spec_combined_v1.md`).  
- **Master Spec Theme** — Short label for the requirement group from the Press/APX master spec.  
- **Summary** — What the requirement demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it’s primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level Requirements)

### 2.1 Core Types & Records

| Req ID   | Master Spec Theme          | Summary                                                                                                             | Primary Specs                                      | Phase | Notes / Tests |
|----------|----------------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|-------|---------------|
| PRESS-01 | APXStream core record      | Define `APXStream_v1` to represent a single encoded integer stream: scheme, parameters, MDL fields, etc.          | SPEC-002, SPEC-005                                 | P1–P2 | P1 uses implicit stream concept for S1/S2 in GF-01; P2 formalises stream type. |
| PRESS-02 | APXManifest core record    | Define `APXManifest_v1` as the per-window manifest: list of streams, their costs, and global `manifest_check`.    | SPEC-002, SPEC-005, SPEC-004                       | P1–P3 | P1 GF-01 APX sheets; P2 generalises; P3 extends with AEON/APXi metadata. |
| PRESS-03 | PressWindowContext         | Context object for managing multiple streams within a Press window: buffering, scheme hints, and closing windows. | SPEC-005, SPEC-004                                 | P2–P3 | P2.3.1 introduces PressWindowContext & registry; P3 reuses it for AEON/APXi. |
| PRESS-04 | Scheme descriptor metadata | Represent scheme configuration & parameters in a structured way (ID/R/GR/AEON/APXi).                               | SPEC-005, SPEC-004                                 | P2–P3 | P2 defines basic scheme descriptors; P3 extends for AEON/APXi. |

### 2.2 Schemes & MDL Accounting

| Req ID   | Master Spec Theme     | Summary                                                                                                     | Primary Specs     | Phase | Notes / Tests |
|----------|-----------------------|-------------------------------------------------------------------------------------------------------------|-------------------|-------|---------------|
| PRESS-10 | ID scheme (identity)  | Implement ID scheme for raw encoding of integer sequences with deterministic MDL accounting.               | SPEC-005          | P2    | P2.3.2 ID scheme implementation and tests (constant/simple sequences). |
| PRESS-11 | R scheme (run-based)  | Implement R scheme (run-length-like) used by GF-01, with exact bit counts and MDL fields.                 | SPEC-002, SPEC-005| P1–P2 | P1 GF-01 reference; P2 cleans up and generalises but must keep GF-01 outputs identical. |
| PRESS-12 | GR scheme (grouped R) | Implement basic GR scheme for clustered runs, with deterministic cost accounting.                          | SPEC-005          | P2    | P2.3.2 GR scheme implementation and tests. |
| PRESS-13 | AEON/APXi scheme set  | Extend scheme set with AEON/APXi, representing hierarchical/descriptor-based coding over windows.         | SPEC-004          | P3    | P3.5 APXi descriptor language; P3.6 integration with manifests/views. |
| PRESS-14 | Integer-only MDL      | All MDL costs (`L_model`, `L_residual`, `L_total`) are integers; no floating point, no probabilistic fudge.| SPEC-002, 005, 004| P1–P3 | Enforced via tests and determinism harness; manifest_check is integer. |

### 2.3 Windows & AEON Grammar

| Req ID   | Master Spec Theme       | Summary                                                                                                      | Primary Specs       | Phase | Notes / Tests |
|----------|-------------------------|--------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| PRESS-20 | Fixed windows (V0/V1)   | Support fixed windows with tick ranges (e.g. ticks 1–8, 1–2 in GF-01) with deterministic manifest outputs. | SPEC-002, SPEC-005  | P1–P2 | GF-01 APX fixtures are canonical tests; P2 generalises for arbitrary ranges. |
| PRESS-21 | Multi-stream windows    | Support multiple named streams per window managed by `PressWindowContext`.                                  | SPEC-005            | P2    | P2.3.1 registry + multiple streams per window. |
| PRESS-22 | AEON window grammar     | Define `AEONWindowGrammar_v1` for hierarchical windows (base windows, aggregates, sliding, etc.).          | SPEC-004            | P3    | P3.4 AEON grammar epic. |
| PRESS-23 | AEON queries            | Provide APIs to query AEON hierarchy: get windows, children, coverage, etc.                                | SPEC-004            | P3    | P3.4 AEON view/query API. |

### 2.4 APXi Descriptor Language

| Req ID   | Master Spec Theme       | Summary                                                                                                     | Primary Specs       | Phase | Notes / Tests |
|----------|-------------------------|-------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| PRESS-30 | APXiDescriptor contract | Define `APXiDescriptor_v1` to encode descriptors (pattern codes) over streams and windows.                 | SPEC-004            | P3    | P3.5 descriptor contract design. |
| PRESS-31 | Primitive descriptors   | Implement primitive APXi types (constant segments, repeats, simple trends, piecewise combos).             | SPEC-004            | P3    | P3.5 primitive set; applied to synthetic sequences in tests. |
| PRESS-32 | APXi MDL accounting     | Implement MDL accounting for APXi descriptors and their residuals, all in integer bit counts.              | SPEC-004            | P3    | P3.5 MDL rules; tests compare APXi vs raw ID/R on simple sequences. |
| PRESS-33 | Integration with streams| Attach APXi descriptors to streams/windows, either inside manifests or companion records.                  | SPEC-004            | P3    | P3.6 AEON/APXi integration. |

### 2.5 Integration with UMX, Loom, Gate, Codex

| Req ID   | Master Spec Theme         | Summary                                                                                                              | Primary Specs               | Phase | Notes / Tests |
|----------|---------------------------|----------------------------------------------------------------------------------------------------------------------|-----------------------------|-------|---------------|
| PRESS-40 | UMX stream sourcing       | Build streams from UMX outputs (e.g. post_u deltas, fluxes) as in GF-01 and beyond.                                 | SPEC-002, SPEC-005, 004     | P1–P3 | GF-01 S1/S2; P2 general multi-stream sourcing; P3 AEON/APXi reuse same base data. |
| PRESS-41 | Loom/chain integration    | Allow chain-related values (e.g. `C_t`, window-level stats) to be included as streams or context for models.       | SPEC-005, SPEC-004          | P2–P3 | Press may encode chain features or use them in descriptors; AEON windows align with Loom ticks. |
| PRESS-42 | Gate/TBP / SceneFrame link| Stream configuration may be driven by Gate/TBP config and SceneFrame metadata (e.g. which windows to run).         | SPEC-003, SPEC-004, SPEC-005| P2–P3 | Gate/SceneFrame specify windowing + which streams to compress; Press follows deterministically. |
| PRESS-43 | Codex ingest & feedback   | Press outputs (manifests, AEON/APXi views) are ingested by Codex for motif learning and proposal generation.       | SPEC-005, SPEC-004, SPEC-007| P2–P5 | CodexContext uses Press artefacts as part of its trace; governance controls actioning. |
| PRESS-44 | U-ledger inclusion        | `APXManifest_v1` and related AEON/APXi artefacts must be serialised & hashed into ULedger entries.                 | SPEC-002, 005, 004, 007     | P1–P5 | SPEC-002: manifest in GF-01 snapshot; SPEC-005: canonical serialisation; SPEC-004: AEON/APXi; SPEC-007: governance links. |

### 2.6 Determinism, manifest_check & Snapshots

| Req ID   | Master Spec Theme        | Summary                                                                                                    | Primary Specs       | Phase | Notes / Tests |
|----------|--------------------------|------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| PRESS-50 | manifest_check invariant | `manifest_check` must be a deterministic, reproducible integer derived from manifest contents.           | SPEC-002, 005, 004  | P1–P3 | GF-01 values (487809945, 869911338) are canonical tests; AEON/APXi must preserve determinism. |
| PRESS-51 | Double-run determinism   | Two runs with same config must yield identical manifests and manifest_checks.                            | SPEC-002, SPEC-005  | P1–P2 | Covered by determinism harness in SPEC-002 and extended in SPEC-005. |
| PRESS-52 | Snapshot regression      | Known-good manifests (GF-01, AEON/APXi demos) must be snapshotted and compared byte-for-byte.            | SPEC-002, SPEC-004, 005 | P1–P3 | P1 GF-01; P3 AEON/APXi scenario(s) added to snapshot suite. |

### 2.7 Governance & Policy (Press-Relevant)

| Req ID   | Master Spec Theme      | Summary                                                                                                  | Primary Specs | Phase | Notes / Tests |
|----------|------------------------|----------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| PRESS-60 | Governance over schemes| Which schemes/modes (ID, R, GR, AEON, APXi) are allowed in a run may be governed via policy.            | SPEC-007      | P5    | Policy config may restrict heavy schemes or experimental modes. |
| PRESS-61 | Budget for Press costs | Budgets may constrain how much complexity/description length can be “spent” on AEON/APXi per period.   | SPEC-007      | P5    | Budget classes could include APXi usage, AEON depth, etc. |
| PRESS-62 | Traceable Press decisions| Governance decisions that affect Press (e.g. disabling APXi) must be visible in NAP CTRL and ledger.  | SPEC-007      | P5    | GovernanceDecision_v1 + U-ledger entries link policy to Press behaviour. |

---

## 3. Phase-by-Phase View (Press/APX Only)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

Press/APX focus:

- Implement minimal R-mode APX for GF-01:  
  - Two streams: S1 (post_u deltas), S2 (flux sequences) (PRESS-40).  
  - Fixed windows: ticks 1–8 and ticks 1–2 (PRESS-20).  
  - Exact `L_total` and `manifest_check` matching GF-01 APX sheets (PRESS-11, PRESS-14, PRESS-50).  
- Manifests & streams may be implicit in the implementation but are functionally equivalent to `APXManifest_v1` and `APXStream_v1` records (PRESS-01, PRESS-02).  
- Determinism harness ensures manifest and manifest_check are stable for GF-01 (PRESS-51, PRESS-52).

Coverage notes:

- P1 is **deliberately narrow**: one profile, two streams, two windows, R-mode only.  
- It establishes GF-01 APX results as hard regression anchors for all future Press/APX work.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

Press/APX upgrades:

- Formalise `APXStream_v1` and `APXManifest_v1` contracts (PRESS-01, PRESS-02).  
- Introduce `PressWindowContext` to manage multiple named streams per window (PRESS-03, PRESS-21).  
- Implement scheme set: ID, R, basic GR (PRESS-10, PRESS-11, PRESS-12, PRESS-14).  
- Ensure manifests are generated for arbitrary windows with mixed scheme usage (PRESS-21, PRESS-50).  
- Strengthen determinism via canonical serialisation and snapshot tests (PRESS-51, PRESS-52).  
- Solid integration with UMX and Loom as stream sources and context (PRESS-40, PRESS-41, PRESS-44).

Coverage notes:

- P2 takes Press/APX from “special GF-01 compressor” to a **general multi-stream, multi-scheme compression engine**.  
- AEON/APXi concepts are not implemented yet; they appear in Phase 3.

---

### Phase 3 — SPEC-003 & SPEC-004 (AEON/APXi & IO)

Press/APX evolves in two directions:

- SPEC-003 (Gate/PFNA V0) interacts mainly via configuration and IO:  
  - Gate/TBP and SceneFrame decide which windows to run, which streams to route, and when (PRESS-42).  
  - PFNA-driven scenarios may adjust what is being compressed (but core Press logic unchanged).

- SPEC-004 (AEON/APXi) adds temporal and descriptive richness:  
  - AEON window grammar (`AEONWindowGrammar_v1`) defined and implemented (PRESS-22, PRESS-23).  
  - APXi descriptor language (`APXiDescriptor_v1`) designed and implemented with MDL accounting (PRESS-30–PRESS-32).  
  - AEON/APXi outputs integrated into manifests or companion records, with deterministic manifest_check (PRESS-33, PRESS-50).  
  - AEON/APXi views become queryable (PRESS-23).  

Coverage notes:

- P3 is where Press/APX moves from “compression” to **structured explanation over time**.  
- GF-01 regression remains a hard requirement: AEON/APXi must not perturb P1/P2 behaviour when disabled.

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

Press/APX interacts with multi-graph and SLP indirectly:

- Multi-graph runs may require:  
  - Streams tagged by graph ID or run context (PRESS-40, PRESS-42).  
  - AEON/APXi to handle multiple graphs’ streams simultaneously or separately.  
- SLP events alter which streams exist or how they’re interpreted, but Press remains a deterministic consumer.

Coverage notes:

- The Press master spec likely treats multi-graph concerns as context rather than core changes:  
  - Streams are still sequences of integers; what changes is which graph/run they come from.  
  - SPEC-006 ensures these contexts are visible and stable; Press simply honours the contracts.

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

Press/APX becomes constrained by governance and budgets:

- Governance policies can enable/disable specific schemes and modes (PRESS-60).  
- Budgets can cap how much APXi/AEON “complexity spend” is allowed per period (PRESS-61).  
- Governance decisions about Press (e.g. “no AEON for this run”) are visible in CTRL layer and ledger (PRESS-62).  
- Codex may propose changes to Press configuration (e.g. adopting AEON for certain windows), which must go through the proposal lifecycle before taking effect (PRESS-43 linked with governance).

Coverage notes:

- P5 doesn’t change the **mathematics** of Press/APX; it wraps it in policy & budgeting so advanced modelling can’t silently explode in complexity or cost.

---

## 4. Known / Likely Gaps (to Refine)

Areas to tighten once we do a line-level pass on the Press/APX master spec:

1. **Exact scheme parameterisation**  
   - Master spec may define detailed parameter sets for ID/R/GR/AEON/APXi.  
   - We should add PRESS-1x/3x rows for specific parameters and bind them to SPEC-00X and tests.

2. **AEON/APXi edge cases**  
   - Handling overlapping windows, nested descriptors, and borderline cases (e.g. empty or trivial windows).  
   - Add coverage rows once grammar and descriptor sets are fully nailed down.

3. **Cross-stream models**  
   - If the master spec calls for APXi to model relationships between streams (e.g. S1 vs S2 correlations), we should:  
     - Add requirements (PRESS-3x),  
     - Map them to SPEC-004 epics and tests.

4. **Performance / scaling constraints**  
   - Any constraints on Press computational complexity, memory usage, or maximum window sizes will likely live in a later performance spec; we can reference that from here.

5. **Codex interaction specifics**  
   - Master spec might define precise hooks for how Codex reads Press outputs (e.g. summary stats or codebooks).  
   - Add PRESS-4x coverage items once Codex contracts are final.

These are not blockers for implementation, but they mark areas for deeper coverage in a v2 of this document.

---

## 5. Next Steps

For the Press/APX pillar coverage:

1. **Add “Master Spec Ref” column**  
   - Attach section/anchor IDs from `astral_press_master_implementation_spec_combined_v1.md` to each requirement row.  

2. **Bind tests once the repo exists**  
   - For each requirement, link to specific tests and fixtures (e.g. `tests/press/test_gf01_manifests.py`, AEON/APXi demo tests).  

3. **Mirror this approach for remaining pillars**  
   - Gate/TBP, Codex Eterna, and U-ledger each get their own coverage matrices, then we can build a global coverage dashboard over all pillars and specs.
