from __future__ import annotations

from dataclasses import replace

from core import run_gf01
from uledger import build_uledger_entries, hash_record


def test_uledger_hash_chain_is_stable():
    result = run_gf01()

    entry_hashes = [hash_record(entry) for entry in result.u_ledger_entries]
    expected_hashes = [
        "3e915909cc818dda52b1759902dcbc349074b48482e7a96dd3152bd9d8c13f08",
        "f423a5d9c2e04d718af9f91d15166fc6de24302b7ea4378c2f5b83ea22944124",
        "8a94d7e5f501264a85a0d54ee52828496d7ae328a9a620200c64b62b4d11db8c",
        "db860c7b5320adc0f18d05db0aadfac49d55baf1faeab8a0a683347f8f325d51",
        "94056e59637c5a50c528d3b64accd91ed66ea25ae7a20571970a958d62386705",
        "ac982a0e3c4d079679312bf028fcf855e7b0af907e4d4de235ca037e3260ddda",
        "99a02e4f8dee9a839be8f2bd1bfebefcfb12a20bb82d149111ec9ad5be5a0b24",
        "fa9ac51c0cb0880f63e3577382353323f28a29eb40321d8e0ae00225f6a885c4",
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
