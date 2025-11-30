from pathlib import Path

import pytest

from config import (
    load_run_config,
    load_scenario_registry,
    load_scenario_run_config,
)


REGISTRY_PATH = Path("docs/fixtures/scenarios/scenario_registry.json")


def test_scenario_registry_enumeration():
    registry = load_scenario_registry(REGISTRY_PATH)
    assert registry.list_ids() == ("gf01", "line-4", "ring-5", "gov-codex-demo")
    gf01 = registry.get("gf01")
    assert gf01.runtime_hint == "very-small"
    assert "CMP-0" in gf01.description


def test_load_scenario_run_config_round_trip():
    run_config = load_scenario_run_config("gf01", registry_path=REGISTRY_PATH)
    assert run_config.run_id == "GF01_config"
    assert run_config.gid == "GF01"
    assert run_config.ticks == 8

    # Ensure it aligns with direct RunConfig loading for determinism
    direct = load_run_config(Path("docs/fixtures/configs/gf01_run_config.json"))
    assert direct == run_config


def test_missing_scenario_id_errors():
    with pytest.raises(KeyError):
        load_scenario_run_config("missing", registry_path=REGISTRY_PATH)


def test_duplicate_scenario_detection(tmp_path):
    registry_data = {
        "v": 1,
        "scenarios": [
            {
                "scenario_id": "dup",
                "description": "duplicate",
                "run_config_path": "../configs/gf01_run_config.json",
            },
            {
                "scenario_id": "dup",
                "description": "duplicate",
                "run_config_path": "../configs/gf01_run_config.json",
            },
        ],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        __import__("json").dumps(registry_data, indent=2), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Duplicate scenario_id"):
        load_scenario_registry(registry_path)


def test_missing_run_config_file(tmp_path):
    registry_data = {
        "v": 1,
        "scenarios": [
            {
                "scenario_id": "ghost",
                "description": "no config present",
                "run_config_path": "./does_not_exist.json",
            }
        ],
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        __import__("json").dumps(registry_data, indent=2), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="run_config_path"):
        load_scenario_run_config("ghost", registry_path=registry_path)
