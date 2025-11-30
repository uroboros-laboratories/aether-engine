from __future__ import annotations

from codex import CodexContext
from core import run_gf01
from gate import NAPEnvelopeV1, PressStreamSpecV1, SessionConfigV1, run_session
from core.tick_loop import TickLoopWindowSpec
from loom.loom import LoomPBlockV1
from press import APXManifestV1
from press.aeon import AEONDerivedWindowV1, AEONWindowDefV1, AEONWindowGrammarV1
from press.apxi import APXiDescriptorV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import load_topology_profile


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
    return LoomPBlockV1(
        gid="G_SYNTH",
        tick=tick,
        seq=tick,
        s_t=1,
        C_t=tick,
        topology_version="test", 
        edge_flux_summary=[],
    )


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


def _demo_aeon_grammar() -> AEONWindowGrammarV1:
    base_first = AEONWindowDefV1(
        window_id="AEON_LINE4_W1_ticks_1_3",
        tick_start=1,
        tick_end=3,
        labels=("demo", "first-half"),
        press_window_id=None,
    )
    base_second = AEONWindowDefV1(
        window_id="AEON_LINE4_W2_ticks_4_6",
        tick_start=4,
        tick_end=6,
        labels=("demo", "second-half"),
        press_window_id=None,
    )
    derived_all = AEONDerivedWindowV1(
        window_id="AEON_LINE4_W_all",
        source_ids=(base_first.window_id, base_second.window_id),
        aggregation="concat",
        labels=("demo", "aggregate"),
        press_window_id="LINE4_APX_W1_T1_6",
    )
    return AEONWindowGrammarV1(
        base_windows={base_first.window_id: base_first, base_second.window_id: base_second},
        derived_windows={derived_all.window_id: derived_all},
    )


def _demo_streams() -> tuple[PressStreamSpecV1, ...]:
    return (
        PressStreamSpecV1(name="S1_post_u_deltas", source="post_u_deltas", description="post_u delta per node"),
        PressStreamSpecV1(name="S2_fluxes", source="fluxes", description="edge flux per edge"),
        PressStreamSpecV1(
            name="S3_prev_chain",
            source="prev_chain",
            description="prev chain checksum per tick",
        ),
    )


def _demo_descriptors() -> dict[str, tuple[APXiDescriptorV1, ...]]:
    aeon_window_id = "AEON_LINE4_W_all"
    return {
        "S1_post_u_deltas": (
            APXiDescriptorV1(
                descriptor_id="apxi_delta_linear",
                descriptor_type="LINEAR_TREND",
                window_id=aeon_window_id,
                stream_id="S1_post_u_deltas",
                params={"intercept": 0, "slope": 1, "start_tick": 1},
            ),
        ),
        "S2_fluxes": (
            APXiDescriptorV1(
                descriptor_id="apxi_flux_const",
                descriptor_type="CONST_SEGMENT",
                window_id=aeon_window_id,
                stream_id="S2_fluxes",
                params={"value": 0},
            ),
        ),
        "S3_prev_chain": (
            APXiDescriptorV1(
                descriptor_id="apxi_chain_const",
                descriptor_type="CONST_SEGMENT",
                window_id=aeon_window_id,
                stream_id="S3_prev_chain",
                params={"value": 0},
            ),
        ),
    }


def _demo_config(*, apxi_enabled: bool) -> SessionConfigV1:
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()

    window_spec = TickLoopWindowSpec(
        window_id="LINE4_W1_T1_6",
        apx_name="LINE4_APX_W1_T1_6",
        start_tick=1,
        end_tick=6,
        streams=_demo_streams(),
        aeon_window_id="AEON_LINE4_W_all",
        apxi_descriptors=_demo_descriptors() if apxi_enabled else {},
        apxi_enabled=apxi_enabled,
        apxi_residual_scheme="R",
    )

    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[1, 0, 0, 0],
        total_ticks=6,
        window_specs=(window_spec,),
        primary_window_id=window_spec.window_id,
        run_id="AEON_APXI_DEMO_RUN",
        nid="aeon-apxi-demo-node",
        press_default_streams=_demo_streams(),
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


def test_codex_ingests_aeon_apxi_motifs() -> None:
    grammar = _demo_aeon_grammar()
    cfg = _demo_config(apxi_enabled=True)
    result = run_session(cfg)

    ctx = CodexContext(library_id="CE_MAIN")
    ctx.ingest(
        gid=result.config.topo.gid,
        run_id=result.tick_result.run_id,
        ledgers=result.tick_result.ledgers,
        p_blocks=result.tick_result.p_blocks,
        i_blocks=result.tick_result.i_blocks,
        manifests=result.tick_result.manifests.values(),
        envelopes=result.tick_result.envelopes,
        aeon_windows=grammar,
        apxi_views=result.tick_result.apxi_views.values(),
        window_id=grammar.derived_windows["AEON_LINE4_W_all"].window_id,
    )

    stats = ctx.runtime_stats
    assert stats.total_aeon_windows == len(grammar.window_ids())
    assert stats.total_apxi_views == len(result.tick_result.apxi_views)

    motifs = ctx.learn_apxi_descriptor_motifs()
    assert len(motifs) == 3
    assert {motif.pattern_descriptor["descriptor"]["descriptor_id"] for motif in motifs} == {
        "apxi_delta_linear",
        "apxi_flux_const",
        "apxi_chain_const",
    }
    for motif in motifs:
        assert motif.pattern_descriptor["type"] == "apxi_descriptor_v1"
        assert motif.created_at_tick == 1
        assert motif.last_updated_tick == 6

    # Replay should not duplicate motifs
    replay = ctx.learn_apxi_descriptor_motifs()
    assert replay == []

