from operator_service.dpi import DpiRegistry
from operator_service.dpi_jobs import apply_job_defaults
from operator_service.dpi_types import DpiJobKind
from operator_service.quantum_ingest import build_ingestion_result_summary
from operator_service.run_registry import HistoryStore


class _DummyRuntime:
    """Minimal runtime stub to satisfy HistoryStore construction."""

    def __getattr__(self, name):  # pragma: no cover - defensive
        raise AttributeError(name)


def test_history_export_carries_tuning_notes(tmp_path, monkeypatch):
    monkeypatch.setenv(DpiRegistry.FEATURE_FLAG, "1")
    registry = DpiRegistry()

    params = apply_job_defaults(
        DpiJobKind.INGESTION,
        {"auto_tune": True, "qubits": 2, "tuning_notes": ["eta tuned"]},
    )
    registry.create_job("quantum", DpiJobKind.INGESTION, params=params, run_id="run-1")

    store = HistoryStore(tmp_path / "history.jsonl", _DummyRuntime(), dpi_registry=registry)

    summaries = store._dpi_job_summaries("run-1")

    assert summaries, "dpi job summaries should be returned for the run"
    assert summaries[0]["params"]["auto_tune"] is True
    assert summaries[0]["tuning_notes"] == ["eta tuned"]


def test_history_export_includes_result_summary(tmp_path, monkeypatch):
    monkeypatch.setenv(DpiRegistry.FEATURE_FLAG, "1")
    registry = DpiRegistry()

    params = apply_job_defaults(
        DpiJobKind.INGESTION, {"auto_tune": False, "qubits": 2, "eta": 10_000, "phase_bins": 64}
    )
    summary = build_ingestion_result_summary(params)
    registry.create_job(
        "quantum", DpiJobKind.INGESTION, params=params, run_id="run-2", result_summary=summary
    )

    store = HistoryStore(tmp_path / "history.jsonl", _DummyRuntime(), dpi_registry=registry)
    summaries = store._dpi_job_summaries("run-2")

    assert summaries and summaries[0]["result_summary"]["pfna_replay"]["events"] == 3
    assert summaries[0]["pfna_replay"]["events"] == 3
    assert summaries[0]["gate_replay"]["events"] >= 0
