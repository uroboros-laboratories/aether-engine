# PFNA_V0_Schema_v1

## Status

- **Version:** v1
- **Phase:** Phase 3 (SPEC-003)
- **Scope:** Deterministic encoding for external integer inputs (PFNA V0)

## Purpose

PFNA V0 standardises how external integer sequences are provided to Gate/TBP. It
describes a minimal, deterministic bundle that can be loaded and applied to a
run without ambiguity. The schema emphasises integer-only data, explicit target
identifiers, and stable ordering for reproducibility.

## Top-level shape

A PFNA V0 document is a single JSON/YAML object with the following required
fields:

- `v` (int): Schema version. Must be `0` for PFNA V0.
- `pfna_id` (str): Identifier for the PFNA bundle.
- `gid` (str): Topology graph identifier the inputs target.
- `run_id` (str): Run identifier the inputs target.
- `nid` (str): Node or endpoint identifier (logical ingress id).
- `entries` (array): Ordered list of PFNA input records.

### Entry records

Each entry in `entries` is an object with required fields:

- `pfna_id` (str): Identifier for this entry (unique within the bundle).
- `tick` (int): Tick index when the values apply. `0` is reserved for
  **initial-state/parameter mapping** (applied before tick 1); `>= 1`
  applies during the run.
- `values` (array of int): Integer vector to apply at that tick.

Optional entry field:

- `description` (str): Human-readable context for the entry.

### Determinism and ordering

- Entries MUST be deterministic: same document yields identical in-memory
  structures when parsed repeatedly.
- Entries SHOULD be provided in tick order; the loader will sort by
  `(tick, pfna_id)` to ensure stable ordering.
- All integer values are treated exactly as provided; no floating-point or
  implicit rounding is allowed.

## Validation rules

- `v` must be `0`.
- `pfna_id`, `gid`, `run_id`, and `nid` must be non-empty strings.
- `entries` must be a non-empty array.
- Each entry must provide `pfna_id`, `tick >= 0`, and a non-empty `values`
  array of integers. `tick == 0` is treated as an initial-state/parameter
  mapping; `tick >= 1` affects the run during execution.
- If an expected vector length is provided by the caller (e.g., topology `N`),
  each entry’s `values` length must match that expectation.

## Loader expectations

- The loader accepts JSON strings/paths or already-decoded dictionaries.
- On success, the loader returns the entries as immutable `PFNAInputV0` objects
  in deterministic order.
- On validation failure, the loader raises `ValueError` with a deterministic
  message describing the first issue encountered.

## Round-trip considerations

PFNA V0 is intentionally simple: serialising a loaded bundle back to JSON using
standard library JSON tools will preserve field values and ordering when the
same sorting strategy (`tick`, then `pfna_id`) is applied. This enables
round-trip tests of the form: source → parse → serialise → parse.
