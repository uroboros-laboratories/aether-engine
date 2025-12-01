# Phase 6 Build Journal: Executing the Master Spec Lineal Plan (Novice Track)

This journal records how we execute the numbered steps in `docs/specs/master_spec_lineal_plan.md` so a newcomer can follow the process end to end. Each entry captures **what we did**, **why**, **how**, and **where** the changes landed, with checkpoints for verification.

## How to use this journal
- Work through the entries sequentially; each one maps to a step in the lineal plan.
- Before starting an entry, skim its prerequisites and gather the files/fixtures it mentions.
- After finishing an entry, note test results and any deviations so future readers can replay the work.

### Entry format
For each step, we log:
- **Goal** — the outcome we want from the step.
- **Context** — why this step matters relative to the master specs.
- **Files/areas** — primary paths we expect to touch.
- **Actions** — ordered checklist to perform.
- **Verification** — commands or observations to confirm success.
- **Notes** — discoveries, blockers, or follow-ups.

## Entry 0 — Baseline and scaffolding check
- **Goal**: Confirm the CMP-0 scaffold still runs and tests (if present) pass before adding new features.
- **Context**: Establishes a clean starting point so regressions can be attributed to Phase 6 work.
- **Files/areas**: Repository root; any existing tests; `docs/specs/phase_gap_validation.md` for gap reminders.
- **Actions**:
  1. Pull latest main branch and ensure the working tree is clean.
  2. Run `python -m pip install -r requirements.txt` (or the project’s env setup) if not already set up.
  3. Execute `pytest` (or the project’s test runner) and record the outcome.
  4. If tests are missing, note that as a gap; the first new tests will appear in Entry 1.
- **Verification**: All tests pass (or document failures with logs). No uncommitted changes remain after the baseline check.
- **Notes**: Keep `docs/specs/phase_gap_validation.md` handy to track which gaps we expect to close.

## Entry 1 — Stabilize UMX core invariants (Lineal Plan Step 1)
- **Goal**: Add causal radius, capacity, epsilon/policy fields to UMX profiles; enforce deterministic edge ordering and conservation/bounds in `umx.engine.step`; emit enriched `UMXTickLedgerV1`; add golden tick fixtures/tests.
- **Context**: This establishes deterministic tick behavior and ledger completeness required by the master UMX spec.
- **Files/areas**: `src/umx/topology_profile.py`, `src/umx/profile_cmp0.py`, `src/umx/engine.py`, `src/umx/diagnostics.py` (new/extended), `tests/umx/` (new fixtures).
- **Actions**:
  1. Extend profile dataclasses with causal radius/capacity/epsilon/policy fields and defaults.
  2. Update `umx.engine.step` to enforce ordering, causal bounds, and invariant checks; include NAP refs and invariants in `UMXTickLedgerV1`.
  3. Add diagnostics helpers (conservation, bounds) and call them inside `step`.
  4. Create small topology fixtures and expected ledgers under `tests/umx/`.
  5. Run targeted tests (`pytest tests/umx -k ledger`) and record results.
- **Verification**: New tests pass and `step` returns enriched ledgers with deterministic ordering.
- **Notes**: Document any policy defaults chosen for epsilon handling.

## Entry 2 — UMX diagnostics and policy hooks (Lineal Plan Step 2)
- **Goal**: Implement per-tick validation helpers (conservation, causal bounds), epsilon policy handling, and kill-switch semantics; expand tests for violations/recovery.
- **Context**: Ensures runtime detects policy breaches early and supports safe recovery paths.
- **Files/areas**: `src/umx/diagnostics.py`, `src/umx/engine.py`, `src/umx/policy.py` (new), `tests/umx/`.
- **Actions**:
  1. Add policy structures for epsilon caps/kill-switches and wire them into `step`.
  2. Extend diagnostics to surface structured errors/warnings.
  3. Add tests that trigger policy violations and verify kill-switch or recovery behavior.
  4. Run `pytest tests/umx` and capture results/logs.
- **Verification**: Policy violation scenarios are caught deterministically; recovery/kill-switch paths behave as expected.
- **Notes**: Keep policy defaults minimal; document any temporary scaffolding.

