from operator_service.quantum_ingest import (
    auto_tune_ingestion_params,
    build_ingestion_result_summary,
    generate_ingestion_outputs,
    quantize_statevector,
    replay_tbp_as_pfna_events,
    simulate_preset_statevector,
    summarize_gate_pfna_replay,
    summarize_pfna_replay,
    tbp_to_pfna_bundle,
    tbp_to_pfna_inputs,
)


def test_auto_tune_ingestion_params_uses_statevector_defaults():
    params = {"auto_tune": True, "qubits": 8}

    tuned = auto_tune_ingestion_params(params)

    assert tuned["eta"] > 0
    assert tuned["phase_bins"] >= 32
    assert tuned["input_source"].startswith("synthetic:")
    assert any("auto-tuned" in note for note in tuned.get("tuning_notes", []))


def test_tbp_to_pfna_bundle_shapes_match_quantization():
    statevector, _ = simulate_preset_statevector("qft", qubits=6)
    encoded = quantize_statevector(statevector, eta=50_000, phase_bins=128)

    inputs = tbp_to_pfna_inputs(encoded, pfna_id="pfna_test", run_id="run123", tick=5)
    assert len(inputs) == 3
    for item in inputs:
        assert item.pfna_id.startswith("pfna_test")
        assert item.tick == 5
        assert len(item.values) == len(encoded["masses"])
        assert all(isinstance(val, int) for val in item.values)

    bundle = tbp_to_pfna_bundle(encoded, pfna_id="pfna_test", run_id="run123", tick=5)
    assert bundle["pfna_id"] == "pfna_test"
    assert bundle["run_id"] == "run123"
    assert bundle["v"] == 0
    assert len(bundle["entries"]) == 3
    assert {entry["tick"] for entry in bundle["entries"]} == {5}
    assert all(len(entry["values"]) == len(encoded["phases"]) for entry in bundle["entries"])


def test_replay_tbp_as_pfna_events_integerizes_payloads():
    statevector, _ = simulate_preset_statevector("ghz", qubits=7)
    encoded = quantize_statevector(statevector, eta=100_000, phase_bins=256)

    events = replay_tbp_as_pfna_events(
        encoded, pfna_id="pfna_replay", gid="GATE", run_id="run42", tick=7
    )

    assert events, "pfna events should be generated for the provided tick"
    for event in events:
        assert event.pfna.tick == 7
        assert event.pfna.run_id == "run42"
        assert event.pfna.pfna_id.startswith("pfna_replay")
        assert len(event.integerized) == len(encoded["masses"])
        assert all(isinstance(val, int) for val in event.integerized)


def test_summarize_pfna_replay_reports_clamped_counts():
    statevector, _ = simulate_preset_statevector("random_clifford", qubits=5)
    encoded = quantize_statevector(statevector, eta=25_000, phase_bins=96)

    summary = summarize_pfna_replay(
        encoded,
        pfna_id="pfna_summary",
        run_id="run77",
    )

    assert summary["events"] == 3
    assert summary["values"] == len(encoded["masses"]) * 3
    assert "min" in summary and "max" in summary


def test_ingestion_result_summary_captures_pfna_replay(monkeypatch):
    monkeypatch.setenv("PYTHONHASHSEED", "0")
    params = {
        "auto_tune": False,
        "qubits": 6,
        "eta": 50_000,
        "phase_bins": 192,
    }

    encoded, fidelity, tune_notes, replay, gate_replay, source = generate_ingestion_outputs(params)

    assert encoded["eta"] == 50_000
    assert fidelity["prob_l1"] >= 0
    assert replay["events"] == 3
    assert source.startswith("synthetic:")

    summary = build_ingestion_result_summary(params)
    assert summary["pfna_replay"]["events"] == 3
    assert summary["masses"] == len(encoded["masses"])
    assert gate_replay["events"] == summary["gate_replay"]["events"]


def test_gate_pfna_replay_runs_through_cmp0_harness():
    statevector, _ = simulate_preset_statevector("qft", qubits=6)
    encoded = quantize_statevector(statevector, eta=50_000, phase_bins=192)

    summary = summarize_gate_pfna_replay(
        encoded, pfna_id="pfna_gate_smoke", run_id="gate_smoke"
    )

    assert summary["events"] > 0
    assert 0 < summary["values"] <= len(encoded["masses"])
    assert "clamped" in summary
