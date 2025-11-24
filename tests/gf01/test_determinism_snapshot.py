from __future__ import annotations

import json
from pathlib import Path

from core import dumps_gf01_run, run_gf01, serialize_gf01_run


SNAPSHOT_PATH = Path(__file__).parent.parent / "snapshots" / "gf01_run_snapshot.json"


def test_gf01_double_run_is_bytewise_identical():
    first_json = dumps_gf01_run(run_gf01())
    second_json = dumps_gf01_run(run_gf01())

    assert first_json == second_json


def test_gf01_matches_snapshot():
    result = run_gf01()
    serialized = serialize_gf01_run(result)

    with SNAPSHOT_PATH.open("r", encoding="utf-8") as f:
        snapshot = json.load(f)

    assert serialized == snapshot

