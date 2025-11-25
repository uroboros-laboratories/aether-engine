# Contracts (`docs/contracts/`)

This folder defines the **small, cross‑pillar contracts** that glue the Aether engine together.

Each file here should be treated as a mini‑spec for one record type (or a small family of types):

- It defines fields, meanings, and invariants.
- It is **not optional**: UMX / Loom / Press / Gate / Codex / U‑ledger implementations must
  reflect these contracts exactly.

---

## Core contracts

- `TopologyProfile_v1.md`
  - How graphs/topologies are described: nodes, edges, parameters.
- `Profile_CMP0_v1.md`
  - Numeric profile for CMP‑0: modulus, scaling constant, I‑block spacing, and rule hooks.
- `RunConfig_v1.md`
  - File-driven run configuration tying together topology, profile, windows, and runtime flags.
- `ScenarioRegistry_v1.md`
  - Catalogue of named scenarios pointing to runnable `RunConfig_v1` documents.
- `StructuredLogging_v1.md`
  - Structured lifecycle logging entries and configuration for Phase 3 runs.
- `Metrics_v1.md`
  - Run-level metrics snapshot structure for Phase 3 governance.
- `Introspection_v1.md`
  - Read-only APIs for querying UMX/Loom/APX/NAP/U-ledger artefacts from run results.
- `UMXTickLedger_v1.md`
  - Per‑tick record of UMX flux application over a topology.
- `LoomBlocks_v1.md`
  - Structures for P‑blocks and I‑blocks (Aevum Loom chain).
- `APXManifest_v1.md`
  - APX manifest structure: streams, schemes, MDL lengths, `manifest_check`.
- `PressWindowContext_v1.md`
  - Window‑level Press/APX context (streams, schemes, lifecycle).
- `AEONWindowGrammar_v1.md`
  - AEON window definitions (base + derived) and hierarchy, aligned to Loom ticks and Press windows.
- `APXiDescriptor_v1.md`
  - Descriptor language for APXi primitives over AEON windows and Press streams.
- `NAPEnvelope_v1.md`
  - NAP envelopes emitted by Gate/TBP for each tick / scene.
- `SceneFrame_v1.md`
  - Canonical per‑tick integration object used by Gate/TBP.
- `TickLoop_v1.md`
  - Tick orchestration contract: how UMX, Loom, Press, Gate, Codex, and U‑ledger connect.
- `ULedgerEntry_v1.md`
  - Universal ledger entry structure, including hash references into pillar outputs.
- `CodexContracts_v1.md`
  - Contracts for Codex motifs, library entries, and proposals.

Helper docs:

- `Aether_Contracts_Explainer_v1.md`
  - How to read these contracts and how they relate to the pillars and specs.
- `Aether_Existing_Contracts_Index_v1.md`
  - Index of all contracts, with pointers to the specs and pillars that rely on them.
- `GF01_V0_Exam.md`
  - The official definition of what it means to pass the GF‑01 exam.

---

## How to use this folder

- When you implement a feature in `src/`, start from the relevant contract(s) here.
- If you find you need a new field or change an invariant:
  - Update the contract file first.
  - Then update the pillar spec / phase spec.
  - Then change the implementation and tests.

There should be **no hidden types** that aren’t reflected here. If it’s important enough to cross
a pillar boundary, it should have a contract.
