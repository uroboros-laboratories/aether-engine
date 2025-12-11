# Quantum DPI & Base Engine CLI Hero Tests — v1

This document defines a **v1 Hero Test Pack** for validating the Quantum DPI and base Aether engine (Gate → UMX → Loom → Press → Codex) purely from the **command line (CLI)**.

Assumed repo layout (example on Windows):

- Repo root: `C:\Users\bjsti\Desktop\aether-engine-main 0.08.0\aether-engine-main`
- All commands are run from: `...\aether-engine-main\src`

Adjust paths as needed for your actual layout / OS.

---

## Block A — Quantum DPI Hero Tests (CLI Only)

These tests exercise `dpi_quantum.py` directly, without spinning a full Gate session (except the ingest + gate replay hero).

### Hero Q1 — Quantum DPI CLI Wiring

**Goal:** Confirm the Quantum DPI CLI is discoverable and wired correctly.

**Command (from `src`):**

```bash
python -m dpi_quantum --help
```

**Pass if:**

- Exit code = 0.
- Help text prints with a clear header (e.g. `Quantum DPI CLI`) and shows subcommands such as:
  - `ingest`
  - `simulate`
  - `experiment`
  - `summarize`

This confirms the module is importable and the basic CLI entrypoint works.

---

### Hero Q2 — Simulation Hero (Bell State → TBP)

**Goal:** Prove the DPI can:

- Build a small **statevector** (Bell state).
- Quantize it to **TBP** (η, P, masses, residuals) with auto-tune.
- Emit basic **fidelity metrics**.
- Optionally write TBP + PFNA payloads to disk.

**Example command (from `src`):**

```bash
python -m dpi_quantum simulate \
  --circuit bell \
  --qubits 2 \
  --layers 1 \
  --output ../tmp/bell_q2_tbp.json \
  --pfna-output ../tmp/bell_q2_pfna.json
```

(Use `..\tmp\...` on Windows PowerShell; `../tmp/...` on Linux/macOS.)

**Expected console shape:**

- First line: `simulation completed`.
- Followed by lines similar to:
  - `circuit: bell(qubits=2,layers=1)`
  - `eta=... P=...`
  - `masses: 4 entries`
  - `residuals: max=... min=...`
  - `fidelity: prob_l1=0.000000 amp_l2=0.0xxxxx`
  - Optional PFNA replay summary.

**Pass criteria:**

- Exit code = 0.
- No `Simulation failed` line.
- `bell_q2_tbp.json` exists and is valid JSON.
- `bell_q2_pfna.json` exists and is valid JSON.

This is a **pure DPI hero**: it validates statevector → TBP → PFNA without involving a full engine run.

---

### Hero Q3 — Experiment Hero (Spin Chain, DPI Only)

**Goal:** Exercise the **experiment** path using a spin-chain preset and inspect richer metrics.

**Example command (from `src`):**

```bash
python -m dpi_quantum experiment \
  --name spin_chain \
  --qubits 4 \
  --ticks 4 \
  --episodes 1
```

**Expected console shape:**

- `experiment completed`.
- A line like: `experiment: spin_chain(q=4,ticks=4,episodes=1)`.
- Then:
  - `eta=... P=...`
  - `masses: 16 entries`
  - `residuals: max=... min=...`
  - `fidelity: prob_l1=0.000000 amp_l2=0.0xxxxx`
  - Auto-tune notes for η and P.

**Pass criteria:**

- Exit code = 0.
- No `Experiment failed` line.
- Fidelity metrics show a good match (prob_l1 near 0, amp_l2 small).

This is the **canonical DPI hero test** — the spin-chain preset.

---

### Hero Q4 — Ingest + Gate Replay Hero (DPI + Base Engine, Single Tick)

**Goal:** Validate that:

- Ingestion → TBP → PFNA works **and**
- A **Gate + Loom** tick can round-trip the PFNA payload, with proper replay summaries.

`dpi_quantum ingest` uses `generate_ingestion_outputs(...)`, which:

- Builds TBP from an input state (synthetic if none given).
- Runs **PFNA replay**.
- Runs **Gate PFNA replay** via `run_cmp0_tick_loop` (exercising GF01 + Loom once or twice).

**Example command (from `src`):**

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

(This assumes a synthetic source if no `--input` is supplied.)

**Expected console shape:**

- `ingestion completed`.
- TBP stats: η, P, masses, residuals.
- A `fidelity: prob_l1=... amp_l2=...` line.
- A `pfna_replay:` line (events, values range, etc.).
- A `gate_replay:` line (events, values range) indicating a GF01 tick via `run_cmp0_tick_loop`.

**Pass criteria:**

- Exit code = 0.
- No `Ingestion failed` line.
- `ingest_q4_pfna.json` exists.
- `gate_replay` summary is present, confirming DPI → PFNA → Gate → Loom worked for at least one tick.

