"""Press/APX GF-01 tests for Issue 4."""
from __future__ import annotations

import pytest

from press import APXiDescriptorV1, PressWindowContextV1
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.run_context import UMXRunContext
from umx.topology_profile import gf01_topology_profile


def _build_press_manifest(num_ticks: int, apx_name: str):
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    run_ctx = UMXRunContext(topo=topo, profile=profile, gid="GF01", run_id="run_0")
    run_ctx.init_state([3, 1, 0, 0, 0, 0])
    press_ctx = PressWindowContextV1(
        gid="GF01",
        run_id="run_0",
        window_id=apx_name,
        start_tick=1,
        end_tick=num_ticks,
        profile=profile,
    )

    press_ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
    press_ctx.register_stream("S2_fluxes", description="edge flux per edge")

    for _ in range(num_ticks):
        ledger = run_ctx.step()
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        press_ctx.append("S1_post_u_deltas", deltas)
        press_ctx.append("S2_fluxes", fluxes)

    manifest = press_ctx.close_window(apx_name)
    return manifest


def test_gf01_full_window_manifest_matches_spec():
    manifest = _build_press_manifest(num_ticks=8, apx_name="GF01_APX_v0_full_window")

    assert manifest.apx_name == "GF01_APX_v0_full_window"
    assert manifest.profile == "CMP-0"
    assert len(manifest.streams) == 2
    assert manifest.streams[0].stream_id == "S1_post_u_deltas"
    assert manifest.streams[0].scheme == "R"
    assert manifest.streams[0].L_total == 7
    assert manifest.streams[1].stream_id == "S2_fluxes"
    assert manifest.streams[1].scheme == "R"
    assert manifest.streams[1].L_total == 8
    assert manifest.manifest_check == 487809945


def test_gf01_two_tick_window_manifest_matches_spec():
    manifest = _build_press_manifest(num_ticks=2, apx_name="GF01_APX_v0_ticks_1_2")

    assert manifest.apx_name == "GF01_APX_v0_ticks_1_2"
    assert manifest.profile == "CMP-0"
    assert len(manifest.streams) == 2
    assert manifest.streams[0].L_total == 1
    assert manifest.streams[1].L_total == 2
    assert manifest.manifest_check == 869911338


def test_press_window_context_enforces_tick_alignment():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="w1", start_tick=1, end_tick=2, profile=profile
    )
    press_ctx.register_stream("S_delta")

    with pytest.raises(ValueError):
        press_ctx.append("S_delta", 1, tick=2)

    press_ctx.append("S_delta", 1)
    press_ctx.append("S_delta", 2)
    manifest = press_ctx.close_window("w1_manifest")
    assert manifest.streams[0].L_total == 1


def test_press_window_context_rejects_incomplete_streams():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="w1", start_tick=1, end_tick=2, profile=profile
    )
    press_ctx.register_stream("S_delta")
    press_ctx.append("S_delta", 1)

    with pytest.raises(ValueError):
        press_ctx.close_window("w1_manifest")


def test_press_window_context_clears_buffers_on_close():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="w1", start_tick=1, end_tick=1, profile=profile
    )
    press_ctx.register_stream("S_delta")
    press_ctx.append("S_delta", 1)

    _ = press_ctx.close_window("w1_manifest")
    assert press_ctx.streams["S_delta"].values == []
    # Ensure tick counter reset for reuse
    press_ctx.append("S_delta", 2)


def test_id_scheme_counts_entries_and_width():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="id_stream", start_tick=1, end_tick=3, profile=profile
    )
    press_ctx.register_stream("S_id", scheme_hint="ID")
    press_ctx.append("S_id", 5)
    press_ctx.append("S_id", 7)
    press_ctx.append("S_id", 9)

    manifest = press_ctx.close_window("id_manifest")
    stream = manifest.streams[0]
    assert stream.scheme == "ID"
    assert (stream.L_model, stream.L_residual, stream.L_total) == (1, 3, 4)


def test_r_scheme_validates_width_and_lengths():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="r_stream", start_tick=1, end_tick=3, profile=profile
    )
    press_ctx.register_stream("S_r", scheme_hint="R")
    press_ctx.append("S_r", (1, 2))
    press_ctx.append("S_r", (3, 4))
    press_ctx.append("S_r", (5, 6))

    manifest = press_ctx.close_window("r_manifest")
    stream = manifest.streams[0]
    assert stream.scheme == "R"
    assert (stream.L_model, stream.L_residual, stream.L_total) == (0, 2, 2)


def test_gr_scheme_groups_runs():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="gr_stream", start_tick=1, end_tick=6, profile=profile
    )
    press_ctx.register_stream("S_gr", scheme_hint="GR")
    for value in (1, 1, 2, 2, 2, 5):
        press_ctx.append("S_gr", value)

    manifest = press_ctx.close_window("gr_manifest")
    stream = manifest.streams[0]
    assert stream.scheme == "GR"
    assert (stream.L_model, stream.L_residual, stream.L_total) == (2, 3, 5)


