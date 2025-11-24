# U-ledger Subsystem Coverage Matrix — v1 (Draft)

## Status

- **Subsystem:** Universal Ledger (U-ledger)  
- **Role:** Cross-pillar substrate (not a standalone pillar)  
- **Doc:** Coverage of U-ledger implementation requirements across SPEC-00X  
- **Version:** v1 (draft)  
- **Goal:** Map U-ledger-related requirements (hashing, serialisation, chain semantics, replay) to SPEC-001–007 and phases, without promoting it to a “6th pillar”.

U-ledger is treated here as a **cross-cutting substrate** that stitches the five core pillars together:

- UMX  
- Loom  
- Astral Press/APX  
- Trinity Gate/TBP + NAP/PFNA  
- Codex Eterna  

This matrix just makes sure all the ledger behaviours those pillars rely on are covered by SPEC-00X and tests.

---

## 1. Legend

- **Req ID** — Synthetic requirement identifier for this U-ledger coverage doc.  
- **Theme** — Short label for the requirement group.  
- **Summary** — What the requirement demands.  
- **Primary Specs** — SPEC-00X doc(s) that define implementation for this requirement.  
- **Phase** — Project phase where it’s primarily delivered (P1–P5).  
- **Notes / Tests** — How it’s validated (tests, fixtures, snapshots) or anything still TBD.

---

## 2. Coverage Table (High-Level U-ledger Requirements)

### 2.1 Core Types & Records

| Req ID     | Theme                          | Summary                                                                                                           | Primary Specs                | Phase | Notes / Tests |
|------------|--------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------|-------|---------------|
| ULED-01    | ULedgerEntry core record       | Define `ULedgerEntry_v1` as the canonical ledger record linking hashes from all pillars plus chain/meta fields.  | SPEC-005, SPEC-007          | P2–P5 | U-ledger contracts live here; entries include references to UMX, Loom, Press, NAP, Codex, governance. |
| ULED-02    | Ledger run metadata            | Each entry must carry run/session metadata: `gid`, `run_id`, tick/window IDs, timestamps or sequence counters.   | SPEC-005, SPEC-007          | P2–P5 | Provides indexing for replay and audit. |
| ULED-03    | Cross-pillar hash slots        | ULedgerEntry_v1 must have structured slots for hashes of UMX tick, Loom block, APX manifest, NAP envelope, etc. | SPEC-005                    | P2    | The exact set of hash fields is driven by pillar contracts. |

### 2.2 Canonical Serialisation & Hashing

| Req ID     | Theme                          | Summary                                                                                             | Primary Specs       | Phase | Notes / Tests |
|------------|--------------------------------|-----------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| ULED-10    | Canonical JSON serialisation   | Define canonical JSON serialisation rules for core records (ordering, numeric formats, whitespace).| SPEC-002, SPEC-005  | P1–P2 | SPEC-002 uses an early form for GF-01 snapshot; SPEC-005 formalises canonical rules. |
| ULED-11    | Hash algorithm                 | Choose and fix a hash algorithm (e.g. SHA-256) used uniformly across all U-ledger entries.         | SPEC-005            | P2    | Encapsulated in utility functions; no per-call algorithm changes. |
| ULED-12    | Hashing of records             | Implement `hash_record(record) -> hash_string` over canonical serialisation for each pillar record. | SPEC-005           | P2    | UMX/Loom/Press/NAP/Codex records hashed via shared utilities. |
| ULED-13    | Deterministic byte layout      | Given same record, canonical serialisation must produce identical bytes regardless of code path.   | SPEC-005            | P2    | Tests serialising from multiple paths and comparing byte-for-byte. |

### 2.3 Ledger Chain Semantics

| Req ID     | Theme                          | Summary                                                                                                              | Primary Specs       | Phase | Notes / Tests |
|------------|--------------------------------|----------------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| ULED-20    | Hash chain across entries      | ULedgerEntry_v1 includes `prev_entry_hash` so entries form a single, forward-only hash chain per run.               | SPEC-005            | P2    | Basic blockchain-like semantics (no forks in V1). |
| ULED-21    | Chain per run/session          | Each run/session has its own ledger chain identified by `run_id` (and optionally `gid`).                            | SPEC-005, SPEC-006  | P2–P4 | Multi-graph runs may share run_id but have graph-specific context. |
| ULED-22    | Inclusion of pillar hashes     | Each entry includes hashes of relevant pillar states/artefacts (UMX/Loom/Press/NAP/Codex/governance).              | SPEC-005, SPEC-007  | P2–P5 | Pillar coverage docs already expect these hash slots. |
| ULED-23    | Invariance under pillar replay | Recomputing pillar outputs and rehashing them for the same tick/window/run must yield the same ledger entries.      | SPEC-002, SPEC-005  | P1–P2 | Determinism harness tests; GF-01 snapshot is canonical example. |

