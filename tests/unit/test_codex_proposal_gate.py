from __future__ import annotations

from codex import CodexContext, CodexProposalGatePolicyV1
from loom.loom import LoomPBlockV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1


def _ledger_and_pblock(tick: int = 1) -> tuple[UMXTickLedgerV1, LoomPBlockV1]:
    ledger = UMXTickLedgerV1(
        tick=tick,
        sum_pre_u=2,
        sum_post_u=2,
        z_check=2,
        pre_u=[1, 1],
        post_u=[1, 1],
        edges=[EdgeFluxV1(e_id=1, i=0, j=1, du=0, raw=0, cap=10, f_e=0)],
    )
    p_block = LoomPBlockV1(
        gid="G",
        tick=tick,
        seq=tick,
        s_t=9,
        C_t=0,
    )
    return ledger, p_block


def test_emit_proposals_records_structural_ledger():
    context = CodexContext(library_id="LIB1")
    ledger, p_block = _ledger_and_pblock()
    context.ingest(gid="G", run_id="R1", ledgers=[ledger], p_blocks=[p_block])

    context.learn_edge_flux_motifs(threshold=1)
    proposals = context.emit_proposals(usage_threshold=1)

    assert len(proposals) == 1
    assert len(context.structural_ledger) == 1
    entry = context.structural_ledger[0]
    assert entry.state == "PROPOSE"
    assert entry.decision == "PENDING"
    assert entry.entry_hash
    assert entry.prev_hash == ""


def test_evaluate_proposals_accepts_and_commits_when_policy_passes():
    context = CodexContext(library_id="LIB1")
    ledger, p_block = _ledger_and_pblock()
    context.ingest(gid="G", run_id="R1", ledgers=[ledger], p_blocks=[p_block])
    context.learn_edge_flux_motifs(threshold=1)
    proposals = context.emit_proposals(usage_threshold=1)

    policy = CodexProposalGatePolicyV1(min_delta_L_total=0.5, min_fidelity=0.5)
    decisions = context.evaluate_proposals(policy=policy, fidelity_scores={proposals[0].proposal_id: 0.9})

    assert proposals[0].status == "ACCEPTED"
    assert proposals[0].governance_status == "OK"
    assert len(context.structural_ledger) == 3
    propose_entry, review_entry, commit_entry = context.structural_ledger
    assert review_entry.prev_hash == propose_entry.entry_hash
    assert commit_entry.prev_hash == review_entry.entry_hash
    assert commit_entry in decisions


def test_evaluate_proposals_rejects_when_policy_fails():
    context = CodexContext(library_id="LIB1")
    ledger, p_block = _ledger_and_pblock()
    context.ingest(gid="G", run_id="R1", ledgers=[ledger], p_blocks=[p_block])
    context.learn_edge_flux_motifs(threshold=1)
    proposals = context.emit_proposals(usage_threshold=1)

    policy = CodexProposalGatePolicyV1(min_delta_L_total=5.0, min_fidelity=1.0)
    decisions = context.evaluate_proposals(policy=policy, fidelity_scores={proposals[0].proposal_id: 0.2})

    assert proposals[0].status == "REJECTED"
    assert proposals[0].governance_status == "HARD_FAIL"
    assert proposals[0].violated_policies == ("delta_L_total", "fidelity")
    assert len(context.structural_ledger) == 2
    propose_entry, review_entry = context.structural_ledger
    assert review_entry.prev_hash == propose_entry.entry_hash
    assert decisions[0] == review_entry
