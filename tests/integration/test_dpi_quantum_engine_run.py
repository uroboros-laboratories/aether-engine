from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_experiment_run_engine_executes_end_to_end(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    logs_root = tmp_path / "quantum_logs"
    env = os.environ.copy()
    existing_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(repo_root / "src") + (f":{existing_path}" if existing_path else "")

    cmd = [
        sys.executable,
        "-m",
        "dpi_quantum",
        "--logs-dir",
        str(logs_root),
        "experiment",
        "--name",
        "spin_chain",
        "--qubits",
        "4",
        "--ticks",
        "4",
        "--run-engine",
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root, env=env)

    assert completed.returncode == 0, completed.stderr
    assert "stub" not in completed.stdout.lower()

    logs_dir = logs_root / "logs"
    jsonl_path = logs_dir / "quantum_runs.jsonl"
    csv_path = logs_dir / "quantum_runs.csv"
    assert jsonl_path.exists()
    assert csv_path.exists()

    entries = [json.loads(line) for line in jsonl_path.read_text().splitlines() if line.strip()]
    assert entries, "no run summaries were recorded"
    last = entries[-1]

    for field in [
        "runtime_total_ms",
        "runtime_engine_ms",
        "ticks",
        "loom_p_blocks",
        "loom_i_blocks",
        "loom_bytes",
    ]:
        assert last.get(field) not in (None, ""), f"missing {field}"

    assert last.get("status") == "OK"
    assert int(last.get("ticks")) >= 1
    assert int(last.get("loom_p_blocks")) >= 1
