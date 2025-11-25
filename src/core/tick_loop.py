"""Tick loop orchestration for CMP-0 runs backed by SceneFrame_v1."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

from gate import (
    NAPEnvelopeV1,
    PFNAInputV0,
    SceneFrameV1,
    build_scene_and_envelope,
)
from loom.loom import LoomIBlockV1, LoomPBlockV1
from loom.run_context import LoomRunContext
from press import APXManifestV1, PressWindowContextV1
from uledger import ULedgerEntryV1, build_uledger_entries
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.run_context import UMXRunContext
from umx.tick_ledger import UMXTickLedgerV1
from umx.topology_profile import TopologyProfileV1, gf01_topology_profile


@dataclass(frozen=True)
class GF01RunResult:
    """Aggregate outputs from a CMP-0 tick loop run."""

    run_id: str
    profile: ProfileCMP0V1
    topo: TopologyProfileV1
    ledgers: List[UMXTickLedgerV1]
    p_blocks: List[LoomPBlockV1]
    i_blocks: List[LoomIBlockV1]
    manifests: Dict[str, APXManifestV1]
    scenes: List[SceneFrameV1]
    envelopes: List[NAPEnvelopeV1]
    u_ledger_entries: List[ULedgerEntryV1]


@dataclass(frozen=True)
class TickLoopWindowSpec:
    """Definition for a Press/APX window in the tick loop."""

    window_id: str
    apx_name: str
    start_tick: int
    end_tick: int


def _init_window_context(
    spec: TickLoopWindowSpec, profile: ProfileCMP0V1, gid: str, run_id: str
) -> PressWindowContextV1:
    ctx = PressWindowContextV1(
        gid=gid,
        run_id=run_id,
        window_id=spec.window_id,
        start_tick=spec.start_tick,
        end_tick=spec.end_tick,
        profile=profile,
    )
    ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
    ctx.register_stream("S2_fluxes", description="edge flux per edge")
    return ctx


def _append_press_values(
    contexts: Dict[str, PressWindowContextV1],
    specs: Dict[str, TickLoopWindowSpec],
    deltas: tuple[int, ...],
    fluxes: tuple[int, ...],
    tick: int,
) -> None:
    for window_id, ctx in contexts.items():
        spec = specs[window_id]
        if spec.start_tick <= tick <= spec.end_tick:
            ctx.append("S1_post_u_deltas", deltas)
            ctx.append("S2_fluxes", fluxes)


def _group_pfna_inputs(
    pfna_inputs: Iterable[PFNAInputV0], topo: TopologyProfileV1, gid: str, run_id: str
) -> Dict[int, List[PFNAInputV0]]:
    grouped: Dict[int, List[PFNAInputV0]] = {}
    for pfna in pfna_inputs:
        if pfna.gid != gid:
            raise ValueError("PFNA gid must match the topology gid")
        if pfna.run_id != run_id:
            raise ValueError("PFNA run_id must match the run")
        if len(pfna.values) != topo.N:
            raise ValueError("PFNA values length must match topology N")
        grouped.setdefault(pfna.tick, []).append(pfna)
    return grouped


def run_cmp0_tick_loop(
    *,
    topo: TopologyProfileV1,
    profile: ProfileCMP0V1,
    initial_state: Sequence[int],
    total_ticks: int,
    window_specs: Iterable[TickLoopWindowSpec],
    primary_window_id: str,
    run_id: str,
    nid: str,
    pfna_inputs: Optional[Iterable[PFNAInputV0]] = None,
) -> GF01RunResult:
    """Execute a CMP-0 tick loop and assemble SceneFrame-driven artefacts."""

    specs = {spec.window_id: spec for spec in window_specs}
    if primary_window_id not in specs:
        raise ValueError("primary_window_id must match one of the provided window specs")

    contexts = {
        spec.window_id: _init_window_context(spec, profile=profile, gid=topo.gid, run_id=run_id)
        for spec in specs.values()
    }

    ctx = UMXRunContext(topo=topo, profile=profile, gid=topo.gid, run_id=run_id)
    ctx.init_state(initial_state)
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=ctx)

    pfna_by_tick: Dict[int, List[PFNAInputV0]] = {}
    if pfna_inputs:
        pfna_by_tick = _group_pfna_inputs(pfna_inputs, topo=topo, gid=topo.gid, run_id=run_id)

    ledgers: List[UMXTickLedgerV1] = []
    p_blocks: List[LoomPBlockV1] = []
    i_blocks: List[LoomIBlockV1] = []
    tick_cache: List[tuple[UMXTickLedgerV1, LoomPBlockV1, int, List[str]]] = []

    for _ in range(total_ticks):
        next_tick = ctx.tick + 1
        pfna_refs_for_tick: List[str] = []
        if next_tick in pfna_by_tick:
            pfna_deltas = [0 for _ in range(topo.N)]
            for pfna in pfna_by_tick[next_tick]:
                pfna_refs_for_tick.append(pfna.pfna_id)
                pfna_deltas = [acc + int(delta) for acc, delta in zip(pfna_deltas, pfna.values)]
            ctx.apply_external_inputs(pfna_deltas)

        prev_chain = loom_ctx.current_chain_value()
        ledger, p_block, maybe_i_block = loom_ctx.step()
        tick = ledger.tick
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        _append_press_values(contexts, specs, deltas, fluxes, tick)

        ledgers.append(ledger)
        p_blocks.append(p_block)
        tick_cache.append((ledger, p_block, prev_chain, pfna_refs_for_tick))
        if maybe_i_block:
            i_blocks.append(maybe_i_block)

    manifests: Dict[str, APXManifestV1] = {}
    for window_id, ctx in contexts.items():
        spec = specs[window_id]
        manifests[spec.apx_name] = ctx.close_window(spec.apx_name)

    primary_manifest = manifests[specs[primary_window_id].apx_name]

    scenes: List[SceneFrameV1] = []
    envelopes: List[NAPEnvelopeV1] = []
    for ledger, p_block, prev_chain, pfna_refs in tick_cache:
        scene, envelope = build_scene_and_envelope(
            gid=topo.gid,
            run_id=run_id,
            nid=nid,
            window_id=specs[primary_window_id].window_id,
            ledger=ledger,
            p_block=p_block,
            C_prev=prev_chain,
            manifest_check=primary_manifest.manifest_check,
            profile=profile,
            p_block_ref=f"loom_p_block_{ledger.tick}",
            manifest_ref=primary_manifest.apx_name,
            pfna_refs=pfna_refs,
        )
        scenes.append(scene)
        envelopes.append(envelope)

    u_ledger_entries = build_uledger_entries(
        gid=topo.gid,
        run_id=run_id,
        window_id=specs[primary_window_id].window_id,
        ledgers=ledgers,
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=primary_manifest,
    )

    return GF01RunResult(
        run_id=run_id,
        profile=profile,
        topo=topo,
        ledgers=ledgers,
        p_blocks=p_blocks,
        i_blocks=i_blocks,
        manifests=manifests,
        scenes=scenes,
        envelopes=envelopes,
        u_ledger_entries=u_ledger_entries,
    )


def run_gf01(run_id: str = "GF01", nid: str = "N/A") -> GF01RunResult:
    """Execute the full GF-01 CMP-0 tick loop for ticks 1–8."""

    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    window_specs = [
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_8",
            apx_name="GF01_APX_v0_full_window",
            start_tick=1,
            end_tick=8,
        ),
        TickLoopWindowSpec(
            window_id="GF01_W1_ticks_1_2",
            apx_name="GF01_APX_v0_ticks_1_2",
            start_tick=1,
            end_tick=2,
        ),
    ]

    return run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=[3, 1, 0, 0, 0, 0],
        total_ticks=8,
        window_specs=window_specs,
        primary_window_id="GF01_W1_ticks_1_8",
        run_id=run_id,
        nid=nid,
    )

