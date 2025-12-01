# Master Spec Lineal Implementation Plan (Novice Track)

This plan orders the remaining work from the current CMP-0 scaffolding to full master-spec coverage. Each step builds on the last and keeps scope narrow so progress is easy to track.

## Prerequisites
- Confirm current CMP-0 code compiles and existing tests pass.
- Keep the Phase 1–5 assets and notes (e.g., `docs/specs/phase_gap_validation.md`) handy for reference.

## Lineal steps
1. **Stabilize UMX core invariants**
   - Add causal radius, capacity, and epsilon/policy fields to UMX profiles.
   - Enforce deterministic edge ordering and conservation/bounds in `umx.engine.step`.
   - Emit enriched `UMXTickLedgerV1` with NAP envelope refs and invariant checks.
   - Add golden tick fixtures and validation tests for small topologies.

2. **Add UMX diagnostics and policy hooks**
   - Implement per-tick validation helpers (conservation, causal bounds) and wire into `step`.
   - Introduce policy-driven epsilon handling and kill-switch semantics.
   - Extend tests to cover policy violations and recovery paths.

3. **Implement Loom integrity chain**
   - Canonicalize tick data and compute hash-chain/Merkle roots for P-/I-blocks.
   - Persist serialized blocks with an index for replay and rollback windows.
   - Add schedule enforcement (I-block every W ticks) and chain state export.
   - Create replay/rehydration tests that verify chain and Merkle roots.

4. **Persist Loom blocks and Press-ready schemas**
   - Define binary P-/I-block schemas compatible with Press ingestion.
   - Store compressed/canonicalized blocks on disk and expose pointers for Press manifests.
   - Validate deterministic encoding with round-trip tests.

5. **Build Press SimA encoders/decoders**
   - Implement ID/ΔR/GR codecs with MDL scoring to choose schemes per payload.
   - Generate manifests with checksums and deterministic ordering.
   - Add round-trip tests for integer tables, vectors, and mixed payloads.

6. **Add Press residual (SimB) and APX capsules**
   - Handle residual streams, headers, and APX bundle creation.
   - Validate manifest checksum/hash chains on decode.
   - Expand tests to cover mixed SimA/SimB payloads and APX bundle integrity.

7. **Implement Gate PFNA ingress + integerization**
   - Add PFNA math (scale/origin/clamp) with audit trails and idempotent ordering queue.
   - Define scene frame validation and link payload refs to Press manifests.
   - Generate NAP envelopes with canonical ordering and prev_chain linkage.
   - Test integerization, envelope chaining, and idempotence.

8. **Governed Gate/TBP workflow**
   - Attach governance/policy hooks to envelope generation and ingress/egress.
   - Enforce approval paths and rejection logging in TBP decision loops.
   - Add tests that exercise governed acceptance and rejection flows.

9. **Codex proposal gate and structural ledger**
   - Introduce proposal objects with predicted ΔL/fidelity metadata and MDL evaluator.
   - Enforce acceptance gates and record PROPOSE → REVIEW → COMMIT transitions in a hash-chained ledger.
   - Write tests simulating accepted/rejected proposals with ledger verification.

10. **Unify cross-pillar U-Ledger**
    - Define canonical ledger entries referencing NAP envelopes, Loom chain state, Press manifests, and UMX tick ledgers.
    - Add policy validation for ordering/completeness/versioning and emit checkpoints.
    - Integrate ledger updates into Gate ingress, UMX ticks, Loom block flush, and Press capsule finalization.
    - Build end-to-end audit tests that walk the ledger across pillars.

11. **Full-system demo and regression harness**
    - Create a minimal scenario wiring Gate → Press → Loom → UMX → Codex with U-Ledger checkpoints.
    - Capture fixtures/snapshots and add integration tests that replay from stored blocks/APX bundles.
    - Document runbooks for setup, execution, and verification.

## Usage tips
- Work one step at a time; keep each PR small and aligned with the numbered steps.
- After each step, add or update regression tests before moving on.
- Keep ledger/checksum outputs stable by fixing canonical ordering and encoding choices early.
