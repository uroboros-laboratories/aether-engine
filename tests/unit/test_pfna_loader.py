import json
from pathlib import Path

import pytest

from gate import PFNAInputV0, dump_pfna_v0, load_pfna_v0


@pytest.fixture
def pfna_dict():
    return {
        "v": 0,
        "pfna_id": "BUNDLE_A",
        "gid": "LINE_PFNA",
        "run_id": "RUN01",
        "nid": "N1",
        "entries": [
            {"pfna_id": "E1", "tick": 2, "values": [1, 2, 3]},
            {"pfna_id": "E0", "tick": 1, "values": [0, 0, 0], "description": "init"},
        ],
    }


def test_load_pfna_v0_from_dict_sorted_and_valid(pfna_dict):
    loaded = load_pfna_v0(pfna_dict, expected_length=3)
    assert [p.pfna_id for p in loaded] == ["E0", "E1"]
    assert loaded[0].tick == 1
    assert loaded[1].values == (1, 2, 3)
    assert all(isinstance(p, PFNAInputV0) for p in loaded)


def test_load_pfna_v0_from_json_file(tmp_path: Path, pfna_dict):
    pfna_path = tmp_path / "pfna.json"
    pfna_path.write_text(json.dumps(pfna_dict), encoding="utf-8")

    loaded = load_pfna_v0(pfna_path, expected_length=3)
    assert len(loaded) == 2
    assert loaded[0].gid == pfna_dict["gid"]
    assert loaded[1].run_id == pfna_dict["run_id"]


def test_load_pfna_v0_invalid_length_raises(pfna_dict):
    pfna_dict["entries"][0]["values"] = [1, 2]  # wrong length
    with pytest.raises(ValueError, match="values length must match expected_length"):
        load_pfna_v0(pfna_dict, expected_length=3)


def test_load_pfna_v0_missing_field_raises(pfna_dict):
    pfna_dict["entries"][0].pop("pfna_id")
    with pytest.raises(ValueError, match="missing required field 'pfna_id'"):
        load_pfna_v0(pfna_dict)


def test_load_pfna_v0_allows_tick_zero_for_initial_state(pfna_dict):
    pfna_dict["entries"].append({"pfna_id": "INIT", "tick": 0, "values": [9, 9, 9]})
    loaded = load_pfna_v0(pfna_dict, expected_length=3)
    assert loaded[0].pfna_id == "INIT"
    assert loaded[0].tick == 0


def test_pfna_round_trip_serialise_and_parse(pfna_dict):
    loaded = load_pfna_v0(pfna_dict, expected_length=3)
    dumped = dump_pfna_v0(
        bundle_id=pfna_dict["pfna_id"],
        gid=pfna_dict["gid"],
        run_id=pfna_dict["run_id"],
        nid=pfna_dict["nid"],
        entries=loaded,
    )

    # Sorting ensures deterministic ordering for the comparison
    reloaded = load_pfna_v0(dumped, expected_length=3)
    assert reloaded == loaded
