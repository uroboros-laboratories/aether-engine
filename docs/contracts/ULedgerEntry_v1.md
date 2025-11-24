# ULedgerEntry_v1 — Universal Ledger Entry

## Purpose

`ULedgerEntry_v1` is the **global commit record** that ties together:

- Per-tick engine state (UMX),
- Time-chain state (Loom),
- Compression state (Press/APX),
- Envelope state (NAP),
- Optional learning state (Codex).

It is the unit that a higher-level system can treat as “the canonical record” for a tick (or window) in the Aether engine.

---

## Record Shape

Logical record name: `ULedgerEntry_v1`

Top-level fields:

1. **gid: string**  
   - Graph / run identifier (e.g. `"GF01"`).

2. **run_id: string**  
   - Unique run identifier.

3. **tick: int**  
   - Tick index `t` this entry corresponds to.

4. **window_id: string**  
   - Identifier for the window that contains tick `t` (e.g. `"GF01_W1_ticks_1_8"`).

5. **C_t: int**  
   - Loom chain value at tick `t`.

6. **manifest_check: int**  
   - APX `manifest_check` for the window containing `t`.

7. **nap_envelope_hash: string**  
   - Hash of the `NAPEnvelope_v1` content for tick `t` (e.g. SHA-256 of its canonical JSON).

8. **umx_ledger_hash: string**  
   - Hash of the `UMXTickLedger_v1` for tick `t`.

9. **loom_block_hash: string**  
   - Hash of the `LoomPBlock_v1` for tick `t`.

10. **apx_manifest_hash: string**  
    - Hash of the `APXManifest_v1` for the relevant window.

11. **codex_library_hash: string (optional)**  
    - Hash of the Codex library snapshot after processing tick `t`.

12. **prev_entry_hash: string (optional)**  
    - Hash of the previous `ULedgerEntry_v1` in the run, forming a commit chain.

13. **timestamp_utc: string (optional)**  
    - ISO 8601 timestamp when the entry was committed.

14. **meta: object (optional)**  
    - Additional metadata (e.g. operator annotations, tags, environment info).

---

## Hashing & Canonicalisation

- Hashes should be computed from a **canonical serialisation** of the referenced records:
  - e.g. JSON with:
    - Sorted keys,
    - No extraneous whitespace,
    - Deterministic integer and string encodings.

- The exact hash algorithm (e.g. SHA-256) should be fixed at profile level and documented alongside `Profile_CMP0_v1` or its successors.

An example spec snippet:

```jsonc
{
  "hash_algorithm": "sha256",
  "serialization": "canonical_json_v1"
}
```

---

## Usage in CMP-0 GF-01

For the GF-01 exam, the U-ledger can be implemented in a minimal way:

- Each tick `t` emits a `ULedgerEntry_v1` with:
  - `gid = "GF01"`
  - `run_id = "GF01"`
  - `tick = t`
  - `window_id = "GF01_W1_ticks_1_8"`
  - `C_t` from Loom
  - `manifest_check = 487809945`
  - `nap_envelope_hash` from the NAP envelope for t
  - `umx_ledger_hash` from UMX ledger for t
  - `loom_block_hash` from Loom P-block for t
  - `apx_manifest_hash` from the APX manifest for ticks 1..8
  - `prev_entry_hash` = hash of the previous entry (or empty/zero for t=1)

This produces a simple, append-only commit chain over the run.

---

## Invariants

- The sequence of `ULedgerEntry_v1` entries for a run must:
  - Have strictly increasing `tick` values.
  - Have `prev_entry_hash` forming a valid hash chain (if enabled).

- For each entry:
  - `C_t` must match the Loom P-block for tick `t`.
  - `manifest_check` must match the APX manifest for the window including `t`.
  - The referenced hashes must be consistent with the actual records.

`ULedgerEntry_v1` gives the system a single, immutable reference per tick/window that a higher-level coordinator or auditor can rely on.
