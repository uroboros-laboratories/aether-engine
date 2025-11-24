# TopologyProfile_v1 Contract

## Purpose

`TopologyProfile_v1` captures the static structure and parameters of a Universal Matrix (UMX) graph:

- Node set (IDs, optional labels),
- Edge set (which nodes are connected),
- Integer parameters needed by the CMP profile (e.g. `k_e`, `cap_e`, `SC`).

It is the digital counterpart to the **GF-01 topology card** and the more general topology forms in the Aether paper pack.

This record is **read-only** during a run under CMP-0; dynamic topology changes (SLP, graph growth/prune) come later under higher profiles.

---

## Record Shape

Logical record name: `TopologyProfile_v1`

Top-level fields:

1. **gid: string**  
   - Graph / run identifier.  
   - For the GF-01 fixture: `"GF01"`.

2. **profile: string**  
   - Name of the numeric profile this topology is intended to run under.  
   - For the initial engine: `"CMP-0"`.

3. **N: int**  
   - Number of nodes in the graph.

4. **nodes: list<NodeProfile_v1>**  
   - One entry per node, in **canonical ID order** (sorted by `node_id` ascending).

5. **edges: list<EdgeProfile_v1>**  
   - One entry per edge, in **canonical ID order** (sorted by `e_id` ascending).  
   - This ordering MUST match the order used in `UMXTickLedger_v1.edges`.

6. **SC: int**  
   - Global scale constant for this profile (e.g. `SC = 32` in CMP-0 / GF-01).  
   - Included here for convenience; per-edge references inherit this.

7. **meta: object (optional)**  
   - Free-form metadata (e.g. human description, tags, provenance).

---

## NodeProfile_v1

Each node profile has:

- **node_id: int**  
  - Unique node ID in `[1..N]`.

- **label: string (optional)**  
  - Human-readable label, may be empty.

- **attrs: object (optional)**  
  - Placeholder for future node attributes (e.g. type, capacity); unused in CMP-0 / GF-01.

Canonical example (GF-01):

```jsonc
{
  "node_id": 1,
  "label": "n1",
  "attrs": {}
}
```

---

## EdgeProfile_v1

Each edge profile has:

- **e_id: int**  
  - Unique edge ID, typically 1-based: `1, 2, ..., E`.

- **i: int**  
  - One endpoint node ID.

- **j: int**  
  - Other endpoint node ID.  
  - For an undirected edge, `(i, j)` is chosen such that `i < j`.

- **k: int**  
  - Integer coupling constant `k_e` for this edge under CMP-0.  
  - Used in the UMX raw flux formula `raw = floor(k * |du| / SC)`.

- **cap: int**  
  - Integer capacity `cap_e` for this edge.  
  - In GF-01 this is effectively "no binding cap" (may be represented as a large integer or a sentinel).

- **SC: int**  
  - Scale constant used for this edge’s flux updates.  
  - In CMP-0, all edges share the same SC as the profile.

- **c: int (optional)**  
  - Spare per-edge integer constant (e.g. for future profiles).  
  - MUST be present but may be `0` in CMP-0 / GF-01.

- **attrs: object (optional)**  
  - Free-form attributes (type hints, labels, etc.).

Canonical example (GF-01-style):

```jsonc
{
  "e_id": 1,
  "i": 1,
  "j": 2,
  "k": 32,
  "cap": 2147483647,
  "SC": 32,
  "c": 0,
  "attrs": {}
}
```

---

## Invariants

For any valid `TopologyProfile_v1`:

- Node IDs are contiguous: `{ node_id } = {1, 2, ..., N }`.
- Edge IDs are contiguous: `{ e_id } = {1, 2, ..., E }` for some `E ≥ 0`.
- `edges` is sorted strictly by `e_id` ascending.
- All referenced `i` and `j` node IDs are within `[1..N]`.
- `SC > 0`.
- For CMP-0:
  - All `k` and `cap` are integers (no floats).
  - `SC` is identical across edges (unless explicitly overridden by a future profile).

UMX and Loom use this profile as **read-only configuration** for GF-01 and other fixed-topology runs.
