# Aether — Planning Agent vs Coding Agent Roles (v1)

## 1. Roles

### 1.1 Planning / Spec Agent (this chat)

- Owns **roadmap, phases, and sprints**.
- Defines **SPEC docs, contracts, exams, issue templates**.
- Decides **what** needs to be built and **in what order**.
- Outputs files you can commit to `docs/` and use as the source of truth.
- Treats all pillar specs + physics as **canonical** and designs around them.

### 1.2 Coding Agent (GitHub / Codex)

- Works **inside the repo**, close to the code.
- Takes **SPECs, contracts, and GitHub issues** as input.
- Decides **how** to implement (file structure, function names, refactors)
  as long as it obeys the contracts and passes the exams.
- Should not invent new behaviour that isn’t in the specs.

In short:

> Planning/spec here, implementation there.  
> Coding agent follows the plan; it doesn’t rewrite the roadmap.

---

## 2. Who decides sprints?

- **You + this planning agent** decide:
  - Sprint boundaries,
  - Which SPEC/phase/epic is in scope,
  - The text of the GitHub issues.

- The **coding agent**:
  - Picks up those issues,
  - Writes code + tests,
  - May suggest refactors or extra issues,
  - But doesn’t move milestones or redefine phases unless you update the plan here.

If the coding agent proposes something big (e.g. a new design pattern or change
to a contract), best practice is:

1. Capture that suggestion as notes / issues.
2. Come back here and **update the specs/plan**.
3. Then let future coding work follow the updated specs.

---

## 3. How to feed the coding agent cleanly

When you start coding:

1. Create the repo skeleton from the tree we designed.
2. Commit the key docs:
   - Master pillar specs,
   - SPEC-002, SPEC-005,
   - Physics core + GF-01 exam,
   - Core contracts (`TopologyProfile_v1`, `Profile_CMP0_v1`, `UMXTickLedger_v1`),
   - Any relevant issue packs.
3. In GitHub:
   - Create issues by pasting the prepared issue bodies.
   - Group them into milestones (`Phase 1`, `Phase 2`, etc.).
4. Point the coding agent at:
   - A specific issue,
   - The relevant docs (by path),
   - And say: “Implement this issue using these contracts/specs, do not change them.”

That keeps the **source of truth** here, and the **mechanics of code** in the
coding agent, without them stepping on each other.