This is the **first true DPI + base engine hero test** from a single CLI command.

---

## Block B — Base Engine Hero Tests (No DPI)

These tests validate the core GF01 engine, Loom, and Press using `cli.py` utilities, independent of the Quantum DPI.

### Hero E1 — GF01 Baseline Run + Snapshot

**Goal:** Prove the **base engine + Press + Loom** can run the default GF01 scenario and produce a session snapshot.

`gf01` is defined in the scenario registry and points at a standard GF01 run config.

**Example command (from `src`):**

```bash
python -m cli snapshot generate gf01 \
  --output ../tmp/gf01_run_snapshot_hero.json
```

**What it does:**

- Looks up `gf01` in the scenario registry.
- Loads the associated GF01 run config.
- Calls `gate.run_session(...)` to execute GF01 through the tick loop.
- Writes a full run snapshot (UMX, Loom, NAP, manifests, etc.) to the specified output path.

**Pass criteria:**

- Exit code = 0.
- Console prints a confirmation (e.g. `Wrote snapshot to ../tmp/gf01_run_snapshot_hero.json`).
- Snapshot file exists and contains structured JSON with at least:
  - `run_id`
  - `ticks_total`
  - Loom blocks / U-ledger entries / manifests (you don’t need to inspect all fields, just sanity-check structure).

This is the **base engine hero**: no DPI involved, pure GF01 run.

---

### Hero E2 — GF01 Snapshot Compare vs Golden Snapshot

**Goal:** Confirm the engine and Loom behaviour match the repository’s golden GF01 snapshot.

The baseline snapshot lives under the test snapshots directory (e.g. `tests/snapshots/gf01_run_snapshot.json`).

**Example command (from `src`):**

```bash
python -m cli snapshot compare gf01 \
  --baseline tests/snapshots/gf01_run_snapshot.json
```

(Adjust path separators as needed.)

**What it does:**

- Generates a fresh GF01 run snapshot (or uses a candidate snapshot, depending on CLI behaviour).
- Compares it against the baseline snapshot.
- Prints any diffs up to the CLI’s `--max-diffs` limit.

**Pass criteria:**

- Exit code = 0.
- Console reports **no diffs** (or only known, explicitly tolerated tiny differences).

If this passes, it strongly suggests Gate + UMX + Loom + Press + U-ledger are behaving identically to the expected GF01 reference.

---

## How to Use This Hero Pack

1. Navigate to the `src` directory of your `aether-engine-main` repo.
2. Run the hero tests in order:
   - Q1 → Q2 → Q3 → Q4
   - E1 → E2
3. For each test, tick it off in your own checklist when it meets the pass criteria.
4. Once all six heroes are consistently green, you have strong evidence that:
   - Quantum DPI CLI is wired and producing sensible TBP/PFNA + fidelity metrics.
   - DPI can drive a Gate + Loom tick via ingest + gate replay.
   - The base GF01 engine behaves as expected and matches the golden snapshot.

Future work:

- Attach the **run sheet** machinery so that Q3/Q4 and E1/E2 automatically append structured rows to `logs/quantum_runs.csv` / `logs/quantum_runs.jsonl`.
- Add a `quantum-sweep` command to automate qubit-range sweeps using the Q3/Q4 patterns and build benchmark sheets with a single CLI call.


---

## Block C — Sweep Families v1 (Ingest, Experiment, Simulation, Emulation)

This section defines **sweep families** that extend the hero tests into systematic ranges over qubits, ticks, and modes.

### C1 — Ingest / Round-trip Sweep (Static, Single Tick)

**Goal:**

Measure how far we can push `N_qubits` for **pure ingest + round-trip fidelity** through the full stack, with minimal dynamics.

**Mode:** `ingest`

**Shape:**

- Use `dpi_quantum ingest` with:
  - `--qubits N`
  - `--phase-bins P` (e.g. 32)
  - `--auto-tune`
  - `--pfna-output ...`
  - `--pfna-tick 0`
  - `--run-id ...`
  - `--gid GATE`
- Ensure a single GF01 tick via `run_cmp0_tick_loop` so Loom + Gate are exercised.
- `ticks = 1` (or 2 at most).

**Sweep parameters:**

- `N_qubits`: e.g. `[4, 6, 8, 10, 12, 14, 16, 18, ...]`.
- `loom_mode`: `minimal`, `hero`, `forensic` (to see audit cost differences).

**Recorded metrics (per run, appended to run sheet):**

- `n_qubits`, `eta`, `P`, fidelity metrics.
- `runtime_total_ms`, `runtime_engine_ms` (if available), `peak_mem_mb`.
- `loom_p_blocks`, `loom_i_blocks`, `loom_bytes`.
- `status`, `error_code` (if any).

