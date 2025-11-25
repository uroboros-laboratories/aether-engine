from pathlib import Path

import pytest

from config import load_run_session_config
from gate import run_session
from ops import build_introspection_view


def test_introspection_view_gf01_recovers_core_artefacts() -> None:
    cfg = load_run_session_config(Path("docs/fixtures/configs/gf01_run_config.json"))
    session = run_session(cfg)

    view = build_introspection_view(session)

    assert view.gid == cfg.topo.gid
    assert view.run_id == cfg.run_id

    ledger_1 = view.get_umx_ledger(1)
    assert ledger_1.tick == 1
    assert ledger_1 is session.tick_result.ledgers[0]

    p_block_final = view.get_loom_p_block(cfg.total_ticks)
    assert p_block_final.tick == cfg.total_ticks

    assert session.tick_result.i_blocks, "GF-01 should emit at least one I-block"
    i_block_tick = session.tick_result.i_blocks[0].tick
    assert view.get_loom_i_block(i_block_tick).tick == i_block_tick

    manifest = view.get_apx_manifest(cfg.primary_window_id)
    assert manifest.apx_name == cfg.window_specs[0].apx_name

    ctrl_envelopes = view.get_nap_envelopes(layer="CTRL")
    assert {env.tick for env in ctrl_envelopes} == {1, cfg.total_ticks}

    data_envelopes = view.get_nap_envelopes(layer="DATA")
    assert len(data_envelopes) == cfg.total_ticks

    egress_envelopes = view.get_nap_envelopes(layer="EGRESS")
    assert len(egress_envelopes) == len(session.tick_result.egress_envelopes)

    uledger_entry = view.get_uledger_entry(3)
    assert uledger_entry.tick == 3


def test_introspection_view_handles_additional_scenario() -> None:
    cfg = load_run_session_config(Path("docs/fixtures/configs/line_4_run_config_cmp1.json"))
    session = run_session(cfg)

    view = build_introspection_view(session)

    assert view.window_ids == tuple(sorted(spec.window_id for spec in cfg.window_specs))
    assert len(view.get_nap_envelopes(layer="DATA")) == cfg.total_ticks

    p_block_final = view.get_loom_p_block(cfg.total_ticks)
    assert p_block_final.tick == cfg.total_ticks

    with pytest.raises(ValueError):
        view.get_loom_i_block(1)

