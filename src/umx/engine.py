"""CMP-0 UMX engine implementation.

Implements the integer-only CMP-0 flux rule and exposes a `step` helper
that emits `UMXTickLedger_v1` records.
"""
from __future__ import annotations

from typing import List

from .profile_cmp0 import ProfileCMP0V1
from .tick_ledger import EdgeFluxV1, UMXTickLedgerV1
from .topology_profile import EdgeProfileV1, TopologyProfileV1


def _sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _compute_flux(edge: EdgeProfileV1, pre_u: List[int]) -> EdgeFluxV1:
    i_idx = edge.i - 1
    j_idx = edge.j - 1
    du = pre_u[i_idx] - pre_u[j_idx]
    magnitude = abs(du)
    raw = (edge.k * magnitude) // edge.SC
    f_e = _sign(du) * min(raw, edge.cap, magnitude)
    return EdgeFluxV1(
        e_id=edge.e_id,
        i=edge.i,
        j=edge.j,
        du=du,
        raw=raw,
        cap=edge.cap,
        f_e=f_e,
    )


def step(tick: int, state: List[int], topo: TopologyProfileV1, profile: ProfileCMP0V1) -> UMXTickLedgerV1:
    """Run one CMP-0 tick and return a UMX tick ledger."""

    if len(state) != topo.N:
        raise ValueError("State length must equal topology N")
    pre_u = list(state)
    net = [0 for _ in pre_u]
    fluxes: List[EdgeFluxV1] = []

    for edge in topo.edges:
        flux = _compute_flux(edge, pre_u)
        fluxes.append(flux)
        i_idx = edge.i - 1
        j_idx = edge.j - 1
        net[i_idx] -= flux.f_e
        net[j_idx] += flux.f_e

    post_u = [pre + delta for pre, delta in zip(pre_u, net)]
    sum_pre_u = sum(pre_u)
    sum_post_u = sum(post_u)
    z_check = sum_pre_u

    return UMXTickLedgerV1(
        tick=tick,
        sum_pre_u=sum_pre_u,
        sum_post_u=sum_post_u,
        z_check=z_check,
        pre_u=pre_u,
        edges=fluxes,
        post_u=post_u,
    )
