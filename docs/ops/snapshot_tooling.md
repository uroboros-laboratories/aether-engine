# Snapshot Management Tooling (SPEC-006 P3.3.2)

Phase 3 adds CLI helpers to regenerate and compare regression snapshots across
reference scenarios. Snapshots live under `tests/snapshots/`.

## Commands

```
python -m cli snapshot generate <scenario-id> [--run-config <path>] \
    [--registry <path>] [--output <path>]

python -m cli snapshot compare <scenario-id> --baseline <path> \
    [--candidate <path> | --run-config <path>] [--registry <path>] \
    [--output <path>] [--max-diffs <int>]
```

- `generate` runs the scenario (or explicit RunConfig) and writes a snapshot. If
  `--output` is omitted, it defaults to `tests/snapshots/<scenario-id>_run_snapshot.json`.
- `compare` checks a baseline snapshot against a candidate file, a new run from
  `--run-config`, or a scenario resolved via the registry. The command exits
  non-zero and prints a concise diff if differences are found. Passing
  `--output` writes the candidate snapshot for review.

The CLI relies on the scenario registry at
`docs/fixtures/scenarios/scenario_registry.json` by default.
