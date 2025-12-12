import argparse

from src.dpi_quantum import _ingest


def test_ingest_reports_gate_replay_metrics(tmp_path):
    args = argparse.Namespace(
        command="ingest",
        input=None,
        eta=1_000_000,
        phase_bins=64,
        qubits=6,
        output=None,
        pfna_output=None,
        pfna_tick=None,
        run_id="gate_cli_smoke",
        gid=None,
        max_prob_l1=None,
        max_amp_l2=None,
        diagnostics_path=str(tmp_path / "diagnostics.jsonl"),
        auto_tune=True,
        kind=None,
    )

    result = _ingest(args)

    assert result.exit_code == 0
    assert "gate replay: events=" in result.message
    assert "replay: events=" in result.message
