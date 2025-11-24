"""Press/APX GF-01 tests for Issue 4."""
from __future__ import annotations

from press import PressWindowContextV1
from umx.engine import step as umx_step
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def _build_press_manifest(num_ticks: int, apx_name: str):
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    state = [3, 1, 0, 0, 0, 0]
    ctx = PressWindowContextV1(
        gid="GF01",
        run_id="run_0",
        window_id=apx_name,
        start_tick=1,
        end_tick=num_ticks,
        profile=profile,
    )

    ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
    ctx.register_stream("S2_fluxes", description="edge flux per edge")

    for tick in range(1, num_ticks + 1):
        ledger = umx_step(tick, state, topo, profile)
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        ctx.append("S1_post_u_deltas", deltas)
        ctx.append("S2_fluxes", fluxes)
        state = ledger.post_u

    manifest = ctx.close_window(apx_name)
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
