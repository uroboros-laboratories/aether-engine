# SPEC-004 — Aether v1 Dev Workflow & Codex Guide

## Status

- **Spec ID:** SPEC-004
- **Name:** Aether v1 Dev Workflow & Codex Guide
- **Version:** v1
- **Scope:** Development workflow, repo usage, GPT-5.1 Codex usage, testing & CI guardrails
- **Assumes:** 
  - SPEC-002 (GF-01 CMP-0 Baseline Build Plan) is accepted as the baseline.
  - SPEC-003 (Aether v1 Full Pillar Implementation Roadmap) is accepted as the long-range roadmap.

---

## 1. Purpose

This spec defines **how** development should be done on the Aether engine repo, including:

- How to use the **specs** and **contracts** when coding,
- How to work with **GPT-5.1 Codex** against the repo,
- Coding constraints and guardrails (integer-only core, determinism, etc.),
- Testing and CI expectations (GF-01 as a hard baseline).

It is intentionally **language-agnostic**. Whatever implementation language(s) you choose, these rules apply.

---

## 2. Repo Structure & Sources of Truth

### 2.1 Structure (high-level)

When the repo exists, it should roughly follow:

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
        ...PDFs and JSON fixtures...
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

### 2.2 Priority of Truth

The **priority order** when making decisions or resolving conflicts:

1. **Contracts in `docs/contracts/`**  
   - These define record shapes and invariants (e.g. `UMXTickLedger_v1`, `NAPEnvelope_v1`).

2. **Build specs in `docs/specs/`**  
   - SPEC-002 (GF-01 build plan) and SPEC-003 (roadmap) define *what* to build and in what order.

3. **Pillar master specs**  
   - Trinity Gate, Astral Press, Aevum Loom, UMX, Codex Eterna pillar docs.

4. **Code comments and implementation notes**  
   - Must not contradict 1–3; if they do, the specs win and the code is wrong.

---

## 3. Coding Guardrails (Global)

These rules apply to all core Aether code:

### 3.1 Integer-Only Core

- UMX, Loom, Press/APX, and NAP **must not** use floating-point arithmetic in the core algorithms.
- All state and flux values are integers.
- Any division is **explicitly floor division** where defined (see `Profile_CMP0_v1`).
- If a helper library forces float usage, results must be converted back to integers and tests must ensure there is no drift.

### 3.2 Determinism

- Given the same inputs, topology, profile, and config:
  - UMX outputs must be identical.
  - Loom chain and blocks must be identical.
  - Press/APX manifests and `manifest_check` must be identical.
  - NAP envelopes must be identical.
  - U-ledger entries and Codex artefacts must be identical.

- No randomness, system time, or non-deterministic iteration order is allowed in the core path.

### 3.3 Contracts-First Development

- Before writing code for a data structure or API:
  - Find or create the corresponding contract in `docs/contracts/`.
  - Ensure struct/class/record fields match the contract exactly (names, types, meanings).

- If code needs a new field or behaviour:
  - Update the contract document first,
  - Then update code and tests to match.

### 3.4 No Silent Auto-Magic

- No hidden global state changes.
- No background threads or async behaviour in the core pipeline unless explicitly specified in a future spec.
- The per-tick flow should be visible and traceable via the tick loop (`TickLoop_v1`).

---

## 4. Working with GPT-5.1 Codex

The repo is designed to be worked on heavily via **GPT-5.1 Codex** in GitHub. This section defines how to collaborate with Codex effectively.

### 4.1 The “Spec Sandwich” Prompt Pattern

When asking Codex to implement something, use this shape:

1. **Context:**  
   - Mention the relevant spec and contract filenames.  
   - Example:  
     > “We are implementing `UMX.step` as per `UMXTickLedger_v1.md` and SPEC-002, Issue 2.”

2. **Constraints:**  
   - Remind Codex of critical guardrails:  
     - Integer-only, no floats, determinism, no randomness.

3. **Task:**  
   - Describe the concrete change or feature to implement.

Example prompt to Codex:

> Implement the `UMX.step` function for GF-01.  
> Use `docs/contracts/UMXTickLedger_v1.md` as the source of truth for the ledger structure and SPEC-002 (Issue 2) for behaviour.  
> Integer-only math, deterministic, no randomness, no floating-point types.

### 4.2 Don’t Let Codex Invent Specs

- Codex must **not** create new data structures or behaviours that contradict the contracts.
- If Codex proposes a new field or behaviour:
  - Treat it as a suggestion, not fact.
  - Decide in this planning space (ChatGPT) whether to adopt it.
  - Only then update contracts and repo.

### 4.3 Always Anchor Tests to Fixtures

