"""Simple CLI entrypoints for Phase 3 introspection commands (SPEC-006 P3.2.4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from config import load_run_session_config, load_scenario_registry
from core.serialization import (
    serialize_apx_manifest,
    serialize_loom_p_block,
    serialize_nap_envelope,
    serialize_session_run,
    serialize_umx_tick_ledger,
    serialize_uledger_entry,
)
from gate import run_session
from ops import build_introspection_view
from ops.snapshots import (
    DEFAULT_SNAPSHOT_DIR,
    compare_snapshots,
    render_snapshot_diffs,
    write_snapshot,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCENARIO_REGISTRY = REPO_ROOT / "docs/fixtures/scenarios/scenario_registry.json"


def _load_session_config(*, run_config: Optional[str], scenario: str, registry: Path):
    if run_config:
        return load_run_session_config(Path(run_config))

    scenario_registry = load_scenario_registry(registry)
    try:
        entry = scenario_registry.get(scenario)
    except KeyError as exc:
        raise SystemExit(f"Unknown run-id or scenario id '{scenario}'") from exc

    config_path = (registry.parent / entry.run_config_path).resolve()
    return load_run_session_config(config_path)


def _json_print(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, indent=2))
    sys.stdout.write("\n")


def _default_snapshot_output(target: str, output: Optional[str]) -> Path:
    if output:
        return Path(output)
    return DEFAULT_SNAPSHOT_DIR / f"{target}_run_snapshot.json"


def _build_view(args: argparse.Namespace):
    registry_path = Path(args.registry or DEFAULT_SCENARIO_REGISTRY)
    session_config = _load_session_config(
        run_config=args.run_config, scenario=args.target, registry=registry_path
    )
    session = run_session(session_config)
    return build_introspection_view(session)


def _inspect_command(args: argparse.Namespace) -> None:
    view = _build_view(args)
    payload: Dict[str, Any] = {}

    if args.summary or (args.tick is None and args.window is None):
        payload["summary"] = {
            "gid": view.gid,
            "run_id": view.run_id,
            "total_ticks": view.total_ticks,
            "window_ids": list(view.window_ids),
            "nap_envelopes": len(view.envelopes),
            "uledger_entries": len(view.uledger_by_tick),
        }

    if args.tick is not None:
        ledger = view.get_umx_ledger(args.tick)
        p_block = view.get_loom_p_block(args.tick)
        envelopes = view.get_nap_envelopes(tick=args.tick)
        payload["tick"] = {
            "tick": args.tick,
            "ledger": serialize_umx_tick_ledger(ledger),
            "p_block": serialize_loom_p_block(p_block),
            "nap_envelopes": [serialize_nap_envelope(env) for env in envelopes],
        }

    if args.window is not None:
        manifest = view.get_apx_manifest(args.window)
        payload["window"] = {
            "window_id": args.window,
            "manifest": serialize_apx_manifest(manifest),
        }

    _json_print(payload)


def _snapshot_generate_command(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry or DEFAULT_SCENARIO_REGISTRY)
    output_path = _default_snapshot_output(args.target, args.output)

    session_config = _load_session_config(
        run_config=args.run_config, scenario=args.target, registry=registry_path
    )
    result = run_session(session_config)
    write_snapshot(serialize_session_run(result), output_path)
    sys.stdout.write(f"Wrote snapshot to {output_path}\n")


def _snapshot_compare_command(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry or DEFAULT_SCENARIO_REGISTRY)
    baseline_path = Path(args.baseline)

    candidate_path = Path(args.candidate) if args.candidate else None
    run_config = Path(args.run_config) if args.run_config else None

    diffs, candidate = compare_snapshots(
        baseline_path=baseline_path,
        candidate_path=candidate_path,
        scenario=args.target if not run_config and not candidate_path else None,
        run_config=run_config,
        registry_path=registry_path if not run_config and not candidate_path else None,
        max_diffs=args.max_diffs,
    )

    if args.output:
        write_snapshot(candidate, Path(args.output))

    if diffs:
        sys.stdout.write(render_snapshot_diffs(diffs) + "\n")
        raise SystemExit(1)

    sys.stdout.write("Snapshots match\n")


def _show_ledger_command(args: argparse.Namespace) -> None:
    view = _build_view(args)
    ordered_ticks = sorted(view.uledger_by_tick.keys())
    entries = [view.get_uledger_entry(tick) for tick in ordered_ticks]
    payload = [serialize_uledger_entry(entry) for entry in entries]
    _json_print({"ledger": payload})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Aether introspection CLI")
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "target",
        help="Run id or scenario id. Defaults to scenario registry lookup unless --run-config is provided.",
    )
    parent.add_argument(
        "--registry",
        help="Scenario registry path (defaults to docs/fixtures/scenarios/scenario_registry.json)",
    )
    parent.add_argument(
        "--run-config",
        help="Optional RunConfig JSON path (overrides scenario registry lookup).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect", help="Inspect run artefacts", parents=[parent]
    )
    inspect_parser.add_argument("--summary", action="store_true", help="Print run summary")
    inspect_parser.add_argument("--tick", type=int, help="Inspect artefacts for a specific tick")
    inspect_parser.add_argument("--window", help="Inspect artefacts for a specific window id")
    inspect_parser.set_defaults(func=_inspect_command)

    ledger_parser = subparsers.add_parser(
        "show-ledger", help="Print U-ledger entries", parents=[parent]
    )
    ledger_parser.set_defaults(func=_show_ledger_command)

    snapshot_parent = argparse.ArgumentParser(add_help=False)
    snapshot_parent.add_argument(
        "--candidate",
        help="Optional candidate snapshot path (compare only).",
    )
    snapshot_parent.add_argument(
        "--output", help="Optional output path for generated or candidate snapshots."
    )
    snapshot_parent.add_argument(
        "--max-diffs",
        type=int,
        default=50,
        help="Maximum differences to report when comparing snapshots.",
    )

    snapshot_parser = subparsers.add_parser(
        "snapshot", help="Snapshot management tools"
    )
    snapshot_subparsers = snapshot_parser.add_subparsers(dest="snapshot_command", required=True)

    snapshot_gen = snapshot_subparsers.add_parser(
        "generate",
        help="Generate a snapshot for a scenario or run-config",
        parents=[parent],
    )
    snapshot_gen.add_argument(
        "--output", help="Output path (defaults to tests/snapshots/<target>_run_snapshot.json)"
    )
    snapshot_gen.set_defaults(func=_snapshot_generate_command)

    snapshot_cmp = snapshot_subparsers.add_parser(
        "compare",
        help="Compare a baseline snapshot with a candidate or fresh run",
        parents=[parent, snapshot_parent],
    )
    snapshot_cmp.add_argument(
        "--baseline",
        required=True,
        help="Baseline snapshot JSON path",
    )
    snapshot_cmp.set_defaults(func=_snapshot_compare_command)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
