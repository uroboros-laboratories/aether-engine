"""Run lifecycle management for the Operator Service."""
from __future__ import annotations

import threading
import json
import zipfile
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Optional
from uuid import uuid4

from config import EngineRuntime
from gate import SessionConfigV1, SessionRunResult, run_session
from ops import StructuredLogEntryV1, StructuredLogger


@dataclass
class RunStatus:
    """Lightweight run lifecycle status for Operator Service APIs."""

    run_id: str
    scenario_id: str
    state: str = "pending"
    stop_requested: bool = False
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    ticks_total: Optional[int] = None
    ticks_completed: Optional[int] = None
    fault_reason: Optional[str] = None


@dataclass
class RunHandle:
    """Handle to a running or completed session."""

    scenario_id: str
    session_config: SessionConfigV1
    status: RunStatus
    thread: Optional[threading.Thread] = None
    result: Optional[SessionRunResult] = None
    error: Optional[BaseException] = None
    logger: Optional[StructuredLogger] = None


@dataclass(frozen=True)
class HistoryEntry:
    """Persisted summary for a completed or faulted run."""

    run_id: str
    scenario_id: str
    started_at: Optional[str]
    ended_at: Optional[str]
    result: str
    ticks_total: Optional[int]
    summary_metrics: Optional[Mapping[str, object]] = None
    governance: Optional[Mapping[str, object]] = None
    pillars: tuple[str, ...] = ()
    status: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "run_id": self.run_id,
            "scenario_id": self.scenario_id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "result": self.result,
            "ticks_total": self.ticks_total,
            "pillars": list(self.pillars),
            "status": dict(self.status),
        }
        if self.summary_metrics is not None:
            payload["summary_metrics"] = dict(self.summary_metrics)
        if self.governance is not None:
            payload["governance"] = dict(self.governance)
        return payload

    @classmethod
    def from_dict(cls, raw: Mapping[str, object]) -> "HistoryEntry":
        return cls(
            run_id=str(raw.get("run_id", "")),
            scenario_id=str(raw.get("scenario_id", "")),
            started_at=raw.get("started_at"),
            ended_at=raw.get("ended_at"),
            result=str(raw.get("result", "")),
            ticks_total=raw.get("ticks_total"),
            summary_metrics=raw.get("summary_metrics"),
            governance=raw.get("governance"),
            pillars=tuple(raw.get("pillars", ()) or ()),
            status=raw.get("status", {}),
        )


class HistoryStore:
    """JSONL-backed persistence for run history entries."""

    def __init__(self, path: Path, runtime: EngineRuntime):
        self.path = path
        self.runtime = runtime
        self.export_root = self.path.parent / "exports"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("")

    def record_run(self, handle: RunHandle) -> HistoryEntry:
        entry = self._build_entry(handle)
        with self.path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry.to_dict(), sort_keys=True))
            fp.write("\n")
        try:
            self._write_export_bundle(handle, entry)
        except Exception:
            # Best-effort only: exporting should not block history recording.
            pass
        return entry

    def load_entries(self) -> list[HistoryEntry]:
        if not self.path.exists():
            return []
        entries: list[HistoryEntry] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, Mapping):
                entries.append(HistoryEntry.from_dict(payload))
        return entries

    def get_entry(self, run_id: str) -> HistoryEntry:
        for entry in self.load_entries():
            if entry.run_id == run_id:
                return entry
        raise KeyError(f"unknown run_id: {run_id}")

    def ensure_export(self, run_id: str, handle: RunHandle | None = None) -> Path:
        """Return a path to an export zip for the run, generating it if needed."""

        bundle = self.export_root / f"{run_id}.zip"
        if bundle.exists():
            return bundle

        entry = None
        try:
            entry = self.get_entry(run_id)
        except KeyError:
            entry = None

        if handle is None and entry is None:
            raise KeyError(f"unknown run_id: {run_id}")

        if handle is not None:
            entry = entry or self._build_entry(handle)
            self._write_export_bundle(handle, entry)
        elif entry is not None:
            self._write_export_from_entry(entry)

        if not bundle.exists():
            raise FileNotFoundError(bundle)

        return bundle

    def _build_entry(self, handle: RunHandle) -> HistoryEntry:
        scenario = None
        try:
            scenario = self.runtime.load_registry().get(handle.status.scenario_id)
        except Exception:
            scenario = None

        governance = dict(handle.session_config.governance.to_dict())
        governance.pop("policy_set_hash", None)

        summary_metrics = None
        if handle.result and handle.result.metrics:
            summary_metrics = handle.result.metrics.to_dict()

        return HistoryEntry(
            run_id=handle.status.run_id,
            scenario_id=handle.status.scenario_id,
            started_at=_isoformat(handle.status.started_at),
            ended_at=_isoformat(handle.status.ended_at),
            result=_result_label(handle.status),
            ticks_total=handle.status.ticks_total,
            summary_metrics=summary_metrics,
            governance=governance,
            pillars=tuple(getattr(scenario, "pillars", ())),
            status=_serialize_status(handle.status),
        )

    def _write_export_bundle(self, handle: RunHandle, entry: HistoryEntry) -> None:
        payload = _build_export_payload(handle, entry, self.runtime)
        bundle_dir = self.export_root
        bundle_dir.mkdir(parents=True, exist_ok=True)
        zip_path = bundle_dir / f"{entry.run_id}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("export.json", json.dumps(payload, indent=2, sort_keys=True))

    def _write_export_from_entry(self, entry: HistoryEntry) -> None:
        bundle_dir = self.export_root
        bundle_dir.mkdir(parents=True, exist_ok=True)
        zip_path = bundle_dir / f"{entry.run_id}.zip"
        payload = {
            "run": dict(entry.status),
            "history_entry": entry.to_dict(),
            "pillars": list(entry.pillars),
            "metrics": entry.summary_metrics,
            "governance": entry.governance,
            "logs": [],
        }
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("export.json", json.dumps(payload, indent=2, sort_keys=True))


