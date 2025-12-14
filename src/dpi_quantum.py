"""Console entrypoint for the Quantum Domain Plug-in (DPI).

This CLI is intentionally console-first and independent of the UI layer.
Subcommands are stubbed for now so argument parsing and help output are
stable while the ingestion/simulation/experiment logic is implemented.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional

from config import EngineRuntime
from operator_service.diagnostics import DiagnosticsStore, build_fidelity_result
from operator_service.dpi import DpiJobKind
from operator_service.dpi_jobs import apply_job_defaults, validate_job_params
from operator_service.run_registry import HistoryStore
from operator_service.quantum_ingest import (
    generate_ingestion_outputs,
    quantize_with_auto_tune,
    run_experiment_statevector,
    simulate_preset_statevector,
    summarize_gate_pfna_replay,
    summarize_pfna_replay,
    tbp_to_pfna_inputs,
    tbp_to_pfna_bundle,
)
from ops import RunSummary, append_run_summaries
from core.tick_loop import TickLoopWindowSpec, run_cmp0_tick_loop
from gate.gate import PFNAInputV0, PFNATransformV1
from loom.chain import LoomBlockStore
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import gf01_topology_profile


@dataclass
class CommandResult:
    exit_code: int = 0
    message: Optional[str] = None
    extras: Optional[dict[str, object]] = None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quantum DPI CLI")
    parser.add_argument(
        "--logs-dir",
        dest="logs_dir",
        help="Override run log directory (defaults to <repo>/logs)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest", help="Ingest quantum data into the engine")
    ingest.add_argument("--input", required=False, help="Path to quantum data payload (JSON)")
    ingest.add_argument("--eta", type=float, required=False, help="Quantization scale factor (η)")
    ingest.add_argument("--phase-bins", type=int, default=64, help="Number of phase bins (P)")
    ingest.add_argument("--qubits", type=int, default=2, help="Qubit width of statevector")
    ingest.add_argument("--output", help="Optional output path for TBP payload")
    ingest.add_argument(
        "--pfna-output",
        help="Optional PFNA V0 output path for Gate replay of the TBP payload",
    )
    ingest.add_argument("--pfna-tick", type=int, default=0, help="Tick to attach PFNA entries to")
    ingest.add_argument("--run-id", help="Optional run id to tag PFNA/diagnostics with")
    ingest.add_argument("--gid", help="Override gid when emitting PFNA bundles")
    ingest.add_argument("--max-prob-l1", type=float, help="Fail if probability L1 gap exceeds this threshold")
    ingest.add_argument("--max-amp-l2", type=float, help="Fail if amplitude L2 gap exceeds this threshold")
    ingest.add_argument(
        "--diagnostics-path",
        help="Path to diagnostics.jsonl for recording fidelity failures (defaults to repo fixtures)",
    )
    ingest.add_argument(
        "--auto-tune",
        dest="auto_tune",
        action="store_true",
        default=True,
        help="Auto-tune η/P when not explicitly provided",
    )
    ingest.add_argument(
        "--no-auto-tune",
        dest="auto_tune",
        action="store_false",
        help="Disable auto-tuning even when η/P are omitted",
    )
    ingest.set_defaults(kind=DpiJobKind.INGESTION)

    simulate = subparsers.add_parser("simulate", help="Simulate preset quantum circuits")
    simulate.add_argument("--circuit", required=False, help="Circuit preset id (bell, ghz4, qft4, random_clifford)")
    simulate.add_argument("--qubits", type=int, required=False, help="Number of qubits")
    simulate.add_argument("--layers", type=int, required=False, help="Circuit depth/layers")
    simulate.add_argument("--output", help="Optional output path for TBP payload")
    simulate.add_argument("--pfna-output", help="Optional PFNA V0 output path for Gate replay")
    simulate.add_argument("--pfna-tick", type=int, default=0, help="Tick to attach PFNA entries to")
    simulate.add_argument(
        "--auto-tune",
        dest="auto_tune",
        action="store_true",
        default=True,
        help="Auto-tune η/P when not explicitly provided",
    )
    simulate.add_argument(
        "--no-auto-tune",
        dest="auto_tune",
        action="store_false",
        help="Disable auto-tuning even when η/P are omitted",
    )
    simulate.add_argument("--run-engine", action="store_true", help="Also start an engine run")
    simulate.set_defaults(kind=DpiJobKind.SIMULATION)

    experiment = subparsers.add_parser("experiment", help="Run quantum experiments (e.g. H1 spin chain)")
    experiment.add_argument("--name", default="spin_chain", help="Experiment identifier")
    experiment.add_argument("--qubits", type=int, required=False, help="Qubit count for experiment")
    experiment.add_argument("--ticks", type=int, required=False, help="Ticks per episode")
    experiment.add_argument("--episodes", type=int, required=False, help="Episode count")
    experiment.add_argument("--output", help="Optional output path for TBP payload")
    experiment.add_argument("--pfna-output", help="Optional PFNA V0 output path for Gate replay")
    experiment.add_argument("--pfna-tick", type=int, default=0, help="Tick to attach PFNA entries to")
    experiment.add_argument(
        "--auto-tune",
        dest="auto_tune",
        action="store_true",
        default=True,
        help="Auto-tune η/P when not explicitly provided",
    )
    experiment.add_argument(
        "--no-auto-tune",
        dest="auto_tune",
        action="store_false",
        help="Disable auto-tuning even when η/P are omitted",
    )
    experiment.add_argument("--run-engine", action="store_true", help="Also start an engine run")
    experiment.set_defaults(kind=DpiJobKind.EXPERIMENT)

    summarize = subparsers.add_parser("summarize", help="Summarize past DPI jobs or runs")
    summarize.add_argument("--run-id", help="Engine run id tagged to a DPI job")
    summarize.add_argument("--job-id", help="DPI job id")
    summarize.add_argument(
        "--history-path",
        help="Optional history.jsonl path (defaults to docs/fixtures/history/history.jsonl)",
    )
    summarize.add_argument(
        "--diagnostics-path",
        help="Optional diagnostics.jsonl path (defaults to docs/fixtures/history/diagnostics.jsonl)",
    )
    summarize.set_defaults(kind=None)

    return parser


def _render_stub(kind: Optional[DpiJobKind], args: argparse.Namespace) -> CommandResult:
    hint = "This command is scaffolded; hook up quantum ingestion/simulation logic next."
    params = _safe_params(args)
    validation_errors = validate_job_params(kind, params) if kind else []
    if validation_errors:
        formatted = "\n - ".join([""] + validation_errors)
        return CommandResult(
            exit_code=1,
            message=f"Invalid {kind.value.lower()} parameters:{formatted}\nUse --help to see required fields.",
        )

    normalized = apply_job_defaults(kind, params) if kind else params
    summary_lines = ["Parsed parameters:"]
    summary_lines.extend([f"  - {key}: {value}" for key, value in normalized.items() if value is not None])
    summary_lines.append(hint)
    return CommandResult(exit_code=0, message="\n".join(summary_lines))


def _summarize(args: argparse.Namespace) -> CommandResult:
    repo_root = Path(__file__).resolve().parents[1]
    params = _safe_params(args)
    history_path = Path(params.get("history_path") or repo_root / "docs/fixtures/history/history.jsonl")
    diagnostics_path = Path(params.get("diagnostics_path") or history_path.parent / "diagnostics.jsonl")

    runtime = EngineRuntime(repo_root=repo_root)
    history = HistoryStore(history_path, runtime)
    entries = history.load_entries()

    run_id = params.get("run_id")
    job_id = params.get("job_id")
    selected: List[object] = []
    for entry in entries:
        if run_id and getattr(entry, "run_id", None) == run_id:
            selected.append(entry)
            continue
        if job_id and getattr(entry, "dpi", None):
            dpi_meta = getattr(entry, "dpi") or {}
            if dpi_meta.get("dpi_job_id") == job_id:
                selected.append(entry)

    lines: List[str] = []
    if run_id:
        lines.append(f"lookup: run_id={run_id}")
    if job_id:
        lines.append(f"lookup: job_id={job_id}")

    if not selected:
        lines.append("no history entries found for the provided identifiers")
    else:
        for entry in selected:
            lines.append(
                "run {run} ({scenario}) -> {result}".format(
                    run=entry.run_id, scenario=entry.scenario_id, result=entry.result
                )
            )
            if entry.dpi:
                lines.append(
                    "  dpi: id={dpi_id} kind={dpi_kind} job={dpi_job_id}".format(
                        dpi_id=entry.dpi.get("dpi_id"),
                        dpi_kind=entry.dpi.get("dpi_kind"),
                        dpi_job_id=entry.dpi.get("dpi_job_id"),
                    )
                )
            if entry.summary_metrics:
                lines.append(f"  metrics: {json.dumps(entry.summary_metrics, sort_keys=True)}")
            if entry.status:
                result_summary = entry.status.get("result_summary")
                if result_summary:
                    lines.append(
                        "  result_summary: prob_l1={prob:.6f} amp_l2={amp:.6f}".format(
                            prob=result_summary.get("prob_l1", 0.0),
                            amp=result_summary.get("amp_l2", 0.0),
                        )
                    )

    diag_store = DiagnosticsStore(diagnostics_path)
    diag_matches = []
    for diag in diag_store.load():
        if run_id and run_id in diag.related_run_ids:
            diag_matches.append(diag)
            continue
        if job_id and job_id in diag.related_run_ids:
            diag_matches.append(diag)

    if diag_matches:
        lines.append("diagnostics:")
        for diag in diag_matches:
            lines.append(
                "  {diagnostic_id}: {summary}".format(
                    diagnostic_id=diag.status.diagnostic_id,
                    summary=diag.status.summary or diag.status.state,
                )
            )
    else:
        lines.append("diagnostics: none recorded for selection")

    return CommandResult(exit_code=0, message="\n".join(lines))


def _ingest(args: argparse.Namespace) -> CommandResult:
    params = apply_job_defaults(DpiJobKind.INGESTION, _safe_params(args))
    errors = validate_job_params(DpiJobKind.INGESTION, params)
    if errors:
        formatted = "\n - ".join([""] + errors)
        return CommandResult(
            exit_code=1,
            message=f"Invalid ingestion parameters:{formatted}\nUse --help to see required fields.",
        )

    try:
        (
            encoded,
            fidelity,
            tune_notes,
            replay,
            gate_replay,
            source,
        ) = generate_ingestion_outputs(params)
    except Exception as exc:  # pragma: no cover - CLI error path
        return CommandResult(exit_code=1, message=f"Ingestion failed: {exc}")

    output_path = params.get("output")
    if output_path:
        Path(output_path).write_text(json.dumps(encoded, indent=2))

    pfna_output = params.get("pfna_output")
    pfna_written: Optional[Path] = None
    if pfna_output:
        pfna_bundle = tbp_to_pfna_bundle(
            encoded,
            pfna_id=str(params.get("run_id") or "tbp_ingest"),
            gid=str(params.get("gid") or "GATE"),
            run_id=str(params.get("run_id") or "dpi_quantum"),
            tick=int(params.get("pfna_tick") or 0),
        )
        pfna_path = Path(pfna_output)
        pfna_path.write_text(json.dumps(pfna_bundle, indent=2))
        pfna_written = pfna_path

    summary_lines = ["ingestion completed", f"  source: {source}"]
    summary_lines.append(f"  masses: {len(encoded['masses'])} entries")
    summary_lines.append(
        f"  phases: {len(set(encoded['phases']))} unique buckets across {encoded['P']} bins"
    )
    summary_lines.append(f"  residuals: max={max(encoded['residuals'])} min={min(encoded['residuals'])}")
    prob_l1 = fidelity["prob_l1"]
    amp_l2 = fidelity["amp_l2"]
    summary_lines.append(
        "  fidelity: prob_l1={prob_l1:.6f} amp_l2={amp_l2:.6f}".format(
            prob_l1=prob_l1, amp_l2=amp_l2
        )
    )
    if replay:
        replay_line = "  replay: events={events} values={values}".format(
            events=replay.get("events", 0), values=replay.get("values", 0)
        )
        if replay.get("min") is not None and replay.get("max") is not None:
            replay_line += " range=[{min},{max}]".format(
                min=replay.get("min"), max=replay.get("max")
            )
        if replay.get("clamped"):
            replay_line += f" clamped={replay['clamped']}"
        summary_lines.append(replay_line)
    if gate_replay:
        gate_line = "  gate replay: events={events} values={values}".format(
            events=gate_replay.get("events", 0), values=gate_replay.get("values", 0)
        )
        if gate_replay.get("min") is not None and gate_replay.get("max") is not None:
            gate_line += " range=[{min},{max}]".format(
                min=gate_replay.get("min"), max=gate_replay.get("max")
            )
        if gate_replay.get("clamped"):
            gate_line += f" clamped={gate_replay['clamped']}"
        summary_lines.append(gate_line)
    prob_l1_limit = params.get("max_prob_l1")
    amp_l2_limit = params.get("max_amp_l2")
    failures = []
    if prob_l1_limit is not None and prob_l1 > float(prob_l1_limit):
        failures.append(f"prob_l1={prob_l1:.6f} exceeded max_prob_l1={prob_l1_limit}")
    if amp_l2_limit is not None and amp_l2 > float(amp_l2_limit):
        failures.append(f"amp_l2={amp_l2:.6f} exceeded max_amp_l2={amp_l2_limit}")
    if prob_l1_limit is not None or amp_l2_limit is not None:
        summary_lines.append(
            "  thresholds: max_prob_l1={prob} max_amp_l2={amp}".format(
                prob=prob_l1_limit, amp=amp_l2_limit
            )
        )
    if failures:
        summary_lines.append("  status: FAILED fidelity checks")
        summary_lines.extend([f"    - {item}" for item in failures])
        diagnostics_note = _record_fidelity_diagnostic(
            prob_l1=prob_l1,
            amp_l2=amp_l2,
            params=params,
            diagnostics_path=params.get("diagnostics_path"),
        )
        _record_run_summary(
            kind="ingest",
            params=params,
            fidelity=fidelity,
            status="FAILED",
            notes="; ".join(failures),
        )
        if diagnostics_note:
            summary_lines.append(f"  diagnostics: {diagnostics_note}")
        return CommandResult(exit_code=1, message="\n".join(summary_lines))
    elif prob_l1_limit is not None or amp_l2_limit is not None:
        summary_lines.append("  status: fidelity within configured thresholds")
    if tune_notes:
        summary_lines.extend([f"  auto-tune: {note}" for note in tune_notes])
    if output_path:
        summary_lines.append(f"  written: {output_path}")
    if pfna_written:
        summary_lines.append(f"  pfna_bundle: written to {pfna_written}")
    _record_run_summary(
        kind="ingest",
        params=params,
        fidelity=fidelity,
        status="OK",
        extras={"tune_notes": tune_notes, "replay": replay, "gate_replay": gate_replay},
    )
    return CommandResult(exit_code=0, message="\n".join(summary_lines))


def _simulate(args: argparse.Namespace) -> CommandResult:
    params = apply_job_defaults(DpiJobKind.SIMULATION, _safe_params(args))
    errors = validate_job_params(DpiJobKind.SIMULATION, params)
    if errors:
        formatted = "\n - ".join([""] + errors)
        return CommandResult(
            exit_code=1,
            message=f"Invalid simulation parameters:{formatted}\nUse --help to see required fields.",
        )

    overall_start = time.perf_counter()
    try:
        statevector, desc = simulate_preset_statevector(
            params.get("circuit", "bell"),
            qubits=int(params.get("qubits") or 2),
            layers=int(params.get("layers") or 1),
        )
        encoded, fidelity, tune_notes = quantize_with_auto_tune(statevector, params)
    except Exception as exc:  # pragma: no cover - CLI error path
        return CommandResult(exit_code=1, message=f"Simulation failed: {exc}")

    summary_lines = ["simulation completed", f"  circuit: {desc}"]
    summary_lines.append(f"  eta={encoded['eta']} P={encoded['P']}")
    summary_lines.append(f"  masses: {len(encoded['masses'])} entries")
    summary_lines.append(f"  residuals: max={max(encoded['residuals'])} min={min(encoded['residuals'])}")
    summary_lines.append(
        "  fidelity: prob_l1={prob:.6f} amp_l2={amp:.6f}".format(
            prob=fidelity["prob_l1"], amp=fidelity["amp_l2"]
        )
    )
    replay = summarize_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_simulate"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 0),
    )
    if replay:
        summary_lines.append(
            "  replay: events={events} values={values} range=[{min},{max}]".format(
                events=replay.get("events", 0),
                values=replay.get("values", 0),
                min=replay.get("min"),
                max=replay.get("max"),
            )
        )
    gate_replay = summarize_gate_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_simulate"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 1),
    )
    if gate_replay:
        summary_lines.append(
            "  gate replay: events={events} values={values} range=[{min},{max}]".format(
                events=gate_replay.get("events", 0),
                values=gate_replay.get("values", 0),
                min=gate_replay.get("min"),
                max=gate_replay.get("max"),
            )
        )
    if tune_notes:
        summary_lines.extend([f"  auto-tune: {note}" for note in tune_notes])
    if params.get("output"):
        Path(params["output"]).write_text(json.dumps(encoded, indent=2))
        summary_lines.append(f"  written: {params['output']}")
    pfna_written = _maybe_write_pfna_bundle(encoded, params)
    if pfna_written:
        summary_lines.append(f"  pfna_bundle: written to {pfna_written}")
    engine_metrics = None
    if params.get("run_engine"):
        try:
            engine_metrics = _run_engine_with_pfna(
                kind="simulate",
                encoded=encoded,
                params=params,
                total_ticks=int(params.get("ticks") or params.get("layers") or 4),
            )
            summary_lines.append(f"  engine run: run_id={engine_metrics['run_id']}")
            summary_lines.append(
                "  loom: p_blocks={p} i_blocks={i} bytes={b} ticks={t}".format(
                    p=engine_metrics["loom_p_blocks"],
                    i=engine_metrics["loom_i_blocks"],
                    b=engine_metrics["loom_bytes"],
                    t=engine_metrics["ticks"],
                )
            )
        except Exception as exc:  # pragma: no cover - engine failure path
            runtime_total_ms = (time.perf_counter() - overall_start) * 1000
            summary_lines.append(f"  engine run: failed ({exc})")
            _record_run_summary(
                kind="simulate",
                params=params,
                fidelity=fidelity,
                status="FAILED",
                runtime_total_ms=runtime_total_ms,
                error_message=str(exc),
                error_code="ENGINE_RUN_FAILED",
                extras={"replay": replay, "gate_replay": gate_replay, "tune_notes": tune_notes},
            )
            return CommandResult(exit_code=1, message="\n".join(summary_lines))
    _record_run_summary(
        kind="simulate",
        params=params,
        fidelity=fidelity,
        status="OK",
        runtime_total_ms=(time.perf_counter() - overall_start) * 1000,
        runtime_engine_ms=engine_metrics["runtime_engine_ms"] if engine_metrics else None,
        ticks=engine_metrics["ticks"] if engine_metrics else params.get("ticks"),
        loom_p_blocks=engine_metrics.get("loom_p_blocks") if engine_metrics else None,
        loom_i_blocks=engine_metrics.get("loom_i_blocks") if engine_metrics else None,
        loom_bytes=engine_metrics.get("loom_bytes") if engine_metrics else None,
        run_id=engine_metrics["run_id"] if engine_metrics else None,
        extras={"replay": replay, "gate_replay": gate_replay, "tune_notes": tune_notes},
    )
    return CommandResult(exit_code=0, message="\n".join(summary_lines))


def _experiment(args: argparse.Namespace) -> CommandResult:
    params = apply_job_defaults(DpiJobKind.EXPERIMENT, _safe_params(args))
    errors = validate_job_params(DpiJobKind.EXPERIMENT, params)
    if errors:
        formatted = "\n - ".join([""] + errors)
        return CommandResult(
            exit_code=1,
            message=f"Invalid experiment parameters:{formatted}\nUse --help to see required fields.",
        )

    overall_start = time.perf_counter()
    try:
        statevector, desc = run_experiment_statevector(
            params.get("name", "spin_chain"),
            qubits=int(params.get("qubits") or 4),
            ticks=int(params.get("ticks") or 4),
            episodes=int(params.get("episodes") or 1),
        )
        encoded, fidelity, tune_notes = quantize_with_auto_tune(statevector, params)
    except Exception as exc:  # pragma: no cover - CLI error path
        return CommandResult(exit_code=1, message=f"Experiment failed: {exc}")
    summary_lines = ["experiment completed", f"  experiment: {desc}"]
    summary_lines.append(f"  eta={encoded['eta']} P={encoded['P']}")
    summary_lines.append(f"  masses: {len(encoded['masses'])} entries")
    summary_lines.append(f"  residuals: max={max(encoded['residuals'])} min={min(encoded['residuals'])}")
    summary_lines.append(
        "  fidelity: prob_l1={prob:.6f} amp_l2={amp:.6f}".format(
            prob=fidelity["prob_l1"], amp=fidelity["amp_l2"]
        )
    )
    replay = summarize_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_experiment"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 0),
    )
    if replay:
        summary_lines.append(
            "  replay: events={events} values={values} range=[{min},{max}]".format(
                events=replay.get("events", 0),
                values=replay.get("values", 0),
                min=replay.get("min"),
                max=replay.get("max"),
            )
        )
    gate_replay = summarize_gate_pfna_replay(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_experiment"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 1),
    )
    if gate_replay:
        summary_lines.append(
            "  gate replay: events={events} values={values} range=[{min},{max}]".format(
                events=gate_replay.get("events", 0),
                values=gate_replay.get("values", 0),
                min=gate_replay.get("min"),
                max=gate_replay.get("max"),
            )
        )
    if tune_notes:
        summary_lines.extend([f"  auto-tune: {note}" for note in tune_notes])
    if params.get("output"):
        Path(params["output"]).write_text(json.dumps(encoded, indent=2))
        summary_lines.append(f"  written: {params['output']}")
    pfna_written = _maybe_write_pfna_bundle(encoded, params)
    if pfna_written:
        summary_lines.append(f"  pfna_bundle: written to {pfna_written}")
    engine_metrics = None
    if params.get("run_engine"):
        try:
            engine_metrics = _run_engine_with_pfna(
                kind="experiment",
                encoded=encoded,
                params=params,
                total_ticks=int(params.get("ticks") or 4),
            )
            summary_lines.append(f"  engine run: run_id={engine_metrics['run_id']}")
            summary_lines.append(
                "  loom: p_blocks={p} i_blocks={i} bytes={b} ticks={t}".format(
                    p=engine_metrics["loom_p_blocks"],
                    i=engine_metrics["loom_i_blocks"],
                    b=engine_metrics["loom_bytes"],
                    t=engine_metrics["ticks"],
                )
            )
        except Exception as exc:  # pragma: no cover - engine failure path
            runtime_total_ms = (time.perf_counter() - overall_start) * 1000
            summary_lines.append(f"  engine run: failed ({exc})")
            _record_run_summary(
                kind="experiment",
                params=params,
                fidelity=fidelity,
                status="FAILED",
                runtime_total_ms=runtime_total_ms,
                error_message=str(exc),
                error_code="ENGINE_RUN_FAILED",
                extras={
                    "replay": replay,
                    "gate_replay": gate_replay,
                    "tune_notes": tune_notes,
                },
            )
            return CommandResult(exit_code=1, message="\n".join(summary_lines))

    runtime_total_ms = (time.perf_counter() - overall_start) * 1000
    summary_run_id = engine_metrics["run_id"] if engine_metrics else str(params.get("run_id") or "dpi_quantum")
    _record_run_summary(
        kind="experiment",
        params=params,
        fidelity=fidelity,
        status="OK",
        runtime_total_ms=runtime_total_ms,
        runtime_engine_ms=engine_metrics["runtime_engine_ms"] if engine_metrics else None,
        ticks=engine_metrics["ticks"] if engine_metrics else params.get("ticks"),
        loom_p_blocks=engine_metrics.get("loom_p_blocks") if engine_metrics else None,
        loom_i_blocks=engine_metrics.get("loom_i_blocks") if engine_metrics else None,
        loom_bytes=engine_metrics.get("loom_bytes") if engine_metrics else None,
        run_id=summary_run_id,
        extras={"replay": replay, "gate_replay": gate_replay, "tune_notes": tune_notes},
    )
    return CommandResult(exit_code=0, message="\n".join(summary_lines))


def _run_engine_with_pfna(
    *, kind: str, encoded: Dict[str, object], params: Dict[str, object], total_ticks: int
) -> Dict[str, object]:
    repo_root = Path(__file__).resolve().parents[1]
    logs_root = Path(str(params.get("logs_dir"))).expanduser() if params.get("logs_dir") else repo_root
    run_id = str(params.get("run_id") or f"{kind}-engine")
    nid = str(params.get("nid") or "dpi_quantum")
    profile = gf01_profile_cmp0()
    topo, pfna_inputs = _prepare_pfna_inputs(encoded, params, run_id=run_id)

    window_spec = TickLoopWindowSpec(
        window_id="DPI_GF01_window",
        apx_name="DPI_GF01_APX",
        start_tick=1,
        end_tick=max(int(total_ticks), 1),
    )

    loom_store = LoomBlockStore(logs_root / "logs" / "loom" / run_id)
    engine_start = time.perf_counter()
    result = run_cmp0_tick_loop(
        topo=topo,
        profile=profile,
        initial_state=_initial_state_for_topology(topo.N),
        total_ticks=max(int(total_ticks), 1),
        window_specs=(window_spec,),
        primary_window_id=window_spec.window_id,
        run_id=run_id,
        nid=nid,
        pfna_inputs=pfna_inputs,
        pfna_transform=PFNATransformV1(),
        loom_block_store=loom_store,
    )
    runtime_engine_ms = (time.perf_counter() - engine_start) * 1000

    return {
        "run_id": run_id,
        "result": result,
        "runtime_engine_ms": runtime_engine_ms,
        "loom_p_blocks": len(result.p_blocks),
        "loom_i_blocks": len(result.i_blocks),
        "loom_bytes": _loom_bytes(loom_store),
        "ticks": len(result.ledgers),
        "loom_store": loom_store,
    }


def _initial_state_for_topology(length: int) -> List[int]:
    base = [3, 1, 0, 0, 0, 0]
    if length <= len(base):
        return base[:length]
    return base + [0] * (length - len(base))


def _prepare_pfna_inputs(encoded: Dict[str, object], params: Dict[str, object], *, run_id: str):
    topo = gf01_topology_profile()
    gid = str(params.get("gid") or topo.gid)
    pfna_id = str(params.get("run_id") or params.get("name") or params.get("circuit") or run_id or "tbp_pfna")
    tick = int(params.get("pfna_tick") or 0)
    inputs = tbp_to_pfna_inputs(
        encoded, pfna_id=pfna_id, gid=gid, run_id=run_id, nid=str(params.get("nid") or "quantum"), tick=tick
    )

    adjusted: List[PFNAInputV0] = []
    for item in inputs:
        values = tuple(item.values)
        if len(values) < topo.N:
            values = values + (0,) * (topo.N - len(values))
        elif len(values) > topo.N:
            values = values[: topo.N]
        adjusted.append(
            PFNAInputV0(
                pfna_id=item.pfna_id,
                gid=gid,
                run_id=run_id,
                tick=item.tick,
                nid=item.nid,
                values=values,
                description=item.description,
            )
        )
    return topo, adjusted


def _loom_bytes(store: LoomBlockStore) -> int:
    if not store or not store.index_path.exists():
        return 0
    try:
        index = json.loads(store.index_path.read_text())
        p_bytes = sum(entry.get("bin_size", 0) for entry in index.get("p", []))
        i_bytes = sum(entry.get("bin_size", 0) for entry in index.get("i", []))
        return p_bytes + i_bytes
    except Exception:
        return 0


def _record_run_summary(
    *,
    kind: str,
    params: Dict[str, object],
    fidelity: Dict[str, float],
    status: str,
    notes: str = "",
    extras: Optional[Dict[str, object]] = None,
    runtime_total_ms: Optional[float] = None,
    runtime_engine_ms: Optional[float] = None,
    ticks: Optional[int] = None,
    loom_p_blocks: Optional[int] = None,
    loom_i_blocks: Optional[int] = None,
    loom_bytes: Optional[int] = None,
    peak_mem_mb: Optional[float] = None,
    error_code: Optional[str] = None,
    error_message: Optional[str] = None,
    run_id: Optional[str] = None,
) -> None:
    """Persist a RunSummary row to the shared run sheets."""

    repo_root = Path(__file__).resolve().parents[1]
    logs_root = (
        Path(str(params.get("logs_dir"))).expanduser() if params.get("logs_dir") else repo_root
    )
    scenario_hint = {
        "ingest": params.get("input") or "ingest",
        "simulate": params.get("circuit") or "simulate",
        "experiment": params.get("name") or "experiment",
    }.get(kind, kind)
    summary = RunSummary.from_defaults(
        run_id=str(run_id or params.get("run_id") or f"{kind}-{params.get('pfna_tick', 0)}"),
        scenario=f"{kind}:{scenario_hint}",
        status=status,
        n_qubits=int(params.get("qubits")) if params.get("qubits") is not None else None,
        ticks=int(ticks) if ticks is not None else int(params.get("ticks")) if params.get("ticks") is not None else None,
        dpi_mode=kind,
        loom_mode="GF01",
        runtime_total_ms=runtime_total_ms,
        runtime_engine_ms=runtime_engine_ms,
        loom_p_blocks=loom_p_blocks,
        loom_i_blocks=loom_i_blocks,
        loom_bytes=loom_bytes,
        peak_mem_mb=peak_mem_mb,
        error_code=error_code,
        error_message=error_message,
        fidelity_prob_l1=fidelity.get("prob_l1"),
        fidelity_amp_l2=fidelity.get("amp_l2"),
        notes=notes,
        extras=extras,
    )
    append_run_summaries([summary], repo_root=logs_root)


def _record_fidelity_diagnostic(
    *,
    prob_l1: float,
    amp_l2: float,
    params: Dict[str, object],
    diagnostics_path: Optional[str] = None,
) -> Optional[str]:
    """Persist fidelity failures to diagnostics.jsonl for operator visibility."""

    path = diagnostics_path
    if not path:
        path = Path(__file__).resolve().parents[1] / "docs/fixtures/history/diagnostics.jsonl"
    diag_path = Path(path)

    result = build_fidelity_result(
        prob_l1=prob_l1,
        amp_l2=amp_l2,
        source="dpi_quantum ingest",
        run_id=str(params.get("run_id") or "dpi_quantum"),
        max_prob_l1=float(params["max_prob_l1"]) if params.get("max_prob_l1") is not None else None,
        max_amp_l2=float(params["max_amp_l2"]) if params.get("max_amp_l2") is not None else None,
    )
    DiagnosticsStore(diag_path).record(result)
    return f"recorded fidelity failure to {diag_path}"


def _maybe_write_pfna_bundle(encoded: Dict[str, object], params: Dict[str, object]) -> Optional[Path]:
    pfna_output = params.get("pfna_output")
    if not pfna_output:
        return None
    pfna_bundle = tbp_to_pfna_bundle(
        encoded,
        pfna_id=str(params.get("run_id") or "tbp_ingest"),
        gid=str(params.get("gid") or "GATE"),
        run_id=str(params.get("run_id") or "dpi_quantum"),
        tick=int(params.get("pfna_tick") or 0),
    )
    pfna_path = Path(str(pfna_output))
    pfna_path.write_text(json.dumps(pfna_bundle, indent=2))
    return pfna_path


def _safe_params(args: argparse.Namespace) -> Dict[str, object]:
    return {k: v for k, v in vars(args).items() if k not in {"command", "kind"}}


def _dispatch(args: argparse.Namespace) -> CommandResult:
    handlers: Dict[Optional[DpiJobKind], Callable[[argparse.Namespace], CommandResult]] = {
        None: _summarize,
        DpiJobKind.INGESTION: _ingest,
        DpiJobKind.SIMULATION: _simulate,
        DpiJobKind.EXPERIMENT: _experiment,
    }
    handler = handlers.get(getattr(args, "kind", None))
    if handler is None:
        return CommandResult(exit_code=1, message="Unknown command")
    return handler(args)


def main(argv: Optional[List[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    result = _dispatch(args)
    if result.message:
        sys.stdout.write(result.message + "\n")
    raise SystemExit(result.exit_code)


if __name__ == "__main__":  # pragma: no cover - CLI execution
    main()
