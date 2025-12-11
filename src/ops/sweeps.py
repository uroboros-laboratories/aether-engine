"""Sweep configuration loader and iterator for Phase 9 EPIC 4.

The sweep runner will consume YAML or JSON configs describing a base job type
(`ingest`, `simulate`, or `experiment`) plus parameter grids. This module keeps
parsing logic and point generation separate from the CLI so future automation
can reuse the same loader without depending on `argparse` surfaces.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional


try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback when PyYAML is absent
    yaml = None


SUPPORTED_KINDS = {
    "ingest",
    "simulate",
    "experiment",
    "snapshot_generate",
    "snapshot_compare",
    "emulation_compare",
    "gf01_run",
    "gf01_compare",
}


@dataclass
class SweepPoint:
    """Single sweep point containing resolved parameters."""

    index: int
    params: Dict[str, Any]


@dataclass
class SweepConfig:
    """In-memory representation of a sweep config file."""

    name: str
    kind: str
    base_params: Dict[str, Any] = field(default_factory=dict)
    grid: Mapping[str, Iterable[Any]] = field(default_factory=dict)
    notes: str = ""

    def validate(self) -> None:
        if self.kind not in SUPPORTED_KINDS:
            raise ValueError(f"Unsupported sweep kind '{self.kind}' (expected one of {sorted(SUPPORTED_KINDS)})")
        if not self.grid:
            raise ValueError("Sweep config must include a non-empty parameter grid")


def _load_yaml_or_json(path: Path) -> Mapping[str, Any]:
    text = path.read_text()
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError(
                "PyYAML is required to load YAML sweep configs; install it (e.g.,"
                " python -m pip install -r requirements.txt) or use a JSON sweep file"
            )
        return yaml.safe_load(text)
    return json.loads(text)


def load_sweep_config(path: Path | str) -> SweepConfig:
    """Load and validate a sweep config from disk."""

    cfg_path = Path(path).expanduser().resolve()
    payload = _load_yaml_or_json(cfg_path)
    config = SweepConfig(
        name=str(payload.get("name") or cfg_path.stem),
        kind=str(payload.get("kind") or "").lower(),
        base_params=dict(payload.get("base_params") or {}),
        grid=dict(payload.get("grid") or {}),
        notes=str(payload.get("notes") or ""),
    )
    config.validate()
    return config


def iter_points(config: SweepConfig) -> Iterator[SweepPoint]:
    """Iterate over all parameter combinations defined in the sweep grid."""

    keys: List[str] = list(config.grid.keys())
    values: List[List[Any]] = [list(config.grid[key]) for key in keys]
    for index, combo in enumerate(product(*values)):
        params: Dict[str, Any] = dict(config.base_params)
        params.update({key: value for key, value in zip(keys, combo)})
        yield SweepPoint(index=index, params=params)

