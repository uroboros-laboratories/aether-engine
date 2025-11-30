from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop
from gate import SessionConfigV1, run_session
from governance import BudgetPolicyV1, GovernanceConfigV1
from codex.context import CodexProposalV1
from ops.introspection import build_introspection_view
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def _proposal(proposal_id: str, gid: str) -> CodexProposalV1:
    return CodexProposalV1(
        proposal_id=proposal_id,
        library_id="LIB",
        gid=gid,
        action="PLACE",
        expected_effect={"delta_L_total": -1},
        created_at_tick=1,
        status="PENDING",
        target_location={"edge_ids": [1]},
    )


def test_governance_events_emit_gov_layer_and_meta() -> None:
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    window_specs = [
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_8",
            apx_name="GF01_APX_v0_full_window",
            start_tick=1,
            end_tick=8,
        )
    ]

    governance = GovernanceConfigV1(
        gid=topo.gid,
        run_id="GOV_RUN",
        codex_action_mode="GOVERNED_APPLY",
        budget_policies=(BudgetPolicyV1(policy_id="bp1", max_actions_per_window=1),),
    )

    proposals = [_proposal("P1", topo.gid), _proposal("P2", topo.gid)]

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=8,
        window_specs=window_specs,
        primary_window_id="GF01_W1_ticks_1_8",
        run_id="GOV_RUN",
        nid="gf01-node",
        governance=governance,
        codex_proposals=proposals,
    )

    gov_layers = [env.layer for env in result.governance_envelopes]
    assert gov_layers == ["GOV", "GOV", "GOV"]

    events = [env.meta.get("event") for env in result.governance_envelopes]
    assert events[0] == "POLICY_SET_LOADED"
    assert "GOVERNANCE_DECISION_SUMMARY" in events
    assert "BUDGET_EXHAUSTION" in events

    summary = next(env for env in result.governance_envelopes if env.meta.get("event") == "GOVERNANCE_DECISION_SUMMARY")
    assert summary.meta["policy_set_hash"] == governance.policy_set_hash
    assert summary.meta["actions_accepted"] == 1
    budget = next(env for env in result.governance_envelopes if env.meta.get("event") == "BUDGET_EXHAUSTION")
    assert budget.meta["exhausted_caps"][0]["attr"] == "max_actions_per_window"

    view = build_introspection_view(result)
    gov_from_view = view.get_nap_envelopes(layer="GOV")
    assert len(gov_from_view) == 3
    assert gov_from_view[0].meta["event"] == "POLICY_SET_LOADED"


def test_governance_layer_absent_when_disabled() -> None:
    cfg = SessionConfigV1(
        topo=gf01_topology_profile(),
        profile=gf01_profile_cmp0(),
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=2,
        window_specs=(
            TickLoopWindowSpec(
                window_id="GF01_W1_ticks_1_2",
                apx_name="GF01_APX_v0_ticks_1_2",
                start_tick=1,
                end_tick=2,
            ),
        ),
        primary_window_id="GF01_W1_ticks_1_2",
        run_id="NO_GOV_RUN",
        nid="node-1",
    )

    session = run_session(cfg)
    gov_layers = [env.layer for env in session.all_envelopes if env.layer == "GOV"]
    assert gov_layers == []
    assert session.tick_result.governance_envelopes == []
