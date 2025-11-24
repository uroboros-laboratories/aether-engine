# SPEC-007 — Phase 5 Issue Pack (Governance, Budgets & Codex Actioning V1)

This file is ready to drop into `docs/specs/` in the repo and to use as a copy/paste source for GitHub issues.

---

## Milestone + Labels

**Milestone name:**

> `Phase 5 — SPEC-007 Governance & Codex Actioning V1`

**Suggested labels:**

- `spec:SPEC-007`
- `phase:P5`
- `component:gate`
- `component:codex`
- `component:u-ledger`
- `component:press`
- `component:loom`
- `component:umx`
- `component:governance`
- `type:feature`
- `type:tests`
- `priority:medium`
- `priority:high`

You don’t have to use all labels on each issue; suggestions are given per-issue.

---

## Issue P5.1 — GovernanceConfig_v1 & Policy Contracts

**Title:**  
`[SPEC-007][P5] GovernanceConfig_v1 & policy contracts`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:governance`, `component:gate`, `component:u-ledger`, `type:feature`, `priority:high`

```markdown
## Summary

Define governance and policy contracts for the Aether engine, including:

- GovernanceConfig_v1,
- Policy types (budget, safety, structural constraints),
- How these are attached to sessions and runs.

## Spec References

- Aether full system master spec (governance sections)
- Trinity Gate/TBP pillar spec (governance / TBP sections)
- Codex Eterna master spec (proposal evaluation / governance)
- U-ledger subsystem coverage matrix
- `docs/specs/spec_007_Phase_5_Governance_Codex_Actioning_Plan.md` (this spec, when added)

## Goals

- Provide a clear structure for expressing governance policies and budgets.
- Make governance part of session configuration and ledger/audit trail.

## Tasks

- [ ] Define `GovernanceConfig_v1`:
  - [ ] Per-run budgets (e.g. topological changes, resource use proxies).
  - [ ] Policy references / IDs.
  - [ ] Flags for Codex actioning modes (off, suggest-only, governed-apply).
- [ ] Define policy contract types, e.g.:
  - [ ] `TopologyPolicy_v1` (max nodes/edges, allowed operations).
  - [ ] `BudgetPolicy_v1` (caps on changes, proposals applied per window/tick).
  - [ ] `SafetyPolicy_v1` (invariants that must never be broken).
- [ ] Decide how policies are bound to:
  - [ ] Session config.
  - [ ] U-ledger entries (hash/link to policy set for audit).
- [ ] Add tests:
  - [ ] Construct sample GovernanceConfig_v1 with multiple policies.
  - [ ] Round-trip serialisation with stable hashes/IDs.

## Acceptance Criteria

- [ ] GovernanceConfig_v1 and core policy contracts are defined and test-covered.
- [ ] Policy sets can be unambiguously linked to a given run/session.
```

---

## Issue P5.2 — CodexProposal_v1 Evaluation Against Policies

**Title:**  
`[SPEC-007][P5] Evaluate CodexProposal_v1 against governance policies`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:codex`, `component:governance`, `component:slp`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement evaluation of `CodexProposal_v1` objects against governance policies:

- Check proposals for policy compliance,
- Annotate proposals with evaluation results,
- Prepare them for possible application.

Codex remains the source of proposals; governance decides what’s admissible.

## Spec References

- Codex Eterna master spec (proposals and evaluation)
- Governance policy contracts from P5.1
- `docs/contracts/CodexContracts_v1.md`
- `docs/contracts/SLPEvent_v1.md` (for topology-affecting proposals)

## Goals

- Provide a deterministic policy evaluation path for Codex proposals.
- Separate proposal generation from policy judgement.

## Tasks

- [ ] Implement mapping from `CodexProposal_v1` types to the policies they must satisfy.
- [ ] Implement evaluation engine:
  - [ ] Takes a proposal + current GovernanceConfig_v1 + run context.
  - [ ] Checks against all relevant policies (topology, budgets, safety).
  - [ ] Produces an evaluation record (OK, SOFT_FAIL, HARD_FAIL, reasons).
- [ ] Extend proposal records with evaluation fields:
  - [ ] `governance_status`, `violated_policies`, `scores`.
- [ ] Add tests:
  - [ ] Proposals that clearly comply / clearly violate policies.
  - [ ] Edge cases where multiple policies interact.
  - [ ] Determinism: same proposal + policy set → same evaluation.

## Acceptance Criteria

