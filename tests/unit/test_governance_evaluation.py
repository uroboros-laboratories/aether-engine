"""Tests for governance evaluation of CodexProposal_v1 (P5.2)."""

from codex.context import CodexProposalV1
from governance import (
    BudgetPolicyV1,
    GovernanceConfigV1,
    GovernanceEvaluationResult,
    GovernedActionQueue,
    TopologyPolicyV1,
    annotate_proposal,
    evaluate_proposal,
    governed_decision_loop,
)


def _proposal(
    *, proposal_id: str = "P1", action: str = "PLACE", edge_ids: tuple[int, ...] = (1, 2)
) -> CodexProposalV1:
    return CodexProposalV1(
        proposal_id=proposal_id,
        library_id="LIB",
        gid="G1",
        action=action,
        expected_effect={"delta_L_total": -1},
        created_at_tick=3,
        status="PENDING",
        target_location={"edge_ids": list(edge_ids)},
    )


def test_topology_policy_blocks_disallowed_ops() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        topology_policies=(TopologyPolicyV1(policy_id="tp1", allowed_ops=("ADD_NODE",)),),
    )

    proposal = _proposal(action="MERGE")
    result = evaluate_proposal(proposal=proposal, config=config)

    assert result.status == "HARD_FAIL"
    assert result.violated_policies == ("tp1",)
    assert "required ops" in result.notes[0]


def test_budget_policy_caps_topology_changes() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_topology_changes=1),),
    )

    proposal = _proposal(edge_ids=(1, 2, 3))
    result = evaluate_proposal(proposal=proposal, config=config)

    assert result.status == "HARD_FAIL"
    assert result.violated_policies == ("bp1",)
    assert result.scores["topology_change_count"] == 3.0


def test_successful_evaluation_and_annotation() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        topology_policies=(TopologyPolicyV1(policy_id="tp-ok"),),
        budget_policies=(BudgetPolicyV1(policy_id="bp-ok", max_topology_changes=5),),
    )

    proposal = _proposal(edge_ids=(1,))
    result = evaluate_proposal(proposal=proposal, config=config)

    annotated = annotate_proposal(proposal=proposal, evaluation=result, evaluated_at_tick=4)

    assert result.status == "OK"
    assert result.scores["topology_change_count"] == 1.0
    assert annotated.governance_status == "OK"
    assert annotated.evaluated_at_tick == 4
    assert annotated.violated_policies == ()


def test_governed_decision_loop_respects_budget_caps() -> None:
    proposals = [
        _proposal(proposal_id="P1", edge_ids=(1,)),
        _proposal(proposal_id="P2", edge_ids=(2,)),
        _proposal(proposal_id="P3", edge_ids=(3,)),
    ]

    config = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        budget_policies=(
            BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1, max_proposals_per_window=2),
        ),
    )

    queue = governed_decision_loop(
        proposals=proposals, config=config, window_id="W1", evaluated_at_tick=9
    )

    assert isinstance(queue, GovernedActionQueue)
    assert [p.status for p in queue.approved] == ["ACCEPTED"]
    assert [p.proposal_id for p in queue.approved] == ["P1"]
    assert len(queue.evaluated) == 3
    assert {p.proposal_id for p in queue.rejected} == {"P2", "P3"}
    overflow = next(p for p in queue.rejected if p.proposal_id == "P3")
    assert overflow.governance_status == "SOFT_FAIL"
    assert overflow.evaluated_at_tick == 9
    usage = queue.budget_usage
    assert usage.actions_accepted == 1
    assert usage.proposals_seen == 3
    caps_by_attr = {cap.attr: cap for cap in usage.caps}
    assert caps_by_attr["max_proposals_per_window"].exhausted is True
    assert caps_by_attr["max_actions_per_window"].exhausted is True


def test_suggest_only_evaluates_without_approving() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="SUGGEST_ONLY",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )
    proposals = [_proposal(proposal_id="PX", edge_ids=(1,))]

    queue = governed_decision_loop(
        proposals=proposals, config=config, window_id="WIN", evaluated_at_tick=3
    )

    assert len(queue.approved) == 0
    assert len(queue.rejected) == 1
    rejected = queue.rejected[0]
    assert rejected.proposal_id == "PX"
    assert rejected.governance_status == "OK"
    assert rejected.evaluated_at_tick == 3
    usage = queue.budget_usage
    assert usage.proposals_seen == 1
    assert usage.actions_accepted == 0


def test_dry_run_marks_hypothetical_acceptances() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="DRY_RUN",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )
    proposals = [_proposal(proposal_id="PX", edge_ids=(1,))]

    queue = governed_decision_loop(
        proposals=proposals, config=config, window_id="WIN", evaluated_at_tick=3
    )

    assert queue.dry_run is True
    assert len(queue.approved) == 1
    would_apply = queue.approved[0]
    assert would_apply.status == "ACCEPTED"
    assert "DRY_RUN" in " ".join(would_apply.governance_notes.get("notes", ()))
    usage = queue.budget_usage
    assert usage.proposals_seen == 1
    assert usage.actions_accepted == 1
