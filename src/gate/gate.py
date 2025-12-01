"""Minimal Gate/TBP types and helpers for CMP-0 GF-01."""
from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, field
from functools import cached_property
from typing import (
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from collections import defaultdict

from governance import GovernanceConfigV1
from loom.loom import LoomPBlockV1
from umx.profile_cmp0 import ProfileCMP0V1
from umx.tick_ledger import UMXTickLedgerV1

from ops import (
    LoggingConfigV1,
    MetricsConfigV1,
    MetricsSnapshotV1,
    StructuredLogEntryV1,
    StructuredLogger,
)

if TYPE_CHECKING:  # pragma: no cover - used for type hints only
    from core.tick_loop import GF01RunResult, TickLoopWindowSpec
    from umx.topology_profile import TopologyProfileV1


# Allowed NAP layer/mode values for CMP-0 NAP envelopes.
ALLOWED_NAP_LAYERS = ("INGRESS", "DATA", "CTRL", "EGRESS", "GOV")
ALLOWED_NAP_MODES = ("P", "I", "S", "G")


@dataclass(frozen=True)
class PressStreamSpecV1:
    """Configuration for a Press stream declared by Gate."""

    name: str
    source: str
    scheme_hint: Optional[str] = None
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Press stream name must be provided")
        if self.scheme_hint is not None and self.scheme_hint not in {"R", "GR", "ID"}:
            raise ValueError("scheme_hint must be one of 'R', 'GR', or 'ID'")
        allowed_sources = {
            "post_u_deltas",
            "fluxes",
            "pre_u",
            "post_u",
            "prev_chain",
        }
        if self.source not in allowed_sources:
            raise ValueError(f"source must be one of {sorted(allowed_sources)}")


def _default_press_stream_specs() -> Tuple[PressStreamSpecV1, ...]:
    """Default CMP-0 Press streams (GF-01 compatible)."""

    return (
        PressStreamSpecV1(
            name="S1_post_u_deltas",
            source="post_u_deltas",
            description="post_u delta per node",
        ),
        PressStreamSpecV1(
            name="S2_fluxes",
            source="fluxes",
            description="edge flux per edge",
        ),
    )


def _default_governance_config() -> GovernanceConfigV1:
    """Default governance config keeps Codex suggestions off."""

    return GovernanceConfigV1()


@dataclass(frozen=True)
class SessionConfigV1:
    """Top-level Gate/TBP session configuration for TickLoop_v1 runs."""

    topo: "TopologyProfileV1"
    profile: ProfileCMP0V1
    initial_state: Sequence[int]
    total_ticks: int
    window_specs: Sequence["TickLoopWindowSpec"]
    primary_window_id: str
    run_id: str = "SESSION"
    nid: str = "N/A"
    pfna_inputs: Tuple[PFNAInputV0, ...] = field(default_factory=tuple)
    governance: GovernanceConfigV1 = field(default_factory=_default_governance_config)
    press_default_streams: Tuple[PressStreamSpecV1, ...] = field(
        default_factory=_default_press_stream_specs
    )
    logging_config: LoggingConfigV1 = field(default_factory=LoggingConfigV1)
    metrics_config: MetricsConfigV1 = field(default_factory=MetricsConfigV1)

    def __post_init__(self) -> None:
        if self.total_ticks < 1:
            raise ValueError("total_ticks must be >= 1")
        if len(self.initial_state) != self.topo.N:
            raise ValueError("initial_state length must match topology N")
        if not self.window_specs:
            raise ValueError("At least one window spec must be provided")
        window_ids = {spec.window_id for spec in self.window_specs}
        if self.primary_window_id not in window_ids:
            raise ValueError("primary_window_id must reference a window spec")
        if not self.run_id:
            raise ValueError("run_id must be provided")
        if not isinstance(self.pfna_inputs, tuple):
            object.__setattr__(self, "pfna_inputs", tuple(self.pfna_inputs))
        if not isinstance(self.press_default_streams, tuple):
            object.__setattr__(self, "press_default_streams", tuple(self.press_default_streams))
        if not isinstance(self.governance, GovernanceConfigV1):
            raise ValueError("governance must be a GovernanceConfigV1 instance")
        if not isinstance(self.logging_config, LoggingConfigV1):
            raise ValueError("logging_config must be a LoggingConfigV1 instance")
        if not isinstance(self.metrics_config, MetricsConfigV1):
            raise ValueError("metrics_config must be a MetricsConfigV1 instance")


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
        if self.tick < 0:
            raise ValueError("tick must be >= 0")
        if not self.nid:
            raise ValueError("nid must be provided")
        if not self.values:
            raise ValueError("values must be a non-empty sequence")
        if not all(isinstance(v, int) for v in self.values):
            raise ValueError("values must be integers")


@dataclass(frozen=True)
class PFNATransformV1:
    """Integerization parameters for PFNA ingress with audit trail."""

    scale: float = 1.0
    origin: float = 0.0
    clamp_min: Optional[int] = None
    clamp_max: Optional[int] = None
    description: str = ""

    def __post_init__(self) -> None:
        if self.clamp_min is not None and self.clamp_max is not None:
            if self.clamp_min > self.clamp_max:
                raise ValueError("clamp_min cannot exceed clamp_max")

    def integerize(self, values: Sequence[Union[int, float]]) -> Tuple[Tuple[int, ...], Tuple[Dict[str, object], ...]]:
        """Apply scale/origin/clamp deterministically and emit per-value audits."""

        audited: List[Dict[str, object]] = []
        out: List[int] = []
        for idx, raw in enumerate(values):
            shifted = float(raw) + self.origin
            scaled = shifted * self.scale
            rounded = int(round(scaled))
            clamped = rounded
            if self.clamp_min is not None:
                clamped = max(clamped, int(self.clamp_min))
            if self.clamp_max is not None:
                clamped = min(clamped, int(self.clamp_max))
            out.append(clamped)
            audited.append(
                {
                    "index": idx,
                    "raw": str(raw),
                    "shifted": f"{shifted:.6f}",
                    "scaled": f"{scaled:.6f}",
                    "rounded": rounded,
                    "clamped": clamped,
                }
            )
        return tuple(out), tuple(audited)


@dataclass(frozen=True)
class PFNAIngressEventV1:
    """Integerized PFNA payload with deterministic audit trail."""

    pfna: PFNAInputV0
    integerized: Tuple[int, ...]
    audit: Tuple[Mapping[str, object], ...]

    @cached_property
    def as_pfna_input(self) -> PFNAInputV0:
        """Return a PFNAInputV0 copy with integerized values."""

        return PFNAInputV0(
            pfna_id=self.pfna.pfna_id,
            gid=self.pfna.gid,
            run_id=self.pfna.run_id,
            tick=self.pfna.tick,
            nid=self.pfna.nid,
            values=self.integerized,
            description=self.pfna.description,
        )


class PFNAIngressQueue:
    """Idempotent PFNA ingress buffer that integerizes on enqueue."""

    def __init__(self, *, transform: Optional[PFNATransformV1] = None) -> None:
        self.transform = transform or PFNATransformV1()
        self._seen: set[Tuple[int, str]] = set()
        self._events: List[PFNAIngressEventV1] = []

    def enqueue(self, pfna: PFNAInputV0) -> None:
        key = (pfna.tick, pfna.pfna_id)
        if key in self._seen:
            return

        integerized, audit = self.transform.integerize(pfna.values)
        event = PFNAIngressEventV1(pfna=pfna, integerized=integerized, audit=audit)
        self._events.append(event)
        self._seen.add(key)
        self._events.sort(key=lambda item: (item.pfna.tick, item.pfna.pfna_id))

    def extend(self, pfna_inputs: Iterable[PFNAInputV0]) -> None:
        for pfna in pfna_inputs:
            self.enqueue(pfna)

    def pop_ready(self, tick: int) -> Tuple[PFNAIngressEventV1, ...]:
        ready: List[PFNAIngressEventV1] = []
        remaining: List[PFNAIngressEventV1] = []
        for event in self._events:
            if event.pfna.tick == tick:
                ready.append(event)
            else:
                remaining.append(event)
        self._events = remaining
        return tuple(ready)


def _load_pfna_source(source: Union[str, Path, Mapping[str, object]]) -> Mapping[str, object]:
    """Load a PFNA document from a path, JSON string, or mapping."""

    if isinstance(source, Mapping):
        return source

    if isinstance(source, (str, Path)):
        path = Path(source)
        if path.exists():
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        try:
            return json.loads(str(source))
        except json.JSONDecodeError as exc:  # pragma: no cover - error path
            raise ValueError("PFNA source must be a valid path or JSON string") from exc

    raise TypeError("PFNA source must be a mapping, JSON string, or path")


def load_pfna_v0(
    source: Union[str, Path, Mapping[str, object]], *, expected_length: Optional[int] = None
) -> Tuple[PFNAInputV0, ...]:
    """Load and validate PFNA V0 inputs deterministically.

    The loader enforces the PFNA V0 schema (see docs/contracts/PFNA_V0_Schema_v1.md):
    - top-level fields: v=0, pfna_id, gid, run_id, nid, entries
    - each entry: pfna_id, tick>=0, values (non-empty int sequence), optional description
    - optional `expected_length` enforces the vector length of each entry.
    """

    data = _load_pfna_source(source)

    try:
        version = int(data["v"])
    except Exception as exc:  # pragma: no cover - schema error path
        raise ValueError("PFNA V0 document must provide integer field 'v'") from exc

    if version != 0:
        raise ValueError("PFNA V0 requires v == 0")

    for field_name in ("pfna_id", "gid", "run_id", "nid", "entries"):
        if field_name not in data:
            raise ValueError(f"PFNA V0 document missing required field '{field_name}'")

    bundle_id = str(data["pfna_id"])
    gid = str(data["gid"])
    run_id = str(data["run_id"])
    nid = str(data["nid"])
    entries_raw = data["entries"]

    if not bundle_id:
        raise ValueError("PFNA bundle pfna_id must be non-empty")
    if not gid:
        raise ValueError("PFNA bundle gid must be non-empty")
    if not run_id:
        raise ValueError("PFNA bundle run_id must be non-empty")
    if not nid:
        raise ValueError("PFNA bundle nid must be non-empty")
    if not isinstance(entries_raw, list) or not entries_raw:
        raise ValueError("PFNA entries must be a non-empty list")

    parsed: List[PFNAInputV0] = []
    for entry in entries_raw:
        if not isinstance(entry, Mapping):
            raise ValueError("PFNA entry must be a mapping")
        for field_name in ("pfna_id", "tick", "values"):
            if field_name not in entry:
                raise ValueError(f"PFNA entry missing required field '{field_name}'")

        pfna_id = str(entry["pfna_id"])
        description = str(entry.get("description", ""))
        tick_raw = entry["tick"]
        values_raw = entry["values"]

        tick = int(tick_raw)
        if tick < 0:
            raise ValueError("PFNA entry tick must be >= 0")

        if not isinstance(values_raw, (list, tuple)) or not values_raw:
            raise ValueError("PFNA entry values must be a non-empty list of integers")
        try:
            values = tuple(int(val) for val in values_raw)
        except Exception as exc:  # pragma: no cover - schema error path
            raise ValueError("PFNA entry values must be integers") from exc

        if expected_length is not None and len(values) != expected_length:
            raise ValueError("PFNA entry values length must match expected_length")

        parsed.append(
            PFNAInputV0(
                pfna_id=pfna_id,
                gid=gid,
                run_id=run_id,
                tick=tick,
                nid=nid,
                values=values,
                description=description,
            )
        )

    parsed.sort(key=lambda item: (item.tick, item.pfna_id))
    return tuple(parsed)


def dump_pfna_v0(
    *,
    bundle_id: str,
    gid: str,
    run_id: str,
    nid: str,
    entries: Iterable[PFNAInputV0],
) -> Dict[str, object]:
    """Serialise PFNA inputs back to the PFNA V0 document shape."""

    ordered_entries = [
        {
            "pfna_id": pfna.pfna_id,
            "tick": pfna.tick,
            "values": list(pfna.values),
            **({"description": pfna.description} if pfna.description else {}),
        }
        for pfna in sorted(entries, key=lambda item: (item.tick, item.pfna_id))
    ]

    return {
        "v": 0,
        "pfna_id": bundle_id,
        "gid": gid,
        "run_id": run_id,
        "nid": nid,
        "entries": ordered_entries,
    }


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
    slp_event_ids: tuple[str, ...] = field(default_factory=tuple)
    meta: Mapping[str, object] = field(default_factory=dict)

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
        for event_id in self.slp_event_ids:
            if not isinstance(event_id, str) or not event_id:
                raise ValueError("slp_event_ids must be non-empty strings when provided")
        if not isinstance(self.meta, Mapping):
            raise ValueError("meta must be a mapping")
        object.__setattr__(self, "meta", dict(self.meta))


@dataclass(frozen=True)
class GovernanceDecisionV1:
    """Decision outcome for an envelope under Gate/TBP governance."""

    envelope_ref: str
    tick: int
    seq: int
    status: str
    reasons: Tuple[str, ...] = field(default_factory=tuple)
    policy_set_hash: Optional[str] = None
    window_id: Optional[str] = None

    def to_meta(self) -> Dict[str, object]:
        return {
            "event": "GATE_GOVERNANCE_DECISION",
            "envelope_ref": self.envelope_ref,
            "tick": self.tick,
            "seq": self.seq,
            "status": self.status,
            "reasons": list(self.reasons),
            "policy_set_hash": self.policy_set_hash,
            "window_id": self.window_id,
        }


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
        merged_meta.setdefault(
            "pfna_integerization",
            [{"pfna_id": ref, "values": tuple(), "audit": ()} for ref in pfna_refs],
        )

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


def validate_scene_frame(
    scene: SceneFrameV1,
    *,
    manifest_ref: str,
    manifest_check: int,
    expected_tick: Optional[int] = None,
) -> None:
    """Validate key invariants for a SceneFrame_v1 instance."""

    if expected_tick is not None and scene.tick != expected_tick:
        raise ValueError("scene tick does not match expected_tick")
    if scene.manifest_check != manifest_check:
        raise ValueError("scene manifest_check does not match manifest")
    meta_ref = scene.meta.get("manifest_ref") if isinstance(scene.meta, Mapping) else None
    if meta_ref != manifest_ref:
        raise ValueError("scene manifest_ref meta must reference the manifest")
    if scene.pfna_refs and not isinstance(scene.meta.get("pfna_refs"), list):
        raise ValueError("scene.meta must expose pfna_refs when pfna_refs are set")


def emit_nap_envelope(
    scene: SceneFrameV1,
    profile: ProfileCMP0V1,
    seq: Optional[int] = None,
    payload_ref: Optional[int] = None,
    layer: Optional[str] = None,
    mode: Optional[str] = None,
    sig: str = "",
    slp_event_ids: Optional[Sequence[str]] = None,
    meta: Optional[Mapping[str, object]] = None,
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
        slp_event_ids=tuple(slp_event_ids or ()),
        meta=dict(meta or {}),
    )


def apply_governance_to_envelopes(
    envelopes: Sequence[NAPEnvelopeV1],
    *,
    governance: Optional[GovernanceConfigV1],
    window_id: str,
    profile: ProfileCMP0V1,
    logger: Optional[StructuredLogger] = None,
) -> Tuple[Tuple[NAPEnvelopeV1, ...], Tuple[NAPEnvelopeV1, ...], Tuple[GovernanceDecisionV1, ...]]:
    """Apply Gate governance rules to outbound envelopes and emit GOV events.

    The rules are intentionally minimal/deterministic for CMP-0:
    - If governance is OFF/None, envelopes are returned unchanged and no GOV
      envelopes are emitted.
    - Allowed layers are drawn from governance.meta["allowed_layers"] when
      provided; otherwise all CMP-0 layers are accepted.
    - Optional governance.meta["max_envelopes_per_tick"] caps data envelopes
      per tick. In ENFORCE mode, envelopes that exceed the cap are dropped;
      in OBSERVE/DRY_RUN they are retained but logged as rejected.
    - GOV decision envelopes are emitted with `layer="GOV"` / `mode="G"`
      carrying structured decision metadata.
    """

    if governance is None or (
        governance.codex_action_mode == "OFF" and governance.governance_mode == "OFF"
    ):
        return tuple(envelopes), tuple(), tuple()

    allowed_layers = governance.meta.get("allowed_layers", ALLOWED_NAP_LAYERS)
    max_per_tick = governance.meta.get("max_envelopes_per_tick")
    enforce = governance.governance_mode == "ENFORCE"

    per_tick_counts: dict[int, int] = defaultdict(int)
    filtered: list[NAPEnvelopeV1] = []
    governance_envelopes: list[NAPEnvelopeV1] = []
    decisions: list[GovernanceDecisionV1] = []
    seq_offset = (max((env.seq for env in envelopes), default=0)) + 1

    for envelope in envelopes:
        per_tick_counts[envelope.tick] += 1
        reasons: list[str] = []
        if envelope.layer not in allowed_layers:
            reasons.append(f"layer {envelope.layer} not allowed")
        if max_per_tick is not None and per_tick_counts[envelope.tick] > int(max_per_tick):
            reasons.append(
                f"tick {envelope.tick} exceeds cap {int(max_per_tick)}"
            )

        status = "ACCEPTED" if not reasons else "REJECTED"
        decision = GovernanceDecisionV1(
            envelope_ref=f"nap_{envelope.tick}_{envelope.seq}",
            tick=envelope.tick,
            seq=envelope.seq,
            status=status if enforce else f"{status}_OBSERVED",
            reasons=tuple(reasons),
            policy_set_hash=governance.policy_set_hash,
            window_id=window_id,
        )
        decisions.append(decision)

        if reasons and enforce:
            # Drop envelope in ENFORCE mode.
            pass
        else:
            filtered.append(envelope)

        governance_envelopes.append(
            NAPEnvelopeV1(
                v=int(profile.nap_defaults.get("v", 1)),
                tick=envelope.tick,
                gid=envelope.gid,
                nid=envelope.nid,
                layer="GOV",
                mode="G",
                payload_ref=envelope.payload_ref,
                seq=seq_offset,
                prev_chain=envelope.prev_chain,
                sig="",
                meta=decision.to_meta(),
            )
        )
        seq_offset += 1

    if logger and logger.enabled:
        for decision in decisions:
            logger.log(
                "gate_governance_decision",
                gid=governance.gid or "",
                run_id=governance.run_id or "N/A",
                payload=decision.to_meta(),
            )

    return tuple(filtered), tuple(governance_envelopes), tuple(decisions)


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
    slp_event_ids: Optional[Sequence[str]] = None,
    meta: Optional[Mapping[str, object]] = None,
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
        slp_event_ids=slp_event_ids,
        meta=meta,
    )
    return scene, envelope


