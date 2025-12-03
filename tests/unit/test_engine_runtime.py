import json
import shutil
from pathlib import Path

import pytest

from config import EngineRuntime


@pytest.fixture()
def runtime() -> EngineRuntime:
    repo_root = Path(__file__).resolve().parents[2]
    return EngineRuntime(repo_root=repo_root)


def _build_temp_repo(tmp_path: Path) -> Path:
    fixtures_src = Path(__file__).resolve().parents[2] / "docs" / "fixtures"
    fixtures_dest = tmp_path / "docs" / "fixtures"
    shutil.copytree(fixtures_src, fixtures_dest)
    return tmp_path


def test_build_session_config_applies_defaults(runtime: EngineRuntime) -> None:
    session = runtime.build_session_config("gf01")

    assert session.logging_config.enabled
    assert session.logging_config.destination == "memory"
    assert session.metrics_config.enabled
    assert session.governance.governance_mode == "OBSERVE"
    assert session.governance.codex_action_mode == "OBSERVE"


def test_build_session_config_supports_overrides(runtime: EngineRuntime) -> None:
    overrides = {
        "run_id": "custom-run",
        "ticks": 10,
        "logging": {"enabled": True, "include_ticks": False},
        "metrics": {"enabled": False},
        "governance": {"governance_mode": "ENFORCE"},
    }

    session = runtime.build_session_config("gf01", overrides=overrides)

    assert session.run_id == "custom-run"
    assert session.total_ticks == 10
    assert session.logging_config.include_ticks is False
    assert session.metrics_config.enabled is False
    assert session.governance.governance_mode == "ENFORCE"


def test_governance_base_updates_persist(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    runtime = EngineRuntime(repo_root=repo_root)

    baseline = runtime.load_governance_base()
    assert baseline["codex_action_mode"] == "OBSERVE"

    updated = runtime.update_governance_base(
        {
            "codex_action_mode": "DRY_RUN",
            "budget_policies": [
                {"policy_id": "default", "max_actions_per_window": 5},
                {"policy_id": "secondary", "max_proposals_per_window": 2},
            ],
        }
    )

    assert updated["codex_action_mode"] == "DRY_RUN"
    budgets = {entry["policy_id"]: entry for entry in updated["budget_policies"]}
    assert budgets["default"]["max_actions_per_window"] == 5
    assert budgets["secondary"]["max_proposals_per_window"] == 2

    persisted = json.loads(runtime.governance_base_path.read_text())
    assert persisted["codex_action_mode"] == "DRY_RUN"
