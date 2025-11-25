import json

import pytest

from press import AEONDerivedWindowV1, AEONWindowDefV1, AEONWindowGrammarV1


def test_gf01_window_representation_round_trip():
    base = {
        "ticks_1_8": AEONWindowDefV1(
            window_id="ticks_1_8",
            tick_start=1,
            tick_end=8,
            labels=("gf01", "cmp0"),
            press_window_id="ticks_1_8",
        )
    }
    grammar = AEONWindowGrammarV1(base_windows=base, derived_windows={})

    encoded = grammar.to_json()
    restored = AEONWindowGrammarV1.from_json(encoded)

    assert restored.base_windows["ticks_1_8"].tick_start == 1
    assert restored.base_windows["ticks_1_8"].press_window_id == "ticks_1_8"
    assert restored.to_json() == encoded


def test_hierarchical_windows_and_children_lookup():
    base_windows = {
        "day_1": AEONWindowDefV1("day_1", 1, 4, labels=("daily",), parent_id="week_1"),
        "day_2": AEONWindowDefV1("day_2", 5, 8, labels=("daily",), parent_id="week_1"),
    }
    derived_windows = {
        "week_1": AEONDerivedWindowV1(
            window_id="week_1",
            source_ids=("day_1", "day_2"),
            aggregation="union",
            labels=("weekly",),
            press_window_id="week_1_manifest",
        )
    }

    grammar = AEONWindowGrammarV1(base_windows=base_windows, derived_windows=derived_windows)

    assert grammar.window_ids() == ["day_1", "day_2", "week_1"]
    assert grammar.children_of("week_1") == ["day_1", "day_2"]
    assert grammar.get_window("week_1").aggregation == "union"


def test_validation_errors_for_invalid_ranges_and_refs():
    with pytest.raises(ValueError):
        AEONWindowDefV1("bad", 5, 4)

    base = {"a": AEONWindowDefV1("a", 1, 2)}
    derived = {
        "b": AEONDerivedWindowV1(window_id="b", source_ids=("missing",)),
    }
    with pytest.raises(ValueError):
        AEONWindowGrammarV1(base_windows=base, derived_windows=derived)


def test_serialization_is_stable_and_deterministic():
    grammar = AEONWindowGrammarV1(
        base_windows={
            "w1": AEONWindowDefV1("w1", 1, 1, labels=("demo",)),
            "w2": AEONWindowDefV1("w2", 2, 2, labels=("demo",), parent_id="agg"),
        },
        derived_windows={
            "agg": AEONDerivedWindowV1("agg", ("w1", "w2"), aggregation="concat", labels=("agg",)),
        },
    )

    encoded = grammar.to_json()
    reloaded = AEONWindowGrammarV1.from_json(encoded)

    assert json.loads(encoded)["base_windows"]["w1"]["tick_start"] == 1
    assert reloaded.derived_windows["agg"].aggregation == "concat"
    assert reloaded.to_json() == encoded
