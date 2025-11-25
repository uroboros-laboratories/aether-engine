"""Structured logging tests for Phase 3 governance work."""
from config import load_run_session_config
from gate import SessionConfigV1, run_session
from ops import LoggingConfigV1
from core.tick_loop import TickLoopWindowSpec
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


def _gf01_session_config(logging_enabled: bool) -> SessionConfigV1:
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
        run_id="GF01_SESSION",
        nid="gf01-node",
        logging_config=LoggingConfigV1(enabled=logging_enabled),
    )


def test_logging_disabled_produces_no_entries():
    cfg = _gf01_session_config(logging_enabled=False)
    result = run_session(cfg)
    assert result.logs == []


def test_logging_enabled_captures_run_and_ticks():
    cfg = _gf01_session_config(logging_enabled=True)
    result = run_session(cfg)
    events = [entry.event for entry in result.logs]
    assert events[0] == "run_start"
    assert events[-1] == "run_end"

    tick_events = [entry for entry in result.logs if entry.event == "tick_complete"]
    assert len(tick_events) == cfg.total_ticks
    assert all(entry.tick is not None for entry in tick_events)

    window_events = [entry for entry in result.logs if entry.event == "window_closed"]
    assert len(window_events) == 1
    assert window_events[0].window_id == cfg.primary_window_id


def test_logging_structure_is_stable_across_runs(tmp_path):
    cfg = load_run_session_config("docs/fixtures/configs/gf01_run_config_logging.json")
    first = run_session(cfg)
    second = run_session(cfg)

    def strip_ts(entries):
        cleaned = []
        for entry in entries:
            payload = entry.to_dict()
            payload.pop("ts", None)
            cleaned.append(payload)
        return cleaned

    assert strip_ts(first.logs) == strip_ts(second.logs)
