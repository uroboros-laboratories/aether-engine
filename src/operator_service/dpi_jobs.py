"""Shared Quantum DPI job schema and validation helpers.

These definitions centralize required parameters and lightweight validation
so both the operator service and CLI can agree on job inputs before deeper
ingestion/simulation plumbing is wired. Validation is intentionally minimal
to remain offline- and dependency-friendly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from operator_service.dpi_types import DpiJobKind


@dataclass
class DpiJobSchema:
    """Declarative shape for a DPI job kind."""

    required: List[str] = field(default_factory=list)
    optional: Dict[str, str] = field(default_factory=dict)
    defaults: Dict[str, object] = field(default_factory=dict)

    def describe(self) -> Dict[str, object]:
        """Return a serializable schema description for config exposure."""

        return {
            "required": list(self.required),
            "optional": dict(self.optional),
            "defaults": dict(self.defaults),
        }


JOB_SCHEMAS: Dict[DpiJobKind, DpiJobSchema] = {
    DpiJobKind.INGESTION: DpiJobSchema(
        required=[],
        optional={
            "eta": "float",
            "phase_bins": "int",
            "output": "path",
            "input": "path",
            "qubits": "int",
            "max_prob_l1": "float",
            "max_amp_l2": "float",
            "auto_tune": "bool",
            "pfna_output": "path",
            "pfna_tick": "int",
            "run_id": "string",
            "gid": "string",
        },
        defaults={
            "phase_bins": 64,
            "eta": 1_000_000,
            "qubits": 2,
            "max_prob_l1": 0.05,
            "max_amp_l2": 0.10,
            "auto_tune": True,
            "pfna_tick": 0,
        },
    ),
    DpiJobKind.SIMULATION: DpiJobSchema(
        required=["circuit"],
        optional={
            "qubits": "int",
            "layers": "int",
            "run_engine": "bool",
            "scenario_id": "string",
            "output": "path",
            "pfna_output": "path",
            "pfna_tick": "int",
            "auto_tune": "bool",
        },
        defaults={
            "circuit": "bell",
            "auto_tune": True,
            "pfna_tick": 0,
            "run_engine": False,
            "qubits": 2,
            "layers": 1,
        },
    ),
    DpiJobKind.EXPERIMENT: DpiJobSchema(
        required=["name"],
        optional={
            "qubits": "int",
            "ticks": "int",
            "episodes": "int",
            "scenario_id": "string",
            "output": "path",
            "pfna_output": "path",
            "pfna_tick": "int",
            "auto_tune": "bool",
        },
        defaults={
            "name": "spin_chain",
            "auto_tune": True,
            "pfna_tick": 0,
            "qubits": 4,
            "ticks": 4,
            "episodes": 1,
        },
    ),
}


def validate_job_params(kind: DpiJobKind, params: Optional[Dict[str, object]]) -> List[str]:
    """Validate that required fields are present and non-empty.

    Returns a list of error strings; an empty list means validation passed.
    """

    params = params or {}
    errors: List[str] = []
    schema = JOB_SCHEMAS.get(kind)
    if schema is None:
        return [f"unknown job kind: {kind}"]

    for field in schema.required:
        value = params.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"missing required field '{field}' for kind {kind.value}")

    if kind is DpiJobKind.INGESTION:
        numeric_fields = [
            "eta",
            "phase_bins",
            "qubits",
            "max_prob_l1",
            "max_amp_l2",
        ]
        for name in numeric_fields:
            if name not in params:
                continue
            value = params.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"{name} must be numeric")
                continue
            if value < 0:
                errors.append(f"{name} must be non-negative")
    return errors


def apply_job_defaults(kind: DpiJobKind, params: Optional[Dict[str, object]]) -> Dict[str, object]:
    """Return params merged with schema defaults (without mutating input)."""

    base = dict(params or {})
    schema = JOB_SCHEMAS.get(kind)
    if schema:
        auto_tune = False
        if kind is DpiJobKind.INGESTION:
            auto_tune = bool(base.get("auto_tune", schema.defaults.get("auto_tune", False)))
        for key, value in schema.defaults.items():
            if (
                kind is DpiJobKind.INGESTION
                and auto_tune
                and key in {"eta", "phase_bins"}
                and (key not in base or base.get(key) is None)
            ):
                # Leave eta/phase_bins empty so the operator ingestion path can
                # auto-tune them using the supplied payload.
                continue
            if key not in base or base[key] is None:
                base[key] = value
    return base


def summarize_missing_fields(kind: DpiJobKind, missing: Iterable[str]) -> str:
    required = list(JOB_SCHEMAS.get(kind, DpiJobSchema()).required)
    hint = f"required fields for {kind.value}: {', '.join(required) or 'none'}"
    missing_list = ", ".join(missing)
    return f"Missing {missing_list}. {hint}."
