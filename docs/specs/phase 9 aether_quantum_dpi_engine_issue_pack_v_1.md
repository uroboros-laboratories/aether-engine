# Aether Quantum DPI & Engine — Issue Pack v1

This issue pack defines concrete work items for implementing and validating the Quantum DPI, base engine heroes, run-sheet logging, sweeps, and the one-shot hero-suite orchestration (including comparison to base engine sweeps).

Intended audience: devs integrating and hardening the Aether engine repo (v0.08.x).

Assumed repo root (example on Windows):

- `C:\Users\bjsti\Desktop\aether-engine-main 0.08.0\aether-engine-main`
- Commands are typically run from `...\aether-engine-main\src`.

---

## EPIC 1 — Quantum DPI CLI Hero Tests

**Goal:** Make the Quantum DPI CLI reliable and visible, with clear hero commands and expected outputs.

### Issue 1.1 — Wire up `dpi_quantum` CLI entrypoint

**Scope:**

- Ensure `python -m dpi_quantum --help`:
  - exits with status code 0,
  - prints a clear header (e.g. `Quantum DPI CLI`),
  - lists subcommands at minimum: `ingest`, `simulate`, `experiment`, `summarize`.

**Acceptance criteria:**

- Running `python -m dpi_quantum --help` from `src` succeeds with exit code 0.
- Help text shows a description and the required subcommands.
- Each subcommand has its own help text accessible via `python -m dpi_quantum <subcommand> --help`.

---

### Issue 1.2 — Simulation Hero (Bell → TBP)

**Scope:**

- Implement/verify the `simulate` subcommand for a Bell-state preset:
  - `--circuit bell`
  - `--qubits 2`
  - `--layers 1`
- Support output arguments:
  - `--output <path>` for TBP JSON.
  - `--pfna-output <path>` for PFNA payload JSON.
- Print TBP parameters and fidelity metrics in console output.

**Reference command (example):**

```bash
python -m dpi_quantum simulate \
  --circuit bell \
  --qubits 2 \
  --layers 1 \
  --output ../tmp/bell_q2_tbp.json \
  --pfna-output ../tmp/bell_q2_pfna.json
```

**Acceptance criteria:**

- Command runs with exit code 0.
- Console output includes at least:
  - A completion line (`simulation completed`).
  - Circuit description (`circuit: bell(qubits=2,layers=1)`).
  - TBP parameters (`eta=... P=...`).
  - Masses/residuals summary.
  - Fidelity metrics (`fidelity: prob_l1=... amp_l2=...`).
- Files at `--output` and `--pfna-output` are created and contain valid JSON with TBP/PFNA data.

---

### Issue 1.3 — Experiment Hero (Spin Chain, DPI-only)

**Scope:**

- Implement/verify the `experiment` subcommand for a spin-chain preset:
  - `--name spin_chain`.
  - Accepts `--qubits`, `--ticks`, `--episodes`.
- Auto-tune η and P as per spec (or confirm implementation matches spec).
- Print TBP + fidelity metrics.

**Reference command (example):**

```bash
python -m dpi_quantum experiment \
  --name spin_chain \
  --qubits 4 \
  --ticks 4 \
  --episodes 1
```

**Acceptance criteria:**

- Command runs with exit code 0.
- Console output includes:
  - `experiment completed`.
  - `experiment: spin_chain(q=4,ticks=4,episodes=1)` (or equivalent).
  - TBP stats (`eta`, `P`, masses, residuals).
  - Fidelity metrics.
  - Auto-tune notes for η/P.

---

### Issue 1.4 — Ingest + Gate Replay Hero (DPI + Base Engine)

**Scope:**

- Implement/verify `dpi_quantum ingest` such that it:
  - Builds TBP from an internal or provided quantum state.
  - Produces PFNA outputs when `--pfna-output` is specified.
  - Performs PFNA replay and Gate PFNA replay.
- Gate PFNA replay must invoke `run_cmp0_tick_loop` and exercise GF01 + Loom for at least one tick.

**Reference command (example):**

```bash
python -m dpi_quantum ingest \
  --qubits 4 \
  --phase-bins 32 \
  --auto-tune \
  --pfna-output ../tmp/ingest_q4_pfna.json \
  --pfna-tick 0 \
  --run-id ingest_q4_hero \
  --gid GATE
```

