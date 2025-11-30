from codex.context import CodexProposalV1
from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop
from governance import BudgetPolicyV1, GovernanceConfigV1
from ops import build_governance_summary
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def _proposal(proposal_id: str) -> CodexProposalV1:
    return CodexProposalV1(
        proposal_id=proposal_id,
        library_id="LIB",
        gid="GF01",
        action="PLACE",
        expected_effect={"delta_L_total": -1},
        created_at_tick=0,
        status="PENDING",
        target_location={"edge_ids": [1]},
    )


def test_tick_loop_attaches_governed_action_queue() -> None:
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    window = TickLoopWindowSpec(window_id="W", apx_name="APX", start_tick=1, end_tick=2)

    governance = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )

    proposals = [_proposal("P1"), _proposal("P2")]

    run = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=(3, 1, 0, 0, 0, 0),
        total_ticks=2,
        window_specs=[window],
        primary_window_id=window.window_id,
        run_id="RUN",  # pragma: allowlist secret
        nid="N/A",
        governance=governance,
        codex_proposals=proposals,
    )

    assert len(run.codex_proposals) == 2
    assert len(run.codex_actions) == 1
    assert run.codex_actions[0].status == "ACCEPTED"
    assert run.codex_actions[0].proposal_id == "P1"
    rejected = next(p for p in run.codex_proposals if p.proposal_id == "P2")
    assert rejected.status == "REJECTED"
    assert "cap" in " ".join(rejected.governance_notes.get("notes", []))


def test_dry_run_and_enforce_share_evaluations_but_not_applications() -> None:
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    window = TickLoopWindowSpec(window_id="W", apx_name="APX", start_tick=1, end_tick=2)

    governance_apply = GovernanceConfigV1(
        governance_mode="ENFORCE",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )
    governance_dry = GovernanceConfigV1(
        governance_mode="DRY_RUN",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )

    proposals_apply = [_proposal("P1"), _proposal("P2")]

    run_apply = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=(3, 1, 0, 0, 0, 0),
        total_ticks=2,
        window_specs=[window],
        primary_window_id=window.window_id,
        run_id="RUN-APPLY",  # pragma: allowlist secret
        nid="N/A",
        governance=governance_apply,
        codex_proposals=proposals_apply,
    )

    proposals_dry = [_proposal("P1"), _proposal("P2")]

    run_dry = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=(3, 1, 0, 0, 0, 0),
        total_ticks=2,
        window_specs=[window],
        primary_window_id=window.window_id,
        run_id="RUN-DRY",  # pragma: allowlist secret
        nid="N/A",
        governance=governance_dry,
        codex_proposals=proposals_dry,
    )

    assert len(run_apply.codex_actions) == 1
    assert run_apply.codex_actions[0].status == "ACCEPTED"
    assert len(run_dry.codex_actions) == 0
    assert len(run_dry.codex_hypothetical_actions) == 1
    assert run_dry.codex_hypothetical_actions[0].status == "ACCEPTED"

    summary_apply = build_governance_summary(run_apply)
    summary_dry = build_governance_summary(run_dry)
    assert summary_apply.proposals_seen == summary_dry.proposals_seen
    assert summary_apply.budget_usage == summary_dry.budget_usage
    assert summary_apply.actions_applied == 1
    assert summary_dry.actions_applied == 0
    assert summary_dry.actions_hypothetical == 1
