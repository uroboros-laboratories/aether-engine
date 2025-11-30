"""Governance contracts for Phase 5 policy and budget enforcement."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional, Sequence, Tuple

from uledger.canonical import hash_record

ALLOWED_ACTION_MODES = (
    "OFF",
    "OBSERVE",
    "SUGGEST_ONLY",
    "DRY_RUN",
    "GOVERNED_APPLY",
    "ENFORCE",
)
ALLOWED_TOPOLOGY_OPS = (
    "ADD_NODE",
    "REMOVE_NODE",
    "ADD_EDGE",
    "REMOVE_EDGE",
    "REWIRE",
    "TUNE",
)


def _ensure_policy_id(policy_id: str, label: str) -> None:
    if not isinstance(policy_id, str) or not policy_id:
        raise ValueError(f"{label} must be a non-empty string")


def _ensure_non_negative(value: Optional[int], label: str) -> None:
    if value is None:
        return
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer when provided")


def _normalize_action_mode(
    *, governance_mode: Optional[str], codex_action_mode: str
) -> Tuple[str, str]:
    """Map legacy/new governance mode hints to canonical pairs."""

    raw = governance_mode or codex_action_mode
    if not isinstance(raw, str) or not raw:
        raise ValueError("governance_mode/codex_action_mode must be a non-empty string")

    upper = raw.upper()
    if upper not in ALLOWED_ACTION_MODES:
        raise ValueError(f"codex_action_mode must be one of {sorted(ALLOWED_ACTION_MODES)}")

    if upper == "SUGGEST_ONLY":
        return "OBSERVE", "OBSERVE"
    if upper == "OBSERVE":
        return "OBSERVE", "OBSERVE"
    if upper == "DRY_RUN":
        return "DRY_RUN", "DRY_RUN"
    if upper in {"GOVERNED_APPLY", "ENFORCE"}:
        return "ENFORCE", "GOVERNED_APPLY"
    return "OFF", "OFF"


@dataclass(frozen=True)
class TopologyPolicyV1:
    """Constraints on topology size and allowed structural operations."""

    policy_id: str
    max_nodes: Optional[int] = None
    max_edges: Optional[int] = None
    allowed_ops: Tuple[str, ...] = field(default_factory=lambda: ALLOWED_TOPOLOGY_OPS)
    description: str = ""

    def __post_init__(self) -> None:
        _ensure_policy_id(self.policy_id, "policy_id")
        _ensure_non_negative(self.max_nodes, "max_nodes")
        _ensure_non_negative(self.max_edges, "max_edges")

        if not isinstance(self.allowed_ops, tuple):
            object.__setattr__(self, "allowed_ops", tuple(self.allowed_ops))

        for op in self.allowed_ops:
            if op not in ALLOWED_TOPOLOGY_OPS:
                raise ValueError(
                    f"allowed_ops entries must be one of {sorted(ALLOWED_TOPOLOGY_OPS)}"
                )

        if not isinstance(self.description, str):
            raise ValueError("description must be a string")


@dataclass(frozen=True)
class BudgetPolicyV1:
    """Budget caps for governance-controlled actions and proposals."""

    policy_id: str
    max_actions_per_window: Optional[int] = None
    max_proposals_per_window: Optional[int] = None
    max_topology_changes: Optional[int] = None
    notes: str = ""

    def __post_init__(self) -> None:
        _ensure_policy_id(self.policy_id, "policy_id")
        _ensure_non_negative(self.max_actions_per_window, "max_actions_per_window")
        _ensure_non_negative(self.max_proposals_per_window, "max_proposals_per_window")
        _ensure_non_negative(self.max_topology_changes, "max_topology_changes")
        if not isinstance(self.notes, str):
            raise ValueError("notes must be a string")


@dataclass(frozen=True)
class SafetyPolicyV1:
    """Invariants that must hold during Codex-governed runs."""

    policy_id: str
    invariants: Tuple[str, ...]
    severity: str = "HARD"
    description: str = ""

    def __post_init__(self) -> None:
        _ensure_policy_id(self.policy_id, "policy_id")
        if not isinstance(self.invariants, tuple):
            object.__setattr__(self, "invariants", tuple(self.invariants))
        if not self.invariants:
            raise ValueError("invariants must contain at least one entry")
        for invariant in self.invariants:
            if not isinstance(invariant, str) or not invariant:
                raise ValueError("invariants must be non-empty strings")
        if self.severity not in {"HARD", "SOFT"}:
            raise ValueError("severity must be 'HARD' or 'SOFT'")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")


@dataclass(frozen=True)
class GovernanceConfigV1:
    """Governance configuration for a run/session, including policy sets."""

    governance_mode: Optional[str] = None
    codex_action_mode: str = "OFF"
    topology_policies: Tuple[TopologyPolicyV1, ...] = field(default_factory=tuple)
    budget_policies: Tuple[BudgetPolicyV1, ...] = field(default_factory=tuple)
    safety_policies: Tuple[SafetyPolicyV1, ...] = field(default_factory=tuple)
    gid: Optional[str] = None
    run_id: Optional[str] = None
    meta: Dict[str, object] = field(default_factory=dict)
    policy_set_hash: str = field(init=False)

    def __post_init__(self) -> None:
        governance_mode, codex_mode = _normalize_action_mode(
            governance_mode=self.governance_mode, codex_action_mode=self.codex_action_mode
        )
        object.__setattr__(self, "governance_mode", governance_mode)
        object.__setattr__(self, "codex_action_mode", codex_mode)

        if not isinstance(self.topology_policies, tuple):
            object.__setattr__(self, "topology_policies", tuple(self.topology_policies))
        if not isinstance(self.budget_policies, tuple):
            object.__setattr__(self, "budget_policies", tuple(self.budget_policies))
        if not isinstance(self.safety_policies, tuple):
            object.__setattr__(self, "safety_policies", tuple(self.safety_policies))

        self._validate_policy_ids()

        if self.gid is not None and (not isinstance(self.gid, str) or not self.gid):
            raise ValueError("gid must be a non-empty string when provided")
        if self.run_id is not None and (not isinstance(self.run_id, str) or not self.run_id):
            raise ValueError("run_id must be a non-empty string when provided")
        if not isinstance(self.meta, dict):
            raise ValueError("meta must be a dictionary")

        payload = self._policy_payload()
        policy_hash = hash_record(payload)
        object.__setattr__(self, "policy_set_hash", policy_hash)

    def _validate_policy_ids(self) -> None:
        seen = set()
        for collection in (
            self.topology_policies,
            self.budget_policies,
            self.safety_policies,
        ):
            for policy in collection:
                if policy.policy_id in seen:
                    raise ValueError(f"Duplicate policy_id detected: {policy.policy_id}")
                seen.add(policy.policy_id)

    def _policy_payload(self) -> Dict[str, object]:
        return {
            "governance_mode": self.governance_mode,
            "codex_action_mode": self.codex_action_mode,
            "topology_policies": [
                {
                    "policy_id": p.policy_id,
                    "max_nodes": p.max_nodes,
                    "max_edges": p.max_edges,
                    "allowed_ops": list(p.allowed_ops),
                    "description": p.description,
                }
                for p in sorted(self.topology_policies, key=lambda p: p.policy_id)
            ],
            "budget_policies": [
                {
                    "policy_id": p.policy_id,
                    "max_actions_per_window": p.max_actions_per_window,
                    "max_proposals_per_window": p.max_proposals_per_window,
                    "max_topology_changes": p.max_topology_changes,
                    "notes": p.notes,
                }
                for p in sorted(self.budget_policies, key=lambda p: p.policy_id)
            ],
            "safety_policies": [
                {
                    "policy_id": p.policy_id,
                    "invariants": list(p.invariants),
                    "severity": p.severity,
                    "description": p.description,
                }
                for p in sorted(self.safety_policies, key=lambda p: p.policy_id)
            ],
        }

    def to_dict(self) -> Dict[str, object]:
        payload = self._policy_payload()
        payload.update(
            {
                "gid": self.gid,
                "run_id": self.run_id,
                "meta": dict(self.meta),
                "policy_set_hash": self.policy_set_hash,
            }
        )
        return payload


def governance_config_from_mapping(data: Mapping[str, object]) -> GovernanceConfigV1:
    codex_action_mode = str(data.get("codex_action_mode", "OFF"))
    governance_mode = data.get("governance_mode")

    def _topology(entry: Mapping[str, object]) -> TopologyPolicyV1:
        if not isinstance(entry, Mapping):
            raise ValueError("topology_policies entries must be objects")
        return TopologyPolicyV1(
            policy_id=str(entry.get("policy_id", "")),
            max_nodes=entry.get("max_nodes"),
            max_edges=entry.get("max_edges"),
            allowed_ops=tuple(entry.get("allowed_ops", ALLOWED_TOPOLOGY_OPS)),
            description=str(entry.get("description", "")),
        )

    def _budget(entry: Mapping[str, object]) -> BudgetPolicyV1:
        if not isinstance(entry, Mapping):
            raise ValueError("budget_policies entries must be objects")
        return BudgetPolicyV1(
            policy_id=str(entry.get("policy_id", "")),
            max_actions_per_window=entry.get("max_actions_per_window"),
            max_proposals_per_window=entry.get("max_proposals_per_window"),
            max_topology_changes=entry.get("max_topology_changes"),
            notes=str(entry.get("notes", "")),
        )

    def _safety(entry: Mapping[str, object]) -> SafetyPolicyV1:
        if not isinstance(entry, Mapping):
            raise ValueError("safety_policies entries must be objects")
        invariants_raw = entry.get("invariants", ())
        if not isinstance(invariants_raw, Sequence) or isinstance(invariants_raw, (str, bytes)):
            raise ValueError("safety invariants must be a list of strings")
        return SafetyPolicyV1(
            policy_id=str(entry.get("policy_id", "")),
            invariants=tuple(str(inv) for inv in invariants_raw),
            severity=str(entry.get("severity", "HARD")),
            description=str(entry.get("description", "")),
        )

    def _load_policy_entries(key: str, loader):
        raw = data.get(key, ())
        if raw is None:
            return ()
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            raise ValueError(f"{key} must be a list")
        return tuple(loader(entry) for entry in raw)

    return GovernanceConfigV1(
        governance_mode=governance_mode,
        codex_action_mode=codex_action_mode,
        topology_policies=_load_policy_entries("topology_policies", _topology),
        budget_policies=_load_policy_entries("budget_policies", _budget),
        safety_policies=_load_policy_entries("safety_policies", _safety),
        gid=data.get("gid"),
        run_id=data.get("run_id"),
        meta=dict(data.get("meta", {})),
    )