**Acceptance criteria:**

- Command runs with exit code 0.
- Console output includes:
  - `ingestion completed`.
  - TBP stats (η, P, masses, residuals).
  - Fidelity metrics.
  - `pfna_replay` summary.
  - `gate_replay` summary, confirming `run_cmp0_tick_loop` + Loom executed.
- PFNA output file exists and contains valid JSON.

---

## EPIC 2 — Base Engine GF01 Hero Tests

**Goal:** Prove the base engine (GF01) runs correctly, generates snapshots, and matches a golden reference.

### Issue 2.1 — GF01 Snapshot Generate Hero

**Scope:**

- Implement/verify `cli snapshot generate gf01` such that it:
  - Resolves GF01 scenario from the scenario registry.
  - Loads the GF01 config.
  - Runs `gate.run_session(...)` through the tick loop.
  - Writes a snapshot JSON containing UMX, Loom, NAP, manifests, etc.

**Reference command (example):**

```bash
python -m cli snapshot generate gf01 \
  --output ../tmp/gf01_run_snapshot_hero.json
```

**Acceptance criteria:**

- Command runs with exit code 0.
- Console confirms snapshot creation.
- Output file exists and is valid JSON with at least:
  - `run_id`.
  - `ticks_total`.
  - Loom blocks / U-ledger / manifests (sanity-check structure).

---

### Issue 2.2 — GF01 Snapshot Compare vs Golden

**Scope:**

- Implement/verify `cli snapshot compare gf01` such that it:
  - Uses the GF01 scenario.
  - Compares a run snapshot against `tests/snapshots/gf01_run_snapshot.json` (or configured baseline).
  - Reports differences up to a configurable `max_diffs`.

**Reference command (example):**

```bash
python -m cli snapshot compare gf01 \
  --baseline tests/snapshots/gf01_run_snapshot.json
```

**Acceptance criteria:**

- Command runs with exit code 0 when engine behaviour matches the baseline.
- Console output indicates either:
  - no diffs, or
  - specific diffs if the baseline is not matched.
- Any unexpected deviations from the golden snapshot are clearly surfaced.

---

## EPIC 3 — Run Sheet Logging Infrastructure

**Goal:** Ensure that every relevant CLI run (heroes and sweeps) appends a structured row to run sheets for later analysis.

### Issue 3.1 — Define `RunSummary` struct in code

**Scope:**

- Implement a `RunSummary` (or equivalent) data structure matching the v1 run sheet schema (see separate canvas), including at minimum:
  - `run_id`
  - `timestamp`
  - `scenario`
  - `n_qubits`
  - `ticks`
  - `dpi_mode`
  - `loom_mode`
  - `codex_mode`
  - `runtime_total_ms`
  - `status`
  - `loom_p_blocks`
  - `loom_i_blocks`
- Additional fields should be populated where possible (η, P, fidelity, memory, bytes, etc.).

**Acceptance criteria:**

- `RunSummary` is a single, shared representation used by hero commands and sweep commands.
- All required fields are always filled for runs where they make sense.

---

### Issue 3.2 — Append CSV and JSONL Run Sheets

**Scope:**

- Implement logging such that on completion of each relevant run (heroes + sweeps):
  - A `RunSummary` instance is created.
  - One row is appended to:
    - `logs/quantum_runs.csv` (CSV format, v1-lite column subset or full schema).
    - `logs/quantum_runs.jsonl` (one JSON object per line).
- Ensure logging happens for at least:
  - Q3: DPI experiment hero.
  - Q4: Ingest + Gate replay hero.
  - E1/E2: GF01 runs where metrics are meaningful.
  - All sweep runs (see EPIC 4/5).

**Acceptance criteria:**

- Running any hero or sweep command results in new entries in both CSV and JSONL files.
- Logged rows contain consistent, machine-parseable data matching the `RunSummary` schema.

---

## EPIC 4 — Sweep Runner CLI (Ingest, Experiment, Simulation)

**Goal:** Provide a generic sweep runner that executes parameter sweeps and logs results.

### Issue 4.1 — Sweep Config Format

**Scope:**

