# Aether Toy Topologies — Reference Set (v1)

## Status

- **Name:** Aether_Toy_Topologies_v1
- **Scope:** Small, named example topologies for tests and docs
- **Used by:** UMX tests, Loom tests, SPEC-005 Phase 2

This doc defines a **small standard set of toy graphs** you can use as
canonical examples in tests and specs. They are not physics profiles;
they are just graph shapes you can pair with any profile (e.g. CMP-0).

---

## 1. General Notes

All toy topologies follow the `TopologyProfile_v1` contract:

- Nodes `1..N`.
- Edges `1..E` with `(e_id, i, j, k, cap, SC, c)`.
- For these examples, we keep parameters simple so that tests are easy to reason
  about (mostly unit gains, moderate caps, shared `SC`).

Unless otherwise stated:

- `k = 1`
- `cap = 10`
- `SC = 32`
- `c = 0`

You are free to override these in specific tests if needed, but these are the
defaults for “toy topologies”.

---

## 2. LINE_4 (Directed Line of 4 Nodes)

**ID:** `LINE_4`  
**Description:** Nodes in a simple line: `1 -> 2 -> 3 -> 4`.

- `N = 4`
- `E = 3`

Edges:

| e_id | i | j | k | cap | SC | c |
|------|---|---|---|-----|----|---|
| 1    | 1 | 2 | 1 | 10  | 32 | 0 |
| 2    | 2 | 3 | 1 | 10  | 32 | 0 |
| 3    | 3 | 4 | 1 | 10  | 32 | 0 |

Suggested `TopologyProfile_v1` fields:

- `gid = "LINE_4"`
- `name = "Aether Toy Topology — LINE_4"`

Use cases:

- Simple left-to-right diffusion tests.
- sanity checks for conservation on small graphs.

---

## 3. RING_5 (Directed Ring of 5 Nodes)

**ID:** `RING_5`  
**Description:** Nodes arranged in a directed ring: `1 -> 2 -> 3 -> 4 -> 5 -> 1`.

- `N = 5`
- `E = 5`

Edges:

| e_id | i | j | k | cap | SC | c |
|------|---|---|---|-----|----|---|
| 1    | 1 | 2 | 1 | 10  | 32 | 0 |
| 2    | 2 | 3 | 1 | 10  | 32 | 0 |
| 3    | 3 | 4 | 1 | 10  | 32 | 0 |
| 4    | 4 | 5 | 1 | 10  | 32 | 0 |
| 5    | 5 | 1 | 1 | 10  | 32 | 0 |

Suggested `TopologyProfile_v1` fields:

- `gid = "RING_5"`
- `name = "Aether Toy Topology — RING_5"`

Use cases:

- Testing cyclic flows and steady states.
- Checking that chain/loop behaviour is deterministic.

---

## 4. STAR_6 (Star Topology with 6 Nodes)

**ID:** `STAR_6`  
**Description:** One central node (1) connected to 5 outer nodes (2..6).

You can pick a direction convention; for CMP-0 toy tests we’ll use edges
from centre to leaves:

- `1 -> n` for `n in {2, 3, 4, 5, 6}`.

- `N = 6`
- `E = 5`

Edges:

| e_id | i | j | k | cap | SC | c |
|------|---|---|---|-----|----|---|
| 1    | 1 | 2 | 1 | 10  | 32 | 0 |
| 2    | 1 | 3 | 1 | 10  | 32 | 0 |
| 3    | 1 | 4 | 1 | 10  | 32 | 0 |
| 4    | 1 | 5 | 1 | 10  | 32 | 0 |
| 5    | 1 | 6 | 1 | 10  | 32 | 0 |

Suggested `TopologyProfile_v1` fields:

- `gid = "STAR_6"`
- `name = "Aether Toy Topology — STAR_6"`

Use cases:

- Testing “hub and spoke” flux patterns.
- Checking central node behaviour under CMP-0.

---

## 5. Extending the Set

The above three are the **canonical starting set** for Aether toy topologies.

If you add new ones later:

- Give them clear IDs (e.g. `LINE_8`, `GRID_3x3`, etc.).
- Define them in this doc or a v2 doc.
- Keep them small and hand-checkable where possible.
