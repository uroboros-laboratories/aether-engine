# Aether — “When Can I Start Coding?” Gate (v1)

This is a blunt line in the sand for **when it’s safe to start Phase 1 code**
(SPEC-002 / GF-01 CMP-0 baseline).

Use this as a checklist. Once the boxes under **Gate A** are ticked, you’re
allowed to open the repo and start Sprint 1.

---

## Gate A — Minimum Safe Before Sprint 1 (UMX + GF-01)

You **must** have these done on paper before you touch engine code:

### A1. Physics core

- [x] CMP-0 physics core doc exists and is coherent  
  (`Aether_CMP0_Physics_Core_and_Invariants_v1.md`)
- [x] Flux rule, conservation rule, chain rule, `s_t`, and CMP-0 constants are
      all defined there in one place.

### A2. GF-01 exam

- [x] GF-01 exam doc exists and is coherent  
  (`GF01_V0_Exam_v1.md`)
- [x] It clearly defines the pass/fail conditions for:
  - UMX parity,
  - Loom parity,
  - Press/APX parity,
  - NAP parity,
  - Determinism.

### A3. Core contracts for Sprint 1

These don’t have to be huge, but they should exist as **actual files** in
`docs/contracts/` (or ready to paste there):

- [ ] `TopologyProfile_v1.md`
- [ ] `Profile_CMP0_v1.md`
- [ ] `UMXTickLedger_v1.md` (including `EdgeFlux_v1` inside it or alongside it)

Each of these should specify:

- Field names and types,
- Any invariants the tests will assert,
- How they relate to GF-01 (e.g. “GF-01 uses N=6, edges 1..8, etc.”).

### A4. Quick consistency pass

- [ ] You’ve eyeballed:
  - CMP-0 physics core doc,
  - GF-01 exam,
  - SPEC-002,
  - UMX/Loom/Press pillar specs,
  
  and there are **no obvious contradictions** in:
  - Constant values (`C0`, `M`, `SC`, `W`, etc.),
  - Field names that appear in multiple docs.

> **Rule:** As soon as A1–A4 are true, you can start Sprint 1 and implement:
> - GF-01 topology/profile,
> - UMX CMP-0 engine,
> - GF-01 UMX unit tests.

You do **not** need Part B/C/D fully resolved to begin.

---

## Gate B — Nice-to-Have Before Phase 2 Coding

These are not required before Sprint 1, but are good to have before you dive
into SPEC-005 / Phase 2 work:

- [ ] Short section somewhere that:
  - Names 2–3 canonical toy topologies (LINE_4, RING_5, STAR_6, …).
  - States how multiple topology profiles are referenced in configs.
- [ ] A page describing `PressWindowContext`:
  - Windows, named streams, append, close.
- [ ] A clear statement (in Trinity or SPEC-005) that:
  - `SceneFrame_v1` is the **canonical per-tick integration bundle**,
  - Gate/NAP/ledger/governance derive from scene frames, not from ad hoc wiring.

You can start coding UMX/Loom **before** these are perfect; they matter more
when you’re generalising in Phase 2.

---

## Gate C — Definitely Overkill Pre-Code

You do **not** need these finished before starting any code:

- Full SLP heuristic catalogue,
- Full AEON/APXi grammar designs,
- Full PFNA channel taxonomy,
- Detailed governance formulas and budgets.

Those live in **Part C** of the readiness docs and are explicitly allowed to
be discovered in code, then backfilled into specs later.

---

## TL;DR

- As soon as:
  - CMP-0 physics core doc ✅
  - GF-01 exam doc ✅
  - 3 core contracts exist (`TopologyProfile_v1`, `Profile_CMP0_v1`, `UMXTickLedger_v1`) ✅
  - Quick consistency pass done ✅

  → you’re good to start **Sprint 1 (UMX + GF-01)**.

- Everything else can follow while you code, as long as any new stable behaviour
  eventually gets written back into the specs.
