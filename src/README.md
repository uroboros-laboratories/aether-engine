# Source Layout (`src/`)

This tree is where the **code implementation** of the Aether engine lives.

It is intentionally empty at the start. The idea is:

- Specs and contracts under `docs/` define what the system must do.
- Code under `src/` implements those behaviours.
- Tests under `tests/` prove that the implementation matches the docs.

```text
src/
  README.md          ← this file
  core/
  umx/
  loom/
  press/
  gate/
  codex/
  uledger/
```

---

## Modules

### `src/core/`

Shared runtime pieces:

- Run contexts,
- Global config,
- Tick loop orchestration (as per `TickLoop_v1.md`),
- Common types / errors that don’t belong to a single pillar.

### `src/umx/`

Universal Matrix integer engine:

- CMP‑0 flux implementation as per:
  - `docs/specs/Aether_CMP0_Physics_Core_and_Invariants_v1.md`
  - `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `UMXRunContext` (Phase 2) as per:
  - `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- All data structures must reflect `docs/contracts/UMXTickLedger_v1.md` and
  `TopologyProfile_v1.md` / `Profile_CMP0_v1.md`.

### `src/loom/`

Aevum Loom time axis:

- Chain calculation and P‑/I‑block creation:
  - `docs/contracts/LoomBlocks_v1.md`
  - `docs/contracts/Profile_CMP0_v1.md`
- `LoomRunContext` and replay APIs (`get_chain_at`, `replay_state_at`) as per SPEC‑005.

### `src/press/`

Astral Press / APX compression:

- Window / stream handling (`PressWindowContext_v1`).
- Schemes (ID, R, basic GR).
- Manifest generation as per `APXManifest_v1.md`.
- Must reproduce the GF‑01 APX manifests exactly in Phase 1.

### `src/gate/`

Trinity Gate / TBP:

- `SceneFrame_v1` construction.
- NAP envelope creation (`NAPEnvelope_v1.md`).
- PFNA placeholder routing as per `spec_003_Gate_PFNA_V0_External_Inputs_and_Layering.md`.

### `src/codex/`

Codex Eterna (observer only in Phase 2):

- `CodexContext` to ingest traces.
- Motif identification and proposal emission as per:
  - `docs/contracts/CodexContracts_v1.md`
  - SPEC‑005 Codex issues.

### `src/uledger/`

Universal ledger subsystem:

- Canonical serialisation and hashing rules.
- `ULedgerEntry_v1` construction per tick/window.

---

## How to work here

1. Pick a phase + spec:
   - Phase 1: `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
   - Phase 2: `spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
2. Use the matching issue pack (`SPEC_002_…Issue_Pack_v1.md`, `SPEC_005_…Issue_Pack_v1.md`) to
   decide which module to work in.
3. Implement only what the spec requires in the relevant subfolder.
4. Add / extend tests in `tests/` to prove parity with the fixtures and docs.

Code must not silently diverge from docs. If you need to change behaviour, update the specs and
contracts first, then adjust the implementation.
