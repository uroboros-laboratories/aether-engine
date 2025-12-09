# Phase 8 Lineal Implementation Plan

This lineal plan sequences the issues from the Phase 8 Quantum DPI issue pack and the Trinity Gate quantum ingestion pack into a single ordered execution path. Each step names the originating issue so progress can be tracked end-to-end.

## Pre-flight
1. **Readiness sweep** — Confirm Phase 7 operator service and CLI entrypoints run locally; note current history/diagnostic paths.
2. **Feature flag contract** — Decide the feature flag name and defaults for enabling DPIs across operator service and CLI surfaces.

## Operator Service foundations
3. **DPI registry shell (Issue 1)** — Add in-memory registry/types for `DpiSummary`, `DpiDetail`, and `DpiJob`; expose `GET /dpis` and `GET /dpis/{id}` gated by the feature flag.
4. **Job base schema (Issue 2)** — Define shared Quantum DPI job schema (job ids, kinds, status enums, params validation stubs) in one module reusable by service + CLI.

## Quantum CLI scaffolding
5. **CLI entrypoint (Issue 3)** — Create `dpi_quantum` argparse CLI with `ingest`, `simulate`, `experiment`, and `summarize` subcommands and friendly error handling.

## Ingestion pathway
6. **Quantum loader (TG Issue 1)** — Implement dual-source loader (real/simulated) for statevectors with backend logging.
7. **TBP encoder (TG Issue 2)** — Add `quantize_statevector` and residual handling; wire fixtures.
8. **CLI ingest command (Issue 4)** — Wrap loader + encoder behind `dpi_quantum ingest`, returning TBP payloads and summaries.
9. **Harness injection (TG Issue 3)** — Connect quantized payloads into Gate tick harness and ensure ledger/NAP metadata is emitted.
10. **Fidelity metrics (TG Issue 4)** — Compute Prob-L1 and Amp-L2; assert against thresholds; surface in ingest summaries.
11. **Auto-tune (TG Issue 5)** — Provide tier-based η/P auto-tuning utility. *(CLI + operator ingestion auto-tuning landed.)*

## Simulation + experiment flows
12. **CLI simulate command (Issue 5)** — Generate circuits (bell/GHZ/QFT/Clifford), encode to TBP, optional engine run triggering and tagging (Issue 7 linkage start). *(Preset generators + PFNA export wired via CLI; operator wiring pending.)*
13. **Hero experiment scaffold (Issue 6)** — Implement spin-chain loop with optional engine stub; record MDL/motif placeholders. *(CLI spin-chain statevector + quantization wired; engine hook pending.)*
14. **Run linkage (Issue 7)** — Tag engine runs with `dpi_id`/`dpi_kind`/`dpi_job_id`; persist in history store and retrieval helpers.
    *Run tagging is in place and DPI job summaries now carry tuning notes in history exports to aid debugging. Simulation/experiment job creation now starts tagged runs when `run_engine` is requested.*

## Summaries, history, and exports
15. **Summarize command (Issue 8)** — Fetch job/run metadata and print human-readable summaries; handle not-found paths without stack traces.
16. **Results integration** — Ensure history exports carry DPI tags and helper prints lookup hints.

The summarize command now reads `history.jsonl` and `diagnostics.jsonl` so operators can filter by run/job id and see DPI tags plus fidelity diagnostics without touching the UI.

## Tests, fixtures, and docs
17. **CLI tests & fixtures (Issue 9 + TG Issue 6/7)** — Add argument parsing tests, ingest/simulate smoke tests, stress harness sweeps, and generated graphs artifacts. *(PFNA replay smoke tests added; harness sweeps pending.)*
    - PFNA ingress replay metrics now surface in CLI summaries and job exports for ingestion previews.
    - Added a cmp0 Gate harness smoke replay that feeds TBP-derived PFNA payloads through the gf01 topology and records clamp/value stats for job summaries and exports.
18. **Documentation (Issue 10)** — Author Quantum DPI README/usage guide with cross-links and prerequisites.

## Exit checks
19. **Regression sweep** — Run project tests and sample CLI commands with feature flag on/off; update completion report. *(Completed; Phase 8 exit sign-off captured in the build report.)*
