from governance import (
    BudgetPolicyV1,
    GovernanceConfigV1,
    SafetyPolicyV1,
    TopologyPolicyV1,
    governance_config_from_mapping,
)


def test_policy_set_hash_is_stable_across_ordering():
    topo_policy = TopologyPolicyV1(
        policy_id="topo_main",
        max_nodes=12,
        max_edges=18,
        allowed_ops=("ADD_NODE", "ADD_EDGE", "TUNE"),
        description="GF01 structural limits",
    )
    budget_a = BudgetPolicyV1(
        policy_id="budget_cap",
        max_actions_per_window=2,
        max_topology_changes=1,
    )
    budget_b = BudgetPolicyV1(
        policy_id="budget_buffer",
        max_proposals_per_window=3,
        notes="allow a few proposals for scoring",
    )
    safety_policy = SafetyPolicyV1(
        policy_id="safety_core",
        invariants=("no_negative_flux", "preserve_chain_continuity"),
        severity="HARD",
    )

    cfg = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        topology_policies=(topo_policy,),
        budget_policies=(budget_a, budget_b),
        safety_policies=(safety_policy,),
        gid="GF01",
        run_id="GF01_RUN",
    )

    reordered = GovernanceConfigV1(
        codex_action_mode="GOVERNED_APPLY",
        topology_policies=(topo_policy,),
        budget_policies=(budget_b, budget_a),
        safety_policies=(safety_policy,),
        gid="GF01",
        run_id="GF01_RUN",
    )

    assert cfg.policy_set_hash == reordered.policy_set_hash


def test_governance_config_round_trips_via_mapping():
    cfg = GovernanceConfigV1(
        codex_action_mode="SUGGEST_ONLY",
        topology_policies=(
            TopologyPolicyV1(
                policy_id="ops_only",
                allowed_ops=("ADD_NODE", "REMOVE_NODE"),
            ),
        ),
        budget_policies=(),
        safety_policies=(SafetyPolicyV1(policy_id="safety_tag", invariants=("no_overflow",)),),
        gid="GF01",
        run_id="GF01_DEMO",
        meta={"nap": {"ctrl_layer": True}},
    )

    mapping = cfg.to_dict()
    rebuilt = governance_config_from_mapping(mapping)

    assert rebuilt.policy_set_hash == cfg.policy_set_hash
    assert rebuilt.gid == cfg.gid
    assert rebuilt.run_id == cfg.run_id
    assert rebuilt.codex_action_mode == cfg.codex_action_mode
    assert rebuilt.topology_policies[0].allowed_ops == cfg.topology_policies[0].allowed_ops
