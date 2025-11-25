# AEONWindowGrammar_v1 Contract

## Status

- **Name:** AEONWindowGrammar_v1
- **Scope:** Astral Press / AEON window definitions and relationships
- **Used by:** Press/APX windowing, AEON/APXi descriptors, TickLoop integration

This contract defines the **grammar for AEON windows**: how base windows are
expressed on the Loom tick axis, how derived/aggregated windows reference base
windows, and how hierarchical relationships are encoded. It is intentionally
small so that Press, AEON, and APXi can share a common description of window
structure.

---

## 1. Purpose

An AEON window grammar describes a set of windows over ticks:

- **Base windows**: contiguous tick ranges (inclusive) that align to the Loom
  chain.
- **Derived/aggregated windows**: logical windows composed from one or more
  other windows (base or derived) with an optional aggregation label.
- **Hierarchy**: parent/child relationships so that views can be organised
  (e.g. base windows belong to a larger period window).

The grammar keeps links back to Press manifests when a window is materialised as
an APX capsule.

---

## 2. Type definitions

### 2.1 AEONWindowDef_v1 (base window)

Fields:

- `window_id: string` — unique identifier for the window.
- `tick_start: int`   — first tick in the window (inclusive).
- `tick_end: int`     — last tick in the window (inclusive, must satisfy
  `tick_end >= tick_start`).
- `labels: list<string>` — optional labels/tags for grouping (e.g. `"daily"`,
  `"gf01"`).
- `press_window_id: string | null` — optional Press/APX window identifier when
  this AEON window is realised as a manifest.
- `parent_id: string | null` — optional parent window identifier to form a
  hierarchy.

All fields must be deterministic: IDs are case-sensitive; labels are ordered as
provided.

### 2.2 AEONDerivedWindow_v1 (aggregated/derived window)

Fields:

- `window_id: string` — unique identifier.
- `source_ids: list<string>` — ordered list of other window IDs (base or
  derived) that compose this window.
- `aggregation: string` — optional aggregation label (e.g. `"sum"`,
  `"union"`, `"concat"`). Default is `"aggregate"` when no specific method is
  needed for bookkeeping.
- `labels: list<string>` — optional tags.
- `press_window_id: string | null` — optional Press/APX window identifier.
- `parent_id: string | null` — optional parent window identifier.

Invariants:

- `source_ids` must be non-empty and contain no duplicates.
- All `source_ids` must resolve to windows defined in the same grammar.
- A derived window must not reference itself (directly or via `parent_id`).

### 2.3 AEONWindowGrammar_v1 (grammar container)

Fields:

- `base_windows: map<string, AEONWindowDef_v1>` — keyed by `window_id`.
- `derived_windows: map<string, AEONDerivedWindow_v1>` — keyed by `window_id`.

Invariants:

- `window_id` values must be unique across base and derived windows.
- Parent/child references must resolve to windows in the grammar.
- All ticks are integers on the Loom axis; no fractional ticks.

---

## 3. Relationships and references

### 3.1 Loom / tick axis

All windows are defined using integer ticks (`tick_start`, `tick_end`) that map
onto the Loom chain. This allows AEON windows to be aligned with P-block/I-block
boundaries when needed. There are no implicit offsets: ticks are inclusive and
monotonic.

### 3.2 Press / APX linkage

When a window is materialised as an APX capsule, `press_window_id` records the
associated Press/APX window identifier so manifests and AEON windows can be
cross-referenced deterministically.

### 3.3 Hierarchy

Parents can be assigned to either base or derived windows. This is used to build
simple hierarchies such as:

- `daily_1` and `daily_2` (base windows) belong to `week_1` (derived window),
- `week_1` may belong to `quarter_1`, etc.

---

## 4. Examples

### 4.1 GF-01 style fixed window

```json
{
  "base_windows": {
    "ticks_1_8": {
      "window_id": "ticks_1_8",
      "tick_start": 1,
      "tick_end": 8,
      "labels": ["gf01", "cmp0"],
      "press_window_id": "ticks_1_8",
      "parent_id": null
    }
  },
  "derived_windows": {}
}
```

This captures the GF-01 CMP-0 window over ticks 1..8 and links it to the Press
window ID used by manifests.

### 4.2 Simple hierarchy (daily → weekly)

```json
{
  "base_windows": {
    "day_1": {"window_id": "day_1", "tick_start": 1, "tick_end": 4, "labels": ["daily"], "press_window_id": null, "parent_id": "week_1"},
    "day_2": {"window_id": "day_2", "tick_start": 5, "tick_end": 8, "labels": ["daily"], "press_window_id": null, "parent_id": "week_1"}
  },
  "derived_windows": {
    "week_1": {"window_id": "week_1", "source_ids": ["day_1", "day_2"], "aggregation": "union", "labels": ["weekly"], "press_window_id": "week_1_manifest", "parent_id": null}
  }
}
```

Here `week_1` aggregates the two daily windows, records its aggregation method,
and holds an optional Press manifest reference.

---

## 5. Acceptance criteria

- The types above must be serialisable (JSON or mapping form) with deterministic
  field names and ordering.
- GF-01 fixed windows and simple hierarchical examples must be representable.
- Validation must enforce the invariants listed for each type.
