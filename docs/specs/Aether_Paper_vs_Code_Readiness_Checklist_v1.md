# Aether Engine — Paper vs Code Readiness Checklist (v1)

This is a practical checklist for **what must be locked on paper** before you start
coding, and what can safely be discovered in code then backfilled into the specs.

It’s written assuming the sprint plan we’ve laid out (Sprints 0–14).

---

## Part A — MUST be final on paper before Sprint 1

These are “physics + contracts” items for **Phase 1 / SPEC-002** (GF-01 CMP-0
baseline). You don’t start coding the engine until these are stable enough that
any changes are rare and deliberate.

### A1. Core physics & invariants

- [ ] **CMP-0 flux rule** fully specified:
  - Exact formula for `du`, `raw`, `f_e`.
  - Constraints on caps, scaling, and allowed ranges.
- [ ] **Conservation rule** clearly stated:
  - `sum_pre_u == sum_post_u == z_check` per tick.
  - What counts as a violation and how it’s handled (hard fail vs diagnostics).
- [ ] **Chain rule** fully specified for CMP-0:
  - `C_t = (a * C_{t-1} + b * s_t + seq_t) mod M` plus exact values for `a`, `b`, `M`.
  - How `seq_t` is defined.
- [ ] **s_t definition** for GF-01:
  - For baseline: explicit statement that `s_t = 9` for all ticks (and where that comes from).
- [ ] **Profile constants** for CMP-0 fixed:
  - `C0`, `modulus_M`, `SC`, `I_block_spacing_W`,
  - Any other baked-in values in Profile_CMP0.

### A2. Type contracts (v1) for Phase 1

All of these need at least a v1 contract doc finished, even if some fields are
marked “reserved” for later phases.

- [ ] `TopologyProfile_v1`
- [ ] `Profile_CMP0_v1`
- [ ] `UMXTickLedger_v1` and `EdgeFlux_v1`
- [ ] `LoomPBlock_v1` and `LoomIBlock_v1`
- [ ] `APXStream_v1` and `APXManifest_v1`
- [ ] `SceneFrame_v1`
- [ ] `NAPEnvelope_v1` (simple DATA/P version)
- [ ] Any run config / “exam” contract you expect tests to reference (e.g. `GF01_V0_Exam` doc, even if that’s a spec not a formal contract).

For each contract, you should have:

- Field names and types (integers, strings, enums, arrays).
- Which fields are required vs optional.
- Any invariants (e.g. sum checks, monotonic tick counters).

### A3. GF-01 reference artefacts

These are the **exam papers** for SPEC-002. They must be finished and checked.

- [ ] GF-01 tick tables 1–8:
  - `pre_u`, `post_u`, `du`, `raw`, `f_e`, `z_check` per tick.
- [ ] GF-01 chain values:
  - Exact list `C_1..C_8`.
- [ ] GF-01 APX sheets:
  - Bit counts for streams,
  - `L_model`, `L_residual`, `L_total`,
  - `manifest_check` for windows 1–8 and 1–2.
- [ ] GF-01 envelope sheet:
  - NAP envelopes tick-by-tick,
  - `prev_chain`, `payload_ref`, `layer`, `mode`, `seq`.
- [ ] A clear “exam” doc:
  - Text stating the conditions a digital implementation must pass to be considered a valid CMP-0 GF-01 baseline.

### A4. SPEC-002 doc & issues

- [ ] `spec_002_GF01_CMP0_Baseline_Build_Plan` (or equivalent) is in a good v1 state:
  - No obviously missing sections,
  - All key numbers present,
  - Cross-references to contracts and GF-01 docs are correct.
- [ ] SPEC-002 GitHub issue pack:
  - Issues 1–7 exist and match the spec.
  - No major TODOs left in the wording (“fill later” style).

Once A1–A4 are done, you’re safe to start **Sprint 1** and let code mirror the paper.

---

## Part B — Should be sketched on paper before Phase 2 coding

These don’t have to be “final forever” but should be more than vibes before you
implement SPEC-005 (Phase 2).

### B1. Topology & profile generalisation

- [ ] `TopologyProfile_v1` clearly supports **multiple named topologies**:
  - Node/edge ID rules,
  - How multiple topologies are referenced in configs.
- [ ] `Profile_CMP0_v1` vs “other profiles” positioning:
  - Statement of how future profiles might differ (even if they’re not defined yet).
- [ ] A written idea of canonical toy topologies:
  - At least: line, ring, star, small mesh.

### B2. Press/APX modes & registry

- [ ] Concept of `PressWindowContext` written down:
  - Windows, named streams, tick-by-tick append.
- [ ] Schemes list and intent:
  - ID, R, GR names and what they are roughly meant to do.
- [ ] Manifest contents & `manifest_check` semantics:
  - What fields must be included,
  - How `manifest_check` is computed in principle (even if not fully formal).

### B3. SceneFrame as the main integration object

- [ ] A short doc section that explicitly states:
  - “SceneFrame_v1 is the canonical per-tick integration object”,
  - Which pillar contributes which fields,
  - That NAP envelopes and later outputs derive from scene frames, not ad hoc wiring.

---

## Part C — Safe to discover in code (then backfill into specs)

These are areas where it’s actually healthy to prototype in code, then update
the specs once you’ve learned what works. The rule: **no behaviour lives only
in code for long**—everything gets written back into docs once it stabilises.

### C1. Dynamic topology heuristics (SLP)

- Exact strategies for:
  - When to grow vs prune,
  - Which edge/node to touch,
  - How to pick parameters for new edges.
- You can start with a simple, arbitrary heuristic in code and then document it
once you like it (or replace it after experiments).

### C2. AEON/APXi grammar richness

- Detailed grammar / codebook design,
- Clever factorizations or compression tricks,
- Multiple AEON/APXi “dialects”.
- Start with a basic structural stream + simple grammar; refine later.

### C3. Codex sophistication

- Types of motifs beyond the first/simple patterns,
- Rich MDL metrics,
- Higher-level proposals and scoring.
- Start with one motif type and a tiny heuristic. If it’s useful, put the exact
heuristic and thresholds back into `CodexContracts_v1` or the relevant SPEC.

### C4. PFNA channel taxonomy

- How many channels,
- How they’re grouped,
- Named families of inputs (sensors, control, user input, etc.).
- Start with a minimal PFNA placeholder; extend once you’ve seen how it wants
to interact with UMX/Loom/Press in practice.

### C5. Governance rules & budgets

- Exact budget formulas,
- How runs are prioritised,
- When Codex proposals are escalated / surfaced.
- You can begin with a very simple batch scheduler and a flat budget, then
write down the more interesting governance patterns as they emerge.

---

## Part D — Operating rule of thumb

- **If it touches physics / invariants / base contracts → paper first.**
- **If it’s a convenience layer or heuristic → code can lead, but specs must catch up.**
- You can always refine and version the specs, but every version should be
good enough that code can treat it as a contract, not a moving target.

This checklist is meant to be dropped into `docs/` or `docs/specs/` and updated
as you evolve the system.
