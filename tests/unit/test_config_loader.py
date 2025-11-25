import json
from pathlib import Path

import pytest

from config import load_run_session_config
from gate import run_session


FIXTURES_ROOT = Path(__file__).resolve().parents[2] / "docs" / "fixtures"


def test_load_run_session_config_runs_gf01():
    cfg_path = FIXTURES_ROOT / "configs" / "gf01_run_config.json"

    session_cfg = load_run_session_config(cfg_path)
    result = run_session(session_cfg)

    assert result.config.primary_window_id == "GF01_W1_ticks_1_8"
    assert result.tick_result.topo.gid == "GF01"
    assert result.tick_result.profile.name == "CMP-0"
    assert result.tick_result.ledgers[0].tick == 1
    assert result.tick_result.ledgers[-1].tick == session_cfg.total_ticks


def test_missing_topology_raises(tmp_path: Path):
    base = tmp_path
    config = {
        "v": 1,
        "gid": "GF01",
        "run_id": "missing_topo",
        "topology_path": "missing_topology.json",
        "profile_path": str(FIXTURES_ROOT / "profiles" / "profile_cmp0.json"),
        "ticks": 2,
        "initial_state": [1, 1, 1, 1, 1, 1],
        "windows": [
            {
                "window_id": "W1",
                "apx_name": "APX",
                "start_tick": 1,
                "end_tick": 2,
                "streams": [{"name": "deltas", "source": "post_u_deltas"}],
            }
        ],
        "primary_window_id": "W1",
    }
    cfg_path = base / "config.json"
    cfg_path.write_text(json.dumps(config))

    with pytest.raises(ValueError, match="topology_path does not exist"):
        load_run_session_config(cfg_path)


def test_pfna_enabled_requires_path(tmp_path: Path):
    cfg_template = json.loads((FIXTURES_ROOT / "configs" / "gf01_run_config.json").read_text())
    cfg_template.update({"enable_pfna": True, "pfna_path": None})
    cfg_template["topology_path"] = str(
        FIXTURES_ROOT / "topologies" / "gf01_topology_profile.json"
    )
    cfg_template["profile_path"] = str(FIXTURES_ROOT / "profiles" / "profile_cmp0.json")
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps(cfg_template))

    with pytest.raises(ValueError, match="enable_pfna is true"):
        load_run_session_config(cfg_path)


def test_non_cmp0_profile_can_run():
    cfg_path = FIXTURES_ROOT / "configs" / "line_4_run_config_cmp1.json"

    session_cfg = load_run_session_config(cfg_path)
    assert session_cfg.profile.name == "CMP-1"

    result = run_session(session_cfg)
    assert result.tick_result.profile.name == "CMP-1"
    assert result.tick_result.ledgers[-1].tick == session_cfg.total_ticks
