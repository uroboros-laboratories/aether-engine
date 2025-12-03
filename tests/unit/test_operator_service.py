import io
import json
import shutil
import tempfile
import threading
import zipfile
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

from config import EngineRuntime
from operator_service import OperatorService, OperatorServiceConfig
from operator_service.run_registry import RunHandle, RunStatus


def _start_service(
    repo_root: Path | None = None,
    history_path: Path | None = None,
    diagnostics_path: Path | None = None,
) -> tuple[ThreadingHTTPServer, threading.Thread, OperatorService]:
    runtime = EngineRuntime(repo_root=repo_root or Path(__file__).resolve().parents[2])
    history_file = history_path or Path(tempfile.mkdtemp()) / "history.jsonl"
    service = OperatorService(
        config=OperatorServiceConfig(
            host="127.0.0.1",
            port=0,
            history_path=history_file,
            diagnostics_path=diagnostics_path,
        ),
        runtime=runtime,
    )
    server = service.build_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, service


def _stop_service(server: ThreadingHTTPServer, thread: threading.Thread) -> None:
    server.shutdown()
    thread.join()


def _build_temp_repo(tmp_path: Path) -> Path:
    fixtures_src = Path(__file__).resolve().parents[2] / "docs" / "fixtures"
    fixtures_dest = tmp_path / "docs" / "fixtures"
    shutil.copytree(fixtures_src, fixtures_dest)
    return tmp_path


def test_cors_headers_allow_cross_origin() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("OPTIONS", "/state", headers={"Origin": "http://example.com"})
        options_resp = conn.getresponse()
        options_resp.read()

        conn.request("GET", "/state", headers={"Origin": "http://example.com"})
        get_resp = conn.getresponse()
        get_resp.read()

        for resp in (options_resp, get_resp):
            assert resp.getheader("Access-Control-Allow-Origin") == "*"
            assert resp.getheader("Access-Control-Allow-Methods") == "GET,POST,OPTIONS"
            assert resp.getheader("Access-Control-Allow-Headers") == "Content-Type"
    finally:
        _stop_service(server, thread)


def test_health_endpoint_reports_registry() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)
        conn.request("GET", "/health")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert body["status"] == "ok"
        assert isinstance(body.get("available_scenarios"), list)
        assert body.get("available_scenarios")
    finally:
        _stop_service(server, thread)


def test_diagnostics_endpoints_run_smoke_profile(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    diagnostics_file = tmp_path / "diagnostics.jsonl"
    server, thread, _ = _start_service(repo_root=repo_root, diagnostics_path=diagnostics_file)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("GET", "/diagnostics/profiles")
        response = conn.getresponse()
        profiles = json.loads(response.read().decode("utf-8"))
        assert any(profile["id"] == "SMOKE" for profile in profiles)

        conn.request("POST", "/diagnostics", body=json.dumps({"profile_id": "SMOKE"}))
        response = conn.getresponse()
        assert response.status == 201
        status = json.loads(response.read().decode("utf-8"))
        diagnostic_id = status["diagnostic_id"]

        for _ in range(30):
            conn.request("GET", f"/diagnostics/{diagnostic_id}")
            detail_resp = conn.getresponse()
            detail = json.loads(detail_resp.read().decode("utf-8"))
            if detail["status"]["state"] in {"PASSED", "FAILED"}:
                break
        else:
            raise AssertionError("diagnostics did not complete")

        assert detail["status"]["diagnostic_id"] == diagnostic_id
        assert detail["checks"]
        assert detail["related_run_ids"]

        conn.request("GET", "/diagnostics")
        list_resp = conn.getresponse()
        listing = json.loads(list_resp.read().decode("utf-8"))
        assert listing["total"] >= 1
        matched = [entry for entry in listing["entries"] if entry["diagnostic_id"] == diagnostic_id]
        assert matched
        assert matched[0]["related_run_ids"]

        related_run_id = detail["related_run_ids"][0]
        conn.request("GET", f"/runs/{related_run_id}/logs")
        logs_resp = conn.getresponse()
        logs_body = json.loads(logs_resp.read().decode("utf-8"))
        assert logs_resp.status == 200
        assert "entries" in logs_body

        conn.request("GET", "/history")
        history_resp = conn.getresponse()
        history = json.loads(history_resp.read().decode("utf-8"))
        assert any(entry["diagnostic_id"] == diagnostic_id for entry in history["diagnostics"])
    finally:
        _stop_service(server, thread)


def test_diagnostics_respects_run_concurrency(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    server, thread, service = _start_service(repo_root=repo_root)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        scenario_id = service.runtime.load_registry().scenarios[0].scenario_id
        session_config = service.runtime.build_session_config(scenario_id)
        status = RunStatus(run_id="test-run", scenario_id=scenario_id, state="running")
        service.run_registry.current = RunHandle(
            scenario_id=scenario_id, session_config=session_config, status=status
        )

        conn.request("POST", "/diagnostics", body=json.dumps({"profile_id": "SMOKE"}))
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 409
        assert "in progress" in body["error"]
    finally:
        _stop_service(server, thread)


def test_unknown_path_returns_404() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)
        conn.request("GET", "/unknown")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 404
        assert body["error"] == "not found"
    finally:
        _stop_service(server, thread)


def test_state_endpoint_reports_active_scenario() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)
        conn.request("GET", "/state")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert body["active_scenario"]["scenario_id"] == "gf01"
        assert body["pillars"]
        assert body["governance"]["codex_action_mode"] == "OBSERVE"
        assert body["current_run"] is None
    finally:
        _stop_service(server, thread)


