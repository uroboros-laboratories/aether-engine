"""Multi-graph configuration, topology registry, and run context utilities."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    Callable,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
)

from core.slp import SLPEventV1, apply_slp_events
from loom.run_context import LoomRunContext
from umx.profile_cmp0 import ProfileCMP0V1
from umx.run_context import UMXRunContext
from umx.topology_profile import TopologyProfileV1, load_topology_profile


@dataclass(frozen=True)
class GraphRunConfigV1:
    """Per-graph configuration for a multi-graph session."""

    gid: str
    topology_path: str
    profile_path: str
    initial_state: Tuple[int, ...]
    ticks: int
    run_id: str | None = None
    nid: str = ""
    window_id: str = ""
    label: str = ""
    meta: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.gid:
            raise ValueError("gid must be provided")
        if self.ticks < 1:
            raise ValueError("ticks must be >= 1")
        if not isinstance(self.initial_state, tuple):
            object.__setattr__(self, "initial_state", tuple(self.initial_state))
        if not self.initial_state:
            raise ValueError("initial_state must be non-empty")
        for value in self.initial_state:
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError("initial_state must contain integers")
        if not isinstance(self.meta, Mapping):
            raise ValueError("meta must be a mapping")
        if not self.nid:
            object.__setattr__(self, "nid", self.gid)
        if not self.window_id:
            object.__setattr__(self, "window_id", f"{self.gid}_window_all_ticks")


@dataclass(frozen=True)
class MultiGraphRunConfigV1:
    """Top-level configuration capturing multiple graph configs for one session."""

    v: int
    graphs: Tuple[GraphRunConfigV1, ...]
    label: str = ""
    meta: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.v != 1:
            raise ValueError("MultiGraphRunConfig_v1 requires v == 1")
        if not isinstance(self.graphs, tuple):
            object.__setattr__(self, "graphs", tuple(self.graphs))
        if not self.graphs:
            raise ValueError("At least one graph config is required")
        seen = set()
        for graph in self.graphs:
            if graph.gid in seen:
                raise ValueError(f"Duplicate gid detected: {graph.gid}")
            seen.add(graph.gid)
        if not isinstance(self.meta, Mapping):
            raise ValueError("meta must be a mapping")


class TopologyRegistry:
    """Load and validate topology/profile pairs keyed by gid."""

    def __init__(
        self, entries: Mapping[str, Tuple[TopologyProfileV1, ProfileCMP0V1]]
    ) -> None:
        self._topologies: Dict[str, TopologyProfileV1] = {}
        self._profiles: Dict[str, ProfileCMP0V1] = {}
        for gid, (topo, profile) in entries.items():
            self._register(gid, topo, profile)

    @classmethod
    def from_config(
        cls, config: MultiGraphRunConfigV1, *, base_dir: Optional[Path] = None
    ) -> "TopologyRegistry":
        from config.schemas import load_profile_config

        base = Path(base_dir) if base_dir else Path.cwd()
        entries: Dict[str, Tuple[TopologyProfileV1, ProfileCMP0V1]] = {}
        for graph in config.graphs:
            topo_path = (base / graph.topology_path).resolve()
            profile_path = (base / graph.profile_path).resolve()
            topo = load_topology_profile(topo_path)
            profile = load_profile_config(profile_path)
            if topo.gid != graph.gid:
                raise ValueError("Topology gid must match graph gid")
            if profile.SC != topo.SC:
                raise ValueError("Profile SC must match topology SC")
            entries[graph.gid] = (topo, profile)
        return cls(entries)

    def _register(
        self, gid: str, topo: TopologyProfileV1, profile: ProfileCMP0V1
    ) -> None:
        if gid in self._topologies:
            raise ValueError(f"Topology registry already has gid {gid}")
        self._topologies[gid] = topo
        self._profiles[gid] = profile

    def topologies(self) -> Mapping[str, TopologyProfileV1]:
        return dict(self._topologies)

    def profiles(self) -> Mapping[str, ProfileCMP0V1]:
        return dict(self._profiles)

    def get_topology(self, gid: str) -> TopologyProfileV1:
        return self._topologies[gid]

    def get_profile(self, gid: str) -> ProfileCMP0V1:
        return self._profiles[gid]

    def update_topology(self, gid: str, topo: TopologyProfileV1) -> None:
        if topo.gid != gid:
            raise ValueError("Topology gid must match registry key")
        if gid not in self._topologies:
            raise KeyError(f"Unknown gid: {gid}")
        self._topologies[gid] = topo


class MultiGraphRunContext:
    """Coordinate multiple UMX/Loom contexts under a shared session tick."""

    def __init__(
        self,
        config: MultiGraphRunConfigV1,
        registry: TopologyRegistry,
        *,
        schedule_hook: Optional[Callable[[str, int], bool]] = None,
    ) -> None:
        self.config = config
        self.registry = registry
        self.tick = 0
        self.umx: Dict[str, UMXRunContext] = {}
        self.loom: Dict[str, LoomRunContext] = {}
        self._config_by_gid: Dict[str, GraphRunConfigV1] = {
            graph.gid: graph for graph in self.config.graphs
        }
        self._slp_queue: MutableMapping[int, List[SLPEventV1]] = {}
        self._last_tick_results: Dict[str, TickResult] = {}
        self._schedule_hook = schedule_hook or (lambda _gid, _tick: True)
        self._init_contexts()

    def _init_contexts(self) -> None:
        for graph in self.config.graphs:
            topo = self.registry.get_topology(graph.gid)
            profile = self.registry.get_profile(graph.gid)
            if len(graph.initial_state) != topo.N:
                raise ValueError("initial_state length must match topology N")
            umx_ctx = UMXRunContext(
                topo=topo,
                profile=profile,
                gid=graph.gid,
                run_id=graph.run_id or graph.gid,
            )
            umx_ctx.init_state(list(graph.initial_state))
            loom_ctx = LoomRunContext(profile=profile, topo=topo, umx_ctx=umx_ctx)
            self.umx[graph.gid] = umx_ctx
            self.loom[graph.gid] = loom_ctx

    def queue_slp_event(self, event: SLPEventV1) -> None:
        if event.gid not in self.umx:
            raise KeyError(f"Unknown gid {event.gid}")
        if event.tick_effective <= self.tick:
            raise ValueError("tick_effective must be greater than the current tick")
        self._slp_queue.setdefault(event.tick_effective, []).append(event)

    def _apply_pending_events(self, next_tick: int) -> None:
        pending = self._slp_queue.pop(next_tick, [])
        by_gid: Dict[str, List[SLPEventV1]] = {}
        for event in pending:
            by_gid.setdefault(event.gid, []).append(event)
        for gid, events in by_gid.items():
            topo = self.registry.get_topology(gid)
            new_topo = apply_slp_events(topo, events)
            self.registry.update_topology(gid, new_topo)
            umx_ctx = self.umx[gid]
            umx_ctx.topo = new_topo
            if umx_ctx.state is not None:
                state = list(umx_ctx.state)
                if len(state) < new_topo.N:
                    state.extend([0] * (new_topo.N - len(state)))
                elif len(state) > new_topo.N:
                    state = state[: new_topo.N]
                umx_ctx.state = state
            loom_ctx = self.loom[gid]
            loom_ctx.topo = new_topo

    def step_all(
        self, *, skip_gids: Optional[Sequence[str]] = None
    ) -> Dict[str, Tuple[UMXRunContext, LoomRunContext]]:
        next_tick = self.tick + 1
        self._apply_pending_events(next_tick)
        results: Dict[str, Tuple[UMXRunContext, LoomRunContext]] = {}
        skip = set(skip_gids or [])
        self._last_tick_results = {}
        for gid, umx_ctx in self.umx.items():
            if gid in skip or not self._schedule_hook(gid, next_tick):
                continue
            ledger = umx_ctx.step()
            loom_ctx = self.loom[gid]
            chain_before = loom_ctx.C_t
            p_block, maybe_i_block = loom_ctx.ingest_tick(ledger)
            self._last_tick_results[gid] = TickResult(
                umx_ctx=umx_ctx,
                loom_ctx=loom_ctx,
                ledger=ledger,
                p_block=p_block,
                i_block=maybe_i_block,
                C_prev=chain_before,
            )
            results[gid] = (umx_ctx, loom_ctx)
        self.tick = next_tick
        return results

    def scene_frames_for_last_tick(
        self,
        *,
        window_id_factory: Optional[Callable[[str], str]] = None,
        manifest_check: Optional[int] = None,
        nap_envelope_ref: Optional[str] = None,
    ) -> Mapping[str, "SceneFrameV1"]:
        if not self._last_tick_results:
            raise ValueError("No tick results available; call step_all() first")

        from gate.gate import build_scene_frame, SceneFrameV1

        frames: Dict[str, SceneFrameV1] = {}
        for gid, tick_result in self._last_tick_results.items():
            graph_cfg = self._config_by_gid[gid]
            window_id = (
                window_id_factory(gid)
                if window_id_factory is not None
                else graph_cfg.window_id
            )
            frames[gid] = build_scene_frame(
                gid=gid,
                run_id=graph_cfg.run_id or gid,
                nid=graph_cfg.nid,
                ledger=tick_result.ledger,
                C_prev=tick_result.C_prev,
                C_t=tick_result.p_block.C_t,
                window_id=window_id,
                manifest_check=manifest_check,
                nap_envelope_ref=nap_envelope_ref,
                ledger_ref=f"{gid}_tick_{tick_result.ledger.tick}",
                meta={"p_block_ref": f"p_block_{tick_result.p_block.seq}"},
            )
        return frames

    def last_tick_results(self) -> Mapping[str, TickResult]:
        """Return the most recent tick results for downstream consumers."""

        if not self._last_tick_results:
            raise ValueError("No tick results available; call step_all() first")
        return dict(self._last_tick_results)


@dataclass(frozen=True)
class TickResult:
    umx_ctx: UMXRunContext
    loom_ctx: LoomRunContext
    ledger: "UMXTickLedgerV1"
    p_block: "LoomPBlockV1"
    i_block: Optional["LoomIBlockV1"]
    C_prev: int


# Config helpers -----------------------------------------------------------

def multigraph_config_from_mapping(data: Mapping[str, object]) -> MultiGraphRunConfigV1:
    if not isinstance(data, Mapping):
        raise ValueError("MultiGraphRunConfig must be an object")
    try:
        version = int(data["v"])
    except KeyError as exc:  # pragma: no cover - explicit messaging
        raise ValueError("MultiGraphRunConfig missing required field: v") from exc
    graphs_raw = data.get("graphs")
    if not isinstance(graphs_raw, Sequence):
        raise ValueError("graphs must be a list")
    graphs = tuple(_graph_from_mapping(entry) for entry in graphs_raw)
    return MultiGraphRunConfigV1(v=version, graphs=graphs, label=str(data.get("label", "")), meta=data.get("meta", {}))


def _graph_from_mapping(data: Mapping[str, object]) -> GraphRunConfigV1:
    if not isinstance(data, Mapping):
        raise ValueError("Graph entry must be an object")
    try:
        gid = str(data["gid"])
        topology_path = str(data["topology_path"])
        profile_path = str(data["profile_path"])
        initial_state_raw = data["initial_state"]
        ticks = int(data["ticks"])
    except KeyError as exc:  # pragma: no cover - explicit messaging
        raise ValueError(f"Graph config missing required field: {exc.args[0]}") from exc
    if not isinstance(initial_state_raw, Sequence) or isinstance(initial_state_raw, (str, bytes)):
        raise ValueError("initial_state must be a list of integers")
    initial_state = tuple(int(v) for v in initial_state_raw)
    return GraphRunConfigV1(
        gid=gid,
        topology_path=topology_path,
        profile_path=profile_path,
        initial_state=initial_state,
        ticks=ticks,
        run_id=str(data.get("run_id") or gid),
        nid=str(data.get("nid") or gid),
        window_id=str(data.get("window_id", "")),
        label=str(data.get("label", "")),
        meta=data.get("meta", {}),
    )


def load_multigraph_run_config(source: str | Path) -> MultiGraphRunConfigV1:
    path = Path(source)
    if path.suffix.lower() in {".yaml", ".yml"}:
        raise ValueError("Multi-graph config loader only supports JSON; please convert YAML")
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError as exc:  # pragma: no cover - surfaced earlier
        raise ValueError(f"Config file not found: {path}") from exc
    return multigraph_config_from_mapping(data)
