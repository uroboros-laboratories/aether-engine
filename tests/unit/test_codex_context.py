from __future__ import annotations

from codex import CodexContext
from core import run_gf01
from gate import NAPEnvelopeV1
from loom.loom import LoomPBlockV1
from press import APXManifestV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1


def _make_dummy_ledger(tick: int) -> UMXTickLedgerV1:
    edges = [
        EdgeFluxV1(e_id=1, i=1, j=2, du=1, raw=1, cap=10, f_e=1),
        EdgeFluxV1(e_id=2, i=2, j=3, du=-1, raw=-1, cap=10, f_e=-1),
    ]
    return UMXTickLedgerV1(
        tick=tick,
        sum_pre_u=0,
        sum_post_u=0,
        z_check=0,
        pre_u=[0, 0, 0],
        edges=edges,
        post_u=[0, 0, 0],
    )


def _make_dummy_p_block(tick: int) -> LoomPBlockV1:
    return LoomPBlockV1(tick=tick, seq=tick, s_t=1, C_t=tick, edge_flux_summary=[])


def _make_custom_ledger(tick: int, du1: int, du2: int) -> UMXTickLedgerV1:
    edges = [
        EdgeFluxV1(e_id=1, i=1, j=2, du=du1, raw=du1, cap=10, f_e=du1),
        EdgeFluxV1(e_id=2, i=2, j=3, du=du2, raw=du2, cap=10, f_e=du2),
    ]
    return UMXTickLedgerV1(
        tick=tick,
        sum_pre_u=0,
        sum_post_u=0,
        z_check=0,
        pre_u=[0, 0, 0],
        edges=edges,
        post_u=[0, 0, 0],
    )


def test_codex_ingests_gf01_and_counts_patterns() -> None:
    result = run_gf01()
    ctx = CodexContext(library_id="CE_MAIN")

    ctx.ingest(
        gid=result.topo.gid,
        run_id=result.run_id,
        ledgers=result.ledgers,
        p_blocks=result.p_blocks,
        i_blocks=result.i_blocks,
        manifests=result.manifests.values(),
        envelopes=result.envelopes,
    )

    stats = ctx.runtime_stats
    assert stats.total_ticks == len(result.ledgers)
    assert stats.total_p_blocks == len(result.p_blocks)
    assert stats.total_i_blocks == len(result.i_blocks)
    assert stats.total_manifests == len(result.manifests)
    assert stats.total_envelopes == len(result.envelopes)

    ordered_edges = tuple(sorted(result.ledgers[0].edges, key=lambda edge: edge.e_id))
    expected_signature = (
        tuple(edge.du for edge in ordered_edges),
        tuple(edge.f_e for edge in ordered_edges),
    )
    assert stats.ledger_pattern_counts[expected_signature] == len(result.ledgers)

    for edge in ordered_edges:
        assert stats.edge_pattern_counts[(edge.e_id, edge.du, edge.f_e)] == len(
            result.ledgers
        )


def test_ingest_rejects_mismatched_sequences() -> None:
    ledger = _make_dummy_ledger(tick=1)
    p_block = _make_dummy_p_block(tick=2)
    ctx = CodexContext(library_id="CE_MAIN")

    try:
        ctx.ingest(
            gid="G1",
            run_id="R1",
            ledgers=[ledger],
            p_blocks=[p_block],
            i_blocks=[],
            manifests=[
                APXManifestV1(apx_name="A1", profile="CMP-0", manifest_check=1, streams=[])
            ],
        )
    except ValueError as err:
        assert "ticks must align" in str(err)
    else:
        raise AssertionError("Expected ValueError for misaligned ticks")


def test_ingest_counts_patterns_across_ticks() -> None:
    ledger1 = _make_dummy_ledger(tick=1)
    ledger2 = _make_dummy_ledger(tick=2)
    ctx = CodexContext(library_id="CE_MAIN")

    ctx.ingest(
        gid="G1",
        run_id="R1",
        ledgers=[ledger1, ledger2],
        p_blocks=[_make_dummy_p_block(1), _make_dummy_p_block(2)],
        i_blocks=[],
        manifests=[
            APXManifestV1(apx_name="A1", profile="CMP-0", manifest_check=1, streams=[])
        ],
    )

    stats = ctx.runtime_stats
    assert stats.total_ticks == 2
    assert stats.edge_pattern_counts[(1, 1, 1)] == 2
    assert stats.edge_pattern_counts[(2, -1, -1)] == 2


def test_codex_learns_edge_flux_motif_from_gf01() -> None:
    result = run_gf01()
    ctx = CodexContext(library_id="CE_MAIN")

    ctx.ingest(
        gid=result.topo.gid,
        run_id=result.run_id,
        ledgers=result.ledgers,
        p_blocks=result.p_blocks,
        i_blocks=result.i_blocks,
        manifests=result.manifests.values(),
        envelopes=result.envelopes,
    )

    motifs = ctx.learn_edge_flux_motifs()
    assert len(motifs) == 1

    motif = motifs[0]
    ordered_edges = tuple(sorted(result.ledgers[0].edges, key=lambda edge: edge.e_id))
    expected_du = [edge.du for edge in ordered_edges]
    expected_fe = [edge.f_e for edge in ordered_edges]

    assert motif.pattern_descriptor == {
        "type": "edge_flux_pattern_v1",
        "edge_ids": [edge.e_id for edge in ordered_edges],
        "du_signature": expected_du,
        "f_e_signature": expected_fe,
    }
    assert motif.usage_stats["usage_count"] == len(result.ledgers)
    assert motif.created_at_tick == result.ledgers[0].tick
    assert motif.last_updated_tick == result.ledgers[-1].tick
    assert motif.source_window_id == f"{result.topo.gid}_ticks_{result.ledgers[0].tick}_{result.ledgers[-1].tick}"


