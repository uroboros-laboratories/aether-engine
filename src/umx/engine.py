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


def _compute_flux(
    edge: EdgeProfileV1,
    pre_u: List[int],
    scale: int,
    *,
    epsilon_cap: int | None,
    causal_radius: int | None,
    max_edge_cap: int | None,
) -> tuple[EdgeFluxV1, bool, bool]:
    i_idx = edge.i - 1
    j_idx = edge.j - 1
    du = pre_u[i_idx] - pre_u[j_idx]
    magnitude = abs(du)
    causal_applied = False
    if causal_radius and magnitude > causal_radius:
        magnitude = causal_radius
        causal_applied = True
    raw = (edge.k * magnitude) // scale
    epsilon_applied = False
    if epsilon_cap is not None and raw > epsilon_cap:
        raw = epsilon_cap
        epsilon_applied = True
    effective_cap = edge.cap if max_edge_cap is None else min(edge.cap, max_edge_cap)
    f_e = _sign(du) * min(raw, effective_cap, magnitude)
    flux = EdgeFluxV1(
        e_id=edge.e_id,
        i=edge.i,
        j=edge.j,
        du=du,
        raw=raw,
        cap=effective_cap,
        f_e=f_e,
    )
    return flux, causal_applied, epsilon_applied


def step(tick: int, state: List[int], topo: TopologyProfileV1, profile: ProfileCMP0V1) -> UMXTickLedgerV1:
    """Run one CMP-0 tick and return a UMX tick ledger."""

    if len(state) != topo.N:
        raise ValueError("State length must equal topology N")
    pre_u = list(state)
    net = [0 for _ in pre_u]
    fluxes: List[EdgeFluxV1] = []

    causal_applied = False
    epsilon_applied = False

    sorted_edges = sorted(topo.edges, key=lambda e: e.e_id)
    for edge in sorted_edges:
        edge_radius = edge.causal_radius or edge.c or topo.causal_radius or None
        flux, applied_causal, applied_epsilon = _compute_flux(
            edge,
            pre_u,
            topo.SC,
            epsilon_cap=profile.epsilon_cap,
            causal_radius=edge_radius,
            max_edge_cap=topo.max_edge_cap,
        )
        causal_applied = causal_applied or applied_causal
        epsilon_applied = epsilon_applied or applied_epsilon
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
        nap_ref=topo.nap_ref or "",
        causal_radius_applied=causal_applied,
        epsilon_applied=epsilon_applied,
        policy_notes=[note for note in [
            "causal_radius_clamped" if causal_applied else None,
            "epsilon_cap_applied" if epsilon_applied else None,
        ] if note],
    )