def _pfna_payload_ref(pfna_inputs: Iterable[PFNAInputV0], *, modulus: int = 1_000_000_007) -> int:
    """Deterministically derive an ingress payload_ref from PFNA inputs."""

    acc = 0
    for pfna in sorted(pfna_inputs, key=lambda p: p.pfna_id):
        for ch in pfna.pfna_id:
            acc = (acc * 31 + ord(ch)) % modulus
        for val in pfna.values:
            acc = (acc * 17 + int(val)) % modulus
    return acc


def _build_ctrl_envelope(
    *,
    gid: str,
    nid: str,
    profile: ProfileCMP0V1,
    tick: int,
    seq: int,
    payload_ref: int,
    prev_chain: int,
) -> NAPEnvelopeV1:
    return NAPEnvelopeV1(
        v=int(profile.nap_defaults.get("v", 1)),
        tick=int(tick),
        gid=gid,
        nid=nid,
        layer="CTRL",
        mode="P",
        payload_ref=int(payload_ref),
        seq=int(seq),
        prev_chain=int(prev_chain),
        sig="",
    )


@dataclass(frozen=True)
class SessionRunResult:
    """Outputs from a Gate/TBP session around TickLoop_v1."""

    config: SessionConfigV1
    lifecycle_envelopes: List[NAPEnvelopeV1]
    tick_result: "GF01RunResult"
    logs: List[StructuredLogEntryV1] = field(default_factory=list)
    metrics: Optional[MetricsSnapshotV1] = None

    @property
    def all_envelopes(self) -> List[NAPEnvelopeV1]:
        lifecycle = list(self.lifecycle_envelopes)
        ingress_by_tick: Dict[int, List[NAPEnvelopeV1]] = {}
        for env in self.tick_result.ingress_envelopes:
            ingress_by_tick.setdefault(env.tick, []).append(env)
        governance_by_tick: Dict[int, List[NAPEnvelopeV1]] = {}
        for env in getattr(self.tick_result, "governance_envelopes", ()):  # pragma: no cover - guarded below
            governance_by_tick.setdefault(env.tick, []).append(env)

        ordered: List[NAPEnvelopeV1] = []
        if lifecycle:
            ordered.append(lifecycle[0])

        data_envelopes = list(self.tick_result.envelopes)
        for idx in range(self.config.total_ticks):
            tick = idx + 1
            ordered.extend(sorted(governance_by_tick.get(tick, ()), key=lambda env: env.seq))
            ordered.extend(ingress_by_tick.get(tick, []))
            if idx < len(data_envelopes):
                ordered.append(data_envelopes[idx])

        if len(lifecycle) > 1:
            ordered.append(lifecycle[1])

        trailing_governance = [
            env
            for tick, envs in governance_by_tick.items()
            if tick > self.config.total_ticks
            for env in envs
        ]
        ordered.extend(sorted(trailing_governance, key=lambda env: env.seq))
        ordered.extend(self.tick_result.egress_envelopes)

        return ordered


