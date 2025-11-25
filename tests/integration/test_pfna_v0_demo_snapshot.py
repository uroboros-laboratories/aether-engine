from __future__ import annotations

import json
from pathlib import Path

from core import TickLoopWindowSpec, dumps_session_run, serialize_session_run
from gate import PressStreamSpecV1, SessionConfigV1, load_pfna_v0, run_session
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import load_topology_profile

SNAPSHOT_PATH = Path(__file__).parent.parent / "snapshots" / "pfna_v0_demo_snapshot.json"
PFNA_PATH = Path(__file__).parent.parent / "fixtures" / "pfna" / "pfna_v0_demo.json"


def _pfna_demo_config() -> SessionConfigV1:
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()

    window_spec = TickLoopWindowSpec(
        window_id="LINE_DEMO_W1_ticks_1_4",
        apx_name="LINE_APX_demo_ticks_1_4",
        start_tick=1,
        end_tick=4,
    )

    pfna_inputs = load_pfna_v0(PFNA_PATH, expected_length=topo.N)

    press_streams = (
        PressStreamSpecV1(
            name="S1_post_u_deltas", source="post_u_deltas", description="post_u delta per node"
        ),
        PressStreamSpecV1(name="S2_fluxes", source="fluxes", description="edge flux per edge"),
        PressStreamSpecV1(
            name="S3_prev_chain",
            source="prev_chain",
            description="prev chain checksum per tick",
        ),
    )

    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[2, 1, 0, 0],
        total_ticks=4,
        window_specs=(window_spec,),
        primary_window_id=window_spec.window_id,
        run_id="PFNA_DEMO_RUN",
        nid="pfna-demo-node",
        pfna_inputs=pfna_inputs,
        press_default_streams=press_streams,
    )


def test_pfna_demo_double_run_is_bytewise_identical():
    cfg = _pfna_demo_config()

    first_json = dumps_session_run(run_session(cfg))
    second_json = dumps_session_run(run_session(cfg))

    assert first_json == second_json


def test_pfna_demo_matches_snapshot():
    cfg = _pfna_demo_config()
    result = run_session(cfg)
    serialized = serialize_session_run(result)

    with SNAPSHOT_PATH.open("r", encoding="utf-8") as handle:
        snapshot = json.load(handle)

    assert serialized == snapshot
