"""Tick loop orchestration for CMP-0 runs backed by SceneFrame_v1."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, TYPE_CHECKING

from gate import (
    NAPEnvelopeV1,
    PFNAInputV0,
    PressStreamSpecV1,
    SceneFrameV1,
    _default_press_stream_specs,
    _pfna_payload_ref,
    build_scene_and_envelope,
)
from governance import BudgetUsage, GovernedActionQueue, GovernanceConfigV1, governed_decision_loop
from ops import StructuredLogger
from loom.loom import LoomIBlockV1, LoomPBlockV1
from loom.run_context import LoomRunContext
from press import APXManifestV1, APXiDescriptorV1, APXiViewV1, PressWindowContextV1
from uledger import ULedgerEntryV1, build_uledger_entries
from umx.profile_cmp0 import ProfileCMP0V1, gf01_profile_cmp0
from umx.run_context import UMXRunContext
from umx.tick_ledger import UMXTickLedgerV1
from umx.topology_profile import TopologyProfileV1, gf01_topology_profile

if TYPE_CHECKING:  # pragma: no cover - import guard for typing only
    from codex.context import CodexContext, CodexLibraryEntryV1, CodexProposalV1


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
    apxi_views: Dict[str, APXiViewV1]
    scenes: List[SceneFrameV1]
    envelopes: List[NAPEnvelopeV1]
    ingress_envelopes: List[NAPEnvelopeV1]
    egress_envelopes: List[NAPEnvelopeV1]
    u_ledger_entries: List[ULedgerEntryV1]
    governance: GovernanceConfigV1 | None = None
    governance_budget_usage: BudgetUsage | None = None
    governance_envelopes: List[NAPEnvelopeV1] = field(default_factory=list)
    codex_motifs: tuple["CodexLibraryEntryV1", ...] = ()
    codex_proposals: tuple["CodexProposalV1", ...] = ()
    codex_actions: tuple["CodexProposalV1", ...] = ()
    codex_hypothetical_actions: tuple["CodexProposalV1", ...] = ()
    codex_hypothetical_actions: tuple["CodexProposalV1", ...] = ()


@dataclass(frozen=True)
class TickLoopWindowSpec:
    """Definition for a Press/APX window in the tick loop."""

    window_id: str
    apx_name: str
    start_tick: int
    end_tick: int
    streams: Sequence[PressStreamSpecV1] = ()
    aeon_window_id: str | None = None
    apxi_descriptors: Mapping[str, Sequence[APXiDescriptorV1]] = field(default_factory=dict)
    apxi_enabled: bool = False
    apxi_residual_scheme: str = "R"

    def __post_init__(self) -> None:
        if self.start_tick < 1:
            raise ValueError("start_tick must be >= 1")
        if self.end_tick < self.start_tick:
            raise ValueError("end_tick must be >= start_tick")
        if not isinstance(self.streams, tuple):
            object.__setattr__(self, "streams", tuple(self.streams))
        if self.apxi_residual_scheme not in {"ID", "R", "GR"}:
            raise ValueError("apxi_residual_scheme must be one of 'ID', 'R', 'GR'")


def _init_window_context(
    spec: TickLoopWindowSpec,
    profile: ProfileCMP0V1,
    gid: str,
    run_id: str,
) -> PressWindowContextV1:
    ctx = PressWindowContextV1(
        gid=gid,
        run_id=run_id,
        window_id=spec.window_id,
        start_tick=spec.start_tick,
        end_tick=spec.end_tick,
        profile=profile,
        aeon_window_id=spec.aeon_window_id,
        apxi_enabled=spec.apxi_enabled,
        apxi_residual_scheme=spec.apxi_residual_scheme,
        apxi_descriptors=spec.apxi_descriptors,
    )
    for stream in spec.streams:
        ctx.register_stream(stream.name, scheme_hint=stream.scheme_hint, description=stream.description)
    return ctx


def _append_press_values(
    contexts: Dict[str, PressWindowContextV1],
    specs: Dict[str, TickLoopWindowSpec],
    *,
    tick: int,
    deltas: tuple[int, ...],
    fluxes: tuple[int, ...],
    ledger: UMXTickLedgerV1,
    p_block: LoomPBlockV1,
    prev_chain: int,
) -> None:
    for window_id, ctx in contexts.items():
        spec = specs[window_id]
        if spec.start_tick <= tick <= spec.end_tick:
            for stream in spec.streams:
                if stream.source == "post_u_deltas":
                    value = deltas
                elif stream.source == "fluxes":
                    value = fluxes
                elif stream.source == "pre_u":
                    value = tuple(ledger.pre_u)
                elif stream.source == "post_u":
                    value = tuple(ledger.post_u)
                elif stream.source == "prev_chain":
                    value = (prev_chain,)
                else:  # pragma: no cover - guarded by validation
                    raise ValueError(f"Unsupported Press stream source '{stream.source}'")
                ctx.append(stream.name, value, tick=tick)


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


def _apply_pfna_initial_state(base_state: Sequence[int], pfna_inputs: Iterable[PFNAInputV0]) -> List[int]:
    """Apply tick-0 PFNA vectors to the initial state deterministically."""

    adjusted = [int(val) for val in base_state]
    for pfna in sorted(pfna_inputs, key=lambda item: item.pfna_id):
        adjusted = [orig + delta for orig, delta in zip(adjusted, pfna.values)]
    return adjusted


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
    press_default_streams: Optional[Iterable[PressStreamSpecV1]] = None,
    logger: Optional[StructuredLogger] = None,
    governance: GovernanceConfigV1 | None = None,
    codex_ctx: "CodexContext" | None = None,
    codex_proposals: Sequence["CodexProposalV1"] | None = None,
) -> GF01RunResult:
    """Execute a CMP-0 tick loop and assemble SceneFrame-driven artefacts."""

    specs = {spec.window_id: spec for spec in window_specs}
    if primary_window_id not in specs:
        raise ValueError("primary_window_id must match one of the provided window specs")

    default_streams = tuple(press_default_streams or _default_press_stream_specs())
    resolved_specs: Dict[str, TickLoopWindowSpec] = {}
    for spec in specs.values():
        if spec.streams:
            resolved_specs[spec.window_id] = spec
        else:
            resolved_specs[spec.window_id] = TickLoopWindowSpec(
                window_id=spec.window_id,
                apx_name=spec.apx_name,
                start_tick=spec.start_tick,
                end_tick=spec.end_tick,
                streams=default_streams,
                aeon_window_id=spec.aeon_window_id,
                apxi_descriptors=spec.apxi_descriptors,
                apxi_enabled=spec.apxi_enabled,
                apxi_residual_scheme=spec.apxi_residual_scheme,
            )

    contexts = {
        spec.window_id: _init_window_context(
            spec, profile=profile, gid=topo.gid, run_id=run_id
        )
        for spec in resolved_specs.values()
    }

    if logger and logger.enabled:
        logger.log(
            "tick_loop_start",
            gid=topo.gid,
            run_id=run_id,
            payload={
                "total_ticks": total_ticks,
                "windows": sorted(resolved_specs.keys()),
                "primary_window_id": primary_window_id,
            },
        )

    pfna_by_tick: Dict[int, List[PFNAInputV0]] = {}
    initial_pfna: List[PFNAInputV0] = []
    effective_initial_state: List[int] = list(initial_state)
    if pfna_inputs:
        pfna_by_tick = _group_pfna_inputs(pfna_inputs, topo=topo, gid=topo.gid, run_id=run_id)
        initial_pfna = pfna_by_tick.pop(0, [])
        if initial_pfna:
            effective_initial_state = _apply_pfna_initial_state(initial_state, initial_pfna)

    ctx = UMXRunContext(topo=topo, profile=profile, gid=topo.gid, run_id=run_id)
    ctx.init_state(effective_initial_state)
    loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=ctx)

    ledgers: List[UMXTickLedgerV1] = []
    p_blocks: List[LoomPBlockV1] = []
    i_blocks: List[LoomIBlockV1] = []
    tick_cache: List[tuple[UMXTickLedgerV1, LoomPBlockV1, int, List[str]]] = []
    ingress_envelopes: List[NAPEnvelopeV1] = []
    egress_envelopes: List[NAPEnvelopeV1] = []

    for _ in range(total_ticks):
        next_tick = ctx.tick + 1
        pfna_refs_for_tick: List[str] = []
        pfna_batch: List[PFNAInputV0] = []
        if next_tick in pfna_by_tick:
            pfna_deltas = [0 for _ in range(topo.N)]
            pfna_batch = pfna_by_tick[next_tick]
            for pfna in pfna_batch:
                pfna_refs_for_tick.append(pfna.pfna_id)
                pfna_deltas = [acc + int(delta) for acc, delta in zip(pfna_deltas, pfna.values)]
            ctx.apply_external_inputs(pfna_deltas)

        prev_chain = loom_ctx.current_chain_value()
        if pfna_batch:
            ingress_envelopes.append(
                NAPEnvelopeV1(
                    v=int(profile.nap_defaults.get("v", 1)),
                    tick=next_tick,
                    gid=topo.gid,
                    nid=nid,
                    layer="INGRESS",
                    mode=str(profile.nap_defaults.get("ingress_mode", "P")),
                    payload_ref=_pfna_payload_ref(pfna_batch, modulus=profile.modulus_M),
                    seq=next_tick,
                    prev_chain=prev_chain,
                    sig="",
                )
            )

        ledger, p_block, maybe_i_block = loom_ctx.step()
        tick = ledger.tick
        deltas = tuple(post - pre for post, pre in zip(ledger.post_u, ledger.pre_u))
        fluxes = tuple(edge.f_e for edge in ledger.edges)
        _append_press_values(
            contexts,
            resolved_specs,
            tick=tick,
            deltas=deltas,
            fluxes=fluxes,
            ledger=ledger,
            p_block=p_block,
            prev_chain=prev_chain,
        )

        ledgers.append(ledger)
        p_blocks.append(p_block)
        tick_cache.append((ledger, p_block, prev_chain, pfna_refs_for_tick))
        if maybe_i_block:
            i_blocks.append(maybe_i_block)

        if logger and logger.enabled and logger.config.include_ticks:
            logger.log(
                "tick_complete",
                gid=topo.gid,
                run_id=run_id,
                tick=tick,
                payload={
                    "pfna_refs": tuple(sorted(pfna_refs_for_tick)),
                    "prev_chain": prev_chain,
                    "C_t": p_block.C_t,
                },
            )

    manifests: Dict[str, APXManifestV1] = {}
    apxi_views: Dict[str, APXiViewV1] = {}
    for window_id, ctx in contexts.items():
        spec = resolved_specs[window_id]
        manifest = ctx.close_window(spec.apx_name)
        manifests[spec.apx_name] = manifest
        apxi_view = ctx.get_apxi_view()
        if apxi_view:
            apxi_views[manifest.apx_name] = apxi_view

        if logger and logger.enabled and logger.config.include_windows:
            logger.log(
                "window_closed",
                gid=topo.gid,
                run_id=run_id,
                window_id=window_id,
                payload={
                    "apx_name": manifest.apx_name,
                    "manifest_check": manifest.manifest_check,
                },
            )

    primary_spec = resolved_specs[primary_window_id]
    primary_manifest = manifests[primary_spec.apx_name]

    scenes: List[SceneFrameV1] = []
    envelopes: List[NAPEnvelopeV1] = []
    for ledger, p_block, prev_chain, pfna_refs in tick_cache:
        scene, envelope = build_scene_and_envelope(
            gid=topo.gid,
            run_id=run_id,
            nid=nid,
            window_id=primary_spec.window_id,
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

    codex_motifs: tuple["CodexLibraryEntryV1", ...] = ()
    codex_proposals_out: tuple["CodexProposalV1", ...] = ()
    codex_actions: tuple["CodexProposalV1", ...] = ()
    codex_hypothetical_actions: tuple["CodexProposalV1", ...] = ()
    budget_usage_meta: dict[str, object] | None = None
    governance_envelopes: list[NAPEnvelopeV1] = []

    proposals_source: Sequence["CodexProposalV1"] | None = codex_proposals
    if codex_ctx:
        codex_ctx.ingest(
            gid=topo.gid,
            run_id=run_id,
            ledgers=ledgers,
            p_blocks=p_blocks,
            i_blocks=i_blocks,
            manifests=manifests,
            envelopes=envelopes,
            window_id=primary_spec.window_id,
        )
        codex_motifs = tuple(codex_ctx.learn_edge_flux_motifs(threshold=1))
        if proposals_source is None:
            proposals_source = codex_ctx.emit_proposals(usage_threshold=1)

    governance_active = governance is not None and governance.codex_action_mode != "OFF"
    if governance_active:
        policy_ids = sorted(
            {
                *[p.policy_id for p in governance.topology_policies],
                *[p.policy_id for p in governance.budget_policies],
                *[p.policy_id for p in governance.safety_policies],
            }
        )
        governance_envelopes.append(
            NAPEnvelopeV1(
                v=int(profile.nap_defaults.get("v", 1)),
                tick=1,
                gid=topo.gid,
                nid=nid,
                layer="GOV",
                mode="G",
                payload_ref=0,
                seq=1,
                prev_chain=profile.C0,
                sig="",
                meta={
                    "event": "POLICY_SET_LOADED",
                    "policy_set_hash": governance.policy_set_hash,
                    "policy_ids": policy_ids,
                    "governance_mode": governance.governance_mode,
                    "codex_action_mode": governance.codex_action_mode,
                },
            )
        )

    if proposals_source:
        codex_proposals_out = tuple(proposals_source)
        if governance is None:
            governance = GovernanceConfigV1()
        decision: GovernedActionQueue = governed_decision_loop(
            proposals=codex_proposals_out,
            config=governance,
            window_id=primary_spec.window_id,
            evaluated_at_tick=total_ticks,
        )
        codex_proposals_out = decision.evaluated
        if decision.dry_run:
            codex_hypothetical_actions = decision.approved
        else:
            codex_actions = decision.approved
        budget_usage_meta = {
            "governance_budget": decision.budget_usage.to_dict()
        }
        governance_budget_usage: BudgetUsage | None = decision.budget_usage
        if governance_active:
            caps = [cap.to_dict() for cap in decision.budget_usage.caps]
            exhausted = [cap for cap in caps if cap.get("exhausted")]
            summary_meta = {
                "event": "GOVERNANCE_DECISION_SUMMARY",
                "policy_set_hash": governance.policy_set_hash,
                "window_id": primary_spec.window_id,
                "governance_mode": governance.governance_mode,
                "proposals_seen": decision.budget_usage.proposals_seen,
                "actions_accepted": decision.budget_usage.actions_accepted,
                "topology_changes_applied": decision.budget_usage.topology_changes_applied,
                "caps": caps,
            }
            governance_envelopes.append(
                NAPEnvelopeV1(
                    v=int(profile.nap_defaults.get("v", 1)),
                    tick=total_ticks,
                    gid=topo.gid,
                    nid=nid,
                    layer="GOV",
                    mode="G",
                    payload_ref=0,
                    seq=total_ticks,
                    prev_chain=p_blocks[-1].C_t if p_blocks else profile.C0,
                    sig="",
                meta=summary_meta,
            )
        )
            if exhausted:
                governance_envelopes.append(
                    NAPEnvelopeV1(
                        v=int(profile.nap_defaults.get("v", 1)),
                        tick=total_ticks,
                        gid=topo.gid,
                        nid=nid,
                        layer="GOV",
                        mode="G",
                        payload_ref=0,
                        seq=total_ticks + 1,
                        prev_chain=p_blocks[-1].C_t if p_blocks else profile.C0,
                        sig="",
                        meta={
                            "event": "BUDGET_EXHAUSTION",
                            "policy_set_hash": governance.policy_set_hash,
                            "window_id": primary_spec.window_id,
                            "governance_mode": governance.governance_mode,
                            "exhausted_caps": exhausted,
                        },
                    )
                )
    else:
        governance_budget_usage = None

    u_ledger_entries = build_uledger_entries(
        gid=topo.gid,
        run_id=run_id,
        window_id=primary_spec.window_id,
        ledgers=ledgers,
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=primary_manifest,
        policy_set_hash=governance.policy_set_hash if governance else None,
        governance_meta=budget_usage_meta,
    )

    final_chain = p_blocks[-1].C_t if p_blocks else profile.C0
    egress_envelopes.append(
        NAPEnvelopeV1(
            v=int(profile.nap_defaults.get("v", 1)),
            tick=total_ticks,
            gid=topo.gid,
            nid=nid,
            layer="EGRESS",
            mode=str(profile.nap_defaults.get("egress_mode", "P")),
            payload_ref=int(primary_manifest.manifest_check),
            seq=total_ticks + 2,
            prev_chain=final_chain,
            sig="",
        )
    )

    if logger and logger.enabled:
        logger.log(
            "tick_loop_end",
            gid=topo.gid,
            run_id=run_id,
            payload={
                "ticks": total_ticks,
                "envelopes": len(envelopes),
                "ingress": len(ingress_envelopes),
                "egress": len(egress_envelopes),
            },
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
        ingress_envelopes=ingress_envelopes,
        egress_envelopes=egress_envelopes,
        governance_envelopes=governance_envelopes,
        u_ledger_entries=u_ledger_entries,
        apxi_views=apxi_views,
        governance=governance,
        governance_budget_usage=governance_budget_usage,
        codex_motifs=codex_motifs,
        codex_proposals=codex_proposals_out,
        codex_actions=codex_actions,
        codex_hypothetical_actions=codex_hypothetical_actions,
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
        governance=GovernanceConfigV1(gid=topo.gid, run_id=run_id),
    )

