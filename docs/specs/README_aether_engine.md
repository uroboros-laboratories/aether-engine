# Aether Engine

> Reference implementation of the Aether v1 engine: Gate/TBP, UMX, Aevum Loom, Astral Press/APX, Codex Eterna, and the Universal Ledger — built to match the paper specs exactly.

This repo is designed to be driven heavily by **GPT-5.1 Codex** plus a small human core. All the heavy thinking lives in `docs/`, and the code is just the faithful implementation.

---

## 1. What This Is

Aether v1 is a **deterministic integer engine** with five pillars:

- **Gate / TBP** — ingress/egress, scenes, PFNA, time-basis.
- **UMX (Universal Matrix)** — integer substrate / graph engine.
- **Aevum Loom** — time chain, P-blocks, I-blocks, replay.
- **Astral Press / APX** — compression, streams, manifests, MDL.
- **Codex Eterna** — learning, motifs, proposals, structural changes.

The initial goal of this repo is **paper parity** with the **GF-01 V0** example under profile **CMP-0**. That’s defined in **SPEC-002** and enforced with tests.

---

## 2. Specs & Contracts

### 2.1 Specs (build-level)

Placed under `docs/specs/`:

- `spec_001_aether_full_system_build_plan_medium_agnostic.md`  
  Full-system build plan and narrative.

- `spec_002_GF01_CMP0_Baseline_Build_Plan.md`  
  **Phase 1** — GF-01 CMP-0 baseline engine (paper parity).  
  Defines the first working implementation and exact exam conditions.

- `spec_003_Aether_v1_Full_Pillar_Roadmap.md`  
  **Phase 2+** — Pillar V1 generalisation, governance/ops, advanced features.

- `spec_004_Dev_Workflow_and_Codex_Guide.md`  
  How to develop in this repo, how to work with GPT-5.1 Codex, guardrails (no floats, determinism, etc.).

### 2.2 Contracts (data-level)

Placed under `docs/contracts/`:

- Core engine records:
  - `UMXTickLedger_v1.md`
  - `LoomBlocks_v1.md`
  - `APXManifest_v1.md`
  - `NAPEnvelope_v1.md`
- Config & loop:
  - `TopologyProfile_v1.md`
  - `Profile_CMP0_v1.md`
  - `TickLoop_v1.md`
  - `SceneFrame_v1.md`
- Ledger & learning:
  - `ULedgerEntry_v1.md`
  - `CodexContracts_v1.md`
- Exam:
  - `GF01_V0_Exam.md` — the acceptance test for the whole core loop.

**Rule of thumb:**  
If you’re unsure about a field or type, the **contracts** are the source of truth. Specs describe behaviour; contracts fix the shapes.

---

## 3. Repo Layout (target)

The repo is expected to roughly follow:

```text
aether-engine/
  docs/
    specs/
      spec_001_aether_full_system_build_plan_medium_agnostic.md
      spec_002_GF01_CMP0_Baseline_Build_Plan.md
      spec_003_Aether_v1_Full_Pillar_Roadmap.md
      spec_004_Dev_Workflow_and_Codex_Guide.md
      ...pillar master specs...
    contracts/
      GF01_V0_Exam.md
      UMXTickLedger_v1.md
      LoomBlocks_v1.md
      APXManifest_v1.md
      NAPEnvelope_v1.md
      TopologyProfile_v1.md
      Profile_CMP0_v1.md
      TickLoop_v1.md
      SceneFrame_v1.md
      ULedgerEntry_v1.md
      CodexContracts_v1.md
    fixtures/
      gf01/
        GF01_Ticks_1_8_Worked_Examples.pdf
        GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf
        GF01_Ticks_1_8_APX_Press_Prefilled.pdf
        GF01_Ticks_1_2_Worked_Examples.pdf
        GF01_Ticks_1_2_APX_Press_Prefilled.pdf
        ...csv/json mirrors...
  src/
    core/
    gate/
    umx/
    loom/
    press/
    codex/
    uledger/
  tests/
    gf01/
    integration/
```

This is a **target** layout; some folders will be empty until you implement the relevant issues.

---

## 4. Core Guardrails

These are hard constraints for the core engine:

1. **Integer-only core**  
   - UMX, Loom, Press/APX, NAP must not depend on floating-point math.
   - All state and flux values are integers.
   - Any division is explicit floor division as defined in `Profile_CMP0_v1.md`.

2. **Determinism**  
   - Same inputs → same outputs, bit-for-bit.
   - No randomness in the core path. No “current system time” hidden in logic.
   - Iteration order must be deterministic (e.g. edges sorted by `e_id`).

