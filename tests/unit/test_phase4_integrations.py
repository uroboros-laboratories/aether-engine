from pathlib import Path

import pytest

from core.multigraph import GraphRunConfigV1, MultiGraphRunConfigV1, MultiGraphRunContext, TopologyRegistry
from core.slp import SLPEventType, SLPEventV1
from codex.context import CodexContext
from config.schemas import load_profile_config
from gate import build_scene_frame, emit_nap_envelope
from loom.run_context import LoomRunContext
from press.press import PressWindowContextV1
from uledger.entry import build_uledger_entries
from umx.run_context import UMXRunContext
from umx.topology_profile import TopologyProfileV1, load_topology_profile

FIXTURES = Path("docs/fixtures")


def _line4_topology_with_version():
    topo = load_topology_profile(FIXTURES / "topologies/line_4_topology_profile.json")
    return TopologyProfileV1(
        gid=topo.gid,
        profile=topo.profile,
        N=topo.N,
        nodes=topo.nodes,
        edges=topo.edges,
        SC=topo.SC,
        meta={"version": "v-test", **topo.meta},
    )


def test_loom_blocks_include_gid_and_topology_version():
    topo = _line4_topology_with_version()
    profile = load_profile_config(FIXTURES / "profiles/profile_cmp1.json")
    umx = UMXRunContext(topo=topo, profile=profile, gid=topo.gid, run_id="run-loom")
    umx.init_state([1, 2, 3, 4])
    loom = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx, W=2)

    ledger, p_block, i_block = loom.step()
    assert p_block.gid == topo.gid
    assert p_block.topology_version == "v-test"
    assert i_block is None

    ledger, p_block, i_block = loom.step()
    assert i_block is not None
    assert i_block.gid == topo.gid
    assert i_block.topology_version == "v-test"


def test_nap_envelope_carries_slp_context():
    topo = load_topology_profile(FIXTURES / "topologies/line_4_topology_profile.json")
    profile = load_profile_config(FIXTURES / "profiles/profile_cmp1.json")
    umx = UMXRunContext(topo=topo, profile=profile, gid="GID1", run_id="RUN1")
    umx.init_state([1, 1, 1, 1])
    ledger = umx.step()
    scene = build_scene_frame(
        gid="GID1",
        run_id="RUN1",
        nid="NODE1",
        ledger=ledger,
        C_prev=0,
        C_t=0,
        window_id="WIN1",
        manifest_check=7,
    )
    envelope = emit_nap_envelope(scene, profile, slp_event_ids=["evt-a", "evt-b"])
    assert envelope.slp_event_ids == ("evt-a", "evt-b")


def test_codex_slp_motifs_and_uledger_refs():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp1.json",
                initial_state=(1, 1, 1, 1),
                ticks=2,
                run_id="RUN-CX",
                nid="NODE-CX",
                window_id="WIN-CX",
            ),
        ),
    )
    registry = TopologyRegistry.from_config(config, base_dir=FIXTURES)
    ctx = MultiGraphRunContext(config, registry)
    disable_event = SLPEventV1(
        event_id="disable",
        gid="LINE4",
        tick_effective=2,
        op_type=SLPEventType.GRAPH_DISABLE,
        meta={"reason": "test"},
    )
    ctx.queue_slp_event(disable_event)

    ctx.step_all()
    ctx.step_all()
    results = ctx.last_tick_results()
    tick_result = results["LINE4"]

    window = PressWindowContextV1(
        gid="LINE4",
        run_id="RUN-CX",
        window_id="WIN-CX",
        start_tick=tick_result.ledger.tick,
        end_tick=tick_result.ledger.tick,
        profile=registry.get_profile("LINE4"),
    )
    window.register_stream("u", description="state")
    window.append("u", tick_result.ledger.post_u, tick=tick_result.ledger.tick)
    manifest = window.close_window(apx_name="APX-CX")

    scene = build_scene_frame(
        gid="LINE4",
        run_id="RUN-CX",
        nid="NODE-CX",
        ledger=tick_result.ledger,
        C_prev=tick_result.C_prev,
        C_t=tick_result.p_block.C_t,
        window_id="WIN-CX",
        manifest_check=manifest.manifest_check,
    )
    envelope = emit_nap_envelope(
        scene,
        registry.get_profile("LINE4"),
        seq=tick_result.p_block.seq,
        payload_ref=manifest.manifest_check,
        slp_event_ids=[disable_event.event_id],
    )

    entries = build_uledger_entries(
        gid="LINE4",
        run_id="RUN-CX",
        window_id="WIN-CX",
        ledgers=[tick_result.ledger],
        p_blocks=[tick_result.p_block],
        envelopes=[envelope],
        manifest=manifest,
        slp_events_by_tick={tick_result.ledger.tick: [disable_event.event_id]},
    )
    assert entries[0].slp_event_refs == (disable_event.event_id,)
    assert entries[0].topology_version == tick_result.p_block.topology_version

    codex = CodexContext(library_id="LIB-CX")
    codex.ingest(
        gid="LINE4",
        run_id="RUN-CX",
        ledgers=[tick_result.ledger],
        p_blocks=[tick_result.p_block],
        window_id="WIN-CX",
        slp_events=[disable_event],
    )
    motifs = codex.learn_slp_event_motifs()
    assert motifs
    assert motifs[0].pattern_descriptor["op_types"] == ["GRAPH_DISABLE"]
    assert motifs[0].source_gid == "LINE4"
