from __future__ import annotations

import argparse
import json
from pathlib import Path

from dpi_quantum import _summarize
from operator_service.diagnostics import DiagnosticsStore, build_fidelity_result
from operator_service.run_registry import HistoryEntry


def _write_history(path: Path, entry: HistoryEntry) -> None:
    path.write_text(json.dumps(entry.to_dict()) + "\n", encoding="utf-8")


def test_summarize_reports_history_and_diagnostics(tmp_path):
    history_path = tmp_path / "history.jsonl"
    diagnostics_path = tmp_path / "diagnostics.jsonl"

    entry = HistoryEntry(
        run_id="run-123",
        scenario_id="gf01",
        started_at="2025-01-01T00:00:00Z",
        ended_at="2025-01-01T00:01:00Z",
        result="completed",
        ticks_total=2,
        summary_metrics={"prob_l1": 0.001},
        status={"result_summary": {"prob_l1": 0.001, "amp_l2": 0.002}},
        dpi={"dpi_id": "dpi-1", "dpi_kind": "INGESTION", "dpi_job_id": "job-abc"},
    )
    _write_history(history_path, entry)

    diagnostics_store = DiagnosticsStore(diagnostics_path)
    diagnostics_store.record(
        build_fidelity_result(
            prob_l1=0.001,
            amp_l2=0.002,
            source="unit test",
            run_id="run-123",
            dpi_job_id="job-abc",
        )
    )

    args = argparse.Namespace(
        run_id="run-123",
        job_id=None,
        history_path=str(history_path),
        diagnostics_path=str(diagnostics_path),
    )
    result = _summarize(args)

    assert result.exit_code == 0
    assert "run run-123 (gf01) -> completed" in result.message
    assert "dpi: id=dpi-1 kind=INGESTION job=job-abc" in result.message
    assert "diagnostics:" in result.message


def test_summarize_handles_missing_entries(tmp_path):
    args = argparse.Namespace(
        run_id="missing",
        job_id=None,
        history_path=str(tmp_path / "history.jsonl"),
        diagnostics_path=str(tmp_path / "diagnostics.jsonl"),
    )
    result = _summarize(args)

    assert result.exit_code == 0
    assert "no history entries" in result.message
    assert "diagnostics: none" in result.message
