"""Minimal Operator Service skeleton for Phase 7.

Provides a simple HTTP server with a health endpoint and wiring to
:class:`config.EngineRuntime`. This is intentionally lightweight (standard
library only) so it can run in constrained offline environments.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from config import EngineRuntime
from operator_service.diagnostics import DiagnosticsManager, DiagnosticsStore
from operator_service.run_registry import HistoryStore, RunRegistry, RunStatus


@dataclass
class OperatorServiceConfig:
    """Configuration for the Operator Service server."""

    host: str = "127.0.0.1"
    port: int = 8000
    repo_root: Optional[Path] = None
    scenario_registry_path: Optional[Path] = None
    history_path: Optional[Path] = None
    diagnostics_path: Optional[Path] = None


class _OperatorRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler for the Operator Service.

    Parameters are injected via ``functools.partial`` in ``OperatorService``
    so the handler has access to the runtime and config without global state.
    """

    server_version = "OperatorService/0.1"
    runtime: EngineRuntime
    run_registry: RunRegistry
    service: "OperatorService"
    history_store: HistoryStore
    diagnostics: DiagnosticsManager

    def do_OPTIONS(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler signature
        """Respond to CORS preflight requests."""

        self.send_response(204)
        self._send_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler signature
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._handle_health()
        elif parsed.path == "/state":
            self._handle_state()
        elif parsed.path == "/governance":
            self._handle_governance()
        elif parsed.path == "/scenarios":
            self._handle_scenarios()
        elif parsed.path.startswith("/scenarios/"):
            _, _, scenario_id, *_ = parsed.path.split("/")
            if not scenario_id:
                self._send_json({"error": "missing scenario id"}, status_code=400)
                return
            self._handle_scenario_detail(scenario_id)
        elif parsed.path.startswith("/runs/") and parsed.path.endswith("/pillars"):
            _, _, run_id, *_ = parsed.path.split("/")
            if not run_id:
                self._send_json({"error": "missing run id"}, status_code=400)
                return
            self._handle_run_pillars(run_id)
        elif parsed.path.startswith("/runs/") and parsed.path.endswith("/logs"):
            _, _, run_id, *_ = parsed.path.split("/")
            if not run_id:
                self._send_json({"error": "missing run id"}, status_code=400)
                return
            self._handle_run_logs(run_id, parsed.query)
        elif parsed.path == "/history":
            self._handle_history()
        elif parsed.path.startswith("/history/") and parsed.path.endswith("/export"):
            _, _, run_id, *_ = parsed.path.split("/")
            if not run_id:
                self._send_json({"error": "missing run id"}, status_code=400)
                return
            self._handle_history_export(run_id)
        elif parsed.path.startswith("/history/"):
            _, _, run_id, *_ = parsed.path.split("/")
            if not run_id:
                self._send_json({"error": "missing run id"}, status_code=400)
                return
            self._handle_history_detail(run_id)
        elif parsed.path == "/diagnostics/profiles":
            self._handle_diagnostic_profiles()
        elif parsed.path == "/diagnostics":
            self._handle_diagnostics()
        elif parsed.path.startswith("/diagnostics/"):
            _, _, diagnostic_id, *_ = parsed.path.split("/")
            if not diagnostic_id:
                self._send_json({"error": "missing diagnostic id"}, status_code=400)
                return
            self._handle_diagnostic_detail(diagnostic_id)
        else:
            self._send_json({"error": "not found"}, status_code=404)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler signature
        parsed = urlparse(self.path)
        if parsed.path == "/runs":
            self._handle_start_run()
        elif parsed.path.startswith("/runs/") and parsed.path.endswith("/stop"):
            _, _, run_id, *_ = parsed.path.split("/")
            if not run_id:
                self._send_json({"error": "missing run_id"}, status_code=400)
                return
            self._handle_stop_run(run_id)
        elif parsed.path == "/governance":
            self._handle_update_governance()
        elif parsed.path.startswith("/scenarios/") and parsed.path.endswith("/activate"):
            _, _, scenario_id, *_ = parsed.path.split("/")
            if not scenario_id:
                self._send_json({"error": "missing scenario id"}, status_code=400)
                return
            self._handle_activate_scenario(scenario_id)
        elif parsed.path.startswith("/scenarios/"):
            _, _, scenario_id, *_ = parsed.path.split("/")
            if not scenario_id:
                self._send_json({"error": "missing scenario id"}, status_code=400)
                return
            self._handle_update_scenario(scenario_id)
        elif parsed.path == "/diagnostics":
            self._handle_start_diagnostics()
        else:
            self._send_json({"error": "not found"}, status_code=404)

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - base name
        # Avoid noisy stderr logging; could be routed to structured logging later.
        return

    def _handle_health(self) -> None:
        status = "ok"
        detail = {}
        code = 200

        try:
            registry = self.runtime.load_registry()
            detail = {
                "status": status,
                "registry_path": str(self.runtime.scenario_registry_path),
                "available_scenarios": registry.list_ids(),
            }
        except Exception as exc:  # pragma: no cover - defensive path
            status = "error"
            code = 500
            detail = {"status": status, "detail": str(exc)}

        self._send_json(detail, status_code=code)

    def _handle_state(self) -> None:
        registry = self.runtime.load_registry()
        active_scenario_id = self.service.active_scenario_id
        if active_scenario_id is None:
            active_scenario_id = registry.scenarios[0].scenario_id

        try:
            scenario = registry.get(active_scenario_id)
        except KeyError:
            scenario = None

        current_status = None
        if self.run_registry.current:
            current_status = self._serialize_status(self.run_registry.current.status)

        state = {
            "current_run": current_status,
            "active_scenario": self._serialize_scenario(scenario) if scenario else None,
            "pillars": list(scenario.pillars) if scenario else [],
            "governance": self.runtime.load_governance_base(),
            "diagnostics": self._serialize_diagnostics_state(),
        }
        self._send_json(state)

    def _handle_start_run(self) -> None:
        payload = self._read_json()
        if payload is None:
            return

        scenario_id = payload.get("scenario_id") if isinstance(payload, dict) else None
        overrides = payload.get("overrides") if isinstance(payload, dict) else None
        if not scenario_id:
            self._send_json({"error": "scenario_id is required"}, status_code=400)
            return

        try:
            handle = self.run_registry.start_run(scenario_id, overrides)
        except RuntimeError as exc:
            self._send_json({"error": str(exc)}, status_code=409)
            return
        except Exception as exc:  # pragma: no cover - defensive
            self._send_json({"error": str(exc)}, status_code=400)
            return

        self.service.active_scenario_id = scenario_id
        body = self._serialize_status(handle.status)
        self._send_json(body, status_code=201)

    def _handle_stop_run(self, run_id: str) -> None:
        try:
            status = self.run_registry.request_stop(run_id)
        except KeyError:
            self._send_json({"error": "run not found"}, status_code=404)
            return

        payload = {
            "status": self._serialize_status(status),
            "detail": "stop request recorded; cancellation not yet supported",
        }
        self._send_json(payload, status_code=202)

    def _handle_governance(self) -> None:
        try:
            snapshot = self.runtime.load_governance_base()
        except Exception as exc:  # pragma: no cover - defensive
            self._send_json({"error": str(exc)}, status_code=500)
            return

        self._send_json({"governance": snapshot})

    def _handle_run_logs(self, run_id: str, query: str) -> None:
        params = parse_qs(query)
        cursor_raw = params.get("cursor", ["0"])[0]
        try:
            cursor = int(cursor_raw)
        except ValueError:
            self._send_json({"error": "cursor must be an integer"}, status_code=400)
            return

        event_type = params.get("event_type", [None])[0]
        level = params.get("level", [None])[0]
        try:
            entries, next_cursor = self.run_registry.get_logs(
                run_id, cursor=cursor, event_type=event_type, level=level
            )
        except KeyError:
            self._send_json({"error": "run not found"}, status_code=404)
            return
        except ValueError as exc:
            self._send_json({"error": str(exc)}, status_code=400)
            return

        payload = {"entries": entries, "cursor": next_cursor}
        self._send_json(payload)

    def _handle_run_pillars(self, run_id: str) -> None:
        try:
            pillars = self.run_registry.get_pillars(run_id)
        except KeyError:
            self._send_json({"error": "run not found"}, status_code=404)
            return

        self._send_json({"pillars": pillars})

    def _handle_scenarios(self) -> None:
        registry = self.runtime.load_registry()
        scenarios = [self._serialize_scenario(entry) for entry in registry.scenarios]
        self._send_json({"scenarios": scenarios})

    def _handle_update_governance(self) -> None:
        payload = self._read_json()
        if payload is None:
            return

        try:
            snapshot = self.runtime.update_governance_base(payload)
        except Exception as exc:  # pragma: no cover - validation guard
            self._send_json({"error": str(exc)}, status_code=400)
            return

        self._send_json({"governance": snapshot})

    def _handle_scenario_detail(self, scenario_id: str) -> None:
        try:
            scenario = self.runtime.load_registry().get(scenario_id)
        except KeyError:
            self._send_json({"error": "scenario not found"}, status_code=404)
            return

        run_config, _ = self.runtime.load_run_config(scenario_id)
        payload = self._serialize_scenario_detail(scenario, run_config)
        self._send_json(payload)

    def _handle_history(self) -> None:
        entries = [entry.to_dict() for entry in self.history_store.load_entries()]
        diagnostics = [
            _serialize_diag_summary(result) for result in self.diagnostics.list_results()
        ]
        self._send_json(
            {
                "entries": entries,
                "total": len(entries),
                "diagnostics": diagnostics,
                "diagnostics_total": len(diagnostics),
            }
        )

    def _handle_history_detail(self, run_id: str) -> None:
        try:
            entry = self.history_store.get_entry(run_id)
            payload = {
                "run": entry.status,
                "pillars": list(entry.pillars),
                "governance": entry.governance,
                "metrics": entry.summary_metrics,
            }
            self._send_json(payload)
            return
        except KeyError:
            pass

        handle = self.run_registry.history.get(run_id)
        if handle is None:
            self._send_json({"error": "run not found"}, status_code=404)
            return

        metrics = None
        if handle.result and handle.result.metrics:
            metrics = handle.result.metrics.to_dict()

        scenario = None
        try:
            scenario = self.runtime.load_registry().get(handle.status.scenario_id)
        except Exception:
            scenario = None

        payload = {
            "run": self._serialize_status(handle.status),
            "pillars": list(getattr(scenario, "pillars", ())),
            "governance": dict(handle.session_config.governance.to_dict()),
            "metrics": metrics,
        }
        payload["governance"].pop("policy_set_hash", None)
        self._send_json(payload)

    def _handle_history_export(self, run_id: str) -> None:
        handle = self.run_registry.history.get(run_id)
        try:
            bundle = self.history_store.ensure_export(run_id, handle)
        except KeyError:
            self._send_json({"error": "run not found"}, status_code=404)
            return
        except Exception as exc:  # pragma: no cover - defensive guard
            self._send_json({"error": str(exc)}, status_code=500)
            return

        data = bundle.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header(
            "Content-Disposition", f"attachment; filename=\"{bundle.name}\""
        )
        self.send_header("Content-Length", str(len(data)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def _handle_diagnostic_profiles(self) -> None:
        payload = [
            {
                "id": profile.id,
                "label": profile.label,
                "description": profile.description,
            }
            for profile in self.diagnostics.list_profiles()
        ]
        self._send_json(payload)

    def _handle_start_diagnostics(self) -> None:
        payload = self._read_json()
        if payload is None:
            return

        profile_id = None
        if isinstance(payload, dict):
            profile_id = payload.get("profile_id")

        if not profile_id:
            self._send_json({"error": "profile_id is required"}, status_code=400)
            return

        try:
            status = self.diagnostics.start_diagnostics(str(profile_id))
        except KeyError as exc:
            self._send_json({"error": str(exc)}, status_code=404)
            return
        except RuntimeError as exc:
            self._send_json({"error": str(exc)}, status_code=409)
            return

        self._send_json(_serialize_diag_status(status), status_code=201)

    def _handle_diagnostics(self) -> None:
        results = self.diagnostics.list_results()
        payload = {
            "entries": [_serialize_diag_summary(result) for result in results],
            "total": len(results),
        }
        self._send_json(payload)

    def _handle_diagnostic_detail(self, diagnostic_id: str) -> None:
        try:
            result = self.diagnostics.get_result(diagnostic_id)
        except KeyError:
            self._send_json({"error": "diagnostic not found"}, status_code=404)
            return

        payload = _serialize_diag_result(result)
        self._send_json(payload)

    def _handle_update_scenario(self, scenario_id: str) -> None:
        payload = self._read_json()
        if payload is None:
            return

        try:
            scenario_updates = {
                key: payload[key]
                for key in ("description", "runtime_hint")
                if key in payload
            }
            if scenario_updates:
                self.runtime.update_scenario_metadata(scenario_id, **scenario_updates)

            run_config_updates = {
                key: payload[key]
                for key in ("ticks", "enable_codex", "enable_pfna", "run_id", "gid")
                if key in payload
            }
            run_config = None
            if run_config_updates:
                run_config = self.runtime.update_run_config(scenario_id, run_config_updates)
            else:
                run_config, _ = self.runtime.load_run_config(scenario_id)

            scenario = self.runtime.load_registry().get(scenario_id)
        except KeyError:
            self._send_json({"error": "scenario not found"}, status_code=404)
            return
        except Exception as exc:  # pragma: no cover - defensive validation path
            self._send_json({"error": str(exc)}, status_code=400)
            return

        payload = self._serialize_scenario_detail(scenario, run_config)
        self._send_json(payload)

    def _handle_activate_scenario(self, scenario_id: str) -> None:
        try:
            scenario = self.runtime.load_registry().get(scenario_id)
        except KeyError:
            self._send_json({"error": "scenario not found"}, status_code=404)
            return

        self.service.active_scenario_id = scenario_id
        payload = {
            "active_scenario": self._serialize_scenario(scenario),
            "detail": "active scenario updated",
        }
        self._send_json(payload)

    def _serialize_diagnostics_state(self) -> dict:
        current = None
        if self.diagnostics.current:
            current = _serialize_diag_summary(self.diagnostics.current.result)
        return {"current": current}

    def _send_json(self, payload: object, *, status_code: int = 200) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _read_json(self) -> Optional[dict]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, status_code=400)
            return None
        if not isinstance(data, dict):
            self._send_json({"error": "body must be an object"}, status_code=400)
            return None
        return data

    @staticmethod
    def _serialize_status(status: RunStatus) -> dict:
        def _ts(dt: Optional[object]) -> Optional[str]:
            return dt.isoformat() if hasattr(dt, "isoformat") else None

        return {
            "run_id": status.run_id,
            "scenario_id": status.scenario_id,
            "state": status.state,
            "stop_requested": status.stop_requested,
            "started_at": _ts(status.started_at),
            "ended_at": _ts(status.ended_at),
            "ticks_total": status.ticks_total,
            "ticks_completed": status.ticks_completed,
            "fault_reason": status.fault_reason,
        }

    @staticmethod
    def _serialize_scenario(scenario: Optional[object]) -> Optional[dict]:
        if scenario is None:
            return None
        return {
            "scenario_id": getattr(scenario, "scenario_id", None),
            "description": getattr(scenario, "description", ""),
            "pillars": list(getattr(scenario, "pillars", ())),
            "runtime_hint": getattr(scenario, "runtime_hint", ""),
        }

    @staticmethod
    def _serialize_scenario_detail(scenario: object, run_config: object) -> dict:
        detail = _OperatorRequestHandler._serialize_scenario(scenario) or {}
        detail.update(
            {
                "run_config": {
                    "gid": getattr(run_config, "gid", None),
                    "run_id": getattr(run_config, "run_id", None),
                    "ticks": getattr(run_config, "ticks", None),
                    "enable_codex": getattr(run_config, "enable_codex", None),
                    "enable_pfna": getattr(run_config, "enable_pfna", None),
                    "primary_window_id": getattr(run_config, "primary_window_id", None),
                    "topology_path": getattr(run_config, "topology_path", None),
                    "profile_path": getattr(run_config, "profile_path", None),
                }
            }
        )
        return detail


@dataclass
class OperatorService:
    """Build and run the Operator Service HTTP server."""

    config: OperatorServiceConfig = field(default_factory=OperatorServiceConfig)
    runtime: EngineRuntime = field(default_factory=EngineRuntime)
    run_registry: RunRegistry = field(init=False)
    history_store: HistoryStore = field(init=False)
    diagnostics: DiagnosticsManager = field(init=False)
    active_scenario_id: Optional[str] = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.config.repo_root is not None:
            self.runtime.repo_root = self.config.repo_root
        if self.config.scenario_registry_path is not None:
            self.runtime.scenario_registry_path = self.config.scenario_registry_path
        history_path = self.config.history_path
        if history_path is None:
            history_path = self.runtime.repo_root / "docs/fixtures/history/history.jsonl"
        self.history_store = HistoryStore(history_path, self.runtime)
        self.run_registry = RunRegistry(self.runtime, history_store=self.history_store)
        diagnostics_path = self.config.diagnostics_path
        if diagnostics_path is None:
            diagnostics_path = history_path.parent / "diagnostics.jsonl"
        diagnostics_store = DiagnosticsStore(diagnostics_path)
        self.diagnostics = DiagnosticsManager(
            runtime=self.runtime, run_registry=self.run_registry, store=diagnostics_store
        )
        try:
            self.active_scenario_id = self.runtime.load_registry().scenarios[0].scenario_id
        except Exception:  # pragma: no cover - defensive default
            self.active_scenario_id = None

    def build_server(self) -> ThreadingHTTPServer:
        class _BoundHandler(_OperatorRequestHandler):
            ...

        _BoundHandler.runtime = self.runtime
        _BoundHandler.run_registry = self.run_registry
        _BoundHandler.service = self
        _BoundHandler.history_store = self.history_store
        _BoundHandler.diagnostics = self.diagnostics

        server = ThreadingHTTPServer(
            (self.config.host, self.config.port), _BoundHandler
        )
        return server

    def serve_forever(self) -> None:
        with self.build_server() as server:
            server.serve_forever()


def _serialize_diag_summary(result: object) -> dict:
    status = _serialize_diag_status(getattr(result, "status", None))
    summary = dict(status)
    summary["related_run_ids"] = list(getattr(result, "related_run_ids", []) or [])
    return summary


def _serialize_diag_status(status: object) -> dict:
    def _ts(dt: Optional[object]) -> Optional[str]:
        return dt.isoformat() if hasattr(dt, "isoformat") else None

    return {
        "diagnostic_id": getattr(status, "diagnostic_id", None),
        "profile_id": getattr(status, "profile_id", None),
        "state": getattr(status, "state", None),
        "created_at": _ts(getattr(status, "created_at", None)),
        "started_at": _ts(getattr(status, "started_at", None)),
        "finished_at": _ts(getattr(status, "finished_at", None)),
        "summary": getattr(status, "summary", None),
        "checks_passed": getattr(status, "checks_passed", None),
        "checks_failed": getattr(status, "checks_failed", None),
    }


def _serialize_diag_result(result: object) -> dict:
    status = _serialize_diag_status(getattr(result, "status", None))
    checks = []
    for check in getattr(result, "checks", []) or []:
        checks.append(
            {
                "id": getattr(check, "id", None),
                "name": getattr(check, "name", None),
                "description": getattr(check, "description", None),
                "state": getattr(check, "state", None),
                "message": getattr(check, "message", None),
            }
        )

    related_run_ids = list(getattr(result, "related_run_ids", []) or [])

    return {
        "status": status,
        "checks": checks,
        "related_run_ids": related_run_ids,
    }


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the Operator Service")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    parser.add_argument(
        "--registry",
        type=Path,
        help="Optional path to a scenario registry (defaults to repo fixtures)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Optional repository root for EngineRuntime path resolution",
    )
    return parser.parse_args(argv)


def run_operator_service(argv: Optional[list[str]] = None) -> None:
    """CLI entrypoint to start the Operator Service."""

    args = _parse_args(argv)
    config = OperatorServiceConfig(
        host=args.host,
        port=args.port,
        repo_root=args.repo_root,
        scenario_registry_path=args.registry,
    )
    service = OperatorService(config=config)
    service.serve_forever()


if __name__ == "__main__":  # pragma: no cover - CLI execution
    run_operator_service()
