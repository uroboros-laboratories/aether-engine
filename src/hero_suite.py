"""Hero-suite orchestrator for Phase 9 EPIC 6.

Runs a curated set of hero commands and sweep configs, reporting a
pass/fail summary so contributors can exercise the full surface from a
single entrypoint.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Mapping, Optional

from ops.run_summaries import ensure_logs_dir

REPO_ROOT = Path(__file__).resolve().parent.parent


def _logs_root(logs_dir: Optional[str]) -> Path:
    return Path(logs_dir).expanduser().resolve() if logs_dir else REPO_ROOT


def _prepare_run_sheet(logs_dir: Optional[str], *, fresh: bool) -> Path:
    logs_path = ensure_logs_dir(_logs_root(logs_dir))
    if fresh:
        for name in ("quantum_runs.jsonl", "quantum_runs.csv"):
            target = logs_path / name
            target.unlink(missing_ok=True)
        sys.stdout.write(f"[hero-suite] Reset run sheet at {logs_path}\n")
    return logs_path


@dataclass
class StepResult:
    label: str
    ok: bool
    exit_code: int
    output: str


@dataclass
class RunSheetLoadResult:
    """Run-sheet rows captured for this suite invocation."""

    entries: list[Mapping[str, object]]
    malformed_rows: int = 0
    stale_rows: int = 0


def _run_step(label: str, cmd: List[str]) -> StepResult:
    sys.stdout.write(f"[hero-suite] {label}: {' '.join(cmd)}\n")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    combined_output = (proc.stdout or "") + (proc.stderr or "")
    if combined_output:
        sys.stdout.write(combined_output)
    return StepResult(label=label, ok=proc.returncode == 0, exit_code=proc.returncode, output=combined_output)


def _hero_commands(logs_dir: Optional[str]) -> list[list[str]]:
    logs_flag = ["--logs-dir", logs_dir] if logs_dir else []
    baseline_snapshot = str(REPO_ROOT / "tests/snapshots/gf01_run_snapshot.json")
    return [
        [sys.executable, "-m", "dpi_quantum", "--help"],
        [sys.executable, "-m", "dpi_quantum", *logs_flag, "simulate", "--circuit", "bell", "--qubits", "2", "--layers", "1"],
        [sys.executable, "-m", "dpi_quantum", *logs_flag, "experiment", "--name", "spin_chain", "--qubits", "4", "--ticks", "4", "--episodes", "1"],
        [sys.executable, "-m", "dpi_quantum", *logs_flag, "ingest", "--qubits", "2", "--phase-bins", "32", "--eta", "0.1"],
        [
            sys.executable,
            "-m",
            "cli",
            *logs_flag,
            "snapshot",
            "generate",
            "gf01",
            "--registry",
            str(REPO_ROOT / "docs/fixtures/scenarios/scenario_registry.json"),
        ],
        [
            sys.executable,
            "-m",
            "cli",
            *logs_flag,
            "snapshot",
            "compare",
            "gf01",
            "--baseline",
            baseline_snapshot,
            "--candidate",
            baseline_snapshot,
            "--registry",
            str(REPO_ROOT / "docs/fixtures/scenarios/scenario_registry.json"),
        ],
    ]


def _sweep_commands(logs_dir: Optional[str], limit: Optional[int]) -> list[list[str]]:
    logs_flag = ["--logs-dir", logs_dir] if logs_dir else []
    limit_flag: list[str] = ["--limit", str(limit)] if limit is not None else []
    configs = [
        REPO_ROOT / "docs/fixtures/sweeps/c1_ingest.json",
        REPO_ROOT / "docs/fixtures/sweeps/c2_experiment.json",
        REPO_ROOT / "docs/fixtures/sweeps/c3_snapshot_generate.json",
        REPO_ROOT / "docs/fixtures/sweeps/c3_snapshot_compare.json",
        REPO_ROOT / "docs/fixtures/sweeps/c4_emulation.json",
        REPO_ROOT / "docs/fixtures/sweeps/c4_emulation_ghz.json",
        REPO_ROOT / "docs/fixtures/sweeps/c4_emulation_spin_chain.json",
        REPO_ROOT / "docs/fixtures/sweeps/c5_gf01_run.json",
        REPO_ROOT / "docs/fixtures/sweeps/c6_gf01_compare.json",
    ]
    return [
        [sys.executable, "-m", "quantum_sweep", str(path), *logs_flag, *limit_flag, "--no-resume"]
        for path in configs
    ]


def _load_run_sheet(
    logs_dir: Optional[str], *, since: Optional[datetime] = None
) -> RunSheetLoadResult:
    """Load JSONL run-sheet entries newer than ``since`` and track skipped rows."""

    run_sheet_dir = ensure_logs_dir(_logs_root(logs_dir))
    run_sheet_path = run_sheet_dir / "quantum_runs.jsonl"
    if not run_sheet_path.exists():
        return RunSheetLoadResult(entries=[])

    entries: list[Mapping[str, object]] = []
    malformed_rows = 0
    stale_rows = 0
    for line in run_sheet_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            malformed_rows += 1
            continue

        if since:
            ts_raw = payload.get("timestamp")
            try:
                ts_val = datetime.fromisoformat(ts_raw) if ts_raw else None
            except (TypeError, ValueError):
                ts_val = None
            if ts_val is None or ts_val < since:
                stale_rows += 1
                continue

        entries.append(payload)

    return RunSheetLoadResult(
        entries=entries, malformed_rows=malformed_rows, stale_rows=stale_rows
    )


def _summarize_run_sheet(
    load_result: RunSheetLoadResult,
    *,
    expected_scenarios: Optional[set[str]] = None,
) -> bool:
    """Emit a human-friendly summary of new run-sheet entries and signal health."""

    entries = load_result.entries
    if load_result.malformed_rows or load_result.stale_rows:
        skipped_bits = []
        if load_result.malformed_rows:
            skipped_bits.append(f"{load_result.malformed_rows} malformed rows")
        if load_result.stale_rows:
            skipped_bits.append(
                f"{load_result.stale_rows} stale/undated rows (before suite start)"
            )
        sys.stdout.write(f"Run-sheet note: skipped {', '.join(skipped_bits)} while loading.\n")

    if not entries:
        sys.stdout.write("Run-sheet summary: no new entries captured.\n")
        return True

    ok = True
    sys.stdout.write(f"Run-sheet summary: {len(entries)} new entries\n")
    status_counts = Counter(entry.get("status", "UNKNOWN") for entry in entries)
    for status, count in sorted(status_counts.items()):
        sys.stdout.write(f"  - {status}: {count}\n")

    observed_scenarios = {entry.get("scenario") for entry in entries if entry.get("scenario")}
    if expected_scenarios:
        missing = expected_scenarios - observed_scenarios
        if missing:
            ok = False
            sys.stdout.write("  - Missing expected scenarios:\n")
            for scenario in sorted(missing):
                sys.stdout.write(f"    * {scenario}\n")
        coverage = len(expected_scenarios) - len(missing)
        sys.stdout.write(
            f"  - Scenario coverage: {coverage}/{len(expected_scenarios)} present\n"
        )

    emulation = [
        entry
        for entry in entries
        if isinstance(entry.get("extras"), Mapping) and "emulation_ok" in entry.get("extras", {})
    ]
    if emulation:
        emu_ok = sum(1 for entry in emulation if entry.get("extras", {}).get("emulation_ok"))
        emu_fail = [entry for entry in emulation if not entry.get("extras", {}).get("emulation_ok")]

        prob_gaps = [
            entry.get("extras", {}).get("fidelity_prob_l1")
            for entry in emulation
            if "fidelity_prob_l1" in entry.get("extras", {})
        ]
        prob_tols = [
            entry.get("extras", {}).get("prob_tolerance")
            for entry in emulation
            if "prob_tolerance" in entry.get("extras", {})
        ]
        amp_gaps = [
            entry.get("extras", {}).get("fidelity_amp_l2")
            for entry in emulation
            if "fidelity_amp_l2" in entry.get("extras", {})
        ]
        amp_tols = [
            entry.get("extras", {}).get("amp_tolerance")
            for entry in emulation
            if "amp_tolerance" in entry.get("extras", {})
        ]

        sys.stdout.write(
            f"  - Emulation comparisons: {emu_ok}/{len(emulation)} within tolerance\n"
        )
        if prob_gaps:
            max_prob_gap = max(float(val) for val in prob_gaps)
            prob_tol = max(float(val) for val in prob_tols) if prob_tols else None
            tol_str = f" (tolerance <= {prob_tol})" if prob_tol is not None else ""
            sys.stdout.write(
                f"    * Max probability L1 gap: {max_prob_gap}{tol_str}\n"
            )
        if amp_gaps:
            max_amp_gap = max(float(val) for val in amp_gaps)
            amp_tol = max(float(val) for val in amp_tols) if amp_tols else None
            tol_str = f" (tolerance <= {amp_tol})" if amp_tol is not None else ""
            sys.stdout.write(
                f"    * Max amplitude L2 gap: {max_amp_gap}{tol_str}\n"
            )

        if emu_fail:
            ok = False
            sys.stdout.write("  - Emulation regressions:\n")
            for entry in emu_fail:
                extras = entry.get("extras", {})
                prob_gap = extras.get("fidelity_prob_l1")
                amp_gap = extras.get("fidelity_amp_l2")
                prob_tol = extras.get("prob_tolerance")
                amp_tol = extras.get("amp_tolerance")
                gap_bits = []
                if prob_gap is not None:
                    gap_bits.append(
                        f"prob_gap={prob_gap}" + (f" (tol {prob_tol})" if prob_tol is not None else "")
                    )
                if amp_gap is not None:
                    gap_bits.append(
                        f"amp_gap={amp_gap}" + (f" (tol {amp_tol})" if amp_tol is not None else "")
                    )
                gap_info = "; ".join(gap_bits) if gap_bits else "emulation_ok=False"
                sys.stdout.write(
                    f"    * {entry.get('run_id', 'unknown')} ({entry.get('scenario', 'n/a')}) -> {gap_info}\n"
                )

    gf01_diffs = [
        entry
        for entry in entries
        if "gf01_compare" in str(entry.get("scenario", ""))
        and isinstance(entry.get("extras"), Mapping)
    ]
    if gf01_diffs:
        max_diff = max(int(entry.get("extras", {}).get("diff_count", 0)) for entry in gf01_diffs)
        sys.stdout.write(f"  - GF01 comparisons: max diff_count={max_diff}\n")
        if max_diff > 0:
            ok = False

    ok_statuses = {"OK", "PLANNED", "PASS", "SNAPSHOT_GENERATED"}
    failed = [entry for entry in entries if entry.get("status") not in ok_statuses]
    if failed:
        ok = False
        sys.stdout.write("  - Failed entries:\n")
        for entry in failed:
            sys.stdout.write(
                f"    * {entry.get('run_id', 'unknown')} ({entry.get('scenario', 'n/a')}) -> {entry.get('status')}\n"
            )

    return ok


def _summarize(results: Iterable[StepResult], heading: str) -> tuple[int, int]:
    results_list = list(results)
    ok = sum(1 for result in results_list if result.ok)
    total = len(results_list)
    sys.stdout.write(f"{heading}: {ok}/{total} passed\n")
    for result in results_list:
        sys.stdout.write(f"  - {result.label}: {'OK' if result.ok else f'FAIL (exit={result.exit_code})'}\n")
    return ok, total


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Hero-suite orchestrator")
    parser.add_argument("--mode", choices=["full-sweep", "smoke"], default="full-sweep", help="Suite execution mode")
    parser.add_argument("--logs-dir", help="Override run log directory (defaults to <repo>/logs)")
    parser.add_argument("--sweep-limit", type=int, help="Limit sweep points (helps for CI dry runs)")
    parser.add_argument(
        "--fresh-run-sheet",
        action="store_true",
        help="Truncate run sheets before executing to avoid stale entries",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    logs_path = _prepare_run_sheet(args.logs_dir, fresh=args.fresh_run_sheet)
    sys.stdout.write(
        f"[hero-suite] Logging to {logs_path / 'quantum_runs.jsonl'} (CSV sibling available)\n"
    )

    start_time = datetime.now(timezone.utc)
    sys.stdout.write(f"Running hero-suite mode={args.mode}\n")
    hero_cmds = _hero_commands(args.logs_dir)
    sweep_cmds = _sweep_commands(args.logs_dir, args.sweep_limit if args.mode == "full-sweep" else 1)

    hero_results = [
        _run_step(label=f"Hero {index+1}", cmd=cmd)
        for index, cmd in enumerate(hero_cmds)
    ]

    sweep_results: list[StepResult] = []
    if args.mode == "full-sweep":
        sweep_results = [
            _run_step(label=f"Sweep {index+1}", cmd=cmd)
            for index, cmd in enumerate(sweep_cmds)
        ]
    else:
        sys.stdout.write("Skipping sweeps in smoke mode\n")

    hero_ok, hero_total = _summarize(hero_results, heading="Hero checks")
    sweep_ok, sweep_total = _summarize(sweep_results, heading="Sweep runs") if sweep_results else (0, 0)

    expected_scenarios = {
        "simulate:bell",
        "experiment:spin_chain",
        "ingest:ingest",
        "gf01",
    }
    if args.mode == "full-sweep":
        expected_scenarios.update(
            {
                "sweep:ingest:c1_ingest_eta_sweep",
                "sweep:experiment:spin_chain",
                "sweep:snapshot_generate:gf01",
                "sweep:snapshot_compare:gf01",
                "sweep:emulation_compare:bell",
                "sweep:emulation_compare:ghz_3",
                "sweep:emulation_compare:spin_chain",
                "sweep:gf01_run:gf01_suite",
                "sweep:gf01_compare:gf01",
            }
        )

    load_result = _load_run_sheet(args.logs_dir, since=start_time)
    run_sheet_ok = _summarize_run_sheet(
        load_result,
        expected_scenarios=expected_scenarios,
    )

    overall_pass = (
        hero_ok == hero_total
        and (not sweep_results or sweep_ok == sweep_total)
        and run_sheet_ok
    )
    sys.stdout.write(f"Overall result: {'PASS' if overall_pass else 'FAIL'}\n")
    raise SystemExit(0 if overall_pass else 1)


if __name__ == "__main__":  # pragma: no cover - CLI execution
    main()

