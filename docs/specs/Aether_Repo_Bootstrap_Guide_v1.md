# Aether Engine Repo Bootstrap Guide (v1)

This document is a **practical bridge** between the Aether paper specs and a working GitHub repo that GPT 5.1 Codex can use to build the codebase.

It’s meant to live near the top of the repo, for example as:

- `docs/Aether_Repo_Bootstrap_Guide_v1.md`  
- or you can rename it to `docs/README_repo_bootstrap.md`

---

## 1. Goal & Scope

This guide explains how to:

1. Stand up the **initial GitHub repo** for the Aether engine.  
2. Lay out the **folders and key docs** so GPT tools can navigate cleanly.  
3. Create **milestones, labels, and projects** aligned to SPEC-000…007.  
4. Define some **working conventions** so the implementation stays faithful to the paper system.

It does **not** prescribe language/stack details; GPT 5.1 Codex and future you can choose language and test framework as long as the contracts and integer-only behaviour are respected.

---

## 2. Recommended Repo Skeleton

You don’t have to follow this exactly, but it’s tuned for:

- Clear separation between **specs**, **contracts**, **fixtures**, **src**, and **tests**.  
- Easy navigation for GPT tools (low ambiguity).

### 2.1 Top-Level Layout

Recommended initial structure:

```text
aether-engine/
  docs/
    specs/
    contracts/
    fixtures/
  src/
    core/
    umx/
    loom/
    press/
    gate/
    codex/
    uledger/
    slp/
    governance/
  tests/
    unit/
    integration/
    gf01/
    snapshots/
  .github/
    workflows/
```

You can create these directories up front before adding any code.

### 2.2 `docs/` Layout

**Specs** (design & planning):

- `docs/specs/SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`
- `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
- `docs/specs/spec_002_GF01_CMP0_Baseline_Build_Plan.md`
- `docs/specs/SPEC_003_Phase_3_Issue_Pack_v1.md`
- `docs/specs/SPEC_004_Phase_3_Issue_Pack_v1.md`
- `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md`
- `docs/specs/SPEC_006_Phase_4_Issue_Pack_v1.md`
- `docs/specs/SPEC_007_Phase_5_Issue_Pack_v1.md`

**Contracts** (type-level definitions for all pillars):

- `docs/contracts/UMXTickLedger_v1.md`
- `docs/contracts/LoomBlocks_v1.md`
- `docs/contracts/APXManifest_v1.md`
- `docs/contracts/NAPEnvelope_v1.md`
- `docs/contracts/TopologyProfile_v1.md`
- `docs/contracts/Profile_CMP0_v1.md` (and follow-ons)
- `docs/contracts/SceneFrame_v1.md`
- `docs/contracts/TickLoop_v1.md`
- `docs/contracts/ULedgerEntry_v1.md`
- `docs/contracts/CodexContracts_v1.md`
- `docs/contracts/AEONWindowGrammar_v1.md`
- `docs/contracts/APXiDescriptor_v1.md`
- `docs/contracts/SLPEvent_v1.md`
- `docs/contracts/PFNA_V0_Schema_v1.md`
- `docs/contracts/GovernanceConfig_v1.md` + policy types

(Names here are canonical targets; add/migrate the actual pillar master spec contracts into this folder.)

**Fixtures** (paper + reference runs):

```text
docs/fixtures/
  gf01/
    GF01_Ticks_1_8_Worked_Examples.pdf
    GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf
    GF01_Ticks_1_8_APX_Press_Prefilled.pdf
    GF01_Ticks_1_2_Worked_Examples.pdf
    GF01_Ticks_1_2_APX_Press_Prefilled.pdf
    # optional CSV/JSON mirrors later
  aether_v0/
    AETHER_V0_Lookup_Booklet.pdf
    AETHER_V0_Paper_Templates.pdf
    GF01_Ticks_1_8_APX_Press_Prefilled.pdf
    GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf
    # etc, as you organise
