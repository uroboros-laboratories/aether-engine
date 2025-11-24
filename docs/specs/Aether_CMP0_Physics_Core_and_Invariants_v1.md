# Aether CMP-0 Physics Core and Invariants (v1)

## Status

- **Profile:** CMP-0
- **Scope:** GF-01 V0 baseline, Phase 1 / SPEC-002
- **Goal:** Define the **exact maths and invariants** the digital engine must obey
  for CMP-0 runs, especially GF-01.

This doc is the single, canonical reference for CMP-0 physics. Implementation
code and tests should treat this as the primary source of truth.

---

## 1. State, Topology, and Profiles (CMP-0)

### 1.1 Node state

At tick `t`, the system has:

- `N` nodes, indexed `1..N`.
- A state vector:

```text
u(t) = [u_1(t), u_2(t), ..., u_N(t)]
```

All entries are **integers** (no floats).

For GF-01:

- `N = 6`
- Initial state:

```text
u(0) = [3, 1, 0, 0, 0, 0]
```

### 1.2 Edges and topology

The graph is represented by a **topology profile**:

- Edge set `E = {1, 2, ..., E_max}`.
- Each edge `e` has:

```text
(i_e, j_e, k_e, cap_e, SC_e, c_e)
```

where:

- `i_e` = source node index (integer in `[1..N]`)
- `j_e` = target node index (integer in `[1..N]`)
- `k_e` = gain or conductance-like parameter (integer)
- `cap_e` = capacity (non-negative integer)
- `SC_e` = scale or normalisation constant (positive integer)
- `c_e` = optional cost/label parameter (integer; not used in CMP-0 physics)

For GF-01 under CMP-0:

- Edges are **labelled 1..8** with fixed `(i, j, k, cap, SC, c)` from the GF-01 tables.
- All `SC_e` are equal to the profile-level `SC` (currently 32).

### 1.3 CMP-0 profile constants

Profile CMP-0 is defined by:

- Profile name: `"CMP-0"`
- Modulus: `M = 1_000_000_007`
- Initial chain seed: `C_0 = 1234567`
- Scale constant: `SC = 32`
- I-block spacing: `W = 8` (i.e. emit an I-block every 8 ticks)

These constants are used in the flux, chain, and Loom rules below.

---

## 2. CMP-0 Flux Rule (UMX)

The CMP-0 flux rule determines how state flows along edges each tick.

### 2.1 Per-edge quantities

For each tick `t` and each edge `e` with endpoints `(i, j)`:

1. **State difference**

```text
du_e(t) = u_i(t-1) - u_j(t-1)
```

2. **Raw magnitude**

```text
raw_e(t) = floor( k_e * abs(du_e(t)) / SC_e )
```

where:

- `k_e` is the edge's gain,
- `SC_e` is the edge's scale (for CMP-0, `SC_e = SC = 32`),
- `floor` is the integer floor function,
- `abs` is absolute value.

3. **Flux per edge**

```text
f_e(t) = sign(du_e(t)) * min( raw_e(t), cap_e, abs(du_e(t)) )
```

where:

- `cap_e` is the edge capacity,
- `sign(x)` is:
  - `+1` if `x > 0`
  - `0` if `x = 0`
  - `-1` if `x < 0`

The sign ensures flux direction is from higher to lower node state.

### 2.2 Node update rule

For each node `n`, the state update is:

```text
u_n(t) = u_n(t-1)
         - sum_{e out of n} f_e(t)
         + sum_{e into n}  f_e(t)
```

Where:

- “edge out of n” means `i_e = n`,
- “edge into n” means `j_e = n`,
- `f_e(t)` follows the orientation `(i_e -> j_e)`.

All operations are in **integer arithmetic**. No floats, no rounding beyond the
explicit `floor` in `raw_e`.

### 2.3 Conservation invariant

Define:

```text
sum_pre_u(t)  = sum_n u_n(t-1)
sum_post_u(t) = sum_n u_n(t)
z_check(t)    = sum_pre_u(t)
```

**Invariant (must hold for all ticks):**

```text
sum_pre_u(t) == sum_post_u(t) == z_check(t)
```

If this fails at any tick, the CMP-0 implementation is considered invalid for
that run.

---

