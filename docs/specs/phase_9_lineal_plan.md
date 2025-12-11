# Phase 9 Lineal Implementation Plan

This plan sequences the issues from the **Phase 9 Aether Quantum DPI & Engine issue pack** into a single execution path. Each step references the originating epic/issue so progress can be tracked end-to-end while keeping the surface area approachable for new contributors.

## Pre-flight and validation
1. **Repo + CLI smoke (EPIC 1 pre-flight)** — Confirm existing `dpi_quantum` and `cli` entrypoints run with `--help` from `src/` and note current argument coverage.
2. **Fixture + snapshot audit (EPIC 2 pre-flight)** — Inspect `tests/snapshots/gf01_run_snapshot.json` and fixture directories to ensure baseline assets exist and note missing coverage for Phase 9 heroes.

## EPIC 1 — Quantum DPI CLI heroes
3. **Entrypoint wiring (Issue 1.1)** — Ensure `python -m dpi_quantum --help` advertises `ingest`, `simulate`, `experiment`, and `summarize` with clear headers and exit code 0.
4. **Bell simulation hero (Issue 1.2)** — Implement `dpi_quantum simulate --circuit bell --qubits 2 --layers 1` to emit TBP + PFNA outputs, fidelity metrics, and completion banners.
5. **Spin-chain experiment hero (Issue 1.3)** — Implement `dpi_quantum experiment --name spin_chain ...` with η/P auto-tuning, TBP/fidelity metrics, and run-id aware summaries.
6. **Ingest + gate replay hero (Issue 1.4)** — Wire `dpi_quantum ingest` to produce PFNA outputs, run `run_cmp0_tick_loop`, and print PFNA + gate replay summaries.

## EPIC 2 — Base engine GF01 heroes
7. **GF01 snapshot generate (Issue 2.1)** — Ensure `python -m cli snapshot generate gf01` resolves the scenario, runs the tick loop, and writes a full snapshot artifact.
8. **GF01 snapshot compare (Issue 2.2)** — Implement `python -m cli snapshot compare gf01 --baseline ...` to diff current runs against the golden snapshot with clear pass/fail messaging.

## EPIC 3 — Run sheet logging
9. **RunSummary struct (Issue 3.1)** — Add a shared `RunSummary` data class capturing run metadata (ids, modes, counts, fidelity, loom stats, timings) for heroes and sweeps.
10. **CSV/JSONL appends (Issue 3.2)** — Create helpers that append `RunSummary` rows to `logs/quantum_runs.csv` and `logs/quantum_runs.jsonl` after each hero/sweep execution.

## EPIC 4 — Sweep runner CLI
11. **Sweep config format (Issue 4.1)** — Define YAML/JSON sweep schemas plus examples for ingest (C1), experiment (C2), and base-engine simulations (C3a).
12. **`quantum-sweep` command (Issue 4.2)** — Implement CLI to load configs, run parameter grids, honour stop/resume rules, and emit `RunSummary` entries per point.
13. **Sweep families C1–C3 (Issue 4.3)** — Provide runnable configs and wiring for ingest, experiment, and base-engine sweeps using the shared sweep runner.

Status: Sweep config loader, examples, and logging scaffolds are in place (`quantum_sweep` CLI). DPI hero sweeps execute with checkpointed stop/resume; GF01 snapshot sweeps are wired via the same runner, and emulation comparisons now land metrics + `emulation_ok` flags across Bell, GHZ, and spin-chain presets. A hero-suite CLI orchestrates heroes + sweeps with optional point limits (entry: `python -m cli hero-suite --mode full-sweep`). Base-engine GF01 sweeps now capture snapshots and a `gf01_compare` kind diffs them against the golden baseline so the hero-suite can fail fast on regressions. The suite summarizes newly appended run-sheet entries (status mix, emulation tolerance hits, GF01 diff counts) after every run, fails the suite when new run-sheet entries show emulation drift or GF01 diffs, surfaces the max L1/L2 gaps alongside the configured tolerances so failures are easier to triage, filters run-sheet loads by suite start time, reports how many malformed vs stale/undated rows were skipped so truncated logs do not silently skew health checks, enforces scenario coverage by flagging missing hero/sweep entries when they fail to append to the run sheet, and can now reset run sheets up front (`--fresh-run-sheet`) so CI/clean runs avoid stale data before filtering kicks in. The hero-suite now prints the exact run-sheet path it will write before launching heroes/sweeps; Phase 9 is complete and ready for handoff—run `python -m cli hero-suite --mode full-sweep --fresh-run-sheet` for a clean validation pass when dependencies are available.

## EPIC 5 — Emulation & comparison sweeps
14. **Oracle vs emulation helper (Issue 5.1)** — Build helper to pair DPI-only oracle runs with full-stack runs and compute error metrics + `emulation_ok` flag.
15. **Emulation sweep configs (Issue 5.2)** — Add configs that iterate Bell/GHZ/spin_chain circuits across qubit counts and record comparison metrics into run sheets.

## EPIC 6 — Hero-suite orchestrator
16. **Entrypoint docs (Issue 6.1)** — Document and expose `hero-suite --mode full-sweep` (or equivalent module) with clear help text.
17. **End-to-end orchestration (Issue 6.2)** — Implement the command to run all heroes, sweeps, comparisons, and logging; compute base-engine vs DPI+engine summaries; exit non-zero on failures.

## Exit + validation
18. **Regression + hero sweep (Global completion)** — Execute all hero commands, sweeps, and the hero-suite end-to-end; confirm run sheets populated and comparisons computed; update the Phase 9 build report with outcomes and remaining gaps.
