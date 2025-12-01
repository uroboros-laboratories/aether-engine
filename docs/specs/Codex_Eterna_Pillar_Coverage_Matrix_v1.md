# Codex Eterna Pillar Coverage Matrix — v1 (Draft)

## Status

- **Pillar:** Codex Eterna (Motifs, Library, Proposals)  
- **Doc:** Coverage of Codex Eterna master-spec implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Map Codex Eterna master spec requirements to SPEC-001–007 and phases, surfacing gaps on the way to 100% coverage.

This is a **first-pass coverage map** grouped by theme. Once the repo and tests exist we can tighten this to section/line-level references against `Codex Eterna — Master spec.txt` and Codex contract docs.

## Phase 6 Coverage Crosswalk

- **Proposal gate + ledger delivered.** `tests/unit/test_codex_proposal_gate.py` covers proposal evaluation, acceptance/rejection, and hash-chained structural ledger entries.
- **Governance linkage validated.** Governance snapshots and `tests/integration/test_full_system_demo.py` show Codex decisions entering U-Ledger alongside PFNA and Loom artifacts.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this coverage doc (later mapped to section refs in Codex master spec / contracts).  
- **Master Spec Theme** — Short label for the requirement group from Codex.  
- **Summary** — What the requirement demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it’s primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level Requirements)

### 2.1 Core Types & Records

| Req ID   | Master Spec Theme            | Summary                                                                                                  | Primary Specs                   | Phase | Notes / Tests |
|----------|------------------------------|----------------------------------------------------------------------------------------------------------|---------------------------------|-------|---------------|
| CDEX-01  | CodexLibraryEntry core       | Define `CodexLibraryEntry_v1` to represent a learned motif/template plus MDL/usage stats.               | SPEC-005, SPEC-007              | P2–P5 | Introduced in SPEC-005 Codex contracts; extended in SPEC-007 for governance context. |
| CDEX-02  | CodexProposal core           | Define `CodexProposal_v1` as a record describing a proposed structural/config change based on motifs.   | SPEC-005, SPEC-007              | P2–P5 | Observer-only in P2 (no action); governed in P5. |
| CDEX-03  | CodexContext runtime         | Define `CodexContext` as the runtime container holding library entries, proposals, and ingest state.    | SPEC-005                        | P2    | P2.6.1 CodexContext epic. |
| CDEX-04  | Motif descriptor types       | Define motif-specific record types (e.g. edge flux pattern, window pattern, AEON/APXi motif handles).   | SPEC-005, SPEC-004              | P2–P3 | First motif types in P2; AEON/APXi-linked motifs in P3. |

### 2.2 Ingest & Trace Sources

| Req ID   | Master Spec Theme            | Summary                                                                                          | Primary Specs                      | Phase | Notes / Tests |
|----------|------------------------------|--------------------------------------------------------------------------------------------------|------------------------------------|-------|---------------|
| CDEX-10  | UMX ingest                    | Codex can ingest sequences of `UMXTickLedger_v1` as raw state/flux traces.                      | SPEC-005, SPEC-006                 | P2–P4 | P2 baseline; P4 adds multi-graph context. |
| CDEX-11  | Loom ingest                   | Codex can ingest Loom P/I-blocks and chain values as temporal context for motifs.               | SPEC-005, SPEC-006                 | P2–P4 | Time-aware motifs rely on Loom chain/blocks. |
| CDEX-12  | Press/APX ingest              | Codex can ingest `APXManifest_v1`, AEON windows, and APXi descriptors as higher-level descriptors. | SPEC-005, SPEC-004              | P2–P3 | P2 basic manifest ingest; P3 AEON/APXi-aware ingest. |
| CDEX-13  | NAP/Gate ingest               | Codex can ingest selected NAP envelopes (especially CTRL/DATA) to learn from external IO patterns. | SPEC-005, SPEC-003, SPEC-007  | P2–P5 | Governance-aware motifs may depend on NAP CTRL patterns in P5. |
| CDEX-14  | U-ledger ingest               | Codex can read ULedgerEntry_v1 chains as a compressed view of system evolution and decisions.   | SPEC-005, SPEC-007                 | P2–P5 | Useful for governance-aware motif learning. |