- [ ] All proposals can be evaluated against applicable policies.
- [ ] Evaluation outcomes are deterministic and traceable.
```

---

## Issue P5.3 — TBP Decision Loop & Action Queue (Governed)

**Title:**  
`[SPEC-007][P5] TBP decision loop & governed action queue`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:gate`, `component:governance`, `component:codex`, `component:slp`, `type:feature`, `type:tests`, `priority:high`

```markdown
## Summary

Implement a **governed decision loop** in TBP that:

- Collects candidate Codex proposals,
- Evaluates them against governance,
- Queues approved actions,
- Applies them at controlled boundaries (e.g. between ticks/windows).

## Spec References

- Trinity Gate/TBP pillar spec (TBP decision loop)
- Codex Eterna master spec (proposal lifecycle)
- Governance policy contracts
- `docs/contracts/SLPEvent_v1.md`
- `docs/specs/spec_006_Phase_4_MultiGraph_SLP_Plan.md` (SLP application)

## Goals

- Move from “observer-only Codex” to “governed Codex actioning”.
- Ensure all applied actions are policy-compliant and auditable.

## Tasks

- [ ] Extend TBP logic with a decision loop that:
  - [ ] Periodically fetches proposals from CodexContext (e.g. per window).
  - [ ] Evaluates them via the governance evaluation engine (P5.2).
  - [ ] Builds an action queue of approved proposals.
- [ ] Map approved proposals to concrete actions, e.g.:
  - [ ] SLPEvent_v1 batches (topology modification).
  - [ ] Config tweaks (within safe bounds).
- [ ] Define application boundaries:
  - [ ] E.g. SLP actions only applied between ticks, window-level actions at window boundaries.
- [ ] Add tests:
  - [ ] Scenario where multiple proposals compete for limited budget, ensuring governance caps are enforced.
  - [ ] Scenario with zero approved proposals (engine runs unchanged).

## Acceptance Criteria

- [ ] TBP decision loop exists and is governed by policy and budgets.
- [ ] Only approved proposals are turned into actions and applied.
```

---

## Issue P5.4 — Budget Tracking & Exhaustion Behaviour

**Title:**  
`[SPEC-007][P5] Budget tracking & exhaustion behaviour`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:governance`, `component:u-ledger`, `component:gate`, `component:codex`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Implement **budget tracking** for governance, including:

- Counting applied actions against budgets,
- Handling budget exhaustion,
- Recording budget usage in U-ledger for audit.

## Spec References

- Governance policy contracts (BudgetPolicy_v1)
- U-ledger subsystem coverage matrix
- `docs/contracts/ULedgerEntry_v1.md`
- `docs/specs/spec_007_Phase_5_Governance_Codex_Actioning_Plan.md`

## Goals

- Ensure there is a hard cap on certain types of changes (e.g. SLP operations) per run/window/etc.
- Make budget usage transparent and replayable.

## Tasks

- [ ] Implement budget counters in the governance subsystem:
  - [ ] Per policy (e.g. SLP ops per run, per window).
  - [ ] Per proposal type if needed.
- [ ] Define exhaustion behaviours:
  - [ ] Hard stop, or
  - [ ] “No more changes” but engine continues to run, or
  - [ ] Configurable choice.
- [ ] Integrate with U-ledger:
  - [ ] Record budget usage and exhaustion events in ledger entries.
- [ ] Add tests:
  - [ ] Scenario where budget is partially used and then exhausted.
  - [ ] Verify behaviour when budget is exceeded matches config.

## Acceptance Criteria

- [ ] Budget use is tracked deterministically and visible in logs/ledger.
- [ ] Engine behaviour at/after budget exhaustion is clearly defined and test-covered.
```

---

## Issue P5.5 — Governance-Aware NAP IO (CTRL & GOV Layers)

**Title:**  
`[SPEC-007][P5] Governance-aware NAP IO (CTRL & GOV layers)`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:nap`, `component:gate`, `component:governance`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Extend NAP IO so that governance events are clearly visible via NAP layers/modes, including:

- Governance CTRL signals,
- Optional GOV-specific layer/mode for audits.

## Spec References

- Trinity Gate/TBP pillar spec (NAP layers & governance)
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/specs/spec_003_Phase_3_Gate_TBP_PFNA_IO_Plan.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`

## Goals

- Make governance status and events visible in the same NAP stream as other engine activity.
- Preserve determinism and maintain separation between data and governance signalling.

## Tasks