## Entry 3 — Loom integrity chain (Lineal Plan Step 3)
- **Goal**: Canonicalize tick data, compute hash-chain/Merkle roots for P-/I-blocks, and persist serialized blocks with replay/rollback support.
- **Context**: Delivers authenticated replay foundation for Loom per master spec requirements.
- **Files/areas**: `src/loom/` (new `chain.py` or similar), block serialization modules, replay index, `tests/loom/`.
- **Actions**:
  1. Define canonicalization and hashing for P-/I-blocks; include Merkle construction for I-blocks.
  2. Persist blocks and maintain a replay index with rollback window enforcement.
  3. Expose chain state export (roots, heights) for NAP envelopes.
  4. Add replay/rehydration tests verifying hash/merkle roots and rollback limits.
  5. Run `pytest tests/loom`.
- **Verification**: Stored blocks rehydrate faithfully; chain/merkle roots match expected vectors.
- **Notes**: Choose stable hash and serialization formats early to avoid churn.

**Progress note (completed)**
- Implemented deterministic canonicalization + SHA-256 hashing for P-/I-blocks.
- Added Loom chain recorder that emits per-P-block hashes, per-I-block Merkle roots (windowed), and exports chain tip state.
- Persisted blocks with a JSON index and rollback pruning for replay windows.
- Verified via unit tests that merkle roots and persistence behave deterministically.

## Entry 4 — Persist Loom blocks with Press-ready schemas (Lineal Plan Step 4)
- **Goal**: Define binary P-/I-block schemas compatible with Press ingestion; store compressed/canonicalized blocks; validate deterministic encoding with round-trip tests.
- **Context**: Bridges Loom output into Press so chain data can be compressed and transported.
- **Files/areas**: `src/loom/` schema definitions, Press integration points, `tests/loom/` round-trips.
- **Actions**:
  1. Specify binary schemas (field order, endianness) and implement serializers/deserializers.
  2. Integrate compression hooks aligned with Press expectations; store block pointers.
  3. Add round-trip tests covering P-/I-block encode/decode.
  4. Run `pytest tests/loom -k schema`.
- **Verification**: Encoded blocks decode identically and satisfy deterministic hashing.
- **Notes**: Document schema versions for future migrations.

## Entry 5 — Press SimA encoders/decoders (Lineal Plan Step 5)
- **Goal**: Implement ID/ΔR/GR codecs with MDL scoring to pick schemes; generate manifests with checksums and deterministic ordering; add round-trip tests.
- **Context**: Establishes the primary compression path aligned with master Press spec.
- **Files/areas**: `src/press/` codecs/manifests, MDL scoring, `tests/press/` fixtures.
- **Actions**:
  1. Implement bit-precise SimA encoders/decoders for ID/ΔR/GR.
  2. Add MDL scoring to select schemes per payload.
  3. Emit manifests with checksums/hash chains and deterministic ordering.
  4. Add round-trip tests for tables/vectors/mixed payloads.
  5. Run `pytest tests/press -k sima`.
- **Verification**: Round-trips succeed with expected bit lengths and manifest hashes.
- **Notes**: Keep manifest field order stable to avoid rehashing downstream.

**Progress note (completed)**
- Added SimA ID/R/GR encoders with zigzag-varint packing, MDL scoring, and deterministic tie-breaking across streams.
- Added payload-aware manifest generation (`encode_window`) that emits per-stream checksums alongside manifests, keeping APXi hooks intact.
- Implemented decoders to round-trip SimA payloads and added regression tests for GF-01 windows plus simple GR payloads.
- Verified via targeted tests: `pytest tests/unit/test_press.py -q` and `pytest tests/unit/test_apxi_mdl.py -q`.

## Entry 6 — Press residual (SimB) and APX capsules (Lineal Plan Step 6)
- **Goal**: Handle residual streams, headers, and APX bundle creation; validate manifests on decode; expand tests for mixed SimA/SimB payloads and bundle integrity.
- **Context**: Completes Press coverage for residual data and packaging.
- **Files/areas**: `src/press/` residual codecs, APX container builder, `tests/press/` bundles.
- **Actions**:
  1. Implement SimB residual handling and headers.
  2. Build APX bundle writer/reader with manifest hash checks.
  3. Add mixed payload tests and bundle integrity checks.
  4. Run `pytest tests/press -k apx`.
