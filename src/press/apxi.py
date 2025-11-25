"""APXi descriptor primitives, validation, and MDL accounting (v1)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from press.press import compute_gr_mode_lengths, compute_id_mode_lengths, compute_r_mode_lengths


APXI_PRIMITIVE_CONST = "CONST_SEGMENT"
APXI_PRIMITIVE_RUN = "RUN_SEGMENT"
APXI_PRIMITIVE_LINEAR = "LINEAR_TREND"
APXI_PRIMITIVES = {APXI_PRIMITIVE_CONST, APXI_PRIMITIVE_RUN, APXI_PRIMITIVE_LINEAR}

_SUPPORTED_RESIDUAL_SCHEMES = {
    "ID": compute_id_mode_lengths,
    "R": compute_r_mode_lengths,
    "GR": compute_gr_mode_lengths,
}

# Public alias for consumers that need to validate schemes without importing internals.
SUPPORTED_APXI_RESIDUAL_SCHEMES = tuple(_SUPPORTED_RESIDUAL_SCHEMES.keys())


@dataclass(frozen=True)
class APXiDescriptorV1:
    """Descriptor describing a Press stream segment over an AEON window."""

    descriptor_id: str
    descriptor_type: str
    window_id: str
    stream_id: str
    params: Mapping[str, object]
    labels: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.descriptor_id, str) or not self.descriptor_id:
            raise ValueError("descriptor_id must be a non-empty string")
        if self.descriptor_type not in APXI_PRIMITIVES:
            raise ValueError(f"descriptor_type must be one of {sorted(APXI_PRIMITIVES)}")
        if not isinstance(self.window_id, str) or not self.window_id:
            raise ValueError("window_id must be a non-empty string")
        if not isinstance(self.stream_id, str) or not self.stream_id:
            raise ValueError("stream_id must be a non-empty string")
        _validate_labels(self.labels)

        params_dict = _normalize_params(self.descriptor_type, self.params)
        object.__setattr__(self, "params", params_dict)

    def to_dict(self) -> Dict[str, object]:
        params_obj: Dict[str, object] = dict(self.params)
        pattern = params_obj.get("pattern")
        if pattern is not None:
            params_obj["pattern"] = list(pattern)  # type: ignore[arg-type]

        return {
            "descriptor_id": self.descriptor_id,
            "descriptor_type": self.descriptor_type,
            "window_id": self.window_id,
            "stream_id": self.stream_id,
            "params": params_obj,
            "labels": list(self.labels),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "APXiDescriptorV1":
        return cls(
            descriptor_id=_require_str(data, "descriptor_id"),
            descriptor_type=_require_str(data, "descriptor_type"),
            window_id=_require_str(data, "window_id"),
            stream_id=_require_str(data, "stream_id"),
            params=_require_mapping(data, "params"),
            labels=tuple(_require_labels(data.get("labels", ()))),
        )

    @classmethod
    def from_json(cls, text: str) -> "APXiDescriptorV1":
        return cls.from_dict(json.loads(text))


@dataclass(frozen=True)
class APXiMDLBreakdown:
    """MDL accounting results for an APXi descriptor over a concrete sequence."""

    descriptor: APXiDescriptorV1
    residual_scheme: str
    L_model: int
    L_residual: int
    L_total: int

    def __post_init__(self) -> None:
        if self.residual_scheme not in _SUPPORTED_RESIDUAL_SCHEMES:
            raise ValueError("Unsupported residual_scheme")
        if self.L_total != self.L_model + self.L_residual:
            raise ValueError("L_total must equal L_model + L_residual")


@dataclass(frozen=True)
class APXiViewV1:
    """Companion view that attaches APXi breakdowns to a Press/APX window."""

    apx_name: str
    window_id: str
    aeon_window_id: str | None
    residual_scheme: str
    descriptors_by_stream: Dict[str, Tuple[APXiMDLBreakdown, ...]]

    _BreakdownType = APXiMDLBreakdown

    def __post_init__(self) -> None:
        if self.residual_scheme not in _SUPPORTED_RESIDUAL_SCHEMES:
            raise ValueError("Unsupported residual_scheme for APXiViewV1")
        normalized: Dict[str, Tuple[APXiMDLBreakdown, ...]] = {}
        for stream_name, breakdowns in self.descriptors_by_stream.items():
            normalized[stream_name] = tuple(breakdowns)
        object.__setattr__(self, "descriptors_by_stream", normalized)

    @property
    def view_id(self) -> str:
        suffix = self.aeon_window_id or self.window_id
        return f"{self.apx_name}::{suffix}::APXiView_v1"

    def to_dict(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "apx_name": self.apx_name,
            "window_id": self.window_id,
            "aeon_window_id": self.aeon_window_id,
            "residual_scheme": self.residual_scheme,
            "descriptors_by_stream": {},
        }
        for stream_name, breakdowns in self.descriptors_by_stream.items():
            result["descriptors_by_stream"][stream_name] = [
                {
                    "descriptor": breakdown.descriptor.to_dict(),
                    "residual_scheme": breakdown.residual_scheme,
                    "L_model": breakdown.L_model,
                    "L_residual": breakdown.L_residual,
                    "L_total": breakdown.L_total,
                }
                for breakdown in breakdowns
            ]
        return result


def compute_apxi_lengths(
    values: Sequence[Sequence[int]],
    descriptor: APXiDescriptorV1,
    *,
    residual_scheme: str = "R",
) -> Dict[str, int]:
    """Return MDL bit counts for a descriptor applied to a concrete sequence.

    The descriptor acts as the model (``L_model``) and residuals are encoded
    with the chosen residual scheme (``L_residual``). All arithmetic is
    integer-only and deterministic.
    """

    breakdown = compute_apxi_breakdown(
        values, descriptor, residual_scheme=residual_scheme
    )
    return {
        "L_model": breakdown.L_model,
        "L_residual": breakdown.L_residual,
        "L_total": breakdown.L_total,
    }


def compute_apxi_breakdown(
    values: Sequence[Sequence[int]],
    descriptor: APXiDescriptorV1,
    *,
    residual_scheme: str = "R",
) -> APXiMDLBreakdown:
    """Compute a deterministic MDL breakdown for an APXi descriptor."""

    if residual_scheme not in _SUPPORTED_RESIDUAL_SCHEMES:
        raise ValueError("residual_scheme must be one of 'ID', 'R', 'GR'")

    normalized_values = [_as_tuple(value) for value in values]
    if not normalized_values:
        return APXiMDLBreakdown(
            descriptor=descriptor,
            residual_scheme=residual_scheme,
            L_model=0,
            L_residual=0,
            L_total=0,
        )

    width = _ensure_consistent_width(normalized_values)
    predicted = _render_descriptor(descriptor, length=len(normalized_values), width=width)
    residuals = _compute_residuals(normalized_values, predicted)

    L_model = _model_cost(descriptor, length=len(normalized_values), width=width)
    residual_lengths = _compute_residual_lengths(residuals, scheme=residual_scheme)
    L_residual = residual_lengths["L_residual"]
    L_total = L_model + L_residual

    return APXiMDLBreakdown(
        descriptor=descriptor,
        residual_scheme=residual_scheme,
        L_model=L_model,
        L_residual=L_residual,
        L_total=L_total,
    )


def _normalize_params(descriptor_type: str, params: Mapping[str, object]) -> Dict[str, object]:
    if not isinstance(params, Mapping):
        raise TypeError("params must be a mapping")
    if descriptor_type == APXI_PRIMITIVE_CONST:
        return _normalize_const_params(params)
    if descriptor_type == APXI_PRIMITIVE_RUN:
        return _normalize_run_params(params)
    if descriptor_type == APXI_PRIMITIVE_LINEAR:
        return _normalize_linear_params(params)
    raise ValueError(f"Unsupported descriptor_type '{descriptor_type}'")


def _normalize_const_params(params: Mapping[str, object]) -> Dict[str, object]:
    if set(params.keys()) != {"value"}:
        raise ValueError("CONST_SEGMENT params must only contain 'value'")
    value = params.get("value")
    if not isinstance(value, int):
        raise TypeError("CONST_SEGMENT value must be an integer")
    return {"value": value}


def _normalize_run_params(params: Mapping[str, object]) -> Dict[str, object]:
    expected_keys = {"pattern", "repeats"}
    if set(params.keys()) != expected_keys:
        raise ValueError("RUN_SEGMENT params must contain exactly 'pattern' and 'repeats'")
    pattern_raw = params.get("pattern")
    if not isinstance(pattern_raw, Sequence) or isinstance(pattern_raw, (str, bytes)):
        raise TypeError("RUN_SEGMENT pattern must be a non-empty sequence of integers")
    pattern: list[int] = []
    for entry in pattern_raw:
        if not isinstance(entry, int):
            raise TypeError("RUN_SEGMENT pattern entries must be integers")
        pattern.append(entry)
    if not pattern:
        raise ValueError("RUN_SEGMENT pattern must be non-empty")

    repeats = params.get("repeats")
    if not isinstance(repeats, int):
        raise TypeError("RUN_SEGMENT repeats must be an integer")
    if repeats < 1:
        raise ValueError("RUN_SEGMENT repeats must be >= 1")

    return {"pattern": tuple(pattern), "repeats": repeats}


def _normalize_linear_params(params: Mapping[str, object]) -> Dict[str, object]:
    allowed_keys = {"intercept", "slope", "start_tick"}
    if not set(params.keys()).issubset(allowed_keys):
        raise ValueError("LINEAR_TREND params contain unknown fields")

    intercept = params.get("intercept")
    slope = params.get("slope")
    if intercept is None or slope is None:
        raise ValueError("LINEAR_TREND params must include 'intercept' and 'slope'")
    if not isinstance(intercept, int) or not isinstance(slope, int):
        raise TypeError("LINEAR_TREND intercept and slope must be integers")

    start_tick = params.get("start_tick", 0)
    if not isinstance(start_tick, int):
        raise TypeError("LINEAR_TREND start_tick must be an integer")

    return {"intercept": intercept, "slope": slope, "start_tick": start_tick}


def _ensure_consistent_width(values: Sequence[Tuple[int, ...]]) -> int:
    width = len(values[0])
    for value in values:
        if len(value) != width:
            raise ValueError("All values must share the same width")
    return width


def _as_tuple(value: Sequence[int]) -> Tuple[int, ...]:
    if isinstance(value, (list, tuple)):
        if not value:
            return ()
        for entry in value:
            if not isinstance(entry, int):
                raise TypeError("APXi values must be integers")
        return tuple(value)
    if not isinstance(value, int):
        raise TypeError("APXi values must be integers")
    return (value,)


def _render_descriptor(
    descriptor: APXiDescriptorV1, *, length: int, width: int
) -> List[Tuple[int, ...]]:
    if length <= 0:
        return []
    if descriptor.descriptor_type == APXI_PRIMITIVE_CONST:
        return [tuple(descriptor.params["value"] for _ in range(width))] * length
    if descriptor.descriptor_type == APXI_PRIMITIVE_RUN:
        pattern = descriptor.params["pattern"]
        repeats = descriptor.params["repeats"]
        if width != 1:
            raise ValueError("RUN_SEGMENT currently supports width=1 streams")
        expanded = list(pattern) * repeats
        if len(expanded) != length:
            raise ValueError("RUN_SEGMENT pattern length does not cover the window")
        return [(value,) for value in expanded]
    if descriptor.descriptor_type == APXI_PRIMITIVE_LINEAR:
        intercept = descriptor.params["intercept"]
        slope = descriptor.params["slope"]
        start_tick = descriptor.params["start_tick"]
        return [
            tuple(intercept + slope * (start_tick + idx) for _ in range(width))
            for idx in range(length)
        ]
    raise ValueError(f"Unsupported descriptor_type '{descriptor.descriptor_type}'")


def _compute_residuals(
    values: Sequence[Tuple[int, ...]], predicted: Sequence[Tuple[int, ...]]
) -> List[Tuple[int, ...]]:
    if len(values) != len(predicted):
        raise ValueError("Residual computation requires matching lengths")
    residuals: List[Tuple[int, ...]] = []
    for observed, expected in zip(values, predicted):
        if len(observed) != len(expected):
            raise ValueError("Residual computation requires matching widths")
        residuals.append(tuple(o - e for o, e in zip(observed, expected)))
    return residuals


def _model_cost(descriptor: APXiDescriptorV1, *, length: int, width: int) -> int:
    """Return a deterministic model bit cost for the descriptor."""

    if descriptor.descriptor_type == APXI_PRIMITIVE_CONST:
        base = 1
        return base

    if descriptor.descriptor_type == APXI_PRIMITIVE_RUN:
        pattern: Tuple[int, ...] = descriptor.params["pattern"]
        _ = descriptor.params["repeats"]
        base = 1
        return base

    if descriptor.descriptor_type == APXI_PRIMITIVE_LINEAR:
        intercept = descriptor.params["intercept"]
        slope = descriptor.params["slope"]
        start_tick = descriptor.params["start_tick"]
        base = 3
        offset_cost = 1 if start_tick else 0
        slope_cost = 1 if slope else 0
        intercept_cost = 1 if intercept else 0
        width_cost = 1 if width > 1 else 0
        return base + offset_cost + slope_cost + intercept_cost + width_cost

    raise ValueError(f"Unsupported descriptor_type '{descriptor.descriptor_type}'")


def _compute_residual_lengths(
    residuals: Sequence[Tuple[int, ...]], *, scheme: str
) -> Dict[str, int]:
    if not residuals:
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    if _all_zero(residuals):
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    handler = _SUPPORTED_RESIDUAL_SCHEMES[scheme]
    return handler(residuals)


def _int_cost(value: int) -> int:
    return max(1, abs(int(value)).bit_length() + 1)


def _all_zero(residuals: Iterable[Tuple[int, ...]]) -> bool:
    return all(all(entry == 0 for entry in residual) for residual in residuals)


def _require_str(data: Mapping[str, object], key: str) -> str:
    if key not in data:
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, str) or not value:
        raise TypeError(f"Field '{key}' must be a non-empty string")
    return value


def _require_mapping(data: Mapping[str, object], key: str) -> Mapping[str, object]:
    if key not in data:
        raise KeyError(f"Missing required field '{key}'")
    value = data[key]
    if not isinstance(value, Mapping):
        raise TypeError(f"Field '{key}' must be a mapping")
    return value


def _require_labels(value: object) -> Sequence[str]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise TypeError("labels must be an iterable of strings")
    labels: list[str] = []
    for entry in value:
        if not isinstance(entry, str) or not entry:
            raise TypeError("labels must contain non-empty strings")
        labels.append(entry)
    return tuple(labels)


def _validate_labels(labels: Sequence[str]) -> None:
    for label in labels:
        if not isinstance(label, str) or not label:
            raise TypeError("labels must contain non-empty strings")
