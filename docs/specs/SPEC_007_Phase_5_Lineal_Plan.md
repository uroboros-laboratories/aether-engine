# SPEC-007 Phase 5 Lineal Implementation Plan

## What we reviewed
- Read the Phase 5 issue pack at `docs/specs/SPEC_007_Phase_5_Issue_Pack_v1.md` to extract tasks and components.

## Planned lineal order
1. **P5.1 GovernanceConfig_v1 & policy contracts** — define governance config and policy shapes before any evaluation.
2. **P5.2 CodexProposal_v1 evaluation** — wire proposals to policies and annotate evaluations.
3. **P5.3 TBP decision loop & governed action queue** — drive proposal intake and turn approved ones into actions.
4. **P5.4 Budget tracking & exhaustion behaviour** — enforce limits and ledger logging for applied actions.
5. **P5.5 Governance-aware NAP IO (CTRL/GOV layers)** — surface governance events through NAP envelopes.
6. **P5.6 Governance & Codex integration demo scenario** — end-to-end demo with snapshots.
7. **P5.7 Governance introspection & dry-run mode** — add safe inspection path without applying actions.

## Status snapshot (plain words)
- Work done: completed P5.1 (governance config + policy contracts), P5.2 (Codex proposal governance evaluation/annotation), P5.3 (governed TBP decision loop that evaluates proposals, applies budget caps, and records accepted Codex actions on runs), P5.4 (budget tracking and exhaustion behaviour with ledger annotations), P5.5 (governance-aware NAP IO via GOV/G layer signalling), P5.6 (governed Codex actioning demo scenario with snapshots), and P5.7 (governance introspection + dry-run mode for hypothetical actioning).
- Where: governance contracts live in `docs/contracts/GovernanceConfig_v1.md` with code in `src/governance/` (config + evaluation + decision loop + budget tracking), session wiring in `src/config/schemas.py` and `src/gate/gate.py`, ledger binding in `src/core/tick_loop.py` / `src/uledger/entry.py`, Codex proposal governance coverage in `tests/unit/test_governance_evaluation.py`, governance budget checks in `tests/unit/test_governed_action_queue_integration.py`, governance NAP signalling in `src/core/tick_loop.py` plus `tests/unit/test_governance_nap_io.py`, and the Codex governance demo snapshots in `docs/fixtures/configs/gov_codex_demo_run_config.json` with regression coverage under `tests/integration/test_governance_codex_demo.py`.
- Phase completion: **100%** (7 of 7 Phase 5 issues completed).