- **Verification**: Bundles validate, and mixed payloads round-trip with correct hashes.
- **Notes**: Record any interim shortcuts for future hardening.

**Progress note (completed)**
- Added SimB residual encoder/decoder for integer tables with checksums and bit-length accounting.
- Implemented APX capsule writer/reader that staples manifests, SimA payloads, and SimB residual tables with checksum and manifest-check validation.
- Added round-trip tests covering SimB residual tables, mixed SimA/SimB capsules, and manifest tamper detection.

## Entry 7 — Gate PFNA ingress + integerization (Lineal Plan Step 7)
- **Goal**: Add PFNA math with audit trails and idempotent ordering queue; validate scene frames and link payload refs to Press manifests; generate NAP envelopes.
- **Context**: Provides governed, reproducible ingress into the pipeline.
- **Files/areas**: `src/gate/` PFNA math, scene validation, NAP envelope builder, `tests/gate/`.
- **Actions**:
  1. Implement PFNA scale/origin/clamp functions with audit logs.
  2. Add deterministic ingress queue and scene frame validation.
  3. Generate NAP envelopes with canonical ordering and prev_chain linkage.
  4. Add tests for integerization, envelope chaining, idempotence.
  5. Run `pytest tests/gate`.
- **Verification**: Envelopes chain correctly and integerization logs are reproducible.
- **Notes**: Capture sample PFNA configs for reuse.

**Progress note (completed)**
- Added PFNA integerization transform with scale/origin/clamp plus per-value audit logs and idempotent ingress queue.
- Recorded PFNA audits on scenes/meta, attached ingress envelopes that hash integerized payloads, and added scene validation helpers.
- Added regression tests for integerization math, queue ordering/deduplication, and tick-loop integration metadata.

## Entry 8 — Governed Gate/TBP workflow (Lineal Plan Step 8)
- **Goal**: Attach governance/policy hooks to envelope generation; enforce approval/rejection logging; test governed flows.
- **Context**: Aligns ingress/egress with governance requirements in the master spec.
- **Files/areas**: `src/gate/` governance hooks, TBP decision logic, `tests/gate/` policy cases.
- **Actions**:
  1. Add policy evaluation steps to envelope generation and queue handling.
  2. Record decisions with structured logs/ledger entries.
  3. Add tests for acceptance/rejection paths.
  4. Run `pytest tests/gate -k governance`.
- **Verification**: Governance outcomes are deterministic and logged.
- **Notes**: Keep policy configs minimal and documented.

**Progress note (completed)**
- Added governance-aware envelope filter with allowed layer lists and per-tick caps, emitting GOV decision envelopes for each data envelope.
- Logged gate governance decisions via structured logger hooks and preserved observed vs enforced outcomes deterministically.
- Added unit coverage for enforced caps and observed rejections; verified with `PYTHONPATH=src pytest tests/unit/test_gate_governance.py -q`.

## Entry 9 — Codex proposal gate and structural ledger (Lineal Plan Step 9)
- **Goal**: Introduce proposals with ΔL/fidelity metadata and MDL evaluator; enforce acceptance gates; record hash-chained ledger transitions; add tests.
- **Context**: Enables master-spec governance and motif tracking in Codex.
- **Files/areas**: `src/codex/` proposals/ledger, MDL evaluator, `tests/codex/`.
- **Actions**:
  1. Define proposal types and MDL evaluation criteria.
  2. Implement structural ledger with PROPOSE → REVIEW → COMMIT transitions.
  3. Add tests for accepted/rejected proposals with ledger verification.
  4. Run `pytest tests/codex`.
- **Verification**: Ledger hashes remain consistent; proposals gate correctly.
- **Notes**: Capture example proposals for regression fixtures.