### 2.4 Integration with Determinism & Snapshots

| Req ID     | Theme                          | Summary                                                                                                       | Primary Specs          | Phase | Notes / Tests |
|------------|--------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------|-------|---------------|
| ULED-30    | Double-run determinism harness | Two identical runs must produce identical U-ledger chains (byte-for-byte equality).                           | SPEC-002, SPEC-005     | P1–P2 | GF-01 harness in SPEC-002; extended in SPEC-005 to more scenarios. |
| ULED-31    | Snapshot baseline              | Known-good ledger chains (e.g. GF-01, demo runs) must be snapshotted and used for regression tests.          | SPEC-002, SPEC-005, SPEC-004 | P1–P3 | GF-01 first snapshot; AEON/APXi demos may add more. |
| ULED-32    | Replay from snapshots          | From a ledger snapshot, the system should be able to replay state and confirm equality with fresh runs.      | SPEC-005, SPEC-006     | P2–P4 | Uses pillar replay APIs plus ledger chain as reference. |

### 2.5 Multi-Graph & SLP Awareness

| Req ID     | Theme                          | Summary                                                                                                            | Primary Specs       | Phase | Notes / Tests |
|------------|--------------------------------|--------------------------------------------------------------------------------------------------------------------|---------------------|-------|---------------|
| ULED-40    | Multi-graph context            | Ledger entries must be able to encode which graph(s) a record relates to in multi-graph runs.                     | SPEC-006            | P4    | Graph IDs (gid) and possibly graph link info appear in entries. |
| ULED-41    | SLP event inclusion            | Structural events (SLP topology changes) are represented or referenced in ledger entries.                          | SPEC-006            | P4    | SLPEvent_v1 hashes added to or referenced by ULedgerEntry_v1. |
| ULED-42    | Consistent ordering with SLP   | Ordering of SLP events in the ledger must match their ordering in runtime (no reordering on replay).              | SPEC-006            | P4    | Replay tests for dynamic topology scenarios. |

### 2.6 Governance, Budgets & Audit Trail

| Req ID     | Theme                          | Summary                                                                                                             | Primary Specs | Phase | Notes / Tests |
|------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| ULED-50    | Governance decision recording  | GovernanceDecision_v1 (decisions on proposals, budgets, policies) must be hashed and/or linked in U-ledger.        | SPEC-007      | P5    | Each accepted/rejected proposal is traceable through ledger. |
| ULED-51    | Budget / policy snapshots      | Changes to budgets/policies are represented in ledger so that historical policy regimes are reconstructible.       | SPEC-007      | P5    | Enables time-travel audit: “what were the rules at tick T?”. |
| ULED-52    | End-to-end audit trail         | From ledger alone, an auditor can see: engine states, structural changes, governance decisions, and when they occurred. | SPEC-007  | P5    | Design requirement; validated via replay and inspection tooling. |
| ULED-53    | Governance determinism trail   | Same inputs/governance config → identical governance-related ledger history; differences mean genuine divergence.  | SPEC-007      | P5    | Detected via snapshot and replay tests. |

### 2.7 Scope & Guardrails (What U-ledger Is / Is Not)

| Req ID     | Theme                          | Summary                                                                                                       | Primary Specs | Phase | Notes / Tests |
|------------|--------------------------------|---------------------------------------------------------------------------------------------------------------|---------------|-------|---------------|
| ULED-60    | Read-only for engine           | U-ledger does **not** drive engine state; it records it. No write-back from ledger into live pillars.       | SPEC-005, SPEC-007 | P2–P5 | Replay uses ledger as reference, not as authoritative input that mutates live runs. |
| ULED-61    | Cross-pillar substrate         | U-ledger is not a sixth pillar; it’s infrastructure that sits underneath all five pillars.                  | SPEC-005, SPEC-007 | P2–P5 | Reflected in architecture and docs, including this coverage matrix. |
| ULED-62    | Performance & size constraints | Ledger must be append-only and efficient enough for intended workloads; pruning/archiving may be added later. | SPEC-007 (or future perf spec) | P5+ | Might be handled in a performance extension spec rather than core specs. |

---

## 3. Phase-by-Phase View (U-ledger as Substrate)

