"""Read-only introspection helpers for Phase 3 governance (SPEC-006 P3.2.3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union

if TYPE_CHECKING:  # pragma: no cover - import guard for typing only
    from codex.context import CodexLibraryEntryV1, CodexProposalV1
    from core.tick_loop import GF01RunResult
    from gate import NAPEnvelopeV1, SessionRunResult
    from loom.loom import LoomIBlockV1, LoomPBlockV1
    from press import APXManifestV1, APXiViewV1
    from uledger import ULedgerEntryV1
    from umx.tick_ledger import UMXTickLedgerV1


def _map_by_tick(items: Iterable[object]) -> Dict[int, object]:
    grouped: Dict[int, object] = {}
    for item in items:
        tick = int(getattr(item, "tick"))
        grouped[tick] = item
    return grouped


def _all_envelopes_from_run(
    run: object, lifecycle: Sequence["NAPEnvelopeV1"]
) -> Tuple["NAPEnvelopeV1", ...]:
    ordered: list["NAPEnvelopeV1"] = list(lifecycle)
    ingress_by_tick: Dict[int, list["NAPEnvelopeV1"]] = {}
    for env in run.ingress_envelopes:
        ingress_by_tick.setdefault(env.tick, []).append(env)

    for idx in range(len(run.envelopes)):
        tick = idx + 1
        ordered.extend(ingress_by_tick.get(tick, []))
        ordered.append(run.envelopes[idx])

    ordered.extend(run.egress_envelopes)
    return tuple(ordered)


def _map_artifacts_by_window(
    artifacts: Mapping[str, object], window_specs: Sequence[object] | None, scenes: Sequence[object]
) -> Dict[str, object]:
    if not artifacts:
        return {}

    mapping: Dict[str, object] = {}
    if window_specs:
        by_apx = {spec.apx_name: spec.window_id for spec in window_specs}
        for apx_name, artifact in artifacts.items():
            window_id = by_apx.get(apx_name)
            if window_id:
                mapping[window_id] = artifact

    if not mapping:
        for artifact in artifacts.values():
            window_id = getattr(artifact, "window_id", None)
            if window_id:
                mapping.setdefault(str(window_id), artifact)

    if not mapping:
        manifest_by_check = {getattr(obj, "manifest_check", None): obj for obj in artifacts.values()}
        for scene in scenes:
            manifest = manifest_by_check.get(getattr(scene, "manifest_check", None))
            window_id = getattr(scene, "window_id", None)
            if window_id and manifest is not None:
                mapping.setdefault(str(window_id), manifest)

    if not mapping:
        mapping = dict(artifacts)

    return mapping


@dataclass(frozen=True)
class IntrospectionViewV1:
    """Deterministic, read-only view over run artefacts."""

    gid: str
    run_id: str
    total_ticks: int
    window_ids: Tuple[str, ...]
    ledgers_by_tick: Mapping[int, UMXTickLedgerV1]
    p_blocks_by_tick: Mapping[int, LoomPBlockV1]
    i_blocks_by_tick: Mapping[int, LoomIBlockV1]
    manifests_by_window: Mapping[str, APXManifestV1]
    apxi_views_by_window: Mapping[str, APXiViewV1]
    envelopes: Tuple["NAPEnvelopeV1", ...]
    uledger_by_tick: Mapping[int, ULedgerEntryV1]
    codex_motifs: Tuple["CodexLibraryEntryV1", ...] = field(default_factory=tuple)
    codex_proposals: Tuple["CodexProposalV1", ...] = field(default_factory=tuple)

    def get_umx_ledger(self, tick: int) -> UMXTickLedgerV1:
        try:
            return self.ledgers_by_tick[int(tick)]
        except KeyError as exc:
            raise ValueError(f"No UMX tick ledger found for tick {tick}") from exc

    def get_loom_p_block(self, tick: int) -> LoomPBlockV1:
        try:
            return self.p_blocks_by_tick[int(tick)]
        except KeyError as exc:
            raise ValueError(f"No Loom P-block found for tick {tick}") from exc

    def get_loom_i_block(self, tick: int) -> LoomIBlockV1:
        try:
            return self.i_blocks_by_tick[int(tick)]
        except KeyError as exc:
            raise ValueError(f"No Loom I-block found for tick {tick}") from exc

    def get_apx_manifest(self, window_id: str) -> APXManifestV1:
        try:
            return self.manifests_by_window[window_id]
        except KeyError as exc:
            raise ValueError(f"No APX manifest found for window_id '{window_id}'") from exc

    def get_apxi_view(self, window_id: str) -> APXiViewV1:
        try:
            return self.apxi_views_by_window[window_id]
        except KeyError as exc:
            raise ValueError(f"No APXi view found for window_id '{window_id}'") from exc

    def get_nap_envelopes(
        self, *, tick: Optional[int] = None, layer: Optional[str] = None
    ) -> Tuple["NAPEnvelopeV1", ...]:
        envelopes = self.envelopes
        if tick is not None:
            envelopes = tuple(env for env in envelopes if env.tick == int(tick))
        if layer is not None:
            envelopes = tuple(env for env in envelopes if env.layer == layer)
        return envelopes

    def get_uledger_entry(self, tick: int) -> ULedgerEntryV1:
        try:
            return self.uledger_by_tick[int(tick)]
        except KeyError as exc:
            raise ValueError(f"No U-ledger entry found for tick {tick}") from exc

    def list_codex_motifs(self) -> Tuple[CodexLibraryEntryV1, ...]:
        return self.codex_motifs

    def list_codex_proposals(self) -> Tuple[CodexProposalV1, ...]:
        return self.codex_proposals


def build_introspection_view(
    run: Union[SessionRunResult, "GF01RunResult"],
    *,
    codex_motifs: Optional[Sequence[CodexLibraryEntryV1]] = None,
    codex_proposals: Optional[Sequence[CodexProposalV1]] = None,
) -> IntrospectionViewV1:
    """Create an IntrospectionViewV1 from a run result.

    The view is read-only and returns existing artefacts without mutation.
    """

    from core.tick_loop import GF01RunResult as _GF01RunResult
    from gate import SessionRunResult

    if isinstance(run, SessionRunResult):
        gid = run.config.topo.gid
        run_id = run.config.run_id
        tick_result = run.tick_result
        lifecycle = tuple(run.lifecycle_envelopes)
    elif isinstance(run, _GF01RunResult):
        gid = run.topo.gid
        run_id = run.run_id
        tick_result = run
        lifecycle = ()
    else:  # pragma: no cover - defensive
        raise TypeError("build_introspection_view expects SessionRunResult or GF01RunResult")

    ledgers_by_tick = _map_by_tick(tick_result.ledgers)
    p_blocks_by_tick = _map_by_tick(tick_result.p_blocks)
    i_blocks_by_tick = _map_by_tick(tick_result.i_blocks)
    window_specs = getattr(run, "config", None) and run.config.window_specs or None
    scenes = getattr(tick_result, "scenes", ())
    manifests_by_window = _map_artifacts_by_window(
        tick_result.manifests,
        window_specs,
        scenes,
    )
    apxi_views_by_window = _map_artifacts_by_window(
        tick_result.apxi_views,
        window_specs,
        scenes,
    )
    envelopes = _all_envelopes_from_run(tick_result, lifecycle)
    uledger_by_tick = {entry.tick: entry for entry in tick_result.u_ledger_entries}
    window_ids = tuple(sorted(manifests_by_window.keys()))

    motifs = tuple(codex_motifs) if codex_motifs is not None else ()
    proposals = tuple(codex_proposals) if codex_proposals is not None else ()

    return IntrospectionViewV1(
        gid=gid,
        run_id=run_id,
        total_ticks=len(tick_result.ledgers),
        window_ids=window_ids,
        ledgers_by_tick=ledgers_by_tick,
        p_blocks_by_tick=p_blocks_by_tick,
        i_blocks_by_tick=i_blocks_by_tick,
        manifests_by_window=manifests_by_window,
        apxi_views_by_window=apxi_views_by_window,
        envelopes=envelopes,
        uledger_by_tick=uledger_by_tick,
        codex_motifs=motifs,
        codex_proposals=proposals,
    )
