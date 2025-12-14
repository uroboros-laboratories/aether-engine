# Phase 9.1 — Quantum DPI Engine Wiring Gap & Fix Plan (0.09.0)

This document is a **separate handoff note** describing why the current repo can look “complete” while still missing the critical intent: **Quantum DPI driving full-stack engine runs** (Gate → UMX → Loom → Press → Codex), not just DPI-side computation and replay summaries.

---

## 1) Executive Summary

**Current state (0.09.0):**

- The CLI surfaces and orchestration exist (hero-suite, sweep runner, run sheets).
- GF01 engine runs are functional (snapshot generate/compare).
- Quantum DPI can compute TBP/PFNA and print fidelity + replay summaries.

**Missing intent:**

- Quantum DPI **does not yet drive** an engine session end-to-end via `--run-engine` (beyond replay checks).
- Operator Service can start runs for jobs, but **does not execute** the Quantum DPI job and inject PFNA outputs into the tick loop.
- Emulation sweeps are **not yet “paired execution”** (oracle + candidate run + compare); comparison currently depends on pre-supplied arrays.

**Why this matters:**

- “Completion” was likely interpreted as “CLI exists and produces outputs,” rather than the stronger requirement: “DPI produces PFNA that drives a real engine run and logs Loom metrics in the run sheets.”

---

## 2) What Works (Confirmed Behaviour)

### 2.1 CLI surfaces

- `python -m dpi_quantum --help` works.
- `python -m dpi_quantum simulate ...` works (DPI simulation + TBP/PFNA + fidelity summaries).
- `python -m dpi_quantum experiment ...` works (DPI experiment + TBP/PFNA + fidelity summaries).
- `python -m cli snapshot generate gf01` runs a multi-tick engine session and writes a snapshot.
- `python -m cli snapshot compare gf01 --baseline tests/snapshots/gf01_run_snapshot.json` compares against the golden baseline.

### 2.2 Run-sheet output

- Repo writes progressive run sheets to:
  - `logs/quantum_runs.jsonl`
  - `logs/quantum_runs.csv`

---

## 3) What’s Missing (The Exact Wiring Gap)

### 3.1 `dpi_quantum --run-engine` is stubbed

In `src/dpi_quantum.py`, the code prints explicit “stubbed wiring / integrate with operator service” messages for engine-driven execution.

Meaning:

- The DPI can compute TBP/PFNA.
- It does not yet start a full Gate session and inject the PFNA as a driver.

### 3.2 Operator Service does not execute Quantum DPI jobs

There is a helper path in `operator_service` to start runs for jobs when `run_engine=true`.

But the service does not yet:

- execute Quantum DPI computation as a job step, or
- inject DPI-derived PFNA bundles into the Gate tick loop.

So even when a “DPI job with run_engine=true” exists, it behaves like:

- “Start a GF01 run and tag metadata,”

not:

- “Use Quantum DPI as the PFNA driver for the run.”

### 3.3 Emulation sweeps are not true oracle-vs-candidate paired runs

Current “emulation compare” behaviour is effectively:

- compute gap metrics **if arrays are already provided**, rather than:
  - run oracle path,
  - run candidate path,
  - extract comparable outputs,
  - compute gaps and emit `emulation_ok`.

---

## 4) Why Codex Could Report “Completion”

This looks like an **acceptance criteria mismatch**.

The work delivered aligns with:

- CLI entrypoints exist,
- hero-suite runs,
- run sheets are produced,
- “replay summaries” exist,

…which is plausibly enough to mark an EPIC “done” if the acceptance tests were only checking those surfaces.

But your intended acceptance criteria were closer to:

- “Quantum DPI runs *through the full stack* with `run_engine=true`, injecting PFNA into a real multi-tick run, and logs Loom metrics.”

That stronger requirement is not enforced by the current tests/criteria, so completion can be claimed without the critical end-to-end behaviour.

---

## 5) Phase 9.1 Delta — What Devs Must Implement

### 5.1 Implement `--run-engine` for Quantum DPI (remove stubs)

**Required behaviour:**

- `dpi_quantum simulate --run-engine` and `dpi_quantum experiment --run-engine` must:
  1. compute TBP/PFNA as they do now,
  2. start an engine run (Gate/GF01 session),
  3. inject PFNA payload(s) into the tick loop (at least tick 0 in v1),
  4. return a `run_id` and/or snapshot artifact,
  5. append a run-sheet row with both DPI and Loom metrics.

**Implementation option A (fastest): in-process run**

- Import Gate runtime directly and call `run_cmp0_tick_loop(...)` with PFNA inputs.
- This avoids HTTP and keeps everything in one process.

**Implementation option B (platform): job submission to Operator Service**

- Add a local client call from `dpi_quantum` to Operator Service to create/execute a DPI job with `run_engine=true`.

### 5.2 Make Operator Service execute Quantum DPI jobs

Add a job executor path so `run_engine=true` means:

- Quantum DPI runs as part of the job,
- PFNA bundles are produced,
- PFNA bundles are consumed by Gate during the tick loop.

### 5.3 Upgrade emulation sweeps to paired execution

Emulation sweeps must:

1. run oracle (DPI-only),
2. run candidate (full stack),
3. extract comparable outputs,
4. compute `prob_l1`, `amp_l2`, etc.
5. set `emulation_ok` based on tolerance.

### 5.4 Ensure run-sheet metrics are fully populated

Populate these fields (not left null):

- `runtime_total_ms` (always)
- `runtime_engine_ms` (where applicable)
- `loom_p_blocks`, `loom_i_blocks`, `loom_bytes`
- `ticks` (engine ticks)
- `peak_mem_mb` (best-effort)

---

## 6) Make It Un-Fakeable — Add One Hard Acceptance Test

Add a single acceptance test (CLI-level) that forces the missing wiring to exist:

**Command:**

```bash
python -m dpi_quantum experiment \
  --name spin_chain \
  --qubits 4 \
  --ticks 4 \
  --run-engine
```

**Pass if and only if:**

- An engine run is created and executed.
- The run is tagged with DPI metadata.
- Run-sheet row contains **non-null** Loom metrics.
- No “stubbed wiring / integrate with operator service” strings appear.

---

## 7) Practical Outcome

When Phase 9.1 is complete, you can:

- run **one command** to sweep qubits for ingest/experiment/sim/emulation,
- have every point produce progressive run sheets,
- and know that the Quantum DPI is genuinely exercising the full Aether stack, not only DPI-local computations and replay summaries.