- [ ] Decide whether to introduce a dedicated GOV layer or reuse CTRL with GOV modes.
- [ ] Emit envelopes for key governance events, e.g.:
  - [ ] Policy set loaded.
  - [ ] Budget exhaustion.
  - [ ] Proposal approved/rejected (summary).
- [ ] Include necessary references (policy IDs, proposal IDs, ledger hashes).
- [ ] Add tests:
  - [ ] Scenario where governance events occur; verify corresponding CTRL/GOV envelopes.
  - [ ] Scenario with governance disabled; verify no governance NAP events.

## Acceptance Criteria

- [ ] Governance events are encoded in NAP envelopes in a stable, documented way.
- [ ] Governance signalling can be filtered/consumed independently of data/ingress/egress.
```

---

## Issue P5.6 — Governance & Codex Integration Demo Scenario

**Title:**  
`[SPEC-007][P5] Governance & Codex actioning demo scenario`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:governance`, `component:codex`, `component:gate`, `component:slp`, `component:u-ledger`, `type:tests`, `priority:high`

```markdown
## Summary

Create a **governance + Codex actioning demo scenario** that exercises:

- Codex motif learning and proposal emission,
- Governance evaluation and budgets,
- TBP decision loop,
- Applied SLP actions under policy control,
- Full ledger + NAP signalling.

## Spec References

- All governance-related specs (P5.1–P5.5)
- Codex Eterna master spec
- Trinity Gate/TBP pillar spec
- U-ledger subsystem coverage matrix

## Goals

- Provide a small but complete example of a governed Codex-driven structural adaptation.
- Lock in outputs via snapshots for regression.

## Tasks

- [ ] Design scenario:
  - [ ] Small 1–2 graph setup where Codex can learn simple motifs.
  - [ ] Governance policies that allow a limited number of SLP changes.
- [ ] Implement test harness:
  - [ ] Run scenario long enough for Codex to propose at least one actionable change.
  - [ ] Allow TBP to evaluate and apply proposals under budget.
  - [ ] Collect U-ledger, NAP, AEON/APXi, Codex library/proposals.
- [ ] Snapshot outputs under:
  - [ ] `tests/fixtures/snapshots/governance_codex_demo/`.
- [ ] Add regression tests:
  - [ ] Re-running scenario produces identical governance decisions and applied actions.

## Acceptance Criteria

- [ ] Governance + Codex demo scenario is deterministic and documented.
- [ ] Snapshot tests guard against accidental changes to governance or actioning behaviour.
```

---

## Issue P5.7 — Governance Introspection & Dry-Run Mode

**Title:**  
`[SPEC-007][P5] Governance introspection & dry-run mode`

**Labels:**  
`spec:SPEC-007`, `phase:P5`, `component:governance`, `component:gate`, `component:codex`, `type:feature`, `type:tests`, `priority:medium`

```markdown
## Summary

Add governance introspection tools and a **dry-run mode** where:

- Governance evaluates proposals,
- Budgets and policies are exercised,
- But no actions are actually applied (engine stays structurally fixed).

## Spec References

- Governance policy contracts
- Trinity Gate/TBP pillar spec
- Codex Eterna master spec

## Goals

- Let operators see **what would have happened** under a given policy set without changing the engine.
- Provide a safe way to test governance configurations.

## Tasks

- [ ] Implement a `governance_mode` config flag:
  - [ ] `off`, `observe`, `dry_run`, `enforce` (or similar).
- [ ] In `dry_run` mode:
  - [ ] Evaluate proposals and track budget usage as normal.
  - [ ] Log which actions *would* have been applied, but do not apply them.
  - [ ] Emit appropriate governance NAP/ledger entries.
- [ ] Introspection:
  - [ ] Provide a summarised view of evaluated proposals, policy hits, and hypothetical actions.
- [ ] Add tests:
  - [ ] Scenario where `dry_run` vs `enforce` produce same governance evaluations but differ in applied actions.
  - [ ] Snapshot or strong assertions for the dry-run summaries.

## Acceptance Criteria

- [ ] Governance supports a dry-run mode suitable for policy testing.
- [ ] Introspection outputs are deterministic and useful for operators.
```

---

## Notes

- SPEC-007 is the final “activation” layer:
  - All structural changes are still deterministic, integer-only, and governed.
  - Codex only acts when governance explicitly allows it.
- This phase assumes SPEC-002, SPEC-005, SPEC-003, SPEC-004 and SPEC-006 are already implemented and passing their regression suites.