def run_session(config: SessionConfigV1) -> SessionRunResult:
    """Run a CMP-0 session via Gate/TBP and TickLoop_v1."""

    from core.tick_loop import run_cmp0_tick_loop

    logger = StructuredLogger(config.logging_config)
    logger.log(
        "run_start",
        gid=config.topo.gid,
        run_id=config.run_id,
        payload={
            "total_ticks": config.total_ticks,
            "windows": sorted(spec.window_id for spec in config.window_specs),
            "primary_window_id": config.primary_window_id,
        },
    )

    codex_ctx = None
    if config.governance.codex_action_mode != "OFF":
        from codex.context import CodexContext

        codex_ctx = CodexContext(
            library_id=f"{config.run_id}_LIB", profile=config.profile.name
        )

    tick_result = run_cmp0_tick_loop(
        topo=config.topo,
        profile=config.profile,
        initial_state=config.initial_state,
        total_ticks=config.total_ticks,
        window_specs=config.window_specs,
        primary_window_id=config.primary_window_id,
        run_id=config.run_id,
        nid=config.nid,
        pfna_inputs=config.pfna_inputs,
        press_default_streams=config.press_default_streams,
        logger=logger,
        governance=config.governance,
        codex_ctx=codex_ctx,
    )

    lifecycle: List[NAPEnvelopeV1] = []
    lifecycle.append(
        _build_ctrl_envelope(
            gid=config.topo.gid,
            nid=config.nid,
            profile=config.profile,
            tick=1,
            seq=1,
            payload_ref=0,
            prev_chain=config.profile.C0,
        )
    )

    final_chain = tick_result.p_blocks[-1].C_t if tick_result.p_blocks else config.profile.C0
    payload_ref = tick_result.envelopes[-1].payload_ref if tick_result.envelopes else 0
    lifecycle.append(
        _build_ctrl_envelope(
            gid=config.topo.gid,
            nid=config.nid,
            profile=config.profile,
            tick=config.total_ticks,
            seq=config.total_ticks + 1,
            payload_ref=payload_ref,
            prev_chain=final_chain,
        )
    )

    logger.log(
        "run_end",
        gid=config.topo.gid,
        run_id=config.run_id,
        payload={
            "envelopes": len(tick_result.envelopes),
            "ingress": len(tick_result.ingress_envelopes),
            "egress": len(tick_result.egress_envelopes),
        },
    )

    metrics: Optional[MetricsSnapshotV1] = None
    if config.metrics_config.enabled:
        metrics = _build_metrics_snapshot(
            config=config,
            tick_result=tick_result,
            lifecycle_envelopes=lifecycle,
        )

    return SessionRunResult(
        config=config,
        lifecycle_envelopes=lifecycle,
        tick_result=tick_result,
        logs=logger.entries,
        metrics=metrics,
    )


