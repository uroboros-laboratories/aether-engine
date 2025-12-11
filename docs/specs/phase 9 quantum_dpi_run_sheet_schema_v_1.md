# Quantum DPI Run Sheet Schema v1

This schema defines the **standard run sheet row** for any Quantum DPI + Gate + Loom + Codex run executed via the console.

Each **run = one row** in the sheet.

---

## Columns

| # | Column name           | Type        | Required | Example                                     | Description |
|---|-----------------------|------------|----------|---------------------------------------------|-------------|
| 1 | `run_id`              | string     | yes      | `gf01_2025-12-10T12-30-00`                  | Globally-unique run identifier (from Operator Service / RunRegistry). |
| 2 | `timestamp`           | string     | yes      | `2025-12-10T12:30:00Z`                      | ISO-8601 timestamp when the run started (UTC or AWST, but be consistent). |
| 3 | `scenario`            | string     | yes      | `spin_chain`                                | Logical scenario name (hero experiment / scenario id). |
| 4 | `scenario_version`    | string     | no       | `v1`, `hf01`                                | Optional scenario version / variant tag if you introduce tuned versions. |
| 5 | `dpi_id`              | string     | yes      | `quantum_dpi_v1`                            | Identifier of the DPI implementation used for this run. |
| 6 | `dpi_mode`            | string     | yes      | `experiment`, `ingest`, `emulate`           | High-level DPI mode (matches CLI / job config). |
| 7 | `n_qubits`            | integer    | yes      | `12`                                        | Number of qubits in the logical quantum experiment. |
| 8 | `ticks`               | integer    | yes      | `40`                                        | Number of engine ticks / steps for this run (for CMP0 loop). |
| 9 | `episodes`            | integer    | no       | `1`                                         | Number of episodes / repetitions (if relevant for the DPI mode). |
|10 | `shots`               | integer    | no       | `1024`                                      | Number of measurement samples (if applicable to scenario). |
|11 | `topology_profile`    | string     | yes      | `gf01_cmp0`                                 | Engine topology profile (e.g. `gf01_cmp0`, `toy_topo_01`). |
|12 | `math_profile`        | string     | yes      | `cmp0_default`                              | Math / precision profile name used for the run. |
|13 | `loom_mode`           | string     | yes      | `forensic`, `hero`, `minimal`               | Loom logging/audit profile in effect for the run. |
|14 | `codex_mode`          | string     | yes      | `OFF`, `OBSERVE`                            | Codex action mode for this run (`OFF` or `OBSERVE` in 0.08.0). |
|15 | `press_profile`       | string     | no       | `default`, `high_compression`               | Optional named Press config/profile if you vary it. |
|16 | `eta`                 | float      | no       | `640000.0`                                  | TBP η parameter selected / auto-tuned for this run (if applicable). |
|17 | `P`                   | integer    | no       | `32`                                        | TBP P parameter (phase bins) selected / auto-tuned (if applicable). |
|18 | `runtime_total_ms`    | integer    | yes      | `18432`                                     | Total wall-clock runtime of the run in milliseconds (DPI + engine + Loom + Codex). |
|19 | `runtime_engine_ms`   | integer    | no       | `15000`                                     | Time spent inside the engine/tick loop only, in milliseconds (if measured). |
|20 | `peak_mem_mb`         | integer    | no       | `723`                                       | Approximate peak memory usage for the process during this run, in megabytes. |
|21 | `loom_p_blocks`       | integer    | yes      | `80`                                        | Count of Loom P-blocks emitted for this run. |
|22 | `loom_i_blocks`       | integer    | yes      | `3`                                         | Count of Loom I-blocks emitted for this run. |
|23 | `loom_bytes`          | integer    | no       | `524288`                                    | Total bytes written to Loom block store for this run (if using persistent store). |
|24 | `press_bytes`         | integer    | no       | `196608`                                    | Total bytes written for Press-compressed artefacts attached to this run (if trackable separately). |
|25 | `pfna_events`         | integer    | no       | `64`                                        | Number of PFNA input events generated/consumed during this run. |
|26 | `pfna_clamps`         | integer    | no       | `0`                                         | Count of PFNA clamp events (values clamped to bounds) for this run. |
|27 | `epsilon_bytes`       | integer    | no       | `0`                                         | Total bytes used by ε-ledger corrections for this run. |
|28 | `status`              | string     | yes      | `OK`, `ERROR`, `OOM`, `TIMEOUT`             | Final status of the run. |
|29 | `error_code`          | string     | no       | `oom_statevector`, `dpi_config_error`       | Short error code if `status != OK`. |
|30 | `error_message`       | string     | no       | `OutOfMemoryError in statevector builder`   | Short human-readable error message (truncated if needed). |
|31 | `notes`               | string     | no       | `first hero run at N=16 (hero mode)`        | Free-form note field for human annotations. |

---

## Minimal required subset (if you want a "lite" run sheet)

If you want a smaller CSV for quick benchmarking, this is the minimal "v1-lite" subset that should always be present:

- `run_id`
- `timestamp`
- `scenario`
- `n_qubits`
- `ticks`
- `dpi_mode`
- `loom_mode`
- `codex_mode`
- `runtime_total_ms`
- `peak_mem_mb` (if you can get it)
- `loom_p_blocks`
- `loom_i_blocks`
- `status`

You can still keep the full schema as JSONL for deeper analysis and Codex ingestion, while the CSV only uses the lite subset.

