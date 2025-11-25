# Introspection CLI (SPEC-006 P3.2.4)

Phase 3 introduces a small CLI wrapper so developers can inspect run artefacts without
writing Python. The commands wrap the read-only Introspection APIs and reuse the Phase 3
scenario registry plus RunConfig files.

## Commands

- `python -m cli inspect <scenario-id> [--summary] [--tick N] [--window ID]`
  - Looks up `<scenario-id>` in the scenario registry (or uses `--run-config` if provided),
    executes the run deterministically, builds an introspection view, and prints JSON to stdout.
  - With no flags, a summary block is emitted. `--tick` adds the tick ledger, P-block, and NAP
    envelopes for the given tick. `--window` adds the APX manifest for the selected window ID.
- `python -m cli show-ledger <scenario-id>`
  - Runs the scenario and prints the ordered U-ledger entries as JSON.

## Options

- `--registry PATH` — optional scenario registry path (defaults to
  `docs/fixtures/scenarios/scenario_registry.json`).
- `--run-config PATH` — bypasses the registry lookup and runs the explicit RunConfig JSON.

All outputs are JSON with deterministic ordering (`sort_keys=True`). Unknown scenario/run IDs
produce a non-zero exit code with a helpful error message.
