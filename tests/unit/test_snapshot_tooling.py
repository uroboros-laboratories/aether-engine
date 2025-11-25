from __future__ import annotations

import json
from pathlib import Path

from ops.snapshots import (
    compare_snapshots,
    diff_snapshots,
    render_snapshot_diffs,
    write_snapshot,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
LINE_CONFIG = REPO_ROOT / "docs/fixtures/configs/line_4_run_config.json"
LINE_SNAPSHOT = REPO_ROOT / "tests/snapshots/line_4_run_snapshot.json"


def test_diff_snapshots_reports_changes_and_renders() -> None:
    baseline = {"a": 1, "b": [1, 2]}
    candidate = {"a": 2, "b": [1, 3, 4]}

    diffs = diff_snapshots(baseline, candidate, max_diffs=5)
    diff_paths = {d.path for d in diffs}

    assert "a" in diff_paths
    assert "b[1]" in diff_paths
    assert "b.length" in diff_paths

    rendered = render_snapshot_diffs(diffs)
    assert "baseline" in rendered and "candidate" in rendered


def test_compare_snapshots_matches_line_and_can_write(tmp_path: Path) -> None:
    diffs, candidate = compare_snapshots(
        baseline_path=LINE_SNAPSHOT, run_config=LINE_CONFIG, max_diffs=10
    )

    assert diffs == []

    out_path = tmp_path / "gf01_candidate.json"
    write_snapshot(candidate, out_path)
    assert json.loads(out_path.read_text()) == candidate
