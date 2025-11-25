"""Tests for CMP-0 topology and profile helpers."""
from umx import (
    EdgeProfileV1,
    NodeProfileV1,
    ProfileCMP0V1,
    TopologyProfileV1,
    gf01_profile_cmp0,
    gf01_topology_profile,
    load_topology_profile,
    topology_profile_from_dict,
)


def test_gf01_topology_structure():
    topo = gf01_topology_profile()

    assert topo.gid == "GF01"
    assert topo.profile == "CMP-0"
    assert topo.N == 6
    assert [node.node_id for node in topo.nodes] == list(range(1, 7))

    expected_edges = [
        (1, 1, 2, 1),
        (2, 1, 4, 2),
        (3, 1, 6, 1),
        (4, 2, 3, 1),
        (5, 2, 5, 2),
        (6, 3, 4, 1),
        (7, 4, 5, 1),
        (8, 5, 6, 1),
    ]
    assert [(e.e_id, e.i, e.j, e.k) for e in topo.edges] == expected_edges
    assert all(isinstance(edge.cap, int) and edge.cap > 0 for edge in topo.edges)
    assert all(edge.SC == topo.SC for edge in topo.edges)
    assert all(edge.c == 0 for edge in topo.edges)

    # Deterministic construction
    assert topo == gf01_topology_profile()


def test_topology_invariants():
    # Valid topology should not raise
    topo = TopologyProfileV1(
        gid="TEST",
        profile="CMP-0",
        N=2,
        nodes=[NodeProfileV1(node_id=1), NodeProfileV1(node_id=2)],
        edges=[
            EdgeProfileV1(e_id=1, i=1, j=2, k=1, cap=10, SC=32, c=0),
        ],
        SC=32,
    )
    assert topo.N == 2


def test_load_gf01_topology_from_fixture():
    topo = load_topology_profile("docs/fixtures/topologies/gf01_topology_profile.json")

    assert topo == gf01_topology_profile()


def test_load_additional_topologies():
    line_topology = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    assert line_topology.N == 4
    assert [edge.e_id for edge in line_topology.edges] == [1, 2, 3]
    assert line_topology.meta.get("description") == "Four-node line topology"

    ring_topology = load_topology_profile("docs/fixtures/topologies/ring_5_topology_profile.json")
    assert ring_topology.N == 5
    assert ring_topology.edges[0].SC == ring_topology.SC
    assert ring_topology.edges[-1].j == 5

    star_topology = load_topology_profile("docs/fixtures/topologies/star_5_topology_profile.json")
    assert star_topology.N == 5
    assert star_topology.edges[0].i == 1
    assert all(edge.i == 1 for edge in star_topology.edges)


def test_rejects_invalid_profiles():
    # Non-contiguous nodes
    invalid_nodes = {
        "gid": "TEST",
        "profile": "CMP-0",
        "N": 3,
        "nodes": [
            {"node_id": 1},
            {"node_id": 3},
        ],
        "edges": [],
        "SC": 8,
    }
    try:
        topology_profile_from_dict(invalid_nodes)
        assert False, "Expected ValueError for missing node 2"
    except ValueError as exc:
        assert "Nodes must be contiguous" in str(exc)

    # Edge references out of range
    invalid_edges = {
        "gid": "TEST",
        "profile": "CMP-0",
        "N": 2,
        "nodes": [
            {"node_id": 1},
            {"node_id": 2},
        ],
        "edges": [
            {"e_id": 1, "i": 1, "j": 3, "k": 1, "cap": 10, "SC": 8, "c": 0},
        ],
        "SC": 8,
    }
    try:
        topology_profile_from_dict(invalid_edges)
        assert False, "Expected ValueError for j out of range"
    except ValueError as exc:
        assert "Edge endpoints" in str(exc)

    # Non-integer k
    invalid_k = {
        "gid": "TEST",
        "profile": "CMP-0",
        "N": 2,
        "nodes": [
            {"node_id": 1},
            {"node_id": 2},
        ],
        "edges": [
            {"e_id": 1, "i": 1, "j": 2, "k": 1.5, "cap": 10, "SC": 8, "c": 0},
        ],
        "SC": 8,
    }
    try:
        topology_profile_from_dict(invalid_k)
        assert False, "Expected ValueError for non-integer k"
    except ValueError as exc:
        assert "edge.k must be an integer" in str(exc)


def test_gf01_profile_constants():
    profile = gf01_profile_cmp0()

    assert isinstance(profile, ProfileCMP0V1)
    assert profile.name == "CMP-0"
    assert profile.modulus_M == 1_000_000_007
    assert profile.C0 == 1_234_567
    assert profile.SC == 32
    assert profile.I_block_spacing_W == 8
    assert profile.s_t_rule.get("gf01_constant") == 9
    assert profile.flux_rule.get("type") == "CMP0_flux_v1"
    assert profile.chain_rule.get("type") == "CMP0_chain_v1"
    assert profile.nap_defaults.get("mode") == "P"
    assert "S1_post_u_deltas" in profile.press_defaults.get("gf01_streams", [])

    # Deterministic construction
    assert profile == gf01_profile_cmp0()
