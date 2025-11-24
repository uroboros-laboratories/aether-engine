# Tests (`tests/`)

This tree is where all verification lives:

- GF‑01 paper parity for CMP‑0 (Phase 1),
- Pillar V1 generalisation checks (Phase 2),
- Governance, proposals, advanced features (later phases),
- Regression / determinism harnesses.

```text
tests/
  README.md              ← this file
  gf01/
  integration/
  snapshots/
  unit/
```

---

## `tests/gf01/` — GF‑01 CMP‑0 Exam (Phase 1)

Tests here should implement the full **GF‑01 V0 exam** as per:

- `docs/specs/GF01_V0_Exam_v1.md`
- `docs/contracts/GF01_V0_Exam.md`
- PDFs under `docs/fixtures/gf01/`

For SPEC‑002 (Phase 1), GF‑01 is the only scenario that truly matters:

- `UMXTickLedger_v1` parity with paper tick tables (ticks 1–8).
- Loom chain parity (`C_1..C_8`).
- APX manifest parity (bit counts + `manifest_check`).
- NAP envelope parity (one per tick, matching envelopes sheet).

Integration helpers like `run_gf01()` should be exercised here.

---

## `tests/integration/` — Cross‑Pillar & End‑to‑End

Use this for tests that span multiple pillars:

- Full tick loop (UMX + Loom + Press + Gate/NAP + U‑ledger).
- Multi‑graph / dynamic topology scenarios (Phase 3+).
- Governance flows that involve Codex proposals and U‑ledger checks.

Keep GF‑01‑specific logic in `tests/gf01/`; this folder is for more general / synthetic scenarios.

---

## `tests/snapshots/` — Regression & Determinism

Snapshot tests exist to catch **behaviour drift**:

- For GF‑01:
  - Serialise UMX tick ledgers, Loom blocks, APX manifests, NAP envelopes, and U‑ledger entries.
  - Store them as canonical JSON snapshots.
  - Re‑run and compare byte‑for‑byte.
- For later scenarios:
  - Similar pattern, using the same serialisation rules.

See:

- `docs/contracts/ULedgerEntry_v1.md`
- SPEC‑002 Issue 7 (determinism harness)

for guidance.

---

## `tests/unit/` — Low‑Level Units

Use this for small, focused tests:

- CMP‑0 flux rule edge cases (UMX).
- Chain update function (Loom).
- Scheme handlers (ID/R/GR) for Press.
- Envelope construction and PFNA routing (Gate).
- Motif extraction heuristics (Codex).
- Serialisation / hashing helpers (U‑ledger).

Unit tests should be fast and not depend on big fixtures.

---

## General rules

- Tests must be deterministic and repeatable.
- Where possible, assert **exact equality** (no fuzzy tolerances).
- If behaviour changes legitimately, update both:
  - The relevant spec / contract, and
  - The snapshots / expectations here.
