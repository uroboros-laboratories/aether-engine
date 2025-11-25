# StructuredLogging_v1

Phase 3 introduces a lightweight structured logging contract so Aether runs can
emit machine-readable lifecycle events without altering deterministic outputs.

## Entry shape

Each log entry is a JSON object with the following fields:

- `event` (string): event name such as `run_start`, `tick_loop_start`,
  `tick_complete`, `window_closed`, or `run_end`.
- `gid` (string): graph identifier for the run.
- `run_id` (string): run identifier supplied by the caller.
- `ts` (ISO 8601 string): UTC timestamp when the entry was emitted.
- `tick` (integer, optional): tick number for tick-scoped events.
- `window_id` (string, optional): window identifier for window-scoped events.
- `payload` (object, optional): event-specific details, e.g. envelope counts or
  manifest hashes.

Entries are emitted in-order and can be streamed to memory, stdout, or a file.

## Configuration

`LoggingConfig_v1` controls structured logging with these fields:

- `enabled` (bool, default `false`): enable or disable logging.
- `destination` (string, default `"memory"`): one of `memory`, `stdout`, or
  `file`.
- `file_path` (string, optional): required when `destination` is `file`.
- `include_ticks` (bool, default `true`): emit `tick_complete` events.
- `include_windows` (bool, default `true`): emit `window_closed` events.

The config is embedded inside `RunConfig_v1.logging` and surfaced as
`SessionConfigV1.logging_config` for runtime wiring.

## Determinism

- Logging is out-of-band and does **not** modify TickLoop, Press, or U-ledger
  outputs.
- Timestamps are expected to differ between runs; shape and ordering of entries
  remain stable for identical inputs.
