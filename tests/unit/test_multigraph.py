from pathlib import Path

import pytest

from core.multigraph import (
    GraphRunConfigV1,
    MultiGraphRunConfigV1,
    MultiGraphRunContext,
    TopologyRegistry,
    load_multigraph_run_config,
)
from core.slp import SLPEventType, SLPEventV1


FIXTURES = Path("docs/fixtures")


def test_multigraph_config_rejects_duplicate_gids():
    graph = GraphRunConfigV1(
        gid="G1",
        topology_path="topologies/line_4_topology_profile.json",
        profile_path="profiles/profile_cmp1.json",
        initial_state=(1, 1, 1, 1),
        ticks=3,
    )
    with pytest.raises(ValueError):
        MultiGraphRunConfigV1(v=1, graphs=(graph, graph))


def test_registry_validates_profile_sc_mismatch():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp0.json",  # SC mismatch (32 vs 16)
                initial_state=(1, 1, 1, 1),
                ticks=2,
            ),
        ),
    )
    with pytest.raises(ValueError):
        TopologyRegistry.from_config(config, base_dir=FIXTURES)


def test_multigraph_context_steps_and_applies_slp():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp1.json",
                initial_state=(1, 2, 3, 4),
                ticks=3,
            ),
            GraphRunConfigV1(
                gid="RING5",
                topology_path="topologies/ring_5_topology_profile.json",
                profile_path="profiles/profile_cmp2.json",
                initial_state=(0, 0, 0, 0, 0),
                ticks=3,
            ),
        ),
    )
    registry = TopologyRegistry.from_config(config, base_dir=FIXTURES)
    ctx = MultiGraphRunContext(config, registry)

    first_step = ctx.step_all()
    assert ctx.tick == 1
    assert set(first_step.keys()) == {"LINE4", "RING5"}
    for umx_ctx, _loom_ctx in first_step.values():
        assert umx_ctx.tick == 1

    ctx.queue_slp_event(
        SLPEventV1(
            event_id="add-node-5",
            gid="LINE4",
            tick_effective=2,
            op_type=SLPEventType.ADD_NODE,
            payload={"node_id": 5},
        )
    )

    ctx.step_all()
    assert ctx.tick == 2
    updated_topo = ctx.registry.get_topology("LINE4")
    assert updated_topo.N == 5
    assert len(ctx.umx["LINE4"].state) == 5


def test_queue_rejects_events_for_past_tick():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp1.json",
                initial_state=(1, 2, 3, 4),
                ticks=3,
            ),
        ),
    )
    registry = TopologyRegistry.from_config(config, base_dir=FIXTURES)
    ctx = MultiGraphRunContext(config, registry)
    ctx.step_all()

    with pytest.raises(ValueError):
        ctx.queue_slp_event(
            SLPEventV1(
                event_id="late", gid="LINE4", tick_effective=1, op_type=SLPEventType.ADD_NODE, payload={"node_id": 5}
            )
        )


def test_scene_frames_emitted_from_last_tick():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp1.json",
                initial_state=(1, 2, 3, 4),
                ticks=3,
                run_id="RUN_A",
                nid="NODE_A",
                window_id="WIN_A",
            ),
        ),
    )
    registry = TopologyRegistry.from_config(config, base_dir=FIXTURES)
    ctx = MultiGraphRunContext(config, registry)
    ctx.step_all()

    frames = ctx.scene_frames_for_last_tick()
    assert set(frames.keys()) == {"LINE4"}
    scene = frames["LINE4"]
    assert scene.gid == "LINE4"
    assert scene.run_id == "RUN_A"
    assert scene.nid == "NODE_A"
    assert scene.window_id == "WIN_A"
    assert scene.tick == 1

    def custom_window(gid: str) -> str:
        return f"custom-{gid}"

    custom_frames = ctx.scene_frames_for_last_tick(window_id_factory=custom_window)
    assert custom_frames["LINE4"].window_id == "custom-LINE4"


def test_step_all_respects_schedule_hook_and_skip_set():
    config = MultiGraphRunConfigV1(
        v=1,
        graphs=(
            GraphRunConfigV1(
                gid="LINE4",
                topology_path="topologies/line_4_topology_profile.json",
                profile_path="profiles/profile_cmp1.json",
                initial_state=(1, 2, 3, 4),
                ticks=3,
            ),
            GraphRunConfigV1(
                gid="RING5",
                topology_path="topologies/ring_5_topology_profile.json",
                profile_path="profiles/profile_cmp2.json",
                initial_state=(0, 0, 0, 0, 0),
                ticks=3,
            ),
        ),
    )
    registry = TopologyRegistry.from_config(config, base_dir=FIXTURES)

    def schedule_hook(gid: str, tick: int) -> bool:
        return not (gid == "RING5" and tick == 1)

    ctx = MultiGraphRunContext(config, registry, schedule_hook=schedule_hook)

    first_step = ctx.step_all()
    assert ctx.tick == 1
    assert set(first_step.keys()) == {"LINE4"}
    assert ctx.umx["LINE4"].tick == 1
    assert ctx.umx["RING5"].tick == 0

    ctx.step_all(skip_gids=["LINE4"])
    assert ctx.tick == 2
    assert ctx.umx["LINE4"].tick == 1
    assert ctx.umx["RING5"].tick == 1


def test_load_multigraph_run_config(tmp_path: Path):
    config_path = tmp_path / "mg.json"
    config_path.write_text(
        """
        {
          "v": 1,
          "graphs": [
            {
              "gid": "G1",
              "topology_path": "topologies/line_4_topology_profile.json",
              "profile_path": "profiles/profile_cmp1.json",
              "initial_state": [1, 1, 1, 1],
              "ticks": 2
            }
          ]
        }
        """
    )
    config = load_multigraph_run_config(config_path)
    assert config.v == 1
    assert len(config.graphs) == 1
    assert config.graphs[0].gid == "G1"
