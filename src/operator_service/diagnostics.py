"""Diagnostics runner and persistence for the Operator Service."""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Optional
from uuid import uuid4

from config import EngineRuntime
from operator_service.run_registry import RunRegistry


@dataclass(frozen=True)
class DiagnosticProfile:
    """A named diagnostics profile discoverable by the UI."""

    id: str
    label: str
    description: str


@dataclass
class DiagnosticCheck:
    """Result for a single diagnostics check."""

    id: str
    name: str
    description: str | None = None
    state: str = "PENDING"
    message: str | None = None


@dataclass
class DiagnosticStatus:
    """Lifecycle summary for a diagnostics run."""

    diagnostic_id: str
    profile_id: str
    state: str = "PENDING"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    summary: Optional[str] = None
    checks_passed: Optional[int] = None
    checks_failed: Optional[int] = None


@dataclass
class DiagnosticResult:
    """Detailed outcome of a diagnostics run."""

    status: DiagnosticStatus
    checks: list[DiagnosticCheck] = field(default_factory=list)
    related_run_ids: list[str] = field(default_factory=list)


@dataclass
class DiagnosticHandle:
    """Track a running or completed diagnostics execution."""

    status: DiagnosticStatus
    result: DiagnosticResult
    thread: Optional[threading.Thread] = None