When writing tests with Codex:

- Reference GF-01 fixtures and exam conditions:
  - E.g. “Expected `C_1..C_8` values are listed in `LoomBlocks_v1.md` and `GF01_V0_Exam.md`.”
- Codex should never “guess” expected values that are already in the specs/fixtures; it should copy them.

### 4.4 Pull Requests & Diff Review

- For each PR (even if authored by Codex):
  - Confirm that:
    - It references the relevant spec/issue IDs.
    - It does not introduce floating-point arithmetic in core paths.
    - It updates or adds tests alongside code changes.

- Any PR that changes core behaviour must update:
  - Specs (if the behaviour change is intentional),
  - Regression snapshots (after confirming new behaviour is desired).

---

## 5. Testing Strategy

### 5.1 Required Test Layers

1. **Unit Tests (per pillar)**  
   - UMX tick stepping and conservation.  
   - Loom chain update and I-blocks.  
   - Press/APX manifest generation, bit counts, `manifest_check`.  
   - NAP envelope creation and field correctness.  
   - U-ledger record formation, hash chaining.

2. **Integration Tests**  
   - `run_gf01()` integration test (SPEC-002) is mandatory.  
   - Future scenarios (non-GF-01 graphs, profiles) as they’re added.

3. **Determinism Tests**  
   - Double-run GF-01 and compare all outputs bit-by-bit.

4. **Regression Snapshot Tests**  
   - Store canonical output snapshots for key scenarios.  
   - Fail tests on any diff unless the spec has been consciously updated.

### 5.2 When Tests Must Be Updated

- Any change to:
  - Contract shapes,
  - Profile constants,
  - Core algorithms,
  - Window sizes or stream definitions
- Must also update:
  - Unit tests,
  - Integration tests,
  - GF-01 regression snapshots (if behaviour is meant to change).

No “quick hacks” that temporarily break GF-01 are allowed; GF-01 should remain green at all times.

---

## 6. Branching & CI Expectations

### 6.1 Branching

- Use feature branches per issue or per small group of issues:
  - Example: `feature/umx-cmp0-step`, `feature/loom-chain-cmp0`.

- Each branch should:
  - Target one or a small number of SPEC-002/SPEC-003 issues.
  - Contain both code and tests.

### 6.2 CI Requirements

CI should at minimum:

- Run:
  - GF-01 unit tests,
  - GF-01 integration test (`run_gf01()`),
  - Determinism tests,
  - Regression snapshot tests.

- Fail the build on:
  - Any failing tests,
  - Any non-deterministic or flaky behaviour.

---

## 7. When to Add New Specs vs New Contracts

### 7.1 New Behaviour (Conceptual)

If you are introducing **new conceptual behaviour** (e.g. a new Loom profile, dynamic topology):

- Add or update a **SPEC** under `docs/specs/` (e.g. SPEC-005).
- Update or create relevant contracts in `docs/contracts/`.
- Then implement code and tests.

### 7.2 New Data Shape Only

If you are only introducing a **new record shape** (e.g. a new type of NAP payload):

- Add or update a **contract** under `docs/contracts/`.
- Reference it in the existing build specs where relevant.
- Then implement code and tests.

---

## 8. First-Time Setup Checklist (When Repo is Created)

When you first create the GitHub repo:

1. **Copy in docs:**
   - `spec_001_aether_full_system_build_plan_medium_agnostic.md`
   - `spec_002_GF01_CMP0_Baseline_Build_Plan.md`
   - `spec_003_Aether_v1_Full_Pillar_Roadmap.md`
   - `spec_004_Aether_v1_Dev_Workflow_and_Codex_Guide.md`
   - All contracts under `docs/contracts/`.

2. **Set up tests directory:**
   - `tests/gf01/` with placeholders for:
     - UMX tests,
     - Loom tests,
     - Press tests,
     - NAP tests,
     - Integration tests.

3. **Set up CI pipeline:**
   - Ensure tests are run on each PR and on main.

4. **Create initial GitHub issues:**
   - One per Issue in SPEC-002 (Issues 1–7).
   - One epic/project for SPEC-002.
   - Later, epics for SPEC-003 phases.

5. **Start coding via Codex:**
   - Begin with SPEC-002 Issue 1 (topology & profile).
   - Use the “spec sandwich” prompt pattern consistently.

---

## 9. Out of Scope for SPEC-004

The following are **not** defined here and will be addressed in other specs:

- Exact choice of programming language(s) and frameworks.
- Detailed CLI design and UX.
- Advanced profiling, performance tuning, or hardware-specific optimisations.

SPEC-004 is focused purely on **how** to develop Aether v1 safely, using Codex and the existing specs as anchors.
