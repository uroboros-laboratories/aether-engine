"""AEON window grammar types and helpers (v1)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from core.tick_loop import TickLoopWindowSpec
    from press.press import APXManifestV1


@dataclass(frozen=True)
class AEONWindowDefV1:
    """Base AEON window definition over the Loom tick axis."""

    window_id: str
    tick_start: int
    tick_end: int
    labels: tuple[str, ...] = ()
    press_window_id: str | None = None
    parent_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.window_id, str) or not self.window_id:
            raise ValueError("window_id must be a non-empty string")
        if not isinstance(self.tick_start, int) or not isinstance(self.tick_end, int):
            raise TypeError("tick_start and tick_end must be integers")
        if self.tick_end < self.tick_start:
            raise ValueError("tick_end must be >= tick_start")
        _validate_labels(self.labels)

    def to_dict(self) -> Dict[str, object]:
        return {
            "window_id": self.window_id,
            "tick_start": self.tick_start,
            "tick_end": self.tick_end,
            "labels": list(self.labels),
            "press_window_id": self.press_window_id,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "AEONWindowDefV1":
        return cls(
            window_id=_require_str(data, "window_id"),
            tick_start=_require_int(data, "tick_start"),
            tick_end=_require_int(data, "tick_end"),
            labels=tuple(_require_labels(data.get("labels", ()))),
            press_window_id=_require_optional_str(data.get("press_window_id")),
            parent_id=_require_optional_str(data.get("parent_id")),
        )


@dataclass(frozen=True)
class AEONDerivedWindowV1:
    """Derived/aggregated AEON window."""

    window_id: str
    source_ids: tuple[str, ...]
    aggregation: str = "aggregate"
    labels: tuple[str, ...] = ()
    press_window_id: str | None = None
    parent_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.window_id, str) or not self.window_id:
            raise ValueError("window_id must be a non-empty string")
        if not self.source_ids:
            raise ValueError("source_ids must be non-empty")
        for source_id in self.source_ids:
            if not isinstance(source_id, str) or not source_id:
                raise ValueError("source_ids must be non-empty strings")
        if len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("source_ids must be unique")
        if not isinstance(self.aggregation, str) or not self.aggregation:
            raise ValueError("aggregation must be a non-empty string")
        _validate_labels(self.labels)

    def to_dict(self) -> Dict[str, object]:
        return {
            "window_id": self.window_id,
            "source_ids": list(self.source_ids),
            "aggregation": self.aggregation,
            "labels": list(self.labels),
            "press_window_id": self.press_window_id,
            "parent_id": self.parent_id,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "AEONDerivedWindowV1":
        return cls(
            window_id=_require_str(data, "window_id"),
            source_ids=tuple(_require_str_list(data, "source_ids")),
            aggregation=_require_str(data, "aggregation", default="aggregate"),
            labels=tuple(_require_labels(data.get("labels", ()))),
            press_window_id=_require_optional_str(data.get("press_window_id")),
            parent_id=_require_optional_str(data.get("parent_id")),
        )


@dataclass
class AEONWindowGrammarV1:
    """Container for AEON windows and relations."""

    base_windows: Dict[str, AEONWindowDefV1]
    derived_windows: Dict[str, AEONDerivedWindowV1]

    def __post_init__(self) -> None:
        self._validate_uniqueness()
        self._validate_references()

    def _validate_uniqueness(self) -> None:
        base_ids = set(self.base_windows)
        derived_ids = set(self.derived_windows)
        intersect = base_ids & derived_ids
        if intersect:
            raise ValueError(f"window IDs must be unique across base and derived: {sorted(intersect)}")

    def _validate_references(self) -> None:
        known_ids = set(self.base_windows) | set(self.derived_windows)
        for window in self.base_windows.values():
            _validate_parent(window.parent_id, known_ids, window.window_id)
        for window in self.derived_windows.values():
            _validate_parent(window.parent_id, known_ids, window.window_id)
            for source_id in window.source_ids:
                if source_id not in known_ids:
                    raise ValueError(f"source_id '{source_id}' is not defined in grammar")
                if source_id == window.window_id:
                    raise ValueError("derived window cannot reference itself")

    def to_mapping(self) -> Dict[str, MutableMapping[str, object]]:
        base = {wid: window.to_dict() for wid, window in sorted(self.base_windows.items())}
        derived = {wid: window.to_dict() for wid, window in sorted(self.derived_windows.items())}
        return {"base_windows": base, "derived_windows": derived}

    @classmethod
    def from_mapping(cls, data: Mapping[str, object]) -> "AEONWindowGrammarV1":
        base_raw = _require_mapping(data, "base_windows")
        derived_raw = _require_mapping(data, "derived_windows")
        base_windows = {wid: AEONWindowDefV1.from_dict(entry) for wid, entry in base_raw.items()}
        derived_windows = {wid: AEONDerivedWindowV1.from_dict(entry) for wid, entry in derived_raw.items()}
        return cls(base_windows=base_windows, derived_windows=derived_windows)

    def to_json(self) -> str:
        return json.dumps(self.to_mapping(), sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "AEONWindowGrammarV1":
        return cls.from_mapping(json.loads(text))

    def window_ids(self) -> List[str]:
        return sorted(set(self.base_windows) | set(self.derived_windows))

    def get_window(self, window_id: str) -> AEONWindowDefV1 | AEONDerivedWindowV1:
        if window_id in self.base_windows:
            return self.base_windows[window_id]
        if window_id in self.derived_windows:
            return self.derived_windows[window_id]
        raise KeyError(window_id)

    def children_of(self, window_id: str) -> List[str]:
        return sorted(
            [wid for wid, window in self.base_windows.items() if window.parent_id == window_id]
            + [wid for wid, window in self.derived_windows.items() if window.parent_id == window_id]
        )


class AEONWindowRegistry:
    """Registry for AEON windows with query helpers."""

    def __init__(self, grammar: AEONWindowGrammarV1) -> None:
        self.grammar = grammar
        self._coverage_ranges: Dict[str, tuple[int, int]] = {}
        self._parent_lookup: Dict[str, str | None] = {}
        self._reindex()

    @classmethod
    def from_windows(
        cls,
        base_windows: Mapping[str, AEONWindowDefV1],
        derived_windows: Mapping[str, AEONDerivedWindowV1],
    ) -> "AEONWindowRegistry":
        grammar = AEONWindowGrammarV1(
            base_windows=dict(base_windows),
            derived_windows=dict(derived_windows),
        )
        return cls(grammar)

    @classmethod
    def from_grammar(cls, grammar: AEONWindowGrammarV1) -> "AEONWindowRegistry":
        return cls(grammar)

    def register_base(self, window: AEONWindowDefV1) -> None:
        if window.window_id in self.grammar.base_windows or window.window_id in self.grammar.derived_windows:
            raise ValueError(f"window_id '{window.window_id}' already registered")
        base = dict(self.grammar.base_windows)
        base[window.window_id] = window
        self.grammar = AEONWindowGrammarV1(base_windows=base, derived_windows=dict(self.grammar.derived_windows))
        self._reindex()

    def register_derived(self, window: AEONDerivedWindowV1) -> None:
        if window.window_id in self.grammar.base_windows or window.window_id in self.grammar.derived_windows:
            raise ValueError(f"window_id '{window.window_id}' already registered")
        derived = dict(self.grammar.derived_windows)
        derived[window.window_id] = window
        self.grammar = AEONWindowGrammarV1(base_windows=dict(self.grammar.base_windows), derived_windows=derived)
        self._reindex()

    def get_window(self, window_id: str) -> AEONWindowDefV1 | AEONDerivedWindowV1:
        return self.grammar.get_window(window_id)

    def parent_of(self, window_id: str) -> str | None:
        if window_id not in self._parent_lookup:
            raise KeyError(window_id)
        return self._parent_lookup[window_id]

    def children_of(self, window_id: str) -> List[str]:
        return self.grammar.children_of(window_id)

    def windows_covering_tick(self, tick: int) -> List[str]:
        if not isinstance(tick, int):
            raise TypeError("tick must be an integer")
        covering: List[str] = []
        for window_id, (start, end) in self._coverage_ranges.items():
            if start <= tick <= end:
                covering.append(window_id)
        return sorted(covering)

    def _reindex(self) -> None:
        self._coverage_ranges.clear()
        self._parent_lookup.clear()
        for window in self.grammar.base_windows.values():
            self._parent_lookup[window.window_id] = window.parent_id
        for window in self.grammar.derived_windows.values():
            self._parent_lookup[window.window_id] = window.parent_id

        cache: Dict[str, tuple[int, int]] = {}
        visited: Set[str] = set()
        for window_id in self.grammar.window_ids():
            self._coverage_ranges[window_id] = self._compute_range(window_id, cache=cache, visited=visited)

    def _compute_range(
        self, window_id: str, *, cache: Dict[str, tuple[int, int]], visited: Set[str]
    ) -> tuple[int, int]:
        if window_id in cache:
            return cache[window_id]
        if window_id in visited:
            raise ValueError(f"Cyclic window dependency detected at '{window_id}'")
        visited.add(window_id)

        if window_id in self.grammar.base_windows:
            window = self.grammar.base_windows[window_id]
            start_end = (window.tick_start, window.tick_end)
        else:
            window = self.grammar.derived_windows[window_id]
            ranges = [self._compute_range(src, cache=cache, visited=visited) for src in window.source_ids]
            starts, ends = zip(*ranges)
            start_end = (min(starts), max(ends))

        cache[window_id] = start_end
        visited.remove(window_id)
        return start_end


def build_registry_from_press_windows(
    window_specs: Iterable["TickLoopWindowSpec"],
    manifests: Mapping[str, "APXManifestV1"] | None = None,
) -> AEONWindowRegistry:
    """Create an AEON registry from TickLoop/Press window specs.

    Each Press window becomes a base AEON window with Loom-aligned tick ranges and
    a `press_window_id` referencing the manifest or APX name.
    """

    base_windows: Dict[str, AEONWindowDefV1] = {}
    for spec in window_specs:
        press_window_id = spec.apx_name
        if manifests and spec.apx_name in manifests:
            press_window_id = manifests[spec.apx_name].apx_name
        base_windows[spec.window_id] = AEONWindowDefV1(
            window_id=spec.window_id,
            tick_start=spec.start_tick,
            tick_end=spec.end_tick,
            labels=("press",),
            press_window_id=press_window_id,
        )

    return AEONWindowRegistry.from_windows(base_windows=base_windows, derived_windows={})


def _require_str(data: Mapping[str, object], key: str, *, default: str | None = None) -> str:
    if key not in data:
        if default is not None:
            return default
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, str) or not value:
        raise TypeError(f"Field '{key}' must be a non-empty string")
    return value


def _require_int(data: Mapping[str, object], key: str) -> int:
    if key not in data:
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, int):
        raise TypeError(f"Field '{key}' must be an integer")
    return value


def _require_labels(value: object) -> Sequence[str]:
    if value is None:
        return ()
    if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
        raise TypeError("labels must be an iterable of strings")
    labels: List[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise TypeError("labels must be non-empty strings")
        labels.append(item)
    return tuple(labels)


def _require_optional_str(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise TypeError("optional string fields must be non-empty strings when provided")
    return value


def _require_str_list(data: Mapping[str, object], key: str) -> Sequence[str]:
    if key not in data:
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
        raise TypeError(f"Field '{key}' must be an iterable of strings")
    result: List[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise TypeError(f"Field '{key}' must contain non-empty strings")
        result.append(item)
    if not result:
        raise ValueError(f"Field '{key}' must be non-empty")
    return tuple(result)


def _require_mapping(data: Mapping[str, object], key: str) -> Mapping[str, Mapping[str, object]]:
    if key not in data:
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, Mapping):
        raise TypeError(f"Field '{key}' must be a mapping")
    return value  # type: ignore[return-value]


def _validate_labels(labels: Sequence[str]) -> None:
    for label in labels:
        if not isinstance(label, str) or not label:
            raise TypeError("labels must be non-empty strings")


def _validate_parent(parent_id: str | None, known_ids: set[str], window_id: str) -> None:
    if parent_id is None:
        return
    if not isinstance(parent_id, str) or not parent_id:
        raise TypeError("parent_id must be a non-empty string when provided")
    if parent_id not in known_ids:
        raise ValueError(f"parent_id '{parent_id}' is not defined in grammar")
    if parent_id == window_id:
        raise ValueError("window cannot be its own parent")
