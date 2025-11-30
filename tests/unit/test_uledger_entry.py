from __future__ import annotations

from dataclasses import replace

from core import run_gf01
from uledger import build_uledger_entries, hash_record


def test_uledger_hash_chain_is_stable():
    result = run_gf01()

    entry_hashes = [hash_record(entry) for entry in result.u_ledger_entries]
    expected_hashes = [
        "ee62bad190fa264e3eab1c00b605dd0c0a9f4083fcea2166233f12923ba98f18",
        "540ed3a0be3affcd641a485ee398475b2bfbefd3dc3e8e9bd42306a19debb918",
        "07b9c88e1339ba4a78da9f9b1cc301b6b7de83fe31cc422525157e5d1a779771",
        "7597d15a832fd98a62653cb1c04b0b131651ebcd2d5620c2e7049b2f428ea2ef",
        "b65ae7880d750ac7422062064216b1480a413e63d74e31716ecf21748a974197",
        "eeddb1034591cd1eba82a6f191877e7b2088481d725164e9d54c93f67df90259",
        "988936a76b69fa711fe065b11a4ccd2b86bf760a6b20fbb953703a97668ad2ba",
        "f8028061e0ac9a66d1a70cba95ef47c89a9b9dda912b6fee92a5df36deb81656",
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


def test_uledger_includes_governance_meta_when_provided():
    baseline = run_gf01()

    entries_with_meta = build_uledger_entries(
        gid=baseline.topo.gid,
        run_id=baseline.run_id,
        window_id=baseline.scenes[0].window_id,
        ledgers=baseline.ledgers,
        p_blocks=baseline.p_blocks,
        envelopes=baseline.envelopes,
        manifest=baseline.manifests["GF01_APX_v0_full_window"],
        governance_meta={"governance_budget": {"caps": [], "proposals_seen": 0}},
    )

    assert entries_with_meta[0].meta.get("governance_budget") == {
        "caps": [],
        "proposals_seen": 0,
    }