- Define a simple YAML/JSON config format for sweeps, with fields such as:
  - `name`
  - `scenario`
  - `dpi_mode`
  - `topology_profile`
  - `math_profile`
  - `loom_mode`
  - `codex_mode`
  - Fixed parameters: `ticks`, `episodes`, `shots` (as applicable).
  - `qubits`: either `values: [...]` or `start`/`stop`/`step`.
  - `runs_per_point`.
  - `stop_on`: e.g. `hard_error`, `timeout_ms`.

**Acceptance criteria:**

- At least one example config exists for each of:
  - Ingest / round-trip sweep (C1).
  - Experiment sweep (C2a DPI-only and/or C2b full-stack).
  - Base engine simulation sweep (C3a).
- Configs are well-documented and discoverable in the repo.

---

### Issue 4.2 — Implement `quantum-sweep` CLI Command

**Scope:**

- Implement a CLI command, e.g.:

```bash
python -m operator_service quantum-sweep --config <path>
```

- Behaviour:
  - Load sweep config.
  - Build a grid of parameter points (qubits, ticks, etc.).
  - For each point:
    - Run the appropriate hero-like command or job.
    - Capture outputs into `RunSummary`.
    - Append to run sheets.
  - Honour `stop_on` settings (stop on hard errors / timeouts if configured).
  - Optionally support `--resume` to skip already-logged points.

**Acceptance criteria:**

- Running `quantum-sweep` with sample configs executes all defined parameter points.
- Each run results in a `RunSummary` logged to CSV/JSONL.
- Console prints progress and a final summary (counts of OK/ERROR and simple stats).

---

### Issue 4.3 — Implement Sweep Families C1–C3

**Scope:**

- Provide configs and wiring for the following sweep families (aligned with the hero patterns):

1. **C1 — Ingest / Round-trip Sweep (Static, Single Tick)**
   - Mode: `ingest` via `dpi_quantum`.
   - Sweep over `N_qubits` and `loom_mode`.
   - Single GF01 tick via `run_cmp0_tick_loop`.

2. **C2 — Experiment Sweep (DPI-only and/or Full-stack)**
   - DPI-only: `dpi_quantum experiment` with `spin_chain` and varying `N_qubits` (and optionally ticks).
   - Full-stack: corresponding jobs through Operator Service with `run_engine=true`.

3. **C3a — Base Engine Simulation Sweep**
   - GF01 runs with varying `ticks_total` (e.g. 20, 50, 100, 200).

**Acceptance criteria:**

- Each sweep config runs successfully through `quantum-sweep`.
- All runs are logged in run sheets with correct modes (`dpi_mode`, `loom_mode`, etc.).

---

## EPIC 5 — Emulation & Comparison Sweeps (v1)

**Goal:** Compare DPI-only "oracle" runs to full-stack behaviour and track emulation quality.

### Issue 5.1 — Oracle vs Emulation Comparison Helper

**Scope:**

- Implement a helper that, for a given logical config (circuit, `N_qubits`, depth/ticks):
  - Runs a DPI-only oracle path (e.g. `simulate`/`experiment` with `run_engine=false`) to obtain reference observables/distributions.
  - Runs a full-stack path through Gate/UMX/Loom/Codex.
  - Computes error metrics (e.g. prob_l1, amp_l2, total variation distance) between oracle and emulation outputs.
  - Sets an `emulation_ok` flag based on configurable tolerances.

**Acceptance criteria:**

- For a simple circuit (e.g. Bell, GHZ), helper returns error metrics and `emulation_ok=true` when errors are below threshold.
- Helper output is attached to `RunSummary` for emulation sweeps.

---

### Issue 5.2 — Emulation Sweep Configs

**Scope:**

- Provide sweep configs that:
  - Iterate over small circuits (Bell, GHZ, spin_chain) and `N_qubits`.
  - For each point, run oracle + emulation and log comparison metrics.

**Acceptance criteria:**

- Running emulation sweeps via `quantum-sweep` produces:
  - Paired runs per config point.
  - Logged error metrics and `emulation_ok` flags in run sheets.

---

## EPIC 6 — Hero Suite Orchestrator (Single Command, Full Sweep + Base Engine Comparison)

**Goal:** Provide a **single CLI command** that runs all hero tests and sweeps, logs everything, and includes a comparison between base engine sweeps and DPI+engine sweeps.