class RunRegistry:
    """Track the current run and completed runs."""

    def __init__(self, runtime: EngineRuntime, history_store: HistoryStore | None = None):
        self.runtime = runtime
        self.history_store = history_store
        self._lock = threading.Lock()
        self.current: Optional[RunHandle] = None
        self.history: dict[str, RunHandle] = {}

    # Public API -----------------------------------------------------
    def start_run(
        self, scenario_id: str, overrides: Optional[Mapping[str, object]] = None
    ) -> RunHandle:
        """Start a new run for the given scenario and track its lifecycle."""

        with self._lock:
            if self.current and self.current.status.state in {"pending", "running"}:
                raise RuntimeError("a run is already in progress")

            run_id = None
            if overrides:
                run_id = overrides.get("run_id")  # type: ignore[arg-type]
            if not run_id:
                run_id = f"{scenario_id}-{uuid4().hex[:8]}"

            merged_overrides = dict(overrides or {})
            merged_overrides["run_id"] = run_id
            session_config = self.runtime.build_session_config(
                scenario_id, overrides=merged_overrides
            )

            logger = StructuredLogger(session_config.logging_config)

            status = RunStatus(
                run_id=run_id,
                scenario_id=scenario_id,
                ticks_total=session_config.total_ticks,
                ticks_completed=0,
            )

            handle = RunHandle(
                scenario_id=scenario_id,
                session_config=session_config,
                status=status,
                logger=logger,
            )
            worker = threading.Thread(
                target=self._run_session, args=(handle,), daemon=True
            )
            handle.thread = worker
            self.current = handle
            self.history[run_id] = handle

        worker.start()
        return handle

    def get_status(self, run_id: str) -> RunStatus:
        """Return a copy of the current status for the given run."""

        with self._lock:
            handle = self.history.get(run_id)
            if handle is None:
                raise KeyError(f"unknown run_id: {run_id}")
            return replace(handle.status)

    def request_stop(self, run_id: str) -> RunStatus:
        """Record a best-effort stop request for a running session."""

        with self._lock:
            handle = self.history.get(run_id)
            if handle is None:
                raise KeyError(f"unknown run_id: {run_id}")

            handle.status.stop_requested = True
            return replace(handle.status)

    def get_logs(
        self,
        run_id: str,
        *,
        cursor: int = 0,
        event_type: Optional[str] = None,
        level: Optional[str] = None,
    ) -> tuple[list[dict[str, object]], int]:
        """Return structured logs for a run starting from a cursor."""

        if cursor < 0:
            raise ValueError("cursor must be non-negative")

        with self._lock:
            handle = self.history.get(run_id)
            if handle is None:
                raise KeyError(f"unknown run_id: {run_id}")
            entries = list(_resolve_logs(handle))

        sliced = entries[cursor:]
        filtered: list[dict[str, object]] = []
        for entry in sliced:
            if event_type and entry.event != event_type:
                continue
            if level is not None:
                payload_level = None
                if isinstance(entry.payload, Mapping):
                    payload_level = entry.payload.get("level")
                if payload_level != level:
                    continue
            filtered.append(entry.to_dict())

        return filtered, len(entries)

    def get_pillars(self, run_id: str) -> list[dict[str, object]]:
        """Return PillarStatus-style snapshots for a run."""

        entry: HistoryEntry | None = None
        with self._lock:
            handle = self.history.get(run_id)

        if handle is None:
            if self.history_store:
                try:
                    entry = self.history_store.get_entry(run_id)
                except KeyError:
                    pass
            if entry is None:
                raise KeyError(f"unknown run_id: {run_id}")

        metrics: Mapping[str, object] | None = None
        state = "unknown"
        scenario_id = run_id
        pillars: tuple[str, ...] = ()

        if handle:
            state = handle.status.state
            scenario_id = handle.status.scenario_id
            metrics = _metrics_from_handle(handle)
            pillars = _pillars_for_scenario(self.runtime, scenario_id)
        if entry:
            state = entry.status.get("state", state)
            scenario_id = entry.scenario_id or scenario_id
            pillars = pillars or tuple(entry.pillars)
            metrics = metrics or entry.summary_metrics
            if not pillars:
                pillars = _pillars_for_scenario(self.runtime, scenario_id, fallback=entry.pillars)

        if not pillars:
            pillars = _pillars_for_scenario(self.runtime, scenario_id)

        return _build_pillar_statuses(pillars, metrics, state)

    # Internal helpers ------------------------------------------------
    def _run_session(self, handle: RunHandle) -> None:
        self._mark_running(handle)
        try:
            result = run_session(handle.session_config, logger=handle.logger)
        except Exception as exc:  # pragma: no cover - defensive path
            self._mark_fault(handle, exc)
        else:
            self._mark_completed(handle, result)

    def _mark_running(self, handle: RunHandle) -> None:
        with self._lock:
            handle.status.state = "running"
            handle.status.started_at = datetime.now(timezone.utc)
            handle.status.ticks_completed = 0

    def _mark_completed(self, handle: RunHandle, result: SessionRunResult) -> None:
        with self._lock:
            handle.result = result
            handle.status.state = "completed"
            handle.status.ended_at = datetime.now(timezone.utc)
            handle.status.ticks_completed = handle.session_config.total_ticks
            if self.current is handle:
                self.current = None
            if self.history_store:
                self.history_store.record_run(handle)

    def _mark_fault(self, handle: RunHandle, exc: BaseException) -> None:
        with self._lock:
            handle.error = exc
            handle.status.state = "fault"
            handle.status.ended_at = datetime.now(timezone.utc)
            handle.status.fault_reason = str(exc)
            if self.current is handle:
                self.current = None
            if self.history_store:
                self.history_store.record_run(handle)


