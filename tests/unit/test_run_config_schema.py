import json
from pathlib import Path

import pytest

from config import load_run_session_config, run_config_from_mapping
from umx.topology_profile import load_topology_profile

FIXTURES_ROOT = Path(__file__).resolve().parents[2] / "docs" / "fixtures"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_gf01_example_config_matches_schema_and_topology():
    cfg_path = FIXTURES_ROOT / "configs" / "gf01_run_config.json"
    cfg = run_config_from_mapping(_load_json(cfg_path))

    assert cfg.gid == "GF01"
    assert cfg.primary_window_id == "GF01_W1_ticks_1_8"
    assert len(cfg.windows) == 2
    assert cfg.enable_codex is True

    topo_path = (cfg_path.parent / cfg.topology_path).resolve()
    topo = load_topology_profile(topo_path)
    assert len(cfg.initial_state) == topo.N

    session_cfg = load_run_session_config(cfg_path)
    assert session_cfg.topo.N == topo.N
    assert session_cfg.profile.name == "CMP-0"


def test_line_and_ring_examples_cover_integer_vectors():
    for name, expected_len in (("line_4_run_config.json", 4), ("ring_5_run_config.json", 5)):
        cfg_path = FIXTURES_ROOT / "configs" / name
        cfg = run_config_from_mapping(_load_json(cfg_path))
        topo_path = (cfg_path.parent / cfg.topology_path).resolve()
        topo = load_topology_profile(topo_path)
        assert len(cfg.initial_state) == expected_len == topo.N
        assert cfg.ticks > 0
        assert cfg.windows[0].start_tick == 1


def test_alt_profile_run_config_is_valid_and_selects_profile():
    cfg_path = FIXTURES_ROOT / "configs" / "line_4_run_config_cmp1.json"
    cfg = run_config_from_mapping(_load_json(cfg_path))
    assert cfg.profile_path.endswith("profile_cmp1.json")

    session_cfg = load_run_session_config(cfg_path)
    assert session_cfg.profile.name == "CMP-1"


def test_invalid_run_config_rejected():
    bad = {
        "v": 1,
        "gid": "BAD",
        "run_id": "missing_window",
        "topology_path": "../topologies/gf01_topology_profile.json",
        "profile_path": "../profiles/profile_cmp0.json",
        "ticks": 2,
        "initial_state": [1, 1, 1],
        "windows": [],
        "primary_window_id": "none",
    }
    with pytest.raises(ValueError):
        run_config_from_mapping(bad)
