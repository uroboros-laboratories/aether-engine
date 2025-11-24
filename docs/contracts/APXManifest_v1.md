# APXManifest_v1 Contract

## Purpose

`APXManifest_v1` is the top-level manifest for an Astral Press capsule over a fixed tick window.  
It describes:

- Which streams are being compressed,
- Which schemes and parameters are applied, and
- The total description length and check value for the capsule.

`manifest_check` is the value that NAP envelopes reference via `payload_ref`.

---

## Record Shape

Logical record name: `APXManifest_v1`

Top-level fields:

1. **apx_name: string**  
   - Human-readable name for the APX capsule window.  
   - Examples:
     - `"GF01_APX_v0_full_window"` for ticks 1..8.
     - `"GF01_APX_v0_ticks_1_2"` for ticks 1..2.

2. **profile: string**  
   - Compression/MDL profile identifier.  
   - For V0 GF-01, this is `"CMP-0"`.

3. **manifest_check: int**  
   - Decimal check value derived from the selected streams and their schemes.  
   - This is the value that NAP `payload_ref` points to for that window.

4. **streams: list<APXStream_v1>**  
   - One entry per compressed stream in this capsule.

---

## APXStream_v1

Each stream entry describes how one logical series is compressed.

Fields:

- **stream_id: string**  
  - Identifier for the stream, e.g.:
    - `"S1_post_u_deltas"`
    - `"S2_fluxes"`

- **description: string**  
  - Human-readable explanation of what this stream covers.

- **scheme: enum { "ID", "R", "GR" }**  
  - Compression mode:
    - `"ID"`: identity / no compression.
    - `"R"`: basic rANS-like / run-length scheme (V0 uses this).
    - `"GR"`: Golomb–Rice.

- **params: string or int**  
  - Scheme parameters:
    - For `"GR"`, the parameter `p`.
    - For `"R"`, any run/cut parameters; GF-01 examples typically use a simple setting (often effectively “no extra parameter”).

- **L_model: int**  
  - Number of bits used by the model (e.g. header, scheme description).

- **L_residual: int**  
  - Number of bits used by the residuals (encoded data).

- **L_total: int**  
  - `L_model + L_residual`, the total per-stream description length in bits.

---

## Relationship to NAP (`payload_ref`)

For a given window W (set of ticks), there is exactly one APX capsule with:

- One `APXManifest_v1` record, and
- Zero or more encoded streams.

The manifest determines the window’s `manifest_check` integer.

**NAP envelopes for any tick in W must:**

- Set `payload_ref = manifest_check` for that window.
- Leave the actual compressed bytes entirely inside Press / APX; NAP only carries the check integer.

---

## GF-01 Specific Fixtures

### Full 8-tick window (ticks 1..8)

For GF-01 window ticks 1..8, V0 defines:

- `apx_name = "GF01_APX_v0_full_window"`
- `profile = "CMP-0"`
- Two streams:
  - `S1_post_u_deltas`
  - `S2_fluxes`
- Both use scheme `"R"` (basic R mode).
- `L_total` for the two streams are:
  - `L_total(S1) = 7`
  - `L_total(S2) = 8`

The resulting manifest has:

- `manifest_check = 487809945`

For digital parity:

- Given the same input streams (post_u deltas and flux sequences across ticks 1..8),
- And the same R-mode implementation and profile constants,
- Your Press implementation must reproduce:
  - The same scheme choices (`"R"` for both streams),
  - The same `L_total` values, and
  - The same `manifest_check = 487809945`.

### 2-tick window (ticks 1..2)

GF-01 also provides a shorter window example over ticks 1..2 with:

- `apx_name = "GF01_APX_v0_ticks_1_2"`
- `profile = "CMP-0"`
- The same two streams, but shorter sequences.
- The resulting `manifest_check = 869911338`.

This second fixture is useful for unit tests that focus on a smaller window.

---

## Implementation Guidance

To keep V1 manageable:

- Treat `APXManifest_v1` as pure metadata describing the chosen schemes and bit counts.
- You do **not** need to expose the full APX byte layout to other pillars.
- For now, implement the minimal R / GR schemes necessary to reproduce the GF-01 worked examples and `manifest_check` values.

As long as the digital implementation:

- Obeys this manifest shape,
- Produces exact `L_model`, `L_residual`, `L_total`, and `manifest_check` values for GF-01,

it is considered parity with the paper V0 for Press/APX at this profile.
