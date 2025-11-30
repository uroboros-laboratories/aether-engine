from governance import BudgetPolicyV1, GovernanceConfigV1, governed_decision_loop
from governance.evaluation import BudgetUsage
from codex.context import CodexProposalV1


def _proposal(proposal_id: str, change_count: int) -> CodexProposalV1:
    return CodexProposalV1(
        proposal_id=proposal_id,
        library_id="LIB",
        gid="GF",
        action="PLACE",
        expected_effect={"delta_L_total": -1},
        created_at_tick=0,
        status="PENDING",
        target_location={"edge_ids": list(range(change_count))},
    )


def test_topology_budget_tracks_usage_and_exhaustion() -> None:
    config = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        budget_policies=(
            BudgetPolicyV1(
                policy_id="bp-topo", max_topology_changes=2, max_actions_per_window=3
            ),
        ),
    )

    proposals = [_proposal("P1", 2), _proposal("P2", 1), _proposal("P3", 1)]

    queue = governed_decision_loop(
        proposals=proposals, config=config, window_id="W1", evaluated_at_tick=5
    )

    assert [p.status for p in queue.approved] == ["ACCEPTED"]
    rejected_ids = [p.proposal_id for p in queue.rejected]
    assert rejected_ids == ["P2", "P3"]
    rejected_notes = " ".join(queue.rejected[0].governance_notes.get("notes", []))
    assert "max_topology_changes=2" in rejected_notes

    usage: BudgetUsage = queue.budget_usage
    assert usage.topology_changes_applied == 2
    caps_by_attr = {cap.attr: cap for cap in usage.caps}
    topo_cap = caps_by_attr["max_topology_changes"]
    assert topo_cap.exhausted is True
    assert topo_cap.limit == 2
    assert topo_cap.used == 2
