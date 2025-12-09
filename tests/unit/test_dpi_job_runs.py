from pathlib import Path

import pytest

from config import EngineRuntime
from operator_service.dpi import DpiJobStatus, DpiRegistry
from operator_service.dpi_jobs import apply_job_defaults
from operator_service.dpi_types import DpiJobKind
from operator_service.run_registry import HistoryStore, RunRegistry
from operator_service.service import _start_run_for_job


@pytest.fixture()
def runtime() -> EngineRuntime:
    return EngineRuntime(repo_root=Path(__file__).resolve().parents[2])


def test_simulation_job_requests_run(monkeypatch, tmp_path, runtime: EngineRuntime) -> None:
    monkeypatch.setenv(DpiRegistry.FEATURE_FLAG, "1")
    dpi_registry = DpiRegistry()
    history = HistoryStore(tmp_path / "history.jsonl", runtime, dpi_registry=dpi_registry)
    run_registry = RunRegistry(runtime, history_store=history)

    params = apply_job_defaults(
        DpiJobKind.SIMULATION, {"run_engine": True, "scenario_id": "gf01"}
    )
    job = dpi_registry.create_job(
        "quantum", DpiJobKind.SIMULATION, params=params, status=DpiJobStatus.QUEUED
    )

    handle, summary = _start_run_for_job(runtime, run_registry, dpi_registry, job)

    assert handle is not None, "run should start when run_engine is requested"
    handle.thread.join(timeout=10)
    assert job.run_id == handle.status.run_id
    assert job.status == DpiJobStatus.RUNNING
    assert summary and summary["scenario_id"] == "gf01"
    assert dpi_registry.list_jobs_for_run(job.run_id)
