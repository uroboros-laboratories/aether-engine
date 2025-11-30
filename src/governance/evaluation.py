"""Governance evaluation helpers for Codex proposals (Phase 5 P5.2)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Sequence, Tuple, TYPE_CHECKING

from governance.config import BudgetPolicyV1, GovernanceConfigV1, TopologyPolicyV1

if TYPE_CHECKING:  # pragma: no cover - import guard to avoid circular deps
    from codex.context import CodexProposalV1

GOVERNANCE_STATUSES = ("OK", "SOFT_FAIL", "HARD_FAIL")

ACTION_TO_TOPOLOGY_OPS = {
    "ADD": ("ADD_NODE", "ADD_EDGE"),
    "PLACE": ("ADD_NODE", "ADD_EDGE"),
    "MERGE": ("REWIRE",),
    "RETIRE": ("REMOVE_NODE", "REMOVE_EDGE"),
    "TUNE": ("TUNE",),
}


@dataclass(frozen=True)
class GovernanceEvaluationResult:
    """Structured governance evaluation output for a proposal."""

    status: str
    violated_policies: Tuple[str, ...] = ()
    scores: Dict[str, float] = None
    notes: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in GOVERNANCE_STATUSES:
            raise ValueError(f"status must be one of {GOVERNANCE_STATUSES}")
        if self.scores is None:
            object.__setattr__(self, "scores", {})
        if not isinstance(self.violated_policies, tuple):
            object.__setattr__(self, "violated_policies", tuple(self.violated_policies))
        for policy_id in self.violated_policies:
            if not isinstance(policy_id, str) or not policy_id:
                raise ValueError("violated_policies entries must be non-empty strings")
        if not isinstance(self.notes, tuple):
            object.__setattr__(self, "notes", tuple(self.notes))


@dataclass(frozen=True)
class BudgetCapUsage:
    """Usage snapshot for a single budget dimension."""

    attr: str
    limit: int | None
    used: int
    exhausted: bool
    policy_id: str | None = None

    def to_dict(self) -> Dict[str, object]:
        return {
            "attr": self.attr,
            "limit": self.limit,
            "used": self.used,
            "exhausted": self.exhausted,
            "policy_id": self.policy_id,
        }


@dataclass(frozen=True)
class BudgetUsage:
    """Aggregate budget usage for a governed window."""

    proposals_seen: int
    actions_accepted: int
    topology_changes_applied: int
    caps: Tuple[BudgetCapUsage, ...] = ()

    def to_dict(self) -> Dict[str, object]:
        return {
            "proposals_seen": self.proposals_seen,
            "actions_accepted": self.actions_accepted,
            "topology_changes_applied": self.topology_changes_applied,
            "caps": [cap.to_dict() for cap in self.caps],
        }


def _required_topology_ops(proposal: CodexProposalV1) -> Tuple[str, ...]:
    return ACTION_TO_TOPOLOGY_OPS.get(proposal.action, ())


def _check_topology_policies(
    proposal: CodexProposalV1, policies: Sequence[TopologyPolicyV1]
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    if not policies:
        return (), ()

    required_ops = _required_topology_ops(proposal)
    if not required_ops:
        return (), ()

    violations: list[str] = []
    notes: list[str] = []
    for policy in policies:
        missing = [op for op in required_ops if op not in policy.allowed_ops]
        if missing:
            violations.append(policy.policy_id)
            notes.append(
                f"Policy {policy.policy_id} does not allow required ops: {sorted(set(missing))}"
            )
    return tuple(violations), tuple(notes)


def _topology_change_count(proposal: CodexProposalV1) -> int:
    edge_ids = proposal.target_location.get("edge_ids", [])
    if isinstance(edge_ids, Sequence):
        return len(edge_ids)
    return 1


def _check_budget_policies(
    proposal: CodexProposalV1, policies: Sequence[BudgetPolicyV1]
) -> Tuple[Tuple[str, ...], Tuple[str, ...], Dict[str, float]]:
    if not policies:
        return (), (), {}

    violations: list[str] = []
    notes: list[str] = []
    scores: dict[str, float] = {}

    change_count = _topology_change_count(proposal)
    scores["topology_change_count"] = float(change_count)

    for policy in policies:
        if (
            policy.max_topology_changes is not None
            and change_count > policy.max_topology_changes
        ):
            violations.append(policy.policy_id)
            notes.append(
                f"Policy {policy.policy_id} caps topology changes at {policy.max_topology_changes}"
            )
    return tuple(violations), tuple(notes), scores


def evaluate_proposal(
    *, proposal: CodexProposalV1, config: GovernanceConfigV1
) -> GovernanceEvaluationResult:
    """Evaluate a Codex proposal against governance policies (P5.2)."""

    topo_violations, topo_notes = _check_topology_policies(
        proposal, config.topology_policies
    )
    budget_violations, budget_notes, scores = _check_budget_policies(
        proposal, config.budget_policies
    )

    violated = tuple(sorted({*topo_violations, *budget_violations}))
    notes = topo_notes + budget_notes

    if violated:
        status = "HARD_FAIL"
    else:
        status = "OK"

    return GovernanceEvaluationResult(
        status=status, violated_policies=violated, scores=scores, notes=notes
    )


def annotate_proposal(
    *,
    proposal: CodexProposalV1,
    evaluation: GovernanceEvaluationResult,
    evaluated_at_tick: int | None = None,
) -> CodexProposalV1:
    """Return a proposal annotated with governance evaluation metadata."""

    return replace(
        proposal,
        governance_status=evaluation.status,
        violated_policies=evaluation.violated_policies,
        governance_scores=evaluation.scores,
        governance_notes={"notes": list(evaluation.notes)},
        evaluated_at_tick=evaluated_at_tick,
    )


def _cap_value(policies: Sequence[BudgetPolicyV1], attr: str) -> int | None:
    caps = [getattr(policy, attr) for policy in policies if getattr(policy, attr) is not None]
    if not caps:
        return None
    return min(int(value) for value in caps)


def _cap_policy_id(policies: Sequence[BudgetPolicyV1], attr: str, value: int | None) -> str | None:
    for policy in policies:
        current = getattr(policy, attr)
        if current is not None and value == int(current):
            return policy.policy_id
    if policies:
        return policies[0].policy_id
    return None


@dataclass(frozen=True)
class GovernedActionQueue:
    """Outcome of the TBP governed decision loop for a window."""

    evaluated: Tuple[CodexProposalV1, ...]
    approved: Tuple[CodexProposalV1, ...]
    rejected: Tuple[CodexProposalV1, ...]
    budget_usage: BudgetUsage
    dry_run: bool = False


def governed_decision_loop(
    *,
    proposals: Sequence[CodexProposalV1],
    config: GovernanceConfigV1,
    window_id: str,
    evaluated_at_tick: int | None = None,
) -> GovernedActionQueue:
    """Evaluate proposals and build a governed action queue (P5.3)."""

    mode = config.codex_action_mode
    dry_run_mode = mode == "DRY_RUN"

    if mode == "OFF" or not proposals:
        empty_usage = BudgetUsage(
            proposals_seen=len(proposals),
            actions_accepted=0,
            topology_changes_applied=0,
            caps=(),
        )
        return GovernedActionQueue(
            evaluated=(), approved=(), rejected=(), budget_usage=empty_usage, dry_run=dry_run_mode
        )

    proposal_cap = _cap_value(config.budget_policies, "max_proposals_per_window")
    action_cap = _cap_value(config.budget_policies, "max_actions_per_window")
    topology_cap = _cap_value(config.budget_policies, "max_topology_changes")

    evaluated: list[CodexProposalV1] = []
    approved: list[CodexProposalV1] = []
    rejected: list[CodexProposalV1] = []

    proposals_seen = 0
    topology_changes_applied = 0

    for idx, proposal in enumerate(proposals):
        proposals_seen += 1
        if proposal_cap is not None and idx >= proposal_cap:
            policy_id = _cap_policy_id(config.budget_policies, "max_proposals_per_window", proposal_cap)
            overflow_eval = GovernanceEvaluationResult(
                status="SOFT_FAIL",
                violated_policies=(policy_id,) if policy_id else (),
                scores={},
                notes=(
                    f"Budget cap max_proposals_per_window={proposal_cap} reached for window {window_id}",
                ),
            )
            annotated_overflow = annotate_proposal(
                proposal=proposal, evaluation=overflow_eval, evaluated_at_tick=evaluated_at_tick
            )
            final_overflow = replace(annotated_overflow, status="REJECTED")
            evaluated.append(final_overflow)
            rejected.append(final_overflow)
            continue

        evaluation = evaluate_proposal(proposal=proposal, config=config)
        annotated = annotate_proposal(
            proposal=proposal, evaluation=evaluation, evaluated_at_tick=evaluated_at_tick
        )

        if mode == "OBSERVE":
            final = replace(
                annotated,
                status="REJECTED",
                governance_notes={
                    **annotated.governance_notes,
                    "notes": tuple(annotated.governance_notes.get("notes", ()))
                    + ("Governance mode OBSERVE (no actions applied)",),
                },
            )
            evaluated.append(final)
            rejected.append(final)
            continue

        change_count = _topology_change_count(proposal)
        if (
            evaluation.status == "OK"
            and (action_cap is None or len(approved) < action_cap)
            and (
                topology_cap is None
                or topology_changes_applied + change_count <= topology_cap
            )
        ):
            notes: tuple[str, ...] = tuple(annotated.governance_notes.get("notes", ()))
            if dry_run_mode:
                notes = notes + ("Governance mode DRY_RUN (action not applied)",)
            final = replace(
                annotated,
                status="ACCEPTED",
                governance_notes={"notes": notes} if notes else dict(annotated.governance_notes),
            )
            approved.append(final)
            evaluated.append(final)
            topology_changes_applied += change_count
        else:
            policy_id = _cap_policy_id(
                config.budget_policies, "max_actions_per_window", action_cap if action_cap is not None else -1
            )
            notes = list(evaluation.notes)
            if evaluation.status == "OK" and action_cap is not None:
                notes.append(
                    f"Budget cap max_actions_per_window={action_cap} reached for window {window_id}"
                )
            if evaluation.status == "OK" and topology_cap is not None and topology_changes_applied + change_count > topology_cap:
                policy_id = _cap_policy_id(
                    config.budget_policies, "max_topology_changes", topology_cap
                )
                notes.append(
                    f"Budget cap max_topology_changes={topology_cap} reached for window {window_id}"
                )
            final = replace(
                annotated,
                status="REJECTED",
                violated_policies=annotated.violated_policies
                if evaluation.status != "OK"
                else (
                    (policy_id,)
                    if policy_id
                    and ((action_cap is not None) or (topology_cap is not None))
                    else ()
                ),
                governance_notes={"notes": notes},
            )
            evaluated.append(final)
            rejected.append(final)

    caps: list[BudgetCapUsage] = []
    caps.append(
        BudgetCapUsage(
            attr="max_proposals_per_window",
            limit=proposal_cap,
            used=proposals_seen,
            exhausted=proposal_cap is not None and proposals_seen >= proposal_cap,
            policy_id=_cap_policy_id(config.budget_policies, "max_proposals_per_window", proposal_cap)
            if proposal_cap is not None
            else None,
        )
    )
    caps.append(
        BudgetCapUsage(
            attr="max_actions_per_window",
            limit=action_cap,
            used=len(approved),
            exhausted=action_cap is not None and len(approved) >= action_cap,
            policy_id=_cap_policy_id(config.budget_policies, "max_actions_per_window", action_cap)
            if action_cap is not None
            else None,
        )
    )
    caps.append(
        BudgetCapUsage(
            attr="max_topology_changes",
            limit=topology_cap,
            used=topology_changes_applied,
            exhausted=topology_cap is not None
            and topology_changes_applied >= topology_cap,
            policy_id=_cap_policy_id(config.budget_policies, "max_topology_changes", topology_cap)
            if topology_cap is not None
            else None,
        )
    )

    return GovernedActionQueue(
        evaluated=tuple(evaluated),
        approved=tuple(approved),
        rejected=tuple(rejected),
        budget_usage=BudgetUsage(
            proposals_seen=proposals_seen,
            actions_accepted=len(approved),
            topology_changes_applied=topology_changes_applied,
            caps=tuple(caps),
        ),
        dry_run=dry_run_mode,
    )

