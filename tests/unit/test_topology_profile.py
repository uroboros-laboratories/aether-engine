"""Tests for CMP-0 topology and profile helpers."""
from umx import (
    EdgeProfileV1,
    NodeProfileV1,
    ProfileCMP0V1,
    TopologyProfileV1,
    gf01_profile_cmp0,
    gf01_topology_profile,
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