def test_motif_learning_is_repeatable_and_thresholded() -> None:
    ledger_a1 = _make_custom_ledger(tick=1, du1=1, du2=-1)
    ledger_b = _make_custom_ledger(tick=2, du1=2, du2=-2)
    ledger_a2 = _make_custom_ledger(tick=3, du1=1, du2=-1)

    ctx = CodexContext(library_id="CE_MAIN")
    ctx.ingest(
        gid="G_SYNTH",
        run_id="R_SYNTH",
        ledgers=[ledger_a1, ledger_b, ledger_a2],
        p_blocks=[_make_dummy_p_block(1), _make_dummy_p_block(2), _make_dummy_p_block(3)],
        i_blocks=[],
        manifests=[],
        envelopes=[],
    )

    motifs = ctx.learn_edge_flux_motifs(threshold=2)
    assert len(motifs) == 1

    motif = motifs[0]
    assert motif.pattern_descriptor["du_signature"] == [1, -1]
    assert motif.usage_stats["usage_count"] == 2
    assert motif.created_at_tick == 1
    assert motif.last_updated_tick == 3

    ctx_replay = CodexContext(library_id="CE_MAIN")
    ctx_replay.ingest(
        gid="G_SYNTH",
        run_id="R_SYNTH",
        ledgers=[ledger_a1, ledger_b, ledger_a2],
        p_blocks=[_make_dummy_p_block(1), _make_dummy_p_block(2), _make_dummy_p_block(3)],
        i_blocks=[],
        manifests=[],
        envelopes=[],
    )
    motifs_repeat = ctx_replay.learn_edge_flux_motifs(threshold=2)

    assert len(motifs_repeat) == 1
    repeat = motifs_repeat[0]
    assert repeat.pattern_descriptor == motif.pattern_descriptor
    assert repeat.mdl_stats == motif.mdl_stats


def test_codex_emits_proposals_from_learned_motifs() -> None:
    result = run_gf01()
    ctx = CodexContext(library_id="CE_MAIN")

    ctx.ingest(
        gid=result.topo.gid,
        run_id=result.run_id,
        ledgers=result.ledgers,
        p_blocks=result.p_blocks,
        i_blocks=result.i_blocks,
        manifests=result.manifests.values(),
        envelopes=result.envelopes,
    )

    motifs = ctx.learn_edge_flux_motifs()
    proposals = ctx.emit_proposals(usage_threshold=1)

    assert len(motifs) == 1
    assert len(proposals) == 1

    proposal = proposals[0]
    motif = motifs[0]

    assert proposal.motif_id == motif.motif_id
    assert proposal.target_window_id == motif.source_window_id
    assert proposal.status == "PENDING"
    assert proposal.action == "PLACE"
    assert proposal.target_location["edge_ids"] == motif.pattern_descriptor["edge_ids"]
    assert proposal.expected_effect["delta_L_total"] == motif.mdl_stats["delta_vs_baseline"]
    assert ctx.proposals == proposals


def test_proposal_emission_is_repeatable_and_thresholded() -> None:
    ledger_a1 = _make_custom_ledger(tick=1, du1=1, du2=-1)
    ledger_b = _make_custom_ledger(tick=2, du1=2, du2=-2)
    ledger_a2 = _make_custom_ledger(tick=3, du1=1, du2=-1)

    ctx = CodexContext(library_id="CE_MAIN")
    ctx.ingest(
        gid="G_SYNTH",
        run_id="R_SYNTH",
        ledgers=[ledger_a1, ledger_b, ledger_a2],
        p_blocks=[_make_dummy_p_block(1), _make_dummy_p_block(2), _make_dummy_p_block(3)],
        i_blocks=[],
        manifests=[],
        envelopes=[],
    )

    ctx.learn_edge_flux_motifs(threshold=2)
    proposals = ctx.emit_proposals(usage_threshold=2)
    assert len(proposals) == 1

    replay_ctx = CodexContext(library_id="CE_MAIN")
    replay_ctx.ingest(
        gid="G_SYNTH",
        run_id="R_SYNTH",
        ledgers=[ledger_a1, ledger_b, ledger_a2],
        p_blocks=[_make_dummy_p_block(1), _make_dummy_p_block(2), _make_dummy_p_block(3)],
        i_blocks=[],
        manifests=[],
        envelopes=[],
    )
    replay_ctx.learn_edge_flux_motifs(threshold=2)
    replay_proposals = replay_ctx.emit_proposals(usage_threshold=2)

    assert len(replay_proposals) == 1
    assert replay_proposals[0].proposal_id == proposals[0].proposal_id
    assert replay_proposals[0].target_location == proposals[0].target_location
    assert replay_proposals[0].expected_effect == proposals[0].expected_effect

