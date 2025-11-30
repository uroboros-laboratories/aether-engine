from __future__ import annotations

from dataclasses import replace

from core import run_gf01
from uledger import build_uledger_entries, hash_record


def test_uledger_hash_chain_is_stable():
    result = run_gf01()

    entry_hashes = [hash_record(entry) for entry in result.u_ledger_entries]
    expected_hashes = [
        "784b534cef972b1ce7363e767269c5598bf421120becc2480f4ff3ba72bce822",
        "ab66b5cb30a1708f8767ed08469aed21576cb0f05b15699e741acdacc0c410ba",
        "61462ea526d81d547b945eceede374b987cce7b98e33e66e585cabb15b54778f",
        "c9fbbe12b8e1b68a5378d05db36c537decf899be5fd1fb868a9ef30167d4cb7a",
        "f33f02af19a89e3fa1f674c843fc9c87affa080c81449bbc5bfa888dfa7b79bb",
        "be77e1ecd85b81cd9855f03f7e1ed85a681f6c6f02102d438edd344f65c25d4d",
        "a79d756811233fb10df9f4a9d7e6692eaf49a0a6910c7da0baa9654c8ec9bcb1",
        "243be9d8484c7223bd275e62f377d7d122ee7bbf41689743c9b0581d10a53306",
    ]

    assert entry_hashes == expected_hashes
    for idx, entry in enumerate(result.u_ledger_entries):
        if idx == 0:
            assert entry.prev_entry_hash is None
        else:
            assert entry.prev_entry_hash == expected_hashes[idx - 1]


def test_uledger_chain_changes_when_pillar_changes():
    baseline = run_gf01()
    baseline_hashes = [hash_record(entry) for entry in baseline.u_ledger_entries]

    mutated_ledgers = list(baseline.ledgers)
    mutated_ledgers[0] = replace(
        baseline.ledgers[0],
        sum_pre_u=5,
        sum_post_u=5,
        z_check=5,
        pre_u=[4, 1, 0, 0, 0, 0],
        post_u=[4, 1, 0, 0, 0, 0],
    )

    mutated_entries = build_uledger_entries(
        gid=baseline.topo.gid,
        run_id=baseline.run_id,
        window_id=baseline.scenes[0].window_id,
        ledgers=mutated_ledgers,
        p_blocks=baseline.p_blocks,
        envelopes=baseline.envelopes,
        manifest=baseline.manifests["GF01_APX_v0_full_window"],
    )

    mutated_hashes = [hash_record(entry) for entry in mutated_entries]
    assert mutated_hashes != baseline_hashes
    assert mutated_entries[0].prev_entry_hash is None
    assert mutated_entries[1].prev_entry_hash == mutated_hashes[0]
