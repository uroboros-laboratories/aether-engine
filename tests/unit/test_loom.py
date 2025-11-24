from loom import compute_chain_value, compute_s_t, step
from umx.engine import step as umx_step
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def _run_gf01_chain():
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    state = [3, 1, 0, 0, 0, 0]
    C_prev = profile.C0
    ledgers = []
    p_blocks = []
    i_blocks = []
    for tick in range(1, 9):
        ledger = umx_step(tick, state, topo, profile)
        p_block, C_prev, i_block = step(ledger, C_prev, tick, topo, profile)
        state = ledger.post_u
        ledgers.append(ledger)
        p_blocks.append(p_block)
        if i_block:
            i_blocks.append(i_block)
    return profile, topo, ledgers, p_blocks, i_blocks


def test_cmp0_chain_rule_matches_formula():
    profile = ProfileCMP0V1()
    assert compute_chain_value(1_234_567, 9, 1, profile) == 20987847


def test_cmp0_s_t_uses_gf01_constant():
    profile = ProfileCMP0V1()
    dummy_ledger = umx_step(1, [3, 1, 0, 0, 0, 0], gf01_topology_profile(), profile)
    assert compute_s_t(dummy_ledger, profile) == 9


def test_gf01_chain_sequence_and_iblock_snapshot():
    profile, topo, ledgers, p_blocks, i_blocks = _run_gf01_chain()
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

    assert [p_block.C_t for p_block in p_blocks] == expected_chain
    assert all(p_block.s_t == 9 for p_block in p_blocks)
    assert len(i_blocks) == 1
    i_block = i_blocks[0]
    assert i_block.tick == 8
    assert i_block.W == profile.I_block_spacing_W
    assert i_block.C_t == expected_chain[-1]
    assert i_block.profile_version == profile.name
    assert i_block.post_u == ledgers[-1].post_u

    expected_snapshot = [
        (edge.e_id, edge.i, edge.j, edge.k, edge.cap, edge.SC, edge.c)
        for edge in topo.edges
    ]
    actual_snapshot = [
        (edge.e_id, edge.i, edge.j, edge.k, edge.cap, edge.SC, edge.c)
        for edge in i_block.topology_snapshot
    ]
    assert actual_snapshot == expected_snapshot
