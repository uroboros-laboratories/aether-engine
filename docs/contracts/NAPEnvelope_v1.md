# NAPEnvelope_v1 Contract

## Purpose

`NAPEnvelope_v1` is the canonical wrapper for per-tick payloads across the Aether / Trinity system.  
It provides a stable, deterministic surface that Gate, UMX, Loom, Press, and Codex can all agree on.

This is the bridge between:
- The **paper V0 forms** (A1 envelopes) and
- The **digital implementation** (structs / JSON records).

---

## Record Shape

Logical record name: `NAPEnvelope_v1`

Fields (canonical key order):

1. **v: int**  
   - Schema version of the envelope.  
   - For GF-01 V0, this MUST be `1`.

2. **tick: int**  
   - Global tick index `t ≥ 1` within the run.

3. **gid: string**  
   - Graph/run ID.  
   - For GF-01, this MUST be `"GF01"`.

4. **nid: string**  
   - Node/engine ID.  
   - For the single-engine GF-01 fixture you can use `"N/A"` (or a stable ID string).

5. **layer: enum { "INGRESS", "EGRESS", "CTRL", "DATA" }**  
   - Logical layer of this envelope.
   - GF-01 uses `"DATA"`.

6. **mode: enum { "I", "P" }**  
   - `"I"` for I-block (checkpoint) windows.  
   - `"P"` for P-block (per-tick) entries within a window.  
   - GF-01 uses `"P"` for ticks 1–8 in the worked examples.

7. **payload_ref: int**  
   - Decimal check value from the APX Manifest (`manifest_check`) of the current window.  
   - No raw state goes here; it is **only** a reference.

8. **seq: int**  
   - Monotone sequence number per envelope.  
   - In GF-01, this is simply `seq = tick`.

9. **prev_chain: int**  
   - Previous Loom chain value `C_{t-1}`.  
   - For tick 1, this is the profile’s starting `C_0`.  
   - For tick t>1, this is the `C_{t-1}` that Loom computed.

10. **sig: string**  
    - Signature / witness field.  
    - On paper V0 this is just human text (e.g. initials, “witness at I-block”).  
    - Digitally this can start as an empty string, and later be upgraded to a cryptographic signature.

---

## Canonical Digital Representation

In code, treat this as a struct or JSON object with exactly these fields:

```jsonc
{
  "v": 1,
  "tick": 1,
  "gid": "GF01",
  "nid": "N/A",
  "layer": "DATA",
  "mode": "P",
  "payload_ref": 487809945,
  "seq": 1,
  "prev_chain": 1234567,
  "sig": ""
}
```

### Invariants

For every envelope E at tick `t`:

- `E.tick == t`
- `E.seq` is strictly increasing per run and unique per envelope.  
  - In the GF-01 fixture: `E.seq == t`.
- `E.prev_chain == C_{t-1}` where `C_t` is Loom’s hash chain.

For any complete window W:

- All envelopes in W share the same `payload_ref`, equal to the APX `manifest_check` of that window.

### GF-01 Specific Values

For the GF-01 8-tick window (ticks 1–8):

- `gid = "GF01"`
- `layer = "DATA"`
- `mode = "P"` for every tick.
- `payload_ref = 487809945` for every tick in 1..8.
- `seq = tick`.
- `prev_chain` sequence is `[C_0, C_1, ..., C_7]` with:
  - `C_0 = 1234567`
  - `C_1..C_8` as defined in the Loom contract.

Any implementation that claims parity with V0 must emit NAP envelopes that match this fixture exactly for GF-01.
