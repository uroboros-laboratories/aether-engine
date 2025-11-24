# UMXTickLedger_v1 Contract

## Purpose

`UMXTickLedger_v1` is the per-tick record produced by the Universal Matrix (UMX) integer engine.  
It captures:

- The full **pre-tick state**,
- The **edge fluxes** used to update the state,
- The full **post-tick state**, and
- A **conservation check**.

This is the main thing Loom, Press, and higher layers “see” from the substrate.

---

## Record Shape

Logical record name: `UMXTickLedger_v1`

Top-level fields:

1. **tick: int**  
   - Tick index `t ≥ 1`.

2. **sum_pre_u: int**  
   - Sum over all node values before the tick:  
     `sum_pre_u = Σ_i pre_u[i]`.

3. **sum_post_u: int**  
   - Sum over all node values after the tick:  
     `sum_post_u = Σ_i post_u[i]`.

4. **z_check: int**  
   - Conservation check value.  
   - MUST satisfy:  
     `z_check == sum_pre_u == sum_post_u`.

5. **pre_u: int[N]**  
   - State before tick `t`, in **canonical node ID order** (e.g. node IDs 1..N mapped to indices 0..N-1).

6. **edges: list<EdgeFlux_v1>**  
   - One entry per edge in the graph.  
   - MUST be sorted strictly by `e_id` ascending, and MUST cover every edge exactly once.

7. **post_u: int[N]**  
   - State after tick `t`, in the same node order as `pre_u`.

---

## EdgeFlux_v1

Each edge flux entry has the shape:

- **e_id: int**  
  - Edge ID (1-based in GF-01).

- **i: int**  
  - Source node ID (or the lower-index node ID in an undirected edge).

- **j: int**  
  - Target node ID.

- **du: int**  
  - Integer difference `du = pre_u[i] - pre_u[j]`.

- **raw: int**  
  - Unclamped “raw” flux magnitude from the CMP-0 profile:  
  - `raw = floor(k_e * |du| / SC)`, where:
    - `k_e` is the edge’s coupling constant,
    - `SC` is the scale constant in the profile.

- **cap: int**  
  - Capacity for this edge, `cap_e`.  
  - In GF-01 this is effectively ∞ (no binding cap) but we still record it explicitly.

- **f_e: int**  
  - Signed, clamped flux:
  - `f_e = sgn(du) * min(raw, cap_e, |du|)`.

---

## Update Rule

Given `pre_u` and `edges`, the new state `post_u` is:

```text
for each node i:
  net_i = Σ_e contribution from f_e
  post_u[i] = pre_u[i] + net_i
```

Where “contribution” is:

- For an edge from i→j, if `f_e` is positive, it flows from i to j:
  - Node i loses `f_e`
  - Node j gains `f_e`

Edge directions / contributions should be implemented consistently with the GF-01 worked examples.

After computing `post_u`:

- `sum_pre_u = Σ_i pre_u[i]`
- `sum_post_u = Σ_i post_u[i]`
- `z_check` is set to that common sum.

An implementation passes the conservation check iff:

- `sum_pre_u == sum_post_u` and
- `z_check == sum_pre_u`.

---

## GF-01 Specific Fixture

For the GF-01 CMP-0 profile:

- N = 6 nodes.
- A fixed edge list with IDs 1..8.
- Single scale constant `SC = 32`.
- Edge constants `k_e` and capacities `cap_e` come from the topology card.

The GF-01 worked examples define:

- Initial state `u(0) = [3, 1, 0, 0, 0, 0]`.
- A sequence of 8 ticks.
- For each tick t=1..8:
  - `pre_u`, `du`, `raw`, `f_e`, and `post_u`.

**Acceptance for digital parity:**

Given the same topology and initial state, the digital UMX implementation must produce `UMXTickLedger_v1` records at ticks 1..8 that **exactly match**:

- The `pre_u` and `post_u` vectors,
- The `du`, `raw`, and `f_e` columns per edge, and
- The conservation (`sum_pre_u`, `sum_post_u`, `z_check`).

Any deviation indicates a mismatch between the code and the canonical paper math.
