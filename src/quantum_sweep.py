"""Sweep runner CLI for Phase 9 EPIC 4.

This version loads sweep configs, expands parameter grids, and can execute
each point against the DPI hero commands or GF01 snapshot tools with
checkpointed stop/resume support.
"""
from __future__ import annotations

import argparse
import sys
import time
import json
from pathlib import Path
from typing import Iterable, Optional

from cli import _snapshot_compare_command, _snapshot_generate_command
from dpi_quantum import CommandResult, _dispatch
from operator_service.dpi import DpiJobKind
from ops import RunSummary, append_run_summaries, compute_emulation_metrics
from ops.snapshots import compare_snapshots
from ops.sweeps import SweepConfig, iter_points, load_sweep_config
from core import run_gf01
from core.serialization import serialize_gf01_run


REPO_ROOT = Path(__file__).resolve().parent.parent
DPI_KINDS = {"ingest", "simulate", "experiment"}
EMULATION_KINDS = {"emulation_compare"}
GF01_KINDS = {"gf01_run", "gf01_compare"}


def _logs_root(logs_dir: Optional[str]) -> Path:
    return Path(logs_dir).expanduser().resolve() if logs_dir else REPO_ROOT


def _summary_for_point(
    config: SweepConfig,
    *,
    point_index: int,
    params: dict,
    status: str = "PLANNED",
    runtime_ms: Optional[float] = None,
    notes: str = "sweep plan",
    extras: Optional[dict] = None,
) -> RunSummary:
    scenario_hint = (
        params.get("target")
        or params.get("circuit")
        or params.get("name")
        or params.get("run_id")
        or config.name
    )
    merged_extras = {"params": params, "sweep": config.name, "point_index": point_index}
    if extras:
        merged_extras.update(extras)
    return RunSummary.from_defaults(
        run_id=str(params.get("run_id") or f"{config.kind}-{point_index}"),
        scenario=f"sweep:{config.kind}:{scenario_hint}",
        status=status,
        n_qubits=int(params.get("qubits")) if params.get("qubits") is not None else None,
        ticks=int(params.get("ticks")) if params.get("ticks") is not None else None,
        dpi_mode=config.kind,
        runtime_total_ms=runtime_ms,
        notes=notes,
        extras=merged_extras,
    )


def _state_path(config: SweepConfig, *, logs_dir: Optional[str], state_file: Optional[str]) -> Path:
    if state_file:
        return Path(state_file).expanduser().resolve()
    base = _logs_root(logs_dir) / "logs" / "sweeps"
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{config.name}.state"


def _load_checkpoint(path: Path, *, resume: bool) -> int:
    if not resume:
        return -1
    if path.exists():
        try:
            return int(path.read_text().strip() or -1)
        except ValueError:
            return -1
    return -1


def _persist_checkpoint(path: Path, index: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(index))


def _namespace_for_kind(kind: str, params: dict) -> argparse.Namespace:
    payload = dict(params)
    if kind in DPI_KINDS:
        payload["command"] = kind
        payload["kind"] = {
            "ingest": DpiJobKind.INGESTION,
            "simulate": DpiJobKind.SIMULATION,
            "experiment": DpiJobKind.EXPERIMENT,
        }.get(kind)
    elif kind == "snapshot_generate":
        payload.setdefault("command", "snapshot")
        payload.setdefault("snapshot_command", "generate")
        payload.setdefault("output", None)
        payload.setdefault("run_config", None)
        payload.setdefault("registry", None)
    elif kind == "snapshot_compare":
        payload.setdefault("command", "snapshot")
        payload.setdefault("snapshot_command", "compare")
        payload.setdefault("candidate", None)
        payload.setdefault("output", None)
        payload.setdefault("run_config", None)
        payload.setdefault("registry", None)
        payload.setdefault("max_diffs", 100)
    elif kind in EMULATION_KINDS:
        payload.setdefault("command", "emulation_compare")
    else:  # pragma: no cover - config validation should stop us first
        raise ValueError(f"Unsupported sweep kind '{kind}'")
    return argparse.Namespace(**payload)


