# Phase 8 Progressive Build Report

This report tracks how, what, why, and where changes are made so a new contributor can follow along.

## Progress summary
- **Phase completion:** 100% — PFNA TBP outputs replay through both the Gate ingress shim and a cmp0 harness smoke run, DPI history/export APIs surface replay metrics directly on jobs, simulation/experiment job creation spins up tagged engine runs, ingestion responses report PFNA + Gate replay metrics, and the CLI summarize command can read history/diagnostics for DPI jobs. Gate replay visibility is exposed in CLI ingest/simulate/experiment summaries, and the final regression sweep confirmed feature-flagged stability.

## 2025-XX-XX — Initial planning and scaffolding
- **What:** Authored a lineal plan sequencing Phase 8 Quantum DPI and Trinity Gate ingestion issues; added DPI feature-flagged registry skeleton and Quantum CLI parser stubs.
- **Why:** Establish a clear execution path and non-breaking hooks for DPI discovery before wiring deeper ingestion/simulation behaviours.
- **How:**
  - Added `phase_8_lineal_plan.md` detailing step-by-step implementation order.
  - Introduced operator service DPI models/registry with a Phase 8 feature flag to keep Phase 7 stable when disabled.
  - Created `dpi_quantum` CLI entrypoint with placeholder subcommands to unblock argument parsing and future wiring.
- **Where:** Documentation in `docs/specs/phase_8_lineal_plan.md`; service scaffolding in `src/operator_service/dpi.py` and `src/operator_service/service.py`; CLI stub in `src/dpi_quantum.py`.
- **Next:** Flesh out job schema validation, connect registry to job storage, and implement ingest path backed by quantum loader/quantizer utilities.

## 2025-XX-XX — Job schema consolidation
- **What:** Added a shared DPI job schema helper to keep CLI and operator service aligned on required fields and defaults.
- **Why:** Prevent diverging assumptions about ingestion/simulation inputs before wiring real data paths; provide structured hints for UI/docs.
- **How:**
  - Created `operator_service.dpi_jobs` to hold schemas, defaults, and validation helpers for ingestion, simulation, and experiment job kinds.
  - Exposed the schema through the Quantum DPI config metadata so `/dpis` callers can introspect required fields.
  - Updated the `dpi_quantum` CLI to validate and echo normalized parameters (with defaults) instead of silently accepting missing inputs.
- **Where:** Schema helpers in `src/operator_service/dpi_jobs.py`; registry wiring in `src/operator_service/dpi.py`; CLI validation in `src/dpi_quantum.py`.
- **Next:** Wire registry job creation to persistence/history, then implement ingestion loader + quantizer plumbing.

## 2025-XX-XX — Quantum ingestion plumbing (stubbed runs)
- **What:** Added offline-friendly quantum loader/quantizer and taught the CLI ingest command to produce TBP payloads for early testing.
- **Why:** Unblocks validation of Trinity Gate quantization logic and lets contributors inspect payload shapes before engine wiring lands.
- **How:**
  - Implemented `load_statevector` and `quantize_statevector` utilities that normalize arbitrary JSON payloads or synthesize a Bell state when no file is provided.
  - Relaxed ingestion schema defaults (η, P, qubits) so the CLI can run end-to-end without manual flags.
  - Updated `dpi_quantum ingest` to encode TBP payloads, summarize buckets/residuals, and optionally write JSON to disk.
- **Where:** Utilities in `src/operator_service/quantum_ingest.py`; schema defaults in `src/operator_service/dpi_jobs.py`; CLI wiring in `src/dpi_quantum.py`.
- **Next:** Attach ingestion jobs to the DPI registry/history, add fidelity metrics, and exercise the TBP output inside the engine harness.

## 2025-XX-XX — DPI job creation + fidelity hints
- **What:** Wired the operator service to accept feature-flagged DPI job creation requests and added TBP fidelity metrics to ingestion output.
- **Why:** Starts exercising the job lifecycle for Phase 8 while providing early quality signals on quantized payloads before engine linkage.
- **How:**
  - Added a POST `/dpis/{id}/jobs` endpoint that validates job kinds, applies defaults, and queues DPI jobs in the in-memory registry.
  - Introduced TBP reconstruction helpers to compute probability L1 and amplitude L2 gaps from quantized payloads.
  - Updated the CLI ingest command to emit fidelity metrics alongside TBP bucket stats.
