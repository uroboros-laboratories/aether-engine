from __future__ import annotations

import pytest

from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop, run_gf01
from gate import (
    ALLOWED_NAP_LAYERS,
    PressStreamSpecV1,
    _default_press_stream_specs,
    build_pfna_placeholder,
    emit_nap_envelope,
    validate_scene_frame,
)
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile, load_topology_profile


def test_gf01_scene_frames_anchor_nap_envelopes():
    result = run_gf01()
    manifest = result.manifests["GF01_APX_v0_full_window"]
    profile = result.profile

    expected_chain = [
        20987847,
        356793608,
        65491504,
        113355772,
        927048329,
        759821701,
        916969047,
        588473909,
    ]
    expected_prev_chain = [profile.C0] + expected_chain[:-1]

    assert manifest.manifest_check == 824666593
    assert [scene.C_t for scene in result.scenes] == expected_chain
    assert [scene.C_prev for scene in result.scenes] == expected_prev_chain
    assert [env.prev_chain for env in result.envelopes] == expected_prev_chain
    assert all(scene.manifest_check == manifest.manifest_check for scene in result.scenes)
    assert all(scene.meta["manifest_ref"] == manifest.apx_name for scene in result.scenes)
    assert all(scene.meta["p_block_ref"] == f"loom_p_block_{scene.tick}" for scene in result.scenes)

    envelopes = result.envelopes
    assert all(env.v == 1 for env in envelopes)
    assert all(env.gid == result.topo.gid for env in envelopes)
    assert all(env.nid == "N/A" for env in envelopes)
    assert all(env.layer == "DATA" for env in envelopes)
    assert all(env.mode == "P" for env in envelopes)
    assert all(env.payload_ref == manifest.manifest_check for env in envelopes)
    assert [env.seq for env in envelopes] == list(range(1, 9))
    assert [env.tick for env in envelopes] == list(range(1, 9))


def test_nap_envelopes_support_layers_and_modes():
    result = run_gf01()
    profile = result.profile
    scene = result.scenes[0]

    ctrl_env = emit_nap_envelope(
        scene,
        profile,
        layer="CTRL",
        mode="P",
        seq=99,
        payload_ref=scene.manifest_check,
    )

    assert ctrl_env.layer == "CTRL"
    assert ctrl_env.mode == "P"
    assert ctrl_env.seq == 99
    assert ctrl_env.payload_ref == scene.manifest_check

    default_env = emit_nap_envelope(scene, profile)
    assert default_env.layer == profile.nap_defaults.get("layer") == "DATA"
    assert default_env.mode == profile.nap_defaults.get("mode") == "P"

    with pytest.raises(ValueError):
        emit_nap_envelope(scene, profile, layer="INVALID")
    with pytest.raises(ValueError):
        emit_nap_envelope(scene, profile, mode="X")
    with pytest.raises(ValueError):
        emit_nap_envelope(scene, profile, layer=ALLOWED_NAP_LAYERS[0], mode="")


def test_scene_frames_emitted_for_line_topology():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()

    window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_4",
        apx_name="LINE_APX_v0_ticks_1_4",
        start_tick=1,
        end_tick=4,
    )

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[5, 4, 3, 2],
        total_ticks=4,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE",
        nid="engine-line",
    )

    manifest = result.manifests[window_spec.apx_name]
    assert len(result.scenes) == 4
    assert len(result.envelopes) == 4
    assert all(scene.window_id == window_spec.window_id for scene in result.scenes)
    assert all(scene.manifest_check == manifest.manifest_check for scene in result.scenes)
    assert all(scene.meta["manifest_ref"] == manifest.apx_name for scene in result.scenes)
    assert all(scene.meta["p_block_ref"].startswith("loom_p_block_") for scene in result.scenes)

    for scene, p_block in zip(result.scenes, result.p_blocks):
        assert scene.C_t == p_block.C_t
        assert scene.tick == p_block.tick

    assert [env.payload_ref for env in result.envelopes] == [manifest.manifest_check] * 4
    assert [env.prev_chain for env in result.envelopes] == [scene.C_prev for scene in result.scenes]


def test_pfna_inputs_feed_state_and_scene_meta():
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

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[2, 2, 2, 2],
        total_ticks=3,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_PFNA",
        nid="engine-line",
        pfna_inputs=[pfna],
    )

    first_ledger = result.ledgers[0]
    assert tuple(first_ledger.pre_u) == (3, 2, 2, 2)

    scene = result.scenes[0]
    assert scene.pfna_refs == (pfna.pfna_id,)
    assert scene.meta["pfna_refs"] == [pfna.pfna_id]

    baseline_window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_1",
        apx_name="LINE_APX_v0_tick_1",
        start_tick=1,
        end_tick=1,
    )
    baseline = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[2, 2, 2, 2],
        total_ticks=1,
        window_specs=[baseline_window_spec],
        primary_window_id=baseline_window_spec.window_id,
        run_id="LINE_BASE",
        nid="engine-line",
    )
    assert tuple(baseline.ledgers[0].pre_u) == (2, 2, 2, 2)


def test_gate_drives_press_window_streams_config():
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()

    stream_specs = _default_press_stream_specs()
    gf_window = TickLoopWindowSpec(
        window_id="GF01_W1_ticks_1_8",
        apx_name="GF01_APX_v0_full_window",
        start_tick=1,
        end_tick=8,
        streams=stream_specs,
    )
    gf_window_short = TickLoopWindowSpec(
        window_id="GF01_W1_ticks_1_2",
        apx_name="GF01_APX_v0_ticks_1_2",
        start_tick=1,
        end_tick=2,
        streams=stream_specs,
    )

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=8,
        window_specs=[gf_window, gf_window_short],
        primary_window_id=gf_window.window_id,
        run_id="GF01_CONFIGURED",
        nid="config-gf01",
    )

    manifest = result.manifests[gf_window.apx_name]
    assert manifest.manifest_check == 824666593
    stream_ids = [stream.stream_id for stream in manifest.streams]
    assert stream_ids == [spec.name for spec in stream_specs]


def test_press_streams_accept_chain_value_source():
    profile = gf01_profile_cmp0()
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")

    stream_specs = _default_press_stream_specs() + (
        PressStreamSpecV1(
            name="S3_prev_chain",
            source="prev_chain",
            scheme_hint="ID",
            description="chain accumulator per tick",
        ),
    )

    window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_3",
        apx_name="LINE_APX_v0_ticks_1_3",
        start_tick=1,
        end_tick=3,
        streams=stream_specs,
    )

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[1, 1, 1, 1],
        total_ticks=3,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_CHAIN_STREAM",
        nid="line-chain",
    )

    manifest = result.manifests[window_spec.apx_name]
    chain_stream = next(stream for stream in manifest.streams if stream.stream_id == "S3_prev_chain")
    assert chain_stream.scheme == "ID"
    assert chain_stream.L_model == 16
    assert chain_stream.L_residual == 104
    assert chain_stream.L_total == 120


def test_scene_frame_validation_checks_manifest_refs():
    result = run_gf01()
    manifest = result.manifests["GF01_APX_v0_full_window"]
    scene = result.scenes[0]

    validate_scene_frame(
        scene,
        manifest_ref=manifest.apx_name,
        manifest_check=manifest.manifest_check,
        expected_tick=scene.tick,
    )

    with pytest.raises(ValueError):
        validate_scene_frame(
            scene,
            manifest_ref="BAD_REF",
            manifest_check=manifest.manifest_check,
            expected_tick=scene.tick,
        )
