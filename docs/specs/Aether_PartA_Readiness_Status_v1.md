# Aether Engine — Part A Readiness Status (v1)

This doc is a rough status pass over **Part A** of the
_Aether Paper vs Code Readiness Checklist_ — i.e. what should be locked on paper
before Sprint 1 (SPEC-002 / GF-01 CMP-0 baseline).

Status legend (you can update this by hand):
- ✅ = High confidence this is effectively done in the current docs.
- ⚠️ = Probably mostly there, but worth a focused pass before coding.
- ❌ = Needs real work / not obviously present yet.

You should treat this as a **starting guess**; you’ll know the true state better
once you eyeball the actual specs again.

---

## A1. Core physics & invariants

- ⚠️ CMP-0 flux rule fully specified (formula + constraints).
- ⚠️ Conservation rule stated clearly and explicitly as an invariant.
- ⚠️ Chain rule for CMP-0 fully specified (including `a`, `b`, `M`, `seq_t`).
- ⚠️ s_t definition for GF-01 (constant 9 and rationale) written in one clear place.
- ✅ CMP-0 profile constants (`C0`, `modulus_M`, `SC`, `I_block_spacing_W`) are defined in at least one doc.

**Suggested action:** Do a one-pass “physics core” consolidation in the UMX/Loom
master specs + SPEC-002 so the exact formulas and constants live in a small,
obvious section you can point code at.

---

## A2. Type contracts (v1) for Phase 1

- ⚠️ `TopologyProfile_v1` — present in concept, but worth a clean, dedicated contract doc.
- ⚠️ `Profile_CMP-0_v1` — same deal; ensure all constants & rules are captured.
- ⚠️ `UMXTickLedger_v1` and `EdgeFlux_v1` — shapes are implied; a focused contract doc will help tests.
- ⚠️ `LoomPBlock_v1` and `LoomIBlock_v1` — likely mostly defined in Loom spec; still worth extracting into a contract.
- ⚠️ `APXStream_v1` and `APXManifest_v1` — need to be crystal clear for MDL + `manifest_check` tests.
- ⚠️ `SceneFrame_v1` — conceptually present, but should be written as the canonical per-tick bundle.
- ⚠️ `NAPEnvelope_v1` (DATA/P flavour) — envelope sheet + Trinity spec probably cover it; a contract makes tests easier.

**Suggested action:** For Sprint 1, you mainly need **TopologyProfile**, **Profile_CMP0**,
and **UMXTickLedger/EdgeFlux** nailed. The others are needed before you start Sprint 2/3.

---

## A3. GF-01 reference artefacts

- ✅ GF-01 tick tables 1–8 (pre/post_u, du, raw, f_e, z_check) — present in the GF01 PDFs.
- ✅ GF-01 chain values C1..C8 — present in the worked examples / spec text used in SPEC-002.
- ✅ GF-01 APX sheets (bits, L_model, L_residual, L_total, manifest_check) — present in APX PDFs.
- ✅ GF-01 envelope sheet (prev_chain, payload_ref, layer, mode, seq) — present in envelope PDF.
- ⚠️ Single “GF-01 exam” doc that textually states the pass/fail conditions for SPEC-002.

**Suggested action:** Draft a short `GF01_V0_Exam.md` that just restates the exam
conditions you’ve already used in SPEC-002. It doesn’t have to be long; just
something tests and humans can both reference.

---

## A4. SPEC-002 doc & issues

- ✅ SPEC-002 baseline build plan exists as a dedicated markdown spec.
- ✅ SPEC-002 GitHub issue pack has Issues 1–7 with detailed bodies.
- ⚠️ Light consistency pass between SPEC-002 and the master pillar specs (names, constants, field names).

**Suggested action:** Before Sprint 1, do a single “follow the numbers” pass:
start from SPEC-002, jump into the pillar specs wherever it references them,
and confirm nothing disagrees on constants or field names.

---

## TL;DR Before Sprint 1

If you want a strict gate for yourself before starting Sprint 1 coding, I’d use:

- [ ] **Physics core consolidation:** One short section that pins down CMP-0 flux,
      conservation, chain, and s_t in a single, updated place.
- [ ] **Three key contracts in good shape:** `TopologyProfile_v1`,
      `Profile_CMP0_v1`, `UMXTickLedger_v1` (with `EdgeFlux_v1`).
- [ ] **GF01_V0_Exam.md:** A tiny exam doc, even 1–2 pages, capturing “what tests must assert.”
- [ ] **SPEC-002 ↔ pillar-spec sanity pass:** Confirm constants and names are aligned.

Once those are checked off, Sprint 1 can honestly be “just implementation” rather
than trying to design and code at the same time.