- **Where:** Service handler in `src/operator_service/service.py`; registry sequencing in `src/operator_service/dpi.py`; fidelity helpers in `src/operator_service/quantum_ingest.py`; CLI output in `src/dpi_quantum.py`.
- **Next:** Connect queued jobs to run history, add ingestion fidelity thresholds, and feed TBP payloads into the engine harness.

## 2025-XX-XX — Fidelity thresholds + run tagging
- **What:** Added configurable fidelity thresholds to ingestion and allowed DPI jobs to carry optional run ids for downstream history linkage.
- **Why:** Lets contributors detect poor quantizations automatically and begin threading job metadata into run exports without breaking existing callers.
- **How:**
  - Extended the ingestion job schema with `max_prob_l1`/`max_amp_l2` defaults and numeric validation to keep CLI and service inputs aligned.
  - Updated the `dpi_quantum ingest` command to assert fidelity metrics against thresholds, returning non-zero exits when violated.
  - Allowed POST `/dpis/{id}/jobs` to accept an optional `run_id` so queued jobs can be pre-tagged to engine runs as history plumbing arrives.
- **Where:** Threshold validation in `src/operator_service/dpi_jobs.py`; CLI enforcement in `src/dpi_quantum.py`; run tagging in `src/operator_service/service.py`.
- **Next:** Wire DPI job statuses into `HistoryStore` exports, bubble fidelity failures into diagnostics, and plumb TBP payloads into the Gate harness for replay tests.

## 2025-XX-XX — DPI history exports + tagging
- **What:** Propagated DPI job metadata into run history entries and export bundles while allowing DPI job creation to tag live engine runs.
- **Why:** Ensures Phase 8 jobs stay discoverable in history/diagnostics exports and lets contributors correlate engine runs with DPI ingestion attempts.
- **How:**
  - Added DPI metadata fields to `RunStatus`/`HistoryEntry` and serialized them through history APIs and exports.
  - Allowed `/dpis/{id}/jobs` to tag active runs when a `run_id` is provided and surface whether tagging succeeded.
  - Exposed DPI context on history detail responses so downstream tooling can correlate jobs and runs.
- **Where:** Tagging flow in `src/operator_service/service.py`; history/export plumbing in `src/operator_service/run_registry.py`.
- **Next:** Bubble fidelity failures into diagnostics, and plumb TBP payloads into the Gate harness for replay tests.

## 2025-XX-XX — Fidelity diagnostics + Gate replay bundles
- **What:** Captured fidelity violations as diagnostics entries and emitted PFNA bundles from TBP payloads for Gate harness replay.
- **Why:** Keeps low-fidelity ingestions visible to operators and lets contributors reuse TBP outputs in Gate/PFNA pipelines without hand-editing fixtures.
- **How:**
  - Added a reusable fidelity diagnostics builder and service helper to persist failed checks alongside existing diagnostics history.
  - Extended `dpi_quantum ingest` to write PFNA V0 bundles from TBP payloads and to auto-log fidelity failures into diagnostics.jsonl.
  - Provided TBP→PFNA converters for both in-memory harness replay and file-based ingestion.
- **Where:** Diagnostics utilities in `src/operator_service/diagnostics.py`; PFNA conversion helpers in `src/operator_service/quantum_ingest.py`; CLI wiring in `src/dpi_quantum.py`.
- **Next:** Auto-tune η/P defaults, wire simulate/experiment stubs to real circuits, and add replay smoke tests that consume the PFNA bundles.

## 2025-XX-XX — Auto-tune + simulation circuits
- **What:** Added auto-tuned η/P selection plus real statevector generators for simulation and experiment commands with PFNA emission options.
- **Why:** Lets contributors run the CLI without hand-picking quantization parameters while exercising realistic Bell/GHZ/QFT/spin-chain states for downstream Gate harness replay.
- **How:**
  - Added heuristics to pick η/P based on observed amplitudes and phase diversity, surfacing the choices in CLI summaries.
  - Implemented preset circuit generators (Bell, GHZ, QFT, random Clifford) and a spin-chain-inspired experiment statevector with optional TBP/PFNA file emission.
  - Updated the CLI to quantize simulated/experimental statevectors, report fidelity, and keep auto-tuning optional via flags.
- **Where:** Auto-tune + circuit generators in `src/operator_service/quantum_ingest.py`; CLI wiring in `src/dpi_quantum.py`; schema defaults in `src/operator_service/dpi_jobs.py`.
- **Next:** Add replay smoke tests that consume PFNA bundles, wire simulate/experiment to operator service runs, and fold η/P heuristics into the operator-side ingestion path.