def _build_metrics_snapshot(
    *,
    config: SessionConfigV1,
    tick_result: "GF01RunResult",
    lifecycle_envelopes: Sequence[NAPEnvelopeV1],
) -> MetricsSnapshotV1:
    """Derive a deterministic metrics snapshot for a completed run."""

    from uledger.canonical import hash_record

    uledger_entries = list(tick_result.u_ledger_entries)
    last_hash: Optional[str]
    if uledger_entries:
        last_hash = hash_record(uledger_entries[-1])
    else:
        last_hash = None

    nap_ingress = len(tick_result.ingress_envelopes)
    nap_data = len(tick_result.envelopes)
    nap_egress = len(tick_result.egress_envelopes)
    nap_governance = len(getattr(tick_result, "governance_envelopes", ()))
    nap_total = nap_ingress + nap_data + nap_egress + nap_governance + len(lifecycle_envelopes)

    return MetricsSnapshotV1(
        gid=config.topo.gid,
        run_id=config.run_id,
        total_ticks=config.total_ticks,
        window_count=len(config.window_specs),
        nap_total=nap_total,
        nap_ingress=nap_ingress,
        nap_data=nap_data,
        nap_egress=nap_egress,
        uledger_entries=len(uledger_entries),
        uledger_last_hash=last_hash,
        apx_manifests=len(tick_result.manifests),
        apxi_views=len(tick_result.apxi_views),
    )

