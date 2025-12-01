import hashlib

from loom.chain import (
    LoomBlockStore,
    LoomChainRecorder,
    _HEADER_STRUCT,
    canonicalize_i_block,
    canonicalize_p_block,
    decode_i_block_binary,
    decode_p_block_binary,
    encode_i_block_binary,
    encode_p_block_binary,
)
from loom.loom import LoomIBlockV1, LoomPBlockV1, TopologyEdgeSnapshotV1


def _sample_blocks():
    p_block = LoomPBlockV1(
        gid="g-alpha",
        tick=7,
        seq=3,
        s_t=2,
        C_t=111,
        topology_version="v1",
        edge_flux_summary=[],
    )

    i_block = LoomIBlockV1(
        gid="g-alpha",
        tick=8,
        W=2,
        C_t=222,
        profile_version="p1",
        topology_version="v1",
        post_u=[0, 1, 2],
        topology_snapshot=[
            TopologyEdgeSnapshotV1(e_id=1, i=0, j=1, k=0, cap=5, SC=0, c=0),
            TopologyEdgeSnapshotV1(e_id=2, i=1, j=2, k=0, cap=6, SC=0, c=0),
        ],
    )

    return p_block, i_block


def test_binary_encoding_is_deterministic_round_trip():
    p_block, i_block = _sample_blocks()
    canonical_p = canonicalize_p_block(p_block, prev_hash="abc")
    blob_a = encode_p_block_binary(canonical_p)
    blob_b = encode_p_block_binary(canonical_p)

    assert blob_a == blob_b
    decoded_p, payload_hash = decode_p_block_binary(blob_a)
    assert decoded_p == canonical_p
    # hash is computed over the stored payload portion of the envelope
    payload = blob_a[_HEADER_STRUCT.size :]
    assert payload_hash == hashlib.sha256(payload).hexdigest()

    canonical_i = canonicalize_i_block(i_block, merkle_root="deadbeef", prev_hash="abc")
    blob_i = encode_i_block_binary(canonical_i)
    decoded_i, payload_hash_i = decode_i_block_binary(blob_i)
    assert decoded_i == canonical_i
    payload_i = blob_i[_HEADER_STRUCT.size :]
    assert payload_hash_i == hashlib.sha256(payload_i).hexdigest()


def test_block_store_writes_binary_and_press_pointers(tmp_path):
    p_block, i_block = _sample_blocks()

    store = LoomBlockStore(tmp_path)
    recorder = LoomChainRecorder(store=store)

    p_hash = recorder.record_p_block(p_block)
    recorder.record_i_block(i_block, window_hashes=[p_hash, p_hash])

    decoded_p, bin_hash = store.load_p_block_binary(p_block.tick)
    assert decoded_p["tick"] == p_block.tick
    assert store.load_p_block(p_block.tick)["block"] == decoded_p

    pointer_p = store.press_pointer("P", p_block.tick)
    assert pointer_p["binary_path"].endswith(".bin")
    assert pointer_p["binary_hash"] == bin_hash
    assert pointer_p["schema_version"] == 1
    assert pointer_p["compressed"] is True

    decoded_i, i_bin_hash = store.load_i_block_binary(i_block.tick)
    assert decoded_i == store.load_i_block(i_block.tick)["block"]
    pointer_i = store.press_pointer("I", i_block.tick)
    assert pointer_i["binary_hash"] == i_bin_hash
    assert pointer_i["binary_size"] > 0