### Phase 1 — SPEC-002 (GF-01 CMP-0 Baseline)

U-ledger behaviour is mostly **implicit** but already present as ideas:

- Determinism harness & snapshot tests for GF-01 create the first proto-ledger notion: serialised artefacts compared across runs (ULED-10, ULED-23, ULED-30, ULED-31).  
- There may not be a full ULedgerEntry_v1 in code yet; instead, UMX/Loom/Press/NAP are snapshotted separately and compared.  

Coverage notes:

- P1 proves the concept of “a canonical history you can diff against” but doesn’t yet unify it as a ledger type.

---

### Phase 2 — SPEC-005 (Pillar V1 Generalisation)

U-ledger becomes a **real subsystem**:

- `ULedgerEntry_v1` contract is defined and implemented (ULED-01–03).  
- Canonical serialisation & hashing utilities exist and are used by all pillars (ULED-10–13).  
- Every tick/window/run can produce U-ledger entries chaining via `prev_entry_hash` (ULED-20–22).  
- Double-run determinism harness and snapshots now operate over U-ledger chains instead of ad-hoc bundles (ULED-30–32).  

Coverage notes:

- P2 is where U-ledger becomes the common **audit substrate** for all five pillars, but still without multi-graph/governance richness.

---

### Phase 3 — SPEC-003 & SPEC-004 (PFNA V0 + AEON/APXi)

U-ledger gains visibility into more kinds of artefacts:

- PFNA inputs and richer NAP layer traffic (CTRL/INGRESS/EGRESS) can be hashed/included in entries (ULED-03, ULED-22).  
- AEON/APXi artefacts from Press/AEON appear as additional hashed records or referenced sets (ULED-22, ULED-31).  

Coverage notes:

- U-ledger is still not driving behaviour; it’s just recording more of the system surface as those features appear.

---

### Phase 4 — SPEC-006 (Multi-Graph & Dynamic Topology V1)

U-ledger becomes **topology- and multi-graph-aware**:

- Multi-graph runs add graph IDs to entries (ULED-21, ULED-40).  
- SLP events (topology changes) are hashed and linked to ledger entries for those ticks (ULED-41–42).  
- Replay uses ledger chain + pillar replay APIs to reconstruct dynamic topology and states (ULED-32, ULED-42).  

Coverage notes:

- P4 turns U-ledger into a complete, replayable history of *what structures existed when* and *how they evolved*.

---

### Phase 5 — SPEC-007 (Governance, Budgets & Codex Actioning)

U-ledger becomes the **ground truth audit trail** for governance:

- Governance decisions, policy changes, and budget changes are recorded as ledger entries or referenced records (ULED-50–52).  
- Codex proposals and their statuses are recorded via hashes/refs (ULED-42, ULED-50).  
- Deterministic governance behaviour is validated by replaying from ledger and comparing outcomes (ULED-53).  

Coverage notes:

- P5 does not change U-ledger fundamentals; it cements U-ledger as the audited backbone of structural & governance history.

---

## 4. Known / Likely Gaps (to Refine)

When we do a line-level pass over ULedgerEntry_v1 contracts and references in pillar specs, we should tighten:

1. **Exact field list for ULedgerEntry_v1**  
   - Ensure ULedgerEntry_v1 has all necessary hash slots, IDs, metadata, and that each field is mapped to a spec/phase/test.

2. **Granularity of entries**  
   - Some scenarios may want per-tick entries; others, per-window or per-decision entries.  
   - We should clarify whether U-ledger supports mixed granularity and how that’s specified in config.

3. **Archival / pruning strategy**  
   - Long-term storage and pruning of old entries may need an additional performance spec or ops playbook.  
   - Coverage here just notes that entries are append-only and replayable.

4. **Tooling for inspection**  
   - We’ll likely want CLI/API tools to inspect U-ledger chains; those should get their own requirements once UI/ops specs exist.

These are not blockers for initial implementation but will matter for operational maturity.

---

## 5. Alignment with “Five Pillars” Model

To keep the mental model clean:

- We still have **five core pillars**: UMX, Loom, Press/APX, Gate/TBP, Codex.  
- **U-ledger is not a sixth pillar**; it’s **supporting infrastructure**.  
- This coverage matrix just makes sure that every place the pillars rely on U-ledger behaviour is actually backed by SPEC-00X work and tests.

You can drop this file under something like:

- `docs/specs/ULedger_Subsystem_Coverage_Matrix_v1.md`

and treat it as a cross-pillar reference, not a new pillar spec.
