from core.tick_loop import TickLoopWindowSpec
from gate import SessionConfigV1, run_session
from ops import MetricsConfigV1
from uledger.canonical import hash_record
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile
from config import load_run_session_config


def _gf01_session_config(metrics_enabled: bool) -> SessionConfigV1:
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    window_spec = TickLoopWindowSpec(
        window_id="GF01_W1_ticks_1_8",
        apx_name="GF01_APX_v0_full_window",
        start_tick=1,
        end_tick=8,
    )
    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=8,
        window_specs=(window_spec,),
        primary_window_id=window_spec.window_id,
        run_id="GF01_METRICS_SESSION",
        nid="gf01-node",
        metrics_config=MetricsConfigV1(enabled=metrics_enabled),
    )


def test_metrics_disabled_produces_no_snapshot():
    cfg = _gf01_session_config(metrics_enabled=False)
    result = run_session(cfg)
    assert result.metrics is None


def test_metrics_enabled_captures_counts():
    cfg = _gf01_session_config(metrics_enabled=True)
    result = run_session(cfg)
    metrics = result.metrics
    assert metrics is not None
    assert metrics.total_ticks == cfg.total_ticks
    assert metrics.window_count == 1
    assert metrics.nap_data == cfg.total_ticks
    assert metrics.nap_ingress == 0
    assert metrics.nap_egress == 1
    assert metrics.nap_total == metrics.nap_data + metrics.nap_egress + len(result.lifecycle_envelopes)
    assert metrics.uledger_entries == len(result.tick_result.u_ledger_entries)
    if result.tick_result.u_ledger_entries:
        assert metrics.uledger_last_hash == hash_record(result.tick_result.u_ledger_entries[-1])


def test_run_config_loader_enables_metrics(tmp_path):
    cfg = load_run_session_config("docs/fixtures/configs/gf01_run_config_metrics.json")
    assert cfg.metrics_config.enabled is True
    first = run_session(cfg)
    second = run_session(cfg)
    assert first.metrics is not None and second.metrics is not None
    assert first.metrics.to_dict() == second.metrics.to_dict()
