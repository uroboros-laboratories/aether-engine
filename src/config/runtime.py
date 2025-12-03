"""EngineRuntime wrapper for Phase 7 Operator Service flows."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any, Mapping, Optional

from governance import GovernanceConfigV1, governance_config_from_mapping
from ops import LoggingConfigV1, MetricsConfigV1

from .schemas import (
    RunConfigV1,
    ScenarioRegistryV1,
    SessionConfigV1,
    build_session_config_from_run_config,
    load_run_config,
    load_scenario_registry,
    run_config_from_mapping,
    _load_json,
)


DEFAULT_REGISTRY_PATH = Path("docs/fixtures/scenarios/scenario_registry.json")
DEFAULT_GOVERNANCE_BASE_PATH = Path("docs/fixtures/configs/governance_base.json")
DEFAULT_GOVERNANCE_OVERRIDES: Mapping[str, Any] = {
    "governance_mode": "OBSERVE",
    "codex_action_mode": "OBSERVE",
}


@dataclass
class EngineRuntime:
    """Centralised adapter for scenarios, configs, and SessionConfig construction.

    Defaults are tailored for the Phase 7 Operator Service: in-memory structured
    logging (so run logs can be streamed to the UI), metrics enabled, and a
    conservative governance posture unless explicitly overridden.
    """

    repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    scenario_registry_path: Optional[Path] = None
    governance_base_path: Optional[Path] = None
    default_logging: LoggingConfigV1 = field(
        default_factory=lambda: LoggingConfigV1(enabled=True, destination="memory")
    )
    default_metrics: MetricsConfigV1 = field(default_factory=lambda: MetricsConfigV1(enabled=True))
    default_governance_overrides: Mapping[str, Any] = field(
        default_factory=lambda: dict(DEFAULT_GOVERNANCE_OVERRIDES)
    )

    _registry_cache: Optional[ScenarioRegistryV1] = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.scenario_registry_path is None:
            self.scenario_registry_path = self.repo_root / DEFAULT_REGISTRY_PATH
        self.scenario_registry_path = self.scenario_registry_path.resolve()
        if self.governance_base_path is None:
            self.governance_base_path = self.repo_root / DEFAULT_GOVERNANCE_BASE_PATH
        self.governance_base_path = self.governance_base_path.resolve()

        # Prime governance defaults from disk if present.
        self.load_governance_base()

    def load_registry(self) -> ScenarioRegistryV1:
        """Load and cache the scenario registry."""

        if self._registry_cache is None:
            self._registry_cache = load_scenario_registry(self.scenario_registry_path)
        return self._registry_cache

    def refresh_registry(self) -> ScenarioRegistryV1:
        """Clear and reload the cached registry after a mutation."""

        self._registry_cache = None
        return self.load_registry()

    def load_run_config(self, scenario_id: str) -> tuple[RunConfigV1, Path]:
        """Load a run config for the given scenario and return it with its base dir."""

        registry = self.load_registry()
        scenario = registry.get(scenario_id)
        config_path = self._resolve_run_config_path(scenario)
        run_config = load_run_config(config_path)
        return run_config, config_path.parent

    def load_governance_base(self) -> Mapping[str, Any]:
        """Load the base governance mapping used for UI-launched runs."""

        snapshot: Mapping[str, Any] = self.default_governance_overrides
        if self.governance_base_path and self.governance_base_path.exists():
            raw = _load_json(self.governance_base_path)
            if not isinstance(raw, Mapping):
                raise ValueError("governance base must be an object")
            snapshot = {**DEFAULT_GOVERNANCE_OVERRIDES, **raw}

        validated = governance_config_from_mapping(snapshot)
        sanitized = self._governance_snapshot(validated)
        self.default_governance_overrides = sanitized
        return dict(sanitized)

    def update_governance_base(self, updates: Mapping[str, Any]) -> Mapping[str, Any]:
        """Persist governance overrides for future SessionConfig builds."""

        base = dict(self.load_governance_base())
        merged = {**base}

        if "budget_policies" in updates:
            merged["budget_policies"] = self._merge_budget_policies(
                base.get("budget_policies", ()), updates["budget_policies"]
            )

        for key in (
            "governance_mode",
            "codex_action_mode",
            "topology_policies",
            "safety_policies",
            "gid",
            "run_id",
            "meta",
        ):
            if key in updates:
                merged[key] = updates[key]

        if "codex_action_mode" in updates and "governance_mode" not in updates:
            merged["governance_mode"] = updates["codex_action_mode"]

        validated = governance_config_from_mapping(merged)
        sanitized = self._governance_snapshot(validated)
        self.default_governance_overrides = sanitized

        if self.governance_base_path:
            self.governance_base_path.write_text(
                json.dumps(sanitized, sort_keys=True, indent=2) + "\n"
            )
        return dict(sanitized)

    def update_scenario_metadata(
        self, scenario_id: str, *, description: Optional[str] = None, runtime_hint: Optional[str] = None
    ) -> ScenarioRegistryV1:
        """Persist scenario metadata updates to the registry file."""

        registry_data = _load_json(self.scenario_registry_path)
        scenarios_raw = registry_data.get("scenarios", [])
        found = False
        for entry in scenarios_raw:
            if entry.get("scenario_id") == scenario_id:
                if description is not None:
                    entry["description"] = str(description)
                if runtime_hint is not None:
                    entry["runtime_hint"] = str(runtime_hint)
                found = True
                break
        if not found:
            raise KeyError(f"Scenario not found: {scenario_id}")

        self.scenario_registry_path.write_text(
            json.dumps(registry_data, sort_keys=True, indent=2) + "\n"
        )
        return self.refresh_registry()

    def update_run_config(self, scenario_id: str, updates: Mapping[str, Any]) -> RunConfigV1:
        """Persist whitelisted run config updates for a scenario."""

        scenario = self.load_registry().get(scenario_id)
        config_path = self._resolve_run_config_path(scenario)
        config_data = dict(_load_json(config_path))

        if "ticks" in updates:
            config_data["ticks"] = int(updates["ticks"])
        if "enable_codex" in updates:
            config_data["enable_codex"] = bool(updates["enable_codex"])
        if "enable_pfna" in updates:
            config_data["enable_pfna"] = bool(updates["enable_pfna"])
        if "run_id" in updates:
            config_data["run_id"] = str(updates["run_id"])
        if "gid" in updates:
            config_data["gid"] = str(updates["gid"])

        updated_config = run_config_from_mapping(config_data)
        config_path.write_text(json.dumps(asdict(updated_config), sort_keys=True, indent=2) + "\n")
        return updated_config

    def build_session_config(
        self, scenario_id: str, overrides: Optional[Mapping[str, Any]] = None
    ) -> SessionConfigV1:
        """Resolve a scenario ID into a fully built SessionConfigV1."""

        run_config, base_dir = self.load_run_config(scenario_id)
        patched_config = self._apply_overrides(run_config, overrides or {})
        return build_session_config_from_run_config(patched_config, config_base_dir=base_dir)

    # Internal helpers -------------------------------------------------

    def _apply_overrides(
        self, run_config: RunConfigV1, overrides: Mapping[str, Any]
    ) -> RunConfigV1:
        config = run_config

        if "run_id" in overrides:
            config = replace(config, run_id=str(overrides["run_id"]))

        if "ticks" in overrides:
            config = replace(config, ticks=int(overrides["ticks"]))

        logging_override = overrides.get("logging")
        logging_config = self._resolve_logging_override(config.logging, logging_override)

        metrics_override = overrides.get("metrics")
        metrics_config = self._resolve_metrics_override(config.metrics, metrics_override)

        governance_override = overrides.get("governance")
        governance_mapping = dict(config.governance)
        if governance_override:
            governance_mapping.update(dict(governance_override))
        if self.default_governance_overrides:
            merged_defaults = dict(self.default_governance_overrides)
            merged_defaults.update(governance_mapping)
            governance_mapping = merged_defaults

        return replace(
            config,
            logging=logging_config,
            metrics=metrics_config,
            governance=governance_mapping,
        )

    def _resolve_run_config_path(self, scenario: object) -> Path:
        run_config_path = getattr(scenario, "run_config_path")
        return (self.scenario_registry_path.parent / run_config_path).resolve()

    def _resolve_logging_override(
        self, current: LoggingConfigV1, override: Optional[Mapping[str, Any]]
    ) -> LoggingConfigV1:
        if override is None:
            return current if current.enabled else self.default_logging
        if isinstance(override, LoggingConfigV1):
            return override
        if not isinstance(override, Mapping):
            raise ValueError("logging override must be a mapping or LoggingConfigV1")
        return LoggingConfigV1(
            enabled=bool(override.get("enabled", True)),
            destination=str(override.get("destination", self.default_logging.destination)),
            file_path=override.get("file_path", current.file_path),
            include_ticks=bool(override.get("include_ticks", current.include_ticks)),
            include_windows=bool(override.get("include_windows", current.include_windows)),
        )

    def _resolve_metrics_override(
        self, current: MetricsConfigV1, override: Optional[Mapping[str, Any]]
    ) -> MetricsConfigV1:
        if override is None:
            return current if current.enabled else self.default_metrics
        if isinstance(override, MetricsConfigV1):
            return override
        if not isinstance(override, Mapping):
            raise ValueError("metrics override must be a mapping or MetricsConfigV1")
        return MetricsConfigV1(enabled=bool(override.get("enabled", True)))

    @staticmethod
    def _governance_snapshot(config: GovernanceConfigV1) -> dict[str, Any]:
        snapshot = config.to_dict()
        snapshot.pop("policy_set_hash", None)
        return snapshot

    @staticmethod
    def _merge_budget_policies(
        existing: object, updates: object
    ) -> tuple[Mapping[str, Any], ...]:
        if updates is None:
            return tuple(existing or ())
        if not isinstance(updates, (Mapping, tuple, list)):
            raise ValueError("budget_policies must be a list of objects")

        def _normalize(entries: object) -> dict[str, dict[str, Any]]:
            policies: dict[str, dict[str, Any]] = {}
            if not entries:
                return policies
            if isinstance(entries, Mapping):
                entries = (entries,)
            if not isinstance(entries, (tuple, list)):
                raise ValueError("budget_policies must be a list of objects")
            for entry in entries:
                if not isinstance(entry, Mapping):
                    raise ValueError("budget_policies must contain objects")
                policy_id = str(entry.get("policy_id", ""))
                if not policy_id:
                    raise ValueError("budget_policies entries require policy_id")
                policies[policy_id] = dict(entry)
            return policies

        merged = _normalize(existing)
        for policy_id, payload in _normalize(updates).items():
            if policy_id in merged:
                merged[policy_id].update({k: v for k, v in payload.items() if k != "policy_id"})
            else:
                merged[policy_id] = payload
                merged[policy_id]["policy_id"] = policy_id

        return tuple(merged.values())