class DiagnosticsStore:
    """JSONL-backed persistence for diagnostics results."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def record(self, result: DiagnosticResult) -> None:
        with self.path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(_serialize_result(result), sort_keys=True))
            fp.write("\n")

    def load(self) -> list[DiagnosticResult]:
        entries: list[DiagnosticResult] = []
        if not self.path.exists():
            return entries
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, Mapping):
                entries.append(_deserialize_result(payload))
        return entries


class DiagnosticsManager:
    """Manage diagnostics profiles and executions."""

    def __init__(
        self,
        runtime: EngineRuntime,
        run_registry: RunRegistry,
        store: DiagnosticsStore,
    ):
        self.runtime = runtime
        self.run_registry = run_registry
        self.store = store
        self._lock = threading.Lock()
        self.current: Optional[DiagnosticHandle] = None
        self.history: dict[str, DiagnosticHandle] = {}
        self.profiles: dict[str, DiagnosticProfile] = {
            "SMOKE": DiagnosticProfile(
                id="SMOKE",
                label="Smoke",
                description="Run a tiny Gate scenario end-to-end to validate wiring.",
            )
        }

    # Public API -------------------------------------------------
    def list_profiles(self) -> list[DiagnosticProfile]:
        return list(self.profiles.values())

    def list_results(self) -> list[DiagnosticResult]:
        """Return completed and in-progress diagnostics ordered by creation time."""

        results: dict[str, DiagnosticResult] = {}

        for handle in self.history.values():
            results[handle.status.diagnostic_id] = handle.result

        for entry in self.store.load():
            results.setdefault(entry.status.diagnostic_id, entry)

        ordered = sorted(
            results.values(),
            key=lambda res: res.status.created_at
            or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        return ordered

    def get_result(self, diagnostic_id: str) -> DiagnosticResult:
        if diagnostic_id in self.history:
            return self.history[diagnostic_id].result
        for entry in self.store.load():
            if entry.status.diagnostic_id == diagnostic_id:
                return entry
        raise KeyError(f"unknown diagnostic_id: {diagnostic_id}")

    def start_diagnostics(self, profile_id: str) -> DiagnosticStatus:
        if profile_id not in self.profiles:
            raise KeyError(f"unknown profile: {profile_id}")

        with self._lock:
            if self.current and self.current.status.state in {"PENDING", "RUNNING"}:
                raise RuntimeError("diagnostics already in progress")
            if self.run_registry.current and self.run_registry.current.status.state in {
                "pending",
                "running",
            }:
                raise RuntimeError("a Gate run is in progress")

            diagnostic_id = f"diag-{uuid4().hex[:8]}"
            status = DiagnosticStatus(
                diagnostic_id=diagnostic_id,
                profile_id=profile_id,
            )
            result = DiagnosticResult(status=status, checks=[])
            handle = DiagnosticHandle(status=status, result=result)
            self.current = handle
            self.history[diagnostic_id] = handle

            thread = threading.Thread(
                target=self._run_diagnostics,
                args=(handle,),
                daemon=True,
            )
            handle.thread = thread
            thread.start()
            return status

    # Internal ---------------------------------------------------
    def _run_diagnostics(self, handle: DiagnosticHandle) -> None:
        status = handle.status
        status.state = "RUNNING"
        status.started_at = datetime.now(timezone.utc)

        checks: list[DiagnosticCheck]
        if handle.status.profile_id == "SMOKE":
            checks = [
                DiagnosticCheck(
                    id="engine_smoke",
                    name="Run baseline scenario",
                    description="Execute a small scenario to validate engine wiring.",
                )
            ]
            self._execute_smoke(handle, checks[0])
        else:  # pragma: no cover - defensive future-proofing
            checks = []
            status.state = "FAILED"
            status.summary = "Unsupported profile"

        handle.result.checks = checks
        self._finalize_status(handle)

    def _execute_smoke(self, handle: DiagnosticHandle, check: DiagnosticCheck) -> None:
        try:
            scenario_id = self._select_smoke_scenario()
            run_handle = self.run_registry.start_run(
                scenario_id,
                overrides={"run_id": f"{handle.status.diagnostic_id}-run"},
            )
            handle.result.related_run_ids.append(run_handle.status.run_id)
            if run_handle.thread:
                run_handle.thread.join()
            if run_handle.status.state == "completed":
                check.state = "PASSED"
                check.message = "Scenario completed successfully"
            else:
                check.state = "FAILED"
                check.message = run_handle.status.fault_reason or "Scenario failed"
        except Exception as exc:  # pragma: no cover - defensive
            check.state = "FAILED"
            check.message = str(exc)

    def _finalize_status(self, handle: DiagnosticHandle) -> None:
        passed = len([c for c in handle.result.checks if c.state == "PASSED"])
        failed = len([c for c in handle.result.checks if c.state == "FAILED"])
        handle.status.checks_passed = passed
        handle.status.checks_failed = failed
        handle.status.finished_at = datetime.now(timezone.utc)
        handle.status.state = "PASSED" if failed == 0 else "FAILED"
        handle.status.summary = "All checks passed" if failed == 0 else "Diagnostics failed"

        self.store.record(handle.result)
        with self._lock:
            if self.current is handle:
                self.current = None

    def _select_smoke_scenario(self) -> str:
        registry = self.runtime.load_registry()
        try:
            return registry.scenarios[0].scenario_id
        except Exception:  # pragma: no cover - defensive
            return "gf01"


def _serialize_result(result: DiagnosticResult) -> Mapping[str, object]:
    return {
        "status": _serialize_status(result.status),
        "checks": [
            {
                "id": check.id,
                "name": check.name,
                "description": check.description,
                "state": check.state,
                "message": check.message,
            }
            for check in result.checks
        ],
        "related_run_ids": list(result.related_run_ids),
    }


def _serialize_status(status: DiagnosticStatus) -> Mapping[str, object]:
    return {
        "diagnostic_id": status.diagnostic_id,
        "profile_id": status.profile_id,
        "state": status.state,
        "created_at": _isoformat(status.created_at),
        "started_at": _isoformat(status.started_at),
        "finished_at": _isoformat(status.finished_at),
        "summary": status.summary,
        "checks_passed": status.checks_passed,
        "checks_failed": status.checks_failed,
    }


def _deserialize_result(raw: Mapping[str, object]) -> DiagnosticResult:
    status_raw = raw.get("status", {}) if isinstance(raw.get("status"), Mapping) else {}
    status = DiagnosticStatus(
        diagnostic_id=str(status_raw.get("diagnostic_id", "")),
        profile_id=str(status_raw.get("profile_id", "")),
        state=str(status_raw.get("state", "PENDING")),
        created_at=_parse_dt(status_raw.get("created_at")),
        started_at=_parse_dt(status_raw.get("started_at")),
        finished_at=_parse_dt(status_raw.get("finished_at")),
        summary=status_raw.get("summary"),
        checks_passed=status_raw.get("checks_passed"),
        checks_failed=status_raw.get("checks_failed"),
    )

    checks_raw: Iterable[Mapping[str, object]] = []
    if isinstance(raw.get("checks"), list):
        checks_raw = raw["checks"]  # type: ignore[assignment]

    checks = [
        DiagnosticCheck(
            id=str(entry.get("id", "")),
            name=str(entry.get("name", "")),
            description=entry.get("description"),
            state=str(entry.get("state", "PENDING")),
            message=entry.get("message"),
        )
        for entry in checks_raw
        if isinstance(entry, Mapping)
    ]

    related_run_ids: list[str] = []
    if isinstance(raw.get("related_run_ids"), list):
        related_run_ids = [str(rid) for rid in raw["related_run_ids"]]

    return DiagnosticResult(status=status, checks=checks, related_run_ids=related_run_ids)


def _isoformat(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


def _parse_dt(value: object) -> Optional[datetime]:
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    if isinstance(value, datetime):
        return value
    return None
