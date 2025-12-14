"""Shared run summary structures and run-sheet append helpers.

This module supports Phase 9 EPIC 3 by providing a single `RunSummary`
representation that hero commands and sweep runners can populate. The
append helpers keep both CSV and JSONL run sheets in sync so that follow-
on analysis tools have a consistent source of truth.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Optional


@dataclass
class RunSummary:
    """Minimal run summary schema used by heroes and sweeps.

    Fields are intentionally lightweight so the structure can be filled
    by DPI-only runs, base-engine runs, or full-stack executions. Extra
    metrics can be added incrementally without breaking existing callers
    because JSONL encoding preserves new keys and CSV preserves header
    ordering with defaults.
    """

    run_id: str
    timestamp: str
    scenario: str
    n_qubits: Optional[int] = None
    ticks: Optional[int] = None
    dpi_mode: Optional[str] = None
    loom_mode: Optional[str] = None
    codex_mode: Optional[str] = None
    runtime_total_ms: Optional[float] = None
    runtime_engine_ms: Optional[float] = None
    status: str = "UNKNOWN"
    loom_p_blocks: Optional[int] = None
    loom_i_blocks: Optional[int] = None
    loom_bytes: Optional[int] = None
    peak_mem_mb: Optional[float] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    eta: Optional[float] = None
    phase_bins: Optional[int] = None
    fidelity_prob_l1: Optional[float] = None
    fidelity_amp_l2: Optional[float] = None
    notes: str = ""
    extras: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_defaults(
        cls,
        *,
        run_id: str,
        scenario: str,
        status: str,
        timestamp: Optional[datetime] = None,
        extras: Optional[Mapping[str, object]] = None,
        **kwargs: object,
    ) -> "RunSummary":
        """Build a `RunSummary`, injecting defaults and optional extras."""

        ts = (timestamp or datetime.now(timezone.utc)).isoformat()
        summary = cls(
            run_id=run_id,
            scenario=scenario,
            status=status,
            timestamp=ts,
            **{k: v for k, v in kwargs.items() if k in cls._field_names()},
        )
        if extras:
            summary.extras = dict(extras)
        return summary

    def to_serializable(self) -> dict[str, object]:
        """Return a dict suitable for JSONL serialization."""

        payload = asdict(self)
        if not self.extras:
            payload.pop("extras", None)
        return payload

    def csv_header(self) -> list[str]:
        """Return a stable CSV header ordering."""

        base_fields = [
            "run_id",
            "timestamp",
            "scenario",
            "n_qubits",
            "ticks",
            "dpi_mode",
            "loom_mode",
            "codex_mode",
            "runtime_total_ms",
            "runtime_engine_ms",
            "status",
            "loom_p_blocks",
            "loom_i_blocks",
            "loom_bytes",
            "peak_mem_mb",
            "error_code",
            "error_message",
            "eta",
            "phase_bins",
            "fidelity_prob_l1",
            "fidelity_amp_l2",
            "notes",
        ]
        # Extras are flattened into a JSON string to keep CSV rows single-line.
        return base_fields + ["extras"]

    def csv_row(self) -> list[object]:
        """Return a CSV row matching `csv_header` ordering."""

        extras_blob = json.dumps(self.extras, sort_keys=True) if self.extras else ""
        values = [
            self.run_id,
            self.timestamp,
            self.scenario,
            self.n_qubits,
            self.ticks,
            self.dpi_mode,
            self.loom_mode,
            self.codex_mode,
            self.runtime_total_ms,
            self.runtime_engine_ms,
            self.status,
            self.loom_p_blocks,
            self.loom_i_blocks,
            self.loom_bytes,
            self.peak_mem_mb,
            self.error_code,
            self.error_message,
            self.eta,
            self.phase_bins,
            self.fidelity_prob_l1,
            self.fidelity_amp_l2,
            self.notes,
            extras_blob,
        ]
        return values

    @classmethod
    def _field_names(cls) -> set[str]:
        return set(field.name for field in cls.__dataclass_fields__.values())


def ensure_logs_dir(repo_root: Path | str) -> Path:
    """Ensure the logs directory exists and return its path."""

    path = Path(repo_root).expanduser().resolve() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def append_run_summaries(
    summaries: Iterable[RunSummary],
    *,
    repo_root: Path | str,
    csv_name: str = "quantum_runs.csv",
    jsonl_name: str = "quantum_runs.jsonl",
) -> None:
    """Append run summaries to both CSV and JSONL run sheets."""

    logs_dir = ensure_logs_dir(repo_root)
    summaries = list(summaries)
    if not summaries:
        return

    csv_path = logs_dir / csv_name
    jsonl_path = logs_dir / jsonl_name

    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if write_header:
            writer.writerow(summaries[0].csv_header())
        for summary in summaries:
            writer.writerow(summary.csv_row())

    with jsonl_path.open("a", encoding="utf-8") as handle:
        for summary in summaries:
            handle.write(json.dumps(summary.to_serializable(), sort_keys=True))
            handle.write("\n")