```

You can expand fixtures as more worked examples appear.

---

## 3. Bootstrapping the Repo (Step-by-Step)

### 3.1 Create the GitHub Repo

1. In GitHub, create a new repository (e.g. `aether-engine`):  
   - Visibility: your choice (private recommended at first).  
   - Initialise with a plain README if you like; no code yet.

2. Clone it locally.

3. Inside the repo root, create the directories from section **2.1**.

### 3.2 Add Specs & Contracts

1. Copy all **spec markdown files** (SPEC-000…007 and pillar master specs) into `docs/specs/`.  
2. Copy **contract markdown files** into `docs/contracts/`.  
   - If some contracts currently live inside pillar specs, you can either:
     - Keep them duplicated (pillar spec + contracts file), or  
     - Move the canonical definition to contracts and leave references in pillar specs.

3. Commit this as your first content commit, e.g.:

> `chore: add Aether specs and contracts (no code yet)`

### 3.3 Add Fixtures

1. Copy the GF-01 PDFs into `docs/fixtures/gf01/`.  
2. Copy the AETHER V0 booklets and templates into `docs/fixtures/aether_v0/` (or similar).  
3. Commit with a message like:

> `chore: add GF-01 and AETHER V0 fixtures`

At this point, the repo is **docs-only** but fully navigable for humans and GPT tools.

---

## 4. Milestones & Labels in GitHub

Set these up once so the issue packs slot straight in.

### 4.1 Milestones

Create milestones matching the phases:

- `Phase 0 — Foundations`
- `Phase 1 — SPEC-002 GF-01 CMP-0 Baseline`
- `Phase 2 — SPEC-005 Pillar V1 Generalisation`
- `Phase 3 — SPEC-003 Gate/TBP & PFNA V0 IO`
- `Phase 3 — SPEC-004 Press AEON/APXi`
- `Phase 4 — SPEC-006 Multi-graph & SLP V1`
- `Phase 5 — SPEC-007 Governance & Codex Actioning V1`

You can also have an ongoing `Backlog / Ideas` milestone if you like.

### 4.2 Labels

Create these label families:

- **Spec:**  
  - `spec:SPEC-000` (optional)  
  - `spec:SPEC-001`  
  - `spec:SPEC-002`  
  - `spec:SPEC-003`  
  - `spec:SPEC-004`  
  - `spec:SPEC-005`  
  - `spec:SPEC-006`  
  - `spec:SPEC-007`

- **Phase:**  
  - `phase:P0`  
  - `phase:P1`  
  - `phase:P2`  
  - `phase:P3`  
  - `phase:P4`  
  - `phase:P5`

- **Components:**  
  - `component:umx`  
  - `component:loom`  
  - `component:press`  
  - `component:gate`  
  - `component:nap`  
  - `component:aeon`  
  - `component:apxi`  
  - `component:slp`  
  - `component:codex`  
  - `component:u-ledger`  
  - `component:governance`

- **Type & Priority:**  
  - `type:feature`  
  - `type:tests`  
  - `type:docs`  
  - `priority:high`  
  - `priority:medium`  
  - `priority:low`

Once these exist, the SPEC issue packs can reference them directly.

---

## 5. Importing the Issue Packs

Use the SPEC-002, 003, 004, 006, and 007 issue-pack markdown files as **source text** for GitHub issues.

### 5.1 General Pattern

For each issue in a SPEC pack:

1. Copy the **Title** (the backticked line).  
2. Create a new GitHub issue.  
3. Paste the **Body** block (inside the ```markdown code fences) into the issue description.  
4. Apply the suggested labels.  
5. Assign the correct milestone based on the SPEC/phase.

### 5.2 Recommended Order

To keep things clean:

1. **Phase 1:**  
   - Create issues from `spec_002_GF01_CMP0_Baseline_Build_Plan.md` issue pack.  
   - Milestone: `Phase 1 — SPEC-002 GF-01 CMP-0 Baseline`.

2. **Phase 2:**  
   - Create issues from SPEC-005 issue pack.  
   - Milestone: `Phase 2 — SPEC-005 Pillar V1 Generalisation`.

3. **Phase 3:**  
   - SPEC-003 (Gate/TBP & PFNA).  
   - SPEC-004 (AEON/APXi).

4. **Phase 4:**  
   - SPEC-006 (multi-graph & SLP).

5. **Phase 5:**  
   - SPEC-007 (governance & Codex actioning).

You don’t have to populate every phase on day one—Phase 1 + 2 might be enough to start.

---

## 6. GitHub Projects Setup (Optional but Recommended)

Use **GitHub Projects (beta)** to track work per phase.

### 6.1 One Project per Phase

Example project names:

- `P1 — GF-01 Baseline`
- `P2 — Pillar V1`
- `P3 — Gate/PFNA + AEON/APXi`
- `P4 — Multi-graph & SLP`
- `P5 — Governance & Codex`