**Question answered:**

> For pure ingest + round-trip (no dynamics), how far can we push qubits in each Loom mode before it becomes slow or fails?

---

### C2 — Experiment Sweep (DPI Experiment Mode)

**Goal:**

Sweep over `N_qubits` (and optionally experiment ticks) in **DPI experiment mode**, with and without running the engine, to understand DPI scaling separately from and together with the base engine.

**Mode:** `experiment`

#### C2a — DPI-only Experiment Sweep

- Run `dpi_quantum experiment` directly with:
  - `--name spin_chain` (or other preset experiment name).
  - `--qubits N`.
  - `--ticks T_experiment` (DPI’s internal notion of ticks, e.g. 4, 8, 16).
  - `--episodes 1` (or more for repeats).
- No Gate/UMX involvement (pure DPI numerics).

**Sweep parameters:**

- `N_qubits`: e.g. `[4, 6, 8, 10, 12, 14, 16, ...]`.
- `T_experiment`: fixed (e.g. 4) or a small set (e.g. `[4, 8, 16]`).

**Metrics:**

- `n_qubits`, `ticks` (experiment ticks), `eta`, `P`, fidelity metrics.
- `runtime_total_ms`, `peak_mem_mb`.
- `status`, `error_code`.

This isolates **DPI statevector + TBP scaling** without engine/Loom overhead.

#### C2b — Full-stack Experiment Sweep

- Wrap the same experiment configs as DPI jobs via the Operator Service with `run_engine=true` so:
  - DPI config → Gate scenario.
  - GF01 runs for `T_engine >= 1` ticks.
  - Loom + Codex are engaged.

**Additional metrics:**

- `runtime_engine_ms`.
- `loom_p_blocks`, `loom_i_blocks`, `loom_bytes`.
- Codex ingestion volume if available.

**Question answered:**

> For our canonical **spin-chain experiment**, what is the comfortable N/ticks region for both the DPI and the full Aether stack?

---

### C3 — Simulation Sweep (Multi-tick Dynamics)

**Goal:**

Understand how **Aether’s own dynamics** (not just static ingest) behave over many ticks, with Loom + Press + Codex active.

There are two sub-types:

#### C3a — Base Engine Simulation Sweep (No Quantum DPI)

- Use `cli snapshot generate gf01` (or equivalent) to run the standard GF01 scenario.
- Vary the number of engine ticks via config or CLI overrides.

**Sweep parameters:**

- `ticks_total`: e.g. `[20, 50, 100, 200]`.

**Metrics:**

- `ticks`, `runtime_total_ms`, `runtime_engine_ms`, `peak_mem_mb`.
- `loom_p_blocks`, `loom_i_blocks`, `loom_bytes`.
- Snapshot size / Press-compressed snapshot bytes.

This tests **Loom/Press scaling** over long histories and Codex’s ability to ingest many-tick runs.

#### C3b — Quantum-driven Simulation Sweep (Future Work)

- Design a scenario where each GF01 tick is driven by PFNA inputs derived from a quantum-like evolution (via Quantum DPI or precomputed TBP sequences).
- Run for `T_engine > 1` ticks.

**Sweep parameters:**

- `N_qubits`.
- `ticks_total` (e.g. `[20, 40, 80]`).

This tests **combined DPI + engine dynamics** over time.

---

### C4 — Emulation Sweep (Aether vs Oracle Behaviour)

**Goal:**

Measure how well Aether (full stack) can **emulate** an “oracle” quantum model (or other external reference), focusing on output behaviour and error tolerances rather than internal details.

**Mode:** `emulate`

**Oracle path:**

- Use DPI-only runs (e.g. `dpi_quantum simulate` / `experiment` with `run_engine=false`) or golden distributions as the reference.

**Full-stack path:**

- Run equivalent configs through Gate/UMX/Loom/Codex with `run_engine=true`.

**Sweep parameters:**

- `N_qubits`.
- Circuit type (e.g. `bell`, `ghz`, `spin_chain`).
- Depth / ticks (circuit depth or engine ticks).

**Metrics per pair of runs (oracle vs emulation):**

- Output distributions / observable arrays.
- Error metrics (e.g. total variation distance, prob_l1, amp_l2).
- Timing and resource metrics (from the run sheet schema).
- Boolean `emulation_ok` flag where error stays within tolerance.

**Question answered:**

> When Aether is trying to behave like a given quantum model, up to what qubit counts and depths does it stay within acceptable error margins?

---

In combination with the **Hero Tests** (Blocks A and B), these sweep families define a clear roadmap for:

- Validating core functionality (heroes).
- Characterising scaling and behaviour across modes (sweeps).
- Feeding structured results into the Quantum DPI run sheets for later analysis and Codex learning.
