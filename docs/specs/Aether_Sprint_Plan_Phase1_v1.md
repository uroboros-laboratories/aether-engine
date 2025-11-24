# Aether Engine — Phase 1 Sprint Plan (SPEC-002)

This is a lightweight sprint plan you can use **before** the GitHub repo exists.  
When you _do_ create the repo, you can drop this into `docs/specs/` (or `docs/`)
and wire it into your Projects board.

Scope here = **Phase 1 / SPEC-002 — GF-01 CMP-0 Baseline**.

---

## Sprint 0 — Bootstrap & Wiring (optional but recommended)

**Theme:** Get the playground ready, no “real” engine yet.

**Duration:** 0.5–1 week (can be background work while we refine later phases).

### Goals

- Have a working `aether-engine` repo on GitHub.
- Local dev environment ready (Python/TypeScript/whatever stack you choose later).
- Contracts + CI skeleton in place so Phase 1 work has a home.

### Suggested Work

- [ ] Create GitHub repo from the `aether-engine` skeleton zip.
- [ ] Commit:
  - [ ] `docs/specs/SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`
  - [ ] `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`
  - [ ] All pillar master specs.
  - [ ] All SPEC-002..007 issue packs.
- [ ] Set up:
  - [ ] Milestones for Phase 1–5.
  - [ ] Labels from the issue packs (spec, phase, component, type, priority).
  - [ ] GitHub Project board (Kanban or table view).
- [ ] Add minimal CI:
  - [ ] Lint + tests job (even if tests are empty).
  - [ ] Branch protection on `main` (optional but nice).

**Exit condition:** You can create issues from SPEC-002 and run a basic test workflow
(green) on the default branch.

---

## Sprint 1 — GF-01 Topology, Profile, and UMX CMP-0 Core

**Theme:** Make the **integer flux engine** real and match GF-01 tables.

**Duration:** ~1 week (depending on your evenings/weekends bandwidth).

### Targets (Issues from SPEC-002)

- **Issue 1:** CMP-0 Topology & Profile
- **Issue 2:** UMX CMP-0 Engine & Tick Ledger

### Goals

- Encode GF-01 topology + CMP-0 profile exactly in code.
- Implement the UMX CMP-0 step function and tick ledger.
- Pass tick-by-tick GF-01 tests for ticks 1–8.

### Suggested Breakdown

- [ ] Implement contracts:
  - [ ] `TopologyProfile_v1`
  - [ ] `NodeProfile_v1`, `EdgeProfile_v1`
  - [ ] `Profile_CMP0_v1`
  - [ ] `UMXTickLedger_v1`, `EdgeFlux_v1`
- [ ] Implement GF-01 profile:
  - [ ] `gid = "GF01"`, `N = 6`
  - [ ] Edges 1..8 with correct `(i, j, k, cap, SC, c)`.
  - [ ] `modulus_M`, `C0`, `SC`, `I_block_spacing_W` as per SPEC-002.
- [ ] Implement flux rule (CMP-0):
  - [ ] `du = pre_u[i] - pre_u[j]`
  - [ ] `raw = floor(k * abs(du) / SC)`
  - [ ] `f_e = sign(du) * min(raw, cap, abs(du))`
  - [ ] Conservation check on sums.
- [ ] Implement `UMX.step(...) -> UMXTickLedger_v1`.
- [ ] Tests vs paper:
  - [ ] `u(0) = [3,1,0,0,0,0]`.
  - [ ] Ticks `t = 1..8`: `pre_u`, `post_u`, `du`, `raw`, `f_e` match GF-01 tables.
  - [ ] `sum_pre_u == sum_post_u == z_check` per tick.

**Exit condition:** For GF-01, running the UMX engine alone for ticks 1–8
perfectly reproduces the paper tables (no floats anywhere).

---

## Sprint 2 — Loom Chain & Press/APX R-Mode

**Theme:** Add the **time axis** and **compression manifest** on top of UMX.

**Duration:** ~1–1.5 weeks.

### Targets (Issues from SPEC-002)

- **Issue 3:** Loom CMP-0 Chain & Blocks
- **Issue 4:** Press/APX CMP-0 (R-mode & Manifest)

### Goals

- Implement Loom chain `C_t` and P/I-blocks for CMP-0.
- Implement minimal Press/APX to match GF-01 manifests and `manifest_check` values.

