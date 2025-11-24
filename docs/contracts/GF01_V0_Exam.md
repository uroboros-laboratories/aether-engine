# GF-01 V0 Exam — Digital Parity Acceptance Criteria

## Purpose

GF-01 is the **golden fixture** for validating the first digital implementation of:

- UMX (integer engine),
- Loom (time chain + blocks),
- Press/APX (compression & manifest),
- NAP (envelopes / payload_ref).

This document defines the **exam conditions** a codebase must pass to be considered parity with the paper V0 implementation under profile **CMP-0**.

---

## Given

From the Aether system build plan and GF-01 materials:

1. **Profile CMP-0 constants:**
   - `M = 1_000_000_007` (Loom modulus).
   - `C_0 = 1_234_567` (initial Loom chain value).
   - `SC = 32` (scale constant for UMX flux).
   - Edge list with IDs 1..8, associated `k_e` and `cap_e` values.
   - I-block spacing `W = 8`.

2. **Topology:**
   - N = 6 nodes.
   - 8 edges connecting them, as per the GF-01 topology card.

3. **Initial state:**
   - `u(0) = [3, 1, 0, 0, 0, 0]` in canonical node order.

4. **Tick range:**
   - Ticks `t = 1..8`.

The paper V0 worked examples provide full tables for:

- `pre_u` at each tick,
- Edge `du`, `raw`, `f_e`,
- `post_u` at each tick,
- Loom summaries `s_t`, chain values `C_t`,
- APX streams, bit-counts, and manifest checks,
- NAP envelopes with `payload_ref` and `prev_chain`.

---

## Must-Haves (Pass/Fail Conditions)

To pass the GF-01 V0 exam, a digital implementation must satisfy **all** of the following:

### 1. UMX — UMXTickLedger_v1 parity

For ticks 1..8:

- The engine produces a `UMXTickLedger_v1` record per tick.
- For each tick `t`:

  1. `pre_u` matches the paper table exactly.
  2. For every edge:
     - `du`, `raw`, and `f_e` match the paper table.
  3. `post_u` matches the paper table exactly.
  4. `sum_pre_u`, `sum_post_u`, and `z_check` satisfy:
     - `sum_pre_u == sum_post_u == z_check`
     - And these sums match the GF-01 worked example values.

Any mismatch in a single entry is a **hard fail** for UMX parity.

---

### 2. Loom — LoomPBlock_v1 and LoomIBlock_v1 parity

Given the same UMX tick sequence and CMP-0 constants:

- The Loom implementation must emit:

  1. `LoomPBlock_v1` for each tick 1..8 with:
     - `tick = t`
     - `seq = t`
     - `s_t` matching the GF-01 scalar summary (constant 9 for each tick in V0).
     - `C_t` matching the GF-01 chain sequence:

       ```text
       C_1..C_8 = [
         20987847,
         356793608,
         65491504,
         113355772,
         927048329,
         759821701,
         916969047,
         588473909
       ]
       ```

  2. One `LoomIBlock_v1` at tick 8 with:
     - `tick = 8`
     - `W = 8`
     - `C_t = 588473909`
     - `profile_version = "CMP-0"`
     - `post_u` equal to the UMX `post_u` at tick 8
     - `topology_snapshot` equal to the original topology card.

Any discrepancy in `C_t`, `s_t`, or the I-block payload is a **hard fail** for Loom parity.

---

### 3. Press/APX — APXManifest_v1 parity

For the full 8-tick window (ticks 1..8):

- Press must construct an APX capsule with an `APXManifest_v1` that:

  1. Has `apx_name = "GF01_APX_v0_full_window"`.
  2. Has `profile = "CMP-0"`.
  3. Contains the same two streams as the paper example:
     - `"S1_post_u_deltas"`
     - `"S2_fluxes"`
  4. Uses scheme `"R"` for both streams.
  5. Produces the same `L_total` bit counts per stream:
     - `L_total(S1) = 7`
     - `L_total(S2) = 8`
  6. Produces exactly:

     ```text
     manifest_check = 487809945
     ```

For the short 2-tick window (ticks 1..2):

- A second APX manifest with:

  1. `apx_name = "GF01_APX_v0_ticks_1_2"`
  2. `profile = "CMP-0"`
  3. Same two streams, truncated to ticks 1..2.
  4. The paper’s scheme choices and bit counts.
  5. Exactly:

     ```text
     manifest_check = 869911338
     ```

Any deviation in bit counts or manifest_check is a **hard fail** for Press/APX parity.

---

### 4. NAP — NAPEnvelope_v1 parity

Over the 8-tick window:

- For each tick t=1..8, a `NAPEnvelope_v1` is emitted with:

  1. `v = 1`
  2. `tick = t`
  3. `gid = "GF01"`
  4. `nid = "N/A"` (or the chosen stable node ID)
  5. `layer = "DATA"`
  6. `mode = "P"`
  7. `payload_ref = 487809945`
  8. `seq = t`
  9. `prev_chain = C_{t-1}` (with C_0 = 1234567)
  10. `sig` set to some deterministic placeholder (e.g. empty string)

This means, concretely, `prev_chain` must follow:

```text
prev_chain(1) = 1234567
prev_chain(2) = 20987847
prev_chain(3) = 356793608
prev_chain(4) = 65491504
prev_chain(5) = 113355772
prev_chain(6) = 927048329
prev_chain(7) = 759821701
prev_chain(8) = 916969047
```

Any mismatch in these envelope fields, especially `payload_ref` and `prev_chain`, is a **hard fail** for NAP parity.

---

### 5. Determinism

Finally, the entire system must be **bitwise deterministic**:

- Running the code twice with the same configuration and inputs MUST produce:
  - The same UMXTickLedger_v1 sequence,
  - The same LoomPBlock_v1 and LoomIBlock_v1,
  - The same APXManifest_v1 records,
  - The same NAPEnvelope_v1 stream.

No randomness, no floating-point drift, no ordering-dependent nondeterminism is allowed.

---

## Outcome

If an implementation passes all of the above:

- You have a **digitally faithful V1** of the Aether core loop (UMX + Loom + Press + NAP) under CMP-0.
- You can safely refactor internals as long as tests continue to enforce these fixtures.
- Future profiles (richer compression, more complex MDL, Codex integration) can be layered on top without breaking the GF-01 baseline.
