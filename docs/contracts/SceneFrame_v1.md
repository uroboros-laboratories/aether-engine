# SceneFrame_v1 — Minimal Gate/TBP Scene Record

## Purpose

`SceneFrame_v1` is a minimal, implementation-facing record that Gate/TBP can use to:

- Summarise what happened during a tick,
- Provide a stable surface for NAP envelope emission,
- Offer a hook for richer “scenes” later (external inputs, observations, etc.).

In CMP-0 GF-01, external inputs are trivial, so `SceneFrame_v1` is mostly a convenient bundle of the core artefacts for a tick.

---

## Record Shape

Logical record name: `SceneFrame_v1`

Top-level fields:

1. **gid: string**  
   - Graph/run identifier (e.g. `"GF01"`).

2. **run_id: string**  
   - Unique run identifier; may be equal to `gid` for simple runs.

3. **tick: int**  
   - Tick index `t ≥ 1`.

4. **nid: string**  
   - Engine/node identifier for Gate; for GF-01, `"N/A"` or a simple engine ID string.

5. **pre_u: int[N]**  
   - State before UMX tick `t` (copied from `UMXTickLedger_v1.pre_u`).

6. **post_u: int[N]**  
   - State after UMX tick `t` (copied from `UMXTickLedger_v1.post_u`).

7. **ledger_ref: string**  
   - Logical reference to the `UMXTickLedger_v1` record for this tick.  
   - Implementation detail (could be a hash, file path, or in-memory ID).

8. **C_prev: int**  
   - Loom chain value from previous tick, `C_{t-1}`.

9. **C_t: int**  
   - Loom chain value after this tick, `C_t`.

10. **window_id: string**  
    - Identifier for the window this tick belongs to (e.g. `"GF01_W1_ticks_1_8"`).

11. **manifest_check: int (optional)**  
    - `manifest_check` for the APX manifest associated with this window.  
    - When a window is partially filled, this may still reference the previous window’s manifest or be left as a sentinel.

12. **nap_envelope_ref: string (optional)**  
    - Logical reference to the `NAPEnvelope_v1` emitted for this tick.

13. **meta: object (optional)**  
    - Free-form metadata (e.g. external inputs, annotations, debug info).

---

## Usage in CMP-0 GF-01

In a simple GF-01 run, the tick loop can materialise a `SceneFrame_v1` after UMX and Loom steps:

1. Construct the frame:

   ```jsonc
   {
     "gid": "GF01",
     "run_id": "GF01",
     "tick": t,
     "nid": "engine0",
     "pre_u": ledger_t.pre_u,
     "post_u": ledger_t.post_u,
     "ledger_ref": "umx_ledger_t",
     "C_prev": C_prev,
     "C_t": C_t,
     "window_id": "GF01_W1_ticks_1_8",
     "manifest_check": 487809945,
     "nap_envelope_ref": "nap_env_t",
     "meta": {}
   }
   ```

2. Use fields from this frame to populate `NAPEnvelope_v1`:
   - `gid`, `nid`, `tick` carry over directly.
   - `prev_chain = C_prev`.
   - `payload_ref = manifest_check`.

3. Persist or stream the scene frame for inspection, debugging, or as a source for richer Gate/TBP implementations later.

---

## Invariants

- `pre_u` and `post_u` must match the corresponding `UMXTickLedger_v1` record for this tick.
- `C_prev` and `C_t` must match the Loom P-block (`LoomPBlock_v1`) for this tick.
- `manifest_check`, if present, must match the `APXManifest_v1` for the window that includes this tick.
- `window_id` must be consistent across all ticks in the same window.

`SceneFrame_v1` is intentionally minimal and strongly typed so it can evolve into a richer Gate/TBP scene record without breaking existing code.
