from __future__ import annotations

from dataclasses import replace

from core import run_gf01
from uledger import build_uledger_entries, hash_record


def test_uledger_hash_chain_is_stable():
    result = run_gf01()

    entry_hashes = [hash_record(entry) for entry in result.u_ledger_entries]
    expected_hashes = [
        "0a0f3072c6a987596e816d0119c022a9f1da036d3529970ff07851068aa71545",
        "00c9874ea2eab47066b3eb5ee1ac0cf376844d19ef5ae913163d6184622fcabc",
        "ddf8579ddd1eda45bcc09f86655bb9826795d7efdbbd041fad5c69c05b93678d",
        "c2df0be45d9dd7ffcb1d8f094d72d5b62202882303038e22c3d458b6f9cda0e4",
        "0b0b7782b0d9680d8d4e08be18e4e0c3289ee62fac8591ffe7e314d4f3877224",
        "c7bfa5ba76f22cb1559d7bb30bd36c761b36a4233e7679e2cb45872e60368bf5",
        "ec17b39c3c27aa71c4c9a46f8fe559dd8fd5754bb1e5ab12993824836e9326d3",
        "0eee650890304cb6ba163654bc827423e65106e2cfece814e98ef5e8ed4ffd0c",
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