def _capture_cli_call(func, args: argparse.Namespace) -> CommandResult:
    """Run a CLI handler and capture its exit semantics as CommandResult."""

    try:
        func(args)
        return CommandResult(exit_code=0, message="OK")
    except SystemExit as exc:  # pragma: no cover - mirrors CLI behaviour
        code = exc.code if isinstance(exc.code, int) else 1
        return CommandResult(exit_code=code, message=str(exc))
    except Exception as exc:  # pragma: no cover - unexpected handler failure
        return CommandResult(exit_code=1, message=str(exc))


def _execute_point(
    config: SweepConfig, *, point_index: int, params: dict, logs_dir: Optional[str]
) -> CommandResult:
    enriched = dict(params)
    if config.kind in DPI_KINDS:
        enriched.setdefault("run_id", f"{config.name}-{point_index}")
    if logs_dir:
        enriched.setdefault("logs_dir", logs_dir)

    if config.kind in DPI_KINDS:
        args = _namespace_for_kind(config.kind, enriched)
        return _dispatch(args)
    if config.kind == "snapshot_generate":
        args = _namespace_for_kind(config.kind, enriched)
        return _capture_cli_call(_snapshot_generate_command, args)
    if config.kind == "snapshot_compare":
        args = _namespace_for_kind(config.kind, enriched)
        return _capture_cli_call(_snapshot_compare_command, args)
    if config.kind == "emulation_compare":
        metrics = compute_emulation_metrics(
            oracle_probs=enriched.get("oracle_probs"),
            candidate_probs=enriched.get("emulated_probs") or enriched.get("candidate_probs"),
            oracle_amps=enriched.get("oracle_amps"),
            candidate_amps=enriched.get("emulated_amps") or enriched.get("candidate_amps"),
            prob_tolerance=float(enriched.get("prob_tolerance", 0.05)),
            amp_tolerance=float(enriched.get("amp_tolerance", 0.1)),
        )
        ok = metrics.get("emulation_ok", False)
        message = "Emulation within tolerance" if ok else "Emulation drift beyond tolerance"
        return CommandResult(exit_code=0 if ok else 1, message=message, extras=dict(metrics))

    if config.kind in GF01_KINDS:
        run_id = str(enriched.get("run_id") or f"gf01-{point_index}")
        snapshot_dir = _logs_root(logs_dir) / "logs" / "snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        if config.kind == "gf01_run":
            target_path = Path(
                enriched.get("output") or snapshot_dir / f"{run_id}_snapshot.json"
            ).expanduser().resolve()
            result = run_gf01(run_id=run_id)
            snapshot = serialize_gf01_run(result)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(snapshot, indent=2))
            extras = {
                "snapshot_path": str(target_path),
                "ledger_count": len(snapshot.get("ledgers", [])),
                "p_block_count": len(snapshot.get("p_blocks", [])),
                "i_block_count": len(snapshot.get("i_blocks", [])),
            }
            return CommandResult(
                exit_code=0,
                message=f"GF01 run captured at {target_path}",
                extras=extras,
            )

        baseline_raw = enriched.get("baseline")
        if not baseline_raw:
            return CommandResult(exit_code=1, message="baseline is required for gf01_compare sweeps")

        baseline_path = Path(baseline_raw).expanduser().resolve()
        candidate_path = (
            Path(enriched["candidate"]).expanduser().resolve()
            if enriched.get("candidate")
            else None
        )
        run_config = (
            Path(enriched["run_config"]).expanduser().resolve()
            if enriched.get("run_config")
            else None
        )
        registry_path = Path(
            enriched.get("registry")
            or REPO_ROOT / "docs/fixtures/scenarios/scenario_registry.json"
        ).expanduser().resolve()
        scenario = enriched.get("target") or "gf01"
        output_path = Path(
            enriched.get("output") or snapshot_dir / f"{run_id}_snapshot.json"
        ).expanduser().resolve()

        diffs, candidate = compare_snapshots(
            baseline_path=baseline_path,
            candidate_path=candidate_path,
            scenario=None if candidate_path or run_config else scenario,
            run_config=run_config,
            registry_path=None if candidate_path or run_config else registry_path,
            max_diffs=int(enriched.get("max_diffs", 25)),
        )

        if candidate_path is None or output_path != candidate_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(candidate, indent=2))

        extras = {
            "baseline_path": str(baseline_path),
            "candidate_path": str(candidate_path or output_path),
            "diff_count": len(diffs),
            "ledger_count": len(candidate.get("ledgers", []) or []),
            "p_block_count": len(candidate.get("p_blocks", []) or []),
            "i_block_count": len(candidate.get("i_blocks", []) or []),
        }
        message = "Snapshots match" if not diffs else f"{len(diffs)} GF01 snapshot diffs"
        return CommandResult(exit_code=0 if not diffs else 1, message=message, extras=extras)

    return CommandResult(exit_code=1, message=f"Unsupported sweep kind {config.kind}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quantum sweep runner (scaffold)")
    parser.add_argument("config", help="Path to sweep config (YAML or JSON)")
    parser.add_argument("--logs-dir", help="Override run log directory (defaults to <repo>/logs)")
    parser.add_argument("--limit", type=int, help="Limit number of sweep points for dry runs")
    parser.add_argument("--dry-run", action="store_true", help="Do not execute runs; log planned points only")
    parser.add_argument(
        "--state-file",
        help="Checkpoint path for stop/resume (defaults to <logs>/sweeps/<config>.state)",
    )
    parser.add_argument(
        "--resume",
        dest="resume",
        action="store_true",
        default=True,
        help="Resume from checkpoint when present (use --no-resume to start fresh)",
    )
    parser.add_argument("--no-resume", dest="resume", action="store_false")
    return parser


