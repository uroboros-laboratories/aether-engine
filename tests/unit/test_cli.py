import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_ENTRY = [sys.executable, "-m", "cli"]
DEFAULT_REGISTRY = REPO_ROOT / "docs/fixtures/scenarios/scenario_registry.json"
ENV = {**os.environ, "PYTHONPATH": str(REPO_ROOT / "src")}


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*CLI_ENTRY, *args],
        cwd=REPO_ROOT,
        env=ENV,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_inspect_summary_and_tick() -> None:
    result = run_cli(
        "inspect",
        "gf01",
        "--summary",
        "--tick",
        "2",
        "--registry",
        str(DEFAULT_REGISTRY),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["summary"]["gid"] == "GF01"
    assert payload["summary"]["total_ticks"] == 8
    tick_info = payload["tick"]
    assert tick_info["tick"] == 2
    assert tick_info["ledger"]["tick"] == 2
    assert tick_info["p_block"]["tick"] == 2
    assert tick_info["nap_envelopes"], "NAP envelopes should be present for the tick"


def test_cli_inspect_window_and_ledger() -> None:
    window_id = "GF01_W1_ticks_1_8"
    result = run_cli(
        "inspect",
        "gf01",
        "--window",
        window_id,
        "--registry",
        str(DEFAULT_REGISTRY),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["window"]["window_id"] == window_id
    assert payload["window"]["manifest"]["apx_name"] == "GF01_APX_v0_full_window"

    ledger_result = run_cli(
        "show-ledger",
        "gf01",
        "--registry",
        str(DEFAULT_REGISTRY),
    )
    assert ledger_result.returncode == 0, ledger_result.stderr
    ledger_payload = json.loads(ledger_result.stdout)
    assert len(ledger_payload["ledger"]) == 8
    assert ledger_payload["ledger"][0]["tick"] == 1


def test_cli_handles_unknown_scenario() -> None:
    result = run_cli(
        "inspect",
        "unknown-scenario",
        "--summary",
        "--registry",
        str(DEFAULT_REGISTRY),
    )
    assert result.returncode != 0
    assert "Unknown run-id" in result.stderr or "Unknown run-id" in result.stdout


def test_cli_snapshot_generate_and_compare(tmp_path: Path) -> None:
    baseline = REPO_ROOT / "tests/snapshots/line_4_run_snapshot.json"
    output_path = tmp_path / "line_4_snapshot.json"

    gen_result = run_cli(
        "snapshot",
        "generate",
        "line-4",
        "--registry",
        str(DEFAULT_REGISTRY),
        "--output",
        str(output_path),
    )
    assert gen_result.returncode == 0, gen_result.stderr
    assert output_path.exists()

    cmp_result = run_cli(
        "snapshot",
        "compare",
        "line-4",
        "--registry",
        str(DEFAULT_REGISTRY),
        "--baseline",
        str(baseline),
        "--candidate",
        str(output_path),
    )
    assert cmp_result.returncode == 0, cmp_result.stderr
    assert "Snapshots match" in cmp_result.stdout
