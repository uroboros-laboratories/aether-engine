"""Minimal Gate/TBP types and helpers for CMP-0 GF-01."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from loom.loom import LoomPBlockV1
from umx.profile_cmp0 import ProfileCMP0V1
from umx.tick_ledger import UMXTickLedgerV1


# Allowed NAP layer/mode values for CMP-0 NAP envelopes.
ALLOWED_NAP_LAYERS = ("INGRESS", "DATA", "CTRL", "EGRESS")
ALLOWED_NAP_MODES = ("P", "S")


@dataclass(frozen=True)
class PFNAInputV0:
    """Deterministic placeholder for an external PFNA-like input sequence."""

    pfna_id: str
    gid: str
    run_id: str
    tick: int
    nid: str
    values: Tuple[int, ...]
    description: str = ""

    def __post_init__(self) -> None:
        if not self.pfna_id:
            raise ValueError("pfna_id must be provided")
        if not self.gid:
            raise ValueError("gid must be provided")
        if not self.run_id:
            raise ValueError("run_id must be provided")
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if not self.nid:
            raise ValueError("nid must be provided")
        if not self.values:
            raise ValueError("values must be a non-empty sequence")
        if not all(isinstance(v, int) for v in self.values):
            raise ValueError("values must be integers")


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
    pfna_refs: Tuple[str, ...] = field(default_factory=tuple)
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
        if any(not ref for ref in self.pfna_refs):
            raise ValueError("pfna_refs must be non-empty strings when provided")


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
        if self.layer not in ALLOWED_NAP_LAYERS:
            raise ValueError(f"layer must be one of {ALLOWED_NAP_LAYERS}")
        if self.mode not in ALLOWED_NAP_MODES:
            raise ValueError(f"mode must be one of {ALLOWED_NAP_MODES}")
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
    pfna_refs: Optional[Iterable[str]] = None,
    p_block_ref: Optional[str] = None,
    manifest_ref: Optional[str] = None,
    ledger_ref: Optional[str] = None,
    nap_envelope_ref: Optional[str] = None,
    meta: Optional[Dict[str, object]] = None,
) -> SceneFrameV1:
    """Construct a SceneFrame_v1 from UMX/Loom artefacts."""

    merged_meta = dict(meta or {})
    if p_block_ref is not None:
        merged_meta.setdefault("p_block_ref", p_block_ref)
    if manifest_ref is not None:
        merged_meta.setdefault("manifest_ref", manifest_ref)
    if pfna_refs:
        merged_meta.setdefault("pfna_refs", list(pfna_refs))

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
        pfna_refs=tuple(pfna_refs or ()),
        meta=merged_meta,
    )


def emit_nap_envelope(
    scene: SceneFrameV1,
    profile: ProfileCMP0V1,
    seq: Optional[int] = None,
    payload_ref: Optional[int] = None,
    layer: Optional[str] = None,
    mode: Optional[str] = None,
    sig: str = "",
) -> NAPEnvelopeV1:
    """Emit a NAPEnvelope_v1 from a SceneFrame_v1 and profile defaults."""

    nap_defaults = profile.nap_defaults
    if payload_ref is None:
        if scene.manifest_check is None:
            raise ValueError("payload_ref or scene.manifest_check must be provided")
        payload_ref = scene.manifest_check

    effective_layer = str(layer if layer is not None else nap_defaults.get("layer", "DATA"))
    effective_mode = str(mode if mode is not None else nap_defaults.get("mode", "P"))

    return NAPEnvelopeV1(
        v=int(nap_defaults.get("v", 1)),
        tick=scene.tick,
        gid=scene.gid,
        nid=scene.nid,
        layer=effective_layer,
        mode=effective_mode,
        payload_ref=int(payload_ref),
        seq=seq or scene.tick,
        prev_chain=scene.C_prev,
        sig=sig,
    )


def build_pfna_placeholder(
    *,
    pfna_id: str,
    gid: str,
    run_id: str,
    tick: int,
    nid: str,
    values: Sequence[int],
    description: str = "",
) -> PFNAInputV0:
    """Convenience helper to wrap a raw integer sequence as a PFNA input."""

    return PFNAInputV0(
        pfna_id=pfna_id,
        gid=gid,
        run_id=run_id,
        tick=int(tick),
        nid=nid,
        values=tuple(int(v) for v in values),
        description=description,
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
    p_block_ref: Optional[str] = None,
    manifest_ref: Optional[str] = None,
    pfna_refs: Optional[Iterable[str]] = None,
    nap_layer: Optional[str] = None,
    nap_mode: Optional[str] = None,
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
        pfna_refs=pfna_refs,
        p_block_ref=p_block_ref,
        manifest_ref=manifest_ref,
    )
    envelope = emit_nap_envelope(
        scene,
        profile,
        seq=p_block.seq,
        payload_ref=manifest_check,
        layer=nap_layer,
        mode=nap_mode,
    )
    return scene, envelope