3. **Contracts-first**  
   - Data shapes (fields, types) are defined in `docs/contracts/`.
   - Code structs/classes/records must follow those shapes exactly.
   - If behaviour or shape changes, update the contract first, then code, then tests.

4. **No silent magic**  
   - No background threads, no hidden async in core tick loop.
   - Tick processing follows `TickLoop_v1.md` and is traceable per tick.

See `spec_004_Dev_Workflow_and_Codex_Guide.md` for the full dev policy.

---

## 5. Development Workflow

### 5.1 Implementation Order (high-level)

Phase 1 (from `spec_002`):

1. **CMP-0 topology & profile (GF-01)**  
2. **UMX CMP-0 engine + `UMXTickLedger_v1`**  
3. **Loom CMP-0 chain + blocks**  
4. **Press/APX CMP-0 (R-mode, `APXManifest_v1`)**  
5. **NAP + minimal Gate/TBP using `NAPEnvelope_v1` + `SceneFrame_v1`**  
6. **Tick loop wiring (`run_gf01()` end-to-end)**  
7. **Determinism harness + regression snapshot**

Phase 2+ (from `spec_003`):

- Generalised UMX, Loom, Press, Gate, U-ledger, Codex V1, then governance & advanced features.

### 5.2 Using GPT-5.1 Codex

When you ask Codex to implement something, use a **spec sandwich**:

1. **Context:**  
   > “We’re implementing UMX CMP-0 step for GF-01 as per `UMXTickLedger_v1.md` and `spec_002_GF01_CMP0_Baseline_Build_Plan.md` (Issue 2).”

2. **Constraints:**  
   > “Integer-only, deterministic, no randomness, no floats, contracts in `docs/contracts/` are the source of truth.”

3. **Task:**  
   > “Write the `UMX.step` function that takes `(t, state, topo, profile)` and returns a `UMXTickLedger_v1` that matches the GF-01 tick tables.”

Always anchor expected values (e.g. `C_1..C_8`, `manifest_check`) to the specs or fixtures, not guesses.

---

## 6. Testing

### 6.1 Minimal Required Suites

- **Unit tests** (`tests/gf01/`):
  - UMX: flux maths, conservation, tick ledger fields.
  - Loom: chain updates, I-blocks.
  - Press: APX manifests, bit counts, `manifest_check`.
  - NAP: envelope fields (`payload_ref`, `prev_chain`, etc.).
  - U-ledger: hashes and chain.

- **Integration tests** (`tests/integration/`):
  - `run_gf01()` end-to-end as defined in SPEC-002.

- **Determinism tests**:
  - Run GF-01 twice, serialise all artefacts, compare byte-for-byte.

- **Regression snapshot tests**:
  - Store canonical JSON for GF-01 outputs.
  - Fail on any diff unless you explicitly update specs & snapshots.

### 6.2 CI Expectations

CI should:

- Run all tests on every PR to `main`.
- Block merges if:
  - Any GF-01 test fails,
  - Determinism/snapshot tests fail.

GF-01 green is non-negotiable: it’s the “golden fixture” for the whole engine.

---

## 7. Getting Started (Humans)

1. **Read:**
   - `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
   - `spec_004_Dev_Workflow_and_Codex_Guide.md`

2. **Pick an issue from SPEC-002** (Issues 1–7) and mirror it as a GitHub Issue.

3. **Create a feature branch**:
   - e.g. `feature/umx-cmp0-step`, `feature/loom-chain-cmp0`.

4. **Implement with Codex** using the spec sandwich pattern.

5. **Add tests** for what you just implemented.

6. **Run the full GF-01 suite** locally before opening a PR.

---

## 8. Getting Started (Codex)

When you first point GPT-5.1 Codex at the repo, give it this minimal context:

> This repo is the Aether v1 engine.  
> Specs live in `docs/specs/`. Contracts live in `docs/contracts/`.  
> The current milestone is SPEC-002: GF-01 CMP-0 baseline.  
> Start by opening `spec_002_GF01_CMP0_Baseline_Build_Plan.md` and implement Issue 1.

Then paste the relevant section of SPEC-002 into the Codex chat so it has full context.

---

## 9. Status

Right now this README and the specs are the **scaffolding**. Until code exists, treat the repo as:

- A spec library for the Aether v1 engine,
- A planning space for implementation work,
- The reference context for GPT-5.1 Codex.

Once the first pass of SPEC-002 is implemented and green, you’ll have a working Aether core loop with real artefacts you can inspect, replay, and extend.

---

## 10. License

TBD.

(Decide on a license before making the repo public. Until then, treat it as private research code.)
