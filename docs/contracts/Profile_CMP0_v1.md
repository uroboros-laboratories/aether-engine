# Profile_CMP0_v1 — CMP-0 Numeric Profile

## Purpose

`Profile_CMP0_v1` defines the numeric constants and update rules for the **CMP-0** profile:

- UMX flux computation,
- Loom chain update,
- I-block spacing for checkpoints,
- Any fixed defaults relevant to GF-01.

This profile is **integer-only** and is the simplest “paper parity” profile.

---

## Record Shape

Logical record name: `Profile_CMP0_v1`

Top-level fields:

1. **name: string**  
   - MUST be `"CMP-0"` for this profile.

2. **modulus_M: int**  
   - Large prime modulus for Loom chain.  
   - Default: `1_000_000_007`.

3. **C0: int**  
   - Initial Loom chain value `C_0`.  
   - GF-01: `C0 = 1_234_567`.

4. **SC: int**  
   - Global scale constant for UMX flux computation.  
   - GF-01: `SC = 32`.

5. **I_block_spacing_W: int**  
   - Number of ticks between I-block checkpoints.  
   - GF-01: `W = 8`.

6. **flux_rule: object**  
   - Encodes the UMX flux update rule for documentation and self-description.

7. **chain_rule: object**  
   - Encodes the Loom chain update rule.

8. **s_t_rule: object**  
   - Describes how `s_t` (per-tick scalar summary) is derived from state.

9. **nap_defaults: object (optional)**  
   - Default NAP envelope settings for this profile (e.g. `v`, `layer`, `mode`).

10. **press_defaults: object (optional)**  
    - Default Press/APX settings (e.g. preferred schemes).

---

## flux_rule (UMX)

For CMP-0, the UMX flux rule is:

```text
Given:
  - TopologyProfile_v1 with edge parameter k_e and SC
  - Pre-tick state vector pre_u (integers)

For each edge e = (i, j):

  du_e   = pre_u[i] - pre_u[j]
  mag    = abs(du_e)
  raw_e  = floor(k_e * mag / SC)
  cap_e  = topology.cap for this edge
  f_e    = sign(du_e) * min(raw_e, cap_e, mag)

Then for each node i:

  post_u[i] = pre_u[i] + sum_e contribution from f_e
```

In JSON-like form:

```jsonc
"flux_rule": {
  "type": "CMP0_flux_v1",
  "du_formula": "du = pre_u[i] - pre_u[j]",
  "raw_formula": "raw = floor(k * abs(du) / SC)",
  "f_e_formula": "f_e = sign(du) * min(raw, cap, abs(du))",
  "conservation": "sum(pre_u) == sum(post_u)"
}
```

All arithmetic is integer-only; divisions use floor.

---

## chain_rule (Loom)

For CMP-0, the Loom chain rule is:

```text
C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M
```

Where:

- `C_0 = C0` from the profile,
- `s_t` is the scalar summary for tick t,
- `seq_t` is the envelope/sequence number (usually `t` for simple runs),
- `M = modulus_M`.

JSON-like representation:

```jsonc
"chain_rule": {
  "type": "CMP0_chain_v1",
  "update": "C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M",
  "constants": {
    "a": 17,
    "b": 23
  }
}
```

---

## s_t_rule (Loom summary)

For CMP-0 GF-01, `s_t` is a simple, deterministic function of the state:

- In the paper GF-01 example, `s_t` is a constant 9 derived from a prime-weighted sum over the occupied nodes.
- For digital CMP-0, it is sufficient to define:

```jsonc
"s_t_rule": {
  "type": "CMP0_s_t_v1",
  "description": "A fixed deterministic integer derived from state; for GF-01, s_t = 9 for all ticks.",
  "gf01_constant": 9
}
```

A later refinement can implement the full prime-weighted scheme; for parity with V0 we only require `s_t = 9` on GF-01.

---

## nap_defaults (optional)

Useful for initialising `NAPEnvelope_v1`:

```jsonc
"nap_defaults": {
  "v": 1,
  "layer": "DATA",
  "mode": "P"
}
```

---

## press_defaults (optional)

For GF-01 V0, the APX manifests use:

- Scheme `"R"` for both streams,
- Minimal model overhead.

You can encode this as:

```jsonc
"press_defaults": {
  "preferred_schemes": ["R", "GR", "ID"],
  "gf01_streams": [
    "S1_post_u_deltas",
    "S2_fluxes"
  ]
}
```

---

## Invariants

For CMP-0:

- All state and flux values are integers.
- All updates are deterministic given the same inputs, topology, and profile.
- `sum(pre_u) == sum(post_u)` at every tick.
- The Loom chain `C_t` is uniquely determined by `(C_0, s_1..s_t, seq_1..seq_t, M)`.
