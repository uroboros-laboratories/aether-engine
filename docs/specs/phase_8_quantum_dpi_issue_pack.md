# Phase 8 — Quantum DPI (Console-First) Issue Pack

## Epic: Phase 8 — Domain Plug-ins (DPI) & Quantum DPI (CLI)

**Goal**  
Add a console-first **Domain Plug-in** layer on top of the Aether stack, with a **Quantum DPI** that can:

- Ingest quantum data (from files/simulators).
- Run quantum simulations.
- Run the H1 spin-chain hero experiment.
- Log everything via the existing engine plumbing.

UI comes later; Phase 8 is driven entirely from the console/CLI.

---

### Issue 1 — Implement DPI registry & feature flag

**Title:** Implement DPI registry and feature flag in operator service

**Description:**  
- Add a minimal in-memory (or config-backed) **DPI registry** that knows about available domain plug-ins (starting with `quantum`).  
- Add a **Phase 8 feature flag** (e.g. env var or config key) that controls whether DPIs are exposed at all.  
- For now, this is purely backend; no UI integration required.

**Acceptance Criteria:**

- A `DpiSummary` / `DpiDetail`-like structure (or equivalent) exists in the operator service domain model.
- The operator service can list at least one DPI: `Quantum DPI`, `type=quantum`, `status=IDLE` when the engine is up.
- Turning the feature flag off disables all DPI-related behaviour cleanly (no crashes, no dangling calls).
- No impact on existing Phase 7 behaviour when the feature flag is off.

---

### Issue 2 — Define Quantum DPI config schema and job model

**Title:** Define Quantum DPI config schema and job model

**Description:**  
- Introduce internal data structures for **Quantum DPI jobs**:
  - `kind`: `INGESTION`, `SIMULATION`, `EXPERIMENT`.
  - `params`: opaque dict for domain-specific config.
  - `status`: `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`.
  - Optional `run_id` pointer into the existing engine run model.
- Define explicit **parameter schemas** for:
  - Ingestion jobs (file path / payload type).
  - Simulation jobs (circuit id, qubits, depth).
  - Experiment jobs (H1: qubits, ticks, episodes).

**Acceptance Criteria:**

- There is a single place in the codebase where Quantum DPI job shapes are defined and documented.
- All three job kinds share a consistent base model with `job_id`, `dpi_id`, `kind`, `status`.
- Invalid or missing params are rejected early with clear errors.

---

### Issue 3 — Add `dpi_quantum` CLI entrypoint with subcommands

**Title:** Add `dpi_quantum` CLI entrypoint with subcommands

**Description:**  
- Add a Python CLI (via `argparse` or similar), e.g. `dpi_quantum.py` or `python -m aether.dpi.quantum`.  
- Support subcommands:
  - `ingest`
  - `simulate`
  - `experiment`
  - `summarize`
- Wire the CLI to construct and submit **Quantum DPI jobs** via the operator service or directly via an internal API, depending on repo architecture.

**Acceptance Criteria:**

- Running `python dpi_quantum.py --help` (or equivalent) shows subcommands and arguments.
- CLI runs without importing any UI code.
- CLI errors are human-readable and do not expose stack traces by default for user mistakes (bad args, missing flags).

---

### Issue 4 — Implement `dpi_quantum ingest` using quantum_data_ingest logic

**Title:** Implement `dpi_quantum ingest` using quantum_data_ingest logic

**Description:**  
- Take the existing `quantum_data_ingest.py` behaviour and wrap it behind a CLI command, e.g.:

  python dpi_quantum.py ingest \
    --input path/to/file.json \
    --eta 1e6 \
    --phase-bins 64 \
    --output tbp_payload.json

- Supported sources v0.1:
  - `--input` file with statevector/counts in a known JSON format.
  - Optional: a `--mode simulated` path that uses Qiskit/Aer to generate ψ.
- Output:
  - TBP-style payload with `masses`, `phases`, `eta`, `P` written to a JSON file **and** printed summary to console.

**Acceptance Criteria:**

- `dpi_quantum ingest` can be run from console in repo context without touching UI.
- Given a valid input, the command produces a TBP payload file and prints a short summary (qubits, vector length, η, P, basic norms).
- Given a bad input file, the command fails fast with a clear error message (no raw stack trace).

---

### Issue 5 — Implement `dpi_quantum simulate` for emulated circuits

**Title:** Implement `dpi_quantum simulate` for emulated circuits

**Description:**  
- Add a `simulate` subcommand that:
  - Accepts args like:
    - `--circuit {bell,ghz4,qft4,random_clifford}`
    - `--qubits N`
    - `--layers L`
  - Uses the same underlying logic as `quantum_data_ingest.py` to:
    - Generate ψ (statevector) from the chosen circuit.
    - TBP-encode it (η, P).
  - Either:
    - (a) just writes out the TBP payload, or
    - (b) optionally (`--run-engine`) kicks off a short Aether engine run configured as a scenario.

**Acceptance Criteria:**

