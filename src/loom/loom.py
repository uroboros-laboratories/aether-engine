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

    tick: int
    seq: int
    s_t: int
    C_t: int
    edge_flux_summary: List[FluxSummaryV1] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if self.seq < 1:
            raise ValueError("seq must be >= 1")


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

    tick: int
    W: int
    C_t: int
    profile_version: str
    post_u: List[int]
    topology_snapshot: List[TopologyEdgeSnapshotV1]

    def __post_init__(self) -> None:
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if self.W < 1:
            raise ValueError("W must be >= 1")
        if not self.post_u:
            raise ValueError("post_u must be populated")
        if not self.topology_snapshot:
            raise ValueError("topology_snapshot must be populated")


def compute_s_t(ledger: UMXTickLedgerV1, profile: ProfileCMP0V1) -> int:
    """Compute CMP-0 s_t; GF-01 uses the fixed constant."""

    _ = ledger  # placeholder for future derived calculations
    return profile.s_t_rule.get("gf01_constant", 9)


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
) -> Tuple[LoomPBlockV1, int, Optional[LoomIBlockV1]]:
    """Process one tick through the Loom chain.

    Returns the P-block, the updated chain value C_t, and optionally
    an I-block when the tick hits the configured window spacing.
    """

    s_t = compute_s_t(ledger, profile)
    C_t = compute_chain_value(C_prev, s_t, seq, profile)
    p_block = LoomPBlockV1(
        tick=ledger.tick,
        seq=seq,
        s_t=s_t,
        C_t=C_t,
        edge_flux_summary=_summarize_fluxes(ledger.edges),
    )

    i_block: Optional[LoomIBlockV1] = None
    if ledger.tick % profile.I_block_spacing_W == 0:
        i_block = LoomIBlockV1(
            tick=ledger.tick,
            W=profile.I_block_spacing_W,
            C_t=C_t,
            profile_version=profile.name,
            post_u=list(ledger.post_u),
            topology_snapshot=_snapshot_topology(topo),
        )

    return p_block, C_t, i_block