**Progress note (completed)**
- Added Codex proposal gate policy defaults with delta-L and fidelity thresholds.
- Emitted structural ledger entries for PROPOSE → REVIEW → COMMIT with hash chaining per proposal.
- Implemented deterministic evaluation that updates proposal governance status and records ledger transitions.
- Added unit coverage for proposal emission, acceptance/commit, and rejection paths.

## Entry 10 — Cross-pillar U-Ledger (Lineal Plan Step 10)
- **Goal**: Define canonical ledger entries referencing NAP envelopes, Loom chain state, Press manifests, and UMX tick ledgers; add policy validation and checkpoints; integrate updates into each pillar.
- **Context**: Ties outputs together for end-to-end auditability.
- **Files/areas**: `src/uledger/` schemas/validators, pillar integration points, `tests/uledger/` end-to-end audit.
- **Actions**:
  1. Define ledger schema and policy checks for ordering/completeness/versioning.
  2. Hook ledger updates into Gate ingress, UMX ticks, Loom block flush, and Press finalization.
  3. Build audit tests that traverse the ledger across pillars.
  4. Run `pytest tests/uledger`.
- **Verification**: Ledger walk succeeds with consistent hashes and references.
- **Notes**: Document checkpoint formats for exports.

**Progress note (completed)**
- Added validation and checkpoint helpers that verify ULedgerEntry chain continuity, manifest hash alignment, and policy hash consistency.
- Integrated ULedger construction/validation into the CMP-0 tick loop so each run emits entries plus a checkpoint summary for audits.
- Added regression tests covering prev-hash alignment, manifest mismatches, and contiguous tick enforcement.


## Entry 11 — Full-system demo and regression harness (Lineal Plan Step 11)
- **Goal**: Wire Gate → Press → Loom → UMX → Codex with U-Ledger checkpoints; capture fixtures/snapshots and add integration tests; document runbooks.
- **Context**: Demonstrates full master-spec coverage and provides regression safety net.
- **Files/areas**: Integration harness under `tests/` or `examples/`, runbooks in `docs/`.
- **Actions**:
  1. Build a minimal scenario with synthetic inputs flowing through all pillars.
  2. Persist fixtures (blocks, APX bundles, ledgers) and add integration tests that replay them.
  3. Write runbook documenting setup, execution, and verification commands.
  4. Run full test suite (`pytest`) and capture outputs.
- **Verification**: End-to-end replay matches stored fixtures; checkpoints align across pillars.
- **Notes**: Note any gaps or future hardening tasks discovered during the demo.

**Progress note (completed)**
- Captured the GF-01 end-to-end run with persisted Loom P-/I-block binaries via `LoomBlockStore` and kept the serialized snapshot aligned with integration expectations.
- Added an integration regression that replays stored blocks, validates Press-ready pointers, and checks the full serialized run against the canonical snapshot.

## Recording progress
- After completing each entry, append a dated note under its **Notes** with what changed, commands run, and outcomes.
- If an entry is skipped or reordered, record the rationale so others can follow the divergence.
- Keep the journal in version control so it evolves with the codebase.

## Progress update — Phase 6 (Lineal Plan)
- **Steps complete**: 11 / 11 (100%).
- **Covered**: Entry 1 (UMX core invariants: causal radius + epsilon caps), Entry 2 (diagnostics/policy enforcement with kill-switch support), Entry 3 (Loom integrity chain: hashing, Merkle roots, persistence + rollback window), Entry 4 (binary Loom block schemas + compressed storage + Press pointers with deterministic round-trips), Entry 5 (Press SimA encoders/decoders, MDL scoring, manifests + payload checksums, decode round-trips), Entry 6 (Press SimB residual tables and APX capsule stapling with manifest validation), Entry 7 (Gate PFNA ingress with integerization audit trail, idempotent queue, and scene/meta validation), Entry 8 (Governed Gate/TBP workflow with policy-aware envelope filtering and GOV decision events), Entry 9 (Codex proposal gate + structural ledger with hash chaining and governance evaluation), Entry 10 (Cross-pillar U-Ledger integration + checkpoints), Entry 11 (Full-system demo harness with persisted Loom blocks and serialized snapshot replay).
- **Next up**: Lineal plan complete; follow-ups can focus on hardening, additional fixtures, or performance tuning.