def test_runs_endpoint_starts_run_and_updates_state() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)
        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 201
        run_id = body["run_id"]
        assert body["scenario_id"] == "gf01"
        assert body["state"] in {"pending", "running", "completed"}

        conn.request("GET", "/state")
        state_response = conn.getresponse()
        state_body = json.loads(state_response.read().decode("utf-8"))

        assert state_response.status == 200
        current = state_body["current_run"]
        if current is not None:
            assert current["run_id"] == run_id
    finally:
        _stop_service(server, thread)


def test_stop_endpoint_handles_unknown_and_running_run() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("POST", "/runs/unknown/stop")
        response = conn.getresponse()
        assert response.status == 404

        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        run_response = conn.getresponse()
        run_body = json.loads(run_response.read().decode("utf-8"))
        run_id = run_body["run_id"]

        conn.request("POST", f"/runs/{run_id}/stop")
        stop_response = conn.getresponse()
        stop_body = json.loads(stop_response.read().decode("utf-8"))

        assert stop_response.status == 202
        assert stop_body["status"]["stop_requested"] is True
    finally:
        _stop_service(server, thread)


def test_scenarios_list_and_detail() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("GET", "/scenarios")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert any(entry["scenario_id"] == "gf01" for entry in body["scenarios"])

        conn.request("GET", "/scenarios/gf01")
        detail_response = conn.getresponse()
        detail_body = json.loads(detail_response.read().decode("utf-8"))

        assert detail_response.status == 200
        assert detail_body["scenario_id"] == "gf01"
        assert detail_body["run_config"]["ticks"] >= 1
    finally:
        _stop_service(server, thread)


def test_activate_scenario_updates_state() -> None:
    server, thread, _ = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("POST", "/scenarios/ring-5/activate")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert body["active_scenario"]["scenario_id"] == "ring-5"

        conn.request("GET", "/state")
        state_response = conn.getresponse()
        state_body = json.loads(state_response.read().decode("utf-8"))

        assert state_body["active_scenario"]["scenario_id"] == "ring-5"
    finally:
        _stop_service(server, thread)


