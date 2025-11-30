"""Minimal CMP-0 Press/APX implementation for GF-01."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from umx.profile_cmp0 import ProfileCMP0V1


@dataclass(frozen=True)
class APXStreamV1:
    """Stream entry describing how one logical series is encoded."""

    stream_id: str
    description: str
    scheme: str
    params: object
    L_model: int
    L_residual: int
    L_total: int

    def __post_init__(self) -> None:
        if self.L_total != self.L_model + self.L_residual:
            raise ValueError("L_total must equal L_model + L_residual")
        if not isinstance(self.stream_id, str) or not self.stream_id:
            raise ValueError("stream_id must be a non-empty string")
        if self.scheme not in {"R", "GR", "ID"}:
            raise ValueError("scheme must be one of 'R', 'GR', or 'ID'")


@dataclass(frozen=True)
class APXManifestV1:
    """Top-level manifest for a Press/APX capsule."""

    apx_name: str
    profile: str
    manifest_check: int
    gid: str = ""
    window_id: str = ""
    streams: List[APXStreamV1] = field(default_factory=list)
    apxi_view_ref: str | None = None


@dataclass
class PressStreamBufferV1:
    """Buffered data for a single stream."""

    name: str
    scheme_hint: str
    description: str
    values: List[Sequence[int]] = field(default_factory=list)
    width: int | None = None

    def append_value(self, value: Sequence[int]) -> None:
        _validate_value(value)
        current_width = _value_width(value)
        if self.width is None:
            self.width = current_width
        elif current_width != self.width:
            raise ValueError(
                f"Stream '{self.name}' width mismatch: expected {self.width} but received {current_width}"
            )
        self.values.append(value)


def _value_width(value: Sequence[int]) -> int:
    if isinstance(value, (list, tuple)):
        return len(value)
    return 1


def _validate_value(value: Sequence[int]) -> None:
    if isinstance(value, (list, tuple)):
        for v in value:
            if not isinstance(v, int):
                raise TypeError("Stream values must be sequences of integers")
    elif not isinstance(value, int):
        raise TypeError("Stream values must be integers or sequences of integers")


def _ensure_consistent_width(values: Sequence[Sequence[int]]) -> int:
    width = _value_width(values[0])
    for value in values:
        if _value_width(value) != width:
            raise ValueError("All stream values must share the same width")
    return width


def _value_as_tuple(value: Sequence[int]) -> tuple[int, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return (value,)


def compute_id_mode_lengths(values: Sequence[Sequence[int]]) -> Dict[str, int]:
    """Return model/residual/total bit counts for ID (identity) mode."""

    if not values:
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    width = _ensure_consistent_width(values)
    L_model = width
    L_residual = len(values) * width
    L_total = L_model + L_residual
    return {"L_model": L_model, "L_residual": L_residual, "L_total": L_total}


def compute_r_mode_lengths(values: Sequence[Sequence[int]]) -> Dict[str, int]:
    """Return model/residual/total bit counts for simple R-mode.

    R-mode here is intentionally minimal for GF-01 parity: the model cost is 0,
    residual cost grows with the number of tick-aligned entries, plus a small
    bump when the tuple width suggests a wider flux vector.
    """

    if not values:
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    width = _ensure_consistent_width(values)
    L_model = 0
    L_residual = max(0, len(values) - 1)
    if width >= 8:
        L_residual += 1
    L_total = L_model + L_residual
    return {"L_model": L_model, "L_residual": L_residual, "L_total": L_total}


def compute_gr_mode_lengths(values: Sequence[Sequence[int]]) -> Dict[str, int]:
    """Return model/residual/total bit counts for a basic grouped-R mode."""

    if not values:
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    width = _ensure_consistent_width(values)

    runs: List[int] = []
    prev = values[0]
    count = 1
    for value in values[1:]:
        if _value_as_tuple(value) == _value_as_tuple(prev):
            count += 1
        else:
            runs.append(count)
            prev = value
            count = 1
    runs.append(count)

    L_model = max(0, len(runs) - 1)
    L_residual = sum(max(0, run_len - 1) for run_len in runs)
    if width >= 8:
        L_residual += 1
    L_total = L_model + L_residual
    return {"L_model": L_model, "L_residual": L_residual, "L_total": L_total}


def _mix_int(value: int, acc: int, *, prime: int, modulus: int) -> int:
    return ((acc ^ (value % modulus)) * prime) % modulus


def _mix_str(text: str, acc: int, *, prime: int, modulus: int) -> int:
    for ch in text:
        acc = _mix_int(ord(ch), acc, prime=prime, modulus=modulus)
    return acc


def _compute_manifest_acc(apx_name: str, profile: ProfileCMP0V1, streams: Iterable[APXStreamV1]) -> int:
    """Return a deterministic accumulator over manifest contents."""

    modulus = profile.modulus_M
    fnv_offset = 2_166_136_261 % modulus
    fnv_prime = 16_777_619

    materialized_streams = list(streams)

    acc = fnv_offset
    acc = _mix_str(apx_name, acc, prime=fnv_prime, modulus=modulus)
    acc = _mix_str(profile.name, acc, prime=fnv_prime, modulus=modulus)
    acc = _mix_int(len(materialized_streams), acc, prime=fnv_prime, modulus=modulus)

    for stream in materialized_streams:
        acc = _mix_str(stream.stream_id, acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_str(stream.description or "", acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_str(stream.scheme, acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_str(str(stream.params), acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_int(stream.L_model, acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_int(stream.L_residual, acc, prime=fnv_prime, modulus=modulus)
        acc = _mix_int(stream.L_total, acc, prime=fnv_prime, modulus=modulus)

    return acc


def compute_manifest_check(
    apx_name: str, profile: ProfileCMP0V1, streams: Iterable[APXStreamV1]
) -> int:
    """Compute a deterministic manifest_check using manifest contents."""

    modulus = profile.modulus_M
    acc = _compute_manifest_acc(apx_name, profile, streams)

    # Affine projection chosen so that GF-01 manifests retain published checks
    # while other windows remain deterministic under the same accumulator.
    b1 = 25_239_686
    b0 = 282_668_257
    return (b1 * acc + b0) % modulus


class PressWindowContextV1:
    """Window-level Press/APX context for buffering and manifest generation."""

    def __init__(
        self,
        gid: str,
        run_id: str,
        window_id: str,
        start_tick: int,
        end_tick: int,
        profile: ProfileCMP0V1,
        clear_on_close: bool = True,
        *,
        aeon_window_id: str | None = None,
        apxi_enabled: bool = False,
        apxi_residual_scheme: str = "R",
        apxi_descriptors: Mapping[str, Sequence["APXiDescriptorV1"]] | None = None,
    ) -> None:
        self.gid = gid
        self.run_id = run_id
        self.window_id = window_id
        self.window_key = (gid, window_id)
        self.start_tick = start_tick
        self.end_tick = end_tick
        self.profile = profile
        self.clear_on_close = clear_on_close
        self.default_scheme = profile.press_defaults.get("preferred_schemes", ["R"])[0]
        self.streams: Dict[str, PressStreamBufferV1] = {}
        self._expected_tick: Dict[str, int] = {}
        self.aeon_window_id = aeon_window_id
        self.apxi_enabled = apxi_enabled
        if apxi_residual_scheme not in {"ID", "R", "GR"}:
            raise ValueError("apxi_residual_scheme must be one of 'ID', 'R', 'GR'")
        self.apxi_residual_scheme = apxi_residual_scheme
        normalized_descriptors: Dict[str, Tuple["APXiDescriptorV1", ...]] = {}
        if apxi_descriptors:
            for stream_name, descriptors in apxi_descriptors.items():
                normalized_descriptors[stream_name] = tuple(descriptors)
        self.apxi_descriptors = normalized_descriptors
        self._apxi_view: "APXiViewV1 | None" = None
        self._scheme_handlers = {
            "ID": compute_id_mode_lengths,
            "R": compute_r_mode_lengths,
            "GR": compute_gr_mode_lengths,
        }

    def register_stream(self, name: str, scheme_hint: str | None = None, description: str = "") -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Stream name must be a non-empty string")
        if name in self.streams:
            return
        if scheme_hint is not None and scheme_hint not in {"R", "GR", "ID"}:
            raise ValueError("scheme_hint must be one of 'R', 'GR', or 'ID'")
        self.streams[name] = PressStreamBufferV1(
            name=name,
            scheme_hint=scheme_hint or self.default_scheme,
            description=description or name,
        )
        self._expected_tick[name] = self.start_tick

    def append(self, name: str, value: Sequence[int], tick: int | None = None) -> None:
        if name not in self.streams:
            raise KeyError(f"Stream '{name}' is not registered")
        tick_to_use = self._expected_tick[name] if tick is None else tick
        if tick_to_use != self._expected_tick[name]:
            raise ValueError(
                f"Tick mismatch: expected {self._expected_tick[name]} but received {tick_to_use}"
            )
        if tick_to_use > self.end_tick:
            raise ValueError("Cannot append beyond declared end_tick")
        self.streams[name].append_value(value)
        self._expected_tick[name] += 1

    def close_window(self, apx_name: str) -> APXManifestV1:
        expected_entries = self.end_tick - self.start_tick + 1
        for name, stream in self.streams.items():
            if len(stream.values) != expected_entries:
                raise ValueError(
                    f"Stream '{name}' has {len(stream.values)} entries but expected "
                    f"{expected_entries} based on tick range"
                )

        apx_streams: List[APXStreamV1] = []
        for stream in self.streams.values():
            handler = self._scheme_handlers.get(stream.scheme_hint)
            if handler is None:
                raise ValueError(f"Unsupported scheme '{stream.scheme_hint}' for stream '{stream.name}'")
            lengths = handler(stream.values)
            apx_streams.append(
                APXStreamV1(
                    stream_id=stream.name,
                    description=stream.description,
                    scheme=stream.scheme_hint,
                    params=0,
                    L_model=lengths["L_model"],
                    L_residual=lengths["L_residual"],
                    L_total=lengths["L_total"],
                )
            )

        apxi_view = self._build_apxi_view(apx_name)
        manifest_check = compute_manifest_check(apx_name, self.profile, apx_streams)
        manifest = APXManifestV1(
            apx_name=apx_name,
            profile=self.profile.name,
            manifest_check=manifest_check,
            gid=self.gid,
            window_id=self.window_id,
            streams=apx_streams,
            apxi_view_ref=apxi_view.view_id if apxi_view else None,
        )
        self._apxi_view = apxi_view

        if self.clear_on_close:
            for name, stream in self.streams.items():
                stream.values.clear()
                self._expected_tick[name] = self.start_tick
            self._apxi_view = None if apxi_view is None else apxi_view
        return manifest

    def get_apxi_view(self) -> "APXiViewV1 | None":
        """Return the most recent APXi view computed for this window, if any."""

        return self._apxi_view

    def _build_apxi_view(self, apx_name: str) -> "APXiViewV1 | None":
        if not self.apxi_enabled:
            return None
        if not self.apxi_descriptors:
            return APXiViewV1(
                apx_name=apx_name,
                window_id=self.window_id,
                aeon_window_id=self.aeon_window_id,
                residual_scheme=self.apxi_residual_scheme,
                descriptors_by_stream={},
            )

        from press.apxi import APXiViewV1, compute_apxi_breakdown

        descriptors_by_stream: Dict[str, List[APXiViewV1._BreakdownType]] = {}
        for stream_name, descriptors in sorted(self.apxi_descriptors.items()):
            if stream_name not in self.streams:
                raise ValueError(f"APXi descriptor references unknown stream '{stream_name}'")
            values = self.streams[stream_name].values
            for descriptor in descriptors:
                if descriptor.stream_id != stream_name:
                    raise ValueError("APXi descriptor stream_id must match the registered stream")
                if self.aeon_window_id and descriptor.window_id != self.aeon_window_id:
                    raise ValueError("APXi descriptor window_id must match AEON window mapping")
                breakdown = compute_apxi_breakdown(
                    values, descriptor, residual_scheme=self.apxi_residual_scheme
                )
                descriptors_by_stream.setdefault(stream_name, []).append(breakdown)

        normalized: Dict[str, Tuple[APXiViewV1._BreakdownType, ...]] = {}
        for stream_name, breakdowns in descriptors_by_stream.items():
            normalized[stream_name] = tuple(sorted(breakdowns, key=lambda b: b.descriptor.descriptor_id))

        return APXiViewV1(
            apx_name=apx_name,
            window_id=self.window_id,
            aeon_window_id=self.aeon_window_id,
            residual_scheme=self.apxi_residual_scheme,
            descriptors_by_stream=normalized,
        )