def test_stream_width_mismatch_raises():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="GF01", run_id="run_0", window_id="width_mismatch", start_tick=1, end_tick=2, profile=profile
    )
    press_ctx.register_stream("S_width", scheme_hint="ID")
    press_ctx.append("S_width", (1, 2))
    with pytest.raises(ValueError):
        press_ctx.append("S_width", 3)


def test_manifest_supports_multiple_streams_and_schemes():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="G", run_id="R", window_id="mixed", start_tick=1, end_tick=3, profile=profile
    )
    press_ctx.register_stream("S_id", scheme_hint="ID", description="id stream")
    press_ctx.register_stream("S_r", scheme_hint="R", description="r stream")
    press_ctx.register_stream("S_gr", scheme_hint="GR", description="gr stream")

    for tick in range(1, 4):
        press_ctx.append("S_id", tick)
        press_ctx.append("S_r", (tick, tick + 1))
        press_ctx.append("S_gr", 5 if tick < 3 else 7)

    manifest = press_ctx.close_window("mixed_window")

    assert [s.stream_id for s in manifest.streams] == ["S_id", "S_r", "S_gr"]
    assert [s.scheme for s in manifest.streams] == ["ID", "R", "GR"]
    assert [(s.L_model, s.L_residual, s.L_total) for s in manifest.streams] == [
        (1, 3, 4),
        (0, 2, 2),
        (1, 1, 2),
    ]
    assert manifest.manifest_check == 483033096


def test_manifest_check_reflects_scheme_choice():
    profile = gf01_profile_cmp0()
    press_ctx_r = PressWindowContextV1(
        gid="G", run_id="R", window_id="w_r", start_tick=1, end_tick=2, profile=profile
    )
    press_ctx_id = PressWindowContextV1(
        gid="G", run_id="R", window_id="w_id", start_tick=1, end_tick=2, profile=profile
    )

    press_ctx_r.register_stream("S", scheme_hint="R")
    press_ctx_id.register_stream("S", scheme_hint="ID")

    for value in (1, 1):
        press_ctx_r.append("S", value)
        press_ctx_id.append("S", value)

    manifest_r = press_ctx_r.close_window("manifest_r")
    manifest_id = press_ctx_id.close_window("manifest_id")

    assert manifest_r.manifest_check != manifest_id.manifest_check


def test_apxi_disabled_matches_phase2_behaviour():
    profile = gf01_profile_cmp0()
    press_ctx = PressWindowContextV1(
        gid="G", run_id="R", window_id="w_apxi_off", start_tick=1, end_tick=2, profile=profile
    )
    press_ctx.register_stream("S_delta", scheme_hint="R")
    press_ctx.append("S_delta", 1)
    press_ctx.append("S_delta", 1)

    manifest = press_ctx.close_window("w_apxi_off_manifest")
    assert manifest.apxi_view_ref is None
    assert press_ctx.get_apxi_view() is None


def test_apxi_view_attaches_to_manifest_and_window():
    profile = gf01_profile_cmp0()
    descriptor = APXiDescriptorV1(
        descriptor_id="apxi_const",
        descriptor_type="CONST_SEGMENT",
        window_id="AEON_W1",
        stream_id="S_delta",
        params={"value": 7},
    )
    press_ctx = PressWindowContextV1(
        gid="G",
        run_id="R",
        window_id="w_apxi_on",
        start_tick=1,
        end_tick=2,
        profile=profile,
        aeon_window_id="AEON_W1",
        apxi_enabled=True,
        apxi_descriptors={"S_delta": (descriptor,)},
    )
    press_ctx.register_stream("S_delta", scheme_hint="ID")
    press_ctx.append("S_delta", 7)
    press_ctx.append("S_delta", 7)

    manifest = press_ctx.close_window("w_apxi_on_manifest")
    view = press_ctx.get_apxi_view()

    assert view is not None
    assert manifest.apxi_view_ref == view.view_id
    assert view.residual_scheme == "R"
    breakdown = view.descriptors_by_stream["S_delta"][0]
    assert breakdown.L_model == 1
    assert breakdown.L_residual == 0


def test_apxi_window_id_mismatch_raises():
    profile = gf01_profile_cmp0()
    descriptor = APXiDescriptorV1(
        descriptor_id="apxi_wrong_window",
        descriptor_type="CONST_SEGMENT",
        window_id="AEON_W2",
        stream_id="S_delta",
        params={"value": 3},
    )
    press_ctx = PressWindowContextV1(
        gid="G",
        run_id="R",
        window_id="w_apxi_on",
        start_tick=1,
        end_tick=1,
        profile=profile,
        aeon_window_id="AEON_W1",
        apxi_enabled=True,
        apxi_descriptors={"S_delta": (descriptor,)},
    )
    press_ctx.register_stream("S_delta", scheme_hint="ID")
    press_ctx.append("S_delta", 3)

    with pytest.raises(ValueError):
        press_ctx.close_window("w_apxi_on_manifest")
