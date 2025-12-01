"""SimA encoders/decoders for ID/ΔR/GR streams with MDL scoring."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, Iterable, List, Sequence, Tuple

from press.press import (
    APXStreamV1,
    PressStreamBufferV1,
    _ensure_consistent_width,
    _value_as_tuple,
    compute_gr_mode_lengths,
    compute_id_mode_lengths,
    compute_r_mode_lengths,
)


def _zigzag_encode(value: int) -> int:
    return (value << 1) ^ (value >> 63)


def _zigzag_decode(value: int) -> int:
    return (value >> 1) ^ -(value & 1)


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("varint values must be non-negative after zigzag encoding")
    out = bytearray()
    remaining = value
    while True:
        to_write = remaining & 0x7F
        remaining >>= 7
        if remaining:
            out.append(0x80 | to_write)
        else:
            out.append(to_write)
            break
    return bytes(out)


def _decode_varint(payload: bytes, offset: int) -> Tuple[int, int]:
    shift = 0
    value = 0
    idx = offset
    while True:
        if idx >= len(payload):
            raise ValueError("Unexpected end of payload while decoding varint")
        byte = payload[idx]
        idx += 1
        value |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return value, idx


def _varint_bits(value: int) -> int:
    return len(_encode_varint(value)) * 8


def _encode_header(width: int, count: int) -> bytearray:
    encoded = bytearray()
    encoded.extend(_encode_varint(width))
    encoded.extend(_encode_varint(count))
    return encoded


def _normalize_values(values: Sequence[Sequence[int]]) -> Tuple[int, Tuple[Tuple[int, ...], ...]]:
    width = _ensure_consistent_width(values)
    normalized: List[Tuple[int, ...]] = []
    for value in values:
        normalized.append(_value_as_tuple(value))
    return width, tuple(normalized)


def _encode_id(values: Sequence[Sequence[int]]) -> bytes:
    width, normalized = _normalize_values(values)
    encoded = _encode_header(width, len(normalized))
    for entry in normalized:
        for component in entry:
            encoded.extend(_encode_varint(_zigzag_encode(component)))
    return bytes(encoded)


def _encode_r(values: Sequence[Sequence[int]]) -> bytes:
    width, normalized = _normalize_values(values)
    if not normalized:
        return bytes(_encode_header(width, 0))
    encoded = _encode_header(width, len(normalized))
    prev = normalized[0]
    for component in prev:
        encoded.extend(_encode_varint(_zigzag_encode(component)))
    for entry in normalized[1:]:
        deltas = tuple(current - base for current, base in zip(entry, prev))
        for delta in deltas:
            encoded.extend(_encode_varint(_zigzag_encode(delta)))
        prev = entry
    return bytes(encoded)


def _encode_gr(values: Sequence[Sequence[int]]) -> bytes:
    width, normalized = _normalize_values(values)
    if not normalized:
        return bytes(_encode_header(width, 0))
    runs: List[Tuple[int, Tuple[int, ...]]] = []
    prev = normalized[0]
    count = 1
    for entry in normalized[1:]:
        if entry == prev:
            count += 1
        else:
            runs.append((count, prev))
            prev = entry
            count = 1
    runs.append((count, prev))

    encoded = _encode_header(width, len(runs))
    for run_len, value in runs:
        encoded.extend(_encode_varint(run_len))
        for component in value:
            encoded.extend(_encode_varint(_zigzag_encode(component)))
    return bytes(encoded)


def _decode_id(payload: bytes) -> List[Sequence[int]]:
    offset = 0
    width, offset = _decode_varint(payload, offset)
    count, offset = _decode_varint(payload, offset)
    output: List[Sequence[int]] = []
    for _ in range(count):
        entry: List[int] = []
        for _ in range(width):
            raw, offset = _decode_varint(payload, offset)
            entry.append(_zigzag_decode(raw))
        output.append(entry[0] if width == 1 else tuple(entry))
    return output


def _decode_r(payload: bytes) -> List[Sequence[int]]:
    offset = 0
    width, offset = _decode_varint(payload, offset)
    count, offset = _decode_varint(payload, offset)
    if count == 0:
        return []
    output: List[Sequence[int]] = []
    first: List[int] = []
    for _ in range(width):
        raw, offset = _decode_varint(payload, offset)
        first.append(_zigzag_decode(raw))
    output.append(first[0] if width == 1 else tuple(first))
    prev = tuple(first)
    for _ in range(count - 1):
        deltas: List[int] = []
        for _ in range(width):
            raw, offset = _decode_varint(payload, offset)
            deltas.append(_zigzag_decode(raw))
        entry = tuple(base + delta for base, delta in zip(prev, deltas))
        output.append(entry[0] if width == 1 else entry)
        prev = entry
    return output


def _decode_gr(payload: bytes) -> List[Sequence[int]]:
    offset = 0
    width, offset = _decode_varint(payload, offset)
    run_count, offset = _decode_varint(payload, offset)
    output: List[Sequence[int]] = []
    for _ in range(run_count):
        run_len, offset = _decode_varint(payload, offset)
        entry: List[int] = []
        for _ in range(width):
            raw, offset = _decode_varint(payload, offset)
            entry.append(_zigzag_decode(raw))
        value = entry[0] if width == 1 else tuple(entry)
        output.extend([value] * run_len)
    return output


_ENCODERS = {
    "ID": _encode_id,
    "R": _encode_r,
    "GR": _encode_gr,
}

_DECODERS = {
    "ID": _decode_id,
    "R": _decode_r,
    "GR": _decode_gr,
}


def _mdl_from_payload(values: Sequence[Sequence[int]], scheme: str, payload: bytes) -> Dict[str, int]:
    payload_bits = len(payload) * 8
    if scheme == "ID":
        header_bits = _varint_bits(_ensure_consistent_width(values)) + _varint_bits(len(values))
        L_model = header_bits
    elif scheme == "R":
        baseline = compute_r_mode_lengths(values)
        L_model = baseline["L_model"] + _varint_bits(_ensure_consistent_width(values))
    else:  # GR
        baseline = compute_gr_mode_lengths(values)
        L_model = baseline["L_model"] + _varint_bits(_ensure_consistent_width(values))
    L_residual = max(0, payload_bits - L_model)
    return {"L_model": L_model, "L_residual": L_residual, "L_total": L_model + L_residual}


@dataclass(frozen=True)
class SimAEncodedStreamV1:
    """Encoded payload and manifest lengths for a single stream."""

    stream_id: str
    scheme: str
    payload: bytes
    checksum_hex: str
    lengths: Dict[str, int]


def encode_stream(values: Sequence[Sequence[int]], *, prefer_scheme: str | None = None) -> SimAEncodedStreamV1:
    """Encode a stream using MDL scoring across ID/R/GR.

    `prefer_scheme` biases tie-breaking toward the hinted scheme when totals
    match across candidates.
    """

    if prefer_scheme is not None and prefer_scheme not in _ENCODERS:
        raise ValueError("prefer_scheme must be one of 'ID', 'R', 'GR' or None")

    candidates: List[Tuple[str, bytes, Dict[str, int]]] = []
    for scheme, encoder in _ENCODERS.items():
        payload = encoder(values)
        lengths = _mdl_from_payload(values, scheme, payload)
        candidates.append((scheme, payload, lengths))

    def sort_key(item: Tuple[str, bytes, Dict[str, int]]):
        scheme, payload, lengths = item
        bias = 0 if prefer_scheme is None or scheme != prefer_scheme else -1
        return (lengths["L_total"], lengths["L_model"], bias, scheme)

    scheme, payload, lengths = sorted(candidates, key=sort_key)[0]
    checksum_hex = sha256(payload).hexdigest()
    return SimAEncodedStreamV1(
        stream_id="",
        scheme=scheme,
        payload=payload,
        checksum_hex=checksum_hex,
        lengths=lengths,
    )


def decode_stream(stream: APXStreamV1, payload: bytes) -> List[Sequence[int]]:
    """Decode a SimA payload using the manifest's scheme."""

    decoder = _DECODERS.get(stream.scheme)
    if decoder is None:
        raise ValueError(f"Unsupported scheme '{stream.scheme}'")
    return decoder(payload)


def build_manifest_stream(
    stream_id: str,
    description: str,
    encoded: SimAEncodedStreamV1,
    params: object = 0,
) -> APXStreamV1:
    lengths = encoded.lengths
    return APXStreamV1(
        stream_id=stream_id,
        description=description,
        scheme=encoded.scheme,
        params=params,
        L_model=lengths["L_model"],
        L_residual=lengths["L_residual"],
        L_total=lengths["L_total"],
    )


def encode_window_streams(
    streams: Iterable[PressStreamBufferV1], *, prefer_scheme_hints: bool = True
) -> Dict[str, SimAEncodedStreamV1]:
    encoded: Dict[str, SimAEncodedStreamV1] = {}
    for stream in streams:
        prefer = stream.scheme_hint if prefer_scheme_hints else None
        encoded_stream = encode_stream(stream.values, prefer_scheme=prefer)
        encoded[stream.name] = encoded_stream
    return encoded
