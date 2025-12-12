# Phase 9 CLI run sheet (novice edition)

This page lists the Phase 9 console commands in plain language and shows where their run-sheet logs land. Run everything from the repo root unless noted.

## Quick setup
- Install the light dependencies (PyYAML for YAML sweeps, pytest for test runs):
  - `python -m pip install -r requirements.txt`
- Run-sheet output defaults to `logs/quantum_runs.jsonl` and `logs/quantum_runs.csv` under the repo. Add `--logs-dir <path>` to any CLI below to redirect.
- Use `--fresh-run-sheet` on the hero-suite to truncate stale rows before a run.

## Command cheat sheet
### Quantum DPI CLI (`python -m dpi_quantum`)
- `python -m dpi_quantum ingest --input <payload.json> --qubits <n> --phase-bins <P> --eta <η>` — parse a TBP payload, auto-tune or accept explicit η/P, and log fidelity/ingestion results. Optional: `--pfna-output` to emit a PFNA V0 bundle, `--max-prob-l1/--max-amp-l2` to fail on fidelity drift.
- `python -m dpi_quantum simulate --circuit bell --qubits 2 --layers 1` — generate a preset circuit statevector, optionally emit TBP/PFNA, and log to the run sheet. Add `--run-engine` to flow into the engine runtime.
- `python -m dpi_quantum experiment --name spin_chain --qubits 4 --ticks 4 --episodes 1` — run an experiment preset (spin chain by default) and emit run-sheet telemetry, with the same TBP/PFNA/fidelity options as ingest/simulate.
- `python -m dpi_quantum summarize --run-id <id> | --job-id <dpi_job>` — look up prior DPI runs or jobs from `docs/fixtures/history/history.jsonl` and print a human summary (accepts `--diagnostics-path` to change the history source).

### Introspection CLI (`python -m cli`)
- `python -m cli inspect gf01 --summary` — print a snapshot-style view of a scenario (or run-config), with `--tick` or `--window` to drill into specific ledgers/APX manifests.
- `python -m cli show-ledger gf01` — print the U-ledger entries for a scenario/run.
- `python -m cli snapshot generate gf01 --output tests/snapshots/gf01_run_snapshot.json` — run the GF01 scenario and write a snapshot to compare later; appends a `SNAPSHOT_GENERATED` row to the run sheet.
- `python -m cli snapshot compare gf01 --baseline tests/snapshots/gf01_run_snapshot.json` — compare a baseline snapshot with a candidate or fresh run (supports `--candidate` or `--run-config`); logs `PASS/FAIL` to the run sheet.
- `python -m cli hero-suite --mode full-sweep --fresh-run-sheet` — run the curated hero commands plus all sweeps, summarise new run-sheet entries (status mix, emulation tolerances, GF01 diffs), enforce scenario coverage, and exit non-zero on any failure. Use `--sweep-limit 1` for a quick pass or `--mode smoke` to skip sweeps.

### Sweep runner (`python -m quantum_sweep <config>`)
- `python -m quantum_sweep docs/fixtures/sweeps/c2_experiment.json --dry-run --limit 2` — load a JSON/YAML sweep config, expand the grid, and log planned runs without executing.
- `python -m quantum_sweep docs/fixtures/sweeps/c4_emulation.json --limit 1 --no-resume` — execute sweep points (DPI heroes, snapshot generate/compare, emulation compares, GF01 runs), checkpoint progress, and append run summaries.

## One-line “run everything” command
Run the full test suite first, then the hero + sweep orchestrator, truncating stale run-sheet entries before logging new results. If you see `No module named pytest`, install the dependencies first with `python -m pip install -r requirements.txt` (or `py -m pip ...` on Windows) to make sure `pytest` is available on your active interpreter:

```bash
python -m pytest && python -m cli hero-suite --mode full-sweep --fresh-run-sheet
```