### Issue 6.1 — Define `hero-suite` CLI Entrypoint

**Scope:**

- Add a top-level command, e.g.:

```bash
python -m cli hero-suite --mode full-sweep
```

  or

```bash
python -m operator_service hero-suite --mode full-sweep
```

- `--mode` must support at least:
  - `full-sweep` (required),
  - optional lighter modes (e.g. `smoke`).

**Acceptance criteria:**

- `hero-suite --help` exits with code 0 and documents the `--mode` flag.
- `--mode full-sweep` is clearly described as “run all hero tests and all configured sweeps, then summarise and compare base engine vs DPI+engine”.

---

### Issue 6.2 — Implement `hero-suite --mode full-sweep`

**Scope:**

When invoked as:

```bash
python -m <entry_module> hero-suite --mode full-sweep
```

it must:

1. **Run all hero tests once (in defined order):**
   - Q1: `dpi_quantum --help`.
   - Q2: `dpi_quantum simulate ...` (Bell).
   - Q3: `dpi_quantum experiment ...` (spin_chain).
   - Q4: `dpi_quantum ingest ...` (ingest + gate replay).
   - E1: `cli snapshot generate gf01 ...`.
   - E2: `cli snapshot compare gf01 --baseline ...`.

2. **Run all configured sweeps once:**
   - Ingest / round-trip sweep (C1).
   - Experiment sweeps (C2a DPI-only and/or C2b full-stack).
   - Base engine simulation sweep (C3a).
   - Any implemented emulation sweeps (C4).

3. **Log all runs:**
   - For every run (hero or sweep), create a `RunSummary` and append to:
     - `logs/quantum_runs.csv`.
     - `logs/quantum_runs.jsonl`.

4. **Include base engine vs DPI+engine comparison:**
   - Ensure that for each `ticks_total` used in DPI full-stack experiment sweeps (C2b), there is at least one base engine-only run (C3a) with the same `ticks_total` and topology in this suite execution.
   - Compute per-`ticks_total` averages for:
     - `runtime_total_ms` and `loom_bytes` (or P/I-block counts) for:
       - engine-only runs (`dpi_mode = engine-sim` or equivalent), and
       - DPI+engine runs (`dpi_mode = experiment` / `dpi-fullstack`).
   - Print a summary block such as:

```text
Base engine vs DPI+engine comparison (per ticks_total):

  ticks=40:
    engine-only:  runtime_mean=820 ms, loom_bytes_mean=96 KB (n=3)
    dpi+engine:   runtime_mean=1360 ms, loom_bytes_mean=128 KB (n=3)
```

5. **Produce a final suite summary:**
   - List hero test results (Q1–Q4, E1–E2: OK/FAIL).
   - List sweep results per config (OK/ERROR counts).
   - Show base engine vs DPI+engine comparison block.
   - Provide an overall `PASS` / `FAIL` line.

6. **Exit code semantics:**
   - Exit code 0 **only if**:
     - all hero tests pass, and
     - all sweep runs complete with `status=OK`, and
     - base engine vs DPI+engine comparisons are computed successfully.
   - Exit code non-zero if any hero test fails, any sweep run has `status != OK`, or comparison pairing fails due to missing base engine runs.

**Acceptance criteria:**

- Running the single command in a correctly configured repo:

```bash
python -m <entry_module> hero-suite --mode full-sweep
```

  results in:
  - All hero tests and sweeps executed as described.
  - Every run logged to CSV/JSONL via `RunSummary`.
  - A final summary printed with:
    - hero test statuses,
    - sweep summaries,
    - base engine vs DPI+engine comparison,
    - overall PASS/FAIL.
  - Exit code 0 only when everything in the suite is green.

---

## Global Completion Condition

For this issue pack to be considered **complete**:

1. All EPIC 1 and EPIC 2 hero issues pass when run directly.
2. Run-sheet logging (EPIC 3) captures all hero and sweep runs.
3. Sweep runner (EPIC 4/5) executes the defined configs successfully.
4. A single CLI command (`hero-suite --mode full-sweep`) orchestrates:
   - all hero tests,
   - all sweeps,
   - base engine vs DPI+engine comparisons,
   - logging into run sheets,
   - and returns a correct PASS/FAIL status via exit code.