### 2.3 Motif Identification & Library Growth

| Req ID   | Master Spec Theme            | Summary                                                                                          | Primary Specs      | Phase | Notes / Tests |
|----------|------------------------------|--------------------------------------------------------------------------------------------------|--------------------|-------|---------------|
| CDEX-20  | Primitive motif types        | Implement at least one primitive motif type (e.g. edge flux pattern) with deterministic detection rules. | SPEC-005      | P2    | P2.6.2 motif identification epic. |
| CDEX-21  | Repeated pattern detection   | Detect repeated patterns in sequences (e.g. flux patterns, chain patterns, descriptor patterns).| SPEC-005, SPEC-004 | P2–P3 | Initially simple heuristics; Mapped to APXi/AEON patterns in P3. |
| CDEX-22  | MDL/usage stats              | For each motif, compute MDL-ish metrics (description length vs savings) and usage statistics.   | SPEC-005, SPEC-004 | P2–P3 | Based on Press/APX MDL accounting and AEON/APXi descriptors. |
| CDEX-23  | Deterministic learning       | Given same trace inputs and config, motif learning must be deterministic (no stochastic search).| SPEC-005, SPEC-007 | P2–P5 | Double-run equality tests for motif libraries. |
| CDEX-24  | Library stability            | Library entries are stable across runs unless inputs/config change; supports snapshot/regression.| SPEC-005, SPEC-007 | P2–P5 | Snapshot tests for Codex libraries. |

### 2.4 Proposal Generation (Observer Mode in P2–P4)

| Req ID   | Master Spec Theme            | Summary                                                                                              | Primary Specs        | Phase | Notes / Tests |
|----------|------------------------------|------------------------------------------------------------------------------------------------------|----------------------|-------|---------------|
| CDEX-30  | Proposal emission            | Generate `CodexProposal_v1` records from motifs that meet thresholds (usage, MDL, etc.).            | SPEC-005, SPEC-007   | P2–P5 | P2 observer-only; P5 governance allows some proposals to act. |
| CDEX-31  | Proposal types               | Define proposal types (e.g. `PLACE`, `ADD`, `TUNE`) for structural/config changes across pillars.   | SPEC-005, SPEC-006, SPEC-007 | P2–P5 | Ties into multi-graph and governance specs. |
| CDEX-32  | Proposal determinism         | Identical inputs + config → identical proposal sets (order and content).                            | SPEC-005, SPEC-007   | P2–P5 | Double-run equality tests. |
| CDEX-33  | Observer-only enforcement    | Up to P4, proposals must not directly change engine behaviour; they are logs/observations only.     | SPEC-005, SPEC-006   | P2–P4 | Ensured by architecture: no direct write paths from Codex to UMX/Loom/etc. |

### 2.5 Integration with Governance & U-ledger

| Req ID   | Master Spec Theme            | Summary                                                                                                          | Primary Specs       | Phase | Notes / Tests |
|----------|------------------------------|------------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| CDEX-40  | Proposal → governance link   | In P5, proposals become inputs to governance decision flows (policy evaluation & budgeting).                    | SPEC-007            | P5    | GovernanceDecision_v1 consumes CodexProposal_v1. |
| CDEX-41  | Governance-aware proposal state| Proposals must carry status: `PENDING`, `APPROVED`, `REJECTED`, `EXPIRED`, etc., updated by Gate/TBP governance logic. | SPEC-007  | P5    | Codex tracks statuses but doesn’t decide them. |
| CDEX-42  | U-ledger recording           | Key Codex states (library snapshots, proposal sets) can be hashed and recorded in U-ledger for audit/replay.    | SPEC-005, SPEC-007  | P2–P5 | ULedgerEntry_v1 may include `codex_hash`. |
| CDEX-43  | Replay & rebuild             | Using U-ledger + raw traces, Codex library & proposals should be reconstructible deterministically.             | SPEC-005, SPEC-007  | P2–P5 | Replay tests that rebuild library/proposals from ledger + inputs. |

