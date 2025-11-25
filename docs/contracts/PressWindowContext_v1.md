# PressWindowContext_v1 Contract

## Status

- **Name:** PressWindowContext_v1
- **Scope:** Window-level context for Press/APX streams
- **Used by:** Press/APX implementation, TickLoop wiring, SPEC-002/005

This contract defines the **API and responsibilities** of the Press/APX window
context used to manage streams and produce `APXManifest_v1` records.

It is intentionally minimal and focused on the GF-01 / CMP-0 baseline and
Phase 2 generalisation.

---

## 1. Purpose

A `PressWindowContext_v1`:

- Buffers one or more named streams of integer data across ticks,
- Knows which graph/run/window it belongs to,
- Applies encoding schemes to its streams at window close,
- Produces a single `APXManifest_v1` describing the window.

UMX, Loom, and Gate feed it data per tick; tests examine the manifest.

---

## 2. Type Definition

### 2.1 PressWindowContext_v1

Conceptually, a `PressWindowContext_v1` holds:

- Identity:
  - `gid: string`        — Graph ID (e.g. `"GF01"`).
  - `run_id: string`     — Run identifier.
  - `window_id: string`  — Window identifier (e.g. `"ticks_1_8"`).
  - `profile_id: string` — Profile in use (e.g. `"CMP-0"`).
  - `aeon_window_id: string?` — Optional AEON window linkage (Phase 3).

- Configuration:
  - `start_tick: int`    — First tick in the window (inclusive).
  - `end_tick: int`      — Last tick in the window (inclusive).
  - `default_scheme: string` — Default scheme hint for streams (e.g. `"R"`).

- Streams:
  - `streams: map<string, PressStreamBuffer_v1>` — keyed by stream name.
- APXi (Phase 3 optional):
  - `apxi_descriptors: map<string, list<APXiDescriptor_v1>>` — optional APXi descriptors per stream.
  - `apxi_residual_scheme: string` — residual scheme for APXi MDL (`"ID"`, `"R"`, `"GR"`).
  - `apxi_view_ref: string?` — optional reference to the computed APXi view for the window.

The exact in-memory representation is language-specific; the contract is about
what this context must *do* and what data it must be able to produce.

### 2.2 PressStreamBuffer_v1

A `PressStreamBuffer_v1` is a buffer of data for a single named stream.

Fields:

- `name: string`         — stream name (e.g. `"S1_post_u_deltas"`).
- `scheme_hint: string`  — suggested scheme (`"ID"`, `"R"`, `"GR"`, etc.).
- `values: list<any>`    — sequence of tick-aligned values; typically integers
                           or fixed-size tuples of integers.

In CMP-0 / GF-01:

- `S1_post_u_deltas` uses a tuple per tick (derived from `post_u` deltas).
- `S2_fluxes` uses a tuple per tick (per-edge fluxes).

---

## 3. Behaviour / API

The following operations define the behavioural contract.
Signatures are conceptual; implementations can structure them however they like.

### 3.1 register_stream

```text
register_stream(name: string, scheme_hint: string) -> None
```

- Must create a new `PressStreamBuffer_v1` with the given `name` and `scheme_hint`.
- Must fail (or no-op deterministically) if a stream with the same `name`
  already exists.

### 3.2 append

```text
append(name: string, value_or_tuple: any) -> None
```

- Appends `value_or_tuple` to the named stream’s `values` list.
- Must be deterministic:
  - For a given tick sequence and inputs, the resulting `values` must match.

### 3.3 close_window

```text
close_window() -> APXManifest_v1
```

- Applies the appropriate scheme to each stream (by `scheme_hint` and/or
  profile defaults).
- Computes, per stream:
  - `L_model`, `L_residual`, `L_total` (bit-lengths).
- Aggregates all streams and window metadata into an `APXManifest_v1`.
- Computes `manifest_check` as defined in the APX spec.
- If APXi is enabled for the window, computes an `APXiView_v1` and sets
  `manifest.apxi_view_ref` to a deterministic identifier.
- After this call, the context may either:
  - Become immutable, or
  - Reset its buffers for the next window (implementation choice).

For GF-01, closing the window over ticks `1..8` must yield the manifest with
`L_total(S1) = 7`, `L_total(S2) = 8`, and `manifest_check = 487809945`.

---

## 4. Relationship to APXManifest_v1

`PressWindowContext_v1` is responsible for producing exactly **one** manifest
per window:

- `gid`, `run_id`, `window_id`, `profile_id` must match the context.
- All streams defined in `streams` must appear in the manifest with their
  final MDL stats and scheme identifiers.
- `manifest_check` must be a deterministic function of:
  - Stream contents,
  - Scheme choices,
  - MDL stats,
  - Window metadata.

The exact structure of `APXManifest_v1` is defined in its own contract doc.

---

## 5. GF-01 Specialisation

For GF-01 CMP-0 baseline:

- Windows:
  - Window `ticks_1_8`: ticks `1..8`, streams `S1_post_u_deltas`, `S2_fluxes`.
  - Window `ticks_1_2`: ticks `1..2`, same streams but truncated.
- Schemes:
  - Both streams use scheme `"R"` (run-length-like) in the current examples.
- Manifests:
  - Window `ticks_1_8`:
    - `L_total(S1) = 7`
    - `L_total(S2) = 8`
    - `manifest_check = 487809945`
  - Window `ticks_1_2`:
    - `manifest_check = 869911338`

Any PRESS/APX implementation that claims GF-01 compatibility must be able to
express the above using `PressWindowContext_v1` and `APXManifest_v1`.

---

## 6. Versioning

This is `PressWindowContext_v1`. Future revisions (e.g. with more complex
windowing behaviour) should:

- Use a new name/version,
- Keep the GF-01 behaviour reproducible via `v1` semantics.
