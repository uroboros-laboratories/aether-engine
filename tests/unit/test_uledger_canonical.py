from dataclasses import dataclass

import pytest

from uledger import canonical_json_dumps, hash_record


@dataclass
class SampleDataclass:
    value: int
    label: str


def test_canonical_json_dumps_sorts_keys_and_normalizes():
    record = {"b": 1, "a": [3, {"d": 4, "c": 2}]}
    result = canonical_json_dumps(record)
    assert result == '{"a":[3,{"c":2,"d":4}],"b":1}'


def test_canonical_json_dumps_accepts_dataclasses_and_tuples():
    record = {
        "outer": (SampleDataclass(value=5, label="x"), True, None),
    }
    result = canonical_json_dumps(record)
    assert result == '{"outer":[{"label":"x","value":5},true,null]}'


def test_hash_record_is_stable_and_changes_on_mutation():
    base = {"x": 1, "y": [2, 3]}
    reordered = {"y": [2, 3], "x": 1}
    mutated = {"x": 1, "y": [2, 4]}

    hash_base = hash_record(base)
    hash_reordered = hash_record(reordered)
    hash_mutated = hash_record(mutated)

    assert hash_base == hash_reordered
    assert hash_base != hash_mutated


def test_hash_record_rejects_unknown_algorithm():
    with pytest.raises(ValueError):
        hash_record({"x": 1}, algorithm="md5")


def test_canonical_json_dumps_rejects_unsupported_types():
    with pytest.raises(TypeError):
        canonical_json_dumps({"x": {1, 2, 3}})
