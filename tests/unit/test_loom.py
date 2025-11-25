from loom.loom import compute_chain_value, compute_s_t
from loom.run_context import LoomRunContext
from umx.engine import step as umx_step
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.run_context import UMXRunContext
from umx.topology_profile import gf01_topology_profile, load_topology_profile


def test_cmp0_chain_rule_matches_formula():
    profile = ProfileCMP0V1()
    assert compute_chain_value(1_234_567, 9, 1, profile) == 20987847


def test_cmp0_s_t_uses_gf01_constant():
    profile = ProfileCMP0V1()
    dummy_ledger = umx_step(1, [3, 1, 0, 0, 0, 0], gf01_topology_profile(), profile)
    assert compute_s_t(dummy_ledger, profile) == 9


def test_cmp0_s_t_supports_sum_abs_flux_rule():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = ProfileCMP0V1(
        I_block_spacing_W=3,
        s_t_rule={"mode": "sum_abs_flux", "offset": 5, "scale": 1},
    )

    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state([7, 2, 0, 0])
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx)

    ledgers, p_blocks, i_blocks = loom_ctx.run_until(4)

    expected_s_t = [5 + sum(abs(edge.f_e) for edge in ledger.edges) for ledger in ledgers]
    assert [p_block.s_t for p_block in p_blocks] == expected_s_t
    assert all(i_block.W == profile.I_block_spacing_W for i_block in i_blocks)
    assert [i_block.tick for i_block in i_blocks] == [3]

    # Deterministic run with the derived s_t rule
    umx_ctx_2 = UMXRunContext(topo=topo, profile=profile)
    umx_ctx_2.init_state([7, 2, 0, 0])
    loom_ctx_2 = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx_2)
    _, p_blocks_2, i_blocks_2 = loom_ctx_2.run_until(4)

    assert [p.C_t for p in p_blocks] == [p.C_t for p in p_blocks_2]
    assert [p.s_t for p in p_blocks] == [p.s_t for p in p_blocks_2]
    assert i_blocks == i_blocks_2


def test_loom_run_context_reproduces_gf01_chain_and_iblock():
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state([3, 1, 0, 0, 0, 0])
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx)

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

    for _ in range(8):
        prev_chain = loom_ctx.current_chain_value()
        ledger, p_block, maybe_i_block = loom_ctx.step()

        assert p_block.C_t == loom_ctx.current_chain_value()
        assert p_block.seq == ledger.tick
        assert prev_chain != p_block.C_t

    assert [p_block.C_t for p_block in loom_ctx.p_blocks] == expected_chain
    assert all(p_block.s_t == 9 for p_block in loom_ctx.p_blocks)
    assert len(loom_ctx.i_blocks) == 1

    i_block = loom_ctx.i_blocks[0]
    assert i_block.tick == 8
    assert i_block.W == profile.I_block_spacing_W
    assert i_block.C_t == expected_chain[-1]
    assert i_block.profile_version == profile.name
    assert i_block.post_u == loom_ctx.ledgers[-1].post_u

    expected_snapshot = [
        (edge.e_id, edge.i, edge.j, edge.k, edge.cap, edge.SC, edge.c)
        for edge in topo.edges
    ]
    actual_snapshot = [
        (edge.e_id, edge.i, edge.j, edge.k, edge.cap, edge.SC, edge.c)
        for edge in i_block.topology_snapshot
    ]
    assert actual_snapshot == expected_snapshot


def test_loom_run_context_is_deterministic_on_line_graph():
    profile = gf01_profile_cmp0()
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    u0 = [5, 4, 3, 2]

    def _run_once():
        umx_ctx = UMXRunContext(topo=topo, profile=profile)
        umx_ctx.init_state(list(u0))
        loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx, W=2)
        ledgers, p_blocks, i_blocks = loom_ctx.run_until(4)
        return ledgers, p_blocks, i_blocks

    first_ledgers, first_p, first_i = _run_once()
    second_ledgers, second_p, second_i = _run_once()

    assert [ledger.post_u for ledger in first_ledgers] == [ledger.post_u for ledger in second_ledgers]
    assert [p_block.C_t for p_block in first_p] == [p_block.C_t for p_block in second_p]
    assert [p_block.seq for p_block in first_p] == [p_block.seq for p_block in second_p]
    assert first_p == second_p

    assert [i_block.tick for i_block in first_i] == [2, 4]
    assert first_i == second_i


def test_loom_chain_lookup_and_replay_matches_gf01_iblock():
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state([3, 1, 0, 0, 0, 0])
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx)

    ledgers, p_blocks, i_blocks = loom_ctx.run_until(8)

    assert loom_ctx.get_pblock(3) == p_blocks[2]
    assert loom_ctx.get_chain_at(8) == p_blocks[-1].C_t

    i_block = loom_ctx.get_iblock_for(8)
    assert i_block == i_blocks[0]
    assert loom_ctx.replay_state_at(8) == ledgers[-1].post_u


def test_loom_replay_reconstructs_state_from_iblocks():
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = ProfileCMP0V1(I_block_spacing_W=2)
    u0 = [5, 4, 3, 2]

    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state(list(u0))
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx)

    ledgers, _, _ = loom_ctx.run_until(5)

    for t in range(2, 6):
        assert loom_ctx.replay_state_at(t) == ledgers[t - 1].post_u
