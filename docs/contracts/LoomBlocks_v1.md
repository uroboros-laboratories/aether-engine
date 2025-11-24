# LoomPBlock_v1 and LoomIBlock_v1 Contracts

## Purpose

The Aevum Loom records the evolution of the engine state over time as a sequence of blocks:

- **P-blocks**: Per-tick records that update the Loom hash chain.
- **I-blocks**: Checkpoints that capture full state + topology at a given tick.

`LoomPBlock_v1` and `LoomIBlock_v1` are the canonical shapes for these blocks.

---

## LoomPBlock_v1

Logical record name: `LoomPBlock_v1`

Fields:

1. **tick: int**  
   - Tick index `t ≥ 1` that this P-block corresponds to.

2. **seq: int**  
   - Sequence number aligned with the corresponding NAP envelope.  
   - In GF-01, `seq = tick`.

3. **s_t: int**  
   - Per-tick scalar summary used as input into the Loom chain.  
   - For CMP-0, this is derived from the state using a simple scheme (GF-01 uses a constant 9 as the sum over the chosen prime weights for the occupied nodes).

4. **C_t: int**  
   - Loom chain value at tick `t`.

5. **edge_flux_summary: list<FluxSummary_v1> (optional)**  
   - Optional per-edge summary of the tick’s fluxes, for convenience and introspection:
     - `e_id: int`
     - `f_e: int`

The P-blocks do **not** attempt to encode full state or topology; they are the minimal per-tick “breadcrumb” for the chain and optional summaries.

### FluxSummary_v1

- **e_id: int**  
- **f_e: int**

---

## LoomIBlock_v1

Logical record name: `LoomIBlock_v1`

Fields:

1. **tick: int**  
   - Tick index of the checkpoint (e.g. `t = 8` for the GF-01 example).

2. **W: int**  
   - I-block spacing (window size).  
   - For GF-01, `W = 8`.

3. **C_t: int**  
   - Loom chain value at this checkpoint tick.

4. **profile_version: string**  
   - Loom / compression profile in effect, e.g. `"CMP-0"`.

5. **post_u: int[N]**  
   - Full engine state at this checkpoint, matching the UMX `post_u` at tick `t`.

6. **topology_snapshot: list<TopologyEdge_v1>**  
   - A frozen copy of the topology + key constants at the checkpoint:
     - `e_id: int`
     - `i: int`
     - `j: int`
     - `k: int`
     - `cap: int`
     - `SC: int`
     - `c: int` (any additional per-edge constant, if present)

### TopologyEdge_v1

- **e_id: int**  
- **i: int**  
- **j: int**  
- **k: int**  
- **cap: int**  
- **SC: int**  
- **c: int**

---

## Chain Update Rule (CMP-0)

For every tick `t ≥ 1`, the Loom chain value is updated as:

```text
C_t = (17 * C_{t-1} + 23 * s_t + seq) mod M
```

Where:

- `C_0` is the starting chain value from the profile.
- `s_t` is the per-tick scalar summary.
- `seq` is the envelope/sequence number (GF-01: `seq = t`).
- `M` is a large prime modulus; in CMP-0, `M = 1_000_000_007`.

---

## GF-01 Specific Fixture

Profile CMP-0 for GF-01 defines:

- `C_0 = 1234567`
- `M = 1_000_000_007`
- I-block spacing `W = 8`

Given the worked examples, the Loom chain values for t=1..8 are:

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

and the I-block at t=8 captures:

- `tick = 8`
- `W = 8`
- `C_8 = 588473909`
- `profile_version = "CMP-0"`
- `post_u` equal to the UMX `post_u` at tick 8.
- `topology_snapshot` identical to the topology card used in GF-01.

**Acceptance for digital parity:**

Given the same UMXTickLedger_v1 sequence and CMP-0 constants, a Loom implementation must:

- Produce `s_t` and `C_t` that match GF-01 for ticks 1..8.
- Emit a `LoomIBlock_v1` at t=8 whose fields match the paper V0 checkpoint exactly.
