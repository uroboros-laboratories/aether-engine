"""CMP-0 Loom chain and block structures."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from umx.profile_cmp0 import ProfileCMP0V1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1
from umx.topology_profile import TopologyProfileV1


@dataclass(frozen=True)
class FluxSummaryV1:
    """Per-edge flux summary for a P-block."""

    e_id: int
    f_e: int


@dataclass(frozen=True)
class LoomPBlockV1:
    """Per-tick Loom block carrying the chain value."""

    gid: str
    tick: int
    seq: int
    s_t: int
    C_t: int
    topology_version: str = ""
    edge_flux_summary: List[FluxSummaryV1] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.gid:
            raise ValueError("gid must be provided for LoomPBlockV1")
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if self.seq < 1:
            raise ValueError("seq must be >= 1")
        if not isinstance(self.topology_version, str):
            raise ValueError("topology_version must be a string")


@dataclass(frozen=True)
class TopologyEdgeSnapshotV1:
    """Immutable snapshot of a topology edge for an I-block."""

    e_id: int
    i: int
    j: int
    k: int
    cap: int
    SC: int
    c: int


@dataclass(frozen=True)
class LoomIBlockV1:
    """Checkpoint block emitted every W ticks."""

    gid: str
    tick: int
    W: int
    C_t: int
    profile_version: str
    topology_version: str
    post_u: List[int]
    topology_snapshot: List[TopologyEdgeSnapshotV1]

    def __post_init__(self) -> None:
        if not self.gid:
            raise ValueError("gid must be provided for LoomIBlockV1")
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if self.W < 1:
            raise ValueError("W must be >= 1")
        if not self.post_u:
            raise ValueError("post_u must be populated")
        if not self.topology_snapshot:
            raise ValueError("topology_snapshot must be populated")
        if not isinstance(self.topology_version, str):
            raise ValueError("topology_version must be a string")


def compute_s_t(ledger: UMXTickLedgerV1, profile: ProfileCMP0V1) -> int:
    """Compute CMP-0 s_t using the profile's configured rule.

    Supported rule modes:
    - ``constant`` (default): use ``value`` (falls back to ``gf01_constant`` or 9).
    - ``sum_abs_flux``: derive ``s_t`` from the absolute flux magnitudes with optional
      ``offset`` and ``scale`` multipliers, and an optional ``max_value`` clamp.
    """

    rule = profile.s_t_rule or {}
    mode = rule.get("mode", "constant")

    if mode == "constant":
        value = rule.get("value", rule.get("gf01_constant", 9))
        if not isinstance(value, int):
            raise ValueError("constant s_t value must be an integer")
        return value

    if mode == "sum_abs_flux":
        offset = rule.get("offset", 0)
        scale = rule.get("scale", 1)
        max_value = rule.get("max_value")

        if not isinstance(offset, int) or not isinstance(scale, int):
            raise ValueError("sum_abs_flux offset and scale must be integers")

        total_abs_flux = sum(abs(edge.f_e) for edge in ledger.edges)
        value = offset + scale * total_abs_flux

        if max_value is not None:
            if not isinstance(max_value, int):
                raise ValueError("max_value must be an integer when provided")
            value = min(value, max_value)

        return value

    raise ValueError(f"Unsupported s_t rule mode: {mode}")


def compute_chain_value(C_prev: int, s_t: int, seq: int, profile: ProfileCMP0V1) -> int:
    """Apply the CMP-0 chain update rule."""

    return (17 * C_prev + 23 * s_t + seq) % profile.modulus_M


def _summarize_fluxes(edges: List[EdgeFluxV1]) -> List[FluxSummaryV1]:
    return [FluxSummaryV1(e_id=edge.e_id, f_e=edge.f_e) for edge in edges]


def _snapshot_topology(topo: TopologyProfileV1) -> List[TopologyEdgeSnapshotV1]:
    return [
        TopologyEdgeSnapshotV1(
            e_id=edge.e_id,
            i=edge.i,
            j=edge.j,
            k=edge.k,
            cap=edge.cap,
            SC=edge.SC,
            c=edge.c,
        )
        for edge in topo.edges
    ]


def step(
    ledger: UMXTickLedgerV1,
    C_prev: int,
    seq: int,
    topo: TopologyProfileV1,
    profile: ProfileCMP0V1,
    W: Optional[int] = None,
    s_t: Optional[int] = None,
    gid: Optional[str] = None,
    topology_version: Optional[str] = None,
) -> Tuple[LoomPBlockV1, int, Optional[LoomIBlockV1]]:
    """Process one tick through the Loom chain.

    Returns the P-block, the updated chain value C_t, and optionally
    an I-block when the tick hits the configured window spacing.
    """

    W = profile.I_block_spacing_W if W is None else W
    s_t = compute_s_t(ledger, profile) if s_t is None else s_t
    C_t = compute_chain_value(C_prev, s_t, seq, profile)
    p_block = LoomPBlockV1(
        gid=gid or topo.gid,
        tick=ledger.tick,
        seq=seq,
        s_t=s_t,
        C_t=C_t,
        topology_version=topology_version or str(topo.meta.get("version", "v1")),
        edge_flux_summary=_summarize_fluxes(ledger.edges),
    )

    i_block: Optional[LoomIBlockV1] = None
    if ledger.tick % W == 0:
        i_block = LoomIBlockV1(
            gid=gid or topo.gid,
            tick=ledger.tick,
            W=W,
            C_t=C_t,
            profile_version=profile.name,
            topology_version=topology_version or str(topo.meta.get("version", "v1")),
            post_u=list(ledger.post_u),
            topology_snapshot=_snapshot_topology(topo),
        )

    return p_block, C_t, i_block