## 3. CMP-0 Chain Rule (Loom)

The Loom chain `C_t` is a per-tick integer sequence that ties together
time evolution, used by Loom blocks and NAP envelopes.

### 3.1 s_t for GF-01

For GF-01 under CMP-0:

```text
s_t = 9   for all ticks t >= 1
```

The constant `9` is derived from the GF-01 construction and is treated as a
fixed property of the GF-01 CMP-0 baseline.

### 3.2 Chain update

Let:

- `C_0 = 1234567` (profile seed),
- `M = 1_000_000_007` (profile modulus),
- `a = 17`, `b = 23` (fixed CMP-0 coefficients),
- `seq_t` = per-tick sequence value (for GF-01, typically equal to tick index `t`).

Then for each tick `t >= 1`:

```text
C_t = (a * C_{t-1} + b * s_t + seq_t) mod M
```

For GF-01:

- `s_t = 9`,
- `seq_t = t`,
- `C_1..C_8` are fixed and listed in the GF-01 spec.

### 3.3 Chain invariants

- `C_t` is always in `[0, M-1]`.
- Given the same initial `C_0`, `s_t`, and `seq_t` sequence, `C_t` must be
  deterministic and reproducible across runs.

Any divergence in `C_t` for a fixed input sequence is a failure.

---

## 4. APX and manifest_check (CMP-0 GF-01)

Press/APX compresses one or more **integer sequences** into streams and produces
a manifest with MDL-like stats.

For CMP-0/GF-01, we focus on two streams:

- `S1_post_u_deltas` — state deltas per tick,
- `S2_fluxes` — edge flux sequences per tick.

The **exact grammar and scheme internals** (R/ID/GR) are defined in the APX
spec; here we only state what must be true for GF-01 CMP-0.

### 4.1 Streams and bit-lengths (GF-01)

For the 8-tick window `t = 1..8`, Press/APX must produce:

- A manifest with streams `S1` and `S2`,
- Per-stream code lengths `L_model`, `L_residual`, `L_total`,
- The **total** bit-lengths matching the GF-01 APX sheets.

Specifically for GF-01:

- For window ticks 1–8:
  - `L_total(S1) = 7`
  - `L_total(S2) = 8`
  - `manifest_check = 487809945`
- For window ticks 1–2:
  - `manifest_check = 869911338`
  - Per-stream bit counts as in the APX fixture.

### 4.2 manifest_check semantics

At CMP-0 level, we require:

- `manifest_check` is a deterministic function of:
  - The streams’ contents,
  - Scheme choices per stream,
  - MDL statistics per stream,
  - Basic window metadata (gid, profile, window id, etc.).

For GF-01, an implementation is **valid** if and only if, for the specified
inputs, `manifest_check` exactly matches the values given above.

(Phase 2 / SPEC-005 will tighten the general definition; this doc only pins
the CMP-0/GF-01 behaviour.)

---

## 5. Determinism Requirements

CMP-0 runs must be **bitwise deterministic**:

- For a given topology, profile, initial state, and external inputs (none for GF-01),
  repeating the run must yield identical:
  - UMX tick ledgers,
  - Loom blocks and chain values,
  - APX manifests (`L_*` and `manifest_check`),
  - NAP envelopes.

Formally:

- Let `R1` and `R2` be two runs with identical configuration.
- After canonical serialisation (defined elsewhere), we must have:

```text
bytes(R1) == bytes(R2)
```

Any difference indicates a determinism failure.

---

## 6. GF-01 Baseline Summary

For GF-01 CMP-0 baseline (SPEC-002):

- Topology: GF-01 fixed 6-node, 8-edge graph.
- Profile: CMP-0 with constants:
  - `C0 = 1234567`
  - `M = 1_000_000_007`
  - `SC = 32`
  - `W = 8`
- Initial state: `u(0) = [3, 1, 0, 0, 0, 0]`.
- Flux rule: as in Section 2.
- Chain rule and `s_t`/`seq_t`: as in Section 3.
- APX behaviour and `manifest_check`: as in Section 4.
- Determinism: as in Section 5.

An implementation that satisfies all of the above, and passes the separate
`GF01_V0_Exam.md`, is considered a valid CMP-0 GF-01 baseline engine.
