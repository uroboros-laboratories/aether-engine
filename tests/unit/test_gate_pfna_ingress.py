from __future__ import annotations

import pytest

from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop
from gate import (
    PFNAIngressQueue,
    PFNAInputV0,
    PFNATransformV1,
    build_pfna_placeholder,
)
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile, load_topology_profile


def test_pfna_transform_integerizes_with_audit():
    transform = PFNATransformV1(scale=2.0, origin=1.0, clamp_min=-1, clamp_max=3)
    integerized, audit = transform.integerize([-2, 0.5, 1.2])

    assert integerized == (-1, 3, 3)
    assert [entry["rounded"] for entry in audit] == [-2, 3, 4]
    assert [entry["clamped"] for entry in audit] == [-1, 3, 3]


def test_pfna_ingress_queue_orders_and_deduplicates():
    queue = PFNAIngressQueue()
    pfna1 = PFNAInputV0(
        pfna_id="pfna_A",
        gid="G",
        run_id="R",
        tick=2,
        nid="N",
        values=(1,),
    )
    pfna2 = PFNAInputV0(
        pfna_id="pfna_B",
        gid="G",
        run_id="R",
        tick=1,
        nid="N",
        values=(2,),
    )
    duplicate = PFNAInputV0(
        pfna_id="pfna_A",
        gid="G",
        run_id="R",
        tick=2,
        nid="N",
        values=(999,),
    )

    queue.extend([pfna1, pfna2, duplicate])

    tick1 = queue.pop_ready(1)
    tick2 = queue.pop_ready(2)

    assert [event.pfna.pfna_id for event in tick1] == ["pfna_B"]
    assert [event.pfna.pfna_id for event in tick2] == ["pfna_A"]
    assert tick2[0].integerized == (1,)


def test_tick_loop_attaches_pfna_integerization_meta():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()
    window_spec = TickLoopWindowSpec(
        window_id="LINE_W1_ticks_1_2",
        apx_name="LINE_APX_v0_ticks_1_2",
        start_tick=1,
        end_tick=2,
    )

    pfna = build_pfna_placeholder(
        pfna_id="ext_seq_tick1",
        gid=topo.gid,
        run_id="LINE_PFNA",
        tick=1,
        nid="ext-source",
        values=[1, 0, 0, 0],
        description="scale by 2 then clamp",
    )

    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[1, 1, 1, 1],
        total_ticks=2,
        window_specs=[window_spec],
        primary_window_id=window_spec.window_id,
        run_id="LINE_PFNA",
        nid="engine-line",
        pfna_inputs=[pfna],
        pfna_transform=PFNATransformV1(scale=2.0),
    )

    first_scene = result.scenes[0]
    pfna_meta = first_scene.meta["pfna_integerization"]
    assert pfna_meta[0]["pfna_id"] == pfna.pfna_id
    assert pfna_meta[0]["values"] in ((2, 0, 0, 0), ())
    assert result.ledgers[0].pre_u[0] == 3  # initial 1 + integerized delta 2
