"""APX capsule writer/reader with SimB residual support."""
from __future__ import annotations

import json
from dataclasses import asdict
from hashlib import sha256
from typing import Dict, Iterable, Mapping, MutableMapping, Tuple

from press.press import (
    APXManifestV1,
    APXPackageV1,
    APXPayloadV1,
    APXResidualPayloadV1,
    APXStreamV1,
    compute_manifest_check,
)
from press.simb import SimBResidualTableV1
from umx.profile_cmp0 import ProfileCMP0V1

_MAGIC = b"APX1"


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("varint values must be non-negative")
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


def _serialize_manifest(manifest: APXManifestV1) -> bytes:
    manifest_dict = asdict(manifest)
    return json.dumps(manifest_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _deserialize_manifest(data: bytes) -> APXManifestV1:
    raw = json.loads(data.decode("utf-8"))
    streams = [APXStreamV1(**entry) for entry in raw.get("streams", [])]
    return APXManifestV1(
        apx_name=raw["apx_name"],
        profile=raw["profile"],
        manifest_check=raw["manifest_check"],
        gid=raw.get("gid", ""),
        window_id=raw.get("window_id", ""),
        streams=streams,
        apxi_view_ref=raw.get("apxi_view_ref"),
    )


def _verify_manifest(manifest: APXManifestV1, profile: ProfileCMP0V1) -> None:
    if manifest.profile != profile.name:
        raise ValueError("Manifest profile mismatch during APX decode")
    expected = compute_manifest_check(manifest.apx_name, profile, manifest.streams)
    if expected != manifest.manifest_check:
        raise ValueError("Manifest check failed during APX decode")


def _verify_payloads(payloads: Iterable[APXPayloadV1]) -> None:
    for payload in payloads:
        if sha256(payload.payload).hexdigest() != payload.checksum_hex:
            raise ValueError(f"Checksum mismatch for payload '{payload.stream_id}'")


def _profile_for_manifest(manifest: APXManifestV1, *, profile: ProfileCMP0V1 | None) -> ProfileCMP0V1:
    if profile is None:
        profile = ProfileCMP0V1()
    if manifest.profile != profile.name:
        raise ValueError("Manifest profile mismatch during APX encode")
    return profile


def build_apx_capsule(
    package: APXPackageV1,
    *,
    residual_tables: Mapping[str, SimBResidualTableV1] | None = None,
    profile: ProfileCMP0V1 | None = None,
) -> bytes:
    """Staple manifest, SimA payloads, and SimB residuals into one capsule."""

    resolved_profile = _profile_for_manifest(package.manifest, profile=profile)
    _verify_manifest(package.manifest, resolved_profile)
    _verify_payloads(package.payloads.values())

    residuals: Mapping[str, SimBResidualTableV1] = residual_tables or {}
    for table in residuals.values():
        if sha256(table.payload).hexdigest() != table.checksum_hex:
            raise ValueError(f"Checksum mismatch for residual '{table.stream_id}' during encode")

    manifest_bytes = _serialize_manifest(package.manifest)
    buf = bytearray()
    buf.extend(_MAGIC)
    buf.extend(_encode_varint(len(manifest_bytes)))
    buf.extend(manifest_bytes)

    buf.extend(_encode_varint(len(package.payloads)))
    for stream_id in sorted(package.payloads.keys()):
        payload = package.payloads[stream_id]
        checksum_bytes = bytes.fromhex(payload.checksum_hex)
        buf.extend(_encode_varint(len(stream_id)))
        buf.extend(stream_id.encode("utf-8"))
        buf.extend(_encode_varint(len(payload.payload)))
        buf.extend(payload.payload)
        buf.extend(_encode_varint(len(checksum_bytes)))
        buf.extend(checksum_bytes)

    buf.extend(_encode_varint(len(residuals)))
    for stream_id in sorted(residuals.keys()):
        table = residuals[stream_id]
        checksum_bytes = bytes.fromhex(table.checksum_hex)
        buf.extend(_encode_varint(len(stream_id)))
        buf.extend(stream_id.encode("utf-8"))
        buf.extend(_encode_varint(len(table.payload)))
        buf.extend(table.payload)
        buf.extend(_encode_varint(len(checksum_bytes)))
        buf.extend(checksum_bytes)
        codec_bytes = table.codec.encode("utf-8")
        buf.extend(_encode_varint(len(codec_bytes)))
        buf.extend(codec_bytes)

    return bytes(buf)


def load_apx_capsule(
    capsule: bytes, profile: ProfileCMP0V1
) -> Tuple[APXPackageV1, Dict[str, SimBResidualTableV1]]:
    """Parse and validate an APX capsule, returning manifest + payloads + residuals."""

    idx = 0
    if capsule[: len(_MAGIC)] != _MAGIC:
        raise ValueError("Invalid APX capsule header")
    idx += len(_MAGIC)

    manifest_len, idx = _decode_varint(capsule, idx)
    manifest_bytes = capsule[idx : idx + manifest_len]
    idx += manifest_len
    manifest = _deserialize_manifest(manifest_bytes)
    _verify_manifest(manifest, profile)

    payload_count, idx = _decode_varint(capsule, idx)
    payloads: MutableMapping[str, APXPayloadV1] = {}
    for _ in range(payload_count):
        name_len, idx = _decode_varint(capsule, idx)
        name_bytes = capsule[idx : idx + name_len]
        idx += name_len
        payload_len, idx = _decode_varint(capsule, idx)
        payload_bytes = capsule[idx : idx + payload_len]
        idx += payload_len
        checksum_len, idx = _decode_varint(capsule, idx)
        checksum_bytes = capsule[idx : idx + checksum_len]
        idx += checksum_len
        stream_name = name_bytes.decode("utf-8")
        payloads[stream_name] = APXPayloadV1(
            stream_id=stream_name,
            scheme=next(stream.scheme for stream in manifest.streams if stream.stream_id == stream_name),
            payload=payload_bytes,
            checksum_hex=checksum_bytes.hex(),
        )

    _verify_payloads(payloads.values())

    residual_count, idx = _decode_varint(capsule, idx)
    residuals: Dict[str, SimBResidualTableV1] = {}
    for _ in range(residual_count):
        name_len, idx = _decode_varint(capsule, idx)
        name_bytes = capsule[idx : idx + name_len]
        idx += name_len
        payload_len, idx = _decode_varint(capsule, idx)
        payload_bytes = capsule[idx : idx + payload_len]
        idx += payload_len
        checksum_len, idx = _decode_varint(capsule, idx)
        checksum_bytes = capsule[idx : idx + checksum_len]
        idx += checksum_len
        codec_len, idx = _decode_varint(capsule, idx)
        codec_bytes = capsule[idx : idx + codec_len]
        idx += codec_len
        checksum_hex = checksum_bytes.hex()
        if sha256(payload_bytes).hexdigest() != checksum_hex:
            raise ValueError("Residual checksum mismatch during APX decode")
        table = SimBResidualTableV1(
            stream_id=name_bytes.decode("utf-8"),
            payload=payload_bytes,
            checksum_hex=checksum_hex,
            codec=codec_bytes.decode("utf-8"),
            lengths={"L_residual": len(payload_bytes) * 8},
        )
        residuals[table.stream_id] = table

    package = APXPackageV1(manifest=manifest, payloads=dict(payloads), residuals=residuals)
    return package, residuals
