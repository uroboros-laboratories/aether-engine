import json

import pytest

from loom.chain import (
    LoomBlockStore,
    LoomChainRecorder,
    canonicalize_p_block,
    merkle_root,
)
from loom.loom import LoomIBlockV1, LoomPBlockV1, TopologyEdgeSnapshotV1
from loom.run_context import LoomRunContext
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.run_context import UMXRunContext
from umx.topology_profile import gf01_topology_profile


def _make_blocks():
    p_block = LoomPBlockV1(
        gid="g1",
        tick=1,
        seq=1,
        s_t=9,
        C_t=123,
        topology_version="v1",
        edge_flux_summary=[],
    )
    i_block = LoomIBlockV1(
        gid="g1",
        tick=2,
        W=2,
        C_t=456,
        profile_version="p1",
        topology_version="v1",
        post_u=[1, 2, 3],
        topology_snapshot=[
            TopologyEdgeSnapshotV1(e_id=1, i=0, j=1, k=0, cap=1, SC=0, c=0)
        ],
    )
    return p_block, i_block


def test_p_block_hash_is_deterministic():
    p_block, _ = _make_blocks()
    canonical_a = canonicalize_p_block(p_block, prev_hash=None)
    canonical_b = canonicalize_p_block(p_block, prev_hash=None)

    recorder_a = LoomChainRecorder()
    recorder_b = LoomChainRecorder()
    hash_a = recorder_a.record_p_block(p_block)
    hash_b = recorder_b.record_p_block(p_block)

    assert canonical_a == canonical_b
    assert hash_a == hash_b


def test_merkle_root_tracks_window_hashes():
    profile = ProfileCMP0V1(I_block_spacing_W=2)
    topo = gf01_topology_profile()
    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state([3, 1, 0, 0, 0, 0])

    recorder = LoomChainRecorder()
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx, recorder=recorder)
    _, _, i_blocks = loom_ctx.run_until(4)

    assert len(i_blocks) == 2

    window_hashes_first = recorder.p_hashes[:2]
    expected_root_first = merkle_root(window_hashes_first)
    assert recorder.i_blocks[i_blocks[0].tick] == expected_root_first

    window_hashes_second = recorder.p_hashes[-2:]
    expected_root_second = merkle_root(window_hashes_second)
    assert recorder.i_blocks[i_blocks[1].tick] == expected_root_second


def test_block_store_persists_and_prunes(tmp_path):
    profile = ProfileCMP0V1(I_block_spacing_W=2)
    topo = gf01_topology_profile()
    umx_ctx = UMXRunContext(topo=topo, profile=profile)
    umx_ctx.init_state([3, 1, 0, 0, 0, 0])

    store = LoomBlockStore(tmp_path, rollback_window=3)
    recorder = LoomChainRecorder(store=store)
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx, recorder=recorder)

    loom_ctx.run_until(6)

    index = store.replay_index()
    assert len(index["p"]) == 3  # rollback window keeps last three P-blocks
    assert {entry["tick"] for entry in index["p"]} == {4, 5, 6}

    # Verify persistence contains canonical payloads and hashes
    stored_p_block = store.load_p_block(6)
    assert stored_p_block["type"] == "P"
    assert stored_p_block["block"]["tick"] == 6
    assert "hash" in stored_p_block

    # I-blocks recorded every 2 ticks with pruning
    assert len(index["i"]) == 3
    assert {entry["tick"] for entry in index["i"]} == {2, 4, 6}

    stored_i_block = store.load_i_block(6)
    assert stored_i_block["type"] == "I"
    assert stored_i_block["block"]["merkle_root"] == recorder.i_blocks[6]
