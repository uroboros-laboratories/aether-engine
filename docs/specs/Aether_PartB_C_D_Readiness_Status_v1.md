# Aether Engine — Part B/C/D Readiness Status (v1)

Companion doc to:

- `Aether_Paper_vs_Code_Readiness_Checklist_v1.md`
- `Aether_PartA_Readiness_Status_v1.md`

This one gives a **status + action sketch** for:

- **Part B** — Should be sketched on paper before Phase 2 coding.  
- **Part C** — Safe to discover in code, but must be backfilled into specs.  
- **Part D** — Rule-of-thumb for deciding paper-first vs code-first.

Status legend (same as Part A):

- ✅ = High confidence this is effectively done in your current doc set.
- ⚠️ = Probably mostly there, but worth a focused pass / top-up.
- ❌ = Needs real work / not obviously present yet.

These are *estimates* based on how you’ve described the specs; treat them as a
starting point for your own pass.

---

## Part B — Should be sketched on paper before Phase 2

These don’t need to be “forever-final”, but they should be non-vibes before
you implement SPEC-005 (Phase 2).

### B1. Topology & profile generalisation

- ⚠️ `TopologyProfile_v1` clearly supports **multiple named topologies**
  - You’ve talked about GF-01 + other toy graphs, but the generalisation rules
    (naming, IDs, how to store multiple profiles) are likely spread across specs.
- ⚠️ `Profile_CMP0_v1` vs “other profiles” positioning
  - CMP-0 is well-defined; how other profiles *might* appear is probably only
    implied in the full-system build plan.
- ⚠️ Canonical toy topologies (line, ring, star, mesh) written down explicitly
  - You’ve implicitly used these ideas in planning, but a short section naming
    & defining 2–3 canonical examples will help tests and docs.

**Suggested actions before Phase 2 sprints:**

- [ ] One short section (in SPEC-005 or a contracts doc) that:
  - [ ] Declares at least 2–3 named example topologies (LINE_4, RING_5, STAR_6, etc.).
  - [ ] States how additional profiles/topologies are referenced (IDs, filenames).
  - [ ] Confirms node/edge ID conventions for **all** topologies, not just GF-01.

---

### B2. Press/APX modes & registry

- ⚠️ Concept of `PressWindowContext` written down
  - The idea is in SPEC-005, but it’s worth making a crisp “this is the API”
    description: windows, named streams, append, close.
- ⚠️ Scheme list & intent (ID, R, GR) summarised in one place
  - R is fleshed out via GF-01. ID/GR may only exist as names / rough intent.
- ⚠️ Manifest contents & `manifest_check` semantics
  - You’ve used `manifest_check` in Phase 1; Phase 2 needs a statement like:
    “Here’s exactly what goes into it and why” (even if the definition is still basic).

**Suggested actions before Phase 2 sprints:**

- [ ] In SPEC-005 or APX contracts, add a concise section that:
  - [ ] Defines `PressWindowContext` responsibilities.
  - [ ] Lists schemes: ID, R, GR, with one-line descriptions.
  - [ ] States the *conceptual* recipe for `manifest_check` (inputs & invariants),
        even if the exact hash/MDL mix might be refined.

---

### B3. SceneFrame as canonical integration object

- ⚠️ SceneFrame is conceptually present, but not yet enshrined as “the one true bundle”
  - Trinity/Gate + build plan talk about per-tick integration, but there should
    be a paragraph that explicitly says:
    > All per-tick integration flows through `SceneFrame_v1`. Gate, NAP, and
    > later layers consume scene frames; we do not wire pillars directly.

**Suggested actions before Phase 2 sprints:**

- [ ] In either Trinity spec or SPEC-005:
  - [ ] Add a clear statement that `SceneFrame_v1` is the canonical per-tick integration object.
  - [ ] List which pillar populates which fields (UMX, Loom, Press, Gate/NAP).
  - [ ] Note that NAP envelopes and later governance/ledger layers derive from scene frames.

---

## Part C — Safe to discover in code (then backfill into specs)

For these items, the “status” is less about done/not-done and more about
**remembering the process rule**:

> You’re allowed to prototype these in code first, but nothing is allowed to
> stay “code-only” once it stabilises. Every behaviour needs a home in the specs.

### C1. Dynamic topology heuristics (SLP)

- Status: ✅ **safe to discover in code**, because they’re inherently experimental.
- Guardrail: once you find a growth/prune heuristic that feels promising, capture:
  - Conditions under which it fires.
  - What it does (add/remove/tune) and where.
  - Any thresholds or parameters.
- Target home: SPEC-003 (SLP) + maybe a small “heuristics appendix”.

### C2. AEON/APXi grammar richness

- Status: ✅ safe to prototype with a basic grammar and evolve.
- Guardrail: keep a note of every “encoding trick” you add so you can later
  consolidate them into a coherent AEON/APXi section.

### C3. Codex sophistication

- Status: ✅ safe to evolve in code.
- Guardrail: start with one simple motif type and a deterministic threshold.
  As soon as you like how it behaves on at least one scenario, write that exact
  detection rule and threshold into `CodexContracts_v1` or SPEC-005/SPEC-006.

### C4. PFNA channel taxonomy

- Status: ✅ safe to iterate as you learn which signals matter.
- Guardrail: even if the taxonomy changes, PFNA *format* and mapping rules must
  stay spec’d; only the set of channels / labels can be fluid.

### C5. Governance rules & budgets

- Status: ✅ absolutely fine to start as a toy scheduler with flat budget rules.
- Guardrail: when you introduce any prioritisation or budget formulas you intend
  to keep, write them down in SPEC-007. No silent “magic numbers” in code.

---

## Part D — Rule-of-Thumb (v1)

This is less “status” and more a **decision function** you can reuse whenever
you’re not sure whether something should be paper-first or code-first.

You can treat this as **agreed and ready** unless you explicitly change it later.

### D1. The core rule

- ✅ If it touches **physics, invariants, or base contracts** → paper first.
  - Flux rules, chain rules, conservation, tick semantics.
  - Core record shapes and required fields.
  - Anything GF-01 tests must assert.

- ✅ If it’s a **convenience layer or heuristic** → code can lead, but specs must catch up.
  - SLP heuristics, advanced grammars, Codex ML-ish behaviour.
  - PFNA taxonomy details, governance tweaks.

### D2. Practical application

When in doubt, ask:

1. **Can this break conservation, determinism, or core invariants?**
   - If yes → spec it first, then implement.
2. **Is this just “how we choose to use the engine” (e.g. a policy/heuristic)?**
   - If yes → you may prototype in code, but schedule a spec update task once
     you decide to keep it.

You can paste this rule-of-thumb into SPEC-000 or another top-level doc so it
stays visible as you work through sprints.

---

## TL;DR for Parts B/C/D

Before Phase 2 coding starts in earnest, it’s worth:

- [ ] Making `TopologyProfile_v1`, Press/APX window/streams/schemes, and `SceneFrame_v1`
      conceptually crisp in the specs (even if they’ll evolve).
- [ ] Accepting that SLP, AEON/APXi richness, Codex sophistication, PFNA taxonomy,
      and governance rules are best discovered **with** the code, not before it.
- [ ] Always reflecting any “keeper” behaviour back into the relevant SPEC or contract
      so paper stays the primary source of truth.