### 2.6 Scope & Guardrails (Codex Behaviour)

| Req ID   | Master Spec Theme            | Summary                                                                                                          | Primary Specs | Phase | Notes / Tests |
|----------|------------------------------|------------------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| CDEX-50  | Observer-only until governed | Codex must not directly mutate engine structures; all changes must pass through governance and Gate/TBP.       | SPEC-005, SPEC-007 | P2–P5 | Architecture & tests ensure no direct mutation APIs exist. |
| CDEX-51  | Non-invasive ingest          | Ingest must not alter underlying traces; Codex is a pure consumer.                                             | SPEC-005       | P2    | Tests: ingest vs non-ingest runs produce identical engine outputs. |
| CDEX-52  | Bounded complexity           | Codex analysis must be bounded by budgets/policies (e.g. no infinite motif expansion).                          | SPEC-007       | P5    | Governance budgets for Codex CPU/complexity; tests for enforcement. |
| CDEX-53  | Transparency & explainability| Motifs and proposals must be inspectable: show which traces they came from and their MDL/usage rationale.      | SPEC-005, SPEC-004, SPEC-007 | P2–P5 | Codex APIs to query motifs, coverage, and reasons. |

### 2.7 AEON/APXi-Specific Motifs (Temporal/Structural)

| Req ID   | Master Spec Theme          | Summary                                                                                       | Primary Specs | Phase | Notes / Tests |
|----------|----------------------------|-----------------------------------------------------------------------------------------------|---------------|-------|---------------|
| CDEX-60  | AEON window motifs         | Learn motifs over AEON windows (e.g. frequently recurring temporal shapes or window sequences).| SPEC-004, SPEC-005 | P3–P4 | AEON windows become Codex motif substrates. |
| CDEX-61  | APXi descriptor motifs     | Learn motifs in APXi descriptor space (e.g. repeated descriptor patterns).                   | SPEC-004, SPEC-005 | P3–P4 | APXiDescriptor_v1 becomes motif domain. |
| CDEX-62  | Cross-pillar motifs        | Combine UMX/Loom/Press patterns into composite motifs (e.g. flux + chain + descriptor).      | SPEC-004, SPEC-005, SPEC-006 | P3–P4 | Potentially used for multi-graph SLP proposals. |

---

## 3. Phase-by-Phase View (Codex Eterna Only)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

Codex is not active here.

- No Codex runtime in P1; Codex contracts and behaviour are not required to pass GF-01.  
- The Codex pillar is conceptually present but implementation is deferred.

Coverage notes:

- P1 is purely about getting a deterministic baseline. Codex comes later and **must not retroactively disturb** P1 behaviour.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

Codex comes online in **observer-only mode**:

- `CodexContext` defined and implemented (CDEX-03).  
- Ingest pipelines implemented for UMX, Loom, Press, NAP, and U-ledger traces (CDEX-10–CDEX-14).  
- Primitive motif identification with simple deterministic heuristics (CDEX-20–CDEX-23).  
- Motif libraries stored as `CodexLibraryEntry_v1` records with basic MDL/usage stats (CDEX-01, CDEX-22).  
- Proposals generated as `CodexProposal_v1` but **not applied** (CDEX-30–CDEX-33, CDEX-50).  
- Determinism & snapshot tests ensure same inputs → same library & proposals (CDEX-23, CDEX-24, CDEX-32).  

Coverage notes:

- P2 makes Codex a **read-only analytics pillar** that observes and suggests but cannot act.

---

### Phase 3 — SPEC-003 & SPEC-004 (PFNA V0 + AEON/APXi)

Codex becomes richer in what it can see and describe:

