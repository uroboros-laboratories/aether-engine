"""UMX tick ledger data structures for CMP-0.

Implements the `EdgeFlux_v1` and `UMXTickLedger_v1` shapes from the
contracts. These are light dataclasses that carry per-tick state and
flux details.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class EdgeFluxV1:
    """Per-edge flux details for one tick."""

    e_id: int
    i: int
    j: int
    du: int
    raw: int
    cap: int
    f_e: int


@dataclass(frozen=True)
class UMXTickLedgerV1:
    """Full per-tick ledger emitted by the UMX engine."""

    tick: int
    sum_pre_u: int
    sum_post_u: int
    z_check: int
    pre_u: List[int]
    edges: List[EdgeFluxV1] = field(default_factory=list)
    post_u: List[int] = field(default_factory=list)
    nap_ref: str = ""
    causal_radius_applied: bool = False
    epsilon_applied: bool = False
    policy_notes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.sum_pre_u != self.sum_post_u or self.z_check != self.sum_pre_u:
            raise ValueError("Conservation failed: sum_pre_u, sum_post_u, z_check must match")
        if not self.pre_u or not self.post_u:
            raise ValueError("pre_u and post_u must be populated")
        if len(self.pre_u) != len(self.post_u):
            raise ValueError("pre_u and post_u must have the same length")
        if not isinstance(self.nap_ref, str):
            raise ValueError("nap_ref must be a string")
