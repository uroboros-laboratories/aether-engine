# TickLoop_v1 — Core Per-Tick Runbook

## Purpose

`TickLoop_v1` describes the **canonical per-tick flow** of the Aether engine under CMP-0:

1. Gate/TBP prepares inputs (trivial for GF-01).
2. UMX executes one tick and emits a `UMXTickLedger_v1`.
3. Loom ingests the ledger and updates `C_t`, emitting `LoomPBlock_v1` and optionally `LoomIBlock_v1`.
4. Press/APX compresses streams over windows and emits `APXManifest_v1`.
5. Gate issues `NAPEnvelope_v1` for the tick.
6. (Optional) U-ledger and Codex read/observe.

This is expressed as a **logical contract**, not as code.

---

## Context Objects

The tick loop uses the following context objects:

- `TopologyProfile_v1 topo`
- `Profile_CMP0_v1 profile`
- `state`: current state vector `u(t-1)` (int[N])
- `C_prev`: previous Loom chain value `C_{t-1}`
- `window_state`: window buffers for Press/APX (e.g. post_u deltas, flux sequences)
- `window_config`: window size `W` and current position
- `run_id` / `gid`: run identifiers for NAP and U-ledger

---

## Logical Procedure

We define an abstract function:

```text
TickLoop_v1(t, state, C_prev, topo, profile, window_state) -> outputs
```

Where `t` is the tick index (1-based).

### Step 1 — Gate/TBP Input Preparation (CMP-0 minimal)

For GF-01:

- There are no external inputs; the engine is purely driven by initial conditions and its own dynamics.
- Gate’s role at this stage is:

  - Maintain `gid` (e.g. `"GF01"`),
  - Maintain `nid` (e.g. `"N/A"`),
  - Forward `t` to the engine stack.

In a more general system, this is where you would:

- Read external inputs,
- Normalise them via PFNA,
- Prepare a full scene frame.

### Step 2 — UMX Tick

Call the UMX engine:

```text
ledger_t = UMX.step(t, state, topo, profile)
```

Where `ledger_t` is a `UMXTickLedger_v1`:

- Contains `pre_u`, `edges[du, raw, f_e]`, and `post_u`,
- Satisfies conservation checks.

Update current state:

```text
state_next = ledger_t.post_u
```

### Step 3 — Loom Update (P-block and chain)

Compute the per-tick scalar summary `s_t` using `profile.s_t_rule`:

```text
s_t = compute_s_t(state_next, profile)
```

Compute `seq_t`:

- For CMP-0 GF-01, `seq_t = t`.

Update the Loom chain:

```text
C_t = (17 * C_prev + 23 * s_t + seq_t) mod profile.modulus_M
```

Emit a `LoomPBlock_v1`:

- `tick = t`
- `seq = seq_t`
- `s_t = s_t`
- `C_t = C_t`
- Optional `edge_flux_summary` derived from `ledger_t.edges`.

Checkpoint (`LoomIBlock_v1`) if `t % W == 0`:

```text
if (t % profile.I_block_spacing_W == 0):
    emit I-block with:
      tick = t
      W = profile.I_block_spacing_W
      C_t = C_t
      profile_version = profile.name
      post_u = state_next
      topology_snapshot = topo.edges (plus any node/topology metadata)
```

### Step 4 — Press/APX Window Update

Update the window buffers:

- Append any required values from `ledger_t` and/or `state_next`:
  - e.g. post_u deltas,
  - flux sequences.

If this tick **closes a window** (e.g. `t % W == 0` for a full W-tick window):

1. Build an `APXManifest_v1`:
   - For GF-01:
     - `apx_name = "GF01_APX_v0_full_window"` (or ticks_1_2 etc.)
     - `profile = profile.name`
     - Two streams:
       - `S1_post_u_deltas`
       - `S2_fluxes`
     - Scheme `"R"` for both.
     - Calculate `L_model`, `L_residual`, `L_total`.
     - Compute `manifest_check`.

2. Clear or roll the window buffers as appropriate for the next window.

### Step 5 — NAP Envelope Emission

Using the `APXManifest_v1` for the current window, set:

- `payload_ref = manifest_check`.

For tick `t`, emit a `NAPEnvelope_v1`:

```text
envelope_t = {
  v: profile.nap_defaults.v,     // e.g. 1
  tick: t,
  gid: run_id or topo.gid,
  nid: "N/A" or chosen engine ID,
  layer: profile.nap_defaults.layer,   // "DATA"
  mode: profile.nap_defaults.mode,     // "P"
  payload_ref: manifest_check_for_window_containing_t,
  seq: seq_t,
  prev_chain: C_prev,
  sig: "" // or witness placeholder
}
```

Note:

- `prev_chain` uses **C_prev** (i.e. `C_{t-1}`), not `C_t`.

### Step 6 — (Optional) U-Ledger and Codex

In later phases:

- An `ULedgerEntry_v1` ties together:
  - `tick`,
  - `C_t`,
  - `manifest_check`,
  - `envelope_t` reference,
  - any Codex library hashes.

Codex can consume:

- The full sequence of `UMXTickLedger_v1`,
- Loom blocks,
- APX manifests,

to build library entries and proposals.

---

## Outputs

At minimum, for tick `t`, `TickLoop_v1` yields:

- Updated state: `state_next`,
- Updated Loom chain: `C_t`,
- `UMXTickLedger_v1` record: `ledger_t`,
- `LoomPBlock_v1` record, maybe `LoomIBlock_v1`,
- `APXManifest_v1` when a window closes,
- `NAPEnvelope_v1` for this tick.

In practice, you may also update:

- Window state,
- U-ledger entries,
- Codex artefacts (later phases).

---

## GF-01 Specific Notes

For the **GF-01 CMP-0 exam**:

- Topology is the fixed 6-node, 8-edge graph.
- `s_t = 9` for all ticks,
- `seq_t = t`,
- `C_0 = 1_234_567`,
- Window size `W = 8`,
- `manifest_check = 487809945` for ticks 1..8,
- NAP envelopes use `payload_ref = 487809945` and `prev_chain` equal to the previous `C_t`.

A digital implementation that follows `TickLoop_v1` and the other contracts exactly will reproduce the paper GF-01 tables bit-for-bit.
