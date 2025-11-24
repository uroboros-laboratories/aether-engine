# GF-01 V0 Exam (CMP-0 Baseline) — v1

## Status

- **Graph ID:** GF-01
- **Profile:** CMP-0
- **Scope:** Ticks 1–8 (inclusive)
- **Purpose:** Define the exam that a digital implementation must pass to be
  recognised as a valid CMP-0 GF-01 baseline engine (SPEC-002).

This doc is the canonical, test-friendly definition of “passing GF-01”. Tests
for Phase 1 (SPEC-002) should reference this document.

---

## 1. Inputs and Configuration

A valid GF-01 exam run must use:

- Topology: GF-01, 6 nodes, 8 edges with the exact `(i, j, k, cap, SC, c)`
  values from the GF-01 spec/fixtures.
- Profile: CMP-0 with:
  - `C0 = 1234567`
  - `M = 1_000_000_007`
  - `SC = 32`
  - `W = 8`
- Initial state:
  - `u(0) = [3, 1, 0, 0, 0, 0]`
- Ticks:
  - Run ticks `t = 1..8` (inclusive).
- External inputs:
  - None (no PFNA or external channels for this exam).

The run must use the CMP-0 physics as defined in
`Aether_CMP0_Physics_Core_and_Invariants_v1.md`.

---

## 2. Exam Sections

A run passes the GF-01 exam if and only if it passes **all** of the following
sections:

1. UMX parity
2. Loom parity
3. Press/APX parity
4. NAP parity
5. Determinism

Each section below specifies what must match and what constitutes failure.

---

## 3. UMX Parity (Section U)

For ticks `t = 1..8`, the UMX engine must produce tick ledgers that match the
GF-01 tick tables exactly.

### 3.1 Per-tick state

For each `t`:

- `pre_u(t)` = `u(t-1)`
- `post_u(t)` = `u(t)`

**Requirement:**

- `pre_u(t)` and `post_u(t)` must exactly match the GF-01 V0 worked examples.

### 3.2 Per-edge flux details

For each tick `t` and each edge `e`:

- `du_e(t)`
- `raw_e(t)`
- `f_e(t)`

**Requirement:**

- `du_e(t)`, `raw_e(t)`, and `f_e(t)` must match the GF-01 tables for all edges
  and ticks.

### 3.3 Conservation

For each tick `t`:

- Let `sum_pre_u(t) = sum_n pre_u_n(t)`,
- Let `sum_post_u(t) = sum_n post_u_n(t)`,
- Let `z_check(t)` be the GF-01 reference value.

**Requirements:**

- `sum_pre_u(t) == sum_post_u(t) == z_check(t)`,
- `z_check(t)` must match the GF-01 reference.

Failure of any equality in this section fails the exam.

---

## 4. Loom Parity (Section L)

The Loom chain and block outputs must match the GF-01 reference.

### 4.1 Chain values

For ticks `t = 1..8`, let `C_t` be the chain values produced by Loom.

**Requirement:**

- The vector `C_1..C_8` must exactly match the GF-01 reference chain values
  listed in the GF-01 fixtures/spec.

### 4.2 I-block at t = 8

At `t = 8`, Loom must emit an `I-block` containing:

- `C_8`,
- A snapshot of `post_u(8)`,
- A snapshot of the GF-01 topology (or a reference thereto, as defined by the
  Loom contracts).

**Requirements:**

- `C_8` matches the GF-01 reference,
- The state snapshot equals `post_u(8)` from UMX,
- The topology snapshot matches the GF-01 topology.

Any mismatch fails the exam.

---

## 5. Press/APX Parity (Section P)

Press/APX must produce manifests that match the GF-01 reference values.

### 5.1 Window 1–8

For the tick window `t = 1..8`, using:

- `S1_post_u_deltas`,
- `S2_fluxes`,

as defined in the APX spec, the manifest must satisfy:

- `L_total(S1) = 7`
- `L_total(S2) = 8`
- `manifest_check = 487809945`

Any deviation from these numbers fails the exam.

### 5.2 Window 1–2

For the tick window `t = 1..2`, the manifest must satisfy:

- `manifest_check = 869911338`
- Per-stream MDL stats and bit counts matching the GF-01 APX fixture.

Any deviation fails the exam.

---

## 6. NAP Parity (Section N)

NAP envelopes must match the GF-01 envelope sheet exactly.

For ticks `t = 1..8`, let `E_t` be the envelope for tick `t`. Each `E_t` includes:

- `v`
- `gid`
- `layer`
- `mode`
- `payload_ref`
- `seq`
- `prev_chain`
- `sig` (signature)

**Requirements:**

- `v = 1` for all `t`,
- `gid = "GF01"` for all `t`,
- `layer = "DATA"`, `mode = "P"` for all `t`,
- `payload_ref` equals the 1–8 window `manifest_check` (`487809945`),
- `seq = t`,
- `prev_chain(1) = C_0 = 1234567`,
- For `t >= 2`: `prev_chain(t) = C_{t-1}`,
- `sig` may be an empty string or placeholder value, as specified in the NAP contract,
  but must be deterministic given the run configuration.

Any mismatch with the GF-01 envelope sheet fails the exam.

---

## 7. Determinism (Section D)

Given a fixed configuration (topology, profile, initial state, no external
inputs), running the exam twice must produce **bitwise identical** outputs.

Let `R1` and `R2` be two runs with identical config, and let:

- `U1`, `U2` be the UMX ledgers,
- `L1`, `L2` be the Loom blocks,
- `A1`, `A2` be the APX manifests,
- `N1`, `N2` be the NAP envelopes.

After canonical serialisation:

```text
bytes(U1, L1, A1, N1) == bytes(U2, L2, A2, N2)
```

**Requirement:**

- Any difference indicates a determinism failure and fails the exam.

---

## 8. Overall Pass/Fail

A run **passes** the GF-01 V0 exam if and only if:

- It uses the correct configuration (Section 1),
- It passes UMX parity (Section 3),
- It passes Loom parity (Section 4),
- It passes Press/APX parity (Section 5),
- It passes NAP parity (Section 6),
- It passes the determinism check (Section 7).

Any failure in any section fails the exam.

This document is intended to be stable; changes should be versioned (v2, v3, …)
and treated as spec updates.