### Suggested Breakdown

- [ ] Loom:
  - [ ] Implement `LoomPBlock_v1` and `LoomIBlock_v1`.
  - [ ] CMP-0 `s_t` rule: `s_t = 9` for GF-01.
  - [ ] Chain rule: `C_t = (17 * C_{t-1} + 23 * s_t + seq_t) mod M`.
  - [ ] Emit I-block every `W = 8` ticks with topology + `post_u` snapshot.
  - [ ] Tests:
    - [ ] `C_1..C_8` match GF-01 vector.
    - [ ] I-block at `t=8` matches spec.
- [ ] Press/APX:
  - [ ] Implement `APXManifest_v1` + `APXStream_v1`.
  - [ ] Implement minimal `"R"` scheme encoder.
  - [ ] Build streams:
    - [ ] `S1_post_u_deltas`.
    - [ ] `S2_fluxes`.
  - [ ] Compute `L_model`, `L_residual`, `L_total`, `manifest_check`.
  - [ ] Tests:
    - [ ] Window ticks 1–8: `L_total(S1)=7`, `L_total(S2)=8`, `manifest_check=487809945`.
    - [ ] Window ticks 1–2: `manifest_check=869911338` and bit counts as per sheets.

**Exit condition:** Given the UMX tick ledgers from Sprint 1,
Loom and Press/APX reproduce the exact chain and APX manifest numbers for GF-01.

---

## Sprint 3 — Gate/NAP Wiring, TickLoop, Determinism Harness

**Theme:** Close the loop: full **tick pipeline** + **determinism**.

**Duration:** ~1–1.5 weeks.

### Targets (Issues from SPEC-002)

- **Issue 5:** NAPEnvelope & Minimal Gate/TBP Integration  
- **Issue 6:** TickLoop Wiring (`run_gf01`)  
- **Issue 7:** Determinism Harness & Regression Snapshot

### Goals

- Build `SceneFrame_v1` and `NAPEnvelope_v1` outputs per tick.
- Create a single `run_gf01()` entrypoint that wires UMX, Loom, Press, Gate/NAP.
- Add deterministic snapshot tests so GF-01 becomes your golden baseline.

### Suggested Breakdown

- [ ] Gate/NAP:
  - [ ] Implement `SceneFrame_v1` and `NAPEnvelope_v1`.
  - [ ] Minimal Gate that, per tick, builds a scene frame from:
    - [ ] `gid`, `run_id`, `tick`, `nid`.
    - [ ] `pre_u`, `post_u` (UMX).
    - [ ] `C_prev`, `C_t` (Loom).
    - [ ] `window` info + `manifest_check` (Press/APX).
  - [ ] NAP envelope fields:
    - [ ] `v = 1`, `gid = "GF01"`.
    - [ ] `layer = "DATA"`, `mode = "P"`.
    - [ ] `payload_ref = manifest_check`.
    - [ ] `seq = tick`, `prev_chain = C_prev`, `sig = ""`.
  - [ ] Tests vs GF-01 envelope sheet.
- [ ] TickLoop / `run_gf01()`:
  - [ ] Orchestrate ticks 1–8 end-to-end.
  - [ ] Return UMX ledgers, Loom blocks, APX manifests, NAP envelopes.
  - [ ] One integration test asserting all GF-01 exam conditions.
- [ ] Determinism harness:
  - [ ] Canonical JSON serialisation for all artefact types.
  - [ ] Double-run test: run `run_gf01()` twice, compare outputs byte-for-byte.
  - [ ] Snapshot test: persist known-good GF-01 snapshot and compare on each run.

**Exit condition:**

- `run_gf01()` exists.
- All GF-01 checks pass.
- A snapshot test guards against future regressions.
- SPEC-002 is effectively “done” from a code point of view.

---

## After Phase 1

Once this is complete, you have:

- A deterministic engine that exactly matches paper GF-01 under CMP-0.
- A clean “contract + spec + fixtures + tests” pipeline.
- A clear jumping-off point to start Phase 2 (SPEC-005: UMX/Loom/Press/Gate generalisation).

When you’re ready, we can do a similar sprint plan for **Phase 2 / SPEC-005**
so your GitHub Projects board shows a full path from GF-01 baseline → general engine.