def _build_export_payload(
    handle: RunHandle, entry: HistoryEntry, runtime: EngineRuntime
) -> dict[str, object]:
    metrics = _metrics_from_handle(handle) or entry.summary_metrics
    governance = dict(handle.session_config.governance.to_dict())
    governance.pop("policy_set_hash", None)

    scenario_pillars: tuple[str, ...] = ()
    try:
        scenario = runtime.load_registry().get(handle.status.scenario_id)
        scenario_pillars = tuple(getattr(scenario, "pillars", ()))
    except Exception:
        scenario_pillars = tuple(entry.pillars)

    logs = [_entry.to_dict() for _entry in _resolve_logs(handle)]

    return {
        "run": _serialize_status(handle.status),
        "history_entry": entry.to_dict(),
        "pillars": list(scenario_pillars),
        "metrics": metrics,
        "governance": governance,
        "logs": logs,
    }


def _serialize_status(status: RunStatus) -> dict[str, object]:
    return {
        "run_id": status.run_id,
        "scenario_id": status.scenario_id,
        "state": status.state,
        "stop_requested": status.stop_requested,
        "started_at": _isoformat(status.started_at),
        "ended_at": _isoformat(status.ended_at),
        "ticks_total": status.ticks_total,
        "ticks_completed": status.ticks_completed,
        "fault_reason": status.fault_reason,
    }


def _isoformat(dt: Optional[object]) -> Optional[str]:
    return dt.isoformat() if hasattr(dt, "isoformat") else None