## 2025-XX-XX — Operator auto-tune + PFNA replay smoke tests
- **What:** Brought the operator ingestion path up to parity with CLI auto-tuning and added PFNA bundle smoke coverage to de-risk Gate harness replay.
- **Why:** Ensures η/P heuristics are consistent regardless of entrypoint and verifies PFNA outputs stay structurally valid before wiring real engine calls.
- **How:**
  - Kept ingestion defaults unset when `auto_tune` is true so the operator service can sample the provided statevector and apply heuristic η/P values.
  - Auto-tuned ingestion parameters inside DPI job creation using the same loader/heuristics used by the CLI and recorded tuning notes with the job payload.
  - Added unit smoke tests that quantize Bell states into PFNA bundles and assert PFNA inputs/bundles stay shape-consistent.
- **Where:** Default handling in `src/operator_service/dpi_jobs.py`; ingestion auto-tuning in `src/operator_service/service.py` and `src/operator_service/quantum_ingest.py`; PFNA smoke tests in `tests/unit/test_quantum_ingest_pfna.py`.
- **Next:** Wire simulation/experiment job creation to operator run metadata, replay PFNA bundles through the Gate harness shim, and surface tuning diagnostics in history exports.

## 2025-XX-XX — PFNA ingress replay + tuning traces in exports
- **What:** Replayed TBP→PFNA payloads through the Gate ingress shim and preserved auto-tuning context in history exports and DPI job summaries.
- **Why:** Confirms PFNA bundles remain compatible with Gate integerization paths and ensures tuning breadcrumbs are visible when inspecting exported run artifacts.
- **How:**
  - Added a TBP replay helper that feeds PFNA V0 payloads through the Gate `PFNAIngressQueue` for per-tick integerized events.
  - Extended DPI history export summaries to include job params and tuning notes so operators can recover η/P decisions later.
  - Exercised the replay path and export metadata via new unit tests.
- **Where:** Ingress helper in `src/operator_service/quantum_ingest.py`; export enrichment in `src/operator_service/run_registry.py`; tests in `tests/unit/test_quantum_ingest_pfna.py` and `tests/unit/test_history_dpi_exports.py`.
- **Next:** Hook simulation/experiment job creation into operator run starts, plumb PFNA replay into a Gate harness smoke scenario, and enrich summaries with replay metrics.

## 2025-XX-XX — Simulation/experiment jobs launch tagged runs
- **What:** Added DPI-aware run wiring so simulation and experiment job creation can immediately start an engine run with DPI metadata attached.
- **Why:** Keeps job creation in sync with Gate executions and ensures runs carry DPI job ids for history/diagnostics visibility.
- **How:**
  - Added scenario selection helpers and a DPI job run starter that applies overrides for `dpi_id`, `dpi_kind`, and `dpi_job_id`.
  - Allowed simulation/experiment job schemas to accept `scenario_id` hints and updated `/dpis/{id}/jobs` to trigger tagged runs when `run_engine` is true.
  - Captured run summaries on the created jobs so responses and exports show which scenario/run_id were launched.
- **Where:** Run wiring in `src/operator_service/service.py`; schema hints in `src/operator_service/dpi_jobs.py`; run tagging support in `src/operator_service/dpi.py`; coverage in `tests/unit/test_dpi_job_runs.py`.
- **Next:** Reuse PFNA replay helpers inside a Gate harness smoke scenario and surface replay metrics alongside job summaries.

## 2025-XX-XX — PFNA replay metrics in job + CLI summaries
- **What:** Replayed quantized TBP payloads inside Gate’s PFNA ingress shim to gather value/clamp stats and surfaced the metrics in CLI output and queued ingestion job summaries.
- **Why:** Keeps Gate compatibility visible to operators before full engine wiring and documents PFNA integerization behaviour directly in history exports.
- **How:**
  - Added replay summarization helpers that count PFNA ingress events, integerized ranges, and clamp occurrences.
  - Emitted replay stats from CLI ingest/simulate/experiment commands alongside fidelity lines so users can spot clamp-heavy payloads.
  - Captured ingestion previews as `result_summary` data on queued jobs and exposed PFNA replay metrics via history export summaries.
- **Where:** PFNA replay summaries in `src/operator_service/quantum_ingest.py`; CLI output in `src/dpi_quantum.py`; job summaries and exports in `src/operator_service/service.py` and `tests/unit/test_history_dpi_exports.py`.
- **Next:** Thread replay metrics through a Gate harness smoke scenario and expand summarize tooling around the new DPI job metadata.

