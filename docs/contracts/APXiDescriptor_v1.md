# APXiDescriptor_v1 Contract

## Status

- **Name:** APXiDescriptor_v1
- **Scope:** Astral Press / APXi descriptor language over AEON windows
- **Used by:** AEON/APXi views, Press manifests (companions), Codex motif consumers

This contract defines the **APXi descriptor language (v1)**. Descriptors attach
structured explanations to Press streams over AEON windows. They are small,
deterministic records that can be serialised, compared, and reasoned about by
APXi, Codex, or downstream tooling.

---

## 1. Purpose

- Provide a **minimal, deterministic** descriptor shape for APXi V0/V1.
- Describe simple integer patterns over a stream within an AEON window.
- Keep descriptors composable so MDL accounting can be layered on later phases.

Descriptors never carry raw stream bytes; they only describe structure. All
numeric fields are integers to preserve CMP-0 determinism.

---

## 2. Type definitions

### 2.1 APXiDescriptor_v1 (base record)

Fields:

- `descriptor_id: string` — unique identifier for the descriptor.
- `descriptor_type: enum { "CONST_SEGMENT", "RUN_SEGMENT", "LINEAR_TREND" }`
  — primitive type of the descriptor.
- `window_id: string` — AEON window id this descriptor covers (tick-aligned).
- `stream_id: string` — Press/APX stream identifier the descriptor describes.
- `params: map<string, int|list<int>>` — primitive-specific parameters (see below).
- `labels: list<string>` — optional deterministic tags for grouping.

Invariants:

- All string ids must be non-empty and deterministic (case-sensitive).
- `descriptor_type` must be one of the allowed primitive enums.
- `params` must satisfy the rules for the given primitive type.
- Labels must be non-empty strings; ordering is preserved as given.

### 2.2 Primitive parameter shapes

All primitives are **integer-only** and deterministic. Unknown fields are not
permitted in `params`.

1. **CONST_SEGMENT** — constant value over the window (or sub-window slice):

   - `value: int` — constant integer value.

2. **RUN_SEGMENT** — repeated pattern over the window:

   - `pattern: list<int>` — non-empty sequence of integers to repeat.
   - `repeats: int` — number of whole-pattern repeats (must be ≥ 1).

3. **LINEAR_TREND** — simple linear model across ticks:

   - `intercept: int` — value at `start_tick`.

   - `slope: int` — per-tick increment (integer).

   - `start_tick: int` — optional start tick offset for the model (defaults to 0
     if omitted in serialisation). Tick arithmetic remains integer-only.

---

## 3. Relationships and references

- **AEON windows:** `window_id` must reference an AEON window in the associated
  registry/grammar.
- **Press streams:** `stream_id` must match a Press/APX stream identifier (e.g.
  `APXStream_v1.stream_id`). Descriptors do not alter stream payloads; they
  merely annotate them.
- **MDL accounting:** This contract only defines shapes. MDL code length and
  residual handling are layered on in later issues (P4.4+). The P4.4
  implementation computes `L_model` directly from the descriptor fields and
  window length, and derives `L_residual` by applying the descriptor to the
  target window and encoding the residuals with an ID/R/GR scheme.

---

## 4. Serialisation rules

- Descriptors must be representable as deterministic mappings or JSON objects
  with the field names above.
- Arrays/lists (`labels`, `pattern`) preserve input ordering.
- Integer-only values; no floats or implicit rounding.

Example JSON descriptor set:

```json
[
  {
    "descriptor_id": "d_const_1",
    "descriptor_type": "CONST_SEGMENT",
    "window_id": "ticks_1_8",
    "stream_id": "S1_post_u_deltas",
    "params": {"value": 3},
    "labels": ["gf01", "cmp0"]
  },
  {
    "descriptor_id": "d_run_1",
    "descriptor_type": "RUN_SEGMENT",
    "window_id": "ticks_1_4",
    "stream_id": "S2_fluxes",
    "params": {"pattern": [1, -1], "repeats": 2},
    "labels": []
  },
  {
    "descriptor_id": "d_trend_1",
    "descriptor_type": "LINEAR_TREND",
    "window_id": "ticks_1_8",
    "stream_id": "S1_post_u_deltas",
    "params": {"intercept": 4, "slope": -1, "start_tick": 0},
    "labels": ["trend"]
  }
]
```

---

## 5. Acceptance criteria

- `APXiDescriptor_v1` exists with the fields and invariants listed above.
- Primitive parameter validation matches the shapes defined for CONST_SEGMENT,
  RUN_SEGMENT, and LINEAR_TREND.
- Descriptors can be serialised/deserialised deterministically and retain
  references to AEON windows and Press streams.
- All numeric fields are integers; no stochastic or heuristic variation.
