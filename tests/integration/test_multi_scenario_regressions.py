from __future__ import annotations

import json
from pathlib import Path

import pytest

from config import load_run_session_config
from core import dumps_session_run
from core.serialization import serialize_session_run
from gate import run_session

_REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = _REPO_ROOT / "docs" / "fixtures" / "configs"
SNAPSHOT_ROOT = _REPO_ROOT / "tests" / "snapshots"

SCENARIOS = (
    (
        "line-4",
        CONFIG_ROOT / "line_4_run_config.json",
        SNAPSHOT_ROOT / "line_4_run_snapshot.json",
        6,
    ),
    (
        "ring-5",
        CONFIG_ROOT / "ring_5_run_config.json",
        SNAPSHOT_ROOT / "ring_5_run_snapshot.json",
        5,
    ),
)


def _assert_run_invariants(result, expected_ticks: int) -> None:
    tick_result = result.tick_result

    assert len(tick_result.ledgers) == expected_ticks
    assert [ledger.tick for ledger in tick_result.ledgers] == list(
        range(1, expected_ticks + 1)
    )
    assert len(tick_result.p_blocks) == expected_ticks
    assert len(tick_result.envelopes) == expected_ticks
    assert tick_result.envelopes[-1].tick == expected_ticks
    assert result.lifecycle_envelopes[0].tick == 1
    assert result.lifecycle_envelopes[-1].tick == expected_ticks


@pytest.mark.parametrize(
    "scenario_id, cfg_path, snapshot_path, expected_ticks",
    SCENARIOS,
)
def test_reference_scenarios_are_deterministic_and_regressed(
    scenario_id: str,
    cfg_path: Path,
    snapshot_path: Path,
    expected_ticks: int,
):
    cfg = load_run_session_config(cfg_path)
    first = run_session(cfg)
    second = run_session(load_run_session_config(cfg_path))

    assert dumps_session_run(first) == dumps_session_run(second)

    snapshot = json.loads(snapshot_path.read_text())
    assert serialize_session_run(first) == snapshot

    _assert_run_invariants(first, expected_ticks)
