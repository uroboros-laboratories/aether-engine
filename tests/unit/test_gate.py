from __future__ import annotations

from gate import build_scene_and_envelope
from loom.loom import step as loom_step
from press import PressWindowContextV1
from umx.engine import step as umx_step
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def test_gf01_nap_envelopes_match_contract_values():
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    state = [3, 1, 0, 0, 0, 0]
    gid = "GF01"
    run_id = "GF01"
    window_id = "GF01_W1_ticks_1_8"

    press_ctx = PressWindowContextV1(
        gid=gid,
        run_id=run_id,
        window_id=window_id,
        start_tick=1,
        end_tick=8,
        profile=profile,
    )
    press_ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
    press_ctx.register_stream("S2_fluxes", description="edge flux per edge")

    tick_outputs = []
    C_prev = profile.C0
    for tick in range(1, 9):
        ledger = umx_step(tick, state, topo, profile)
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        press_ctx.append("S1_post_u_deltas", deltas)
        press_ctx.append("S2_fluxes", fluxes)

        prev_for_scene = C_prev
        p_block, C_prev, _ = loom_step(ledger, C_prev, tick, topo, profile)
        tick_outputs.append((ledger, p_block, prev_for_scene))
        state = ledger.post_u

    manifest = press_ctx.close_window("GF01_APX_v0_full_window")
    assert manifest.manifest_check == 487809945

    scenes_and_envelopes = [
        build_scene_and_envelope(
            gid=gid,
            run_id=run_id,
            nid="N/A",
            window_id=window_id,
            ledger=ledger,
            p_block=p_block,
            C_prev=C_prev_tick,
            manifest_check=manifest.manifest_check,
            profile=profile,
        )
        for (ledger, p_block, C_prev_tick) in tick_outputs
    ]

    envelopes = [env for (_, env) in scenes_and_envelopes]
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

    assert all(env.v == 1 for env in envelopes)
    assert all(env.gid == gid for env in envelopes)
    assert all(env.nid == "N/A" for env in envelopes)
    assert all(env.layer == "DATA" for env in envelopes)
    assert all(env.mode == "P" for env in envelopes)
    assert all(env.payload_ref == 487809945 for env in envelopes)
    assert [env.seq for env in envelopes] == list(range(1, 9))
    assert [env.tick for env in envelopes] == list(range(1, 9))
    assert [env.prev_chain for env in envelopes] == expected_prev_chain
