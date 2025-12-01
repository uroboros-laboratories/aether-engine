"""LoomRunContext to manage the CMP-0 time axis alongside UMX."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

from umx.profile_cmp0 import ProfileCMP0V1
from umx.run_context import UMXRunContext
from umx.tick_ledger import UMXTickLedgerV1
from umx.topology_profile import TopologyProfileV1

from .loom import LoomIBlockV1, LoomPBlockV1, compute_s_t, step as loom_step
from .chain import LoomChainRecorder, LoomChainState


SeqRule = Callable[[UMXTickLedgerV1], int]
STRule = Callable[[UMXTickLedgerV1, ProfileCMP0V1], int]


def _default_seq_rule(ledger: UMXTickLedgerV1) -> int:
    """Use the ledger tick as the sequence value by default."""

    return ledger.tick


@dataclass
class LoomRunContext:
    """Manage Loom chain/block generation for one run.

    The context can either drive its own :class:`UMXRunContext` or ingest
    external ledgers. It tracks the evolving chain value ``C_t`` and stores the
    emitted P-/I-blocks for replay or inspection.
    """

    profile: ProfileCMP0V1
    topo: Optional[TopologyProfileV1] = None
    umx_ctx: Optional[UMXRunContext] = None
    W: Optional[int] = None
    seq_rule: SeqRule = _default_seq_rule
    s_t_rule: STRule = compute_s_t
    C_t: int = field(init=False)
    p_blocks: List[LoomPBlockV1] = field(default_factory=list, init=False)
    i_blocks: List[LoomIBlockV1] = field(default_factory=list, init=False)
    ledgers: List[UMXTickLedgerV1] = field(default_factory=list, init=False)
    recorder: LoomChainRecorder = field(default_factory=LoomChainRecorder)

    def __post_init__(self) -> None:
        if self.umx_ctx:
            if self.topo and self.topo is not self.umx_ctx.topo:
                raise ValueError("topo must match the UMXRunContext topology")
            self.topo = self.umx_ctx.topo
            if self.umx_ctx.profile != self.profile:
                raise ValueError("profile must match the UMXRunContext profile")
        if self.topo is None:
            raise ValueError("A topology must be provided")

        self.W = self.profile.I_block_spacing_W if self.W is None else self.W
        if self.W <= 0:
            raise ValueError("I-block spacing W must be a positive integer")

        self.C_t = self.profile.C0

    def ingest_tick(self, ledger: UMXTickLedgerV1) -> Tuple[LoomPBlockV1, Optional[LoomIBlockV1]]:
        """Consume a tick ledger and emit the corresponding Loom blocks."""

        seq = self.seq_rule(ledger)
        s_t = self.s_t_rule(ledger, self.profile)
        prev_chain = self.C_t
        p_block, C_t, maybe_i_block = loom_step(
            ledger=ledger,
            C_prev=prev_chain,
            seq=seq,
            topo=self.topo,
            profile=self.profile,
            W=self.W,
            s_t=s_t,
            gid=self.topo.gid,
            topology_version=str(self.topo.meta.get("version", "v1")),
        )

        self.C_t = C_t
        self.p_blocks.append(p_block)
        self.recorder.record_p_block(p_block)
        self.ledgers.append(ledger)
        if maybe_i_block:
            self.i_blocks.append(maybe_i_block)
            window_hashes = self.recorder.p_hashes[-maybe_i_block.W :]
            self.recorder.record_i_block(maybe_i_block, window_hashes)
        return p_block, maybe_i_block

    def step(self) -> Tuple[UMXTickLedgerV1, LoomPBlockV1, Optional[LoomIBlockV1]]:
        """Advance the bound UMX context and ingest its ledger."""

        if not self.umx_ctx:
            raise ValueError("No UMXRunContext bound; use ingest_tick for external ledgers")
        ledger = self.umx_ctx.step()
        p_block, maybe_i_block = self.ingest_tick(ledger)
        return ledger, p_block, maybe_i_block

    def run_until(self, t_max: int) -> Tuple[List[UMXTickLedgerV1], List[LoomPBlockV1], List[LoomIBlockV1]]:
        """Step through ticks until reaching ``t_max`` using the bound UMX context."""

        if not self.umx_ctx:
            raise ValueError("No UMXRunContext bound; cannot auto-step without it")
        if t_max < self.umx_ctx.tick:
            raise ValueError("t_max must be greater than or equal to the current tick")

        while self.umx_ctx.tick < t_max:
            self.step()

        return list(self.ledgers), list(self.p_blocks), list(self.i_blocks)

    def current_chain_value(self) -> int:
        """Return the latest chain value (``C_t``)."""

        return self.C_t

    def get_pblock(self, tick: int) -> LoomPBlockV1:
        """Return the P-block for a given tick."""

        for p_block in self.p_blocks:
            if p_block.tick == tick:
                return p_block
        raise ValueError(f"No P-block recorded for tick {tick}")

    def get_chain_at(self, tick: int) -> int:
        """Return the chain value ``C_t`` for a given tick."""

        return self.get_pblock(tick).C_t

    def get_iblock_for(self, tick: int) -> LoomIBlockV1:
        """Return the nearest prior I-block for the requested tick."""

        eligible = [i_block for i_block in self.i_blocks if i_block.tick <= tick]
        if not eligible:
            raise ValueError(f"No I-blocks available at or before tick {tick}")
        return eligible[-1]

    def replay_state_at(self, tick: int) -> List[int]:
        """Reconstruct the UMX state at ``tick`` using the nearest prior I-block."""

        if not self.p_blocks:
            raise ValueError("No P-blocks recorded; cannot replay")
        if tick > self.p_blocks[-1].tick:
            raise ValueError("Requested tick exceeds recorded range")

        checkpoint = self.get_iblock_for(tick)
        replay_ctx = UMXRunContext(topo=self.topo, profile=self.profile)
        replay_ctx.init_state(list(checkpoint.post_u))
        replay_ctx.tick = checkpoint.tick
        replay_ctx.run_until(tick)
        return replay_ctx.current_state()

    def chain_state(self) -> LoomChainState:
        """Export chain tip information for NAP envelopes or diagnostics."""

        return self.recorder.chain_state()
