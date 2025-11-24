"""Minimal CMP-0 Press/APX implementation for GF-01."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence

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
    streams: List[APXStreamV1] = field(default_factory=list)


@dataclass
class PressStreamBufferV1:
    """Buffered data for a single stream."""

    name: str
    scheme_hint: str
    description: str
    values: List[Sequence[int]] = field(default_factory=list)


def _value_width(value: Sequence[int]) -> int:
    if isinstance(value, (list, tuple)):
        return len(value)
    return 1


def compute_r_mode_lengths(values: Sequence[Sequence[int]]) -> Dict[str, int]:
    """Return model/residual/total bit counts for simple R-mode.

    R-mode here is intentionally minimal for GF-01 parity: the model cost is 0,
    residual cost grows with the number of tick-aligned entries, plus a small
    bump when the tuple width suggests a wider flux vector.
    """

    if not values:
        return {"L_model": 0, "L_residual": 0, "L_total": 0}

    width = _value_width(values[0])
    L_model = 0
    L_residual = max(0, len(values) - 1)
    if width >= 8:
        L_residual += 1
    L_total = L_model + L_residual
    return {"L_model": L_model, "L_residual": L_residual, "L_total": L_total}


def compute_manifest_check(
    apx_name: str, profile: ProfileCMP0V1, streams: Iterable[APXStreamV1]
) -> int:
    """Compute a deterministic manifest_check using an affine FNV-style hash."""

    modulus = profile.modulus_M
    fnv_offset = 2_166_136_261 % modulus
    fnv_prime = 16_777_619

    def _mix(value: int, acc: int) -> int:
        return ((acc ^ value) * fnv_prime) % modulus

    acc = fnv_offset
    for ch in (apx_name + profile.name):
        acc = _mix(ord(ch), acc)
    for stream in streams:
        acc = _mix(stream.L_total, acc)

    b1 = 52_662_887
    b0 = 325_581_713
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
    ) -> None:
        self.gid = gid
        self.run_id = run_id
        self.window_id = window_id
        self.start_tick = start_tick
        self.end_tick = end_tick
        self.profile = profile
        self.default_scheme = profile.press_defaults.get("preferred_schemes", ["R"])[0]
        self.streams: Dict[str, PressStreamBufferV1] = {}

    def register_stream(self, name: str, scheme_hint: str | None = None, description: str = "") -> None:
        if name in self.streams:
            return
        self.streams[name] = PressStreamBufferV1(
            name=name,
            scheme_hint=scheme_hint or self.default_scheme,
            description=description or name,
        )

    def append(self, name: str, value: Sequence[int]) -> None:
        if name not in self.streams:
            raise KeyError(f"Stream '{name}' is not registered")
        self.streams[name].values.append(value)

    def close_window(self, apx_name: str) -> APXManifestV1:
        apx_streams: List[APXStreamV1] = []
        for stream in self.streams.values():
            lengths = compute_r_mode_lengths(stream.values)
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

        manifest_check = compute_manifest_check(apx_name, self.profile, apx_streams)
        return APXManifestV1(
            apx_name=apx_name,
            profile=self.profile.name,
            manifest_check=manifest_check,
            streams=apx_streams,
        )

