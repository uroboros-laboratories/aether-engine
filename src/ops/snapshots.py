"""Snapshot management utilities (SPEC-006 P3.3.2).

These helpers generate deterministic regression snapshots from run configs and
provide structured diffs to make review of changes explicit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableSequence, Sequence, Tuple

from config import load_run_session_config, load_scenario_registry
from core import serialize_session_run
from gate import run_session

DEFAULT_SNAPSHOT_DIR = Path(__file__).resolve().parents[2] / "tests" / "snapshots"


def generate_snapshot_from_config(config_path: Path) -> Dict[str, Any]:
    """Run a session from a RunConfig JSON path and return the serialized snapshot."""

    session_config = load_run_session_config(config_path)
    return serialize_session_run(run_session(session_config))


def generate_snapshot_from_scenario(scenario_id: str, registry_path: Path) -> Dict[str, Any]:
    """Resolve a scenario via registry and return the serialized snapshot."""

    registry = load_scenario_registry(registry_path)
    entry = registry.get(scenario_id)
    config_path = (registry_path.parent / entry.run_config_path).resolve()
    return generate_snapshot_from_config(config_path)


def load_snapshot(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def write_snapshot(snapshot: Mapping[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, sort_keys=True, indent=2))


@dataclass(frozen=True)
class SnapshotDiff:
    path: str
    baseline: Any
    candidate: Any


def diff_snapshots(
    baseline: Any, candidate: Any, *, path: str = "", max_diffs: int = 100
) -> List[SnapshotDiff]:
    """Recursively diff two JSON-compatible payloads.

    Returns at most ``max_diffs`` entries to keep output readable.
    """

    diffs: MutableSequence[SnapshotDiff] = []

    def _walk(a: Any, b: Any, cur_path: str) -> None:
        if len(diffs) >= max_diffs:
            return

        if type(a) != type(b):
            diffs.append(SnapshotDiff(cur_path, a, b))
            return

        if isinstance(a, Mapping):
            a_keys = set(a.keys())
            b_keys = set(b.keys())
            for key in sorted(a_keys | b_keys):
                next_path = f"{cur_path}.{key}" if cur_path else str(key)
                if key not in a:
                    diffs.append(SnapshotDiff(next_path, "<missing>", b[key]))
                elif key not in b:
                    diffs.append(SnapshotDiff(next_path, a[key], "<missing>"))
                else:
                    _walk(a[key], b[key], next_path)
            return

        if isinstance(a, Sequence) and not isinstance(a, (str, bytes, bytearray)):
            for idx, (av, bv) in enumerate(zip(a, b)):
                _walk(av, bv, f"{cur_path}[{idx}]")
                if len(diffs) >= max_diffs:
                    return
            if len(a) != len(b) and len(diffs) < max_diffs:
                diffs.append(
                    SnapshotDiff(f"{cur_path}.length", len(a), len(b))
                )
            return

        if a != b:
            diffs.append(SnapshotDiff(cur_path, a, b))

    _walk(baseline, candidate, path)
    return list(diffs)


def render_snapshot_diffs(diffs: Iterable[SnapshotDiff]) -> str:
    lines = []
    for diff in diffs:
        lines.append(
            f"{diff.path or '<root>'}: baseline={diff.baseline!r} candidate={diff.candidate!r}"
        )
    return "\n".join(lines)


def compare_snapshots(
    *,
    baseline_path: Path,
    candidate_path: Path | None = None,
    scenario: str | None = None,
    run_config: Path | None = None,
    registry_path: Path | None = None,
    max_diffs: int = 100,
) -> Tuple[List[SnapshotDiff], Dict[str, Any]]:
    """Compare a baseline snapshot with another snapshot or a fresh run."""

    baseline = load_snapshot(baseline_path)

    if candidate_path is not None:
        candidate = load_snapshot(candidate_path)
    elif run_config is not None:
        candidate = generate_snapshot_from_config(run_config)
    elif scenario is not None and registry_path is not None:
        candidate = generate_snapshot_from_scenario(scenario, registry_path)
    else:
        raise ValueError("Provide candidate_path, run_config, or scenario+registry_path")

    diffs = diff_snapshots(baseline, candidate, max_diffs=max_diffs)
    return diffs, candidate
