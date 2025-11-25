# ScenarioRegistry_v1

Phase 3 governance contract describing a registry of named Aether scenarios. Each
entry points to a `RunConfig_v1` document so runners and tooling can enumerate
and select scenarios without bespoke wiring.

## Shape

```json
{
  "v": 1,
  "scenarios": [
    {
      "scenario_id": "gf01",
      "description": "GF-01 baseline CMP-0 run",
      "pillars": ["gate", "press"],
      "runtime_hint": "very-small",
      "run_config_path": "../configs/gf01_run_config.json"
    }
  ]
}
```

- `v`: Schema version, fixed at `1` for Phase 3.
- `scenarios`: Array of scenario entries (must be non-empty).
  - `scenario_id`: Unique identifier for the scenario (string, required).
  - `description`: Human-readable summary (string, required).
  - `pillars`: Optional list of pillar names touched by the scenario (default: []).
  - `runtime_hint`: Optional string describing approximate runtime scale
    (e.g. `very-small`, `small`, `medium`).
  - `run_config_path`: Relative path from the registry file to the `RunConfig_v1`
    JSON document backing the scenario.

## Determinism and resolution rules

- Registry loading is deterministic; duplicate `scenario_id` values are rejected.
- Relative `run_config_path` entries are resolved from the directory containing
  the registry file, then validated to exist when loading.
- Only JSON is supported for registry documents to keep parsing consistent with
  other Phase 3 config contracts.

## Compatibility

- Registry entries must reference `RunConfig_v1` documents (see
  `docs/contracts/RunConfig_v1.md`).
- No Phase 1/2 behaviour is altered; the registry simply provides a catalogue of
  pre-defined runs for Phase 3 governance tooling.
