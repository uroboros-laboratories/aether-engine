# Snapshot Tests

Regression snapshots for runs (e.g. GF-01) to ensure determinism over time.

- `gf01_run_snapshot.json`: Baseline GF-01 CMP-0 run output.
- `pfna_v0_demo_snapshot.json`: Phase 3 PFNA V0 demo run (LINE4 topology with PFNA ingress).
- `aeon_apxi_demo_snapshot.json` (under `tests/fixtures/snapshots/aeon_apxi_demo/`): Phase 3 AEON/APXi demo run (Line-4 topology, AEON windows, APXi descriptors).
- `line_4_run_snapshot.json`: 4-node line scenario run via file-driven config.
- `ring_5_run_snapshot.json`: 5-node ring scenario run via file-driven config.

Use `python -m cli snapshot generate <scenario-id>` to regenerate a snapshot and
`python -m cli snapshot compare <scenario-id> --baseline <path>` to compare
against the stored version. The CLI defaults to the scenario registry under
`docs/fixtures/scenarios/`.
