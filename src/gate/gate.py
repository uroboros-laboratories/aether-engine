"""Minimal Gate/TBP types and helpers for CMP-0 GF-01."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from loom.loom import LoomPBlockV1
from umx.profile_cmp0 import ProfileCMP0V1
from umx.tick_ledger import UMXTickLedgerV1


@dataclass(frozen=True)
class SceneFrameV1:
    """Minimal tick summary consumed by Gate/TBP."""

    gid: str
    run_id: str
    tick: int
    nid: str
    pre_u: List[int]
    post_u: List[int]
    ledger_ref: str
    C_prev: int
    C_t: int
    window_id: str
    manifest_check: Optional[int] = None
    nap_envelope_ref: Optional[str] = None
    meta: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if not self.pre_u or not self.post_u:
            raise ValueError("pre_u and post_u must be populated")
        if len(self.pre_u) != len(self.post_u):
            raise ValueError("pre_u and post_u lengths must match")
        if not self.ledger_ref:
            raise ValueError("ledger_ref must be a non-empty reference")
        if not self.window_id:
            raise ValueError("window_id must be provided")


@dataclass(frozen=True)
class NAPEnvelopeV1:
    """Canonical NAP envelope wrapper for per-tick payload references."""

    v: int
    tick: int
    gid: str
    nid: str
    layer: str
    mode: str
    payload_ref: int
    seq: int
    prev_chain: int
    sig: str

    def __post_init__(self) -> None:
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if self.seq < 1:
            raise ValueError("seq must be >= 1")
        if not self.gid:
            raise ValueError("gid must be provided")
        if not self.nid:
            raise ValueError("nid must be provided")
        if self.payload_ref < 0:
            raise ValueError("payload_ref must be non-negative")
        if self.prev_chain < 0:
            raise ValueError("prev_chain must be non-negative")


def build_scene_frame(
    gid: str,
    run_id: str,
    nid: str,
    ledger: UMXTickLedgerV1,
    C_prev: int,
    C_t: int,
    window_id: str,
    manifest_check: Optional[int],
    ledger_ref: Optional[str] = None,
    nap_envelope_ref: Optional[str] = None,
    meta: Optional[Dict[str, object]] = None,
) -> SceneFrameV1:
    """Construct a SceneFrame_v1 from UMX/Loom artefacts."""

    return SceneFrameV1(
        gid=gid,
        run_id=run_id,
        tick=ledger.tick,
        nid=nid,
        pre_u=list(ledger.pre_u),
        post_u=list(ledger.post_u),
        ledger_ref=ledger_ref or f"umx_ledger_{ledger.tick}",
        C_prev=C_prev,
        C_t=C_t,
        window_id=window_id,
        manifest_check=manifest_check,
        nap_envelope_ref=nap_envelope_ref,
        meta=meta or {},
    )


def emit_nap_envelope(
    scene: SceneFrameV1,
    profile: ProfileCMP0V1,
    seq: Optional[int] = None,
    payload_ref: Optional[int] = None,
    sig: str = "",
) -> NAPEnvelopeV1:
    """Emit a NAPEnvelope_v1 from a SceneFrame_v1 and profile defaults."""

    nap_defaults = profile.nap_defaults
    if payload_ref is None:
        if scene.manifest_check is None:
            raise ValueError("payload_ref or scene.manifest_check must be provided")
        payload_ref = scene.manifest_check

    return NAPEnvelopeV1(
        v=int(nap_defaults.get("v", 1)),
        tick=scene.tick,
        gid=scene.gid,
        nid=scene.nid,
        layer=str(nap_defaults.get("layer", "DATA")),
        mode=str(nap_defaults.get("mode", "P")),
        payload_ref=int(payload_ref),
        seq=seq or scene.tick,
        prev_chain=scene.C_prev,
        sig=sig,
    )


def build_scene_and_envelope(
    gid: str,
    run_id: str,
    nid: str,
    window_id: str,
    ledger: UMXTickLedgerV1,
    p_block: LoomPBlockV1,
    C_prev: int,
    manifest_check: int,
    profile: ProfileCMP0V1,
) -> Tuple[SceneFrameV1, NAPEnvelopeV1]:
    """Convenience wrapper that returns both SceneFrame and NAP envelope."""

    scene = build_scene_frame(
        gid=gid,
        run_id=run_id,
        nid=nid,
        ledger=ledger,
        C_prev=C_prev,
        C_t=p_block.C_t,
        window_id=window_id,
        manifest_check=manifest_check,
    )
    envelope = emit_nap_envelope(scene, profile, seq=p_block.seq, payload_ref=manifest_check)
    return scene, envelope
