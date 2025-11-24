"""Tick loop orchestration for the GF-01 CMP-0 baseline run."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from gate import NAPEnvelopeV1, SceneFrameV1, build_scene_and_envelope
from loom.loom import LoomIBlockV1, LoomPBlockV1, step as loom_step
from press import APXManifestV1, PressWindowContextV1
from umx.engine import step as umx_step
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.tick_ledger import UMXTickLedgerV1
from umx.topology_profile import TopologyProfileV1, gf01_topology_profile


@dataclass(frozen=True)
class GF01RunResult:
    """Aggregate outputs from a full GF-01 tick loop run."""

    profile: ProfileCMP0V1
    topo: TopologyProfileV1
    ledgers: List[UMXTickLedgerV1]
    p_blocks: List[LoomPBlockV1]
    i_blocks: List[LoomIBlockV1]
    manifests: Dict[str, APXManifestV1]
    scenes: List[SceneFrameV1]
    envelopes: List[NAPEnvelopeV1]


def _init_press_contexts(profile: ProfileCMP0V1) -> Dict[str, PressWindowContextV1]:
    full_window_id = "GF01_W1_ticks_1_8"
    short_window_id = "GF01_W1_ticks_1_2"
    contexts = {
        "full": PressWindowContextV1(
            gid="GF01",
            run_id="GF01",
            window_id=full_window_id,
            start_tick=1,
            end_tick=8,
            profile=profile,
        ),
        "short": PressWindowContextV1(
            gid="GF01",
            run_id="GF01",
            window_id=short_window_id,
            start_tick=1,
            end_tick=2,
            profile=profile,
        ),
    }

    for ctx in contexts.values():
        ctx.register_stream("S1_post_u_deltas", description="post_u delta per node")
        ctx.register_stream("S2_fluxes", description="edge flux per edge")

    return contexts


def _append_press_values(
    contexts: Dict[str, PressWindowContextV1],
    deltas: tuple[int, ...],
    fluxes: tuple[int, ...],
    tick: int,
) -> None:
    contexts["full"].append("S1_post_u_deltas", deltas)
    contexts["full"].append("S2_fluxes", fluxes)
    if tick <= 2:
        contexts["short"].append("S1_post_u_deltas", deltas)
        contexts["short"].append("S2_fluxes", fluxes)


def run_gf01(run_id: str = "GF01", nid: str = "N/A") -> GF01RunResult:
    """Execute the full GF-01 CMP-0 tick loop for ticks 1–8.

    Returns all pillar artefacts needed for the GF-01 exam.
    """

    profile = gf01_profile_cmp0()
    topo = gf01_topology_profile()
    contexts = _init_press_contexts(profile)

    state = [3, 1, 0, 0, 0, 0]
    C_prev = profile.C0

    ledgers: List[UMXTickLedgerV1] = []
    p_blocks: List[LoomPBlockV1] = []
    i_blocks: List[LoomIBlockV1] = []
    tick_cache: List[tuple[UMXTickLedgerV1, LoomPBlockV1, int]] = []

    for tick in range(1, 9):
        ledger = umx_step(tick, state, topo, profile)
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        _append_press_values(contexts, deltas, fluxes, tick)

        prev_chain = C_prev
        p_block, C_prev, maybe_i_block = loom_step(ledger, C_prev, tick, topo, profile)

        ledgers.append(ledger)
        p_blocks.append(p_block)
        tick_cache.append((ledger, p_block, prev_chain))
        if maybe_i_block:
            i_blocks.append(maybe_i_block)

        state = ledger.post_u

    manifest_full = contexts["full"].close_window("GF01_APX_v0_full_window")
    manifest_short = contexts["short"].close_window("GF01_APX_v0_ticks_1_2")

    scenes: List[SceneFrameV1] = []
    envelopes: List[NAPEnvelopeV1] = []
    for ledger, p_block, prev_chain in tick_cache:
        scene, envelope = build_scene_and_envelope(
            gid=topo.gid,
            run_id=run_id,
            nid=nid,
            window_id=contexts["full"].window_id,
            ledger=ledger,
            p_block=p_block,
            C_prev=prev_chain,
            manifest_check=manifest_full.manifest_check,
            profile=profile,
        )
        scenes.append(scene)
        envelopes.append(envelope)

    manifests = {
        manifest_full.apx_name: manifest_full,
        manifest_short.apx_name: manifest_short,
    }

    return GF01RunResult(
        profile=profile,
        topo=topo,
        ledgers=ledgers,
        p_blocks=p_blocks,
        i_blocks=i_blocks,
        manifests=manifests,
        scenes=scenes,
        envelopes=envelopes,
    )