## 2025-XX-XX — CLI history/diagnostics summaries
- **What:** Added a DPI-aware summarize command that reads run history and diagnostics logs so operators can quickly inspect fidelity and replay outcomes without spelunking JSON.
- **Why:** Makes Phase 8 artifacts discoverable from the console while UI wiring is pending and keeps history/diagnostics paths visible to new contributors.
- **How:**
  - Introduced a summarize handler that loads `history.jsonl` and `diagnostics.jsonl`, filters by run or job id, and prints DPI metadata, fidelity summaries, and diagnostic outcomes.
  - Added unit coverage to ensure the handler reports history entries, DPI tags, and diagnostics, and degrades gracefully when no matches are found.
- **Where:** CLI wiring in `src/dpi_quantum.py`; coverage in `tests/unit/test_dpi_quantum_summarize.py`.
- **Next:** Thread PFNA replay metrics into a Gate harness smoke scenario and expose the summaries via the operator service APIs.

## 2025-XX-XX — Gate harness replay + API surfacing
- **What:** Replayed TBP→PFNA payloads inside the cmp0 Gate harness and exposed the replay metrics on DPI job APIs and exports.
- **Why:** Validates PFNA bundles against a realistic Gate execution loop and makes clamp/value summaries immediately visible to operator clients without parsing deep result blobs.
- **How:**
  - Added a harness replay helper that runs TBP-derived PFNA inputs through the gf01 cmp0 tick loop and reports integerized value stats and clamp counts.
  - Included Gate replay metrics in ingestion `result_summary` payloads and surfaced them alongside PFNA replay data on `/dpis` job listings and history exports.
  - Added smoke coverage to ensure Gate replay metrics are produced for Bell-state quantizations and preserved in export job summaries.
- **Where:** Harness replay in `src/operator_service/quantum_ingest.py`; API surfacing in `src/operator_service/run_registry.py` and `src/operator_service/service.py`; coverage in `tests/unit/test_quantum_ingest_pfna.py` and `tests/unit/test_history_dpi_exports.py`.
- **Next:** Wire any remaining harness replay hooks into operator-run results, surface Gate replay visibility in CLI output, and complete the regression sweep for Phase 8 exit.

## 2025-XX-XX — CLI Gate replay visibility
- **What:** Surfaced Gate harness replay metrics in CLI summaries so console users see PFNA ingress and Gate cmp0 results side by side.
- **Why:** Keeps CLI experience aligned with operator API exports and helps spot clamp-heavy payloads before shipping them downstream.
- **How:**
  - Updated CLI ingestion/simulation/experiment flows to report cmp0 Gate replay event/value/clamp stats alongside PFNA ingress metrics.
  - Added a CLI unit test that exercises ingest with auto-tuned defaults and asserts PFNA + Gate replay lines are present.
- **Where:** CLI wiring in `src/dpi_quantum.py`; coverage in `tests/unit/test_dpi_quantum_gate_cli.py`.
- **Next:** Run the final regression sweep and mark Phase 8 complete once operator-run result hooks are validated.

## 2025-XX-XX — Regression sweep + Phase exit
- **What:** Validated Phase 8 readiness by running the full offline regression suite and smoke CLI commands behind the DPI feature flag, confirming operator-run hooks and history/diagnostics access remain stable.
- **Why:** Ensures the accumulated Phase 8 work does not regress Phase 7 behaviour and that contributors can trust the documented flows end-to-end.
- **How:**
  - Exercised the offline regression suite (`pytest -q`) to cover PFNA/Gate replay, history exports, job/run wiring, and CLI summaries.
  - Re-ran CLI ingest defaults under feature-flag conditions to verify PFNA + Gate replay lines and fidelity summaries continue to print without manual parameters.
  - Reviewed operator history/diagnostics exports for DPI-tagged runs to confirm run/job linkage remains serialized for downstream tooling.
- **Where:** Tests in `tests/unit/test_quantum_ingest_pfna.py`, `tests/unit/test_history_dpi_exports.py`, `tests/unit/test_dpi_job_runs.py`, and `tests/unit/test_dpi_quantum_gate_cli.py`; CLI smoke invocation via `src/dpi_quantum.py`.
- **Next:** Phase 8 complete — monitor for follow-up polish or UI surfacing tasks.
