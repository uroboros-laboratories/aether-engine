"""Schemas and loaders for file-driven run, topology, and profile configs."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

from gate import PressStreamSpecV1, SessionConfigV1, load_pfna_v0
from governance import GovernanceConfigV1, governance_config_from_mapping
from ops import LoggingConfigV1, MetricsConfigV1
from core.tick_loop import TickLoopWindowSpec
from umx.profile_cmp0 import ProfileCMP0V1
from umx.topology_profile import TopologyProfileV1, load_topology_profile


_ALLOWED_STREAM_SOURCES = {
    "post_u_deltas",
    "fluxes",
    "pre_u",
    "post_u",
    "prev_chain",
}


@dataclass(frozen=True)
class RunWindowStreamConfigV1:
    """Definition of a Press stream declared inside a run config window."""

    name: str
    source: str
    scheme_hint: Optional[str] = None
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Run window stream must provide a name")
        if self.source not in _ALLOWED_STREAM_SOURCES:
            raise ValueError(
                f"Stream source must be one of {sorted(_ALLOWED_STREAM_SOURCES)}"
            )
        if self.scheme_hint is not None and self.scheme_hint not in {"R", "GR", "ID"}:
            raise ValueError("scheme_hint must be one of 'R', 'GR', or 'ID'")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")


@dataclass(frozen=True)
class RunWindowConfigV1:
    """APX/Press window declaration for a run config."""

    window_id: str
    apx_name: str
    start_tick: int
    end_tick: int
    streams: Tuple[RunWindowStreamConfigV1, ...] = field(default_factory=tuple)
    aeon_window_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.window_id:
            raise ValueError("window_id must be provided")
        if not self.apx_name:
            raise ValueError("apx_name must be provided")
        if self.start_tick < 1:
            raise ValueError("start_tick must be >= 1")
        if self.end_tick < self.start_tick:
            raise ValueError("end_tick must be >= start_tick")
        if not isinstance(self.streams, tuple):
            object.__setattr__(self, "streams", tuple(self.streams))
        if self.aeon_window_id is not None and not isinstance(
            self.aeon_window_id, str
        ):
            raise ValueError("aeon_window_id must be a string when provided")


@dataclass(frozen=True)
class RunConfigV1:
    """Top-level configuration for running CMP-0 style scenarios from file."""

    v: int
    gid: str
    run_id: str
    topology_path: str
    profile_path: str
    ticks: int
    initial_state: Tuple[int, ...]
    windows: Tuple[RunWindowConfigV1, ...]
    primary_window_id: str
    nap: Dict[str, Any] = field(default_factory=dict)
    governance: Dict[str, Any] = field(default_factory=dict)
    enable_codex: bool = False
    enable_pfna: bool = False
    pfna_path: Optional[str] = None
    diagnostics: Dict[str, Any] = field(default_factory=dict)
    logging: LoggingConfigV1 = field(default_factory=LoggingConfigV1)
    metrics: MetricsConfigV1 = field(default_factory=MetricsConfigV1)

    def __post_init__(self) -> None:
        if self.v != 1:
            raise ValueError("RunConfig_v1 requires v == 1")
        if not self.gid:
            raise ValueError("gid must be provided")
        if not self.run_id:
            raise ValueError("run_id must be provided")
        if self.ticks < 1:
            raise ValueError("ticks must be >= 1")
        if not self.windows:
            raise ValueError("At least one window must be provided")
        if not isinstance(self.windows, tuple):
            object.__setattr__(self, "windows", tuple(self.windows))
        window_ids = {w.window_id for w in self.windows}
        if self.primary_window_id not in window_ids:
            raise ValueError("primary_window_id must reference a declared window")
        _ensure_int_sequence(self.initial_state, "initial_state")
        if not isinstance(self.initial_state, tuple):
            object.__setattr__(self, "initial_state", tuple(self.initial_state))
        if self.pfna_path is not None and not isinstance(self.pfna_path, str):
            raise ValueError("pfna_path must be a string when provided")
        if not isinstance(self.nap, Mapping):
            raise ValueError("nap must be a mapping if provided")
        if not isinstance(self.governance, Mapping):
            raise ValueError("governance must be a mapping if provided")
        if not isinstance(self.diagnostics, Mapping):
            raise ValueError("diagnostics must be a mapping if provided")
        if not isinstance(self.logging, LoggingConfigV1):
            raise ValueError("logging must be a LoggingConfigV1 instance")
        if not isinstance(self.metrics, MetricsConfigV1):
            raise ValueError("metrics must be a MetricsConfigV1 instance")


@dataclass(frozen=True)
class ScenarioV1:
    """Entry in a scenario registry, referencing a RunConfig."""

    scenario_id: str
    description: str
    run_config_path: str
    pillars: Tuple[str, ...] = field(default_factory=tuple)
    runtime_hint: str = ""

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("scenario_id must be provided")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")
        if not self.run_config_path:
            raise ValueError("run_config_path must be provided")
        if not isinstance(self.pillars, tuple):
            object.__setattr__(self, "pillars", tuple(self.pillars))
        for pillar in self.pillars:
            if not pillar:
                raise ValueError("pillars must contain non-empty strings")
        if not isinstance(self.runtime_hint, str):
            raise ValueError("runtime_hint must be a string")


@dataclass(frozen=True)
class ScenarioRegistryV1:
    """Registry of named scenarios available for file-driven runs."""

    v: int
    scenarios: Tuple[ScenarioV1, ...]

    def __post_init__(self) -> None:
        if self.v != 1:
            raise ValueError("ScenarioRegistry_v1 requires v == 1")
        if not isinstance(self.scenarios, tuple):
            object.__setattr__(self, "scenarios", tuple(self.scenarios))
        if not self.scenarios:
            raise ValueError("Scenario registry must contain at least one entry")
        seen = set()
        for scenario in self.scenarios:
            if scenario.scenario_id in seen:
                raise ValueError(f"Duplicate scenario_id detected: {scenario.scenario_id}")
            seen.add(scenario.scenario_id)

    def list_ids(self) -> Tuple[str, ...]:
        return tuple(s.scenario_id for s in self.scenarios)

    def get(self, scenario_id: str) -> ScenarioV1:
        for scenario in self.scenarios:
            if scenario.scenario_id == scenario_id:
                return scenario
        raise KeyError(f"Scenario not found: {scenario_id}")


def run_window_stream_from_mapping(data: Mapping[str, Any]) -> RunWindowStreamConfigV1:
    if not isinstance(data, Mapping):
        raise ValueError("Stream entry must be an object")
    return RunWindowStreamConfigV1(
        name=str(data.get("name", "")),
        source=str(data.get("source", "")),
        scheme_hint=data.get("scheme_hint"),
        description=str(data.get("description", "")),
    )


def run_window_from_mapping(data: Mapping[str, Any]) -> RunWindowConfigV1:
    if not isinstance(data, Mapping):
        raise ValueError("Window entry must be an object")
    try:
        window_id = str(data["window_id"])
        apx_name = str(data["apx_name"])
        start_tick = int(data["start_tick"])
        end_tick = int(data["end_tick"])
    except KeyError as exc:  # pragma: no cover - explicit messaging
        raise ValueError(f"Missing required window field: {exc.args[0]}") from exc

    streams_raw = data.get("streams", [])
    if not isinstance(streams_raw, Sequence):
        raise ValueError("window.streams must be a list if provided")
    streams = tuple(run_window_stream_from_mapping(entry) for entry in streams_raw)

    aeon_window_id = data.get("aeon_window_id")
    return RunWindowConfigV1(
        window_id=window_id,
        apx_name=apx_name,
        start_tick=start_tick,
        end_tick=end_tick,
        streams=streams,
        aeon_window_id=aeon_window_id,
    )


def logging_config_from_mapping(data: Mapping[str, Any]) -> LoggingConfigV1:
    _ensure_mapping(data, "logging")
    return LoggingConfigV1(
        enabled=bool(data.get("enabled", False)),
        destination=str(data.get("destination", "memory")),
        file_path=data.get("file_path"),
        include_ticks=bool(data.get("include_ticks", True)),
        include_windows=bool(data.get("include_windows", True)),
    )


def metrics_config_from_mapping(data: Mapping[str, Any]) -> MetricsConfigV1:
    _ensure_mapping(data, "metrics")
    return MetricsConfigV1(enabled=bool(data.get("enabled", False)))


def _derive_governance_config(run_config: RunConfigV1) -> GovernanceConfigV1:
    base = dict(run_config.governance)
    if "governance_mode" not in base:
        if "codex_action_mode" in base:
            base["governance_mode"] = base["codex_action_mode"]
        else:
            base["governance_mode"] = "OBSERVE" if run_config.enable_codex else "OFF"
    base.setdefault("codex_action_mode", base.get("governance_mode"))
    base.setdefault("gid", run_config.gid)
    base.setdefault("run_id", run_config.run_id)

    meta = dict(base.get("meta", {}))
    meta.setdefault("nap", dict(run_config.nap))
    meta.setdefault("diagnostics", dict(run_config.diagnostics))
    base["meta"] = meta

    return governance_config_from_mapping(base)


def run_config_from_mapping(data: Mapping[str, Any]) -> RunConfigV1:
    if not isinstance(data, Mapping):
        raise ValueError("RunConfig source must be a mapping")
    try:
        version = int(data["v"])
        gid = str(data["gid"])
        run_id = str(data["run_id"])
        topology_path = str(data["topology_path"])
        profile_path = str(data["profile_path"])
        ticks = int(data["ticks"])
        primary_window_id = str(data["primary_window_id"])
    except KeyError as exc:  # pragma: no cover - explicit message
        raise ValueError(f"Missing required field: {exc.args[0]}") from exc

    windows_raw = data.get("windows")
    if not isinstance(windows_raw, Sequence):
        raise ValueError("windows must be a list")
    windows = tuple(run_window_from_mapping(entry) for entry in windows_raw)

    initial_state_raw = data.get("initial_state")
    _ensure_int_sequence(initial_state_raw, "initial_state")
    initial_state = tuple(int(v) for v in initial_state_raw)

    return RunConfigV1(
        v=version,
        gid=gid,
        run_id=run_id,
        topology_path=topology_path,
        profile_path=profile_path,
        ticks=ticks,
        initial_state=initial_state,
        windows=windows,
        primary_window_id=primary_window_id,
        nap=dict(data.get("nap", {})),
        governance=dict(data.get("governance", {})),
        enable_codex=bool(data.get("enable_codex", False)),
        enable_pfna=bool(data.get("enable_pfna", False)),
        pfna_path=data.get("pfna_path"),
        diagnostics=dict(data.get("diagnostics", {})),
        logging=logging_config_from_mapping(data.get("logging", {})),
        metrics=metrics_config_from_mapping(data.get("metrics", {})),
    )


def _ensure_mapping(obj: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(obj, Mapping):
        raise ValueError(f"{label} must be an object")
    return obj


def _load_json(path: Path) -> Mapping[str, Any]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        raise ValueError(f"{path.name} must be provided as JSON; YAML is not supported")
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:  # pragma: no cover - surfaced earlier
        raise ValueError(f"Config file not found: {path}") from exc


def _validate_path(path: Path, label: str) -> Path:
    if not path.exists():
        raise ValueError(f"{label} does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"{label} must be a file: {path}")
    return path


def load_scenario_registry(source: Union[str, Path]) -> ScenarioRegistryV1:
    """Load a ScenarioRegistry_v1 JSON document and validate its shape."""

    path = Path(source)
    data = _load_json(path)
    registry = _scenario_registry_from_mapping(data)
    return registry


def load_run_config(source: Union[str, Path]) -> RunConfigV1:
    """Load a RunConfig_v1 JSON document and validate its shape."""

    path = Path(source)
    data = _load_json(path)
    config = run_config_from_mapping(data)
    return config


def _scenario_from_mapping(data: Mapping[str, Any]) -> ScenarioV1:
    _ensure_mapping(data, "Scenario entry")
    try:
        scenario_id = str(data["scenario_id"])
        description = str(data["description"])
        run_config_path = str(data["run_config_path"])
    except KeyError as exc:  # pragma: no cover - explicit messaging
        raise ValueError(f"Scenario entry missing required field: {exc.args[0]}") from exc

    pillars_raw = data.get("pillars", [])
    if not isinstance(pillars_raw, Sequence) or isinstance(pillars_raw, (str, bytes)):
        raise ValueError("pillars must be a list of strings")
    pillars = tuple(str(pillar) for pillar in pillars_raw)

    runtime_hint = str(data.get("runtime_hint", ""))
    return ScenarioV1(
        scenario_id=scenario_id,
        description=description,
        run_config_path=run_config_path,
        pillars=pillars,
        runtime_hint=runtime_hint,
    )


def _scenario_registry_from_mapping(data: Mapping[str, Any]) -> ScenarioRegistryV1:
    _ensure_mapping(data, "Scenario registry")
    try:
        version = int(data["v"])
    except KeyError as exc:  # pragma: no cover - explicit messaging
        raise ValueError("Scenario registry missing required field: v") from exc

    scenarios_raw = data.get("scenarios")
    if not isinstance(scenarios_raw, Sequence):
        raise ValueError("scenarios must be a list")
    scenarios = tuple(_scenario_from_mapping(entry) for entry in scenarios_raw)
    return ScenarioRegistryV1(v=version, scenarios=scenarios)


def _profile_cmp_style_from_mapping(data: Mapping[str, Any]) -> ProfileCMP0V1:
    _ensure_mapping(data, "ProfileConfig")
    try:
        name = str(data["name"])
        modulus_M = int(data["modulus_M"])
        C0 = int(data["C0"])
        SC = int(data["SC"])
        I_block_spacing_W = int(data["I_block_spacing_W"])
    except KeyError as exc:  # pragma: no cover - explicit error path
        raise ValueError(f"ProfileConfig missing required field: {exc.args[0]}") from exc

    flux_rule = dict(_ensure_mapping(data.get("flux_rule", {}), "flux_rule"))
    chain_rule = dict(_ensure_mapping(data.get("chain_rule", {}), "chain_rule"))
    s_t_rule = dict(_ensure_mapping(data.get("s_t_rule", {}), "s_t_rule"))
    nap_defaults = dict(_ensure_mapping(data.get("nap_defaults", {}), "nap_defaults"))
    press_defaults = dict(
        _ensure_mapping(data.get("press_defaults", {}), "press_defaults")
    )

    if not name:
        raise ValueError("ProfileConfig name must be provided")

    return ProfileCMP0V1(
        name=name,
        modulus_M=modulus_M,
        C0=C0,
        SC=SC,
        I_block_spacing_W=I_block_spacing_W,
        flux_rule=flux_rule,
        chain_rule=chain_rule,
        s_t_rule=s_t_rule,
        nap_defaults=nap_defaults,
        press_defaults=press_defaults,
    )


def load_profile_config(source: Union[str, Path]) -> ProfileCMP0V1:
    """Load a CMP-style profile configuration (CMP-0 and beyond)."""

    path = Path(source)
    data = _load_json(path)
    return _profile_cmp_style_from_mapping(data)


def _resolve_relative(base_path: Path, reference: str, *, label: str) -> Path:
    ref_path = (base_path / reference).resolve()
    return _validate_path(ref_path, label)


def build_session_config_from_run_config(
    run_config: "RunConfigV1", *, config_base_dir: Union[str, Path]
) -> SessionConfigV1:
    """Materialise a SessionConfigV1 from an in-memory RunConfigV1.

    This mirrors the logic used by :func:`load_run_session_config` but operates on an
    already parsed RunConfig instance so callers can apply overrides before
    constructing the session.
    """

    base_dir = Path(config_base_dir).resolve()

    topo_path = _resolve_relative(base_dir, run_config.topology_path, label="topology_path")
    profile_path = _resolve_relative(base_dir, run_config.profile_path, label="profile_path")

    topo = load_topology_profile(topo_path)
    if topo.gid != run_config.gid:
        raise ValueError("RunConfig gid must match topology gid")

    profile = load_profile_config(profile_path)
    if profile.SC != topo.SC:
        raise ValueError("Profile SC must match topology SC")

    if len(run_config.initial_state) != topo.N:
        raise ValueError("initial_state length must match topology N")

    window_specs = []
    for window in run_config.windows:
        if window.end_tick > run_config.ticks:
            raise ValueError("window end_tick cannot exceed configured ticks")
        streams = tuple(
            PressStreamSpecV1(
                name=stream.name,
                source=stream.source,
                scheme_hint=stream.scheme_hint,
                description=stream.description,
            )
            for stream in window.streams
        )
        window_specs.append(
            TickLoopWindowSpec(
                window_id=window.window_id,
                apx_name=window.apx_name,
                start_tick=window.start_tick,
                end_tick=window.end_tick,
                streams=streams,
                aeon_window_id=window.aeon_window_id,
            )
        )

    if run_config.primary_window_id not in {spec.window_id for spec in window_specs}:
        raise ValueError("primary_window_id must reference a declared window")

    pfna_inputs = ()
    if run_config.enable_pfna:
        if not run_config.pfna_path:
            raise ValueError("enable_pfna is true but pfna_path is missing")
        pfna_path = _resolve_relative(base_dir, run_config.pfna_path, label="pfna_path")
        pfna_inputs = load_pfna_v0(pfna_path, expected_length=topo.N)
    elif run_config.pfna_path:
        _validate_path((base_dir / run_config.pfna_path).resolve(), "pfna_path")

    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=run_config.initial_state,
        total_ticks=run_config.ticks,
        window_specs=tuple(window_specs),
        primary_window_id=run_config.primary_window_id,
        run_id=run_config.run_id,
        nid=run_config.gid,
        pfna_inputs=pfna_inputs,
        governance=_derive_governance_config(run_config),
        logging_config=run_config.logging,
        metrics_config=run_config.metrics,
    )


def load_run_session_config(source: Union[str, Path]) -> SessionConfigV1:
    """Load a RunConfig file and materialise a Gate SessionConfig_v1."""

    config_path = Path(source).resolve()
    run_config = load_run_config(config_path)
    return build_session_config_from_run_config(run_config, config_base_dir=config_path.parent)


def load_scenario_run_config(
    scenario_id: str, *, registry_path: Union[str, Path]
) -> RunConfigV1:
    """Lookup a scenario by id from a registry and load its RunConfig."""

    registry_file = Path(registry_path).resolve()
    registry = load_scenario_registry(registry_file)
    scenario = registry.get(scenario_id)
    scenario_path = (registry_file.parent / scenario.run_config_path).resolve()
    _validate_path(scenario_path, "scenario run_config_path")
    return load_run_config(scenario_path)


def _ensure_int_sequence(values: Any, label: str) -> None:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be a sequence of integers")
    if not values:
        raise ValueError(f"{label} must be non-empty")
    for entry in values:
        if not isinstance(entry, int) or isinstance(entry, bool):
            raise ValueError(f"{label} must contain integers only")