def _plan(config: SweepConfig, *, logs_dir: Optional[str], limit: Optional[int]) -> int:
    summaries: list[RunSummary] = []
    for point in iter_points(config):
        if limit is not None and point.index >= limit:
            break
        summaries.append(
            _summary_for_point(
                config,
                point_index=point.index,
                params=point.params,
            )
        )

    append_run_summaries(summaries, repo_root=_logs_root(logs_dir))
    return len(summaries)


def _execute(
    config: SweepConfig,
    *,
    logs_dir: Optional[str],
    limit: Optional[int],
    state_file: Optional[str],
    resume: bool,
) -> tuple[int, int, Path]:
    checkpoint = _state_path(config, logs_dir=logs_dir, state_file=state_file)
    last_completed = _load_checkpoint(checkpoint, resume=resume)
    processed = 0
    failures = 0
    for point in iter_points(config):
        if limit is not None and point.index >= limit:
            break
        if point.index <= last_completed:
            continue

        start = time.perf_counter()
        result = _execute_point(
            config, point_index=point.index, params=point.params, logs_dir=logs_dir
        )
        duration_ms = (time.perf_counter() - start) * 1000.0
        status = "OK" if result.exit_code == 0 else "FAILED"
        if result.exit_code != 0:
            failures += 1

        extras = {"exit_code": result.exit_code}
        if result.extras:
            extras.update(result.extras)
        summary = _summary_for_point(
            config,
            point_index=point.index,
            params=point.params,
            status=status,
            runtime_ms=duration_ms,
            notes=result.message or "",
            extras=extras,
        )
        append_run_summaries([summary], repo_root=_logs_root(logs_dir))
        _persist_checkpoint(checkpoint, point.index)
        processed += 1

    return processed, failures, checkpoint


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    config = load_sweep_config(args.config)
    if args.dry_run:
        total_points = _plan(config, logs_dir=args.logs_dir, limit=args.limit)
        sys.stdout.write(
            f"Planned {total_points} sweep points for {config.name} (kind={config.kind}).\n"
            "Use --dry-run to verify configs before execution.\n"
        )
        return

    processed, failures, checkpoint = _execute(
        config,
        logs_dir=args.logs_dir,
        limit=args.limit,
        state_file=args.state_file,
        resume=args.resume,
    )
    sys.stdout.write(
        "Executed {processed} sweep points for {name} (kind={kind}); failures={failures}.\n"
        "Checkpoint: {checkpoint}\n".format(
            processed=processed,
            name=config.name,
            kind=config.kind,
            failures=failures,
            checkpoint=checkpoint,
        )
    )
    raise SystemExit(0 if failures == 0 else 1)


if __name__ == "__main__":  # pragma: no cover - CLI execution
    main()