- SPEC-003 (Gate/PFNA V0) adds PFNA + richer NAP semantics:  
  - Codex can include PFNA-coded external inputs and NAP/CTRL patterns in motifs (CDEX-13).  

- SPEC-004 (Press AEON/APXi) extends motif substrate:  
  - AEON windows and APXi descriptors are ingestible; new motif types over those domains (CDEX-21, CDEX-60, CDEX-61).  
  - MDL/usage stats integrate Press/APX costs and descriptor lengths (CDEX-22).  

Coverage notes:

- Codex still cannot act; it just sees **more structure** and can make richer proposals and motif libraries.

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

Codex learns in a multi-graph, dynamic topology world:

- Ingest includes multi-graph UMX/Loom/Press traces and SLP events (CDEX-10–CDEX-12, CDEX-62).  
- Motifs can involve:  
  - Patterns in graph growth/shrinkage,  
  - Recurring SLP event sequences,  
  - Cross-graph relationships found via Gate routing patterns.  
- Proposals may include multi-graph structural suggestions (e.g. new links, typical growth patterns), but still observer-only in P4 (CDEX-31, CDEX-33).  

Coverage notes:

- P4 gives Codex a **richer environment to analyse**, but governance and actioning are still off.

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

Codex becomes an **advisor with teeth**, but only via governance:

- Proposals flow into governance:  
  - GovernanceDecision_v1 evaluates CodexProposal_v1 under policies and budgets (CDEX-40).  
  - Codex tracks proposal status but does not decide it (CDEX-41, CDEX-50).  
- Budgets constrain Codex complexity: how much motif search, how deep descriptor exploration (CDEX-52).  
- Key Codex states and decisions recorded in U-ledger & NAP CTRL for audit and replay (CDEX-42–CDEX-43).  
- Deterministic replay ensures same inputs and governance → same libraries, proposals, and decisions.  

Coverage notes:

- P5 does **not** change Codex’s core learning logic; it wraps it inside a governed loop with U-ledger trail.

---

## 4. Known / Likely Gaps (to Refine)

Once we do a line-level pass on the Codex master spec, we should refine:

1. **Exact motif taxonomy**  
   - Master spec may define multiple motif classes (temporal, structural, cross-graph, cross-pillar).  
   - Each should become a specific CDEX-2x/6x requirement with spec references and tests.

2. **Proposal taxonomy & scopes**  
   - Proposals might be tied to specific pillars (UMX topology, Loom chain params, Press schemes, Gate routing).  
   - We should add CDEX-3x rows per proposal scope and map them to SPEC-006/007 governance rules.

3. **Scoring & ranking of motifs**  
   - Master spec likely includes more precise scoring, ranking, or filtering rules for which motifs/proposals are considered.  
   - Add CDEX-2x/3x entries for scoring/ranking, and tests that prove stability.

4. **Performance & complexity envelopes**  
   - Codex might have explicit complexity constraints (max motifs, max depth, etc.).  
   - Those would be tied tightly to SPEC-007 budgets and might warrant separate performance tests.

5. **User-facing inspection APIs**  
   - Master spec may define how operators can query Codex libraries/proposals.  
   - We should add CDEX-5x entries for these APIs and tests ensuring explainability.

These are not blockers but are important for a v2, fine-grained coverage doc once all Codex contracts are stable.

---

## 5. Next Steps

For Codex Eterna pillar coverage, once the repo exists:

1. **Add “Master Spec Ref” column**  
   - Link each CDEX-xx row to section anchors in `Codex Eterna — Master spec.txt` and Codex contract files.

2. **Bind tests & fixtures**  
   - Map each requirement to specific tests (e.g. `tests/codex/test_motif_learning_gf01.py`, `tests/codex/test_proposals_determinism.py`).

3. **Combine with other pillar coverage docs**  
   - Once UMX, Loom, Press, Gate/TBP, Codex, and U-ledger coverage matrices are all in place, we can build a top-level coverage index that shows **100% mapping** from master specs → SPEC-00X → phases → concrete tests.