def test_governance_get_and_update(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    server, thread, _ = _start_service(repo_root)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request("GET", "/governance")
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))

        assert response.status == 200
        assert body["governance"]["codex_action_mode"] == "OBSERVE"

        conn.request(
            "POST",
            "/governance",
            body=json.dumps(
                {
                    "codex_action_mode": "DRY_RUN",
                    "budget_policies": [
                        {"policy_id": "default", "max_actions_per_window": 3}
                    ],
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        update_response = conn.getresponse()
        update_body = json.loads(update_response.read().decode("utf-8"))

        assert update_response.status == 200
        assert update_body["governance"]["codex_action_mode"] == "DRY_RUN"

        conn.request("GET", "/state")
        state_response = conn.getresponse()
        state_body = json.loads(state_response.read().decode("utf-8"))

        assert state_body["governance"]["codex_action_mode"] == "DRY_RUN"
        budgets = {
            entry["policy_id"]: entry for entry in state_body["governance"]["budget_policies"]
        }
        assert budgets["default"]["max_actions_per_window"] == 3
    finally:
        _stop_service(server, thread)


def test_update_scenario_persists_to_config(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    server, thread, _ = _start_service(repo_root)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request(
            "POST",
            "/scenarios/gf01",
            body=json.dumps({"ticks": 12, "runtime_hint": "custom"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        update_response = conn.getresponse()
        update_body = json.loads(update_response.read().decode("utf-8"))

        assert update_response.status == 200
        assert update_body["run_config"]["ticks"] == 12
        assert update_body["runtime_hint"] == "custom"

        conn.request("GET", "/scenarios/gf01")
        detail_response = conn.getresponse()
        detail_body = json.loads(detail_response.read().decode("utf-8"))

        assert detail_body["run_config"]["ticks"] == 12
        assert detail_body["runtime_hint"] == "custom"
    finally:
        _stop_service(server, thread)


def test_history_endpoints_capture_completed_run(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    server, thread, service = _start_service(repo_root)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        run_body = json.loads(response.read().decode("utf-8"))
        run_id = run_body["run_id"]

        handle = service.run_registry.history[run_id]
        if handle.thread:
            handle.thread.join(timeout=5)

        conn.request("GET", "/history")
        history_response = conn.getresponse()
        history_body = json.loads(history_response.read().decode("utf-8"))

        assert history_response.status == 200
        assert history_body["total"] == 1
        assert history_body["entries"][0]["run_id"] == run_id

        conn.request("GET", f"/history/{run_id}")
        detail_response = conn.getresponse()
        detail_body = json.loads(detail_response.read().decode("utf-8"))

        assert detail_response.status == 200
        assert detail_body["run"]["run_id"] == run_id
        assert detail_body["metrics"]
        assert detail_body["pillars"]
    finally:
        _stop_service(server, thread)


def test_history_export_endpoint_returns_zip(tmp_path: Path) -> None:
    repo_root = _build_temp_repo(tmp_path)
    server, thread, service = _start_service(repo_root)
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        run_body = json.loads(response.read().decode("utf-8"))
        run_id = run_body["run_id"]

        handle = service.run_registry.history[run_id]
        if handle.thread:
            handle.thread.join(timeout=5)

        conn.request("GET", f"/history/{run_id}/export")
        export_response = conn.getresponse()
        bundle_data = export_response.read()

        assert export_response.status == 200
        assert export_response.getheader("Content-Type") == "application/zip"
        assert bundle_data

        archive = zipfile.ZipFile(io.BytesIO(bundle_data))
        export_payload = json.loads(archive.read("export.json").decode("utf-8"))
        assert export_payload["run"]["run_id"] == run_id
        assert isinstance(export_payload.get("logs"), list)
    finally:
        _stop_service(server, thread)


def test_logs_endpoint_supports_cursor_and_filters() -> None:
    server, thread, service = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))
        run_id = body["run_id"]

        handle = service.run_registry.history[run_id]
        if handle.thread:
            handle.thread.join(timeout=5)

        conn.request("GET", f"/runs/{run_id}/logs")
        logs_response = conn.getresponse()
        logs_body = json.loads(logs_response.read().decode("utf-8"))

        assert logs_response.status == 200
        assert logs_body["entries"]
        assert isinstance(logs_body["cursor"], int)

        cursor = logs_body["cursor"]
        conn.request("GET", f"/runs/{run_id}/logs?cursor={cursor}")
        empty_response = conn.getresponse()
        empty_body = json.loads(empty_response.read().decode("utf-8"))

        assert empty_response.status == 200
        assert empty_body["entries"] == []
        assert empty_body["cursor"] == cursor

        event_type = logs_body["entries"][-1]["event"]
        conn.request("GET", f"/runs/{run_id}/logs?event_type={event_type}")
        filtered_response = conn.getresponse()
        filtered_body = json.loads(filtered_response.read().decode("utf-8"))

        assert filtered_response.status == 200
        assert filtered_body["cursor"] == cursor
        assert all(entry["event"] == event_type for entry in filtered_body["entries"])

        conn.request("GET", "/runs/unknown/logs")
        missing_response = conn.getresponse()
        assert missing_response.status == 404

        conn.request("GET", f"/runs/{run_id}/logs?cursor=not-a-number")
        invalid_response = conn.getresponse()
        assert invalid_response.status == 400
    finally:
        _stop_service(server, thread)


def test_pillars_endpoint_returns_pillar_status() -> None:
    server, thread, service = _start_service()
    try:
        host, port = server.server_address
        conn = HTTPConnection(host, port)

        conn.request(
            "POST",
            "/runs",
            body=json.dumps({"scenario_id": "gf01"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        body = json.loads(response.read().decode("utf-8"))
        run_id = body["run_id"]

        handle = service.run_registry.history[run_id]
        if handle.thread:
            handle.thread.join(timeout=5)

        conn.request("GET", f"/runs/{run_id}/pillars")
        pillars_response = conn.getresponse()
        pillars_body = json.loads(pillars_response.read().decode("utf-8"))

        assert pillars_response.status == 200
        assert isinstance(pillars_body["pillars"], list)
        assert pillars_body["pillars"]
        assert all("headline_metric_label" in pill for pill in pillars_body["pillars"])
    finally:
        _stop_service(server, thread)
