import pytest

from core.tick_loop import TickLoopWindowSpec
from press import (
    AEONDerivedWindowV1,
    AEONWindowDefV1,
    AEONWindowGrammarV1,
    AEONWindowRegistry,
    APXManifestV1,
    build_registry_from_press_windows,
)


def test_registry_queries_cover_base_and_derived_windows():
    base_windows = {
        "day_1": AEONWindowDefV1("day_1", 1, 4, labels=("daily",)),
        "day_2": AEONWindowDefV1("day_2", 5, 8, labels=("daily",)),
    }
    derived_windows = {
        "week_1": AEONDerivedWindowV1(
            window_id="week_1",
            source_ids=("day_1", "day_2"),
            aggregation="union",
            labels=("weekly",),
        )
    }

    registry = AEONWindowRegistry.from_windows(base_windows, derived_windows)

    assert registry.get_window("week_1").aggregation == "union"
    assert registry.parent_of("day_1") is None
    assert registry.children_of("week_1") == []
    assert registry.windows_covering_tick(2) == ["day_1", "week_1"]
    assert registry.windows_covering_tick(6) == ["day_2", "week_1"]


def test_duplicate_registration_raises():
    grammar = AEONWindowGrammarV1(base_windows={}, derived_windows={})
    registry = AEONWindowRegistry.from_grammar(grammar)
    registry.register_base(AEONWindowDefV1("w1", 1, 1))

    with pytest.raises(ValueError):
        registry.register_base(AEONWindowDefV1("w1", 2, 2))


def test_press_windows_are_mapped_into_aeon_registry():
    specs = [
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_8",
            apx_name="GF01_APX_v0_full_window",
            start_tick=1,
            end_tick=8,
        ),
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_2",
            apx_name="GF01_APX_v0_ticks_1_2",
            start_tick=1,
            end_tick=2,
        ),
    ]
    manifests = {
        "GF01_APX_v0_full_window": APXManifestV1(
            apx_name="GF01_APX_v0_full_window",
            profile="CMP0",
            manifest_check=123,
            streams=[],
        ),
        "GF01_APX_v0_ticks_1_2": APXManifestV1(
            apx_name="GF01_APX_v0_ticks_1_2",
            profile="CMP0",
            manifest_check=456,
            streams=[],
        ),
    }

    registry = build_registry_from_press_windows(specs, manifests)

    covering_tick_one = registry.windows_covering_tick(1)
    assert covering_tick_one == ["GF01_W1_ticks_1_2", "GF01_W1_ticks_1_8"]

    base_window = registry.get_window("GF01_W1_ticks_1_8")
    assert base_window.tick_start == 1
    assert base_window.press_window_id == "GF01_APX_v0_full_window"