def _result_label(status: RunStatus) -> str:
    if status.state == "completed":
        return "completed"
    if status.state == "fault":
        return "fault"
    if status.stop_requested and status.state != "completed":
        return "cancelled"
    return status.state


def _resolve_logs(handle: RunHandle) -> list[StructuredLogEntryV1]:
    if handle.logger is not None:
        return handle.logger.entries
    if handle.result is not None:
        return list(handle.result.logs)
    return []


def _metrics_from_handle(handle: RunHandle) -> Mapping[str, object] | None:
    if handle.result and handle.result.metrics:
        return handle.result.metrics.to_dict()

    return {
        "total_ticks": handle.session_config.total_ticks,
        "nap_total": handle.status.ticks_completed or 0,
        "window_count": len(handle.session_config.window_specs),
    }


def _pillars_for_scenario(
    runtime: EngineRuntime,
    scenario_id: str,
    *,
    fallback: tuple[str, ...] | list[str] | None = None,
) -> tuple[str, ...]:
    try:
        scenario = runtime.load_registry().get(scenario_id)
        pillars = tuple(getattr(scenario, "pillars", ()))
    except Exception:  # pragma: no cover - defensive lookup
        pillars = ()

    if not pillars and fallback:
        pillars = tuple(fallback)

    if not pillars:
        return ("AETHER", "PRESS", "UMX", "LOOM", "CODEX")

    return tuple(pillars)


def _build_pillar_statuses(
    pillars: tuple[str, ...] | list[str],
    metrics: Mapping[str, object] | None,
    state: str,
) -> list[dict[str, object]]:
    data: Mapping[str, object] = metrics or {}

    def _metric_val(key: str, default: int = 0) -> int:
        value = data.get(key, default)
        try:
            return int(value)
        except Exception:
            return default

    codex_counts = data.get("codex_motif_counts", {})
    codex_total = 0
    if isinstance(codex_counts, Mapping):
        codex_total = sum(int(val) for val in codex_counts.values())

    def _status_label(run_state: str) -> str:
        if run_state == "fault":
            return "FAULT"
        if run_state in {"running", "pending"}:
            return "ACTIVE"
        return "IDLE"

    statuses: list[dict[str, object]] = []
    for pillar in pillars:
        pid = str(pillar)
        pid_upper = pid.upper()
        name = {
            "AETHER": "Aether",
            "GATE": "Gate",
            "PRESS": "Press",
            "NAP": "NAP",
            "UMX": "UMX",
            "LOOM": "Loom",
            "CODEX": "Codex",
        }.get(pid_upper, pid.upper())

        headline_label = "Activity"
        headline_value = _metric_val("total_ticks")
        secondary: list[dict[str, object]] = []

        if pid_upper in {"AETHER", "GATE"}:
            headline_label = "Total ticks"
            headline_value = _metric_val("total_ticks") or _metric_val("nap_total")
            secondary.append({
                "label": "Tick progress",
                "value": _metric_val("nap_total"),
            })
        elif pid_upper in {"PRESS"}:
            headline_label = "APX manifests"
            headline_value = _metric_val("apx_manifests")
            wc = _metric_val("window_count")
            if wc:
                secondary.append({"label": "Windows", "value": wc})
        elif pid_upper in {"NAP", "LOOM"}:
            headline_label = "NAP envelopes"
            headline_value = _metric_val("nap_total")
            ingress = _metric_val("nap_ingress")
            data_count = _metric_val("nap_data")
            egress = _metric_val("nap_egress")
            if ingress:
                secondary.append({"label": "Ingress", "value": ingress})
            if data_count:
                secondary.append({"label": "Data", "value": data_count})
            if egress:
                secondary.append({"label": "Egress", "value": egress})
        elif pid_upper in {"UMX"}:
            headline_label = "ULedger entries"
            headline_value = _metric_val("uledger_entries")
            last_hash = data.get("uledger_last_hash")
            if last_hash:
                secondary.append({"label": "Last hash", "value": last_hash})
        elif pid_upper == "CODEX":
            headline_label = "Codex motifs"
            headline_value = codex_total
            if isinstance(codex_counts, Mapping) and codex_counts:
                for motif, count in codex_counts.items():
                    secondary.append({"label": str(motif), "value": int(count)})

        payload = {
            "pillar_id": pid,
            "name": name,
            "status": _status_label(state),
            "headline_metric_label": headline_label,
            "headline_metric_value": headline_value,
        }
        if secondary:
            payload["secondary_metrics"] = secondary
        statuses.append(payload)

    return statuses
