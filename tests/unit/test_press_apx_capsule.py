from __future__ import annotations

import json
from typing import Tuple

import pytest

from press import (
    PressWindowContextV1,
    build_apx_capsule,
    decode_residual_table,
    encode_residual_table,
    load_apx_capsule,
)
from umx.run_context import UMXRunContext
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


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


def _build_package_with_residuals(window_id: str = "GF01_APX_v0_ticks_1_2"):
    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    run_ctx = UMXRunContext(topo=topo, profile=profile, gid="GF01", run_id="run_0")
    run_ctx.init_state([3, 1, 0, 0, 0, 0])

    press_ctx = PressWindowContextV1(
        gid="GF01",
        run_id="run_0",
        window_id=window_id,
        start_tick=1,
        end_tick=2,
        profile=profile,
    )
    press_ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
    press_ctx.register_stream("S2_fluxes", description="edge flux per edge")

    residual_values = []
    for _ in range(2):
        ledger = run_ctx.step()
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        press_ctx.append("S1_post_u_deltas", deltas)
        press_ctx.append("S2_fluxes", fluxes)
        residual_values.append(fluxes)

    residual_table = encode_residual_table("S2_fluxes_residual", residual_values)
    package = press_ctx.encode_window(window_id, residual_tables={"S2_fluxes_residual": residual_table})
    return profile, package, residual_table, residual_values


def test_simb_residual_round_trip():
    values = [(1,), (-2,), (4,)]
    table = encode_residual_table("residual", values)
    decoded = decode_residual_table(table.payload)

    assert decoded == [v[0] for v in values]
    assert table.lengths["L_total"] == len(table.payload) * 8


def test_apx_capsule_round_trip_with_residuals():
    profile, package, residual_table, residual_values = _build_package_with_residuals()

    capsule = build_apx_capsule(package, residual_tables={residual_table.stream_id: residual_table}, profile=profile)
    loaded_package, residuals = load_apx_capsule(capsule, profile)

    assert loaded_package.manifest.manifest_check == package.manifest.manifest_check
    assert set(loaded_package.payloads.keys()) == set(package.payloads.keys())
    for name, payload in loaded_package.payloads.items():
        assert payload.checksum_hex == package.payloads[name].checksum_hex

    assert residual_table.stream_id in residuals
    decoded_residuals = decode_residual_table(residuals[residual_table.stream_id].payload)
    assert decoded_residuals == residual_values


def test_apx_capsule_manifest_validation_rejects_tamper():
    profile, package, residual_table, _ = _build_package_with_residuals("GF01_APX_v0_ticks_1_3")
    capsule = build_apx_capsule(package, residual_tables={residual_table.stream_id: residual_table}, profile=profile)

    # Locate manifest bytes inside the capsule
    idx = len(b"APX1")
    manifest_len, idx = _decode_varint(capsule, idx)
    manifest_start = idx
    manifest_end = manifest_start + manifest_len
    manifest_bytes = bytearray(capsule[manifest_start:manifest_end])

    manifest_text = manifest_bytes.decode("utf-8")
    manifest_data = json.loads(manifest_text)
    check_str = str(manifest_data["manifest_check"])
    flipped_digit = "0" if check_str[-1] != "0" else "1"
    tampered_check = check_str[:-1] + flipped_digit
    manifest_bytes = bytearray(manifest_text.replace(check_str, tampered_check, 1).encode("utf-8"))
    assert len(manifest_bytes) == manifest_len

    tampered_capsule = bytearray(capsule)
    tampered_capsule[manifest_start:manifest_end] = manifest_bytes

    with pytest.raises(ValueError):
        load_apx_capsule(bytes(tampered_capsule), profile)
