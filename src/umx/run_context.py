"""Reusable run context for CMP-0 UMX simulations.

The :class:`UMXRunContext` keeps per-run state (topology, profile, current
state vector, tick counter, and metadata) so that multiple runs can coexist in
one process without relying on globals or GF-01-specific wiring.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from .engine import step as umx_step
from .diagnostics import UMXDiagnosticsConfig, UMXDiagnosticsRecord
from .profile_cmp0 import ProfileCMP0V1
from .tick_ledger import UMXTickLedgerV1
from .topology_profile import TopologyProfileV1


@dataclass
class UMXRunContext:
    """Manage one deterministic UMX run.

    The context holds the static configuration (topology and CMP-0 profile),
    mutable simulation state, and simple run metadata. It exposes convenience
    methods to initialise the state, advance one tick, or run to a target tick
    while returning the emitted ledgers.
    """

    topo: TopologyProfileV1
    profile: ProfileCMP0V1
    gid: str = ""
    run_id: str = ""
    tick: int = 0
    state: Optional[List[int]] = field(default=None, repr=False)
    diag_config: Optional[UMXDiagnosticsConfig] = None
    diagnostics: List[UMXDiagnosticsRecord] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if not self.gid:
            self.gid = self.topo.gid
        if not self.run_id:
            self.run_id = self.topo.gid
        if self.diag_config is None:
            self.diag_config = UMXDiagnosticsConfig(enabled=False)

    def init_state(self, u0: List[int]) -> None:
        """Set the initial state vector and reset the tick counter.

        Raises ``ValueError`` if the state length does not match the topology
        size. A defensive copy is stored to avoid external mutation.
        """

        if len(u0) != self.topo.N:
            raise ValueError("Initial state length must match topology N")
        self.state = list(u0)
        self.tick = 0

    def apply_external_inputs(self, deltas: Sequence[int]) -> List[int]:
        """Apply a vector of external inputs to the current state.

        The inputs are added element-wise to the current state before the next
        tick is executed. This is intended for PFNA-style external sequences
        that perturb the UMX state deterministically.
        """

        if self.state is None:
            raise ValueError("State is not initialised; call init_state(u0) first")
        if len(deltas) != self.topo.N:
            raise ValueError("External input length must match topology N")
        updated = [int(u) + int(delta) for u, delta in zip(self.state, deltas)]
        self.state = updated
        return list(updated)

    def step(self) -> UMXTickLedgerV1:
        """Advance the run by one tick using the CMP-0 rule."""

        if self.state is None:
            raise ValueError("Call init_state(u0) before stepping the run")

        next_tick = self.tick + 1
        ledger = umx_step(next_tick, self.state, self.topo, self.profile)
        if self.diag_config and self.diag_config.enabled:
            diagnostics = self.diag_config.evaluate_tick(
                tick=ledger.tick,
                pre_u=ledger.pre_u,
                post_u=ledger.post_u,
                sum_pre_u=ledger.sum_pre_u,
                sum_post_u=ledger.sum_post_u,
                z_check=ledger.z_check,
            )
            self.diagnostics.append(diagnostics)
        self.state = ledger.post_u
        self.tick = ledger.tick
        return ledger

    def run_until(self, t_max: int) -> List[UMXTickLedgerV1]:
        """Run ticks until ``tick == t_max`` and return emitted ledgers."""

        if t_max < self.tick:
            raise ValueError("t_max must be greater than or equal to current tick")
        ledgers: List[UMXTickLedgerV1] = []
        while self.tick < t_max:
            ledgers.append(self.step())
        return ledgers

    def current_state(self) -> List[int]:
        """Return a copy of the current state vector."""

        if self.state is None:
            raise ValueError("State is not initialised; call init_state(u0) first")
        return list(self.state)
