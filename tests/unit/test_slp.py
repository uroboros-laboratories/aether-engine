from pathlib import Path

import pytest

from core.slp import SLPEventType, SLPEventV1, apply_slp_events
from umx.topology_profile import load_topology_profile


FIXTURE = Path("docs/fixtures/topologies/line_4_topology_profile.json")


def test_apply_slp_events_adds_nodes_edges_and_toggles_meta():
    topo = load_topology_profile(FIXTURE)

    events = [
        # Intentionally provided out of order to verify deterministic sorting by event_id
        SLPEventV1(
            event_id="b-add-edge",
            gid=topo.gid,
            tick_effective=1,
            op_type=SLPEventType.ADD_EDGE,
            payload={"e_id": 4, "i": 4, "j": 5, "k": 1, "cap": 64, "c": 1},
        ),
        SLPEventV1(
            event_id="c-update-edge",
            gid=topo.gid,
            tick_effective=1,
            op_type=SLPEventType.UPDATE_EDGE,
            payload={"e_id": 2, "j": 5, "c": 2},
        ),
        SLPEventV1(
            event_id="a-add-node",
            gid=topo.gid,
            tick_effective=1,
            op_type=SLPEventType.ADD_NODE,
            payload={"node_id": 5, "label": "n5"},
        ),
        SLPEventV1(
            event_id="d-disable-graph",
            gid=topo.gid,
            tick_effective=1,
            op_type=SLPEventType.GRAPH_DISABLE,
            payload={},
        ),
    ]

    mutated = apply_slp_events(topo, events)

    assert mutated.N == 5
    assert mutated.nodes[-1].label == "n5"
    assert len(mutated.edges) == 4
    assert mutated.edges[1].j == 5  # edge 2 targets the new node after update
    assert mutated.edges[-1].e_id == 4
    assert mutated.meta.get("enabled") is False


def test_apply_slp_events_rejects_invalid_operations():
    topo = load_topology_profile(FIXTURE)

    with pytest.raises(ValueError):
        apply_slp_events(
            topo,
            [
                SLPEventV1(
                    event_id="remove-node-2",
                    gid=topo.gid,
                    tick_effective=1,
                    op_type=SLPEventType.REMOVE_NODE,
                    payload={"node_id": 2},
                )
            ],
        )

    with pytest.raises(ValueError):
        apply_slp_events(
            topo,
            [
                SLPEventV1(
                    event_id="update-edge-invalid",
                    gid=topo.gid,
                    tick_effective=1,
                    op_type=SLPEventType.UPDATE_EDGE,
                    payload={"e_id": 1, "i": 99},
                )
            ],
        )