- `dpi_quantum simulate --circuit ghz4 --qubits 8 --layers 10` runs to completion using the simulator path.
- TBP payload is generated and stored (or passed onwards) in a consistent format with `ingest`.
- If `--run-engine` is supported, a corresponding engine run is invoked and the resulting `run_id` printed.

---

### Issue 6 — Implement H1 spin-chain hero experiment as `experiment` command

**Title:** Implement `dpi_quantum experiment` for H1 spin-chain law-finder

**Description:**  
- Based on the Stage 2 hero experiment spec, implement a command like:

  python dpi_quantum.py experiment \
    --name spin_chain \
    --qubits 8 \
    --ticks 256 \
    --episodes 100

- Behaviour:
  - For each episode:
    - Generate an initial state (as per design: random product/low-depth entangled).
    - TBP-encode and inject.
    - Apply the spin-chain gate pattern via the engine (or a stub that matches engine behaviour).
  - Record:
    - MDL baseline vs with CE (if the CE hook is available).
    - Number of structural motifs discovered (if available).
  - Print a concise summary at the end (per-episode averages + totals) and optionally store a JSON summary file.

**Acceptance Criteria:**

- Running the experiment with modest settings (e.g. 4 qubits, 32 ticks, 10 episodes) completes on a dev machine without crashing.
- Output includes:
  - Quibits, ticks, episodes.
  - MDL/compression stats where available (even if stubbed).
  - Any discovered motifs summarized (even if stubbed names).
- The command either:
  - (a) calls into the engine to do the real updates, or
  - (b) is clearly marked as “engine stubbed” but structurally matches how a real wiring would work.

---

### Issue 7 — Link Quantum DPI jobs to engine runs and history

**Title:** Link Quantum DPI jobs to Aether engine runs and history

**Description:**  
- For any `simulate` or `experiment` invocation that actually runs the engine:
  - Create a **standard engine run** (reusing the existing run/session config path).
  - Tag it with metadata indicating:
    - `dpi_id = quantum`
    - `dpi_kind = {INGESTION,SIMULATION,EXPERIMENT}`
    - `dpi_job_id` if applicable.
- Ensure run metadata is persisted wherever normal run info lives (history/log store).
- Provide a small helper (Python function or CLI output) that prints how to look up this run again (e.g. `run_id`).

**Acceptance Criteria:**

- For a successful `simulate --run-engine` or `experiment` run:
  - A corresponding run record exists in the normal history/log store.
  - That record is clearly tagged as a Quantum DPI run.
- If there is an existing “history CLI” or some programmatic API, it can filter or at least display these tags.

---

### Issue 8 — Implement `dpi_quantum summarize` for past runs/jobs

**Title:** Implement `dpi_quantum summarize` for past runs/jobs

**Description:**  
- Add a `summarize` subcommand, e.g.:

  python dpi_quantum.py summarize --run-id <id>
  # or
  python dpi_quantum.py summarize --job-id <id>

- Using whatever storage/history is available:
  - Fetch high-level info about that run/job:
    - Type (ingest/sim/experiment).
    - Quibits/ticks/episodes (if known).
    - Any recorded MDL or motif metrics.
  - Print a human-readable summary to console.

**Acceptance Criteria:**

- Given an existing run/job id from a Quantum DPI command, `summarize` prints a useful, non-verbose summary.
- If the run id is unknown, it fails with a clear “not found” message, not a stack trace.

---

### Issue 9 — Tests & fixtures for Quantum DPI CLI

**Title:** Add basic tests and fixtures for Quantum DPI CLI

**Description:**  
- Add unit/integration tests (to match the project’s testing style) for:
  - Argument parsing for all subcommands.
  - Happy-path `ingest` with a small fixture input file.
  - Happy-path `simulate` with a very small circuit.
  - Smoke test for `experiment` with tiny settings (e.g. 2 qubits, 4 ticks, 2 episodes), possibly behind a “slow test” marker.
- Add small fixture files:
  - Tiny example statevector/counts input.
  - Expected TBP output for at least one simple case (if stable enough to assert).

**Acceptance Criteria:**

- Running the project’s test runner includes the new DPI tests.
- All new tests pass reliably on a dev machine.
- Tests are isolated and do not require UI or network access (unless explicitly marked as such).

---

### Issue 10 — Quantum DPI README / docs

**Title:** Document Quantum DPI CLI usage and Phase 8 design

**Description:**  
- Add a section to the project `README` (or a new `docs/phase_8_quantum_dpi.md`) that explains:
  - What the Quantum DPI is.
  - High-level relation to the Aether stack (Gate/UMX/Loom/Press/CE).
  - How to:
    - Run `ingest`, `simulate`, `experiment`, and `summarize` commands.
  - Any prerequisites (Python deps, optional Qiskit, etc.).
- Cross-link to:
  - `trinity_gate_quantum_ingest_issues.md`.
  - `aether_quantum_emulation_plan.md` and the hero experiment docs if present in the repo.

**Acceptance Criteria:**

- A new doc section exists and renders correctly in GitHub.
- A new contributor (or Codex) can read it and understand how to run the Quantum DPI CLI without touching the UI.
