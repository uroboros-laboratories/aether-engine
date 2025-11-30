# GovernanceConfig_v1 — Governance & Policy Contracts

## Purpose

`GovernanceConfig_v1` captures the **policy set** that governs a Codex-enabled
run. It defines budgets, safety constraints, and topology rules, and exposes a
stable hash that can be referenced by sessions and U-ledger entries for audit
trails.

This contract is the anchor for SPEC-007 Phase 5 (Governance & Codex
Actioning).

---

## Record Shapes

### GovernanceConfig_v1

Top-level governance record bound to one run/session.

- **governance_mode: enum { "OFF", "OBSERVE", "DRY_RUN", "ENFORCE" }**
  - High-level governance stance for the run.
    - `OFF` → Codex disabled.
    - `OBSERVE` (alias: `SUGGEST_ONLY`) → proposals evaluated/logged but never applied.
    - `DRY_RUN` → proposals evaluated, budgets exercised, hypothetical actions logged, but no structural mutations applied.
    - `ENFORCE` (alias: `GOVERNED_APPLY`) → proposals may be applied after policy checks.
- **codex_action_mode: enum { "OFF", "OBSERVE", "DRY_RUN", "GOVERNED_APPLY" }**
  - Normalised action mode, derived from `governance_mode` and kept for backwards compatibility with earlier Phase 5 steps.
- **topology_policies: TopologyPolicy_v1[]**
- **budget_policies: BudgetPolicy_v1[]**
- **safety_policies: SafetyPolicy_v1[]**
- **gid: string (optional)**
  - Graph/run identifier the policy set is intended for.
- **run_id: string (optional)**
  - Run/session identifier the policy set is bound to.
- **meta: object (optional)**
  - Arbitrary annotations (e.g. diagnostics toggles, NAP governance flags).
- **policy_set_hash: string**
  - Canonical hash of the policy payload for binding into U-ledger entries.

### TopologyPolicy_v1

Defines structural limits and allowed operations.

- **policy_id: string** — unique identifier.
- **max_nodes: int (optional)** — hard cap on node count.
- **max_edges: int (optional)** — hard cap on edge count.
- **allowed_ops: string[]** — allowed topology operations
  (`ADD_NODE`, `REMOVE_NODE`, `ADD_EDGE`, `REMOVE_EDGE`, `REWIRE`, `TUNE`).
- **description: string (optional)** — human-readable notes.

### BudgetPolicy_v1

Defines rate/volume limits for governed changes.

- **policy_id: string** — unique identifier.
- **max_actions_per_window: int (optional)** — how many approved actions may be
  applied per window.
- **max_proposals_per_window: int (optional)** — how many proposals may be
  evaluated/queued per window.
- **max_topology_changes: int (optional)** — cap on topology-modifying actions.
- **notes: string (optional)** — rationale or scope.

### SafetyPolicy_v1

Defines invariants that must not be violated.

- **policy_id: string** — unique identifier.
- **invariants: string[]** — invariant identifiers/descriptions.
- **severity: enum { "HARD", "SOFT" }** — whether violations abort or warn.
- **description: string (optional)** — additional context.

---

## Binding to Sessions and Ledger Entries

- `SessionConfig_v1.governance` carries a `GovernanceConfig_v1` instance.
- When U-ledger entries are built, the **policy_set_hash** is copied into each
  `ULedgerEntry_v1.policy_set_hash`, tying every tick/window to the governing
  policy set.
- Governance hashes are deterministic (canonical JSON + SHA-256) so policy sets
  can be verified independently of runtime state.

---

## Invariants

- `policy_id` values must be unique across all policy lists in a config.
- `allowed_ops` must be drawn from the supported operation list above.
- Numeric limits must be non-negative when provided.
- `policy_set_hash` must match the canonical payload of the policy lists,
  governance_mode, and codex_action_mode.

---

## Usage Notes

- For existing CMP-0 runs with Codex disabled, use `governance_mode = "OFF"`.
- For observational runs, use `governance_mode = "OBSERVE"` to evaluate/log
  proposals without applying them.
- For safe governance rehearsals, use `governance_mode = "DRY_RUN"` so actions
  are recorded as hypothetical but never applied.
- For Phase 5 governed runs, set `governance_mode = "ENFORCE"` (or
  `codex_action_mode = "GOVERNED_APPLY"`) and supply concrete policies for
  budgets, safety, and topology constraints.
- The `meta` bag can surface governance-related diagnostics/NAP flags without
  affecting the canonical policy hash.