Each project can have columns like:

- `Inbox`
- `Ready`
- `In Progress`
- `Blocked`
- `In Review`
- `Done`

You can also add filters/views:

- By spec: `spec:SPEC-002`  
- By component: `component:umx`  
- By type: `type:tests`

This makes it trivial for GPT tools (and you) to see what’s currently active.

---

## 7. Conventions for GPT 5.1 Codex in This Repo

These are **behavioural rules** to nudge GPT tools towards the system you actually want.

### 7.1 Always Anchor to Specs

When asking GPT 5.1 Codex to implement something, include in the prompt:

- A direct reference to the SPEC and issue ID, e.g.:  
  > “Implement the UMX CMP-0 engine as described in SPEC-002, Issue 2.”  
- The relevant contract filename, e.g.:  
  > “Types must match `docs/contracts/UMXTickLedger_v1.md` exactly.”

This prevents “free-styling” on types or behaviour.

### 7.2 Integer-Only Core

Core pillars (UMX, Loom, Press, NAP, AEON/APXi, SLP, governance) must:

- Avoid floating point in behaviour that affects semantics.  
- Use integer arithmetic, modular arithmetic, or fixed representations where needed.  
- Keep all randomness out of the core engine (no RNG in core tick logic).

If a language/runtime makes this tricky, require GPT to wrap operations in tests that assert determinism (especially across runs and platforms).

### 7.3 Determinism & Snapshots

For any **integration-level feature** (GF-01 baseline, PFNA demo, AEON/APXi demo, multi-graph demo, governance demo):

- Implement snapshot tests:  
  - Serialise canonical output to JSON.  
  - Store in `tests/snapshots/<scenario>/`.  
  - Verify new runs against these snapshots.

- Never silently change snapshots; always tie snapshot updates to a SPEC/issue and a commit message like:  
  > `chore: update GF-01 snapshot after SPEC-005 chain rule fix`

### 7.4 Tests First for Core Changes

When GPT proposes a change to core behaviour, require:

1. A failing test based on SPEC text or a fixture.  
2. A fix that makes the test pass.  
3. A note in the PR/commit referencing the SPEC and issue.

This keeps the repo anchored to the paper design rather than drifting towards convenience.

---

## 8. Recommended Implementation Order

When you’re ready for actual code, a safe route is:

1. **Stand up basic project structure & CI** (language + test framework).  
2. **Phase 1 (SPEC-002):**  
   - Implement UMX CMP-0 engine and tick ledger.  
   - Implement Loom CMP-0 chain and blocks.  
   - Implement minimal Press/APX for GF-01.  
   - Implement NAP envelopes for GF-01, Gate minimal integration.  
   - Add determinism harness and GF-01 snapshots.

3. **Phase 2 (SPEC-005):**  
   - Generalise UMX, Loom, Press, Gate to V1.  
   - Implement U-ledger.  
   - Wire Codex observer mode (no actioning).

4. **Phase 3 (SPEC-003 + SPEC-004):**  
   - Gate/TBP sessions, PFNA V0 IO.  
   - NAP layers + modes.  
   - AEON window grammar and APXi descriptors.  
   - AEON/APXi and PFNA demo scenarios with snapshots.

5. **Phase 4 (SPEC-006):**  
   - MultiGraphRunContext and SLPEvent application.  
   - Multi-graph + SLP snapshots.  
   - Codex motifs over multi-graph/SLP patterns.

6. **Phase 5 (SPEC-007):**  
   - Governance config + policies.  
   - Proposal evaluation and TBP decision loop.  
   - Budgets, governance-aware NAP IO.  
   - Governance + Codex demo, dry-run mode.

At each step, you can use GPT 5.1 Codex to implement one issue at a time, with SPEC-000 and the relevant SPEC file open as context.

---

## 9. Versioning & Maintenance of This Guide

- **File:** `Aether_Repo_Bootstrap_Guide_v1.md`  
- **Version:** v1  

When repo practices change (e.g. language switch, CI setup, directory layout), bump this file:

- Update sections 2–8 as needed.  
- Increment the version and briefly describe changes at the bottom.  

Keeping this guide aligned with reality is what will let future GPT tooling load it and immediately understand how to behave inside the repo.

---

End of Aether Repo Bootstrap Guide (v1).
