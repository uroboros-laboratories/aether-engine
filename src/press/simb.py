"""SimB residual encoder/decoder for integer tables."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, List, Sequence, Tuple

from press.sima import _decode_varint, _encode_header, _encode_varint, _normalize_values, _zigzag_decode, _zigzag_encode


@dataclass(frozen=True)
class SimBResidualTableV1:
    """Residual payload emitted by SimB for a single stream."""

    stream_id: str
    payload: bytes
    checksum_hex: str
    codec: str
    lengths: Dict[str, int]


def _encode_residual(values: Sequence[Sequence[int]]) -> Tuple[bytes, Dict[str, int]]:
    width, normalized = _normalize_values(values)
    encoded = bytearray()
    encoded.extend(_encode_header(width, len(normalized)))
    for entry in normalized:
        for component in entry:
            encoded.extend(_encode_varint(_zigzag_encode(component)))
    L_model = _encode_varint(width).__len__() * 8 + _encode_varint(len(normalized)).__len__() * 8
    L_residual = max(0, len(encoded) * 8 - L_model)
    return bytes(encoded), {"L_model": L_model, "L_residual": L_residual, "L_total": len(encoded) * 8}


def encode_residual_table(stream_id: str, values: Sequence[Sequence[int]], *, codec: str = "SB-ID") -> SimBResidualTableV1:
    payload, lengths = _encode_residual(values)
    return SimBResidualTableV1(
        stream_id=stream_id,
        payload=payload,
        checksum_hex=sha256(payload).hexdigest(),
        codec=codec,
        lengths=lengths,
    )


def decode_residual_table(payload: bytes) -> List[Sequence[int]]:
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
