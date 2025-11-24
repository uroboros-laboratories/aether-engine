# Aether Engine — Existing Contracts Index (v1)

This is a quick map of **contracts you already have** inside the pillar packs,
vs the more generic names we’ve been using in the new planning docs.

It’s not exhaustive, just a starting index.

---

## 1. UMX pillar (Universal Matrix)

From `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md` and its
embedded files you already have a bunch of contract-style docs, e.g.:

- `umx_two_phase_tick_contract_v1.md`
- `umx_tick_event_broadcast_contract_v1.md`
- `umx_nap_bus_contract_v1.md`
- `umx_node_manifest_v1.md`
- `umx_slp_snapshot_ir_v1.md`
- `umx_u_ledger_contract_v1.md`
- (and more in the integration / stress_emergence / tbp folders)

These cover many of the roles we’re now calling, more generically:

- **UMXTickLedger_v1**  → tick-level UMX output (per-edge flux, pre/post_u, sums).  
- **ULedgerEntry_v1**   → UMX part of the universal ledger chain.  
- **UMX↔NAP bus**       → how UMX hands data into Gate/NAP.

The new names aren’t replacing these — they’re *wrapping* / standardising them
so the cross-pillar repo can talk about common types in one place.

---

## 2. Astral Press pillar (Press/APX)

From `astral_press_master_implementation_spec_combined_v1.md` and the APX
implementation pack, you already have things like:

- APX stream/manifest contracts,
- MDL accounting layouts,
- Scheme descriptions (R-mode etc.).

These correspond to the more generic contracts we’ve been using in planning:

- **APXStream_v1**      → one compressed integer sequence + MDL stats.  
- **APXManifest_v1**    → a bundle of streams + window metadata + manifest_check.

Again, the plan is not to throw away the Astral Press contracts, but to:

- Extract the core shape (fields + invariants),
- Give it a neutral name under `docs/contracts/`,
- Keep all the rich APX-specific detail in the pillar spec.

---

## 3. Trinity Gate / TBP pillar

From `trinity gate full spec.txt` (and the pillar zip) you already have:

- Gate / TBP integration contracts,
- NAP bus concepts,
- Some envelope and scene-ish structures.

Those align with the generic contracts:

- **NAPEnvelope_v1**    → what actually gets sent as an envelope.  
- **SceneFrame_v1**     → the per-tick integration bundle Gate sees.  
- **TickLoop_v1**       → “who calls who” per tick.

The Trinity docs are the detailed story; the generic contracts become the small,
language-agnostic shapes code and tests are allowed to rely on.

---

## 4. Aevum Loom & Codex Eterna pillars

The Aevum Loom and Codex master specs already describe:

- Loom blocks (P-blocks, I-blocks),
- Chain behaviour,
- Codex library/motif/proposal structures.

These map roughly to:

- **LoomPBlock_v1**, **LoomIBlock_v1**
- **CodexLibraryEntry_v1**
- **CodexProposal_v1**

The work left is mostly:

- Extracting those shapes into dedicated `*_v1.md` contract files under
  `docs/contracts/`,
- Keeping their field names and invariants consistent with the pillar text.

---

## 5. What’s “new” vs what’s already there

So to answer the “don’t we already have some?” question:

- ✅ Yes — you already have **lots** of contract-like docs embedded in the pillar packs.  
- 🔄 What we’re doing now is:
  - Introducing a **clean, cross-pillar naming layer** (`TopologyProfile_v1`, `UMXTickLedger_v1`, `SceneFrame_v1`, etc.).
  - Making tiny, focused contract files in `docs/contracts/` that:
    - Point back to the pillar specs as the detailed story,
    - Give code/tests a single, unambiguous shape to implement/assert.

### 5.1 Contracts we’ve effectively defined but not split out yet

These are the “core three” we called out for Sprint 1, plus a few others:

- `TopologyProfile_v1`   — implied by UMX topology docs and GF-01, not yet a standalone contract file.
- `Profile_CMP0_v1`      — effectively defined in the physics/core docs, but not split out as its own contract file.
- `UMXTickLedger_v1`     — strongly implied by the UMX implementation/contract docs, but not yet lifted into a neutral, cross-pillar contract file.
- `LoomPBlock_v1` / `LoomIBlock_v1` — clearly described in Loom spec, not yet in `docs/contracts/` as separate contracts.
- `APXStream_v1` / `APXManifest_v1` — described in Astral Press, not yet extracted.
- `SceneFrame_v1`        — described conceptually in Trinity/plan, not yet written as the “one true per-tick bundle” contract.
- `NAPEnvelope_v1`       — present in NAP/envelope docs, needs a small dedicated contract.

Those “missing files” are what I was pointing at when I suggested we firm up a
few contracts before coding.

---

## 6. How to treat this going forward

- Keep the **pillar contracts** as the detailed, source-of-truth docs for each pillar.  
- Use the new small `*_v1.md` **generic contracts** as:
  - A stable API contract for code,
  - A place tests can import shapes from,
  - A thin index tying pillar concepts together.

Nothing you’ve done is being replaced — we’re just adding a clean,
cross-pillar “contracts shelf” so the repo is easy to work in.
