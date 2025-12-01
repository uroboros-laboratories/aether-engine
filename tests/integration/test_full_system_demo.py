from __future__ import annotations

import json
from pathlib import Path

from core import run_gf01, serialize_gf01_run
from loom.chain import LoomBlockStore


SNAPSHOT_PATH = Path(__file__).parent.parent / "snapshots" / "gf01_run_snapshot.json"


def test_full_pipeline_persistence_and_replay(tmp_path):
    """Run GF-01, persist Loom blocks, and replay from disk for verification."""

    store = LoomBlockStore(tmp_path / "blocks")
    result = run_gf01(loom_block_store=store)

    snapshot = json.loads(SNAPSHOT_PATH.read_text())
    assert serialize_gf01_run(result) == snapshot

    index = store.replay_index()
    assert len(index["p"]) == len(result.p_blocks)
    assert len(index["i"]) == len(result.i_blocks)

    for tick, p_block in enumerate(result.p_blocks, start=1):
        payload, bin_hash = store.load_p_block_binary(tick)
        assert payload["tick"] == tick
        assert payload["C_t"] == p_block.C_t
        pointer = store.press_pointer("P", tick)
        assert pointer["binary_hash"] == bin_hash

    iblock_tick = result.i_blocks[-1].tick
    i_payload, i_bin_hash = store.load_i_block_binary(iblock_tick)
    assert i_payload["tick"] == iblock_tick
    assert i_payload["C_t"] == result.i_blocks[-1].C_t
    i_pointer = store.press_pointer("I", iblock_tick)
    assert i_pointer["binary_hash"] == i_bin_hash
