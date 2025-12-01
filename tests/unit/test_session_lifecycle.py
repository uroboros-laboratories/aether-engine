from core.tick_loop import TickLoopWindowSpec, run_gf01
from gate import SessionConfigV1, _pfna_payload_ref, build_pfna_placeholder, run_session
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile, load_topology_profile


def _gf01_session_config() -> SessionConfigV1:
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    window_specs = [
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_8",
            apx_name="GF01_APX_v0_full_window",
            start_tick=1,
            end_tick=8,
        ),
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_2",
            apx_name="GF01_APX_v0_ticks_1_2",
            start_tick=1,
            end_tick=2,
        ),
    ]
    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=8,
        window_specs=window_specs,
        primary_window_id="GF01_W1_ticks_1_8",
        run_id="GF01_SESSION",
        nid="gf01-node",
    )


def test_run_session_emits_ctrl_envelopes_and_wraps_tick_loop():
    cfg = _gf01_session_config()
    session = run_session(cfg)
    tick_result = session.tick_result

    manifest = tick_result.manifests["GF01_APX_v0_full_window"]
    assert manifest.manifest_check == 824666593

    # Lifecycle envelopes wrap the per-tick DATA envelopes
    assert [env.layer for env in session.lifecycle_envelopes] == ["CTRL", "CTRL"]
    assert session.lifecycle_envelopes[0].tick == 1
    assert session.lifecycle_envelopes[1].tick == cfg.total_ticks

    all_layers = [env.layer for env in session.all_envelopes]
    assert all_layers[0] == "CTRL"
    assert all_layers[-1] == "EGRESS"
    assert all_layers[-2] == "CTRL"
    assert all(layer == "DATA" for layer in all_layers[1:-2])
    assert session.tick_result.ingress_envelopes == []

    egress = session.tick_result.egress_envelopes
    assert len(egress) == 1
    assert egress[0].payload_ref == manifest.manifest_check
    assert egress[0].mode == "P"

    # Underlying TickLoop_v1 outputs remain aligned with existing GF-01 helper
    baseline = run_gf01()
    assert [env.payload_ref for env in tick_result.envelopes] == [
        env.payload_ref for env in baseline.envelopes
    ]


def test_run_session_applies_pfna_inputs_and_preserves_lifecycle_order():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()
    window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_3",
        apx_name="LINE_APX_v0_ticks_1_3",
        start_tick=1,
        end_tick=3,
    )
    pfna = build_pfna_placeholder(
        pfna_id="ext_seq_tick1",
        gid=topo.gid,
        run_id="LINE_PFNA",
        tick=1,
        nid="ext-source",
        values=[1, 0, 0, 0],
        description="add one to the first node at tick 1",
    )

    cfg = SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[2, 2, 2, 2],
        total_ticks=3,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_PFNA",
        nid="engine-line",
        pfna_inputs=(pfna,),
    )

    session = run_session(cfg)
    first_ledger = session.tick_result.ledgers[0]
    assert tuple(first_ledger.pre_u) == (3, 2, 2, 2)

    scene = session.tick_result.scenes[0]
    assert scene.pfna_refs == (pfna.pfna_id,)

    layers = [env.layer for env in session.all_envelopes]
    assert layers[0] == "CTRL"
    assert layers[1] == "INGRESS"
    assert layers[-1] == "EGRESS"
    assert layers[-2] == "CTRL"
    assert layers[2:-2] == ["DATA", "DATA", "DATA"]
    assert session.lifecycle_envelopes[-1].prev_chain == session.tick_result.p_blocks[-1].C_t

    ingress = session.tick_result.ingress_envelopes
    assert len(ingress) == 1
    assert ingress[0].mode == "P"
    assert ingress[0].payload_ref == _pfna_payload_ref((pfna,))


def test_run_session_pfna_invalid_gid_raises():
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    window_spec = TickLoopWindowSpec(
        window_id="GF01_W1_ticks_1_2",
        apx_name="GF01_APX_v0_ticks_1_2",
        start_tick=1,
        end_tick=2,
    )

    bad_pfna = build_pfna_placeholder(
        pfna_id="bad_gid",
        gid="WRONG",
        run_id="GF01_SESSION",
        tick=1,
        nid="x",
        values=[0 for _ in range(topo.N)],
    )

    cfg = SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=2,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="GF01_SESSION",
        nid="gf01-node",
        pfna_inputs=(bad_pfna,),
    )

    try:
        run_session(cfg)
    except ValueError as exc:
        assert "PFNA gid must match the topology gid" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected PFNA gid validation to fail")


def test_run_session_pfna_initial_state_mapping_and_determinism():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()
    window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_3",
        apx_name="LINE_APX_v0_ticks_1_3",
        start_tick=1,
        end_tick=3,
    )

    pfna_init = build_pfna_placeholder(
        pfna_id="init_boost",
        gid=topo.gid,
        run_id="LINE_PFNA_INIT",
        tick=0,
        nid="init-seed",
        values=[1, -1, 0, 0],
        description="adjust initial state",
    )

    cfg_base = SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[2, 2, 2, 2],
        total_ticks=3,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_PFNA_INIT",
        nid="engine-line",
    )

    cfg_pfna = SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[2, 2, 2, 2],
        total_ticks=3,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_PFNA_INIT",
        nid="engine-line",
        pfna_inputs=(pfna_init,),
    )

    base_run = run_session(cfg_base)
    pfna_run_first = run_session(cfg_pfna)
    pfna_run_second = run_session(cfg_pfna)

    assert base_run.tick_result.ledgers[0].pre_u != pfna_run_first.tick_result.ledgers[0].pre_u
    assert tuple(pfna_run_first.tick_result.ledgers[0].pre_u) == (3, 1, 2, 2)

    assert pfna_run_first.tick_result.ledgers[-1].post_u == pfna_run_second.tick_result.ledgers[-1].post_u
