# UNIVERSAL MATRIX PILLAR — UMX Master Implementation Spec v1 (Aggregated)

> This document was programmatically assembled from the `implementation.zip` pack.
> Every markdown and PDF spec is embedded verbatim below; TSV fixtures are summarized with schema and row counts.
> Source artifacts are preserved under their original filenames so they can be cross‑referenced in code reviews.

## Part 0 — Provenance and Source Artifacts

### 0.1 Root-level implementation pack contents

- `implementation/UMX_README_FOR_DEVS_v1.md`
- `implementation/Umx Complement Doc H — Nap Integration (full).pdf`
- `implementation/Universal Matrix Pillar — Topology Substrate & Conservation Engine.pdf`
- `implementation/Universal_Matrix_Pillar_UMX_v1_2025-11-17_maximal.zip`
- `implementation/astral_press_pillar_dev_implementation_spec_v_0.md`
- `implementation/umx_complement_doc_e_invariants_layout.md`
- `implementation/umx_complement_doc_f_llp_slp_propagation.md`
- `implementation/umx_complement_doc_f_llp→slp_propagation_temporal_behaviour.md`
- `implementation/umx_complement_doc_g_nap_integration.md`
- `implementation/umx_complement_doc_h_nap_integration_full.md`
- `implementation/umx_complement_doc_i_gap_closure_profile_specs.md`
- `implementation/umx_complement_docs_a_d_zero_layer_a_1.md`
- `implementation/umx_fixtures_testbed_integration_pack_2025_11_17.md`
- `implementation/umx_full_buildplan_v_1_2025_11_17.md`
- `implementation/umx_gap_closure_build_plan_pass_01_2025_11_16.md`
- `implementation/umx_gap_closure_build_plan_pass_02_2025_11_16.md`
- `implementation/umx_gap_closure_pass_3_bridge_gate_cross_cut_2025_11_16.md`
- `implementation/umx_gap_closure_pass_5_aether_full_clean_master_pack_2025_11_16.md`
- `implementation/umx_spec_artifacts_bundle_1_2025_11_16.md`
- `implementation/umx_spec_artifacts_bundle_2_2025_11_16.md`
- `implementation/umx_spec_artifacts_bundle_3_2025_11_16.md`
- `implementation/umx_spec_artifacts_bundle_4_umx_tbp_pack_2025_11_16.md`
- `implementation/umx_spec_master_index_readme_2025_11_16.md`
- `implementation/umx_trinity_gate_integration_spec_v_1_2025_11_17.md`
- `implementation/universal_matrix_pillar_spec_v_1.md`

### 0.2 Nested pack contents — `Universal_Matrix_Pillar_UMX_v1_2025-11-17_maximal.zip`

- `README/UMX_Full_Buildplan_v1.md`
- `README/UMX_Spec_Master_Index_v1.md`
- `companions_pending/MDL_Placement_and_Motif_Spec_UMX_Press_Codex_todo.md`
- `companions_pending/PFNA_Universal_Commit_Record_Spec_todo.md`
- `companions_pending/UMX_Profiles_and_Budgets_Annex_todo.md`
- `core/anchor_map_v1.md`
- `core/subtick_semantics_v1.md`
- `core/umx_layers_policy_v1.md`
- `core/umx_mdl_objective_v1.md`
- `core/umx_profile_v1.md`
- `fixtures/UMX/fixtures_index.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/assertions.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/drift_metrics.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/edges.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/events.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/ledger.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/nap_envelopes.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/nodes.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/profile.tsv`
- `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/residual_epsilon.tsv`
- `integration/umx_commit_and_snapshot_manifests_v1.md`
- `integration/umx_nap_bus_contract_v1.md`
- `integration/umx_node_manifest_v1.md`
- `integration/umx_slp_snapshot_ir_v1.md`
- `integration/umx_two_phase_tick_contract_v1.md`
- `integration/umx_u_ledger_contract_v1.md`
- `stress_emergence/umx_drift_and_budget_coupling_v1.md`
- `stress_emergence/umx_emergence_bands_v1.md`
- `stress_emergence/umx_epsilon_layers_and_drift_metrics_v1.md`
- `stress_emergence/umx_kill_switch_and_quarantine_v1.md`
- `stress_emergence/umx_paper_runtime_equivalence_v1.md`
- `stress_emergence/umx_stress_test_matrix_v1.md`
- `tbp/tbp_umx_development_roadmap_v_1.md`
- `tbp/tbp_umx_golden_fixtures_pack_v_1.md`
- `tbp/tbp_umx_implementation_spec_v_1.md`
- `tbp/tbp_umx_operator_runbook_v_1.md`
- `tbp/tbp_umx_verification_plan_fixtures_crosswalk_v_1.md`
- `tbp/tbp_umx_verification_test_plan_v_1.md`
- `testbed/UMX/S01_UMX_MINIMAL/assertions.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/drift_metrics.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/edges.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/events.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/ledger.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/nap_envelopes.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/nodes.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/profile.tsv`
- `testbed/UMX/S01_UMX_MINIMAL/residual_epsilon.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/assertions.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/drift_metrics.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/edges.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/events.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/ledger.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/nap_envelopes.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/nodes.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/profile.tsv`
- `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/residual_epsilon.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/assertions.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/drift_metrics.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/edges.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/events.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/ledger.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/nap_envelopes.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/nodes.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/profile.tsv`
- `testbed/UMX/S03_UMX_PROFILE_MDL/residual_epsilon.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/assertions.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/drift_metrics.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/edges.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/events.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/ledger.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/nap_envelopes.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/nodes.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/profile.tsv`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/residual_epsilon.tsv`
- `testbed/UMX/UMX_Fixtures_and_Testbed_Integration_Pack_v1.md`

## Part 1 — Top-level UMP/UMX Spec, README, and Developer Orientation

### Source: `universal_matrix_pillar_spec_v_1.md` (verbatim)

UNIVERSAL MATRIX PILLAR SPEC V1

---

## 0. Canon & Source of Truth

From the UMP v1 spec:

> “**Canonical name:** Universal Matrix Pillar (UMP)
> **Former name:** Luminous Lattice
> **Protocol counterpart:** Synaptic Ley Protocol (SLP)
> **Role:** Deterministic integer substrate for state storage and conservative propagation.”
> (“Canvas — Universal Matrix Pillar v1 — Build Spec.md”)

From the SLP spec:

> “Flux per edge (u,v): `du = Su − Sv; flux = floor(k * du / SC)`; move `flux` from the higher to the lower potential.
> Manhattan neighborhood with radius `r`, degree cap `D★`, causality cap `c` per tick.
> Strict integer arithmetic and deterministic edge order ensure replayability.
> Invariants: conservation of total sum, causality (no effects beyond `c` hops), determinism.”
> (“Canvas — Synaptic Ley Protocol (SLP) — Propagation Semantics.md”)

From the NAP report:

> “Nexus Aeternus Protocol (NAP)… defines the meta-communication layer… NAP ensures temporal continuity, energetic balance, topological neutrality, and reproducibility across all simulations… no time drift between layers… identical outcomes given the same seed.”
> (“NAP report.pdf”, p.1)

From the UMP summary:

> “Integer-only substrate with deterministic propagation (SLP).
> Gate writes apply at τ+1 with stable ordering.
> Fixed-point coupling scale (SC=256 by default).
> P-deltas every tick; optional I-block checkpoints.”
> (“UMP Concept Summary.md”)

**For devs**: the normative behaviour is defined by:

* `Canvas — Universal Matrix Pillar v1 — Build Spec.md`
* `Canvas — Synaptic Ley Protocol (SLP) — Propagation Semantics.md`
* `Canvas — Gate Integration Guide (UMP v1).md`
* `Canvas — Test Matrix S1–S20 + G1-G6.md`
* `code/js/Aether_Substrate_v1_Core_Tests.ts`
* `NAP report.pdf`
* `AETHER-GATE-JS-main/src/core/nap.js`

Everything else is commentary.

---

## 1. Universal Matrix Pillar (UMX v1)

### 1.1 Role & Invariants

From the UMP spec:

> “Role: Deterministic integer substrate for state storage and conservative propagation.”
> (“Universal Matrix Pillar v1 — Build Spec.md”)

From §8:

> “**Invariants**
> – **Conservation:** Σ cells constant for SLP updates.
> – **Determinism:** Same inputs ⇒ identical root hashes per tick.
> – **Causality:** No effect beyond `c` hops per tick.
> – **Integer-only:** No floats, no randomness.”
> (same file)

**UMX MUST:**

1. Represent state as integer grids.
2. Use **integer-only** math (no floats, no randomness).
3. Preserve **global sum** of each layer under SLP propagation.
4. Guarantee deterministic results for identical configs + inputs.
5. Enforce a hop bound `c` so effects per tick are locally bounded.

> **Plain words:** UMX is a big integer grid where “stuff” moves between neighbouring cells. Total stuff never magically appears or disappears, and if you replay with the same inputs you get exactly the same evolution.

---

### 1.2 State Model

From §1 of the UMP spec:

> “**Grid:** H×W integer field per layer. Address key: `addrKey = y*W + x`.
> **Layers:** `stateWidthsPerLayer: number[]` where each entry i…count of integer fields for that layer (base config uses `[1]`).
> **Scale:** Fixed-point scale `SC = 256` (k = numerator / SC). All math is integer-only.
> **Genesis:** Seeds are applied as Gate writes at τ, become visible at τ+1.”
> (“Universal Matrix Pillar v1 — Build Spec.md”, §1)

From `Aether_Substrate_v1_Core_Tests.ts`:

```ts
export type IntField = Int32Array;
export interface LayerState { fields: IntField[] }

export interface UMXConfig {
  H: number; W: number;
  r: number; c: number; Dcap: number;
  stateWidthsPerLayer: number[];
  layersCouplingScaled: number[];   // k per layer, scaled by SC
  SC: number;
  pressEveryTick: boolean;
  iBlockEvery: number | null;
}
```

**Concrete data model**

* **Grid geometry:**

  * `H` rows, `W` columns.
  * Cell index `idx = y * W + x`, `0 ≤ x < W`, `0 ≤ y < H`.
  * **Address key:** `addrKey = idx = y*W + x`.
* **Layers & fields:**

  * Each layer `ℓ` has `stateWidthsPerLayer[ℓ]` integer fields.
  * Each field is `Int32Array(H * W)` (`IntField`).
  * **Base config:** one field per layer (`[1]`).
* **Scaling:**

  * Global integer scale `SC = 256`.
  * Coupling strength per layer is an integer `kℓ = layersCouplingScaled[ℓ]`.
  * Real coupling is `kℓ / SC`, but you never leave integers.
* **Genesis:**

  * Initial seeds are given as Gate writes (see 1.4).
  * A write scheduled at tick `τ` is visible in the lattice at `τ+1`.

> **Plain words:** Each layer is one or more `Int32Array`s of length `H*W`. Values are fixed-point with denominator 256. Positions are flattened `y*W + x`.

---

### 1.3 Neighborhood & Topology

From §2 of the UMP spec:

> “**Neighborhood radius** `r` (Manhattan metric).
> **Degree cap** `D★` keeps the neighbor set bounded and ordered deterministically.
> **Causality bound** `c` limits effective hops per tick (no effect beyond `dist > c`).”
> (“Universal Matrix Pillar v1 — Build Spec.md”, §2)

From the test matrix:

> Example S1: “64×64, r=1, c=1, D★=4, k_base (/256)=64…”
> (“Test Matrix S1–S20 + G1-G6.md”)

From `Aether_Substrate_v1_Core_Tests.ts` (edge representation):

```ts
private edges: Array<{u:number;v:number;dist:number}>;
// built by buildEdges(H,W,r,Dcap)
```

**Topology definition**

* **Neighbourhood:**

  * Use **Manhattan distance**: `dist = |dx| + |dy|`.
  * A pair of cells `(u,v)` is eligible if `1 ≤ dist ≤ r`.
* **Edges:**

  * Precompute a static list `edges: {u,v,dist}[]` at construction.
  * `u` and `v` are integer indices in `[0, H*W)`.
  * Each cell has at most `D★` outgoing neighbours (degree cap).
* **Edge ordering:**

  * `edges` is stored in a **stable, deterministic order** (as implemented by `buildEdges`).
  * That order is used every tick; replay depends on it.
* **Causality bound `c`:**

  * Propagation for a given tick is restricted so effects do not propagate beyond `c` hops in that tick (see SLP).

> **Plain words:** For each cell, UMX precomputes a fixed list of neighbours within Manhattan radius `r`, capped at `D★` neighbours per cell, and always loops them in the same order.

---

### 1.4 Gate Intake Semantics

From §3 of the UMP spec:

> “Writes are queued with provenance `(sourceId, tauIn, layerId, fieldId, addrKey, mode, intValue)`.
> **Ordering:** stable sort by `(addrKey, layerId, fieldId, sourceId, tauIn, mode, intValue)`.
> **Boundary:** apply at tick boundary; a write arriving at τ takes effect at **τ+1**.
> **Modes:** `set` (overwrite cell), `add` (integer addition).
> **Rejections:** out-of-bounds, invalid layer/field, or timing after the τ+1 window.
> **Idempotence:** enforced at the perimeter by NAP/Gate (see G2/G3/G6 tests).”
> (“Universal Matrix Pillar v1 — Build Spec.md”, §3)

From `Aether_Substrate_v1_Core_Tests.ts`:

```ts
export interface GateWrite {
  sourceId:string;
  tauIn:number;
  addr?: {x:number;y:number};
  addrKey?: AddrKey;
  layerId:number;
  fieldId:number;
  intValue:number;
  mode: "set" | "add";
}
```

With helpers:

```ts
enqueueByteGrid8([{x,y,layerId,fieldId,byte}])
enqueueEventLogTriples([{addrKey,key,value}]) // dev-binding: key=0 → base field add
```

**Intake rules**

* **Queueing:**

  * UMX maintains `pending: GateWrite[]`.
  * `enqueue` appends a write with `tauIn = current τ` unless you override.
* **Modes:**

  * `mode: "set"` → exact assignment of `intValue`.
  * `mode: "add"` → integer addition of `intValue`.
* **Application time:**

  * All writes with `tauIn == current τ` are applied at **boundary of tick τ**, becoming visible to SLP at **τ+1**.
* **Ordering & idempotence:**

  * UMX applies writes in a **stable order** as specified.
  * Idempotence (no double-application) is handled at the Gate/NAP layer (see NAP section and Gate tests).

> **Plain words:** The Gate queues integer writes; UMX applies them at tick boundaries in a fixed order, and those changes show up in the grid one tick later.

---

### 1.5 Propagation & Tick (UMX + SLP)

From §4 and §5 of the UMP spec:

> “For each edge (u,v) up to c-hops:
> `du    = S[u] − S[v]`
> `flux  = floor(k * du / SC)`   // integer division
> `S[u] -= flux`
> `S[v] += flux`
> …
> **Conservation:** Sum over all cells is invariant under SLP.
> **Determinism:** Edge ordering and integer arithmetic guarantee replay.
>
> **τ (tick):** At each tick, queued writes are applied, then SLP executes.
> **P-delta:** Optional per-tick change list for telemetry/press coupling.
> **I-block:** Optional snapshot cadence for checkpointing/replay.”
> (“Universal Matrix Pillar v1 — Build Spec.md”, §§4–5)

From the SLP spec:

> “Flux per edge (u,v): `du = Su − Sv; flux = floor(k * du / SC)`; move `flux` from the higher to the lower potential.
> Manhattan neighborhood with radius `r`, degree cap `D★`, causality cap `c` per tick.”
> (“Synaptic Ley Protocol (SLP) — Propagation Semantics.md”)

From `Aether_Substrate_v1_Core_Tests.ts`:

```ts
async tickOnce(): Promise<TickLedger> { /* applyPendingAtBoundary(); stepIntegerFlux(c); ... */ }

export interface TickLedger {
  tau:number;
  rootHash:string;
  pBlock: PDelta[];
  iBlock?: { snapshotHash:string; sizeBytes:number } | null;
}
```

**Tick pipeline**

For each call to `tickOnce()`:

1. Capture previous state bytes (for diff + hashing).
2. Apply all queued writes with `tauIn == τ` at the boundary.
3. Call `stepIntegerFlux(c)`:

   * For each layer `ℓ` and each edge `(u,v)`:

     * `du = Sℓ[u] − Sℓ[v]`.
     * `flux = floor(kℓ * du / SC)` (`kℓ = layersCouplingScaled[ℓ]`).
     * `Sℓ[u] -= flux`, `Sℓ[v] += flux`.
4. Compute `rootHash` = SHA-256 of current state bytes.
5. If `pressEveryTick == true`, compute `pBlock` = list of `PDelta` for changed cells.
6. If `iBlockEvery != null` and `τ % iBlockEvery == 0`, compute `iBlock` snapshot header:

   * `snapshotHash`, `sizeBytes`.
7. Return `TickLedger`:

   * `{ tau, rootHash, pBlock, iBlock }`.
8. Increment `τ`.

**SLP invariants**

* `Σ_u Sℓ[u]` is conserved for each layer ℓ under `stepIntegerFlux`.
* No effect travels beyond `c` hops per tick due to the hop bound.
* Determinism is guaranteed by:

  * fixed integer math,
  * fixed edge ordering,
  * fixed tick pipeline.

> **Plain words:** Every tick, UMX applies queued writes, then SLP does the “flow” step along all edges. It then hashes the whole grid and optionally records which cells changed and periodic snapshots.

---

### 1.6 Parameters & Test Matrix

From §6–7 in the UMP spec:

> “**Parameters (v1 reference)**
> `H,W` default 64,64; `r=1`; `c=1`; `D★=4`; `SC=256`; `k per layer = SC/4`; `pressEveryTick=true`; `iBlockEvery=32`.
> “…IDs `S1..S20`, `G1`, `G2`, `G3`, `G6` are **built into the core**. The Gate calls `testsList()`, `testsRun([...])`, or `testsRunAll()`; the Matrix does not render.”
> (“Universal Matrix Pillar v1 — Build Spec.md”, §§6–7)

From Test Matrix:

> S1–S20 and G1–G6 define specific combinations of `H×W, r, c, D★, k_base, residualKs, seed, ticks` with focus tags like “Baseline invariants”, “No propagation”, “Scaling sanity”, etc.
> (“Test Matrix S1–S20 + G1-G6.md”)

**Reference configuration**

* Default v1 test config (S1):

  * `H=64`, `W=64`, `r=1`, `c=1`, `D★=4`,
  * single layer, `k_base = 64` (i.e. 0.25),
  * seed at center cell, ticks=24.
* Built-in tests assert:

  * conservation, determinism, no-propagation, scaling, boundary behaviour.

> **Plain words:** There’s already a battery of tests baked in. If they pass, the core is behaving as designed.

---

## 2. Synaptic Ley Protocol (SLP v1)

SLP in v1 is exactly the **flux kernel** used by UMX; there is no public plasticity API in this pack.

From SLP spec:

> “Flux per edge (u,v): `du = Su − Sv; flux = floor(k * du / SC)`; move `flux` from the higher to the lower potential.
> Manhattan neighborhood with radius `r`, degree cap `D★`, causality cap `c` per tick.
> Strict integer arithmetic and deterministic edge order ensure replayability.
> Invariants: conservation of total sum, causality (no effects beyond `c` hops), determinism.”
> (“Synaptic Ley Protocol (SLP) — Propagation Semantics.md”)

From UMP spec §4:

> “For each edge (u,v) up to c-hops:
> `du    = S[u] − S[v]`
> `flux  = floor(k * du / SC)`
> `S[u] -= flux`
> `S[v] += flux`”
> (“Universal Matrix Pillar v1 — Build Spec.md”)

**SLP v1 definition**

* **Input:**

  * Layer field `Sℓ` (Int32Array),
  * Edge list `edges`,
  * Coupling integer `kℓ` (per layer),
  * Scale `SC`,
  * Hop cap `c`.
* **Operation per tick:**

  * Internally, `stepIntegerFlux(c)` iterates edges in deterministic order respecting the `c` hop bound.
  * For each `(u,v)`:

    * `du = Sℓ[u] − Sℓ[v]`.
    * `flux = floor(kℓ * du / SC)` (integer division).
    * `Sℓ[u] -= flux`, `Sℓ[v] += flux`.
* **Constraints:**

  * Integer math only.
  * Use prebuilt `edges` (no dynamic topology changes in v1 core).
  * Must preserve `Σ_u Sℓ[u]`.

> **Plain words:** SLP is literally “for each connection, nudge the higher side toward the lower side by (k/256) times the difference, all in integers.”

**Not in v1, but present in future design docs:**

* Dynamic SLP plasticity operations (`GROW`, `PRUNE`, etc.) are described in the topology PDF, but there is **no code or API for them in `Aether_Substrate_v1_Core_Tests.ts`**. Treat them as **future** (v2+) features.

---

## 3. Nexus Aeternus Protocol (NAP) — Relevant Pieces

### 3.1 Role & Scope

From NAP report:

> “NAP is the umbrella protocol for all inter-node and inter-layer communication in the Trinity architecture. Its core responsibilities include maintaining global synchrony…, enforcing reliable delivery semantics… and providing idempotence via cryptographic nonces and content-addressing… NAP ensures that distributed simulations behave as one synchronous organism with a consistent state across machines…”
> (“NAP report.pdf”, p.1–2)

> “Delivery Guarantees: … effectively exactly-once semantics… idempotence tokens ensure that duplicates have no effect beyond the first application…
> Ordering & Causality: … logical timestamp (tick number τ) and… a topologically sorted order by layer and tick…”
> (ibid., p.2–3)

**For UMX integration, NAP MUST:**

* Provide **envelopes** carrying tick, ids, hashes.
* Enforce **idempotence** (duplicates no-op).
* Enforce **global tick alignment** and **causal ordering**.

---

### 3.2 Envelope Format (JS Gate Implementation)

From `AETHER-GATE-JS-main/src/core/nap.js`:

```js
import { sha256Hex } from "./hash.js";

export function canonicaliseNapEnvelope(env) {
  const canonical = {
    tick: env.tick,
    node_id: env.node_id,
    layer: env.layer,
    seed_hex: env.seed_hex,
    payload_ref: env.payload_ref,
    metrics: env.metrics ?? {},
    mode: env.mode ?? {},
    sig: env.sig ?? "",
  };
  return JSON.stringify(canonical);
}
...
  const payloadHash = sha256Hex(payload);
  const envelope = {
    tick,
    node_id: nodeId,
    layer,
    seed_hex: seedHex,
    payload_ref: `sha256:${payloadHash}`,
    metrics,
    mode,
    sig: "",
  };
  validateNapEnvelope(envelope);
  return { envelope, payloadHash };
```

**NAP envelope schema (JS)**

* `tick: number` — logical tick τ.
* `node_id: string` — sender node ID.
* `layer: string|number` — logical channel (e.g. `"gate"`, `"umx"`).
* `seed_hex: string` — deterministic seed (hex).
* `payload_ref: string` — `sha256:<hex>` content reference for payload.
* `metrics: object` — optional metrics map.
* `mode: object` — optional mode flags.
* `sig: string` — signature placeholder (v1 uses empty string).

> **Plain words:** Every message is a JSON object with tick, who sent it, which layer, a hash of the payload, and some metadata. That JSON is canonicalised and hashed/signed.

---

### 3.3 Delivery, Ordering, Idempotence

From NAP report:

> “NAP delivers messages with effectively exactly-once semantics… idempotence tokens ensure that duplicates have no effect…
> Each envelope’s nonce and content hash allow receivers to detect and discard duplicate messages deterministically.”
> (NAP report.pdf, p.2)

> “All NAP messages include a logical timestamp (tick number τ) and are processed in a globally consistent order… topologically sorted order by layer and tick – for a given tick τ, lower-layer messages are resolved before higher-layer ones, ties broken by node ID.”
> (ibid., p.3)

**Implications for UMX + Gate:**

* **Idempotence:**

  * UMX relies on Gate/NAP to ensure that the same logical write (same payload hash + nonce) is only applied once.
* **Ordering:**

  * UMX’s `tau` and NAP `tick` align.
  * Gate/NAP guarantee that all writes intended for tick `τ` are delivered/processed before UMX’s `tickOnce()` for that tick is called.
* **Exactly-once:**

  * From UMX’s perspective, each `GateWrite` derived from NAP envelopes is either applied once or not at all (if rejected or rolled back upstream).

---

## 4. UMX ↔ Gate ↔ NAP Integration Contract

From Gate Integration Guide:

> “**Contract the core exposes**
> – `testsList(): string[]`
> – `testsGet(id): TestScenarioSpec`
> – `testsRun(ids: string[] | number[]): Promise<TestReport>`
> – `testsRunAll(): Promise<TestReport>`
> – Intake helpers:
>   – `enqueueByteGrid8([{x,y,layerId,fieldId,byte}])`
>   – `enqueueEventLogTriples([{addrKey,key,value}])` (dev-binding: `key=0` routes to base field add)
>
> **Typical flow**
>
> 1. **Discover** tests ⇒ `core.testsList()`
> 2. **Run** a batch ⇒ `await core.testsRun(['S1','S10','G1'])`
> 3. **Render** the returned `TestReport` (your UI choice)
> 4. For live data, keep enqueuing Gate writes, then `await core.tickOnce()`”
>    (“Gate Integration Guide (UMP v1).md”)

From `Aether_Substrate_v1_Core_Tests.ts`:

```ts
export interface TestScenarioSpec { /* includes H,W,r,c,Dcap,kBaseScaled,residualKs,ticks,gatePlan,... */ }

export interface TestResultSummary {
  id:string;
  determinism:boolean;
  finalReach:number;
  totalWrites:number;
  totalRejects:number;
}

export interface TestReport {
  when:number;
  versions:string;
  results:TestResultSummary[];
}
```

**Integration rules**

1. **UMX core instantiation:**

   * Gate constructs `new AetherSubstrateCore(cfg: UMXConfig)`.
   * `cfg` must respect UMP spec (H,W,r,c,Dcap,SC, stateWidthsPerLayer, layersCouplingScaled, pressEveryTick, iBlockEvery).

2. **Test mode:**

   * Gate calls `core.testsList()`, `core.testsGet(id)`, `await core.testsRunAll()` as needed.
   * UMX returns `TestReport`; Gate is responsible for visualisation.

3. **Live mode:**

   * Gate transforms external inputs into:

     * grid writes (byte grid → `enqueueByteGrid8`), or
     * event triples (addrKey/value → `enqueueEventLogTriples`).
   * Gate calls `await core.tickOnce()` each tick.
   * Gate takes the returned `TickLedger` and:

     * optionally wraps it as a NAP payload + envelope,
     * logs it via Gate logbook / Loom,
     * renders state (e.g. from P-deltas).

4. **NAP surfaces (UMX side):**

   * UMX does **not** implement NAP; it only returns `TickLedger`.
   * Gate uses `nap.js` to canonicalise envelope and attach `payload_ref` pointing to the ledger payload hash.

> **Plain words:** The Matrix core is a pure engine. Gate is the one that talks NAP and runs the UI. The handshake surfaces are `enqueue*` and `tickOnce()`.

---

## 5. Concrete JS Implementation Plan (Offline Browser, Gate-Compatible)

This is the part you can literally hand to devs.

### 5.1 UMX Core Module

**Goal:** Import the existing core without modifying its semantics.

1. **Create a module** `src/core/umx.js` or `.ts` in the Gate repo.

2. **Copy or import** `Aether_Substrate_v1_Core_Tests.ts` from:

   * `MATRIX JS.zip → Universal_Matrix_Pillar_Pack_2025-11-08 (1)/code/js/Aether_Substrate_v1_Core_Tests.ts`

3. **Export**:

   * `AetherSubstrateCore`
   * `UMXConfig`, `GateWrite`
   * `TestScenarioSpec`, `TestReport`, `TestResultSummary`

4. **Do not change**:

   * Integer types (`Int32Array`),
   * Tick pipeline,
   * `enqueue*` semantics,
   * `stepIntegerFlux` behaviour.

### 5.2 Default Config Helper

Implement:

```ts
export function createDefaultUMX(): AetherSubstrateCore {
  const cfg: UMXConfig = {
    H: 64,
    W: 64,
    r: 1,
    c: 1,
    Dcap: 4,
    SC: 256,
    stateWidthsPerLayer: [1],
    layersCouplingScaled: [64], // SC/4 → coupling 0.25
    pressEveryTick: true,
    iBlockEvery: 32,
  };
  return new AetherSubstrateCore(cfg);
}
```

This matches the v1 reference (§6 in the UMP spec and S1 test).

### 5.3 Hooking into the Gate

In `AETHER-GATE-JS-main`:

1. **Instantiate UMX** in the operator or dev-console initialisation:

   ```ts
   import { createDefaultUMX } from "./core/umx";

   const umxCore = createDefaultUMX();
   ```

2. **Test harness in dev console**:

   * Provide UI buttons:

     * “List UMX tests” → `umxCore.testsList()`
     * “Run all UMX tests” → `await umxCore.testsRunAll()`

3. **Ingest Gate events into UMX**:

   * When Gate dev-console forms a “byte grid” input (e.g. user draws on a canvas), convert to:

     ```ts
     umxCore.enqueueByteGrid8([{ x, y, layerId, fieldId, byte }]);
     ```

   * When Gate receives an event triple (`addrKey, key, value`), and you want base-field add:

     ```ts
     // dev binding key=0 → base field add
     umxCore.enqueueEventLogTriples([{ addrKey, key: 0, value }]);
     ```

4. **Tick loop integration**:

   * Wherever the Gate advances its internal tick, also call:

     ```ts
     const ledger = await umxCore.tickOnce();
     ```

   * Use `ledger`:

     * `ledger.rootHash` → include in NAP payload_ref / logs.
     * `ledger.pBlock` → visualisation or Press.
     * `ledger.iBlock` → pass to Loom / logbook as checkpoint metadata.

### 5.4 NAP Wrapping

Use existing `nap.js`:

```js
import { createNapEnvelope } from "./core/nap.js"; // whatever factory wraps canonicaliseNapEnvelope

const payload = JSON.stringify(ledger);
const { envelope, payloadHash } = createNapEnvelope({
  tick: ledger.tau,
  nodeId: "umx-core",
  layer: "umx",
  seedHex: currentSeedHex,
  metrics: {},
  mode: {},
  payload,
});
```

* Store `payload` in logbook or local storage keyed by `payloadHash`.
* Forward `envelope` through Gate’s existing operator/logbook pipeline.
* Rely on Gate’s existing dedup + ordering to maintain NAP guarantees.

### 5.5 Validation

1. **Run UMX tests**:

   * `await umxCore.testsRunAll()` and check:

     * `determinism === true` for all,
     * no unexpected rejects,
     * sum invariants match expectations in S1/S17 reports from the pack (`tests/reports/*.md`).

2. **Replay check** (optional but recommended):

   * Capture a sequence of (writes, ledgers) for N ticks.
   * Re-run from a fresh `AetherSubstrateCore` with the same sequence.
   * Confirm all `rootHash` values per tick match.

> **Plain words:** Drop the core in as-is, wire its input/output to the Gate’s existing event and logging machinery, and rely on the baked-in tests to prove it works.

---

### Source: `UMX_README_FOR_DEVS_v1.md` (verbatim)

# UMX v1 — Start Here (Dev Onboarding)

You are holding the **Universal Matrix (UMX) v1** pack.

UMX = **graph substrate + tick engine + drift/emergence + NAP + ledger**  
Paper-first, pure-math core, JS shell around it, offline.

This README tells you:
- What to read.
- What to build.
- In what order.
- What “GO” looks like.

---

## 0. What you are expected to build

You are NOT designing the system. That’s done.

You **are** expected to:

- Implement a **deterministic UMX runtime**:
  - State = nodes, edges, layers, regions, profiles, residuals, epsilon, drift.
  - Tick = two-phase (read/compute, then commit/emit).
  - Integration = NAP envelopes, SLP snapshot IR, U-Ledger rows.
- Make it **round-trip clean** with the TSV fixtures:
  - Read the TSVs in `/fixtures/UMX/golden` and `/testbed/UMX`.
  - Run UMX.
  - Emit TSVs back out.
  - They should match Golden/expected TSVs for the scenarios.

The **math/behaviour is already specified** in the pack.  
Your job: wire it into a real offline JS runtime around a pure-math core.

---

## 1. Read these files first (in this order)

From the root of the ZIP:

1. `README/UMX_Spec_Master_Index_v1.md`  
   - Mental map of the whole spec surface and directory layout.

2. `README/UMX_Full_Buildplan_v1.md`  
   - What modules exist (M1–M9), which ones you implement in which phase, and when you’re allowed to call it “GO”.

3. Skim where you’ll actually live while coding:
   - Core semantics:
     - `core/umx_profile_v1.md`
     - `core/umx_layers_policy_v1.md`
     - `core/anchor_map_v1.md`
     - `core/subtick_semantics_v1.md`
     - `core/umx_mdl_objective_v1.md` (read, but note MDL companion pending)
   - Integration:
     - `integration/umx_node_manifest_v1.md`
     - `integration/umx_two_phase_tick_contract_v1.md`
     - `integration/umx_u_ledger_contract_v1.md`
     - `integration/umx_nap_bus_contract_v1.md`
   - Fixtures & testbed:
     - `fixtures/UMX/fixtures_index.tsv`
     - `testbed/UMX/UMX_Fixtures_and_Testbed_Integration_Pack_v1.md`

You do **not** need to memorise everything. You just need to know **where** things are.

---

## 2. Build order (high level)

Implement in this order:

1. **M1 — Core State & Topology**
2. **M2 — Tick Engine (Two-Phase + Subticks)**
3. **M6 — Drift, Epsilon Layers & Emergence Bands**
4. **M5 — Ledger, Commit & Snapshot Manifests**
5. **M4 — NAP Integration (Envelopes & Budgets)**
6. **M7 — Stress & Safety (Kill-Switch, Quarantine)**
7. **M8 — Fixtures & Paper Testbed Wiring** (really runs in parallel with 1–7)
8. **M9 — JS Shell & Operator UI**
9. **M3 — MDL & Learning Proposals** (last, and partially gated on companion MDL spec)

If you follow that sequence, you’ll be able to run **F01**, then **F02**, then **F04** fully.  
**F03** (MDL) becomes fully wired once the MDL companion spec lands.

---

## 3. Phase 1: Make F01 run end-to-end

Goal: **F01_MINIMAL_TOPOLOGY is green** in both fixtures and testbed.

Paths:

- Golden fixture:  
  `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/`
- Testbed scenario:  
  `testbed/UMX/S01_UMX_MINIMAL/` (this is a 1:1 mirror of F01 for runtime)

### Step 1 — Data structures

Mirror these TSV schemas exactly (column names & types) in your runtime:

- `nodes.tsv`
- `edges.tsv`
- `profile.tsv`
- `residual_epsilon.tsv`
- `drift_metrics.tsv`
- `events.tsv`
- `nap_envelopes.tsv`
- `ledger.tsv`
- `assertions.tsv`

For F01:

- There are 3 nodes (`N1`, `N2`, `N3`) in a line.
- One region (`R_MAIN`).
- Single layer (`layerId = 0`).
- No NAP traffic.
- All residuals/epsilon = 0.
- All drift = 0.
- All assertions = `PASS`.

You need import/export functions that can:

- Read these TSVs into your in-memory model.
- Write them back out exactly (no column renames, no extra junk).

### Step 2 — Tick engine for F01

Implement a **minimal** version of the tick engine:

- Two-phase tick as per `integration/umx_two_phase_tick_contract_v1.md`:
  - Phase A: read state + inputs, compute candidate updates.
  - Phase B: commit updates, append ledger row, emit events/envelopes.
- For F01:
  - There are **no structural changes**.
  - Residuals and epsilon are zero.
  - Drift stays at zero.
  - No NAP envelopes.

You just need enough logic to:

- Step through ticks 1..5.
- Keep state stable.
- Emit the ledger rows that match `ledger.tsv` in F01.

### Step 3 — Make runtime == Golden for F01

Process:

1. Load `S01_UMX_MINIMAL` TSVs into your runtime.
2. Run ticks as per profile (`P_UMX_MINIMAL_V1`).
3. Emit all TSVs again.
4. Compare against the Golden F01 TSVs (file-level diff or exact row comparison).

**Acceptance for Phase 1:**

- `nodes.tsv`, `edges.tsv`, `profile.tsv` round-trip clean.
- `residual_epsilon.tsv`, `drift_metrics.tsv`, `ledger.tsv`, `events.tsv`, `nap_envelopes.tsv`, `assertions.tsv` from runtime match the Golden files for F01.
- All assertion rows for `S01_UMX_MINIMAL` have `result = PASS`.

Once this is true, M1 + minimal M2 + minimal M5 + minimal M6 are effectively alive.

---

## 4. Phase 2: Add residuals, epsilon, drift, emergence (F02)

Next fixture:

- Golden fixture (to be populated later): `fixtures/UMX/golden/F02_RESIDUAL_EPSILON/`
- Scenario: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/`

Your job here:

- Implement **real** `residual_epsilon.tsv` semantics per:
  - `stress_emergence/umx_epsilon_layers_and_drift_metrics_v1.md`
  - `stress_emergence/umx_emergence_bands_v1.md`
- Implement drift metrics and bands:
  - Compute per-node drift over windows.
  - Compute global drift.
  - Map to bands: PASS / INVESTIGATE / FAIL.

Acceptance for Phase 2:

- For S02, drift metrics and bands match the Golden TSVs when they’re filled in.
- At least one window is classified as `INVESTIGATE` in the F02 design.

You’ll likely implement the **full M6** here.

---

## 5. Phase 3: NAP, budgets, stress & safety (F04)

Once F01/F02 are solid:

- Implement full NAP contract logic from:
  - `integration/umx_nap_bus_contract_v1.md`
- Implement budget tracking, backpressure and dead-letter.
- Implement kill-switch and quarantine semantics from:
  - `stress_emergence/umx_kill_switch_and_quarantine_v1.md`
- Implement stress metrics and evaluation per:
  - `stress_emergence/umx_stress_test_matrix_v1.md`

Fixture & scenario:

- `fixtures/UMX/golden/F04_STRESS_SAFETY/`
- `testbed/UMX/S04_UMX_STRESS_SAFETY/`

Acceptance for Phase 3:

- Properties like `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `kill_switch_ok`, `drift_guard_ok` match the Golden/expected values for S04.
- NAP-related fields in `nap_envelopes.tsv` and `ledger.tsv` behave exactly as described.

At this point, **M4**, **M7**, and the rest of **M5** are in good shape.

---

## 6. Phase 4: MDL & proposals (F03) — gated

MDL is defined in:

- `core/umx_mdl_objective_v1.md`
- And will be fully pinned down by:
  - `companions_pending/MDL_Placement_and_Motif_Spec_UMX_Press_Codex_todo.md`

Until that companion spec is finished, treat **M3** and **F03** as:

- **Provisional**: the wiring is there, but the exact coding scheme (how you compute L, and ΔL) comes from the companion.
- Fixtures index already marks F03 as `provisional`.

Your job when the MDL spec lands:

- Implement MDL as **pure math** separate from JS.
- Wire proposal evaluation into the tick engine for F03:
  - One proposal that should be accepted (ΔL ≤ −τ).
  - One proposal that should be rejected (ΔL > −τ).
- Make sure F03’s `assertions.tsv` reflects that.

---

## 7. JS shell & Operator UI (M9)

Everything above can be done without a nice UI. Once the core is working:

- Wrap it with a **simple offline JS UI**:
  - Choose scenario (S01–S04).
  - Load TSVs.
  - Run 1 tick / N ticks.
  - Show basic numeric dashboards for drift, budgets, bands, flags.
  - Export TSVs back to disk.

No fancy charts required for v1. Reliability and determinism matter more.

---

## 8. What you can ignore **for now**

You can safely not worry about:

- The exact details in:
  - `companions_pending/UMX_Profiles_and_Budgets_Annex_todo.md`
  - `companions_pending/PFNA_Universal_Commit_Record_Spec_todo.md`
- Distributed runtime.
- Any cloud infra.

Those will be layered on later. v1 focus is:

- Single-machine.
- Offline.
- Deterministic.
- Matches fixtures & testbed.

---

## 9. Simple “GO” checklist for UMX v1

You are done when:

- ✅ F01 is fully green: minimal topology, zero residuals/epsilon, `PASS` drift, reversible & checkpoints correct.
- ✅ F02 is green: non-zero residuals and epsilon, drift metrics and bands correct (including `INVESTIGATE`).
- ✅ F04 is green: stress & safety properties behave as specified (budgets, backpressure, dead-letter, isolation, kill-switch).
- ✅ JS shell can load S01–S04, run ticks, and export TSVs that match Golden baselines for F01/F02/F04.
- ✅ MDL plumbing is in place and ready for the MDL companion spec (even if F03 is still marked `provisional`/`provisional_mdl`).

If all of that is true, **UMX v1 is implemented according to this pack**.

### Source: `astral_press_pillar_dev_implementation_spec_v_0.md` (verbatim)

# Astral Press Pillar (Aether Press Protocol)
## Developer Implementation Spec — v0.1 (Draft)

**Pillar:** Astral Press Pillar (APP) — Aether Press Protocol  
**Role:** “Data Compression Pillar” in the Aether / Trinity stack  
**Audience:** Implementers / systems devs / architects  
**Status:** Draft spec synthesised from existing Aether Press materials. All direct facts and phrases are taken from:

- `press pillar report.pdf` (**FOCUS_REPORT.md – “Aether Press Protocol (APP) – Data Compression Pillar (Focus Report)”**)  
- `Aether_Press_Protocol_Implementation.pdf`  
- `Aether_Press_Post_Implementation_Report.pdf`  
- `Aether_Press_Protocol_Beyond_Shannon_Limit_Declaration.pdf`  
- `press v2.pdf` (Aether Report 16)  
- `press proformance.pdf` (Aether Report 19)  
- `LCDRM_White_Paper_Uroboros.pdf`

This document:
- Enumerates **all visible functions, features, and capabilities** of the Press pillar.  
- Rewrites them into a **dev-facing, implementation-ready spec**.  
- Adds **explicit math** for the formal core.  
- Flags **gaps** that would block a complete, bit‑for‑bit implementation today. These are tagged as `GAP-APP-XXX`.

Where wording is taken literally from the source, it is kept intact or near-intact (this is on purpose).

---

## 0. Pillar Positioning & Responsibilities

From the Focus Report title and abstract:

> “**FOCUS_REPORT.md**  
> Aether Press Protocol (APP) – Data Compression Pillar (Focus Report)”

> “The Aether Press Protocol is a **symbolic compression framework** that projects raw data into a **structured latent form** and **inverts it back perfectly** to the original dataset. This pillar enables **universal, lossless compression** across domains by **storing only generative rules and minimal residuals instead of entire datasets**, yielding extreme data reduction without violating deterministic fidelity.”

From the **Scope & Responsibilities** section:

> “APP’s Role: The Aether Press Protocol (APP) serves as the **Trinity system’s data compression subsystem**, responsible for **distilling large datasets or simulation outputs into concise mathematical representations**. It operates **downstream of the Trinity architecture as a post‑processing framework** that captures the **underlying structure of information**. APP’s primary responsibility is to **encode data as ‘rule + residual’ pairs and package them for storage or transmission**, guaranteeing that the original information can be **fully reconstructed when needed**. It **standardizes symbolic reduction across any domain (physics, simulation, telemetry, etc.)** and ensures compression is achieved **without introducing irreversibility unless explicitly allowed** (e.g. optional lossy modes).”

### 0.1 High‑level responsibilities (dev framing)

Implementation must support:

1. **Downstream operation**  
   - Press attaches “after” Trinity / Aether processes, taking **structured outputs** or raw files and producing **APP capsules**.

2. **Rule + residual encoding**  
   - Every compressed artefact must be representable as a **model (rules) + residual (exceptions)** pair (possibly stacked into many layers).

3. **Lossless default**  
   - Default mode: **bit‑perfect reconstruction**, with optional **ε‑bounded** modes and a **symbolic‑only** extreme.

4. **Domain‑agnostic design**  
   - Must support “ordinary binary data and structured outputs” by discovering patterns (logs, sensor streams, images, tabular data, etc.).

5. **Portable packaging**  
   - Outputs are **.apx capsules**: deterministic, self‑contained archives (manifest + layer files + metadata + integrity tags).

6. **Stacked / nested extension**  
   - Through **NAP** + **SimA/SimB**, must support multi‑layer stacking and nesting for mixed‑structure data.

7. **Integration with Trinity / Loom / NAP**  
   - Must integrate with **Aevum Loom** (replay) and **NAP** (multi‑layer compression and dimension bus) and respect Press policies from reports 16 and 19.

---

## 1. Capabilities & Behaviours (from Focus Report)

The Focus Report has an explicit **“Capabilities & Behaviours”** section. Key excerpts:

> “**Universal Model-Based Compression:** APP can **compress ordinary binary data and structured outputs** by **discovering an underlying mathematical model or pattern in the data**. It **encodes the behavior or relationships that generate the data, rather than the data itself**, making it a **domain‑agnostic compressor**. … When patterns exist, APP achieves compression far beyond traditional methods by **storing a compact generative description (the ‘rule’) plus a small residual correction**.”

> “For example, in tests it **reduced a structured CSV of 50k rows to a descriptor‑only package (no residual)** – effectively just a few KB describing the entire dataset… Similarly, a nested JSON dataset was compressed with only the generative array rules captured… For highly regular data like a checkerboard pattern, APP identified the base tiling rule and needed **zero residual**, achieving an extremely small descriptor representation.”

> “**Lossless Data Reproduction:** The protocol guarantees **bit‑perfect reconstruction** of losslessly compressed data. The ‘unpress’ operation applies the stored model and residual to **recover the exact original**, which has been verified to be **byte‑for‑byte identical** to the input… one of APP’s core capabilities is **exact round‑trip fidelity – compress data and later expand it to the exact initial state**, as formally: $Unpress(Press(data)) = data$. (APP also supports optional lossy modes or $\varepsilon$‑bounded compression… but by default its behaviour is strictly lossless.)”

> “Press capsules carry **internal integrity tags (per‑block and whole‑file hashes)** so that any corruption or mismatch is detected upon decompression.”

> “APP’s behaviour follows a defined **Rule+Residual Compression Pipeline** …” (covered in detail in §3 below).

> “APP can be extended through the **Nexus Aeternus Protocol (NAP)** to handle data with **mixed structure or partial randomness** by **layering multiple compression passes** … **APP v2 (Stacked/Nested dual‑simulation)** processes data with **two coordinated compressions (SimA and SimB) across hierarchical levels**… it stacks compression vertically (micro → meta → global layers) so that residuals from one level are further compressed by the next.”

### 1.1 Capability list (implementation targets)

From the above, Press must support at least:

1. **Model‑based compression**  
   - Discover / accept a **Domain Model** that maps data to a small set of parameters + invariants.

2. **Residual‑based error capture**  
   - Represent deviation between model output and real data as a separate **Residual** object.

3. **Exact round‑trip**  
   - Provide a deterministic `Press` / `Unpress` pair with $Unpress(Press(S)) = S$ in lossless mode.

4. **Optional ε‑bounded lossy compression**  
   - Provide modes where the residual is quantized / reduced subject to numeric bounds (see §4.2, §7.2).

5. **Stacked / nested multi‑layer compression**  
   - Implement **SimA/SimB + NAP** to separate structured vs random components and compress each hierarchically.

6. **Internal integrity tracking**  
   - Maintain per‑block + whole‑file hashes and expose verification at decode.

7. **Baseline benchmarking**  
   - Compare against “Baseline Codecs (gzip, bzip2, xz)” and others (ZIP, Zstd, FLAC, PNG per Implementation doc) as part of evaluation.

---

## 2. Formal Math Core

The **Post‑Implementation Expansion Report** and the **LCDRM white paper** define the mathematical spine of Press.

### 2.1 Core Press equations (APP / AIF)

From **Aether Press Protocol – Post‑Implementation Expansion Report**:

> “Let $S$ be a dataset represented by bits $b$. Define the model $M(\theta)$ with parameters $\theta$ such that $S \approx M(\theta) + R$, where $R$ is the residual.
>
> (1) $S = M(\theta) \oplus R$ (bitwise XOR for discrete systems)  
> (2) Compression ratio $= (|\theta| + |R|) / |S|$  
> (3) Continuity constraint → $\lim_{|R|→0} \text{Reconstruction} = S$  
> (4) Entropy $H(S) = H(M(\theta)) + H(R) − I(M(\theta); R)$  
> For perfect determinism $I = H(R)$, so $H(S) = H(M(\theta))$.”

Interpretation for implementers:

- **Data**: $S$ is the original dataset (bits or structured array).  
- **Model**: $M(\theta)$ is a family indexed by parameters $\theta$ (and invariants) chosen per segment.  
- **Residual**: $R$ is the correction term that makes the model output exactly match $S$ (lossless) or match up to tolerance (ε‑bounded).  
- **Operator**: `⊕` is **bitwise XOR** for discrete data; more generally, “combine model output and residual” (additive, XOR, or domain‑appropriate).  
- **Compression ratio** is literally “size of model parameters + size of residual” divided by “size of original”.

The continuity constraint states that as residual size tends to zero, reconstruction converges to $S$.

The same report gives the **Axioms of the Aether Information Framework (AIF)**:

> 1. “Data = manifestations of relationships.”  
> 2. “Information = minimal description of those relationships.”  
> 3. “Noise = relationships below current model resolution.”  
> 4. “Entropy = measure of unresolved relational density.”

These axioms are the conceptual basis for Press’s “rules + residuals” operation.

### 2.2 LCDRM equations (layered relational deltas)

From **Layered Compression via Deterministic Relational Mapping (LCDRM)**:

> “LCDRM is a **deterministic, scale‑invariant compression paradigm** that **encodes relationships between data elements rather than the elements themselves**. Each layer represents residual transformations between successive states of the previous layer, achieving **multi‑scale compression and self‑consistent reconstruction without entropy coding**.”

> “Let $D_0 = \{x_i\}$. Each subsequent layer:  
> $L_k = \Delta L_{k−1} = \{x^{(k)}_i − x^{(k−1)}_i \mid x^{(k−1)}_i \in L_{k−1}\}$.  
> Continuous generalization: $L_k(t) = \frac{d}{dt} L_{k−1}(t)$.  
> Compression occurs when $|L_k| < |L_{k−1}|$ until $\Delta L_k → 0$.”

> “Decompression: $L_{k−1}(i) = \sum_{k’\le k} L_{k’}(i) + C$, where $C$ is the base constant. **Guarantees identical reconstruction.**”

> “LCDRM formalizes Trinity’s relational compression method, demonstrating **minimal relational integers can encode full datasets with deterministic reconstruction**. It compresses **across scales of dependency, not merely symbol probability**.”

Press implementation can either:

- Treat LCDRM as a **core internal modelling strategy** (for SimA or residual layers), or  
- Treat it as a **related but sibling theoretical engine** that informs multi‑layer residual design.

**Implementation requirement:** Press must be able to express a dataset as **one or more LCDRM‑style relational layers** when using layered modes.

### 2.3 Two‑track Press math (P_state / P_cite, v3)

From **Aether Report 19 – press proformance.pdf**:

> “**TWO-TRACK PRESS (DO THIS EVERY TIME)**  
> 1. **P_state (reconstructive)** – the *minimal* snapshot needed for $T$ to resume exactly.  
>    • Must satisfy fidelity:  $d(O(S), O(\mathrm{DePr}(\mathrm{Pr}(S))) ) \le \varepsilon$.  
>    • Lossless for critical classes (e.g., $O.\text{struct}$, $O.\text{event}$ = 0‑tolerance).  
> 2. **P_cite (documentary)** – hashed pointers to big originals (docs, PDFs, logs, media).  
>    • Store **content‑hash, byte length, and a few extracted integers you actually use**.  
>    • You don’t carry the whole file inside the checkpoint unless it’s required for $T$.”

> “Result: you keep **exactly what the computational episode needs**, and only **proofs/pointers** for everything else. That’s where the astronomical gains come from.”

And the **Crush without regret checks**:

> 1. “**Field‑level bounds:** For every numeric field $x$ you store after quantization $q$:  
>    $$|x_{\text{post}} − x_{\text{pre}}| \le q/2 \le \varepsilon_x.$$  
> 2. **Replay test:** DePress then run $\Delta = 0$: $O$ unchanged (fidelity at snapshot).  
> 3. **Predictive test:** DePress and run $T^\Delta$; check $d(O_{\text{true}}, O_{\text{replayed}}) \le \varepsilon$.  
> 4. **Document proof:** Keep $\{\text{hash}, \text{bytes}\}$ for each external source in **P_cite** so an auditor can verify you didn’t hallucinate inputs.  
> 5. **Idempotence:** Same envelope + same nonce → no net change to $O$.  
> 6. **Isolation:** Prior checkpoint O‑hashes never change.”

Implementation requirement: Press **must** be able to:

- Maintain **P_state** (replayable internal state snapshot) and **P_cite** (external ref metadata) as distinct artefacts.  
- Enforce **field‑level quantization bounds** and support **replay / predictive tests** as part of acceptance.


---

## 3. Components & Subsystems (from Focus + Implementation)

### 3.1 Named / stated / implied components (Focus Report)

From the **“Components (Named/Stated/Implied)”** section of `press pillar report.pdf`:

> “**Aether Press Protocol (APP)** – *Named:* A **symbolic compression framework** defining the rules for **model‑based data reduction**. It compresses by **capturing relationships instead of raw bits**.”

> “**Residual Encoding** – *Stated:* The step storing only **minimal differences** between a model’s output and the real data. **Residuals represent information not explained by the generative model.**”

> “**Packaging Stage** – *Named:* A phase that wraps the **model ID, parameters, and residuals** into a portable container. Ensures **all pieces needed for reconstruction are kept together**.”

> “**APX Capsule Format** – *Named:* A portable `.apx` container for Aether Press outputs. It is a **deterministic, self‑contained ZIP archive (manifest + layer files)** used to store compressed data and metadata.”

> “**SimA (Symbolic Compressor)** – *Named:* In advanced Press usage, a **generative compression stream** that **models structured patterns (stacked/nested rules)** and **records only math needed to reconstruct data**.”

> “**SimB (Residual Compressor)** – *Named:* A complementary **residual stream capturing any data SimA cannot express, layer by layer**. Together with SimA, it **splits deterministic structure from randomness**.”

> “**NAP Compression Manifest** – *Named:* A Nexus Aeternus Protocol (NAP) manifest that **‘knits’ together SimA and SimB outputs**. Defines how **multi‑layer stacks and nests recombine for exact reconstruction**.”

> “**Baseline Codecs (gzip, bzip2, xz)** – *Named (contextual):* Standard compression tools used as **baseline benchmarks** for Press experiments.”

> “**Press Metadata Manifest** – *Stated:* The `.apxMANIFEST.json` file storing original file metadata: **name, size, hash, compression mode, timestamp, etc.** Extended in later versions to include **file system info (permissions, timestamps)** for archival completeness.”

> “**HMAC Signature (APX)** – *Implied:* Cryptographic signing of capsules to ensure **authenticity and tamper‑detection**. Allows verification that an `.apx` capsule was created by the authorized system and not modified.”

**Implementation mapping:**

- `APP core` → top‑level orchestrator of all sub‑steps.  
- `Residual Encoding` → a dedicated module that takes model output + data, computes residuals, and encodes them.  
- `Packaging` → APX container builder.  
- `APX Capsule` → on‑disk/on‑wire representation.  
- `SimA/SimB` → advanced encoder mode using two coupled streams.  
- `NAP manifest` → structural description of how layers recombine.  
- `Press Metadata Manifest` → JSON metadata inside `.apx`.  
- `HMAC Signature` → optional cryptographic extension for secure deployments.

### 3.2 Encoder / Decoder stages (Implementation doc)

From **Aether_Press_Protocol_Implementation.pdf**:

> “3. **Architecture Overview**  
> **Encoder**  
> 1. **Domain Model** – Defines the governing physics or statistical law.  
> 2. **Parameter Fitting** – Extracts parameters and invariants from data.  
> 3. **Residual Encoding** – Stores minimal differences between the model and data.  
> 4. **Packaging** – Combines model ID, parameters, invariants, and residuals into a standardized container.  
> **Decoder**  
> 1. Load model and metadata.  
> 2. Regenerate the base signal deterministically.  
> 3. Add residuals for full reconstruction.  
> 4. Validate checksum and fidelity.”

This is the **minimal encoder/decoder behaviour** that every implementation must honour.

### 3.3 Compression modes

From the Implementation doc:

> “4. **Compression Modes**  
> – **Lossless** – Full reconstruction, residuals preserved exactly.  
> – **Quasi‑Lossless** – Bounded error within ε‑tolerance.  
> – **Symbolic‑Only** – Stores only rules and invariants; maximum compression.”

**Implementation requirements:**

- **Lossless mode:** $R$ is stored exactly; $Unpress(Press(S)) = S$; matching hash (e.g., SHA‑256) must be possible.  
- **Quasi‑Lossless mode:** $R$ is quantized or otherwise reduced such that field‑level bounds and global acceptance conditions hold (see §2.3).  
- **Symbolic‑Only mode:** `R = 0` or omitted; Press stores only $M(\theta)$ + invariants; decompression reproduces a **model‑generated surrogate** rather than the original raw data. (Useful when only structure matters.)

### 3.4 Container format (APP container)

From Implementation doc, **“7. APP Container Format”**:

> “Header  
> – Model ID, version, and compression mode.  
> – Metadata: dtype, shape, fidelity metric.  
> Body  
> – Model parameters (quantized or raw).  
> – Invariant dictionary.  
> – Residual byte stream.  
> – Metrics and checksum.”

From the Focus Report plus this section:

- The **APP container** corresponds to the `.apx` capsule with:  
  - **Header**: identifies model, version, compression mode, and describes the shape and dtype of the underlying data, plus expected fidelity metrics.  
  - **Body**: carries the *model parameters*, *invariants*, *residual stream*, plus *metrics* (compression ratio, error metrics) and *checksums* (segment and/or whole‑file).  
  - **Metadata manifest**: `.apxMANIFEST.json` with original file name, size, hash, mode, timestamps, etc., and optionally filesystem details.

### 3.5 Subsystems (internal division of labour)

From Implementation doc, **“8. Subsystems”**:

> `| Subsystem | Role |`  
> `| Aether Core | symbolic modeling and invariant extraction |`  
> `| Press Engine | encoding of parameters and residuals |`  
> `| Flux Decoder | reconstruction and fidelity validation |`  
> `| Protocol Layer | serialization schema and metadata registry |`

Implementation should mirror this separation:

1. **Aether Core**  
   - Provides domain models, invariant discovery, and simulation capabilities.  
   - Decides model families (Fourier, polynomial, Markov, LCDRM, etc.).

2. **Press Engine**  
   - Implements the compression pipeline: model fitting, residual computation, residual encoding, container assembly.  
   - Houses `Press` and `Unpress` algorithms and their advanced variants (SimA/SimB, stacking).

3. **Flux Decoder**  
   - Handles decoding of APP capsules; reconstructs base signals; applies residuals; validates checksums and fidelity metrics.

4. **Protocol Layer**  
   - Defines `.apx` structure; manages manifests; integrates HMAC and signatures where used; registers codec versions.


---

## 4. Core Logical Interfaces (Math‑level)

Below is a **language‑agnostic**, **math‑level interface** description. This is not code; it’s a description of functions the implementation is expected to realise.

### 4.1 Basic pair: Press and Unpress

#### 4.1.1 Press

Conceptual signature:

- **Input:**  
  - Dataset $S$ (bytes or structured array)  
  - Compression mode $m \in \{\text{lossless}, \text{quasi‑lossless}, \text{symbolic‑only}\}$  
  - Optional config (model family hints, target ε per field, quantization policy, stack depth, etc.)

- **Output:**  
  - APP capsule $C$ (an `.apx` container) containing header + body + manifest + (optionally) HMAC.

- **Guarantees (lossless mode):**  
  - There exists a corresponding `Unpress` such that $Unpress(C) = S$ and hash($S$) = hash($Unpress(C)$).

- **Guarantees (quasi‑lossless mode):**  
  - For each numeric field $x$: $|x_{\text{post}} − x_{\text{pre}}| \le q/2 \le \varepsilon_x$.  
  - System‑level outputs $O$ obey: $d(O(S), O(Unpress(C))) \le \varepsilon$ as per §2.3.

- **Guarantees (symbolic‑only mode):**  
  - Decompression yields $\hat{S} = M(\theta)$, where $
\hat{S}$ is a model‑generated surrogate consistent with stored invariants.

#### 4.1.2 Unpress

Conceptual signature:

- **Input:** APP capsule $C$ (.apx)  
- **Output:** Reconstructed dataset $\hat{S}$ and verification report.

Steps (from Implementation doc’s Decoder):

1. Load model and metadata from header + manifest.  
2. Regenerate base signal deterministically using $M(\theta)$ and invariants.  
3. Apply residuals $R$ (if present) to recover $\hat{S}$.  
4. Validate checksums and fidelity metrics (hash match in lossless mode, bounds in ε‑bounded).  
5. Return $(\hat{S}, \text{fidelity_report})$.


### 4.2 Domain Model selection and fitting

These functions implement the **Rule+Residual Compression Pipeline** described in the Focus Report:

> “First, a **Domain Model** is chosen or inferred – essentially the form of the mathematical law or pattern expected (for example, a Fourier series, polynomial fit, Markov process, etc.). Next, **Parameter Fitting** occurs, where the model’s parameters and any invariants are tuned to the specific dataset. Then comes **Residual Encoding**, which records the delta between the model’s output and the actual data… Finally, the **Packaging** stage wraps the model identifier, the fitted parameters, and the encoded residual into a portable file container.”

Required logical pieces:

1. **DomainModelSelect**  
   - Input: segment $S_i$, metadata (dtype, shape, domain hints).  
   - Output: selected model family $M \in \mathcal{M}$ (e.g., Fourier, polynomial, autoregressive, LCDRM, etc.).  
   - Behaviour: may use heuristics or configuration to pick the best candidate.

2. **ParamFit / InvariantExtract**  
   - Input: chosen model family $M$, segment $S_i$.  
   - Output: $\theta_i$ (parameters), $I_i$ (invariants).  
   - Behaviour: run optimisation / fitting processes (least squares, maximum likelihood, dynamic programming, etc.) appropriate for $M$.

3. **ModelSimulate**  
   - Input: $M, \theta_i, I_i, \text{len}(S_i)$.  
   - Output: synthetic segment $\tilde{S}_i = M(\theta_i, I_i)$.

4. **ResidualCompute**  
   - Input: original $S_i$, synthetic $\tilde{S}_i$.  
   - Output: residual $R_i$ (difference or XOR depending on dtype).  
   - Behaviour: $R_i = S_i − \tilde{S}_i$ (numeric) or $R_i = S_i \oplus \tilde{S}_i$ (bitwise).

5. **ResidualEncode**  
   - Input: residual $R_i$, mode $m$.  
   - Output: encoded residual bytes $\mathcal{R}_i$.  
   - Behaviour:  
     - Lossless: apply a **lossless encoder** to $R_i$ (e.g., general‑purpose or custom entropy coder).  
     - Quasi‑lossless: apply quantization then entropy encoding, respecting per‑field $\varepsilon_x$ (see §7).

6. **PacketAssemble**  
   - Input: $\text{model\_id}$, $\theta_i$, $I_i$, $\mathcal{R}_i$, metadata (eps, checksums).  
   - Output: segment packet for container body.

**GAP‑APP‑001 (Model library & selection):**  
The docs list **example model families** (“Fourier series, polynomial fit, Markov process, etc.”) but do not define a concrete, finite set $\mathcal{M}$ or the exact selection heuristic. A full implementation must **choose and standardise**:

- Which models are supported (e.g., {Fourier, polynomial, ARMA, LFSR, LCDRM, piecewise‑linear, …}).  
- How they are parameterised (exact meaning and encoding of $\theta$ per family).  
- How the encoder decides between them (fixed config, heuristics, training, or external hinting via Trinity).

### 4.3 APX container handling

Logical functions:

1. **CapsuleBuildHeader**  
   - Fills: model ID, version, compression mode, dtype, shape, declared fidelity metric(s).  

2. **CapsuleBuildManifest**  
   - Creates `.apxMANIFEST.json` with original file metadata (name, size, hash, mode, timestamps, filesystem bits).  

3. **CapsuleEncodeBody**  
   - Serialises model parameters, invariant dict, residual stream, metrics, checksums into canonical layout.

4. **CapsuleSign (optional)**  
   - Computes HMAC / signature over container; stores signature + algorithm ID.

5. **CapsuleVerify**  
   - On decode, verifies integrity tags and signature (if present) and returns an acceptance report.

**GAP‑APP‑002 (Exact .apx schema & signature details):**  
The reports specify **what** must be stored but not the exact **binary layout, field ordering, or signature algorithm**. An implementation must define:

- Canonical byte layout of header, manifest reference, and body segments.  
- JSON schema for `.apxMANIFEST.json`.  
- Hash function(s) for content hashes (SHA‑256 is implied in experiments but not explicitly locked).  
- HMAC / signature algorithms, key management, and how signatures are bound to capsule content.


---

## 5. Advanced Press: Stacked / Nested (SimA / SimB / NAP)

From the Focus Report and APP v2 description:

> “In advanced Press usage, **SimA (Symbolic Compressor)** is a generative compression stream that **models structured patterns (stacked/nested rules)** and records only math needed to reconstruct data. **SimB (Residual Compressor)** is a complementary residual stream capturing any data SimA cannot express, layer by layer. Together they split deterministic structure from randomness.”

> “APP can be extended through the **Nexus Aeternus Protocol (NAP)**… This was demonstrated as **APP v2 (Stacked/Nested dual‑simulation)**, where the data is processed by **two coordinated compressions (SimA and SimB) across hierarchical levels**. In this mode, APP becomes **adaptive**: it **stacks compression vertically (micro → meta → global layers)** so that residuals from one level are further compressed by the next.”

From **v2 report (Aether Report 16)** we also see per‑dimension Press controls (see §6).

### 5.1 SimA / SimB logical roles

- **SimA (Symbolic stream):**  
  - Main job: discover *structured*, *law‑like* patterns and encode them as generative rules.  
  - Output: a stack of model descriptions across scales (micro/meta/global).

- **SimB (Residual stream):**  
  - Main job: capture **leftovers** from SimA – anything not captured by rules.  
  - Output: residual layers, each possibly further compressed via LCDRM or other residual models.

- **NAP Compression Manifest:**  
  - A structural descriptor telling the decoder **how to recombine** SimA and SimB outputs across layers to get $S$ back.

### 5.2 Stacked / nested pipeline

Conceptual flow for a multi‑layer Press run:

1. **Layer 0 (micro):**  
   - Run SimA on small chunks (local structure).  
   - Compute residuals; feed them into SimB for additional compression.  

2. **Layer 1 (meta):**  
   - Observe patterns **across** micro‑layer outputs (e.g., repeating structures across chunks).  
   - Apply further modelling (SimA₁) and residual handling (SimB₁).

3. **Layer 2+ (global):**  
   - Repeat as needed until residuals are no longer compressible (LCDRM’s $|L_k| < |L_{k−1}|$ condition fails).

4. **NAP manifest construction:**  
   - For each layer $k$, record:  
     - which datasets it acts on (SimA vs SimB from previous layer),  
     - how outputs cascade,  
     - how to invert the sequence at decode time.

5. **Decoding:**  
   - Work from highest layer down, reconstructing SimA/SimB outputs in the correct order, guided by the NAP manifest, until you recover $S$.

**GAP‑APP‑003 (NAP manifest concrete schema):**  
The NAP manifest is conceptually described but lacks a fixed schema. Implementation must decide:

- How layers are indexed and ordered.  
- How SimA vs SimB data streams are referenced (IDs, offsets).  
- How to represent dependencies (graph vs strict stack).  
- How this manifest is stored inside `.apx` (embedded JSON vs sidecar).


---

## 6. Dimension‑Level Press Controls (Report 16 — v2)

From **Aether Report 16 – press v2.pdf**:

> “Dims Press per‑entry” (table showing `raw_bytes`, `lores_bytes`, `press_bytes` for `NAP_bus`).

> Bullet list:
>
> • “**Exact vs ‑quantized dims:** choose which dims must match exactly for replay vs which can be bucketed (e.g., [values] to nearest $1e−3$, positions to 1 unit).”  
> • “**Residual fraction:** tighten or loosen Loom’s residual size (e.g., 5–20%) for layers where you need more/less detail.”  
> • “**Selective retention:** mark dims as {**recompute**, **residual**, **full**}:  
>   – _recompute_: derive from other fields on replay (kept out of residual),  
>   – _residual_: store compact delta,  
>   – _full_: store verbatim (e.g., provenance‑critical tags).  
> • **Dict scopes:** keep **per‑node dictionaries** or a **global Press dict** on the NAP bus for cross‑layer dimensional schemas.”

> **BOTTOM LINE:**  
> “New dims can appear mid‑run (we proved it) and get **Loomed (for deterministic replay)** and **Pressed (for compact, reversible storage)** like any other data. You can dial **how faithful** they must be for reuse and **how much detail** to keep in residuals on a **per‑dimension, per‑layer** basis.”

### 6.1 Dim‑level policy model

Each **dimension** (field) on the NAP bus must have a **Press policy** with:

- **Retention mode:** `recompute | residual | full`  
- **Quantization q:** 0 for exact, non‑zero for bucketed values (numeric fields).  
- **Residual fraction:** how much of Loom’s residual budget is allowed for that dimension on a given layer.  
- **Dictionary scope:** local per‑node vs shared global dictionary.

Implementation must:

1. Allow new dimensions to appear at runtime and be assigned policies.  
2. Apply those policies when building P_state and Press residuals.  
3. Honour recompute/full semantics at replay (`recompute` dims derive from other fields; `full` dims are stored verbatim even if compressible).

**GAP‑APP‑004 (Exact residual fraction semantics):**  
Report 16 gives the idea (“residual fraction 5–20%”) but not the exact algorithm for enforcing a per‑dim residual budget. Implementation must choose:

- Whether residual fraction is per‑layer or global.  
- Whether it is enforced in bytes, entropy, or some other metric.  
- What happens when a dim’s residual attempt would exceed its budget (truncate, re‑quantize, or fail?).


---

## 7. Two‑Track Press Policies (Report 19 — P_state / P_cite)

From **Aether Report 19 – press proformance.pdf** (already partly quoted):

> “Press can crush traditional sources by absurd factors… The key is to separate what must be *reconstructible* for the math from everything else.”

> “**TWO-TRACK PRESS (DO THIS EVERY TIME)**” (P_state/P_cite as quoted in §2.3).

It also defines a **Press policy card**:

> “**PRESS POLICY  <source_name>**  
> Type: (text/pdf/image/log/table/sensor)  
> Track: [P_state | P_cite] (pick one; sometimes both)  
> O‑fields derived: { … } (list only what T or O needs)  
> Quantization q per field: {f1:q1, f2:q2, …}  
> Epsilon per field: {f1:ε1, f2:ε2, …} (ensure q/2 ≤ ε)  
> Content‑hash (if P_cite): sha256=<…>, bytes=<…>  
> Seeds/Units: seed=<…>, units=<…>  
> Nonce: <…>  
> Acceptance: snapshot fidelity, predictive, idempotence, isolation, audit.”

And the **“What to avoid”** section:

> “**What to _avoid_ (this is where people get burned)**  
> – **Letting P_state depend on raw docs** you won’t replay. If $T$ doesn’t need the raw, don’t pack it – hash it in **P_cite** instead.  
> – **Quantizing before you set $\varepsilon$.** Always lock $\varepsilon$ first; choose $q$ to fit inside it.  
> – **Comparing anything other than $O$** in acceptance. The whole point is: if $O$ matches under the contracts, you’re good.”

### 7.1 P_state / P_cite implementation requirements

Implementation must:

1. Support **per‑source Press policy cards** capturing the above fields.  
2. Implement **P_state** as the minimum Press snapshot needed for $T$’s deterministic replay (plus Loom state).  
3. Implement **P_cite** as a separate reference structure containing:  
   - Content hashes (e.g., SHA‑256) and byte lengths for original sources.  
   - Minimal extracted integers (e.g., counts, key metrics) used in computation.  
4. Enforce **field‑level quantization bounds** $|x_{post} − x_{pre}| \le q/2 \le \varepsilon_x$.  
5. Provide **replay** and **predictive** tests and an **idempotence** and **isolation** check.

**GAP‑APP‑005 (Exact distance metrics and O‑space definition):**  
The reports refer to $d(O_{true}, O_{replayed})$ but do not fix the metric $d$ or the exact definition of $O$. Implementation must specify:

- What constitutes $O$ for a given application (observables, derived statistics, etc.).  
- Which metric $d$ is used (L2, L∞, domain‑specific) and how ε is chosen and stored.  
- How acceptance thresholds are set and enforced automatically.


---

## 8. Testbed & Metrics (Press Pareto Manifests)

From the **Aether Synthetic Testbed v5/v6** manifests (`press_pareto_manifest_*.json`):

Example (`press_pareto_manifest_image.json`):

```json
{
  "component": "Aether Press",
  "content_type": "image",
  "objective": "minimize {mse, compression_ratio}",
  "front": [
    {"bits": 8, "codec": "zlib", "mse": 0.0,   "comp_ratio": 0.012080078125, ...},
    {"bits": 7, "codec": "zlib", "mse": 0.5,   "comp_ratio": 0.008740234375, ...},
    ...
  ],
  "recommendation_hint": "Pick a point and freeze as barrier: (max_MSE, min_ratio, codec, bits)."
}
```

Key points:

- **Objective:** “minimize {mse, compression_ratio}”.  
- **Front:** a list of Pareto‑optimal points with fields such as `bits`, `codec`, `mse`, `comp_ratio`, `compressed_bytes`, `input_bytes`.  
- **Recommendation:** “Pick a point and freeze as barrier: (max_MSE, min_ratio, codec, bits).”

Implementation implications:

1. Press must be able to **emit metrics** needed for these fronts: MSE, compression ratio, etc.  
2. At runtime or config time, you can choose a **Pareto point** and turn it into a **Press barrier** (max acceptable MSE, minimum acceptable compression ratio, chosen codec and bit‑depth).  
3. Press should then **self‑check** each run against these barriers and either pass / fail or adapt (e.g., choose different settings) accordingly.

**GAP‑APP‑006 (Runtime barrier enforcement semantics):**  
The testbed tells you **what to pick** but not exactly **how the runtime should behave** when a barrier is violated. Implementation must decide whether to:

- Fail the run (hard error).  
- Fall back to a safer configuration (e.g., more bits, different codec).  
- Emit warning and keep going.


---

## 9. Error / Fidelity Guarantees (Implementation doc)

From Implementation doc, **“9. Error and Fidelity Guarantees”**:

> “– **Timeseries:** MAE ≤ ε, spectral error ≤ δ.  
> – **Images/Fields:** PSNR ≥ threshold or SSIM ≥ bound.  
> – **Dynamics:** State fidelity ≥ F, invariants deviation ≤ Δ.”

Combined with §2.3, implementation must:

- Expose configurable **fidelity metrics** per content type (timeseries, images, dynamical systems).  
- Track those metrics for each Press run and store them in the APP container body (“Metrics and checksum”).  
- Provide an API to **assert** that these metrics are inside the configured bounds.

**GAP‑APP‑007 (Exact default thresholds):**  
The docs define *types* of metrics but not the default values for ε, δ, PSNR thresholds, SSIM bounds, F, or Δ. Implementation must:

- Either define authoritative defaults, or  
- Require explicit configuration per deployment.


---

## 10. Summary of Capabilities (Checklist)

From all the above, Press Pillar must be capable of:

1. **Lossless compression with exact round‑trip** (`Unpress(Press(S)) = S`).  
2. **Quasi‑lossless compression** with ε‑bounded errors at field‑level and system‑output level.  
3. **Symbolic‑only compression** (store only rules/invariants, no residual).  
4. **Rule+Residual pipeline**: Domain Model selection, parameter fitting, invariant extraction, model simulation, residual computation, residual encoding, packaging.  
5. **Layered compression** via LCDRM‑style deltas and SimA/SimB stacked/nested architecture.  
6. **Dimension‑level control**: recompute/residual/full, quantization, residual fractions, dictionary scopes.  
7. **Two‑track Press** (P_state/P_cite) with policy cards, hash‑based proofs, and acceptance gates (field‑level, replay, predictive, idempotence, isolation).  
8. **APX containerization** with header, manifest, body, integrity tags, optional HMAC signatures.  
9. **Metric reporting** for compression ratio, MSE, PSNR/SSIM, state fidelity, invariant deviation.  
10. **Baseline benchmarking** vs established codecs (gzip/bzip2/xz/ZIP/Zstd/FLAC/PNG).  
11. **Support for evolving schemas** (new dimensions mid‑run) in combination with Loom and NAP.


---

## 11. Gaps Blocking a Fully Deterministic Reference Implementation

The key **blocking unknowns** that must be resolved to implement a production‑grade, deterministic Press pillar:

### GAP‑APP‑001 — Model library and selection

- No canonical set of model families $\mathcal{M}$ is specified.  
- No fixed parameterization scheme for each model is defined.  
- No exact selection heuristic is given for picking a model per segment.

**Consequence:** Implementers must design and standardise a **model library**, parameter encoding, and selection algorithm.

### GAP‑APP‑002 — Exact .apx binary schema & signature details

- `.apx` is specified only conceptually (“deterministic, self‑contained ZIP archive”).  
- Manifest fields are named, but no JSON schema is fixed.  
- Hash algorithm (e.g., SHA‑256) and HMAC / signature algorithms are not set in stone.  
- No canonical ordering / byte packing is defined.

**Consequence:** A reference wire format must be defined to ensure interop between implementations.

### GAP‑APP‑003 — NAP Compression Manifest schema

- The NAP manifest is described qualitatively (“knits together SimA and SimB outputs”) but has no structural spec.  
- No explicit graph / stack model is defined for layered compression.

**Consequence:** Implementers must define a manifest structure that can encode the dependency graph of layers and streams.

### GAP‑APP‑004 — Residual fraction semantics (per‑dim residual budgets)

- Report 16 introduces residual fractions (e.g., 5–20%) but not how they map to bytes or entropy.  
- No formal rule is given for what happens when residual demand exceeds budget.

**Consequence:** Must design an enforcement strategy for residual budgets (e.g., re‑quantization, dropping, or errors).

### GAP‑APP‑005 — Output space and distance metric for acceptance

- $O$ (observable outputs) and $d(\cdot,\cdot)$ (distance) are left generic.  
- No default or recommended metrics are locked in per domain.

**Consequence:** For any concrete deployment, implementers must specify:  
- what $O$ is (e.g., full trajectories vs summary stats),  
- what $d$ is (e.g., L2, max error, domain‑specific metrics),  
- what ε values are acceptable.

### GAP‑APP‑006 — Runtime barrier enforcement semantics

- Pareto manifests suggest freezing points as barriers but not runtime behaviour when barriers are violated.  
- Interaction between Press barriers and Loom / Trinity schedulers is not fully specified.

**Consequence:** Need a policy: fail, fallback, or degrade gracefully (and how to surface that to the rest of the system).

### GAP‑APP‑007 — Default fidelity thresholds

- Types of metrics are defined (MAE, spectral error, PSNR, SSIM, state fidelity, invariant deviation), but default thresholds are not.

**Consequence:** Implementers must either define standard default profiles (e.g., “archival”, “analysis‑only”, “preview”) or require explicit configuration.

### GAP‑APP‑008 — Streaming vs batch semantics

- Implementation pseudocode hints at segment/window‑based processing, but streaming behaviour (online compression, partial flushes) is not fully specified.  
- No explicit rules for how partial `.apx` capsules behave mid‑stream.

**Consequence:** For streaming use‑cases, Press needs a clearly defined protocol for partial packets, resumption, and error recovery.

### GAP‑APP‑009 — Exact role of LCDRM inside APP

- LCDRM is clearly related and describes layered relational compression, but Press docs do not **mandate** whether LCDRM is:  
  - the default engine for SimA/SimB layers, or  
  - a theoretical sibling used only in some builds.

**Consequence:** Reference implementation must decide whether LCDRM is core to Press or optional.


---

## 12. Next Steps for a Reference Implementation

Given the current docs, a realistic path to a full implementation is:

1. **Lock the model library (resolve GAP‑APP‑001)**  
   - Choose a minimal but expressive set of models (e.g., LFSR‑style integer models for structured bitstreams, polynomial/time‑series models, simple Markov models, LCDRM layers).  
   - Define parameter encodings for each.

2. **Specify the .apx format (resolve GAP‑APP‑002 & GAP‑APP‑003)**  
   - Draft a strict binary + JSON schema for APP capsules and NAP manifests.  
   - Include hash and signature algorithms and compatibility versioning.

3. **Codify Press policies (resolve GAP‑APP‑004/005/006/007)**  
   - Turn Report 16 and 19 guidance into machine‑checkable policies and defaults.  
   - Provide a library or table of common policy cards.

4. **Implement encoder/decoder with metrics**  
   - Build against the architecture described in §3 (Aether Core, Press Engine, Flux Decoder, Protocol Layer).  
   - Ensure metrics, fidelity checks, and barrier checks are all first‑class.

5. **Integrate with Loom and NAP**  
   - Honour dimension‑level Press config, residual fractions, and dynamic schema evolution.  
   - Verify replay correctness under stacked/nested modes.

6. **Benchmark vs baselines**  
   - Follow Implementation doc guidance to compare against ZIP, Zstd, FLAC, PNG, gzip/bzip2/xz, and validate the promised “far beyond traditional methods” behaviour on structured data.

This spec should be treated as **v0.1** of the dev‑facing Aether Press implementation sheet. Once the above GAPs are concretely resolved in code/math, a v1.0 spec can hard‑lock formats and algorithms.

### Source: `umx_spec_master_index_readme_2025_11_16.md` (verbatim)

---
id: umx_spec_master_index_v1
version: 1.0-draft
status: normative-shell
pillar: UMX
created: 2025-11-16
---

# Universal Matrix (UMX) — Spec Master Index & README (v1)

## 0. Purpose and Audience

This document is the **top-level index and README** for the Universal Matrix (UMX) pillar.

It is intended for:

- **Spec authors and system designers** — to see the complete UMX spec surface and document set.
- **Implementers (devs)** — to know which documents are normative for behaviour and which are build guides.
- **Test and verification engineers** — to locate all properties, fixtures and test plans that involve UMX.
- **Operators** — to find the runbook and understand what UMX exposes to the Aether Testbed.

This README does **not** re-specify all behaviours. Instead, it:

- Defines the **canonical document set** for UMX v1.
- Groups documents into **families** (core semantics, stress and emergence, integration contracts, TBP pack).
- Describes **dependencies and read order**.
- Defines a **packaging layout** for handoff as a single ZIP.

Where there is any conflict between this README and a more specific normative artefact, **the specific artefact wins**.

---

## 1. UMX Pillar Snapshot

UMX is the **Universal Matrix pillar** in the Aether / Trinity architecture. At a high level it:

- Maintains a **graph-structured substrate** of nodes and edges over one or more layers.
- Applies **deterministic update rules** over a global tick and optional sub-ticks.
- Integrates with **SLP** (Synaptic Ley Protocol) to consume ley-state snapshots each tick.
- Integrates with **Loom / U-Ledger** to record snapshots, commits and replayable history.
- Integrates with **NAP** (bus) to receive and emit envelopes under strict idempotence and ordering rules.
- Supports **learning and adaptation** driven by a global MDL objective.
- Exposes **residuals, epsilon-layers, drift metrics and emergence bands** as simple numerics to the Aether Paper Testbed.

UMX is designed to be:

- **Paper-first** — all critical behaviour is defined as math on tables and can be executed by hand or spreadsheet.
- **Deterministic** — the same inputs and profile always yield the same outputs.
- **Testbed-native** — every important property is checked via the Aether Testbed MASTER and MAX suites.

This README assumes that conceptual foundations from the following ancestor documents are already understood:

- `universal_matrix_pillar_spec_v_1.md` — original conceptual UMX spec.
- `Universal Matrix Pillar — Topology Substrate & Conservation Engine` (PDF) — topology and conservation framing.
- UMX Complement Docs A–H and `umx_complement_doc_i_gap_closure_profile_specs.md` — gap families and closure notes.

The artefacts indexed here **refine and crystallise** that material into a build-ready pack.

---

## 2. Document Families (Overview)

The UMX v1 document set is organised into four main families:

1. **Core Semantics & Profiles** — foundational behaviour, maths and configuration.
2. **Stress, Epsilon & Emergence** — how UMX behaves under load and how drift is measured and bounded.
3. **Integration & Contracts** — precise wiring to SLP, Loom, NAP and U-Ledger.
4. **TBP Build & Operations Pack** — implementation spec, roadmap, verification and operator guidance.

Each family is described in detail below with a mini-index of its artefacts.

---

## 3. Family I — Core Semantics & Profiles

These documents define the **core behaviour and configuration** of UMX. They are the primary normative references for how UMX thinks and moves.

### 3.1 Artefact List

1. **`umx_mdl_objective_v1.md`**  
   - Defines the Minimum Description Length (MDL) objective used to decide when to accept structural and SLP changes.  
   - Specifies traces, canonical encodings, the codelength functional \(\mathcal{L}\), the baseline codelength \(L_0\), the candidate codelength \(L_1\), the gain \(\Delta L\) and the acceptance rule \(\Delta L \le -\tau\).  
   - Connects directly to Aether Testbed fields like `delta_mdl` and `accepted`.

2. **`umx_layers_policy_v1.md`**  
   - Defines the semantics of `layerId`, the shared coordinate frame and allowed connectivity between layers.  
   - Introduces layer cadences \(k_\ell\) measured in base-layer ticks with \(k_0 = 1\).  
   - Specifies that v1 reference profiles are single-layer but structures must remain layer-aware.

3. **`anchor_map_v1.md`**  
   - Defines base anchors `(node_id, layer=0, tick_ref, coord)` and residual or epsilon anchors that attach to these base anchors.  
   - Enforces a one-to-one mapping from residual or epsilon entries to base anchors for v1.  
   - Guarantees that reconstruction from time ledger plus residuals is unambiguous.

4. **`subtick_semantics_v1.md`**  
   - Defines a macro tick as an input window in the I/P-block time ledger.  
   - Defines sub-ticks as ordered partitions of that window.  
   - Requires that a single macro-step over the full window be equivalent (up to explicit epsilon corrections) to a sequence of sub-steps over the partitions.

5. **`umx_profile_v1.md`**  
   - Defines the structure and semantics of UMX profiles: `tick`, `mdl`, `residual`, `nap`, `ledger`, `layers`, `emergence` and `calibration` sections.  
   - Specifies how profiles control MDL thresholds, residual bounds, budgets, ledger retention, layer cadences and drift tolerances.  
   - Introduces profile status (GO / HOLD / KILL) and coverage manifest fields linking profiles to testbed scenarios.

### 3.2 Recommended Read Order

For someone learning UMX from zero:

1. `umx_profile_v1.md` — to see the knobs and what a profile looks like.  
2. `umx_layers_policy_v1.md` — to understand the spatial and layering assumptions.  
3. `anchor_map_v1.md` — to see how state and corrections are anchored.  
4. `subtick_semantics_v1.md` — to understand time semantics.  
5. `umx_mdl_objective_v1.md` — to understand how learning and structural decisions are made.

---

## 4. Family II — Stress, Epsilon & Emergence

These documents define how UMX handles **residuals, epsilon corrections, drift, emergence bands, stress and safety**.

### 4.1 Artefact List

1. **`umx_epsilon_layers_and_drift_metrics_v1.md`**  
   - Defines epsilon layers as sparse correction records anchored to base anchors.  
   - Defines per-node drift \(\Delta_i(W)\) and global drift \(\Delta(W)\) over a window \(W\), using residual norms and epsilon corrections.  
   - Specifies how drift metrics and epsilon usage are represented in ledger and testbed tables, enabling `drift_guard_ok`, `orthogonal_residuals_ok` and `entropy_bound_ok` evaluations.

2. **`umx_emergence_bands_v1.md`**  
   - Defines emergence bands PASS, INVESTIGATE and FAIL via inequalities on \(\Delta\) and ε: PASS (\(\Delta = 0\)), INVESTIGATE (\(0 < \Delta \le \epsilon_\text{drift}\)), FAIL (\(\Delta > \epsilon_\text{drift}\)).  
   - Defines QUARANTINE as a scenario or region state indicating expected deviations.  
   - Specifies how bands and quarantine flags are expressed in testbed assertion columns, and how they feed into GO/NO-GO outcomes.

3. **`umx_stress_test_matrix_v1.md`**  
   - Defines the UMX stress and overload test matrix: high-load routing scenarios, backpressure scenarios, dead-letter scenarios and isolation scenarios.  
   - Specifies what UMX must expose (message counts, dead-letter queues, region tags, backpressure signals) to support `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty` and `isolation_ok` properties.

4. **`umx_kill_switch_and_quarantine_v1.md`**  
   - Defines kill-switch activation modes (manual, testbed-driven, automatic), scope (NODE, REGION, SYSTEM) and effects (stop accepting new envelopes, freeze or cancel learning proposals, maintain ledger consistency).  
   - Defines scenario-level and region-level quarantine semantics and how they interact with kill-switch behaviour.  
   - Specifies representation of kill events and quarantine flags in events tables and assertion columns for `kill_switch_ok` and related checks.

5. **`umx_drift_and_budget_coupling_v1.md`**  
   - Defines how drift guards and NAP budgets are configured jointly and how they coordinate responses when both budget and drift thresholds are approached or exceeded.  
   - Specifies logging requirements so that the testbed can see the temporal relationship between budget overruns and drift guard activations.  
   - Ties behaviour to properties like `drift_guard_ok` and `back_pressure_ok`.

6. **`umx_paper_runtime_equivalence_v1.md`**  
   - Declares the paper-first principle: the Aether Testbed MASTER and MAX suites are the behavioural spec, and runtime must match them.  
   - Defines scenario IDs `Sxx`, shared data shapes and equality (or epsilon-bounded equality) of outputs between paper-mode and runtime.  
   - Specifies NO-GO handling when runtime and paper results diverge.

### 4.2 Recommended Read Order

1. `umx_epsilon_layers_and_drift_metrics_v1.md` — to understand how drift is defined and measured.  
2. `umx_emergence_bands_v1.md` — to see how drift becomes operator-facing bands.  
3. `umx_drift_and_budget_coupling_v1.md` — to understand how drift interacts with budgets.  
4. `umx_stress_test_matrix_v1.md` — to see required stress scenarios.  
5. `umx_kill_switch_and_quarantine_v1.md` — to understand safety behaviour.  
6. `umx_paper_runtime_equivalence_v1.md` — to understand testbed and runtime coupling.

---

## 5. Family III — Integration & Contracts

These documents define the **wiring** between UMX and other pillars and systems: NAP bus, SLP, Loom and U-Ledger.

### 5.1 Artefact List

1. **`umx_nap_bus_contract_v1.md`**  
   - Defines the UMX ↔ NAP bus contract: envelope fields, message identity, idempotence via `nonce`, exactly-once semantics, ordering and causality.  
   - Specifies backpressure signalling, dead-letter behaviour and isolation.  
   - Connects directly to MAX properties: `exactly_once_ok`, `ordering_causal_ok`, `duplicate_suppression_ok`, `id_key_seed_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `schema_negotiated`, `approval_ok`.

2. **`umx_node_manifest_v1.md`**  
   - Defines the Node Manifest: node table, edge table and region table.  
   - Specifies required fields, constraints (unique IDs, layer constraints, region assignment) and how manifests are used for routing, isolation and stress tests.

3. **`umx_slp_snapshot_ir_v1.md`**  
   - Defines the SLP Snapshot IR: tick, SLP profile ID, per-node or per-edge ley strengths and residuals, proposal flags and MDL deltas.  
   - Specifies when and how UMX consumes this IR in the tick pipeline.

4. **`umx_two_phase_tick_contract_v1.md`**  
   - Defines UMX tick behaviour as Phase A (read and compute) and Phase B (commit and emit).  
   - Specifies how UMX reads SLP IR and NAP envelopes in Phase A, and how it commits state and emits envelopes and ledger entries in Phase B.  
   - Defines constraints on ordering and non-interference between phases.

5. **`umx_commit_and_snapshot_manifests_v1.md`**  
   - Defines Commit Manifests (changes per tick) and Snapshot Manifests (state checkpoints).  
   - Specifies fields, scope, relationships to I/P-blocks and how these manifests are used for replay and skip-ahead or skip-back operations.

6. **`umx_u_ledger_contract_v1.md`**  
   - Defines the contract between UMX and the U-Ledger / time ledger system.  
   - Specifies required per-tick ledger fields, alignment with I-blocks and P-blocks and how replay is performed (snapshot + commits + epsilon corrections).  
   - Connects to properties such as `reversible_ok`, `checkpoint_spacing_ok`, `skip_ahead_ok`, `skip_back_ok`.

### 5.2 Recommended Read Order

1. `umx_node_manifest_v1.md` — to understand the static topology view.  
2. `umx_nap_bus_contract_v1.md` — to understand how UMX talks to the outside world.  
3. `umx_slp_snapshot_ir_v1.md` — to understand what UMX receives from SLP.  
4. `umx_two_phase_tick_contract_v1.md` — to connect static views and streams within ticks.  
5. `umx_commit_and_snapshot_manifests_v1.md` and `umx_u_ledger_contract_v1.md` — to understand time, history and replay.

---

## 6. Family IV — TBP Build & Operations Pack

These documents **translate the spec into a build, test and operations plan**, mirroring the TBP Gate pack.

### 6.1 Artefact List

1. **`tbp_umx_implementation_spec_v_1.md`**  
   - Implementation blueprint for UMX: pure-math core with JS shell, module breakdown, deterministic execution and mapping from modules to spec artefacts.  
   - Defines core state, tick engine, MDL and learning, NAP integration, ledger and manifests, drift and emergence, stress and safety modules.

2. **`tbp_umx_development_roadmap_v_1.md`**  
   - Development roadmap: Phase 0 (paper-only spec pack), Phase 1 (core math prototype in spreadsheets), Phase 2 (JS shell and core wiring), Phase 3 (testbed integration and MAX coverage), Phase 4 (stress, safety and operator tools).  
   - Each phase includes goals, tasks and exit criteria.

3. **`tbp_umx_verification_test_plan_v_1.md`**  
   - Verification strategy: unit-level math tests, integration tests and system tests via the Aether Testbed.  
   - Specifies what must be tested, with what artefacts and how success is defined.

4. **`tbp_umx_golden_fixtures_pack_v_1.md`**  
   - Defines the Golden Fixtures Pack: minimal topology fixture, residual and epsilon fixture, profile and MDL fixture, stress and safety fixture.  
   - Specifies fixture formats and expected outputs for regression.

5. **`tbp_umx_verification_plan_fixtures_crosswalk_v_1.md`**  
   - Crosswalk between verification objectives, Golden Fixtures and Aether Testbed scenarios.  
   - Used to track coverage and gaps.

6. **`tbp_umx_operator_runbook_v_1.md`**  
   - Operator runbook for UMX: pre-run checklist, running and monitoring scenarios, applying controls (kill-switch, quarantine, budgets), post-run tasks and incident response.

### 6.2 Recommended Use

- **Implementers** start with `tbp_umx_implementation_spec_v_1.md` and `tbp_umx_development_roadmap_v_1.md`.  
- **Verification engineers** focus on `tbp_umx_verification_test_plan_v_1.md`, `tbp_umx_golden_fixtures_pack_v_1.md` and the crosswalk.  
- **Operators** focus on `tbp_umx_operator_runbook_v_1.md` after understanding high-level profiles and emergence bands.

---

## 7. Legacy and Ancestor Documents

The following documents are **ancestors or companions** to the UMX v1 spec set. They remain part of the project record and may contain explanatory context, examples and derivations not fully repeated in the v1 artefacts.

- `universal_matrix_pillar_spec_v_1.md` — early UMX spec; now superseded for normative details by the v1 artefacts, but valuable for narrative and intuition.
- `Universal Matrix Pillar — Topology Substrate & Conservation Engine` — detailed treatment of the topology substrate and conservation engine; informs layer and conservation semantics.
- `umx_complement_docs_a_d_zero_layer_a_1.md` — Complement Docs A–D and A1, covering zero-layer and early gap families.
- `umx_complement_doc_e_invariants_layout.md` — invariants layout and early test formulations.
- `umx_complement_doc_f_llp→slp_propagation_temporal_behaviour.md` — propagation and temporal behaviour between LLP and SLP.
- `umx_complement_doc_g_nap_integration.md` and `umx_complement_doc_h_nap_integration_full.md` — early NAP integration framing and stress notes.
- `umx_complement_doc_i_gap_closure_profile_specs.md` — gap family index and initial profile framing that seeded the v1 artefacts.

Where these documents conflict with a **Bundle 1–4 artefact**, the Bundle artefact should be treated as authoritative for v1. Legacy docs should be consulted for understanding and future v2+ design, not to override v1 definitions.

---

## 8. Packaging Layout (UMX Spec Pack v1)

For handoff to implementers and verification teams, the UMX v1 spec should be packaged as a single ZIP, for example:

- `UMX_Spec_Pack_v1_2025-11-16.zip`

A suggested internal directory layout is:

- `README/`
  - `UMX_Spec_Master_Index_v1.md`  
- `core/`
  - `umx_mdl_objective_v1.md`  
  - `umx_layers_policy_v1.md`  
  - `anchor_map_v1.md`  
  - `subtick_semantics_v1.md`  
  - `umx_profile_v1.md`  
- `stress_emergence/`
  - `umx_epsilon_layers_and_drift_metrics_v1.md`  
  - `umx_emergence_bands_v1.md`  
  - `umx_stress_test_matrix_v1.md`  
  - `umx_kill_switch_and_quarantine_v1.md`  
  - `umx_drift_and_budget_coupling_v1.md`  
  - `umx_paper_runtime_equivalence_v1.md`  
- `integration/`
  - `umx_nap_bus_contract_v1.md`  
  - `umx_node_manifest_v1.md`  
  - `umx_slp_snapshot_ir_v1.md`  
  - `umx_two_phase_tick_contract_v1.md`  
  - `umx_commit_and_snapshot_manifests_v1.md`  
  - `umx_u_ledger_contract_v1.md`  
- `tbp/`
  - `tbp_umx_implementation_spec_v_1.md`  
  - `tbp_umx_development_roadmap_v_1.md`  
  - `tbp_umx_verification_test_plan_v_1.md`  
  - `tbp_umx_golden_fixtures_pack_v_1.md`  
  - `tbp_umx_verification_plan_fixtures_crosswalk_v_1.md`  
  - `tbp_umx_operator_runbook_v_1.md`  
- `legacy/`
  - `universal_matrix_pillar_spec_v_1.md`  
  - `Universal Matrix Pillar — Topology Substrate & Conservation Engine.pdf`  
  - `umx_complement_docs_a_d_zero_layer_a_1.md`  
  - `umx_complement_doc_e_invariants_layout.md`  
  - `umx_complement_doc_f_llp→slp_propagation_temporal_behaviour.md`  
  - `umx_complement_doc_g_nap_integration.md`  
  - `umx_complement_doc_h_nap_integration_full.md`  
  - `umx_complement_doc_i_gap_closure_profile_specs.md`  

Additional directories can be added for:

- `fixtures/` — Golden Fixtures Pack files and example Sxx scenarios,  
- `testbed/` — crosswalks and any UMX-specific enrichments to the Aether Testbed.

---

## 9. How to Use This Pack

### 9.1 For Implementers

1. Read this README end-to-end to understand the document map.  
2. Read `core/` and `integration/` artefacts that match the modules you are implementing.  
3. Use `tbp/tbp_umx_implementation_spec_v_1.md` and `tbp/tbp_umx_development_roadmap_v_1.md` as your primary build guides.  
4. Refer to `stress_emergence/` while implementing drift, epsilon and safety features.

### 9.2 For Verification Engineers

1. Read `stress_emergence/` and `integration/` to understand what must be observable.  
2. Use `tbp/tbp_umx_verification_test_plan_v_1.md` and `tbp/tbp_umx_golden_fixtures_pack_v_1.md` to design and run tests.  
3. Use `tbp/tbp_umx_verification_plan_fixtures_crosswalk_v_1.md` to track coverage.

### 9.3 For Operators

1. Skim `core/umx_profile_v1.md` and `stress_emergence/umx_emergence_bands_v1.md` to understand profiles and bands.  
2. Read `tbp/tbp_umx_operator_runbook_v_1.md` carefully.  
3. Use the runbook and spec references when running scenarios and interpreting GO/NO-GO reports.

---

## 10. Versioning and Evolution

This README describes **UMX v1** as of `2025-11-16`.

For any future version:

- Increment `version` in this README and in all updated artefacts.  
- Record changes in a `CHANGELOG` section or companion document.  
- Keep legacy versions in `legacy/` rather than overwriting them.  
- Maintain backwards references so that testbed results can always be tied to the spec version in use.

The UMX pillar is expected to evolve, but the **paper-first, deterministic, testbed-native** principles should remain stable anchors across versions.

### Nested README specs (verbatim)

#### Source: `README/UMX_Full_Buildplan_v1.md`

---
id: umx_full_buildplan_v1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-17
---

# Universal Matrix (UMX) — Full Buildplan v1

## 0. Purpose and Scope

This document is the full buildplan for the Universal Matrix (UMX) pillar v1.

It:

- Translates the UMX v1 spec artefacts and TBP pack into a concrete work breakdown.
- Assigns modules, phases, tasks, dependencies and acceptance criteria.
- Defines what it means to reach UMX v1 GO from an implementation perspective.

Required companion specs (separate docs, not to block UMX v1 build):

- MDL Placement & Motif Spec (UMX + Press + Codex)
- UMX Profiles & Budget / Policy Annex
- PFNA / Universal Commit v1 Record Spec

M3 (MDL) and fixture F03 are provisional until the MDL companion is signed off.

## 1. Build Assumptions and Constraints

- Pure-math core; JS shell. Deterministic execution; paper-first; single-machine, offline.
- Scope includes core state, tick engine, MDL proposals, NAP integration, U-Ledger, drift/epsilon/bands, budgets, kill-switch/quarantine, fixtures F01–F04, minimal operator UI.

## 2. Modules (M1–M9)

1. M1 — Core State & Topology
2. M2 — Tick Engine (Two-Phase + Subticks)
3. M3 — MDL & Learning Proposals
4. M4 — NAP Integration (Envelopes & Budgets)
5. M5 — Ledger, Commit & Snapshot Manifests
6. M6 — Drift, Epsilon Layers & Emergence Bands
7. M7 — Stress & Safety
8. M8 — Fixtures & Paper Testbed Wiring
9. M9 — JS Shell & Operator UI

(Details for each module were agreed in chat and are to be implemented following this breakdown.)

## 3. Phases (P0–P4)

- P0 — Spec Pack Consolidation (this ZIP)
- P1 — Core Math Prototype (paper-mode)
- P2 — JS Shell & Core Wiring
- P3 — Full Semantics & Testbed Integration (M3/F03 provisional if MDL companion not signed)
- P4 — Stress & Operator Tools

GO: modules implemented; Golden fixtures green; operator UX usable; replay/determinism verified.

#### Source: `README/UMX_Spec_Master_Index_v1.md`

---
id: umx_spec_master_index_v1
version: 1.0-draft
status: normative-shell
pillar: UMX
created: 2025-11-16
---

# Universal Matrix (UMX) — Spec Master Index & README (v1)

## 0. Purpose and Audience

This document is the top-level index and README for the Universal Matrix (UMX) pillar.

It is intended for:

- Spec authors and system designers — to see the complete UMX spec surface and document set.
- Implementers (devs) — to know which documents are normative for behaviour and which are build guides.
- Verification engineers — to locate all properties, fixtures and test plans that involve UMX.
- Operators — to find the runbook and understand what UMX exposes to the Aether Paper Testbed.

This README defines the canonical document set for UMX v1, groups documents into families, describes dependencies and read order,
and defines a packaging layout for handoff as a single ZIP. Where conflicts exist, the more specific normative artefact wins.

## 1. UMX Pillar Snapshot

UMX is the substrate and conservation engine for Aether:

- Maintains a graph-structured substrate of nodes and edges over one or more layers.
- Applies deterministic updates over a global tick with optional sub-ticks.
- Consumes SLP Snapshot IR at each tick.
- Records to Loom / U-Ledger using PFNA-compatible commit and snapshot manifests.
- Exchanges NAP envelopes with other pillars through membranes.
- Accepts structural proposals via an MDL objective (ΔL ≤ −τ acceptance rule).
- Exposes residuals, epsilon-layers, drift metrics and emergence bands to the Aether Paper Testbed.

Principles: paper-first; deterministic; testbed-native; conservative by default.

## 2. Document Families

UMX v1 documents are grouped into the following families:

1. Core Semantics & Profiles (`/core`)
2. Stress, Epsilon & Emergence (`/stress_emergence`)
3. Integration & Contracts (`/integration`)
4. TBP Build & Operations Pack (`/tbp`)
5. Fixtures & Testbed Integration Pack (`/fixtures/UMX`, `/testbed/UMX`)
6. Legacy & Companion Specs (`/legacy`, `/companions_pending`)

## 3. Family I — Core Semantics & Profiles (`/core`)

These documents define the behavioural core of UMX:

- `umx_mdl_objective_v1.md`
- `umx_layers_policy_v1.md`
- `anchor_map_v1.md`
- `subtick_semantics_v1.md`
- `umx_profile_v1.md`

## 4. Family II — Stress, Epsilon & Emergence (`/stress_emergence`)

These documents define residual semantics, epsilon layers, drift metrics, and stress/safety behaviour:

- `umx_epsilon_layers_and_drift_metrics_v1.md`
- `umx_emergence_bands_v1.md`
- `umx_stress_test_matrix_v1.md`
- `umx_kill_switch_and_quarantine_v1.md`
- `umx_drift_and_budget_coupling_v1.md`
- `umx_paper_runtime_equivalence_v1.md`

## 5. Family III — Integration & Contracts (`/integration`)

These define UMX’s contracts with other pillars and shared infrastructure:

- `umx_nap_bus_contract_v1.md`
- `umx_node_manifest_v1.md`
- `umx_slp_snapshot_ir_v1.md`
- `umx_two_phase_tick_contract_v1.md`
- `umx_commit_and_snapshot_manifests_v1.md`
- `umx_u_ledger_contract_v1.md`

## 6. Family IV — TBP Build & Operations Pack (`/tbp`)

Guiding and procedural documents for implementation, verification and operations:

- `tbp_umx_implementation_spec_v_1.md`
- `tbp_umx_development_roadmap_v_1.md`
- `tbp_umx_verification_test_plan_v_1.md`
- `tbp_umx_golden_fixtures_pack_v_1.md`
- `tbp_umx_verification_plan_fixtures_crosswalk_v_1.md`
- `tbp_umx_operator_runbook_v_1.md`

## 7. Fixtures & Testbed (`/fixtures/UMX`, `/testbed/UMX`)

- `fixtures/UMX/fixtures_index.tsv`
- Golden fixture directories `F01..F04`
- Scenario directories `S01..S04`

## 8. Legacy & Companions

- `/legacy` — optional background reports (not included in this pack).  
- `/companions_pending` — three companion specs gating cross-pillar details:

  - `MDL_Placement_and_Motif_Spec_UMX_Press_Codex_todo.md`
  - `UMX_Profiles_and_Budgets_Annex_todo.md`
  - `PFNA_Universal_Commit_Record_Spec_todo.md`

## Part 2 — Build Plan, Gap-Closure Passes, and Spec Artifact Bundles

### Source: `umx_full_buildplan_v_1_2025_11_17.md` (verbatim)

---
id: umx_full_buildplan_v1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-17
---

# Universal Matrix (UMX) — Full Buildplan v1

## 0. Purpose and Scope

### Required Companion Specs for v1

This buildplan assumes three **companion spec documents** exist alongside it. They are not optional; they hold shared definitions that span multiple pillars and would otherwise be duplicated or drift.

1. **MDL Placement & Motif Spec (UMX + Press + Codex)**  
   - Defines the shared MDL objective used across Press and UMX for topology placement, motif encoding, and structural proposals.  
   - Specifies:  
     - The exact codelength functional L used for structural models,  
     - Deterministic tie-break rules when two placements have equal cost,  
     - How Press motif IDs / transform graphs map onto UMX’s SLP/placement decisions,  
     - How Codex Eterna may propose motif or threshold adjustments without breaking determinism.  
   - This buildplan only refers to “MDL-aware placement” and “motif catalogues” at the module level; the **concrete math and encodings live in this companion spec**.

2. **UMX Profiles & Budget / Policy Annex**  
   - Defines the full schema for UMX profiles and routing/budget policies beyond the compact `profile.tsv` columns in the Fixtures & Testbed pack.  
   - Specifies:  
     - Field types, ranges and default values,  
     - The policy “dialect” (how to express per-layer/per-region/per-edge budgets and constraints),  
     - How profile versions are calibrated and recorded against testbed scenarios.  
   - This buildplan assumes that such a profile annex exists and treats profile fields as **given inputs**, not as free-form configuration.

3. **PFNA / Universal Commit v1 Record Spec**  
   - Defines the canonical record layout for the global PFNA hash chain and U-Ledger entries shared by UMX, Loom, Gate, Press and other pillars.  
   - Specifies:  
     - The binary or JSON schema for the event encodings,  
     - Field ordering, sizes and enum values for event categories,  
     - How per-pillar events (including UMX structural changes and flow summaries) are normalised into the shared ledger format.  
   - This buildplan states that UMX **must** contribute events to the PFNA hash chain and U-Ledger; the **precise record schema is defined once** in this companion spec.

In any apparent conflict between this buildplan and these companion specs:

- **UMX behaviour and responsibilities** follow this buildplan and the UMX pillar specs (Bundles 1–4).  
- **Cross-pillar encodings and shared math** (MDL, profile schema, PFNA ledger records) follow the companion specs.

Implementation teams should ensure these three documents are present and version-aligned with this buildplan before starting work.


This document is the **full buildplan** for the Universal Matrix (UMX) pillar v1.

It:

- Translates the UMX v1 spec artefacts and TBP pack into a **concrete work breakdown**.
- Assigns **modules, phases, tasks, dependencies and acceptance criteria**.
- Defines what it means to reach **UMX v1 "GO"** from an implementation perspective.

This buildplan assumes:

- UMX v1 specs (Bundles 1–4) and the **UMX Spec Master Index & README** are in place.
- The **UMX Fixtures & Testbed Integration Pack v1** directory and table schemas are defined.
- The first runtime target is an **offline JS page** wrapping pure math functions that can be executed on paper.

Implementation teams should treat this buildplan as the **single source of planning truth** for UMX v1. Where details appear in both this buildplan and a normative spec artefact, the **normative spec** remains authoritative for behaviour.

---

## 1. Build Assumptions and Constraints

### 1.1 Architectural Assumptions

1. **Pure-math core, JS shell**
   - All conceptual behaviour (state update rules, MDL objective, drift calculations, emergence bands, budgets, kill-switch semantics) must be definable as pure math on tables and integers.
   - The JS runtime is a shell that:
     - Calls these math functions,
     - Handles files (TSV import/export),
     - Provides a visual operator UI,
     - Does not introduce new semantics beyond what is defined in the specs.

2. **Determinism**
   - Given the same initial state, profile, NAP envelopes and SLP snapshots, UMX must produce the same ledger and outputs bit-for-bit.
   - No use of randomisation or non-deterministic JS APIs in the core tick path.

3. **Paper-first, testbed-native**
   - The Aether Paper Testbed MASTER and MAX suites are treated as the behavioural spec for observable properties.
   - Paper-mode (spreadsheets + TSVs) remains the arbiter; runtime must match it.

4. **Single-machine, offline**
   - v1 is designed for offline execution on a single machine.
   - No networking, no distributed coordination and no external services are required for basic operation.

### 1.2 Scope Boundaries

In scope for UMX v1 build:

- Core state representation (nodes, edges, layers, regions, residuals, epsilon layers).
- Tick engine (two-phase ticks + optional sub-ticks).
- MDL-based proposal evaluation (accept / reject).
- Integration with:
  - SLP Snapshot IR,
  - NAP envelopes (inbound and outbound),
  - U-Ledger (per-tick entries, commit and snapshot manifests).
- Drift metrics, emergence bands, drift guards.
- Budgets, backpressure, kill-switch, quarantine semantics.
- Fixtures and testbed integration for **F01–F04** and **S01–S04**.
- Minimal operator UI for loading scenarios, stepping ticks and viewing metrics.

Out of scope for UMX v1 build (may be added in later versions):

- Multi-node or distributed runtime.
- Complex UX or visualisations beyond basic charts and tables.
- Automated profile tuning based on live data.

---

## 2. Work Breakdown Structure (Modules)

The build is organised into the following modules. Each module maps directly to one or more normative spec artefacts.

1. **M1 — Core State & Topology**
2. **M2 — Tick Engine (Two-Phase + Subticks)**
3. **M3 — MDL & Learning Proposals**
4. **M4 — NAP Integration (Envelopes & Budgets)**
5. **M5 — Ledger, Commit & Snapshot Manifests**
6. **M6 — Drift, Epsilon Layers & Emergence Bands**
7. **M7 — Stress & Safety (Stress Matrix, Kill-Switch, Quarantine)**
8. **M8 — Fixtures & Paper Testbed Wiring**
9. **M9 — JS Shell & Operator UI**

Each module is described with:

- Objectives.
- Inputs (spec artefacts and fixture requirements).
- Tasks.
- Dependencies.
- Acceptance criteria.

---

## 3. Module Detail

### 3.1 M1 — Core State & Topology

**Objectives:**

- Implement a state representation that mirrors the **Node Manifest**, **Edge table** and **Region table**.
- Enforce constraints from `umx_layers_policy_v1.md` and `umx_node_manifest_v1.md`.

**Inputs:**

- `umx_layers_policy_v1.md`
- `umx_node_manifest_v1.md`
- Node and edge schemas from **UMX Fixtures & Testbed Integration Pack v1**.

**Tasks:**

1. **Define in-memory structures** (conceptual type definitions) that correspond 1:1 with:
   - Node rows (`node_id, layerId, region_id, node_type, capacity, flags, coord_x, coord_y`).
   - Edge rows (`edge_id, from_node_id, to_node_id, layer_relation, weight, capacity, flags`).
   - Region metadata (identifier and any additional per-region parameters).

2. **Implement layer policy checks**:
   - Validate that no edge violates the layer relation rules (no |Δlayer| > 1).
   - Validate that all nodes have valid `layerId` and that `layers_max_layers` in profile is not exceeded.

3. **Implement region assignment checks**:
   - Enforce that each node belongs to exactly one region.
   - Ensure that region IDs used in NAP envelopes and events match region definitions.

4. **Implement capacity checks**:
   - Confirm that node and edge capacities respect profile constraints (for example, `tick_max_nodes`, `tick_max_degree`).

5. **Implement import / export**:
   - Import `nodes.tsv` and `edges.tsv` into these structures.
   - Export them back out without loss (round-trip check).

**Dependencies:**

- None (M1 is foundational).

**Acceptance Criteria:**

- Note: Full, cross-pillar MDL behaviour is gated on the **MDL Placement & Motif Spec (UMX + Press + Codex)** companion. Until that spec is signed off, treat M3 and F03 as **provisional** and clearly document any placeholder MDL in fixtures and code.


- For each of the fixtures **F01–F04**, `nodes.tsv` and `edges.tsv` can be imported and exported without modifying values.
- Layer constraint checks succeed for F01–F04.
- Region assignment checks succeed for F03 and F04 where multiple regions are used.

---

### 3.2 M2 — Tick Engine (Two-Phase + Subticks)

**Objectives:**

- Implement the UMX portion of the global tick pipeline as a **two-phase tick**.
- Support optional sub-ticks that are equivalent to macro ticks up to epsilon corrections.

**Inputs:**

- `umx_two_phase_tick_contract_v1.md`
- `subtick_semantics_v1.md`
- `umx_profile_v1.md` (tick-related fields).

**Tasks:**

1. **Define tick entry point**:
   - Conceptual function signature: `tick_once(state, inputs, profile) -> state', outputs`.
   - `inputs` must include:
     - SLP Snapshot IR for the current tick.
     - NAP envelopes visibile at this tick.
     - Any scenario-specific external signals.

2. **Implement Phase A (Read/Compute)**:
   - Read:
     - Current state (nodes, edges, residuals, epsilon layers).
     - SLP Snapshot IR (M3 and M6 will define how this is used).
     - NAP envelopes (M4 will define how these are interpreted).
   - Compute:
     - Candidate state updates (without committing).
     - MDL proposals and their evaluation (hooks to M3).
     - Drift metrics for the current tick (hooks to M6).

3. **Implement Phase B (Commit/Emit)**:
   - Apply state changes decided in Phase A:
     - Node and edge updates.
     - Residual and epsilon updates.
   - Emit:
     - Outbound NAP envelopes.
     - Ledger entries for this tick.
     - Events such as drift guard activations or kill-switch events.

4. **Implement Sub-ticks (optional for v1 but specified)**:
   - Define how a macro tick can be split into sub-ticks with their own Phase A and Phase B.
   - Ensure that the sequence of sub-ticks produces the same macro-level outcomes (up to explicit epsilon corrections) as a single macro tick.

5. **Tick and profile constraints**:
   - Enforce per-tick limits such as `tick_max_nodes`, `tick_max_degree`, and other tick-related profile fields.

**Dependencies:**

- M1 (state structures).
- M3 (MDL outputs for Phase A decisions).
- M4 (NAP envelope interpretation for Phase A and outbound for Phase B).
- M6 (drift metrics for tick summaries).
- M5 (ledger entries in Phase B).

**Acceptance Criteria:**

- For F01 and F02, running `tick_once` across a small number of ticks produces stable, deterministic state changes that match the paper-mode expectations.
- Phase A and Phase B are clearly separated and do not interleave side effects.
- Optional sub-tick implementation, if used, produces the same end-of-window state as a single macro tick for F01.

---

### 3.3 M3 — MDL & Learning Proposals

**Objectives:**

- Implement the MDL objective evaluation and proposal acceptance logic as defined in `umx_mdl_objective_v1.md`.
- Keep the MDL implementation explicitly parameterised and linked to the **MDL Placement & Motif Spec (UMX + Press + Codex)** companion; until that spec is signed off, M3 may use a documented placeholder MDL consistent with `umx_mdl_objective_v1.md` for local testing.

**Inputs:**

- `umx_mdl_objective_v1.md`
- `umx_profile_v1.md` (MDL thresholds and windows).
- Fixture F03 (`F03_PROFILE_MDL`).

**Tasks:**

1. **Define canonical encodings**:
   - Specify how state or trace segments are encoded into a form suitable for MDL codelength calculation.
   - This should be done using integer-valued functions and simple aggregations.

2. **Implement codelength calculation**:
   - Implement the baseline codelength \(L_0\) for the current model.
   - Implement the candidate codelength \(L_1\) for a proposed change.
   - Compute \(\Delta L = L_1 - L_0\).

3. **Implement acceptance rule**:
   - Use profile parameter `mdl_tau` to check whether a proposal is accepted:
     - Accept if \(\Delta L \le -\tau\).
     - Reject otherwise.

4. **Integrate with tick engine**:
   - Provide a clear call such as `evaluate_proposals(state, snapshot, profile) -> accepted_set, rejected_set, metrics` for use in Phase A of the tick.

5. **Record MDL metrics**:
   - Record `delta_mdl` and acceptance decisions in:
     - Per-tick ledger metrics.
     - Optional events.
     - Any testbed tables required by the fixtures.

**Dependencies:**

- M1 (state representation).
- M2 (tick integration).

**Acceptance Criteria:**

- Fixture F03:
   - At least one proposal is accepted and one is rejected as designed.
   - For accepted proposals, `delta_mdl` in the ledger satisfies \(\Delta L \le -\tau\).
   - For rejected proposals, `delta_mdl` satisfies \(\Delta L > -\tau\).

---

### 3.4 M4 — NAP Integration (Envelopes & Budgets)

**Objectives:**

- Implement the UMX side of the UMX ↔ NAP bus contract.
- Enforce idempotence, exactly-once semantics and budgets as specified.

**Inputs:**

- `umx_nap_bus_contract_v1.md`
- `umx_profile_v1.md` (budgets and tolerances).
- NAP envelope schemas from the Fixtures & Testbed pack.
- Fixtures F01–F04 (envelopes particularly in F04).

**Tasks:**

1. **Envelope parsing and validation**:
   - Import `nap_envelopes.tsv` into internal envelope structures.
   - Validate required fields: `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`.

2. **Idempotence and duplicate suppression**:
   - Maintain a record of seen `nonce` values within a defined window.
   - Ensure that replays of envelopes with the same `nonce` do not cause double-application of state changes.

3. **Exactly-once semantics**:
   - For each processed envelope, record whether the effective state change was applied.
   - Make these records accessible to the testbed via tables or ledger metrics.

4. **Budget accounting**:
   - Track per-tick message counts and bytes.
   - Compare usage against `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance` and `nap_hard_tolerance`.

5. **Backpressure signalling**:
   - When soft thresholds are approached, emit backpressure signals via envelopes and events.
   - When hard thresholds are exceeded, trigger stronger responses (e.g. refusal to process further envelopes or activation of safety behaviour).

6. **Dead-letter and isolation behaviour**:
   - Route envelopes with invalid or unavailable targets to a dead-letter store.
   - Ensure that dead-letter envelopes are visible in `nap_envelopes.tsv` and testbed tables.
   - Respect isolation constraints for regions marked as isolated.

**Dependencies:**

- M1 (regions and nodes).
- M2 (tick integration).
- M5 (ledger metrics for budgets and events).

**Acceptance Criteria:**

- Fixture F01 and F02:
   - All envelopes expected to be applied are applied exactly once.
- Fixture F04:
   - Budget usage metrics match expectations.
   - Backpressure signals appear at the right ticks.
   - At least one envelope is properly marked as dead-letter.
   - `dead_letter_empty` is `FALSE` as designed.

---

### 3.5 M5 — Ledger, Commit & Snapshot Manifests

**Objectives:**

- Implement per-tick ledger entries and Commit / Snapshot Manifests as specified.
- Make replay and skip-ahead / skip-back operations possible.

**Inputs:**

- `umx_commit_and_snapshot_manifests_v1.md`
- `umx_u_ledger_contract_v1.md`
- `umx_paper_runtime_equivalence_v1.md`
- Ledger and manifest-related parts of Fixtures F01–F04.

**Tasks:**

1. **Define ledger record structure**:
   - Map ledger columns to an internal ledger record.
   - Fields include: `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`.

2. **Implement Commit Manifest construction**:
   - For each tick, summarise state changes into a Commit Manifest entry (counts of nodes and edges added/removed/modified, epsilon entries created, MDL statistics).

3. **Implement Snapshot Manifests**:
   - Define when snapshots are taken (based on `ledger_snapshot_interval` and other rules).
   - Record scope and references for snapshots.

4. **Write ledger and manifests to TSV**:
   - Export `ledger.tsv` and any manifest tables in a format that can be consumed by the paper testbed.

5. **Replay utilities (paper-first design)**:
   - Define a procedure for replaying state from a snapshot plus subsequent Commit Manifests.
   - Ensure that replayed state matches original state for F01 and F02.

**Dependencies:**

- M1 (state representation).
- M2 (tick engine).
- M3 (MDL metrics).
- M4 (budget and events for ledger fields).
- M6 (drift metrics for `drift_global`).

**Acceptance Criteria:**

- For F01 and F02:
   - Replaying state from snapshot and Commit Manifests reproduces the original end-of-window state.
   - `reversible_ok`, `checkpoint_spacing_ok`, `skip_ahead_ok` and `skip_back_ok` evaluate as `TRUE` in the paper testbed.

---

### 3.6 M6 — Drift, Epsilon Layers & Emergence Bands

**Objectives:**

- Implement epsilon-layer structures and drift metrics.
- Classify drift into emergence bands.

**Inputs:**

- `umx_epsilon_layers_and_drift_metrics_v1.md`
- `umx_emergence_bands_v1.md`
- `umx_drift_and_budget_coupling_v1.md`
- `umx_profile_v1.md` (residual and emergence sections).
- Fixtures F02 and F04.

**Tasks:**

1. **Epsilon-layer representation**:
   - Implement storage for epsilon entries keyed by anchors and ticks.
   - Ensure one-to-one mapping between epsilon entries and base anchors.

2. **Residual and epsilon import/export**:
   - Import `residual_epsilon.tsv` into combined residual/epsilon structures.
   - Export these structures back to TSV.

3. **Per-node and global drift calculation**:
   - Compute \(\Delta_i(W)\) for a given window \(W\) using residual norms and epsilon corrections.
   - Aggregate per-node drift into global drift \(\Delta(W)\).

4. **Emergence band classification**:
   - Use `emergence_epsilon_drift` from the profile to classify drift values as PASS, INVESTIGATE or FAIL.
   - Implement QUARANTINE flag handling for scenarios or regions.

5. **Drift–budget coupling hooks**:
   - Expose drift metrics to M7 and M4 so that drift guards and budget behaviour can be coordinated.

**Dependencies:**

- M1 (anchors and state).
- M2 (tick context for windows).
- M4 (budget coupling).

**Acceptance Criteria:**

- Fixture F02:
   - Drift metrics computed from `residual_epsilon.tsv` match expected `drift_metrics.tsv`.
   - At least one window falls into `INVESTIGATE` band as defined.
- Fixture F04:
   - Drift metrics respond to stress conditions as expected.
   - `drift_guard_ok` evaluates `TRUE` in the paper testbed.

---

### 3.7 M7 — Stress & Safety (Stress Matrix, Kill-Switch, Quarantine)

**Objectives:**

- Implement the stress test matrix and safety behaviours.

**Inputs:**

- `umx_stress_test_matrix_v1.md`
- `umx_kill_switch_and_quarantine_v1.md`
- `umx_drift_and_budget_coupling_v1.md`
- Fixture F04.

**Tasks:**

1. **Stress scenario recognition**:
   - Implement support for high-load, backpressure, dead-letter and isolation scenario types as described.

2. **Kill-switch implementation**:
   - Implement kill-switch activation for scopes `NODE`, `REGION` and `SYSTEM`.
   - Ensure that activation stops new envelope processing for the scope and that state remains consistent.
   - Record kill events in `events.tsv` and corresponding ledger fields.

3. **Quarantine semantics**:
   - Implement scenario-level and region-level quarantine flags.
   - Ensure that drift and stress behaviour in quarantined regions is interpreted according to spec.

4. **Stress metrics and properties**:
   - Record metrics needed to evaluate `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `kill_switch_ok`.

**Dependencies:**

- M1 (regions and topology).
- M2 (tick engine).
- M4 (budgets and envelopes).
- M6 (drift guards).
- M5 (ledger entries).

**Acceptance Criteria:**

- Fixture F04:
   - Kill-switch events align with envelope and budget triggers.
   - Quarantine flags are set and cleared according to scenario design.
   - Testbed properties `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `kill_switch_ok`, `drift_guard_ok` evaluate as expected.

---

### 3.8 M8 — Fixtures & Paper Testbed Wiring

**Objectives:**

- Implement the Golden Fixtures F01–F04 and connect UMX runtime to the Aether Paper Testbed via TSVs.

**Inputs:**

- UMX Fixtures & Testbed Integration Pack v1.
- All module outputs M1–M7.

**Tasks:**

1. **Concrete fixture construction**:
   - Populate all F01–F04 directories with concrete `nodes.tsv`, `edges.tsv`, `profile.tsv`, `residual_epsilon.tsv`, `drift_metrics.tsv`, `nap_envelopes.tsv`, `events.tsv`, `ledger.tsv`, `assertions.tsv` in line with the spec.
   - For F03 specifically, allow use of a **placeholder MDL** until the MDL Placement & Motif companion spec is final; mark this clearly in `fixtures_index.tsv` and `assertions.tsv` notes as `provisional_mdl`.

2. **Testbed harness wiring**:
   - Define the mapping from TSV files to testbed sheets.
   - Implement export routines to generate TSVs from the UMX runtime that match these shapes.

3. **Fixture execution**:
   - Run UMX runtime against each fixture configuration to produce output TSVs.
   - Run the paper testbed to evaluate properties.

4. **Golden baseline creation**:
   - For each fixture, capture a baseline set of TSV outputs to use as Golden Fixtures for regression.

**Dependencies:**

- M1–M7 (full functionality is needed to exercise all fixtures).

**Acceptance Criteria:**

- All fixtures F01–F04 are fully populated and stable.
- Paper testbed runs for S01–S04 produce `result = PASS` for all properties defined in `assertions.tsv`.
- UMX runtime outputs match Golden Fixture expectations for F01–F04.

---

### 3.9 M9 — JS Shell & Operator UI

**Objectives:**

- Provide an offline JS shell and minimal operator UI for UMX.

**Inputs:**

- `tbp_umx_implementation_spec_v_1.md`
- `tbp_umx_operator_runbook_v_1.md`

**Tasks:**

1. **JS module scaffolding**:
   - Create JS modules corresponding to M1–M7 functions.

2. **File I/O**:
   - Implement import of fixture TSVs.
   - Implement export of runtime TSVs in the exact schemas defined.

3. **Operator UI**:
   - Provide controls for:
     - Selecting profile and scenario.
     - Running ticks (step or batch).
     - Viewing drift metrics, budgets, kill-switch and quarantine status.
   - Ensure that UI does not encode new semantics; it only visualises state and metrics.

4. **Run logging**:
   - Log operator actions such as kill-switch activation and profile changes.
   - Ensure these logs can be correlated with ledger entries.

**Dependencies:**

- M1–M7 (runtime capabilities).
- M8 (fixtures and testbed wiring for end-to-end tests).

**Acceptance Criteria:**

- Operator can load F01–F04, run ticks and export TSVs without editing files by hand.
- Operator can trigger kill-switch and quarantine in F04 via UI controls, and testbed evaluations reflect these actions.

---

## 4. Phased Delivery Plan

This section ties modules to phases and defines milestones.

### 4.1 Phase 0 — Spec Pack Consolidation

**Goal:** UMX spec and packs are assembled and versioned.

**Scope:**

- Finalise Bundles 1–4.
- Finalise UMX Spec Master Index & README.
- Finalise Fixtures & Testbed Integration Pack v1.

**Modules:**

- No code modules; this phase is spec-only.

**Milestone P0:**

- `UMX_Spec_Pack_v1_YYYY-MM-DD.zip` created with the directory layout described in the Master Index.

### 4.2 Phase 1 — Core Math Prototype (Paper-Mode)

**Goal:** Running UMX in pure paper-mode for minimal scenarios.

**Scope:**

- Implement core math in spreadsheets or equivalent representations.
- Cover F01 and core parts of F02.

**Modules:**

- M1 (Core State & Topology) — partial.
- M2 (Tick Engine) — minimal tick for F01.
- M6 (Drift & Epsilon) — minimal drift (zero drift for F01).
- M5 (Ledger) — simple per-tick records.

**Milestone P1:**

- F01 fully implemented in paper-mode; all properties pass.

### 4.3 Phase 2 — JS Shell & Core Wiring

**Goal:** JS runtime exists and matches paper-mode for F01.

**Scope:**

- Implement JS shell for M1, M2 (basic), M5 (basic), M8 (import/export for F01 only).

**Modules:**

- M1 (Core State & Topology).
- M2 (Tick Engine) — limited to features used in F01.
- M5 (Ledger) — limited ledger fields used in F01.
- M8 (Fixtures & Testbed) — F01 only.
- M9 (JS Shell & UI) — minimal UI to run F01.

**Milestone P2:**

- JS runtime runs F01 and produces TSVs that match the paper-mode Golden Fixture for S01.

### 4.4 Phase 3 — Full Semantics & Testbed Integration

**Goal:** Full UMX semantics for F01–F03 and integration with testbed.

**Scope:**

- Implement M3, M4, M6 and expand M2, M5, M8.
- Treat M3 and F03 as **provisional** if the MDL Placement & Motif companion spec is not yet signed off (placeholder MDL is allowed, but must be clearly annotated).

**Modules:**

- M3 (MDL & Learning Proposals).
- M4 (NAP Integration).
- M6 (Drift & Epsilon) — full implementation.
- M2 (Tick Engine) — full implementation.
- M5 (Ledger) — full implementation.
- M8 (Fixtures) — F01–F03 fully wired.

**Milestone P3:**

- F01–F03 run through the JS runtime and paper testbed with all properties passing.
- If the MDL Placement & Motif Spec is not yet final, F03 and M3 are explicitly marked **provisional** (placeholder MDL), and this status is reflected in fixture metadata and operator documentation.

### 4.5 Phase 4 — Stress, Safety & Operator Tools

**Goal:** Stress and safety behaviours are implemented and observable for F04; operator UI is feature-complete for v1.

**Scope:**

- Implement M7.
- Finalise M9.
- Finalise F04 and S04 testbed scenario.

**Modules:**

- M7 (Stress & Safety).
- M9 (JS Shell & Operator UI).
- M8 (Fixtures) — F04.

**Milestone P4:**

- F04 passes all targeted properties.
- Operator can run F01–F04 from UI and export TSVs.

---

## 5. Definition of "UMX v1 GO" (Implementation)

UMX v1 is considered **GO** from an implementation perspective when:

1. **Spec Alignment**
   - All modules M1–M9 are implemented consistently with their corresponding spec artefacts.

2. **Golden Fixtures**
   - All four Golden Fixtures F01–F04 are fully populated and stable.
   - UMX runtime outputs match Golden Fixture expectations for S01–S04.

3. **Testbed Properties**
   - For S01–S04, all properties defined in `assertions.tsv` evaluate with `result = PASS` under the Aether Paper Testbed plus UMX runtime outputs.

4. **Operator UX**
   - Operator can:
     - Load scenarios and profiles via UI.
     - Run ticks and batches.
     - View drift, budgets, kill-switch and quarantine status.
     - Export TSVs for testbed evaluation.

5. **Replay & Determinism**
   - For F01 and F02, replay via Snapshot + Commit Manifests reproduces the original run state.
   - For F01–F04, multiple runs with identical inputs produce identical outputs.

---

## 6. Risk Register and Open Questions (v1)

This section lists known risks and open questions that should be tracked during the build.

1. **MDL Coding Scheme Choice & Dependency on Companion Spec**
   - Risk: The precise numerical form of the codelength functional may need tuning, and final MDL behaviour depends on the shared **MDL Placement & Motif** companion spec and Codex/Press/Loom cores.
   - Mitigation: Start with a simple, clearly-documented placeholder MDL consistent with `umx_mdl_objective_v1.md`; validate using F03. Treat MDL as parameterised, keep it wired to the companion spec, and explicitly mark M3/F03 as **provisional** until the MDL companion spec and Codex/Press/Loom cores are signed off.

2. **Sub-tick Complexity**
   - Risk: Sub-tick implementation may add complexity without immediate test coverage.
   - Mitigation: Initially implement sub-ticks only for F01; ensure spec-defined equivalence is demonstrable; defer advanced use until v2.

3. **Fixture Overfitting**
   - Risk: Runtime could accidentally be tuned to Golden Fixtures at the expense of generality.
   - Mitigation: Keep fixtures transparent and simple; use additional ad hoc scenarios for manual sanity-checking; avoid hard-coding fixture IDs.

4. **Budget and Drift Coupling**
   - Risk: Misalignments between budgets and drift thresholds could cause frequent false positives or masked issues in F04.
   - Mitigation: Use F02 and F04 together to tune profile parameters; explicitly record calibration decisions in profile docs.

---

## 7. Evolution to v2

This buildplan covers **UMX v1**. For v2 and beyond, likely expansions include:

- Multi-layer topologies with non-trivial `layer_relation` patterns.
- Additional fixtures beyond F04 (for example, multi-layer drift, advanced MDL models, more complex NAP interaction patterns).
- Richer UI and visualisations of drift, epsilon usage and MDL decisions.

Any evolution must:

- Preserve paper-first, deterministic, testbed-native principles.
- Extend rather than silently mutate v1 semantics (or clearly document breakage in a versioned changelog).

This concludes the UMX v1 Full Buildplan.

### Source: `umx_gap_closure_build_plan_pass_01_2025_11_16.md` (verbatim)

# UMX — Gap Closure & Build Plan — Pass 01 — 2025-11-16

## 0. Scope & Method (Pass 01)

**Goal of this pass**

Pass 01 is a full sweep over all gap families I‑1 … I‑27 from **Complement Doc I — Gap Closure & Profile Specs (UMX + SLP + NAP v1.x)**. For each gap family we:

1. Record the **pre‑pass status** (what Complement Doc I already says).
2. Add **Pass 01 decisions & clarifications**, especially where we can ground things in the Aether Math Compendium.
3. Explicitly list **features / capabilities / functions** that belong to that gap.
4. Add **build‑plan hooks** – what dev‑facing modules and paper operations this gap implies.
5. Mark a **status after Pass 01**: `Open`, `Partial`, or `Closed (v1.x spec)`.

Pass 01 aims for:

- Deep closure for **math‑critical families** (MDL, residual behaviour, determinism, reversibility, NAP↔UMX mapping, ledger, timing & nesting).
- Light‑touch classification (feature naming + hooks) for the remaining families, which will be deepened in later passes.

**Primary sources used in this pass**

- `umx_complement_doc_i_gap_closure_profile_specs.md` — gap index and baseline Summary / Normative / Artefacts / Implementation for I‑1 … I‑27.
- `Aether Math Compendium – Deterministic Framework & Equations Overview` — global invariants, MDL / Press equations, Lattice energy and residual dynamics, Loom skip‑ahead, Trinity Gate quantisation, NAP nest continuity, U‑ledger and PFNA formalism.

No new mathematics are invented here; Pass 01 only **re‑expresses and pins** what already exists in the compendium and surrounding pillar docs, making it explicit for the UMX build plan.

Notation: we keep the project’s usual symbols (L_total, E_t, Δ_safe, μ, β, etc.) consistent with the compendium.

---

## 1. Global Feature & Capability Frame (Pass 01 Snapshot)

This section lists the cross‑cutting features and capabilities that emerged or were clarified during Pass 01. Later passes will expand and re‑group these.

### 1.1 Core UMX / SLP Features (Pass 01)

- **Deterministic Lattice Update Engine**
  - Integer‑only update rule over a grid of nodes.
  - Each tick is a deterministic function of previous state + Gate inputs.
  - All state transitions respect a global continuity invariant: sum of changes over the lattice is zero for conserved quantities.

- **Residual‑Driven Structural Relaxation**
  - Residuals R(τ) defined as a norm over edge differences |S[u] − S[v]|.
  - SLP seeks to reduce R over time in the absence of new writes, behaving like a diffusive system.

- **MDL‑Aware Topology & Anchor Selection**
  - Topology (anchors, edges) is evaluated under a scalar MDL objective L_total that combines symbolic coding cost, geometric penalties, and degree penalties.
  - Greedy update rule: candidate changes accepted only if they strictly reduce L_total.

- **Multi‑Layer UMX Envelope (PFNA‑Compatible)**
  - UMX is defined over layers ℓ with Δℓ penalties and optional stack_delta semantics.
  - v1 reference remains single‑layer (ℓ = 0) but the spec anticipates multiple layers.

- **SLP Structural Plasticity Overlay**
  - Named operations: grow, potentiate, prune, conduct.
  - Operate over side‑structures (weights, usage counters, candidate queues, MDL scores) that can rebuild the UMX edge list.

### 1.2 NAP / Loom / Press / Ledger Features (Pass 01)

- **Canonical TickRecord v1** (UMX ↔ Loom ↔ Press ↔ NAP)
  - Wraps each UMX TickLedger into a single record containing:
    - Envelope metadata (τ, config hash, profile id, etc.).
    - Full TickLedger body (rootHash, p‑block, i‑block, and any residual summaries).
    - Optional Press summary capsule (compressed view).
    - Hash‑chain fields for Loom / NAP audit.

- **Skip‑Safe Time Evolution & Sub‑Tick Semantics**
  - Loom’s skip‑ahead logic provides Δ_safe bounds on how far we can jump without missing an event, based on Lipschitz or exact motion bounds.
  - Sub‑ticks are defined as multiple tickOnce() calls with scaled inputs; splitting a tick into M sub‑ticks must be equivalent to one macro‑tick for the same integrated input.

- **Reversible Tick Windows & PFNA‑Style Replay**
  - Each tick is recorded as an invertible event; checkpoints plus event sequences allow exact replay of any window.
  - Reversibility windows define how far back one can deterministically roll before discarding older events.

- **U‑Ledger with Universal Integer Indexing**
  - Ledger entries index events by integer tuples (e.g. nodeId, layer, tick, rootHash index) with a documented, universal ordering.
  - Ledger is append‑only and hash‑chained.

- **Budget / Quota & Drift Policies**
  - Per‑node quotas on messages, payload bytes, and μ‑drift per tick.
  - Profiles define allowed drift τ and reactions (log, degrade, fail).

### 1.3 Timing, Nesting & Profile Features (Pass 01)

- **Profiled Global Parameter Sets**
  - Named profiles (dev_low_res, matrix_demo_default, nested_sim_dense, etc.) fix all relevant parameters (grid size, r, c, D★, SC, k, MDL weights, thresholds, quotas).

- **Two‑Phase Tick Hooks for UMX**
  - Phase 1: compute tick (UMX core update).
  - Phase 2: sync tick (NAP message exchange, SEAL, ledger updates, τ increment).

- **Nesting Profiles & Tick Ratios**
  - Logical layers (Village, Town, City, etc.) have fixed tick ratios k_VT, k_TC, etc.
  - Nesting profiles define how summary packets flow and how ticks align across layers.

---

## 2. Gap Family Sweep (I‑1 … I‑27)

For each gap we follow this template:

- **Pre‑pass status** – short recap of Complement Doc I’s gap description.
- **Pass 01 – decisions & clarifications** – what tightened this pass, especially mathematically.
- **Pass 01 – features & capabilities** – explicit named features that live here.
- **Pass 01 – functions / operations** – paper‑level functions, with inputs/outputs.
- **Pass 01 – build‑plan hooks** – how it maps into the eventual dev build plan.
- **Status after Pass 01** – Open / Partial / Closed (v1.x spec).

### I‑1 — MDL / Description‑Length Objective (Topology & SLP)

**Pre‑pass status**

- Docs state that both UMX and SLP choose anchors and edges to minimise description length (MDL) with penalties for distance, degree, movement, etc.
- Complement Doc I notes that the shape of the objective is described but no canonical coding scheme or parameter set is frozen.
- Normative target: a minimal scalar objective L_total over anchor choices and candidate edges, with explicit cost terms and a deterministic greedy update rule. Spec artefacts: `mdl_objective_v1.md`, `mdl_parameters_v1.md`.

**Pass 01 – decisions & clarifications (math)**

1. **Scalar objective definition**
   - Define L_total as a sum over per‑node and per‑edge contributions:
     - For each node i and chosen anchor a_i, a coding cost term L_anchor(i, a_i).
     - For each candidate edge e = (i, j), a coding cost term L_edge(e).
   - L_total is the total bit‑length proxy of representing the topology plus penalties:
     - L_total = Σ_i L_anchor(i, a_i) + Σ_e L_edge(e).

2. **Anchor coding cost term**
   - For an anchor at position p(a_i) in PFNA coordinate space and node position p(i):
     - L_anchor(i, a_i) = L_id(i) + L_id(a_i) + λ_dist · ||p(i) − p(a_i)||_1 + λ_move · |p_old(a_i) − p_new(a_i)|_1.
   - L_id terms approximate the integer coding length of identifiers; λ_dist and λ_move are MDL weights.

3. **Edge coding cost term**
   - For an edge e = (i, j) with degree d_i, d_j and layer difference Δℓ:
     - L_edge(e) = L_pair(i, j) + λ_deg · (d_i + d_j) + λ_layer · |Δℓ|.
   - L_pair(i, j) proxies the bits to specify a pair, e.g. via sorted index encoding.

4. **Greedy update rule**
   - Given a set of candidate modifications M (anchor changes, edge add/drop), we define ΔL_total(m) = L_total(after m) − L_total(before).
   - Fix a deterministic ordering of candidates using a hash of (type, node id(s), τ).
   - Sweep candidates once per evaluation; apply only those with ΔL_total < 0.
   - This rule is **purely integer and local**, and can be executed on paper in principle.

5. **Relationship to Press MDL**
   - L_total is constrained to be consistent with Press’s MDL cost function:
     - For any encoded snapshot of topology into Press, the topology contribution to total description length should be less than or equal to what Press would pay to encode the same structure directly.
   - This ensures that UMX’s internal MDL choices do not contradict the global MDL objective used in compression.

**Pass 01 – features & capabilities**

- **Feature F‑MDL‑1 – MDL Topology Evaluator**
  - Given a frozen UMX snapshot, computes L_total over anchors and edges.

- **Feature F‑MDL‑2 – Greedy MDL Topology Optimiser**
  - Applies a deterministic sweep of candidate changes and accepts those that strictly reduce L_total.

- **Capability C‑MDL‑1 – MDL‑consistent structural plasticity**
  - SLP and topology adjustments are constrained to never increase L_total for accepted changes.

**Pass 01 – functions / operations**

- **Function**: MDL_EVAL(snapshot)
  - Input: UMX snapshot (node positions, anchors, edges, degrees, layers).
  - Output: scalar integer L_total.

- **Function**: MDL_DELTA(snapshot, modification m)
  - Input: snapshot, a single candidate modification m.
  - Output: ΔL_total(m) as an integer.

- **Function**: MDL_GREEDY_PASS(snapshot, candidate list M)
  - Input: snapshot, ordered list M.
  - Output: new snapshot with all accepted modifications.

**Pass 01 – build‑plan hooks**

- The UMX build plan must include:
  - A **pure math specification** of MDL_EVAL and MDL_GREEDY_PASS.
  - A mapping from SLP operations (grow/prune) to candidate modification sets M.
  - Tests comparing UMX’s internal MDL objective against Press MDL on simple topologies.

**Status after Pass 01**

- **Status**: **Partial** (scalar form and greedy rule are pinned; parameter profiles and Press calibration remain to be fully enumerated in later passes).

---

### I‑2 — SLP APIs & Data Structures

**Pre‑pass status**

- Complement Doc I defines the gap as lack of a public SLP API and canonical data structures for plasticity (weights, usage counters, candidate queues, MDL scores) and no numeric thresholds.

**Pass 01 – decisions & clarifications**

1. Treat the **SLP API** as a **logical operation set**, not a language‑bound interface:
   - The core operations are: GROW_EDGES, PRUNE_EDGES, UPDATE_USAGE, RUN_PLASTICITY_PASS.
   - Each operation is defined as a deterministic transform on integer arrays:
     - adjacency data A,
     - weight array W,
     - usage counters U,
     - MDL score arrays S.

2. Plasticity cadence is parameterised by an integer N_plasticity_ticks per profile.

**Pass 01 – features & capabilities**

- **Feature F‑SLP‑1 – Structural Plasticity Overlay**
  - Maintains a side structure (A, W, U, S) that can rebuild the UMX edge list.

- **Capability C‑SLP‑1 – Controlled topology adaptation**
  - The system can adjust edges over time while remaining deterministic and MDL‑consistent.

**Pass 01 – functions / operations**

- GROW_EDGES(A, W, U, S, profile).
- PRUNE_EDGES(A, W, U, S, profile).
- UPDATE_USAGE(A, U, recent traffic).
- RUN_PLASTICITY_PASS(snapshot, profile).

All functions are paper‑computable: pure transforms on integer tables.

**Pass 01 – build‑plan hooks**

- The build plan must show where these SLP operations plug into the tick (before/after core lattice update, and at which cadence).

**Status after Pass 01**

- **Status**: **Open → Partial** (operations and data shapes are established conceptually; numeric thresholds and concrete profiles will be added in later passes).

---

### I‑3 — Multi‑Layer UMX

**Pre‑pass status**

- PFNA allows layers ℓ; routing depends on Δℓ; NAP has stack_delta. Current JS core runs effectively a single layer, with no clear multi‑layer policy.

**Pass 01 – decisions & clarifications**

1. **Layer id semantics**
   - layerId is an integer ℓ ∈ Z attached to each node and edge.
   - For v1 UMX, only a finite band of layers is allowed per profile (e.g. ℓ ∈ {0} for single‑layer, or ℓ ∈ {−1,0,1} for tri‑layer profiles).

2. **Allowed edges and penalties**
   - Edges are allowed only between nodes i, j with |ℓ_i − ℓ_j| ≤ Δℓ_max.
   - Default Δℓ_max = 1 in multi‑layer profiles; Δℓ_max = 0 in strictly single‑layer profiles.
   - Edge cost includes λ_layer · |Δℓ| as in MDL edge term (I‑1).

3. **Single‑layer reference**
   - The reference profile for Matrix v1 is ℓ = 0 only; all multi‑layer semantics must reduce to this when Δℓ_max = 0.

**Pass 01 – features & capabilities**

- **Feature F‑LAY‑1 – Layered UMX Envelope**
  - Same lattice rules replicated across multiple ℓ bands.

- **Capability C‑LAY‑1 – Layer‑aware routing and cost**
  - Topology and routing can trade off within‑layer vs cross‑layer edges via |Δℓ| penalties.

**Pass 01 – functions / operations**

- LAYER_FILTER(edges, Δℓ_max).
- LAYER_COST(e) = λ_layer · |Δℓ(e)|.

**Pass 01 – build‑plan hooks**

- The build plan must:
  - Include a **layer policy table** per profile (allowed ℓ range, Δℓ_max, penalties).
  - Make clear that all v1 examples use ℓ = 0 to keep implementation simple.

**Status after Pass 01**

- **Status**: **Partial** (policy constraints pinned; remaining work is to integrate with NAP nesting profiles and concrete examples).

---

### I‑4 — UMX Node Manifest & Actor Slots

**Pre‑pass status**

- Complement Doc I notes the lack of a formal manifest schema beyond raw integer fields. It proposes a Node Manifest with fields like id, anchor, layer, gridIndex, fieldOffsets, policyFlags, tags.

**Pass 01 – decisions & clarifications**

- No new math is required here; the gap is structural description.
- We treat the Node Manifest as a **deterministic projection** from an integer index space to semantic roles.

**Pass 01 – features & capabilities**

- **Feature F‑NODE‑1 – Node Manifest Table**
  - A finite table mapping each node index k to a tuple of attributes (id, anchor index, layer ℓ, grid index, policy flags, tags).

**Pass 01 – functions / operations**

- MANIFEST_LOOKUP(k) → manifest tuple.
- FIELD_OFFSET(k, fieldId) → integer offset into the core state vector.

**Pass 01 – build‑plan hooks**

- The build plan must specify the manifest table for each profile and how it is derived from basic grid parameters.

**Status after Pass 01**

- **Status**: **Open → Partial** (structure is clear; concrete manifests per profile and actor slot semantics will be specified in later passes).

---

### I‑5 — NAP Bus Backpressure & Flow‑Control Hooks

**Pre‑pass status**

- NAP does backpressure and partitioning conceptually; there is no explicit handshake between NAP and UMX in specs.

**Pass 01 – decisions & clarifications**

- We treat backpressure as a **bounded integer counter** mechanism:
  - For each node, maintain per‑tick counts of outgoing messages and bytes.
  - NAP exposes a per‑tick state (e.g. BUS_LOAD level) which is an integer in a small range (0…K).

**Pass 01 – features & capabilities**

- **Feature F‑NAP‑BP‑1 – Bus Load Meter**
  - Deterministic mapping from envelope counts/bytes to a discrete load level.

**Pass 01 – functions / operations**

- BUS_LOAD(envelopes_this_tick) → load level.
- GATE_THROTTLE_POLICY(load level, profile) → allowed emission per node.

**Pass 01 – build‑plan hooks**

- Build plan must show where BUS_LOAD is computed and how it feeds back into Gate write limits.

**Status after Pass 01**

- **Status**: **Open → Partial** (mechanism shape fixed; thresholds and exact policies to be pinned with quota profiles in I‑20).

---

### I‑6 — Loom/Press Interop (Beyond Hash + P‑deltas)

**Pre‑pass status**

- UMX exposes TickLedger (rootHash, p‑block, i‑block). Loom & Press need a canonical schema for what gets hashed, how P‑deltas and I‑blocks are packaged, and what minimal data Press compresses.

**Pass 01 – decisions & clarifications (math)**

1. **TickRecord v1 structure**
   - TickRecord(τ) contains:
     - Metadata: τ (logical tick), profile id, config hash, layer profile id.
     - TickLedger body: rootHash, p‑block summary, i‑block summary.
     - Optional Press capsule: a Pressed representation of the p‑block and selected observables.
     - Hash chain fields: parentTickHash, tickHash.

2. **Hash chain invariant**
   - tickHash(τ) = H(parentTickHash(τ−1), serialized TickLedger(τ)).
   - This ensures any change in TickLedger is detectable by hash mismatch.

3. **Press contract**
   - Press is required to be **exactly reversible** on its capsule: decompress(Press(p‑block)) = p‑block.
   - Press’s cost function L is used only to choose internal coding modes, not to alter the semantics of TickLedger.

4. **Loom skip integration**
   - When Loom performs a skip of Δ ticks, TickRecord entries for intermediate ticks may be omitted in the primary log, but the hash chain and audit log record the skip window and verification window size.

**Pass 01 – features & capabilities**

- **Feature F‑TR‑1 – TickRecord v1 Schema**
  - A rigid, profile‑independent schema for per‑tick records.

- **Capability C‑TR‑1 – Deterministic Replay & Compression**
  - Any sequence of TickRecords can be replayed exactly, and their Press capsules can be used for space‑efficient archival.

**Pass 01 – functions / operations**

- TICK_RECORD(τ, state_before, state_after) → TickRecord.
- TICK_HASH(parentHash, TickRecord) → tickHash.

**Pass 01 – build‑plan hooks**

- Build plan must:
  - Specify exact field order and integer encodings for TickRecord.
  - Define which observables are included in the Press capsule under each profile.

**Status after Pass 01**

- **Status**: **Partial** (schema fields and invariants fixed; field ranges and example instances to be added later).

---

### I‑7 — Global Parameter Calibration & Profiles

**Pre‑pass status**

- Many parameters (r, c, D★, SC, k, MDL weights, SLP thresholds, NAP quotas, etc.) exist but there is no set of named parameter profiles.

**Pass 01 – decisions & clarifications**

- Profiles are treated as **fully pinned tuples of integers and small rationals**.
- At minimum we define three profile ids: dev_low_res, matrix_demo_default, nested_sim_dense.

**Pass 01 – features & capabilities**

- **Feature F‑PROF‑1 – Profile Registry**
  - A table mapping profileId → full parameter set, covering UMX, SLP, Loom, Press, NAP.

**Pass 01 – functions / operations**

- LOAD_PROFILE(profileId) → parameter tuple.

**Pass 01 – build‑plan hooks**

- Build plan must include a concrete parameter table for each profile.

**Status after Pass 01**

- **Status**: **Open → Partial** (profile ids and registry concept in place; actual values to be pinned via experiments and Math Compendium guidance).

---

### I‑8 — Merge → Propagate → Resolve Phasing (SLP)

**Pre‑pass status**

- Docs describe each tick as Merge, Propagate, Resolve; current implementation exposes a monolithic tickOnce().

**Pass 01 – decisions & clarifications**

- We treat the three phases as **logical partitions of the lattice update**:
  - Merge: apply Gate writes, gather residuals.
  - Propagate: perform flux / neighbour updates.
  - Resolve: commit new state and residuals.

**Pass 01 – features & capabilities**

- **Feature F‑SLP‑PHASE‑1 – Phase‑Partitioned Tick**
  - Internal three‑step tick with optional debug exposure.

**Pass 01 – build‑plan hooks**

- Build plan must show the sequence Merge → Propagate → Resolve and how it interacts with sub‑ticks and NAP tick phases.

**Status after Pass 01**

- **Status**: **Open → Partial** (phases clarified; further work to pin exact equations per phase).

---

### I‑9 — Structural Inertia & Residual Norm Behaviour

**Pre‑pass status**

- Lattice is said to “seek minimal |R|” and behave diffusive, but no explicit inequality is given for residual norm behaviour.

**Pass 01 – decisions & clarifications (math)**

1. **Residual norm definition**
   - For the base field, define:
     - R(τ) = Σ_edges |S[u] − S[v]|.
   - S[u] are integer state values at nodes; edges are undirected or directed pairs.

2. **Monotonicity design goal**
   - In absence of new Gate writes, for standard profiles, R(τ) is required **not to systematically increase** over long runs.
   - More concretely: over any window of T ticks with no external writes, the average residual
     - (1/T) Σ_{k=0}^{T−1} R(τ + k)
     must be non‑increasing once the system has passed an initial transient.

3. **Link to Lyapunov energy**
   - There exists an energy function E_t similar to a quadratic form over state differences, such that E_{t+1} ≤ E_t in absence of new inputs.
   - Residual norm R(τ) is bounded above by a monotone function of E_t (e.g. via inequalities between ℓ1 and ℓ2 norms), so decreasing E_t implies that large residuals become rarer.

**Pass 01 – features & capabilities**

- **Feature F‑RES‑1 – Residual Norm Monitor**
  - Per‑tick computation of R(τ) and optional logging.

- **Capability C‑RES‑1 – Diffusive Relaxation**
  - For fixed inputs, the lattice tends to reduce residuals over time.

**Pass 01 – functions / operations**

- RESIDUAL_NORM(state) → R.
- RESIDUAL_TRACE(state over window) → sequence of R values.

**Pass 01 – build‑plan hooks**

- Build plan must specify test scenarios (random seeds, fixed profiles) that empirically verify R(τ) behaviour, and treat these as part of golden proofs.

**Status after Pass 01**

- **Status**: **Partial** (norm and qualitative monotonicity pinned; quantitative bounds left for later passes).

---

### I‑10 — Anchor‑in‑Layer Rule Formalisation

**Pre‑pass status**

- Residual layers must be anchored to base‑layer nodes; no formal anchor map schema exists.

**Pass 01 – decisions & clarifications**

- Anchor Map is a deterministic mapping from each residual entry to a base anchor index.
- For v1, we adopt a **1:1 mapping** for same‑size grids; more complex mappings are deferred.

**Pass 01 – features & capabilities**

- **Feature F‑ANCHOR‑1 – Anchor Map Table**
  - For each residual cell, stores a single base cell index.

**Pass 01 – functions / operations**

- ANCHOR_OF(residual_index) → base_index.

**Pass 01 – build‑plan hooks**

- Build plan must specify how Anchor Map is stored and updated under SLP changes.

**Status after Pass 01**

- **Status**: **Partial** (v1 mapping rule fixed; multi‑resolutions to be handled later).

---

### I‑11 — No‑Free‑Copy / Reuse‑Constraints Interface

**Pre‑pass status**

- Docs assert “no free lunch” for copies; Gate supports set vs add but with no normative rule.

**Pass 01 – decisions & clarifications**

- Define a **reuse discipline**:
  - Default mode is add; set is only allowed during initialisation or explicit structural events.
  - When set is used, either:
    - the prior content is accounted as residual, or
    - the change is logged as destruction/creation with corresponding budget entries.

**Pass 01 – features & capabilities**

- **Feature F‑REUSE‑1 – Write Mode Tracker**
  - Per‑write flags indicating add vs set and a reason code.

**Pass 01 – functions / operations**

- VALIDATE_WRITE_MODE(mode, context) → allowed / forbidden.

**Pass 01 – build‑plan hooks**

- Build plan must specify which operations are allowed to use set mode, and how this ties into budget/quota accounting (I‑20, I‑25).

**Status after Pass 01**

- **Status**: **Partial** (policy clarified; numeric budget coupling to be finalised).

---

### I‑12 — Determinism Edge Cases (Overflow & Parallelism)

**Pre‑pass status**

- Specs forbid wrap‑around and hardware‑dependent rounding but do not explicitly ban overflow or define allowed parallelisation.

**Pass 01 – decisions & clarifications (math)**

1. **Safe integer range**
   - Each state field x has a defined safe range [x_min, x_max] per profile.
   - All update rules are required to keep x within this range under expected workloads.

2. **Overflow semantics**
   - Overflow is **forbidden** in normative v1.x: any arithmetic that would exceed [x_min, x_max] is defined as a hard failure in spec.

3. **Parallelism constraint**
   - Any parallel implementation must produce exactly the same result as the canonical single‑threaded edge order.
   - Canonical order is defined as a deterministic traversal of nodes/edges (e.g. lexicographic by (layer, gridIndex)).

**Pass 01 – features & capabilities**

- **Feature F‑DET‑1 – Determinism Contract**
  - Explicit declaration of range and traversal order.

**Pass 01 – functions / operations**

- SAFE_ADD(x, y) with pre‑check against [x_min, x_max].

**Pass 01 – build‑plan hooks**

- Build plan must include range analysis or empirical tests proving no overflow under chosen profiles.

**Status after Pass 01**

- **Status**: **Partial** (contract defined; proofs/tests to be supplied).

---

### I‑13 — Sub‑Tick Semantics (Loom‑Driven Substeps)

**Pre‑pass status**

- Loom/NAP can request sub‑ticks; docs require batching invariance but do not formalise it.

**Pass 01 – decisions & clarifications (math)**

- Sub‑ticks are defined as **multiple applications of the same update rule T** with scaled inputs:
  - A macro tick with integrated input I is equivalent to M sub‑ticks each with input I/M (rounded appropriately) if the update rule is linear in inputs over that interval.
- For non‑linear cases, sub‑tick semantics are restricted to profiles where such splitting preserves invariants to within a specified tolerance.

**Pass 01 – features & capabilities**

- **Feature F‑SUBTICK‑1 – Sub‑Tick Mapper**
  - Maps a physical time step to a number of logical sub‑ticks and input splits.

**Pass 01 – build‑plan hooks**

- Build plan must specify which profiles support sub‑ticks and how input scaling is implemented on paper.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑14 — Concrete NAP API Surface (Beyond nap.js Envelope)

**Pre‑pass status**

- Complement Doc I calls for a more explicit NAP API; current surface is minimal.

**Pass 01 – decisions & clarifications**

- For Pass 01 we only pin the **logical operations** NAP must support from UMX’s perspective:
  - ENQUEUE_ENVELOPE, DEQUEUE_ENVELOPE, INSPECT_STATUS, SET_PROFILE, REGISTER_TICK_HOOK.

**Pass 01 – features & capabilities**

- **Feature F‑NAP‑API‑1 – Logical NAP Operation Set**.

**Pass 01 – build‑plan hooks**

- Build plan must place these operations around the two‑phase UMX tick (I‑21).

**Status after Pass 01**

- **Status**: **Open → Partial** (logical set defined; full schema and state machine are for later passes).

---

### I‑15 — Reversibility Window Parameters

**Pre‑pass status**

- Reversible windows are mentioned conceptually; concrete parameters (window size, checkpoint spacing) are not fixed.

**Pass 01 – decisions & clarifications (math)**

1. **Window definition**
   - A reversibility window W is defined by two tick indices (τ_start, τ_end) such that for any τ in this interval, the system can reconstruct the full state by starting from a checkpoint C_k with τ_k ≤ τ_start and replaying logged events.

2. **Checkpoint spacing**
   - Baseline checkpoint spacing Δ* is chosen via the cost‑optimal formula:
     - Δ* = floor(√(2 c_p / c_T)) where c_p is checkpoint cost and c_T is per‑tick simulation cost.

3. **Discard policy**
   - Once a window expires (τ > τ_end + margin), older checkpoints and events may be discarded subject to budget constraints and profile policies.

**Pass 01 – features & capabilities**

- **Feature F‑REV‑1 – Reversibility Window Profile**
  - Per profile, defines window length, margin, and Δ*.

**Pass 01 – functions / operations**

- COMPUTE_DELTA_STAR(c_p, c_T) → Δ*.
- DEFINE_WINDOW(profile) → (τ_start, τ_end) rules.

**Pass 01 – build‑plan hooks**

- Build plan must state the default reversibility window for each profile and how it interacts with U‑ledger storage limits (I‑19, I‑20).

**Status after Pass 01**

- **Status**: **Partial** (formulas fixed; concrete values per profile to follow).

---

### I‑16 — Mapping Between NAP’s c and UMX’s c

**Pre‑pass status**

- There are multiple notions of c (capacity, cost, coupling) across NAP and UMX; mapping between them is underspecified.

**Pass 01 – decisions & clarifications (math)**

- We treat c as a **capacity vector** with components:
  - c_UMX: capacity per UMX node/edge (e.g. max flux).
  - c_NAP: capacity per nest/channel.
- Nest continuity requires that the aggregate of c_UMX at the interface equals the effective c_NAP to within a tolerance τ_c.
- For stacked layers, c propagates via deterministic aggregation (sum or weighted sum) defined per profile.

**Pass 01 – features & capabilities**

- **Feature F‑C‑MAP‑1 – Capacity Mapping Rules**.

**Pass 01 – functions / operations**

- MAP_C_UMX_TO_NAP(local capacities) → channel capacities.

**Pass 01 – build‑plan hooks**

- Build plan must define the mapping formula for each profile and ensure budget checks use the mapped c consistently.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑17 — MDL Consensus ↔ UMX MDL (Unification)

**Pre‑pass status**

- MDL is used both for Press compression and UMX topology; the relationship is not fully unified.

**Pass 01 – decisions & clarifications (math)**

- We require that UMX’s L_total is a **refinement** of Press’s MDL cost L for topology‑related structures:
  - For any encoding of topology via Press, there exists a mapping between UMX’s per‑edge and per‑anchor MDL contributions and Press’s segment‑level MDL contributions.
- In practice, this means that Press’s cost function is treated as an upper bound on the cost of representing topology and that UMX’s L_total is calibrated so that repeated Press encoding of UMX snapshots shows consistent trends: structures with lower L_total should compress to shorter Press capsules (within noise).

**Pass 01 – features & capabilities**

- **Feature F‑MDL‑CONS‑1 – Cross‑Pillar MDL Calibration**.

**Pass 01 – build‑plan hooks**

- Build plan must include calibration tests where UMX topologies with different L_total values are encoded with Press and compared.

**Status after Pass 01**

- **Status**: **Partial** (conceptual unification established; precise calibration procedure to be detailed later).

---

### I‑18 — Commit Manifest Schema & SEAL Semantics

**Pre‑pass status**

- Commit manifest and SEAL semantics are outlined but not fully schema‑fied.

**Pass 01 – decisions & clarifications**

- For this pass, we only fix that the commit manifest is a table of integer‑indexed records keyed by a run id and contains:
  - Profile id, config hash, initial seed, series of TickHashes, and final root hashes for relevant pillars.
- SEAL is a bit or small enum indicating whether the run is closed (no further ticks allowed) and whether all required checks passed.

**Status after Pass 01**

- **Status**: **Open → Partial**.

---

### I‑19 — U‑Ledger Storage & Universal Integer Indexing

**Pre‑pass status**

- U‑Ledger is mentioned; Complement Doc I proposes docs and schemas but does not fully fix the indexing scheme.

**Pass 01 – decisions & clarifications (math)**

1. **Index space**
   - Each ledger entry is indexed by a tuple of integers:
     - (runId, τ, nodeId, layerId, eventType, eventIndex).
   - A universal ordering is defined as lexicographic over this tuple.

2. **Ledger invariants**
   - Ledger is append‑only; all entries respect the universal ordering.
   - Each entry includes a hash that chains back to the previous entry within the run.

**Pass 01 – features & capabilities**

- **Feature F‑LEDGER‑1 – Universal Ledger Indexing**.

**Pass 01 – functions / operations**

- LEDGER_APPEND(tuple, payload) → new ledger entry with updated hash.

**Pass 01 – build‑plan hooks**

- Build plan must specify concrete integer ranges for runId, τ, nodeId, etc., per profile, and show where ledger entries are created in the tick.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑20 — Quotas & Budget‑Drift Policies

**Pre‑pass status**

- Complement Doc I defines Budget Profiles (per‑node quotas, μ‑drift tolerance τ, reaction types) but leaves thresholds open.

**Pass 01 – decisions & clarifications**

- We tie budget drift to the global continuity principle:
  - The sum of certain conserved quantities (e.g. mass, probability, token counts) should remain within a small band over time.
- Budget profiles specify:
  - Per‑tick hard quotas (Q_msg, Q_bytes, Q_mu).
  - A drift band [−τ_mu, +τ_mu] over a window; exceeding it triggers specified reactions.

**Pass 01 – features & capabilities**

- **Feature F‑BUDGET‑1 – Budget Profile Table**.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑21 — Two‑Phase Tick Hooks for UMX

**Pre‑pass status**

- NAP uses a two‑phase tick (compute → sync); UMX exposes only tickOnce().

**Pass 01 – decisions & clarifications**

- Define Phase 1 (compute) as one or more applications of the lattice update T with Gate inputs fixed for that logical tick.
- Define Phase 2 (sync) as:
  - NAP message exchange,
  - SEAL updates,
  - ledger commits,
  - increment of global logical time τ.
- The core invariant: reordering operations **within** a phase must not change the outcome; phases must execute in order.

**Pass 01 – features & capabilities**

- **Feature F‑PHASE‑TICK‑1 – Two‑Phase Tick Contract**.

**Pass 01 – build‑plan hooks**

- Build plan must show the full loop: for each logical tick, run Phase 1 then Phase 2, and where Loom sub‑ticks and skip decisions fit.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑22 — Summary Packet Schema for Stacked Sims

**Pre‑pass status**

- Legacy reports define Village/Town/City summary vectors (counts, means, variances, production, synergy, event counts), but there is no canonical Summary Packet v1 schema.

**Pass 01 – decisions & clarifications**

- Summary Packet is defined as a fixed‑shape vector of integers and small rationals encoding:
  - N (count),
  - means and variances of key fields,
  - aggregated production vectors over a tick window,
  - synergy scores,
  - event counts,
  - explicit tick window size.

**Pass 01 – features & capabilities**

- **Feature F‑SUM‑1 – Cross‑Layer Summary Packet**.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑23 — ε‑Layer Profile & Scaling Factor R

**Pre‑pass status**

- Sub‑Planck stacking uses integer residuals scaled by R; R values and max residual depth are not pinned.

**Pass 01 – decisions & clarifications (math)**

- An ε‑layer profile is defined by:
  - scaling factor R (e.g. 10³, 10⁶),
  - max residual depth D_res,
  - folding rules: when |residual| ≥ R or depth ≥ D_res, residuals must be folded back into base layer.
- Folding is defined as pure integer operations: e.g. base ← base + floor(residual / R); residual ← residual mod R.

**Pass 01 – features & capabilities**

- **Feature F‑EPS‑1 – ε‑Layer Profile Table**.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑24 — Over‑Coupling Detection & Resonance Guards

**Pre‑pass status**

- Over‑coupling and resonance are mentioned; no explicit guard rules.

**Pass 01 – decisions & clarifications**

- Over‑coupling is flagged when coupling coefficients exceed profile‑defined bounds or when empirical measurements of E_t show oscillatory or divergent behaviour.

**Pass 01 – features & capabilities**

- **Feature F‑RES‑GUARD‑1 – Over‑Coupling Monitor**.

**Status after Pass 01**

- **Status**: **Open → Partial**.

---

### I‑25 — Integer vs Float Budget Discipline (Cross‑Pillar)

**Pre‑pass status**

- Cross‑pillar use of integers vs floats is not fully disciplined.

**Pass 01 – decisions & clarifications (math)**

- All core conserved quantities are represented as integers.
- Any floating‑point use (e.g. in diagnostics) must be derived from integer states and never fed back into core dynamics.

**Pass 01 – features & capabilities**

- **Feature F‑INT‑DISC‑1 – Integer Core Discipline**.

**Status after Pass 01**

- **Status**: **Partial**.

---

### I‑26 — Relational NAP Profile (Cadence & Permissions)

**Pre‑pass status**

- Relational NAP profiles for cadence and permissions are not fully spelled out.

**Pass 01 – decisions & clarifications**

- This pass notes only that profiles must specify:
  - Which nodes are allowed to initiate nests,
  - Cadence for communication over each nest type,
  - Permissions for read/write of summary packets.

**Status after Pass 01**

- **Status**: **Open** (intentionally left light for later passes).

---

### I‑27 — Nesting Profile & Tick Ratios

**Pre‑pass status**

- Nesting profile and tick ratios (Village/Town/City etc.) are not fully pinned.

**Pass 01 – decisions & clarifications (math)**

- Tick ratios k_VT, k_TC, etc. are defined as positive integers:
  - One Town tick equals k_VT Village ticks.
  - One City tick equals k_TC Town ticks.
- Nesting profiles specify:
  - Which layer emits summary packets at which multiple of its local tick.
  - How Nest Continuity constraints (e.g. μ_upper = μ_lower) are enforced via summary packets.

**Pass 01 – features & capabilities**

- **Feature F‑NEST‑1 – Nesting Profile Table**.

**Status after Pass 01**

- **Status**: **Partial**.

---

## 3. Global Maps (Pass 01)

These are skeletons for later consolidation; Pass 01 only populates them lightly.

### 3.1 Feature / Capability Catalogue (Pass 01 extract)

This pass identified and named the following feature families (non‑exhaustive):

- F‑MDL‑1 – MDL Topology Evaluator (I‑1).
- F‑MDL‑2 – Greedy MDL Topology Optimiser (I‑1).
- F‑SLP‑1 – Structural Plasticity Overlay (I‑2).
- F‑LAY‑1 – Layered UMX Envelope (I‑3).
- F‑NODE‑1 – Node Manifest Table (I‑4).
- F‑NAP‑BP‑1 – Bus Load Meter (I‑5).
- F‑TR‑1 – TickRecord v1 Schema (I‑6).
- F‑PROF‑1 – Profile Registry (I‑7).
- F‑SLP‑PHASE‑1 – Phase‑Partitioned Tick (I‑8).
- F‑RES‑1 – Residual Norm Monitor (I‑9).
- F‑ANCHOR‑1 – Anchor Map Table (I‑10).
- F‑REUSE‑1 – Write Mode Tracker (I‑11).
- F‑DET‑1 – Determinism Contract (I‑12).
- F‑SUBTICK‑1 – Sub‑Tick Mapper (I‑13).
- F‑NAP‑API‑1 – Logical NAP Operation Set (I‑14).
- F‑REV‑1 – Reversibility Window Profile (I‑15).
- F‑C‑MAP‑1 – Capacity Mapping Rules (I‑16).
- F‑MDL‑CONS‑1 – Cross‑Pillar MDL Calibration (I‑17).
- F‑LEDGER‑1 – Universal Ledger Indexing (I‑19).
- F‑BUDGET‑1 – Budget Profile Table (I‑20).
- F‑PHASE‑TICK‑1 – Two‑Phase Tick Contract (I‑21).
- F‑SUM‑1 – Cross‑Layer Summary Packet (I‑22).
- F‑EPS‑1 – ε‑Layer Profile Table (I‑23).
- F‑RES‑GUARD‑1 – Over‑Coupling Monitor (I‑24).
- F‑INT‑DISC‑1 – Integer Core Discipline (I‑25).
- F‑NEST‑1 – Nesting Profile Table (I‑27).

Later passes will expand this catalogue with more detailed descriptions and cross‑references.

### 3.2 Function & Operation Map (Pass 01 extract)

Pass 01 also pinned a set of paper‑level functions:

- MDL_EVAL, MDL_DELTA, MDL_GREEDY_PASS.
- GROW_EDGES, PRUNE_EDGES, UPDATE_USAGE, RUN_PLASTICITY_PASS.
- LAYER_FILTER, LAYER_COST.
- MANIFEST_LOOKUP, FIELD_OFFSET.
- BUS_LOAD, GATE_THROTTLE_POLICY.
- TICK_RECORD, TICK_HASH.
- RESIDUAL_NORM, RESIDUAL_TRACE.
- ANCHOR_OF.
- VALIDATE_WRITE_MODE.
- SAFE_ADD.
- SUBTICK_MAPPER (conceptual).
- COMPUTE_DELTA_STAR.
- MAP_C_UMX_TO_NAP.
- LEDGER_APPEND.

These will form the backbone of the UMX build plan’s operation table.

### 3.3 Build Plan Spine (Pass 01 sketch)

**Modules touched in Pass 01**

- UMX Core Lattice
  - Residual norm definition and behaviour (I‑9).
  - Determinism and integer ranges (I‑12, I‑25).

- UMX Topology & SLP
  - MDL objective and greedy optimisation (I‑1, I‑17).
  - Structural plasticity operation set (I‑2).
  - Multi‑layer policy (I‑3).
  - Anchor map (I‑10).
  - ε‑layer profiles (I‑23).

- NAP / Loom / Press Interop
  - TickRecord v1 and hash chain (I‑6, I‑19).
  - Reversibility windows and checkpoint spacing (I‑15).
  - Sub‑tick semantics and skip alignment (I‑13).

- Budgeting & Profiles
  - Global parameter profiles (I‑7).
  - Quotas and drift policies (I‑20).
  - Integer‑only discipline and write modes (I‑11, I‑25).

- Nesting
  - Summary packets (I‑22).
  - Nesting profiles and tick ratios (I‑27).

Later passes will flesh this spine out into a fully enumerated, profile‑indexed build plan suitable to hand to implementers.

### Source: `umx_gap_closure_build_plan_pass_02_2025_11_16.md` (verbatim)

# Universal Matrix Pillar — Gap Closure & Build Plan (Pass 02)

> **Scope of this pass**  
> This document takes the gap families from **Complement Doc I — Gap Closure & Profile Specs (UMX + SLP + NAP v1.x)** and pushes them toward **concrete, implementable v1.x specs** using:
>
> - Universal Matrix Pillar Spec v1 (UMX core)
> - Complement Docs A–D (+A1) — topology, nodes, anchors, SLP
> - Complement Doc E — invariants & layout
> - Complement Doc F — LLP → SLP temporal behaviour
> - Complement Doc G — NAP integration
> - Complement Doc H — Legacy NAP / nesting / stress
> - Universal Matrix Pillar — Topology Substrate & Conservation Engine (report)
> - Aether Math Compendium (for MDL, Loom, Press, ledger, and cross-pillar invariants)
>
> The goal is **math-first, paper-runnable specs** that can later be wrapped in JS for the offline Matrix demo, without changing the underlying mathematics.

---

## 0. Pass 02 Metadata

- **Date**: 2025-11-16 (Pass 02)
- **Pillar**: Universal Matrix (UMX + SLP + NAP)
- **Target**: v1.x "Matrix JS + Gate" offline demo, spec-ready for devs
- **Style constraints**:
  - System is **entirely maths**; code is an implementation wrapper.
  - Specs must be executable on paper in principle.
  - Deterministic, integer-first, reversible where promised.

Pass 02 does **not** rewrite Complement Doc I. Instead it:

1. Gives a **coverage table** of all gap families (I-1 → I-27) with Pass 02 status.  
2. For a selected set of **high-leverage families**, it:
   - tightens the **math definitions**,
   - pins down **spec artefacts** (file names / tables / schemas), and
   - states **explicit dev tasks** for the Matrix JS v1 demo.

Later passes can extend this further; the outputs here are already suitable as a build-plan skeleton.

---

## 1. Gap Family Coverage (Pass 02)

Status codes used:

- **SR-V1** = Spec-ready for v1.x (Matrix JS can be implemented from this doc set).
- **PC** = Partially closed (math and intent are clear, but some ergonomics / tuning left for later pass).
- **DEF** = Deferred (no new work in this pass; rely on Complement Doc I only).

| #  | Gap Family (from Complement Doc I)                                           | Pass 02 Status | Notes (Pass 02) |
|----|-------------------------------------------------------------------------------|----------------|-----------------|
| I-1  | MDL / Description-Length Objective (Topology & SLP)                          | SR-V1          | Adopt a concrete MDL objective L_total aligned with Press’ MDL; supply exact term list and update rule. |
| I-2  | SLP APIs & Data Structures                                                   | SR-V1 (core)   | Freeze core state structs and tick/update interfaces used by the demo; advanced APIs left as PC. |
| I-3  | Multi-Layer UMX                                                              | PC             | Clarify layer indexing, PFNA coordinates, and basic stacking invariants; some ergonomics deferred. |
| I-4  | UMX Node Manifest & Actor Slots                                              | SR-V1          | Lock in manifest fields, actor-slot semantics, and minimal profiles needed for Matrix JS. |
| I-5  | NAP Bus Backpressure & Flow-Control Hooks                                    | PC             | State boundary contract and minimal hooks in UMX/SLP; load/shedding policies deferred. |
| I-6  | Loom/Press Interop (beyond hash + P-deltas)                                 | PC             | Define canonical TickRecord and how Press/Loom see UMX states; performance modes deferred. |
| I-7  | Global Parameter Calibration & Profiles                                      | DEF            | Still largely profiling/ops; no new math in this pass. |
| I-8  | Merge → Propagate → Resolve Phasing                                          | SR-V1          | Freeze deterministic three-phase tick order and admissible sub-step structure. |
| I-9  | Structural Inertia & Residual Norm Behaviour                                | PC             | Tie SLP’s inertia terms to Compendium’s Lyapunov-style energy; detailed tuning deferred. |
| I-10 | Anchor-in-Layer Rule Formalisation                                           | SR-V1          | Fix anchor selection rule and allowed re-anchoring moves per tick. |
| I-11 | No-Free-Copy / Reuse-Constraints Interface                                   | SR-V1          | Turn high-level “no free copy” into precise ledger and token constraints. |
| I-12 | Determinism Edge Cases (Overflow & Parallelism)                              | SR-V1          | Adopt F.6 constraints explicitly as UMX/SLP invariant barriers. |
| I-13 | Sub-Tick Semantics (Loom-Driven Substeps)                                   | PC             | Minimal contract written (tick vs sub-tick); full Loom integration later. |
| I-14 | Concrete JS NAP API (Beyond nap.js Envelope)                                | SR-V1          | Document minimal message types, fields, and handshake needed for Matrix JS. |
| I-15 | Reversibility Window Parameters                                             | PC             | Formalise window definition and invariants; concrete window lengths left configurable. |
| I-16 | Mapping Between NAP’s c and UMX’s c                                         | SR-V1          | Pin a simple, exact mapping (shared c, integer cadence). |
| I-17 | MDL Consensus ↔ UMX MDL (Unification)                                       | PC             | Conceptual equivalence stated; full proof-quality unification later. |
| I-18 | Commit Manifest Schema & SEAL Semantics                                     | SR-V1          | Freeze the manifest fields, hash & seal semantics, and failure modes. |
| I-19 | U-Ledger Storage & Universal Integer Indexing                               | SR-V1          | Define ledger key-space, integer-only layout, and indexing scheme. |
| I-20 | Quotas & Budget-Drift Policies                                              | PC             | Specify local rules and detection; global policies deferred. |
| I-21 | Two-Phase Tick Hooks for UMX                                                | SR-V1          | Provide exact pre/post hook semantics around a UMX tick. |
| I-22 | Summary Packet Schema for Stacked Sims                                      | SR-V1          | Nail the shape of summary packets emitted from nested sims. |
| I-23 | ε-Layer Profile & Scaling Factor R                                          | PC             | Define base formulas; leave concrete parameter presets for future tuning. |
| I-24 | Over-Coupling Detection & Resonance Guards                                  | PC             | Provide diagnostic inequalities and trigger conditions; mitigation strategies later. |
| I-25 | Integer vs Float Budget Discipline (Cross-Pillar)                           | SR-V1          | Promote integer-only ledger discipline and float use only as derived views. |
| I-26 | Relational NAP Profile (Cadence & Permissions)                              | PC             | Clarify relational structure (who can send what, when); policy tables later. |
| I-27 | Nesting Profile & Tick Ratios                                               | SR-V1          | Formalise tick-ratio relationships between layers and show how they are configured.

---

## 2. Detailed Gap Closures & Spec Hooks (Pass 02)

Below, only gap families with **new concrete decisions** in this pass. Others remain as in Complement Doc I.

Each section follows:

- **Normative v1 recap** (from Complement Doc I and source docs).  
- **Pass 02 decisions** (added detail, maths, and file-level spec artefacts).  
- **Dev notes (Matrix JS)** — how a JS implementation should wrap the math.

---

### I-1 — MDL / Description-Length Objective (Topology & SLP)

#### Normative v1 recap

Complement Doc I states that both UMX and SLP choose anchors and edges to minimise description length, with:

- A scalar **L_total** over per-node anchor choices and candidate edges.  
- Terms for:
  - coding cost for node/edge parameters (bit-length proxy allowed),
  - L1 distance penalty over PFNA anchors,
  - movement penalty for re-anchoring,
  - degree penalty per node.
- A deterministic greedy update rule:
  - evaluate candidate changes in a fixed hashed order,  
  - accept any with ΔL_total < 0.

#### Pass 02 decisions

**(1) Decompose L_total explicitly.**

For any UMX snapshot S with node set V and edge set E, define:

- L_topology(S): description-length of the graph structure over PFNA coordinates.  
- L_fields(S): description-length of per-node fields that SLP cares about (capacities, tags, etc.).  
- L_residual(S): description-length of residuals (difference between current state and a simple baseline model).  

We set:

- **L_total(S) = L_topology(S) + L_fields(S) + L_residual(S)**.

Each term must itself be decomposable into **model bits + residual bits**, matching the Press-style MDL form (model + residual, with optional library reuse). For v1.x we only need a **simple coding proxy**:

- **Coding cost proxy**: bit-length of integer parameters using a simple prefix-free code approximation, which on paper can be treated as:
  - cost(n) ≈ 1 + ⌊log2(1 + |n|)⌋ for a signed integer n.

**(2) Topology and movement penalties.**

For each node i with anchor a_i (PFNA coordinate) and degree deg(i):

- Distance penalty: proportional to L1 distance between anchor and node’s “natural” position (PFNA coordinate derived from system configuration).  
- Degree penalty: proportional to deg(i).

Let:

- d_i = L1 distance for node i’s anchor,
- m_i = an indicator for whether node i moved anchor at this tick,
- deg(i) = degree of node i.

Then:

- L_topology(S) includes a term:
  - Σ_i [ λ_d · d_i + λ_deg · deg(i) + λ_move · m_i ],
  - with λ_d, λ_deg, λ_move ≥ 0.

These λ parameters are documented in **`spec/md/mdl_parameters_v1.md`** and can be tuned, but the form is fixed.

**(3) Greedy update rule in fixed order.**

For each tick, define a fixed ordering over candidate moves (changing anchors and edges). For v1.x, we:

- Compute a hash over (node_id, move_type, tick_index) to give each move a deterministic rank.
- Iterate candidates in strictly increasing hash order.
- For each candidate move M:
  - Evaluate ΔL_total = L_total(S_after M) − L_total(S_before M).
  - Accept M if ΔL_total < 0 (strict improvement), otherwise reject.

No stochasticity, no backtracking. This yields a locally MDL-improving evolution.

**(4) Spec artefacts (Pass 02 update).**

- `spec/md/mdl_objective_v1.md` —
  - Defines L_total and its decomposition (L_topology, L_fields, L_residual).
  - Lists all penalty terms and λ parameters for v1.x.
  - Describes the deterministic greedy update rule and the hashing scheme used for ordering.
- `spec/md/mdl_parameters_v1.md` —
  - Records default λ_d, λ_deg, λ_move values used in the Matrix JS demo.
  - Clarifies these are tuning knobs, not changes to the objective form.

#### Dev notes (Matrix JS)

- Implement L_total as a pure function from an in-memory UMX snapshot to a scalar integer or fixed-point score.
- Implement a separate **analysis-only pass** at first:
  - Take a frozen snapshot, enumerate candidate anchor/edge moves, and report ΔL_total for each.
- Only once MDL behaviour is validated should this be wired into SLP’s plasticity path as a live decision-maker.

---

### I-2 — SLP APIs & Data Structures

#### Normative v1 recap

Complement Doc I wants a clear set of SLP APIs and data structures, making explicit:

- The shape of SLP state (per-node, per-edge, and global fields).  
- The tick/update interfaces (inputs from UMX, outputs back to topology).  
- How plasticity passes are invoked (e.g., sub-phases within a tick).

#### Pass 02 decisions

We define the **minimal core** for v1.x. This is enough to:

- Run a deterministic tick loop with SLP present but simple.  
- Allow local plasticity (edge-strength and anchor choices) guided by MDL.

**(1) Core SLP state structs.**

Per node i:

- `capacity_i` — integer capacity / slots for edges.  
- `bias_i` — integer bias / preference score (e.g., from Codex Eterna later; fixed for v1.x demo).  
- `layer_i` — the UMX layer index this node belongs to.  
- `flags_i` — bitfield for roles (boundary, core, frozen, etc.).

Per edge (i, j):

- `w_ij` — integer weight, symmetric or directed depending on config.  
- `age_ij` — integer age in ticks (time since creation or last modification).  
- `flags_ij` — bitfield for edge properties (structural, provisional, etc.).

Global SLP:

- `theta_prune` — integer threshold below which an edge may be pruned.  
- `theta_grow` — integer threshold above which a new edge may be formed or strengthened.  
- `lambda_age` — decay parameter for ageing behaviour.  
- Reference to **MDL evaluator** (from I-1).

**(2) Tick-level interface.**

Each UMX tick τ is allowed to call SLP through three canonical entry points (tying into I-8):

1. `slp_merge(umx_state, slp_state)` —
   - Reads UMX events and maps them into SLP’s internal counters / triggers.
2. `slp_propagate(slp_state)` —
   - Runs local update rules (e.g., ageing, threshold checks) independent of UMX topology changes.
3. `slp_resolve(umx_state, slp_state, mdl)` —
   - Uses MDL to decide which edges to create/prune and which anchors to adjust.

For v1.x these can all be **purely sequential**; no parallelism is allowed in the canonical spec.

**(3) Spec artefacts (Pass 02 update).**

- `spec/md/slp_state_core_v1.md` — detailed layout of per-node, per-edge, and global SLP fields.  
- `spec/md/slp_tick_api_v1.md` — defines the three functions above and their allowed side effects.  
- `spec/md/slp_plasticity_rules_v1.md` — enumerates the conditions under which edges/anchors change.

#### Dev notes (Matrix JS)

- Represent nodes and edges in simple JS arrays or maps, mirroring these integer fields exactly.
- The JS functions implementing `slp_merge / slp_propagate / slp_resolve` must act as thin wrappers over the math; no hidden randomness, no side effects outside the snapshot passed to them.

---

### I-3 — Multi-Layer UMX

#### Normative v1 recap

The multi-layer UMX structure is a stack of layers (0, 1, 2, …), each a topology with its own PFNA coordinate system and node types, but sharing global invariants.

Complement Doc I wants:

- A clear enumeration of layers and their roles (e.g., physical, logical, narrative).  
- How edges and anchors can cross or reference adjacent layers.  
- How MDL and conservation apply across layers.

#### Pass 02 decisions

**(1) Layer indexing and PFNA coordinates.**

- Layers are indexed by integers ℓ ∈ ℤ, with ℓ = 0 as the base UMX layer for the Matrix demo.  
- Each layer has its own PFNA coordinate system, but all are embedded into a shared **global index space** for MDL, to keep L_total coherent.

We define a mapping:

- `embed(ℓ, p)` → global PFNA coordinate P, where p is the layer-local PFNA coordinate.

For v1.x, embed can be as simple as concatenating layer index and coordinate components in a fixed-width integer encoding.

**(2) Cross-layer constraints.**

- Nodes may **anchor to layer-local PFNA** only; cross-layer references are via edges whose endpoints exist in potentially different layers.  
- An **inter-layer edge** (i, j) is allowed only if |ℓ(i) − ℓ(j)| ≤ 1 (adjacent layers).

**(3) Multi-layer conservation.**

- The conservation invariants (no token creation/destruction) apply **per global ledger**, not per layer.  
- However, there may be layer-local views where tokens accumulate or deplete; these must still sum correctly globally.

**(4) Spec artefacts.**

- `spec/md/umx_layers_v1.md` — defines layer indices, roles, and allowed edge types.
- `spec/md/umx_cross_layer_edges_v1.md` — states adjacency constraint |ℓ(i) − ℓ(j)| ≤ 1 and any additional rules.

#### Dev notes (Matrix JS)

- Store layer index as an integer field on each node.
- When constructing or updating edges, enforce the cross-layer adjacency rule in code and treat any violation as a hard error (debug assert in dev builds).

---

### I-4 — UMX Node Manifest & Actor Slots

#### Normative v1 recap

Complement Doc I calls for a **node manifest** describing all node types, their actor slots, capacities, and invariants, so the topology can be reasoned about as a structured graph rather than arbitrary nodes.

#### Pass 02 decisions

**(1) Node manifest schema (v1.x).**

Each node type T is described by a manifest entry with fields:

- `type_id` — short string or integer label.  
- `layer` — default layer index for nodes of this type.  
- `capacity_edges` — max degree (hard integer cap).  
- `capacity_slots` — number of actor slots on the node.  
- `roles` — bitfield (boundary, hub, sink, source, ledger, etc.).  
- `default_flags` — initial `flags_i` for nodes of this type.

Actor slots are uniform:

- Each node at runtime has an array of length `capacity_slots`, where each entry is either empty or holds an actor reference (ID or index into an actor table).

**(2) Actor-slot invariants.**

- No slot may hold more than one actor.  
- Actors cannot be duplicated across slots; any duplication must be represented as separate actors with ledger-backed creation events.  
- Actor movement between nodes must be represented as a **transfer** that preserves any conserved quantities (e.g., tokens, budget) via the ledger.

**(3) Spec artefacts.**

- `spec/md/node_manifest_v1.md` — table of node types and their manifest entries.  
- `spec/md/actor_slots_v1.md` — defines the actor-slot structure and invariants.

#### Dev notes (Matrix JS)

- Define a static manifest object in the JS demo that mirrors `node_manifest_v1.md` exactly.
- When constructing nodes, consult the manifest to set `layer`, `capacity_edges`, `capacity_slots`, and `default_flags`.

---

### I-5 — NAP Bus Backpressure & Flow-Control Hooks

#### Normative v1 recap

Complement Doc I wants hooks between UMX/SLP and NAP so that:

- UMX does not assume an infinite-rate message bus.  
- NAP can signal congestion, failures, or rate limits.  
- The combined system avoids double-counting or leakage.

#### Pass 02 decisions

**(1) Backpressure signals.**

NAP exposes two minimal signals to UMX/SLP per tick:

- `bus_ok` — boolean flag: messages are flowing within quota.  
- `bus_congested` — boolean flag: NAP near or beyond quota.

At most one of these may be true per tick; if both false, treat as unknown and default to conservative behaviour (no new large writes).

**(2) UMX/SLP behaviour under congestion.**

When `bus_congested` is true:

- UMX must **not emit** new large bursts of messages that depend on immediate confirmation.  
- SLP may continue internal plasticity, but should treat any external I/O as delayed.

If `bus_ok` is true, normal messaging may proceed.

**(3) Spec artefacts.**

- `spec/md/nap_bus_contract_v1.md` — defines `bus_ok`, `bus_congested`, and required UMX/SLP reactions.

#### Dev notes (Matrix JS)

- In the offline demo, `bus_ok` can be hard-coded to true and `bus_congested` false, but the hooks must still exist.
- Later, when a real NAP implementation is wired in, these flags become live inputs.

---

### I-6 — Loom/Press Interop (beyond hash + P-deltas)

#### Normative v1 recap

The earlier specs mention Loom/Press only via hashes and P-deltas, but Complement Doc I wants a more explicit contract: what exactly is captured, how often, and with what guarantees.

#### Pass 02 decisions

**(1) TickRecord structure.**

Define a canonical **TickRecord** per UMX tick τ:

- `tau` — tick index (integer).  
- `state_hash` — hash of the full UMX+SLP state at tick τ (using a fixed hash function, e.g., 256-bit).  
- `delta_P` — any compressed representation of state changes, suitable for Press.  
- `events` — list of high-level events (optional for v1.x demo).  
- `ledger_head` — pointer to the current U-Ledger entry.

Loom/Press see the world only via this TickRecord stream.

**(2) Checkpoint cadence.**

- Loom may take a checkpoint at any tick, but for v1.x we recommend a simple strategy (e.g., every N ticks or when a significant event occurs).  
- Each checkpoint consists of a TickRecord plus any additional Press metadata (model parameters, etc.).

**(3) Spec artefacts.**

- `spec/md/tick_record_v1.md` — defines TickRecord fields and encoding.  
- `spec/md/loom_press_contract_v1.md` — explains how Loom/Press subscribe to tick records and what invariants they can assume (e.g., determinism, no skipped ticks unless explicitly annotated as a skip-ahead).

#### Dev notes (Matrix JS)

- For the demo, implement TickRecord as a simple JS object emitted once per tick and optionally logged.
- Hashing can be stubbed with a deterministic pseudo-hash for small examples, but the field and semantics must match the spec.

---

### I-8 — Merge → Propagate → Resolve Phasing

#### Normative v1 recap

Complement Doc F sharpens the three-phase structure for SLP/LLP-driven behaviour:

1. **Merge** — integrate incoming deltas and messages.  
2. **Propagate** — run internal dynamics, local updates, and decay.  
3. **Resolve** — apply discrete decisions (create/prune edges, commit changes).

#### Pass 02 decisions

**(1) Frozen phase ordering.**

Per UMX tick τ, the canonical SLP phases are:

1. `slp_merge`  
2. `slp_propagate`  
3. `slp_resolve`

No other order is permitted in the canonical spec. Any implementation must show equivalence if reorderings or batching are attempted.

**(2) Single-commit semantics.**

- All structural changes (edge creation/pruning, anchor moves) are **committed atomically at the end of Resolve**.  
- Merge and Propagate are not allowed to change the visible topology; they only adjust SLP’s internal state.

**(3) Spec artefacts.**

- `spec/md/slp_phasing_v1.md` — defines the phases and what each may and may not do.

#### Dev notes (Matrix JS)

- Implement the tick loop so that all SLP work is explicitly nested inside these three calls in order.
- For debugging, it helps to log which phase produced which change to SLP state.

---

### I-9 — Structural Inertia & Residual Norm Behaviour

#### Normative v1 recap

Structural inertia is the tendency of the topology not to thrash unnecessarily. Complement Doc I and F reference residual norms and Lyapunov-style energy decreases from the Aether Math Compendium.

#### Pass 02 decisions

**(1) Introduce a simple energy-like score E_struct.**

- E_struct aggregates penalties for rapid or large structural changes (e.g., many edges toggled in short time).

Example form:

- E_struct(τ) = α · (#edges_changed at τ) + β · (sum of |Δw_ij| over changed edges) + γ · (#anchor_moves at τ).

Where α, β, γ ≥ 0 are parameters. This is not a physical energy but a control measure guiding policies that avoid unnecessary churn.

**(2) Inertia guard.**

- If E_struct(τ) exceeds a certain threshold, SLP may suppress additional changes in that tick (e.g., only accept the most beneficial moves according to MDL).  
- This threshold and policy are recorded in `mdl_parameters_v1.md` as recommended defaults.

**(3) Spec artefacts.**

- `spec/md/structural_inertia_v1.md` — defines E_struct and the guard behaviour.

#### Dev notes (Matrix JS)

- For the demo, implement the guard as a simple limit on the number of topology mutations per tick (e.g., max K changes), chosen deterministically (by ordering candidates via hash + MDL gain).

---

### I-10 — Anchor-in-Layer Rule Formalisation

#### Normative v1 recap

Complement Doc F wants a precise rule for how nodes choose and change anchors within a layer, to avoid ambiguous behaviour.

#### Pass 02 decisions

**(1) Anchor selection rule.**

For each node i in layer ℓ:

- Candidate anchors are drawn from a finite set A_i(ℓ) of PFNA coordinates allowed for that node type.  
- At each tick, SLP may consider a small set of candidate moves (e.g., stay put, move to one neighbouring anchor, or to a manifest-defined “preferred” anchor).

**(2) Move acceptance rule.**

- For each candidate anchor a′ ∈ A_i(ℓ), compute ΔL_total if node i were moved to a′.  
- Among all candidates, select moves with ΔL_total < 0, ordered by the global hash ordering; accept them until the structural inertia guard (I-9) says to stop.

**(3) Spec artefacts.**

- `spec/md/anchor_in_layer_v1.md` — defines A_i(ℓ), the candidate move set, and the acceptance rule.

#### Dev notes (Matrix JS)

- For v1.x, A_i(ℓ) can be a tiny neighbourhood such as the current anchor plus its immediate PFNA neighbours; this keeps the candidate set small and manageable.

---

### I-11 — No-Free-Copy / Reuse-Constraints Interface

#### Normative v1 recap

Complement Doc I emphasises that the system must avoid “free copies” of conserved quantities (tokens, mass, budget). Any apparent duplication must be backed by a ledger entry that shows where the quantity came from.

#### Pass 02 decisions

**(1) Ledger-backed creation only.**

- Any introduction of a conserved quantity (token, budget unit) must be recorded as a **mint event** in the U-Ledger, with:
  - source (e.g., external reservoir or initial condition),
  - amount (integer),
  - timestamp / tick index,
  - justification tag.

**(2) No local duplication without ledger transfer.**

- Local code must not create new tokens by copying fields. Transfers between nodes must be expressed as integer subtractions and additions that sum to zero on each transaction.

**(3) Spec artefacts.**

- `spec/md/no_free_copy_v1.md` — formalises these constraints and ties them to U-Ledger entries.

#### Dev notes (Matrix JS)

- In JS, disallow direct increment of balances except via a single transfer function that writes corresponding ledger entries.

---

### I-12 — Determinism Edge Cases (Overflow & Parallelism)

#### Normative v1 recap

Complement Doc F spells out constraints around overflow, rounding, and parallel execution.

#### Pass 02 decisions

- **Single rounding rule**: any division or scaling uses truncation toward zero; no alternative rounding allowed.  
- **No wrap-around**: values must be checked and clamped or errors raised before any integer overflow would occur; wrap-around is forbidden.  
- **Frozen update schedule**: the canonical spec is single-threaded; any parallel implementation must prove that observable results are identical.

These are adopted as hard protocol barriers for UMX/SLP.

**Spec artefacts.**

- `spec/md/determinism_edge_cases_v1.md` — codifies these rules for all arithmetic.

#### Dev notes (Matrix JS)

- Use JS bigints or careful integer emulation where necessary to avoid silent overflow.

---

### I-13 — Sub-Tick Semantics (Loom-Driven Substeps)

#### Normative v1 recap

Loom introduces sub-ticks when performing skip-ahead or local replay windows. Complement Doc I flags that UMX needs a clear stance on whether and how these sub-ticks are visible to SLP/UMX.

#### Pass 02 decisions

- For v1.x **Matrix JS**, sub-ticks are an **internal concern of Loom only**. UMX and SLP see only integral ticks τ.  
- Loom may simulate intermediate states between ticks for verification, but must not expose these as official UMX ticks.

**Spec artefacts.**

- `spec/md/sub_tick_semantics_v1.md` — declares that UMX/SLP operate on whole ticks only; Loom is responsible for making any sub-tick work invisible at the UMX interface.

#### Dev notes (Matrix JS)

- For the offline demo, Loom can be omitted or stubbed; the spec simply reserves the sub-tick space for future work.

---

### I-14 — Concrete JS NAP API (Beyond nap.js Envelope)

#### Normative v1 recap

Complement Doc G describes how NAP wraps, routes, and commits messages, but Complement Doc I wants a concrete JS-level API that Matrix JS can call without ambiguity.

#### Pass 02 decisions

**(1) Minimal NAP operations.**

For the Matrix JS demo we define three core NAP actions (in math terms, but intended to map to JS functions):

1. `enqueue(outgoing_message)` — propose a message to be sent.  
2. `poll_committed()` — retrieve a list of messages that have been fully committed.  
3. `get_bus_status()` — read `bus_ok` / `bus_congested` flags (I-5).

Messages have a minimal envelope with fields:

- `id` — unique integer or hash.  
- `src_layer`, `dst_layer` — layer indices.  
- `src_node`, `dst_node` — node identifiers.  
- `payload` — finite integer or small structured payload.  
- `budget_delta` — integer change in budget or tokens implied by this message.

**(2) Commit semantics.**

- Messages are only applied to UMX/SLP once they appear in `poll_committed()` returns.  
- Until then, they may be present in an internal queue but must not affect topology or ledger.

**Spec artefacts.**

- `spec/nap/nap_api_core_v1.md` — defines these operations, message fields, and commit semantics.

#### Dev notes (Matrix JS)

- Implement these operations as pure functions over an in-memory queue and a `committed` list.
- For the offline demo, you can commit messages immediately, but the two-step structure must remain visible.

---

### I-15 — Reversibility Window Parameters

#### Normative v1 recap

Complement Doc G describes a **reversibility window**: a finite number of recent ticks that can be rolled back if needed, as long as certain conditions hold (no external irreversibility beyond that window).

#### Pass 02 decisions

**(1) Window definition.**

Let **K_rev** be a positive integer. At any tick τ, the reversibility window is the set of ticks {τ − K_rev + 1, …, τ} (clipped to ≥ 0 for early ticks).

- Within this window, the system must retain enough information (state snapshots or invertible deltas) to reconstruct any past state exactly.  
- Outside this window, only committed, non-reversible history remains.

**(2) Invariants.**

- No irreversible external side-effect (e.g., real-world I/O, non-reversible compression) may depend on states within the window that could still be rolled back.  
- NAP must mark any message that crosses the reversibility boundary.

**Spec artefacts.**

- `spec/nap/reversibility_window_v1.md` — documents K_rev, storage requirements, and invariant conditions.

#### Dev notes (Matrix JS)

- For the demo, K_rev can be small (e.g., 3 or 5), and implementation can simply store copies of recent snapshots in memory.

---

### I-16 — Mapping Between NAP’s c and UMX’s c

#### Normative v1 recap

Complement Doc G introduces cadence parameters c in both NAP and UMX (e.g., ticks per second or per wall-time).

#### Pass 02 decisions

- For v1.x, we **identify** these cadences: c_nap = c_umx = c, a shared integer defining ticks per unit wall-time (or an abstract time unit if wall-time is ignored).
- This eliminates skew between NAP’s notion of tick cadence and UMX’s; all scheduling is expressed in integer multiples of c.

**Spec artefact.**

- `spec/nap/umx_cadence_mapping_v1.md` — states c_nap = c_umx and describes any future extension where they might differ and require explicit mapping.

#### Dev notes (Matrix JS)

- In the offline demo, you can treat c as a nominal parameter; the main requirement is consistent use in all timing-related code.

---

### I-17 — MDL Consensus ↔ UMX MDL (Unification)

#### Normative v1 recap

Complement Doc G envisions consensus or coordination layers also using MDL-like objectives; Complement Doc I wants these to be **mathematically compatible** with the UMX MDL defined in I-1.

#### Pass 02 decisions

- We adopt the following principle: **any MDL used by NAP/consensus must be representable as an additive extension of L_total** from I-1.  
- That is, consensus MDL adds extra terms L_consensus on top of L_total but does not introduce a conflicting objective.

So the unified MDL is:

- L_unified = L_total + L_consensus,

with L_consensus capturing, for example, cost of disagreement, communication overhead, or reconfiguration.

**Spec artefact.**

- `spec/md/mdl_unification_v1.md` — formalises this additive relationship and identifies which terms belong to L_total vs L_consensus.

#### Dev notes (Matrix JS)

- For the offline demo, you can set L_consensus = 0 (no separate consensus MDL) but structure the code so adding extra terms later is straightforward.

---

### I-18 — Commit Manifest Schema & SEAL Semantics

#### Normative v1 recap

Complement Doc G and the Math Compendium describe a **commit manifest** whose hashes and metadata allow deterministic replay and tamper detection.

#### Pass 02 decisions

**(1) Commit manifest fields.**

Each commit manifest entry M_k for tick τ_k includes:

- `tick` — tick index.  
- `state_hash` — hash of the fully committed state.  
- `parent_hash` — hash of the previous manifest entry.  
- `delta_hash` — hash of compressed deltas (if any).  
- `ledger_head` — pointer to the corresponding U-Ledger entry.  
- `meta` — small metadata dictionary (e.g., version, tag).

**(2) SEAL semantics.**

- A manifest is **SEALED** when all fields are filled and hashes computed; after sealing, it is immutable.  
- Any attempt to change state after sealing requires a new manifest entry; previous entries remain as history.

**Spec artefacts.**

- `spec/nap/commit_manifest_v1.md` — defines the manifest structure and SEAL semantics.

#### Dev notes (Matrix JS)

- Implement the manifest as an append-only list; each entry’s `parent_hash` ties it into a simple hash chain.

---

### I-19 — U-Ledger Storage & Universal Integer Indexing

#### Normative v1 recap

The U-Ledger is an integer-only, append-only ledger capturing all conserved-quantity transactions and significant events.

#### Pass 02 decisions

**(1) Key-space for entries.**

- Each ledger entry has a unique **universal integer key** k ∈ ℕ, starting at 0 and incrementing by 1 per entry.  
- The ledger is thus an ordered sequence (L_0, L_1, …) with no gaps.

**(2) Entry structure.**

Each L_k includes:

- `k` — index.  
- `tick` — tick at which this entry is applied.  
- `type` — event type (mint, transfer, burn, checkpoint, etc.).  
- `amount` — signed integer amount for the event.  
- `from`, `to` — identifiers (node IDs, external reservoir, etc.).  
- `hash` — hash over the entry’s contents and possibly other context.

All numeric fields are integers; any floating-point views are derived only for display, never stored as primary state.

**Spec artefacts.**

- `spec/ledger/u_ledger_v1.md` — defines the ledger entry schema and key-space.

#### Dev notes (Matrix JS)

- Represent the ledger as an array of objects in JS; k can simply be the array index.

---

### I-20 — Quotas & Budget-Drift Policies

#### Normative v1 recap

Complement Doc G (and legacy experiments) discuss quotas and budget drift; Complement Doc I wants explicit policies.

#### Pass 02 decisions

**(1) Per-tick quota.**

- Each node or component has a per-tick quota Q_max for how much budget it can consume or emit.

**(2) Drift detection.**

- Define total budget B_total as the sum over all nodes plus any external reservoirs.  
- Any change in B_total that is not accounted for by a ledger entry is a **drift violation**.

**(3) Spec artefacts.**

- `spec/ledger/budget_policies_v1.md` — defines Q_max and drift-detection rules.

#### Dev notes (Matrix JS)

- Implement runtime assertions that check budget before and after each tick; if B_total changes without a ledger entry, flag an error.

---

### I-21 — Two-Phase Tick Hooks for UMX

#### Normative v1 recap

Complement Doc G wants explicit pre- and post-tick hooks so NAP and other systems can tie into the UMX tick lifecycle.

#### Pass 02 decisions

We define two canonical hooks:

1. **Pre-tick hook** H_pre(τ):
   - Called before any UMX state update for tick τ.  
   - Allowed actions: ingest committed NAP messages for this tick, apply external inputs.
2. **Post-tick hook** H_post(τ):
   - Called after UMX and SLP have completed tick τ.  
   - Allowed actions: emit summary packets, ledger entries, and commit manifests.

These hooks form the boundary where NAP and Loom/Press interact with UMX.

**Spec artefacts.**

- `spec/md/umx_tick_hooks_v1.md` — defines H_pre, H_post, and their allowed operations.

#### Dev notes (Matrix JS)

- Implement tick as:
  - H_pre(τ) → UMX+SLP_tick(τ) → H_post(τ), with no work outside this sandwich.

---

### I-22 — Summary Packet Schema for Stacked Sims

#### Normative v1 recap

Complement Doc H describes summary packets emitted from nested simulations; Complement Doc I wants a stable schema.

#### Pass 02 decisions

Each summary packet O for a nested sim layer includes:

- `layer` — layer index.  
- `tick` — tick index at which the summary is produced.  
- `N` — number of agents or nodes summarised.  
- `means` — vector of mean values for key observables.  
- `variances` — vector of variances for those observables.  
- `events` — list of notable events (optional in v1.x demo).

**Spec artefacts.**

- `spec/nap/summary_packet_v1.md` — defines this schema and how often summaries must be emitted.

#### Dev notes (Matrix JS)

- For the demo, you can emit summary packets every fixed number of ticks or when H_post is called, and log them for inspection.

---

### I-23 — ε-Layer Profile & Scaling Factor R

#### Normative v1 recap

Complement Doc H and the Math Compendium discuss ε-layers and scaling factors R for multi-scale sims; Complement Doc I wants explicit formulas for how these factors are applied.

#### Pass 02 decisions

- Define ε-layer as a layer that runs at a finer temporal resolution or with scaled-down parameters; scaling factor R relates its tick rate or parameters to the parent layer.

For v1.x we set:

- If layer ℓ is an ε-layer of layer ℓ−1 with factor R, then:
  - tick_ℓ advances R times per one tick of layer ℓ−1.  
  - key observables are scaled appropriately when summarised back to the parent.

**Spec artefacts.**

- `spec/md/epsilon_layers_v1.md` — documents R and how it affects tick ratios and summary scaling.

#### Dev notes (Matrix JS)

- You can simulate ε-layers by running multiple inner loops per outer tick in JS.

---

### I-24 — Over-Coupling Detection & Resonance Guards

#### Normative v1 recap

Complement Doc H mentions over-coupling and resonance between layers or components; Complement Doc I calls for guards.

#### Pass 02 decisions

- We define over-coupling heuristically as situations where feedback loops cause oscillations or divergence in certain observables.

Example guard:

- If an observable O oscillates with increasing amplitude over a sliding window of W ticks, flag potential over-coupling.  
- Quantitatively: track variance or amplitude of O; if it grows monotonically over several windows beyond a threshold, trigger a guard event.

**Spec artefacts.**

- `spec/md/over_coupling_guards_v1.md` — specifies observables to monitor and inequalities that define “too much coupling”.

#### Dev notes (Matrix JS)

- For the demo, you can implement one or two simple guards and log when they trigger; no automatic mitigation is required yet.

---

### I-25 — Integer vs Float Budget Discipline (Cross-Pillar)

#### Normative v1 recap

Complement Doc H emphasises a discipline where integers represent conserved quantities and floats are only used for derived or display values.

#### Pass 02 decisions

- All **source-of-truth** budget, token, and mass values are stored as integers.  
- Any floating-point quantity is derived from these integers and their context (e.g., ratios, averages) but never fed back into the ledger as a primary state.

**Spec artefacts.**

- `spec/ledger/integer_budget_discipline_v1.md` — states this rule explicitly and lists which fields must be integer.

#### Dev notes (Matrix JS)

- In JS, use integers for balances and only convert to floats when needed for visualisation.

---

### I-26 — Relational NAP Profile (Cadence & Permissions)

#### Normative v1 recap

Complement Doc H outlines relational profiles: who can talk to whom, how often, and with what permissions.

#### Pass 02 decisions

- For v1.x, we define a minimal relational profile:
  - Each layer has a whitelist of other layers it can send messages to.  
  - Each relation (layer A → layer B) has:
    - a max messages-per-tick quota,  
    - a permission bit indicating whether budget transfers are allowed.

**Spec artefacts.**

- `spec/nap/relational_profile_v1.md` — table listing allowed relations and associated quotas/permissions.

#### Dev notes (Matrix JS)

- Implement these as configuration tables and check them before enqueuing any NAP message.

---

### I-27 — Nesting Profile & Tick Ratios

#### Normative v1 recap

Complement Doc H talks about nesting simulations and aligning tick ratios across layers.

#### Pass 02 decisions

- For each pair of nested layers (inner, outer), define an integer tick ratio k such that:
  - k inner ticks correspond to exactly 1 outer tick.

- These ratios must be recorded in a **nesting profile** so that Loom and NAP can reconcile time across layers.

**Spec artefacts.**

- `spec/md/nesting_profile_v1.md` — lists all nested layer pairs and their tick ratios.

#### Dev notes (Matrix JS)

- In your tick loop, implement nesting by running k inner ticks for every single outer tick, using the recorded ratios.

---

## 3. Summary of Pass 02 Outcomes

- Key MDL definitions (I-1) are now concrete enough to implement as a pure function and to use as the basis for SLP plasticity.  
- SLP’s core state and APIs (I-2, I-8–I-11) are frozen for the Matrix JS demo.  
- Determinism and ledger disciplines (I-11, I-12, I-19, I-25) are turned into explicit, enforceable constraints.  
- NAP integration (I-14–I-21, I-22–I-27) now has concrete schemas and hooks, suitable for a first offline integration.

Remaining work for later passes:

- Parameter calibration and profile-tuning (I-7, and the tuning aspects of I-9, I-20, I-23, I-24, I-26).  
- Deeper MDL unification proofs and performance-focused Loom/Press integration.

This Pass 02 document is intended to be **hand-off ready**: a dev team can implement the Matrix JS demo by following the spec artefacts referenced above and treating this doc as the gap-closure index for v1.x.

### Source: `umx_gap_closure_pass_3_bridge_gate_cross_cut_2025_11_16.md` (verbatim)

---
pass: 3
pillar: Universal Matrix (UMX)
focus: Gap Closure & Build Plan, Bridge/Gate Cross-Cut
status: draft
created: 2025-11-16
---

# UMX Gap Closure — Pass 3 (Bridge / Gate Cross-Cut)

This pass mines the **Bridge / Trinity Gate** and **Aether testbed** material for anything that:

1. **Directly fills** a gap family from **Complement Doc I — Gap Closure & Profile Specs (UMX + SLP + NAP v1.x)**.
2. **Tightens the normative v1 target** (e.g. gives concrete numbers, tables, test patterns).
3. **Suggests a build-plan pattern** we should mirror for the Universal Matrix pillar.

> Standing rule for this doc: **no new magic**. Every claim here must be something you could point back to in the existing bridge / gate / testbed packs or in Complement Doc I itself. Where we extrapolate, we say so explicitly.

---

## 0. Inputs for Pass 3

Pass 3 consumes **all earlier UMX material** (UMX Spec v1 + Complement Docs A–H + Complement Doc I + NAP integration docs + Aether Math Compendium) and adds the following **Bridge/Gate-focused inputs**:

- **Core Bridge Math & Representation**  
  Used for:
  - Two-phase tick scheduling (compute vs sync).  
  - The role of the Gate as a **translation + membrane** in front of Loom/Press/UMX.  
  - The relationship between lattice/UMX state, external byte streams and NAP envelopes.

- **Triune / Trinity Gate Packs** (naming varies slightly across files, but all refer to the same gate stack):
  - `tbp_gate_implementation_spec_v_1.md` — concrete interfaces, schemas and invariants for the Gate implementation.  
  - `tbp_gate_verification_test_plan_v_1.md` — end-to-end acceptance and conformance tests for the Gate.  
  - `tbp_gate_golden_fixtures_pack_v_1.md` — golden input/output pairs and envelopes.  
  - `tbp_gate_operator_runbook_v_1.md` — how a human runs, inspects and recovers the Gate.  
  - `tbp_gate_development_roadmap_v_1.md` — phased build plan from prototype to hardened Gate.

- **Triune Bridge / Trinity Gate meta docs:**
  - `triune_bridge_gate_knowledge_gaps.md` — list of what was still missing for the Gate/Bridge itself.  
  - `trinity_gate_vs_math_compendium_coverage_report.md` — where the Gate is fully backed by math proofs vs still heuristic / TBD.  
  - `trinity_gate_tgp_focus_expansions.md` and `trinity_gate_older_reports_expansions.md` — additional narrative and feature-level detail for the Gate.

- **Universal Matrix Pillar cross-cut docs:**
  - `universal_matrix_pillar_spec_v_1.md` — how UMX currently exposes hooks to Gate, Loom, Press and NAP; includes JS-facing surface like `tickOnce`, ledger hooks, scene integration.
  - `umx_complement_doc_g_nap_integration.md` — particularly G4–G8 (MDL unification, commit manifest, U-Ledger, quotas/drift, two-phase ticks).  
  - `umx_complement_doc_i_gap_closure_profile_specs.md` — the index and v1 targets for gap families **I-1 … I-21** (plus later items under H).

- **Aether / Testbed spec snippets that already include Gate behaviours:**
  - Global modes + switches (canonical JSON, anchor, nonce, tick, budgets, translator pipeline) and their invariants.  
  - System-level acceptance criteria: MDL gain, determinism, idempotence, conservation, auditability.

This pass **does not** try to re-summarise all of the above. Instead, it:

- Selects the **gap families where Bridge/Gate is clearly relevant**.  
- Shows **what the Bridge/Gate material already commits us to** for UMX v1.  
- Proposes **specific UMX artefacts and build-plan steps** that mirror the Gate.

Where a gap family doesn’t materially move, we flag it as **“unchanged in Pass 3”**.

---

## 1. Gap Families Touched by Bridge / Gate

From Complement Doc I’s index, the following gap families are materially updated by Bridge/Gate input in this pass:

- **I-1 — MDL / Description-Length Objective (Topology & SLP)**  
- **I-2 — SLP APIs & Data Structures**  
- **I-4 — UMX Node Manifest & Actor Slots**  
- **I-5 — NAP Bus Backpressure & Flow-Control Hooks**  
- **I-6 — Loom/Press Interop (beyond hash + P-deltas)**  
- **I-7 — Global Parameter Calibration & Profiles**  
- **I-9 — Structural Inertia & Residual Norm Behaviour**  
- **I-11 — No-Free-Copy / Reuse-Constraints Interface**  
- **I-12 — Determinism Edge Cases (Overflow & Parallelism)**  
- **I-14 — Concrete JS NAP API (Beyond nap.js Envelope)**  
- **I-15 — Reversibility Window Parameters**  
- **I-16 — Mapping Between NAP’s c and UMX’s c**  
- **I-17 — MDL Consensus ↔ UMX MDL (Unification)**  
- **I-18 — Commit Manifest Schema & SEAL Semantics**  
- **I-19 — U-Ledger Storage & Universal Integer Indexing**  
- **I-20 — Quotas & Budget-Drift Policies**  
- **I-21 — Two-Phase Tick Hooks for UMX**  

The remaining gap families (I-3, I-8, I-10, I-13 and the H-derived ones beyond I-21) are **not contradicted** by Gate material, but Bridge/Gate doesn’t add enough new, UMX-specific content to warrant a normative change in this pass. They carry forward from Complement Doc I as-is.

---

## 2. Per-Gap Updates (Complement Doc I × Bridge / Gate)

Each subsection below uses the same template:

- **Baseline (from Complement Doc I):** what the gap is and what v1 said we need.  
- **Bridge / Gate evidence:** what we already did for the Gate that clearly applies to UMX.  
- **Pass-3 resolution:** how UMX v1 should behave, plus any new artefacts or build steps.

### 2.1 I-1 — MDL / Description-Length Objective (Topology & SLP)

**Baseline (Complement Doc I)**  
I-1 flagged that UMX/SLP talk about MDL-style learning and compression, but **do not pin down**:

- the exact **codelength functional** ℒ,  
- how ℒ decomposes over nodes / layers / edges,  
- what thresholds (τ, penalties) govern when a topology change is “worth it”.

**Bridge / Gate evidence**  
Across the Aether testbed and Occam/Press material, we already used a concrete MDL functional with:

- Canonical byte representation (canonical JSON, SHA-256 anchors).  
- Per-track MDL deltas: every time a new motif or rule is proposed, we check that **description length decreases by at least τ** before accepting it.  
- Global acceptance criteria in the test suite that require:  
  - “Any adaptive compression (Codex proposals) resulted in a net decrease in total description length by at least the threshold τ. There are no cases where an adopted motif made things worse. Criteria: All accepted motifs have L1 < L0 − τ as measured, and no regression in baseline sizes.”  
- UMX-specific conservation invariants, such as:  
  - “Conservation & Consistency: The global invariants (like total quantity conservation in Matrix/SLP, continuity of history in Loom) held true. Criteria: Net changes summed to zero where expected; any permitted skip-ahead was verified identical to explicit simulation.”

**Pass-3 resolution for UMX**  
For UMX v1, we adopt the following **MDL objective** for topology and SLP learning:

- **State representation for MDL:**
  - Each UMX tick produces a **canonical trace** of the form `T_t = canonical_json(trace_t)`, where `trace_t` contains:  
    - the list of active nodes and their local state,  
    - the active edges / bonds,  
    - any SLP “ley strength” values,  
    - residual / inertia metrics used for continuity checks.
- **Baseline codelength L₀:**
  - For a given configuration (graph + ley field + parameters), the baseline codelength L₀ is defined as the **Shannon-like code length** induced by the current model plus the residual needed to encode deviations.  
  - Practically: UMX can re-use the Press / Occam MDL machinery by feeding it UMX traces rather than generic byte streams.
- **Proposal ΔMDL:**
  - A topology change proposal (e.g. adding/removing an edge, adjusting weights, moving an anchor) is only accepted if, over a validation window W of ticks, the resulting **total description length** L₁ satisfies:  
    - L₁ ≤ L₀ − τ, for a globally configured τ ≥ 0.  
  - τ is part of the **UMX profile** (see I-7 below) and can vary by environment.
- **Separation of concerns:**
  - **UMX MDL** focuses on **structural** economy (graph, ley strengths, layering).  
  - **Codex Eterna / Press MDL** focuses on **compressing traces and external data**.  
  - In v1, UMX delegates the actual numerical MDL computation to the Press/CE stack, but its **accept/reject rules and thresholds are defined in the UMX profile**.

**New artefact:**

- `spec/md/umx_mdl_objective_v1.md`  
  - Defines:  
    - the structure of `trace_t`,  
    - how Press/CE is used to compute codelengths for UMX traces,  
    - the default window size W and threshold τ for UMX learning,  
    - how MDL results feed back into SLP growth/prune decisions.

UMX gap I-1 is **not fully “finished”** (we still need exact numeric τ defaults per profile), but after Pass 3 it is **constrained enough** to implement a working v1 learning loop driven by the same MDL logic already used in Gate / Press tests.

---

### 2.2 I-2 — SLP APIs & Data Structures

**Baseline (Complement Doc I)**  
I-2 noted that SLP is conceptually clear (synaptic ley over the matrix) but its **concrete APIs and data structures** were under-specified, especially:

- How SLP exposes **ley strengths**, growth/prune controls and metrics to other pillars.  
- How SLP state is serialised for **UMX snapshots**, Gate integration, and NAP commit manifests.

**Bridge / Gate evidence**  
The Gate and testbed material give us a pattern for **IR (intermediate representation)** that is both canonical and schema-driven:

- Translator builds a canonical IR:  
  - `IR = { schema: 'generic.v1', fields: [[k, v] ...] }` with keys sorted.  
- Field budgets and tick budgets are enforced at IR level.  
- Loom and Press rely on deterministic, canonical representations (no re-encoding drift) for hashing, sealing and MDL.

UMX Spec v1 also describes **UMX scenes** and node sets as JSON-like structures fed through the Gate, which implies a similar IR layer for matrix/SLP state.

**Pass-3 resolution for UMX**  
We adopt a **UMX SLP IR** that mirrors the Gate IR pattern:

- **Canonical SLP snapshot IR:**
  - At each tick t, SLP can emit a snapshot:
    ```json
    {
      "schema": "umx.slp.snapshot.v1",
      "tick": t,
      "nodes": [
        [node_id, layer_id, ley_state_vector],
        ...
      ],
      "edges": [
        [src_id, dst_id, ley_strength, flags],
        ...
      ],
      "metrics": {
        "total_ley": ...,   
        "avg_strength": ...,  
        "prune_candidates": [...],
        "growth_candidates": [...]
      }
    }
    ```
  - Keys are sorted, numeric fields are integer or fixed-point per the Math Compendium; no floats.
- **APIs:**  
  The UMX core exports SLP hooks in two directions:
  - **To Gate / NAP / external tools:**  
    - `UMX.exportSlpSnapshot(t)` → returns canonical IR as above.  
    - `UMX.applySlpPatch(patch)` → applies a set of changes proposed by Codex or an operator.  
  - **To internal UMX components:**  
    - `SLP.grow(edge_id, Δ)` / `SLP.prune(edge_id)` / `SLP.setLey(node_or_edge_id, value)`; these are math-level operations that the implementation maps to integer updates.

**New artefacts:**

- `spec/json/umx_slp_snapshot_v1.schema.json` — JSON Schema for the snapshot IR.  
- `spec/md/umx_slp_api_v1.md` — documents SLP’s public interface and invariants (e.g. conservation of total ley where applicable, bounds on strengths, deterministic tie-breaking).

This is enough to **wire SLP into Gate / NAP** for v1 builds while still leaving room for richer SLP behaviours in later passes.

---

### 2.3 I-4 — UMX Node Manifest & Actor Slots

**Baseline (Complement Doc I)**  
I-4 highlighted that UMX talks about **nodes, anchors, and actors**, but lacks:

- A precise **Node Manifest** schema.  
- A clear definition of **which “actor slots” exist per node** (e.g. compute, observe, translate) and how they are wired to other pillars.

**Bridge / Gate evidence**  
The Gate and testbed packs already define a pattern of **components with modes/switches** and clear operator-visible configuration fields, such as:

- Global run control (canonical JSON, anchor, nonce, tick, field budgets).  
- Translator switches (`SANITIZE`, IR builder `Tin`, output modes, privacy gates).  
- Loom, Press and NAP components with their own mode toggles and budgets.

UMX Spec v1 also describes UMX as a **scene** with configurable nodes, but the per-node manifest is implicit.

**Pass-3 resolution for UMX**  
We define a **UMX Node Manifest v1** that mirrors the Gate component style:

```json
{
  "schema": "umx.node.manifest.v1",
  "node_id": "umx://node/<uuid>",
  "layer_id": "L0" ,
  "anchors": {
    "topology_anchor": "sha256:...",   
    "slp_anchor": "sha256:..."        
  },
  "actor_slots": {
    "compute": {
      "enabled": true,
      "profile": "default",        
      "tick_budget": 1000
    },
    "observe": {
      "enabled": true,
      "fields": ["local_state", "ley", "residual"]
    },
    "translate": {
      "enabled": true,
      "ingress_schema": "umx.slp.snapshot.v1",
      "egress_schema": "umx.slp.snapshot.v1"
    }
  },
  "limits": {
    "max_degree": 64,
    "max_ley": 1024
  }
}
```

- **Actor slots** are **purely logical** in the spec: a human can carry them out on paper (compute next state, observe metrics, translate to/from IR).  
- The JS / Gate implementation simply wraps these operations, preserving the same inputs/outputs.

**New artefacts:**

- `spec/json/umx_node_manifest_v1.schema.json`  
- `spec/md/umx_node_and_actor_slots_v1.md` — narrative spec that ties Node Manifest fields to Matrix math (e.g. how `max_degree` and `max_ley` map to clamped integer ranges in the math compendium).

---

### 2.4 I-5 — NAP Bus Backpressure & Flow-Control Hooks

**Baseline (Complement Doc I)**  
I-5 recognised that NAP enforces quotas and backpressure, but UMX/SLP lacked **explicit hooks** to:

- react when NAP throttles or drops messages,  
- expose current bus pressure to simulations (e.g. slow down or degrade resolution),  
- document per-node and per-pillar budgets.

**Bridge / Gate evidence**  
In the Gate/testbed material, we already have **field budgets** and tick budgets, e.g.:

- `FIELD_BUDGET = 6` for translator fields, with explicit behaviour when the budget is exceeded (overflow flagged but payload not mutated).  
- Global “field budgets (ON)” mode where each component has a hard budget and clear failure behaviour.  
- NAP descriptions where quotas, drift and protocol-break flags are part of the integration story.

UMX Spec v1 also describes Gate → UMX hooks where events are **queued and ticked**, implying a natural place to honour NAP backpressure.

**Pass-3 resolution for UMX**  
For UMX v1, we define a **NAP bus contract** with the following elements:

1. **Budgets and counters per node:**
   - Each UMX node `i` has a **message budget** per tick `B_i` and a **byte budget** per tick `K_i`.  
   - NAP enforces these budgets and exposes the **actual usage** and **overflows** as part of the envelope metadata.

2. **UMX reaction semantics:**
   - If `usage_i ≤ B_i` and `bytes_i ≤ K_i`: UMX processes all envelopes normally.  
   - If budgets are exceeded but within a configured **soft tolerance** σ:  
     - UMX may **defer non-critical updates** (e.g. low-priority SLP learning) to the next tick.  
     - Core invariants (conservation, determinism) must still hold.  
   - If budgets exceed a **hard cap** (beyond tolerance):  
     - UMX **freezes topology learning** (I-1) for the affected node(s).  
     - Ledger records include a “budget breach” event so the operator can see exactly when and where it occurred.

3. **Exposure of bus pressure to UMX math:**
   - A per-node scalar `π_i(t)` (pressure) is defined as a deterministic function of recent budget utilisation, e.g.:
     - `π_i(t) = floor(100 * usage_i(t) / B_i)` (clamped 0–100).  
   - UMX is allowed to couple structural inertia (I-9) or learning rates to `π_i(t)` (e.g. high pressure → increase inertia or shrink learning window).

**New artefacts:**

- `spec/md/umx_nap_bus_contract_v1.md` — details budgets, tolerance bands (soft vs hard), and the mapping from NAP envelope metadata to `π_i(t)`.  
- `spec/json/umx_nap_envelope_extension_v1.schema.json` — adds fields such as `msg_budget`, `msg_used`, `byte_budget`, `bytes_used`, `pressure_score` to the base NAP envelope.

After Pass 3, I-5 has a concrete **math-compatible story**: budgets are simple integer counters, and UMX’s response is expressed as deterministic rules on those counters.

---

### 2.5 I-6 — Loom/Press Interop (Beyond Hash + P-deltas)

**Baseline (Complement Doc I)**  
I-6 observed that Loom/Press interop was mostly described at the **hash + P-delta** level, without specifying:

- how full UMX snapshots enter Press,  
- what Loom expects from UMX for **history continuity** checks,  
- how much of UMX state is actually compressed vs re-derived.

**Bridge / Gate evidence**  
The Aether testbed and Occam/Press experiments define a rich set of behaviours:

- Canonical JSON and anchors for every object.  
- APX-style layered packaging with `MANIFEST.json` plus `layers/...` payloads.  
- Clear distinction between **identity metadata** (names, hashes, sizes) and payload bytes.  
- Tests that verify both **lossless compression** and **auditability** via hash chains.

**Pass-3 resolution for UMX**  
We specialise Loom/Press interop for UMX as follows:

1. **UMX snapshot packaging:**
   - A UMX snapshot at tick t is packaged as an APX-like capsule:
     - `MANIFEST.json` includes:  
       - `component: "UMX"`,  
       - `tick: t`,  
       - `topology_anchor`, `slp_anchor`,  
       - optional `file_meta`-style details for environment context.  
     - `layers/topology.bin` holds the compressed adjacency + layer assignment.  
     - `layers/slp.bin` holds SLP ley strengths, residuals and metrics.  
   - The capsule is deterministically produced from UMX’s canonical IR (see I-2 and I-4), so a human could reconstruct it with paper math plus simple coding.

2. **Loom expectations:**
   - Loom expects that **successive snapshots** obey continuity:
     - The global sum of conserved quantities is unchanged except where explicit external inputs are declared.  
     - Residual norms stay within profile-specific bounds (I-9, updated below).  
   - Loom’s continuity checks operate entirely on the **manifest + anchors + residual metrics**, not on raw internal structure.

3. **Press expectations:**
   - Press compresses `topology.bin` and `slp.bin` using its existing modules.  
   - For MDL purposes (I-1), UMX uses Press codelengths as the cost of representing its state.

**New artefacts:**

- `spec/md/umx_loom_press_interop_v1.md` — defines exactly what goes into UMX capsules, how anchors are computed and how Loom/Press use them.  
- `spec/json/umx_snapshot_manifest_v1.schema.json` — MANIFEST schema specialised for UMX capsules.

---

### 2.6 I-7 — Global Parameter Calibration & Profiles

**Baseline (Complement Doc I)**  
I-7 pointed out that UMX had many tunable parameters (tick sizes, budgets, MDL thresholds, residual bounds, etc.) but lacked:

- a **profile system** (e.g. “sandbox”, “production”) with defaults,  
- a clear explanation of which parameters live where (UMX vs Gate vs NAP).

**Bridge / Gate evidence**  
The Gate/testbed packs already rely on **named modes and switches** with implied default values and test coverage. Examples include:

- Canonical JSON on/off (G0), anchor behaviour (G1), nonce / exactly-once semantics (G2).  
- Tick / epoch handling (G4).  
- Field budgets (G5) with a fixed integer budget and defined behaviour on overflow.  
- Translator/IO modes (T1, T2, T3…) with explicit defaults.

The Aether acceptance criteria also apply tolerances and thresholds (e.g. MDL threshold τ, drift tolerances, acceptance windows).

**Pass-3 resolution for UMX**  
We define a **UMX Profile v1** structure that collects all relevant parameters in one place:

```json
{
  "schema": "umx.profile.v1",
  "name": "sandbox",
  "tick": {
    "max_nodes": 1024,
    "max_degree": 64,
    "max_layers": 4
  },
  "mdl": {
    "tau": 8,
    "window_ticks": 32
  },
  "residual": {
    "max_norm": 4096,
    "warning_ratio": 0.75
  },
  "nap": {
    "msg_budget": 64,
    "byte_budget": 16384,
    "soft_tolerance": 0.8,
    "hard_tolerance": 1.0
  },
  "ledger": {
    "retention_ticks": 10000,
    "snapshot_interval": 100
  }
}
```

- Profiles are **static JSON blobs** that a human can edit without code; Matrix JS simply reads them and applies the parameters to the math engine.  
- The Bridge / Gate stack may contribute its own defaults, but UMX retains ownership of UMX-specific parameters.

**New artefact:**

- `spec/json/umx_profile_v1.schema.json` and one or more concrete profile instances (e.g. `profiles/umx_sandbox_profile.json`, `profiles/umx_prod_profile.json`).

---

### 2.7 I-9 — Structural Inertia & Residual Norm Behaviour

**Baseline (Complement Doc I)**  
I-9 described the need for a formalisation of:

- how **residuals** are computed in SLP/UMX (difference between desired and actual flows),  
- how **structural inertia** damps or amplifies changes,  
- thresholds for considering a configuration unstable.

**Bridge / Gate evidence**  
The Uroboros genesis and Aether math materials already define:

- Residual metrics for motion and continuity, with norms, bounds and clamping.  
- Conservation laws that use residuals to check whether “hidden instabilities” are creeping in.

The Aether acceptance criteria demand that **global invariants and continuity** are preserved, with explicit checks on sums and replay.

**Pass-3 resolution for UMX**  
UMX v1 adopts a residual/inertia scheme that mirrors the Uroboros math:

- **Residual per node / edge:**  
  - For each node i, define a residual vector `r_i(t)` capturing deviation from expected flow / degree.  
  - For each edge (i, j), define `r_ij(t)` as deviation from expected conserved flow along that bond.
- **Norm and bound:**  
  - Use an integer L1 or L2 norm `‖r_i(t)‖` and ensure:  
    - `‖r_i(t)‖ ≤ R_max` for all i,t under normal operation, where `R_max` is set by the profile (I-7).  
- **Structural inertia:**  
  - Introduce an integer inertia weight `γ_i` per node, such that **topology changes** are gated by residual behaviour:  
    - If residual norms stay low over a window W, allow more aggressive structural updates.  
    - If residual norms spike, freeze SLP growth/prune and possibly reduce NAP budgets.

**New artefact:**

- `spec/md/umx_residual_and_inertia_v1.md` — defines the exact formulas, invariants and default `R_max` vs profile.

---

### 2.8 I-11 — No-Free-Copy / Reuse-Constraints Interface

**Baseline (Complement Doc I)**  
I-11 demanded a clear **no-free-copy / reuse constraint** at the LLP→SLP boundary, i.e.:

- UMX/SLP must not silently clone information without paying the MDL cost.  
- There must be an interface to tell when a reuse is “legal” (e.g. referencing an existing pattern) vs an illicit free copy.

**Bridge / Gate evidence**  
The Aether packs already implement:

- **Anchors and nonces** to avoid double-counting or double-delivery.  
- Exactly-once semantics based on canonical JSON + hashing.  
- Test cases where duplicate messages are injected and must be recognised and neutralised.

**Pass-3 resolution for UMX**  
UMX adopts a **no-free-copy interface** that reuses anchors and ledger semantics:

- Every structural pattern (e.g. a frequently used subgraph or ley motif) has a **pattern anchor** computed from its canonical representation.  
- Reuse of a pattern elsewhere in the matrix must either:
  - **Reference the existing anchor**, in which case MDL sees it as a pointer with known cost, or  
  - **Create a new pattern with a new anchor**, paying the full MDL cost.
- The ledger records all pattern creation events, so external auditors can check that no unlogged copies appeared.

**New artefact:**

- `spec/md/umx_no_free_copy_interface_v1.md` — documents how anchors, MDL and ledger combine to enforce no-free-copy.

---

### 2.9 I-12 — Determinism Edge Cases (Overflow & Parallelism)

**Baseline (Complement Doc I)**  
I-12 noted the need to handle:

- Numeric overflows,  
- Parallelisation / interleaving of updates,  
- Any randomness or tie-breaking,

in a way that preserves **strict determinism**.

**Bridge / Gate evidence**  
The Aether test packs already insist that:

- All randomness is seeded once and then held fixed.  
- Canonical JSON and hashing ensure that the same inputs yield the same outputs.  
- Acceptance criteria include **deterministic replay** and **idempotence** across the entire system.

**Pass-3 resolution for UMX**  
UMX v1 reuses these rules explicitly:

- All UMX numeric operations are on **bounded integers** with explicit clamp functions.  
- Parallel updates are specified as if applied in a particular **canonical order** (e.g. sorted by node_id), even if the implementation uses parallel hardware internally.  
- Any randomness (e.g. for stochastic routing) must use a **global, seed-derived stream**; the UMX Node Manifest records the seed, and the ledger ensures it does not change mid-run.

**New artefact:**

- `spec/md/umx_determinism_and_parallelism_v1.md` — enumerates all edge cases, with explicit rules for overflow, ordering and randomisation.

---

### 2.10 I-14 — Concrete JS NAP API (Beyond nap.js Envelope)

**Baseline (Complement Doc I & G)**  
I-14 observed that the NAP envelope is described conceptually, but there is no concrete, JS-friendly API that:

- exposes envelope creation, signing, budgets and MDL metrics in a usable way,  
- links directly into UMX’s `tickOnce` / ledger / profile systems.

**Bridge / Gate evidence**  
The Gate implementation spec and testbed material already describe:

- NAP envelopes with fields like tick, node id, hashes, metrics, mode, signature.  
- Gate-side functions that **wrap** these envelopes for ingress/egress.  
- Modes and switches for security, sanitisation and budgets.

**Pass-3 resolution for UMX**  
We define a **UMX-facing NAP JS API** that is conceptually simple and math-backed:

- `createUmxNapEnvelope(umxSnapshot, profile, opts) → envelope`  
  - Takes a UMX snapshot IR plus profile-defined budgets and returns a fully formed envelope ready for NAP.  
- `applyUmxNapEnvelope(umxState, envelope) → newUmxState`  
  - Applies incoming updates in a deterministic way, respecting budgets and quotas (I-5, I-20).

The **envelope shape** is a direct lift from the NAP/Gate specs, with UMX-specific fields added for snapshot anchors and profile IDs.

**New artefact:**

- `spec/md/umx_nap_js_api_v1.md` — narrative, plus concrete function signatures for JS implementers.  
- `spec/json/umx_nap_envelope_v1.schema.json` — schema combining base NAP fields with UMX extensions.

---

### 2.11 I-15 — Reversibility Window Parameters

**Baseline (Complement Doc I & G)**  
I-15 called out the need to pin down:

- the **reversibility window** over which UMX/SLP/NAP can roll back,  
- what state is required to support that rollback,  
- when history becomes immutable.

**Bridge / Gate evidence**  
NAP + Gate discussions already assume:

- A commit / SEAL process where participants sign manifests, after which history is immutable.  
- Buffer windows and dedup windows for replay, which imply a maximum reversible span.

**Pass-3 resolution for UMX**  
UMX adopts a **two-tier reversibility model**:

1. **Pre-SEAL window:**  
   - Before a SEAL for tick t is finalised, UMX may **roll back up to W_pre ticks**, where W_pre is given by the profile (I-7).  
   - Rollback requires:
     - the UMX snapshot manifests and residual metrics for the affected ticks,  
     - the NAP envelopes that drove those updates.
2. **Post-SEAL window:**  
   - Once a SEAL is in place, UMX state for ticks ≤ t is **logically immutable**.  
   - Physical rollback is still possible in a lab context (by replaying from an earlier snapshot), but not considered part of the live protocol.

**New artefact:**

- `spec/md/umx_reversibility_windows_v1.md` — defines W_pre, its relationship to NAP buffers, and operator guidance on safe rollback.

---

### 2.12 I-16 — Mapping Between NAP’s c and UMX’s c

**Baseline (Complement Doc I & G)**  
I-16 noted that both NAP and UMX refer to a constant `c` (often the speed of light), but **do not specify** whether these are:

- the same constant,  
- different but related constants, or  
- just scale parameters with different roles.

**Bridge / Gate evidence**  
The Aether experiments and Trinity full systems proofs treat physical constants c, ħ, G as **global, shared constants** across pillars, with a single set of values.

**Pass-3 resolution for UMX**  
For v1, we treat **NAP’s c and UMX’s c as the same physical constant**, with the following implications:

- All timing and distance scales in UMX that depend on c must use the **same numeric value** as NAP (and as used in the Trinity/Aether proofs).  
- Any differences in behaviour (e.g. effective propagation speed in a simulation vs a NAP link) are expressed via additional **dimensionless scale factors**, not separate c values.

**New artefact:**

- `spec/md/umx_physical_constants_v1.md` — one source of truth for c, ħ, G and any derived constants used by UMX, Loom, Press, NAP and Gate.

---

### 2.13 I-17 — MDL Consensus ↔ UMX MDL (Unification)

**Baseline (Complement Doc G / I)**  
G4/I-17 asked for a short **MDL Unification doc** to clarify whether:

- NAP’s MDL for **transport-level consensus** and  
- UMX’s MDL for **topology-level learning**

are the same or different objectives.

**Bridge / Gate evidence**  
The Aether packs implicitly treat MDL as a **single conceptual barrier** (shortest faithful description wins), but with different **domains of application** (traces vs structure vs messages).

**Pass-3 resolution for UMX**  
We adopt the following split:

- There is a single **canonical codelength functional ℒ** defined at the system level (see 2.1).  
- Different subsystems (UMX, NAP, Press) apply ℒ to different **objects**:  
  - UMX applies ℒ to topology + SLP traces.  
  - NAP applies ℒ to message histories and peer behaviour.  
  - Press applies ℒ to raw byte streams.
- Consensus/learning logic always uses the **same sign convention and threshold semantics**:  
  - Proposals are only accepted if they reduce ℒ by at least a configured τ.  
  - τ may differ per subsystem but lives in the global profile.

**New artefact:**

- `spec/md/mdl_unification_umx_nap_v1.md` — a short doc explicitly stating these relationships and pointing to the detailed MDL specs for each subsystem.

After Pass 3, the MDL story is **consistent** across UMX and NAP; the remaining work is mostly numeric calibration.

---

### 2.14 I-18 — Commit Manifest Schema & SEAL Semantics

**Baseline (Complement Doc G / I)**  
G5/I-18 demanded a concrete **Commit Manifest v1 schema** with:

- fields (tick, participants, hash list, budgets),  
- signing rules,  
- how UMX TickLedger hashes plug in.

**Bridge / Gate evidence**  
The Aether and Press packs already define APX manifets and seal behaviours, including:

- `MANIFEST.json` with file names, sizes and hashes.  
- Canonical header hash and seal values that change on tamper.  
- Examples of how a single-bit flip in a payload or TOC entry alters root and seal.

**Pass-3 resolution for UMX**  
We define a **Commit Manifest v1** for UMX+NAP that mirrors APX but is tailored to ticks:

```json
{
  "schema": "umx.commit.manifest.v1",
  "tick": 12345,
  "participants": ["umx://node/A", "umx://node/B"],
  "snapshots": [
    {
      "component": "UMX",
      "anchor": "sha256:...",
      "role": "state"
    },
    {
      "component": "NAP",
      "anchor": "sha256:...",
      "role": "log"
    }
  ],
  "budgets": {
    "nap_msgs": 1024,
    "nap_bytes": 65536,
    "umx_nodes": 1024
  },
  "root_hash": "sha256:...",
  "seal": "ed25519:...",
  "signers": [
    {
      "id": "nap://peer/1",
      "signature": "ed25519:..."
    },
    {
      "id": "umx://coordinator",
      "signature": "ed25519:..."
    }
  ]
}
```

- UMX’s **TickLedger hash** is one of the snapshot anchors.  
- The NAP log hash is another.  
- Budgets record the **intended limits** for that tick, so later audits can detect whether behaviour matched configuration.

**New artefact:**

- `spec/json/umx_commit_manifest_v1.schema.json` — normative schema.  
- `spec/md/umx_commit_and_seal_semantics_v1.md` — narrative explaining signing order, failure modes and how this plug into NAP’s SEAL protocol.

---

### 2.15 I-19 — U-Ledger Storage & Universal Integer Indexing

**Baseline (Complement Doc G / I)**  
G6/I-19 asked for a **U-Ledger / U format doc**:

- record structure (envelope ref, tick, root hash, event type),  
- index keys (by node, tick, hash),  
- reconstruction of UMX state from U.

**Bridge / Gate evidence**  
NAP/ULedger descriptions already assume:

- Each node keeps a local ledger.  
- All nodes feed into a global **Universal Integer stream U**.  
- The testbed emphasises auditability, with hash chains and log replay.

**Pass-3 resolution for UMX**  
We specialise U-Ledger for UMX as follows:

- **Record structure:**  
  Each U-Ledger entry is a fixed-format record:
  ```json
  {
    "tick": 12345,
    "node_id": "umx://node/A",
    "event": "SNAPSHOT_COMMITTED",
    "manifest_anchor": "sha256:...",
    "prev_u": 987654321,
    "u": 987654322
  }
  ```
  where `u` is the next integer in the global U sequence.
- **Indexing:**  
  - Primary index by `u` (global order).  
  - Secondary indices by `tick`, `node_id`, `event`.
- **Reconstruction:**  
  - To reconstruct UMX state at tick t, an auditor walks the ledger entries up to the first manifest with `tick = t` and replays snapshots forward.

**New artefact:**

- `spec/md/umx_u_ledger_and_u_stream_v1.md` — full description of the record types and reconstruction procedure.

---

### 2.16 I-20 — Quotas & Budget-Drift Policies

**Baseline (Complement Doc G / I)**  
G7/I-20 required a **Budget Profile Annex** with:

- default quotas per node / per pillar,  
- drift tolerances τ,  
- required reactions (graceful degrade vs hard fail).

**Bridge / Gate evidence**  
Gate/testbed packs already implement **field budgets** and describe budget behaviour qualitatively, and Complement Doc G spells out that NAP enforces quotas, tracks drift and flags protocol breaks.

**Pass-3 resolution for UMX**  
We tie budgets to the UMX profile (I-7) and NAP bus contract (I-5):

- **Per-node quotas:**  
  - `msg_budget`, `byte_budget` as in 2.4.  
- **Drift tolerances:**  
  - Define a drift metric μ for each node over a rolling window (e.g. ratio of actual to expected usage).  
  - Tolerances `τ_soft`, `τ_hard` are stored in the profile.
- **Reactions:**  
  - When μ exceeds `τ_soft`, UMX logs a warning and may reduce learning rates.  
  - When μ exceeds `τ_hard`, UMX freezes learning and may require operator intervention.

**New artefact:**

- `spec/md/umx_budget_and_drift_policies_v1.md` — precise definitions of μ, τ_soft, τ_hard and their interactions with UMX behaviour.

---

### 2.17 I-21 — Two-Phase Tick Hooks for UMX

**Baseline (Complement Doc G / I)**  
G8/I-21 called for a **simple integration contract** that respects NAP’s two-phase tick:

- compute phase → sync phase,  
- Aether must not move to T+1 before NAP is done.

**Bridge / Gate evidence**  
Core Bridge Math and UMX Spec v1 already describe a **tick loop** where UMX exposes `tickOnce()` and the Gate orchestrates NAP and Loom/Press interactions.

**Pass-3 resolution for UMX**  
We make the two-phase tick **explicit** for UMX:

- The UMX engine exposes two math-level functions:
  - `umx.computeTick(t)` — pure simulation step using inputs available at the start of tick t.  
  - `umx.syncTick(t)` — incorporates any NAP-delivered updates, finalises the tick, and emits snapshot + ledger entries.
- Gate / NAP integration rules:
  - Gate calls `computeTick(t)` during **Phase 1**.  
  - NAP runs its sync / SEAL protocol.  
  - Once SEAL is complete for tick t, Gate calls `syncTick(t)` exactly once.  
  - Only then may the system advance to t+1.

**New artefact:**

- `spec/md/umx_two_phase_tick_contract_v1.md` — short, normative document with timing diagrams showing Gate, NAP and UMX interactions per tick.

---

## 3. UMX Build Plan — Borrowed from Gate Pattern

The Trinity / TBP Gate packs give us a **proven pattern** for moving from math + narrative to a full implementation:

1. Implementation spec (interfaces, invariants, schemas).  
2. Development roadmap (phased tasks).  
3. Verification plan & golden fixtures.  
4. Operator runbook.

UMX should mirror this structure so implementers can treat the Matrix pillar like another well-specified component.

### 3.1 UMX Implementation Spec v1 (Skeleton)

We define an implementation spec for UMX with the following major sections:

1. **Math Core Overview**  
   - Reference to the Aether Math Compendium and Uroboros equations that define UMX dynamics.  
   - Mapping from symbolic math (nodes, edges, residuals) to discrete state structures.

2. **Data Structures & IR**  
   - Node Manifest (I-4).  
   - SLP snapshot IR (I-2).  
   - Snapshot manifest and APX-like packaging (I-6).

3. **APIs**  
   - `tickOnce`, `computeTick`, `syncTick` (I-21).  
   - MDL hooks (I-1, I-17).  
   - NAP JS API wrappers (I-14).  
   - Profile loading and enforcement (I-7).

4. **Invariants & Safety Conditions**  
   - Conservation, continuity, residual bounds (I-9).  
   - No-free-copy and determinism rules (I-11, I-12).  
   - Budget and drift behaviour (I-5, I-20).

5. **Integration Contracts**  
   - With Loom/Press (I-6).  
   - With NAP/SEAL and U-Ledger (I-18, I-19, I-21).

### 3.2 UMX Development Roadmap v1 (Phases)

Borrowing the TBP Gate roadmap’s multi-phase structure, we outline a UMX roadmap:

- **Phase U1 — Math Core & Snapshot Skeleton**  
  - Implement the UMX update rules as paper math + simple reference implementation.  
  - Implement Node Manifest and SLP snapshot IR without MDL learning.

- **Phase U2 — Profiles & Invariants**  
  - Implement profile loading and enforcement (I-7).  
  - Implement residual/inertia behaviour and conservation checks (I-9).

- **Phase U3 — NAP Bus & Budgets**  
  - Implement NAP envelope extensions and bus contract (I-5, I-20).  
  - Integrate with NAP’s quotas and drift tracking.

- **Phase U4 — MDL-Driven Learning**  
  - Connect UMX traces to Press/CE MDL calculations (I-1, I-17).  
  - Implement MDL-based accept/reject of topology changes.

- **Phase U5 — Ledger & Reversibility**  
  - Implement U-Ledger record structure and indexing (I-19).  
  - Implement Commit Manifest and SEAL semantics (I-18).  
  - Implement reversibility windows (I-15).

- **Phase U6 — Two-Phase Tick Integration**  
  - Implement `computeTick` / `syncTick` and integrate with NAP’s two-phase scheduling (I-21).  
  - Wire into Gate’s main loop as a pluggable engine.

- **Phase U7 — Hardening & Operator Ergonomics**  
  - Add operator-facing tooling mirroring the Gate runbook (dashboards for residuals, budgets, MDL gains, ledger health).  
  - Tighten failure modes and observability.

### 3.3 UMX Verification Plan & Golden Fixtures

Mirroring the TBP Gate verification pack, UMX should have:

- **Micro-tests** for each invariant:  
  - MDL monotonic improvement (I-1).  
  - Residual bounds and continuity (I-9).  
  - No-free-copy and determinism (I-11, I-12).  
  - Budget behaviour under normal and overrun conditions (I-5, I-20).

- **Golden fixtures**:  
  - Tiny matrix scenes with known behaviour and hand-computed results.  
  - Encoded as APX-like capsules with MANIFEST + layers, so both paper and JS implementations can verify against them.

- **Runbook**:  
  - A short operator runbook for UMX alone, plus a combined Gate+UMX runbook for full system operation.

New artefacts for this section (names only; contents to be written in subsequent passes):

- `tbp_umx_implementation_spec_v_1.md`  
- `tbp_umx_development_roadmap_v_1.md`  
- `tbp_umx_verification_test_plan_v_1.md`  
- `tbp_umx_golden_fixtures_pack_v_1.md`  
- `tbp_umx_operator_runbook_v_1.md`

---

## 4. Gap Status Summary After Pass 3

High-level status of the I-series gaps after incorporating Bridge/Gate material:

- **Substantially specified (v1-ready pending numeric tuning):**  
  - I-1, I-2, I-4, I-5, I-6, I-7, I-9, I-11, I-12, I-14, I-15, I-16, I-17, I-18, I-19, I-20, I-21.

- **Carried forward (need further work in future passes):**  
  - I-3 (multi-layer UMX structure), I-8 (merge/propagate/resolve phasing details), I-10 (anchor-in-layer formalisation), I-13 (sub-tick semantics), and post-I-21 H-derived stress / nesting gaps.

- **New artefact families established in this pass:**  
  - UMX MDL objective and MDL unification docs.  
  - Node Manifest, SLP snapshot IR, and profile schemas.  
  - NAP bus contract, budget/drift policies, and envelope extensions.  
  - Commit Manifest v1 schema and U-Ledger/U stream documentation.  
  - Two-phase tick contract and reversibility window spec.  
  - UMX implementation spec, roadmap, verification plan and operator runbook skeletons.

These are sufficient for a developer to begin a **full UMX implementation** that stays consistent with the existing Gate / Bridge packs, with the understanding that a later pass will: (a) finish the multi-layer / sub-tick details, and (b) fully populate the new artefact files sketched here.

### Source: `umx_gap_closure_pass_5_aether_full_clean_master_pack_2025_11_16.md` (verbatim)

---
pass: 5
pillar: Universal Matrix (UMX)
focus: Gap Closure & Build Plan — Aether Full Clean Master Pack
status: draft
created: 2025-11-16
---

# UMX Gap Closure — Pass 5 (Aether Full Clean Master Pack)

This pass uses the **Aether Full Clean master bundle** (`aether full clean (2).zip`) as a **system-level ground truth** for:

- Cross-pillar invariants and properties.
- Testbed structure, GO/NO-GO semantics and emergence tolerance.
- Determinism, quotas, drift, kill-switch and provenance behaviour.

The goal is to:

1. Finish tightening the remaining **I-series gap families** from *Complement Doc I* that are explicitly about **stress, emergence, epsilon layers, drift, kill-switches and testbeds**.
2. Align UMX v1 spec + build plan with the **Aether Paper Testbed** and **MAX Test Suite**.
3. Ensure that a UMX implementation can be dropped into the existing Aether testbed and evaluated *without writing new code* (paper-first guarantee).

Per project policy, all normative interpretations in this pass are backed by **direct quotes** from files inside the Aether Full Clean pack.

---

## 0. Inputs for Pass 5

From `aether full clean (2).zip` we use the following **primary sources**:

### 0.1 Canonical chat logs (already referenced but now treated as packaged, canonical copies)

- `aether full clean/cannonical_chat_logs/1 ChatGPT-Uroboros genesis.md`
- `aether full clean/cannonical_chat_logs/2 ChatGPT-Aether computing development v1.md`
- `aether full clean/cannonical_chat_logs/3 ChatGPT-Aether computing V2 build.md`
- `aether full clean/cannonical_chat_logs/4 ChatGPT-Aether press experiments setup.md`
- `aether full clean/cannonical_chat_logs/5 ChatGPT-Aevum loom.md`
- `aether full clean/cannonical_chat_logs/6 ChatGPT-development and testing v1.md`
- `aether full clean/cannonical_chat_logs/7 ChatGPT-development ant testing v2.md`
- `aether full clean/cannonical_chat_logs/8 ChatGPT-Build new computing paradigm.md`

These are the same conceptual logs we already used in Pass 4, but their presence in the master bundle confirms their status as **canonical** and ties them to specific testbed runs.

### 0.2 Aether Paper Testbed — MASTER handover

From `aether full clean/implementation/Aether_Testbed/Aether_Testbed_MASTER_v3_2025-10-30/README_Aether_Testbed_MASTER.md`:

> "# Aether Paper Testbed — MASTER Handover (2025-10-30)\n\nThis bundle contains a **deterministic, code-free testbed** for Aether pillars & protocols.\nIt uses **tabular TSVs and Excel formulas only** (no macros, no scripts) to validate invariants,\nprotocol semantics, and emergence-tolerant behavior."

> "## Contents (top-level)\n- **ledger.tsv, events.tsv, models.tsv, assertions.tsv** — baseline data fabric\n- **Aether_Testbed_v0_2025-10-30_MAIN.xlsx** — main workbook with Summary + emergence wiring\n- **Aether_Testbed_v0.1_2025-10-30.xlsx** — emergence workbook (formulas + config mirror)\n- **Aether_Test_Suite_2025-10-30.xlsx** — full 15-scenario suite with `Suite_Summary` (formulas) and `Suite_Run` (precomputed)\n- **Aether_Testbed_Further_Tests_2025-10-30.xlsx** — earlier 6-scenario checks\n- **EMERGENCE_CONFIG.json** — drift tolerance and guardrail settings (mirrored in sheets)\n- **Run reports** — markdown/TSV snapshots for audit\n- **ZIPs** — per-feature bundles (emergence, further tests, suite)\n- **TEST_PLAN.md / TEST_MATRIX.tsv** — multi-phase plan & matrix"

> "## What each check means\n- **Conservation** — Σφ constant across τ (Press/Lattice invariants).  \n- **Idempotence** — dup nonce must be rejected (NAP/TGP).  \n- **Replay / Contraction / Fidelity** — ledger & residual guarantees (Loom/Press).  \n- **SLL_accept** — if `accepted=TRUE`, require `delta_mdl < 0`.  \n- **Drift** — emergence band: PASS (0), INVESTIGATE (0<Δ≤ε), FAIL (Δ>ε).  \n- **Budget / Sanitize / Routing / HashChain / Causality** — protocol/lattice/time checks."

This testbed is the **paper-mode arbiter** of whether pillars and protocols (including Matrix/UMX) satisfy their invariants.

### 0.3 Aether MAX Test Suite

From `aether full clean/implementation/Aether_Testbed/Aether_Testbed_MASTER_v2_2025-10-30/TEST_PLAN_MAX.md`:

> "# Aether MAX Test Suite — Paper-Mode\n\nThis suite extends coverage to **every pillar & protocol claim** using **booleans + simple numerics** only.\nAll logic remains inside **Excel formulas**; TSVs are editable for scenario crafting."

> "## New properties (Assertions columns)\n- reversible_ok, orthogonal_residuals_ok, entropy_bound_ok\n- checkpoint_spacing_ok, skip_ahead_ok, skip_back_ok\n- isolation_ok, routing_capacity_ok, back_pressure_ok, dead_letter_empty\n- schema_negotiated, approval_ok, kill_switch_ok, provenance_ok\n- exactly_once_ok, ordering_causal_ok, duplicate_suppression_ok, id_key_seed_ok\n- reproducible_training_ok, drift_guard_ok"

> "## Determinism\n- No macros/scripts. Formulas only. Identical inputs ⇒ identical outputs."

This gives us a **complete property vocabulary** that UMX must support and/or surface metrics for.

### 0.4 GO/NO-GO roll-up

From `aether full clean/implementation/Aether_Testbed/Aether_Testbed_MASTER_v3_2025-10-30/GO_NO_GO.md`:

> "# Aether Paper Testbed — Go/No-Go (2025-10-30)\n\n**Verdict:** NO-GO"

> "## Roll-up\n- Base Suite: 5 / 15 meet expectation (33.3%)\n- MAX Suite: 20 / 20 meet expectation (100.0%)\n- OVERALL: 25 / 35 meet expectation (71.4%)"

> "## What \"Go\" means\nAll scenarios produced the *expected* outcome (including intentional FAIL/INVESTIGATE/QUARANTINE where specified)."

> "## Modify thresholds\n- **ε tolerance** lives in the Summary sheet (and/or `EMERGENCE_CONFIG.json`).\n- Budget window/quota are simple first-window demos; extend ranges or add rolling windows as needed."

This document encodes the **system-level GO/HOLD/NO-GO semantics** for Aether.

### 0.5 Trinity full-systems proofs & math packs (structural inputs)

We also rely on the presence (though not fully unpacked content in this pass) of:

- `archive/Trinity_full_systems_proof/full system specs/Trinity_Math_Compendium.pdf`
- `archive/Trinity_full_systems_proof/full system specs/Trinity_System_Equations.pdf`
- `archive/Trinity_full_systems_proof/full system specs/Trinity_System_Equations_Expanded.pdf`
- `archive/Trinity_full_systems_proof/full system specs/Trinity_System_Math_Reference_v1.pdf`
- PFNA integerisation and tag-math packs under `aether computing system framework/`

These establish that the paper testbed and property checks are **derived from a fully specified equation set**, not ad-hoc heuristics. For UMX, we treat their existence as a constraint: our UMX v1 spec must be compatible with those global equations.

---

## 1. Canonical invariant set (from Aether Testbed) and implications for UMX

From the MASTER README and MAX plan, we can extract a **canonical invariant set** that Aether expects all pillars (including UMX) to satisfy.

### 1.1 Core checks from MASTER README

Quoted again for clarity:

> "## What each check means\n- **Conservation** — Σφ constant across τ (Press/Lattice invariants).  \n- **Idempotence** — dup nonce must be rejected (NAP/TGP).  \n- **Replay / Contraction / Fidelity** — ledger & residual guarantees (Loom/Press).  \n- **SLL_accept** — if `accepted=TRUE`, require `delta_mdl < 0`.  \n- **Drift** — emergence band: PASS (0), INVESTIGATE (0<Δ≤ε), FAIL (Δ>ε).  \n- **Budget / Sanitize / Routing / HashChain / Causality** — protocol/lattice/time checks."

Implications for UMX:

- **Conservation:** UMX’s internal update rules must make any conserved quantities **explicit**, with Σφ tracked per tick and exposed to the testbed via `ledger.tsv` / `models.tsv` equivalents.
- **Idempotence:** UMX must not re-apply the same NAP envelope or structural event twice; this dovetails with the no-free-copy and TickLedger semantics already defined in earlier passes.
- **Replay / Contraction / Fidelity:** UMX’s snapshot + ledger design must support exact or epsilon-bounded replay, matching Aevum’s I/P-block and epsilon-ledger model.
- **SLL_accept:** MDL-based learning decisions in SLP (I-1/I-17) must be observable in the assertions TSV as `delta_mdl` and `accepted` flags, so the testbed can enforce `accepted ⇒ delta_mdl < 0`.
- **Drift:** Residuals and epsilon layers must feed into a scalar drift measure Δ, allowing categorisation into PASS / INVESTIGATE / FAIL as per `EMERGENCE_CONFIG.json`.
- **Budget / Sanitize / Routing / HashChain / Causality:** UMX’s integration contracts (with NAP, Gate, Loom, Press) must surface boolean checks for these properties in the MAX test suite.

### 1.2 MAX properties as a property vocabulary

From TEST_PLAN_MAX:

> "## New properties (Assertions columns)\n- reversible_ok, orthogonal_residuals_ok, entropy_bound_ok\n- checkpoint_spacing_ok, skip_ahead_ok, skip_back_ok\n- isolation_ok, routing_capacity_ok, back_pressure_ok, dead_letter_empty\n- schema_negotiated, approval_ok, kill_switch_ok, provenance_ok\n- exactly_once_ok, ordering_causal_ok, duplicate_suppression_ok, id_key_seed_ok\n- reproducible_training_ok, drift_guard_ok"

For UMX, these imply:

- **reversible_ok / checkpoint_spacing_ok / skip_ahead_ok / skip_back_ok:**
  - UMX’s reversibility windows (I-15) and time ledger integration must provide enough structure for these properties to be evaluated directly in the paper testbed.

- **orthogonal_residuals_ok / entropy_bound_ok / drift_guard_ok:**
  - Residuals and epsilon layers (I-9, I-23, I-24, I-26) must be defined tightly enough that orthogonality, entropy bounds and drift guarding can be expressed as boolean formulas over TSV data.

- **isolation_ok / routing_capacity_ok / back_pressure_ok / dead_letter_empty:**
  - NAP bus + UMX routing (I-5, I-20, I-22) must produce explicit metrics and events that the testbed can check for isolation, capacity, backpressure and dead-letter handling.

- **schema_negotiated / approval_ok:**
  - UMX’s interaction with NAP and Gate must expose schema negotiation and approval decisions, likely via NAP envelope metadata and commit manifests.

- **kill_switch_ok:**
  - UMX must support a deterministic kill-switch that can be triggered and observed at the paper level (no hidden state).

- **provenance_ok / exactly_once_ok / ordering_causal_ok / duplicate_suppression_ok / id_key_seed_ok:**
  - These constrain the interplay of U-Ledger, TickLedger, NAP envelopes and Gate; UMX contributes by providing deterministic anchors, IDs and hashes.

- **reproducible_training_ok:**
  - Any learning behaviour in UMX (topology changes, SLP updates) must be replayable with the same seed and input stream, consistent with the determinism requirements already present.

### 1.3 GO/NO-GO semantics

From GO_NO_GO:

> "## Roll-up\n- Base Suite: 5 / 15 meet expectation (33.3%)\n- MAX Suite: 20 / 20 meet expectation (100.0%)\n- OVERALL: 25 / 35 meet expectation (71.4%)"

> "## What \"Go\" means\nAll scenarios produced the *expected* outcome (including intentional FAIL/INVESTIGATE/QUARANTINE where specified)."

> "## Modify thresholds\n- **ε tolerance** lives in the Summary sheet (and/or `EMERGENCE_CONFIG.json`).\n- Budget window/quota are simple first-window demos; extend ranges or add rolling windows as needed."

Implications for UMX profiles and stress gaps:

- A UMX profile cannot be considered **GO** unless it passes both **Base** and **MAX** suites under the same criteria.
- Emergence tolerances (ε) and budgets live in **EMERGENCE_CONFIG.json** and profile JSONs; UMX must bind its internal thresholds to these values, not ad-hoc constants.
- Intentional FAIL/INVESTIGATE/QUARANTINE scenarios must be supported by UMX’s logging and behaviour; these states are part of normal operation for testing.

---

## 2. Per-Gap Updates (Complement Doc I × Aether Full Clean)

In this pass we focus primarily on the **stress, emergence, epsilon and testbed** gaps, which we denote (following Complement Doc I/H terminology):

- I-22 — Stress & Overload Test Matrix (UMX under load / failure).  
- I-23 — ε-Layer Metrics & Instrumentation.  
- I-24 — Emergence Tolerance Bands (PASS / INVESTIGATE / FAIL / QUARANTINE).  
- I-25 — Kill-Switch, Quarantine & Safety Cut-Through.  
- I-26 — Drift Guards & Budget Interplay.  
- I-27 — Paper Testbed ↔ Runtime Equivalence.

Where needed, we also refine earlier gaps (I-7, I-9, I-15, I-20) to integrate with these.

Each subsection below uses the familiar template:

- **Baseline (Complement Doc I/H):** what the gap expressed.  
- **Aether Full Clean evidence:** what the master pack says.  
- **Pass-5 resolution:** concrete, UMX-specific decisions + artefacts.

---

### 2.1 I-22 — Stress & Overload Test Matrix

**Baseline (Complement Doc I/H)**  
I-22 identified that UMX must be tested under **stress and overload conditions** (high routing pressure, quota breaches, failure of peers, dead-letter queues), but:

- No explicit **test matrix** or required scenarios were defined.  
- It was unclear how UMX would integrate with Aether’s emerging testbed.

**Aether Full Clean evidence**  
From TEST_PLAN_MAX:

> "- isolation_ok, routing_capacity_ok, back_pressure_ok, dead_letter_empty"

From MASTER README:

> "- **Budget / Sanitize / Routing / HashChain / Causality** — protocol/lattice/time checks."

From GO_NO_GO:

> "Budget window/quota are simple first-window demos; extend ranges or add rolling windows as needed."

Interpretation:

- Aether expects **explicit properties** for routing capacity, backpressure and dead-letter behaviour, with budgets and quotas configurable in `EMERGENCE_CONFIG.json`.
- Stress behaviour is not an afterthought; it is integrated into the same boolean assertion framework as all other properties.

**Pass-5 resolution for UMX**  
UMX v1 adopts the following stress test matrix structure:

1. **Required stress properties:** UMX must provide metrics and behaviours so that the following MAX properties can be evaluated purely from TSV data:
   - `routing_capacity_ok` — under a synthetic load scenario, UMX must either route all messages within capacity or signal backpressure and/or dead-letter events as defined in the profile.
   - `back_pressure_ok` — when NAP or Gate apply backpressure, UMX must slow or drop non-critical work according to the NAP bus contract (I-5/I-20) without violating invariants.
   - `dead_letter_empty` — for scenarios marked as non-pathological, dead-letter queues must be empty at scenario end.
   - `isolation_ok` — faults injected in one region of the Matrix must not spill into isolated regions, as observed via ledger/events TSVs.

2. **Scenario pattern:** Stress scenarios for UMX follow the Aether paper-mode pattern (from MASTER README and GO_NO_GO):
   - Each scenario is represented by a quad of sheets `SxxL/E/M/A` (Ledger, Events, Models, Assertions) or equivalent TSVs.
   - Stress is applied by setting specific budget, routing and isolation fields in `models.tsv` and injecting crafted events.

3. **UMX-specific artefact:**
   - `spec/md/umx_stress_test_matrix_v1.md` will:
     - List required stress scenarios and their mapping to MAX properties.  
     - Define the expected shape of ledger and events entries for `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`.  
     - Provide example Sxx patterns that UMX implementers must be able to reproduce.

With this, I-22 becomes a **concrete requirement**: UMX must support a specific, paper-described stress matrix rather than a vague “should be stress-tested”.

---

### 2.2 I-23 — ε-Layer Metrics & Instrumentation

**Baseline (Complement Doc I/H)**  
I-23 described ε-layers as places where **small residual corrections** and **nonlocal effects** are recorded, but:

- It did not define the exact metrics the system must emit.  
- It did not connect ε-layers to an external testbed.

**Aether Full Clean evidence**  
From MASTER README:

> "**Drift** — emergence band: PASS (0), INVESTIGATE (0<Δ≤ε), FAIL (Δ>ε)."

From GO_NO_GO:

> "- **ε tolerance** lives in the Summary sheet (and/or `EMERGENCE_CONFIG.json`)."

From TEST_PLAN_MAX:

> "- orthogonal_residuals_ok, entropy_bound_ok\n- ...\n- drift_guard_ok"

Interpretation:

- ε-layers are not just conceptual; they must feed **drift metrics** Δ into the testbed.
- Testbed configuration defines ε and drift-guard behaviour via `EMERGENCE_CONFIG.json` and summary sheets.

**Pass-5 resolution for UMX**  
UMX v1 defines ε-layer instrumentation and metrics as follows:

1. **Residual metrics:**
   - Each node (and optionally each edge) emits per-tick integer residuals `r_i(t)` and a norm `‖r_i(t)‖` as defined in earlier passes (I-9).

2. **Drift metric Δ:**
   - For each scenario/run, a scalar drift Δ is computed over a window, using only data exposed in `models.tsv` / `ledger.tsv` style tables.
   - The precise formula is defined in `EMERGENCE_CONFIG.json` and mirrored in UMX docs (e.g., weighted sum of norm deviations, normalised by baseline).

3. **ε-layers:**
   - ε-layers store **sparse correction records** when `‖r_i(t)‖` or Δ exceed profile-level thresholds but are still within emergence tolerances.
   - Each ε-record is anchored via the Anchor Map (I-10) and shows up in events/ledger TSVs so the testbed can check `orthogonal_residuals_ok` and `entropy_bound_ok`.

4. **Artefact:**
   - `spec/md/umx_epsilon_layers_and_drift_metrics_v1.md` will:
     - Define residual metrics, Δ, and their representation in TSVs.  
     - Describe how `EMERGENCE_CONFIG.json` supplies ε and drift-guard parameters.  
     - Connect these directly to MAX properties: `orthogonal_residuals_ok`, `entropy_bound_ok`, `drift_guard_ok`.

I-23 moves from “ε-layers exist” to “ε-layers emit specific metrics consumed by the Aether Testbed”.

---

### 2.3 I-24 — Emergence Tolerance Bands

**Baseline (Complement Doc I/H)**  
I-24 introduced the idea of **emergence bands** (e.g., harmless micro-variance, tolerable macro-variance, unacceptable drift) but did not define how these map onto concrete categories or where the thresholds live.

**Aether Full Clean evidence**  
From MASTER README:

> "**Drift** — emergence band: PASS (0), INVESTIGATE (0<Δ≤ε), FAIL (Δ>ε)."

From GO_NO_GO:

> "All scenarios produced the *expected* outcome (including intentional FAIL/INVESTIGATE/QUARANTINE where specified)."

Interpretation:

- Aether uses at least three explicit bands: PASS, INVESTIGATE, FAIL, plus QUARANTINE as a scenario status.
- ε comes from configuration (Summary sheet / EMERGENCE_CONFIG.json), not from code.

**Pass-5 resolution for UMX**  
UMX v1 adopts the following emergence band structure:

1. **Bands defined over Δ:**
   - Given a scalar drift Δ (see I-23), we define bands:
     - PASS: Δ = 0.  
     - INVESTIGATE: 0 < Δ ≤ ε.  
     - FAIL: Δ > ε.

2. **QUARANTINE as a scenario state:**
   - Scenarios (or specific nodes/regions) may be flagged QUARANTINE in the assertions table.  
   - QUARANTINE means “expected deviation beyond ε, under investigation or intentionally exposed to stress”.

3. **Where ε lives:**
   - ε is stored in `EMERGENCE_CONFIG.json` and mirrored in UMX profiles; UMX code must not hard-code ε.

4. **Artefact:**
   - `spec/md/umx_emergence_bands_v1.md` will:
     - Spell out these bands.  
     - Define how they map to assertions columns (PASS/INVESTIGATE/FAIL) and QUARANTINE marks.  
     - Clarify operator expectations for each band.

I-24 thus becomes an explicit mapping between drift metrics and scenario classification, fully compatible with the paper testbed.

---

### 2.4 I-25 — Kill-Switch, Quarantine & Safety Cut-Through

**Baseline (Complement Doc I/H)**  
I-25 required that the system have a **kill-switch and quarantine mechanism** that is:

- Deterministic.  
- Observable in the ledger/testbed.  
- Able to isolate misbehaving subsystems without collapsing the whole run.

**Aether Full Clean evidence**  
From TEST_PLAN_MAX:

> "- kill_switch_ok"

From MASTER README:

> "**Idempotence** — dup nonce must be rejected (NAP/TGP)."

From GO_NO_GO:

> "All scenarios produced the *expected* outcome (including intentional FAIL/INVESTIGATE/QUARANTINE where specified)."

Interpretation:

- Kill-switch behaviour is treated as a boolean property (`kill_switch_ok`) in MAX.  
- Some scenarios explicitly expect QUARANTINE outcomes and must not be treated as simple FAILs.

**Pass-5 resolution for UMX**  
UMX v1 defines kill-switch and quarantine semantics as follows:

1. **Kill-switch semantics:**
   - UMX exposes a **kill-switch control** per profile/scenario that, when activated:
     - Immediately stops accepting new NAP envelopes for the affected region or whole system (profile-defined).  
     - Flushes any pending learning/topology changes (set to no-op).  
     - Leaves the ledger in a consistent, replayable state (no half-applied events).

2. **Observability:**
   - Kill-switch activation must appear as a specific event type in `events.tsv` (e.g., `KILL_SWITCH_TRIGGERED`) with fields:
     - target scope (node/region/system),  
     - cause (manual/testbed-driven/automatic guard),  
     - tick and sequence index.

3. **Quarantine semantics:**
   - QUARANTINE scenarios set expectations in assertions TSVs, not direct PASS/FAIL.  
   - UMX must support **partial shutdown / isolation** of regions while keeping other regions operational.

4. **Artefact:**
   - `spec/md/umx_kill_switch_and_quarantine_v1.md` will:
     - Define control surfaces (how kill-switch is invoked).  
     - Define ledger/event representations.  
     - Map behaviour to `kill_switch_ok` and QUARANTINE scenarios in the testbed.

I-25 is now fully tied to Aether’s MAX property vocabulary and testbed expectations.

---

### 2.5 I-26 — Drift Guards & Budget Interplay

**Baseline (Complement Doc I/H)**  
I-26 recognised that **drift control** and **budget enforcement** interact, but left this as a conceptual statement (e.g. heavy throttling might increase drift if corrections are delayed).

**Aether Full Clean evidence**  
From MASTER README:

> "**Drift** — emergence band: PASS (0), INVESTIGATE (0<Δ≤ε), FAIL (Δ>ε)."

From TEST_PLAN_MAX:

> "- drift_guard_ok"  
> "- ... back_pressure_ok ... budget ..."

From GO_NO_GO:

> "Budget window/quota are simple first-window demos; extend ranges or add rolling windows as needed."

Interpretation:

- Aether explicitly tests `drift_guard_ok` alongside budget and backpressure checks.  
- Budget windows/quotas and drift bands are configured together.

**Pass-5 resolution for UMX**  
UMX v1 ties drift guards and budgets together as follows:

1. **Drift guard behaviour:**
   - UMX defines a per-node or per-region drift guard that:
     - Monitors Δ over a rolling window.  
     - Triggers corrective actions (e.g. freeze learning, increase checkpoint frequency, widen ε-layers) when Δ approaches ε.

2. **Budget interplay:**
   - Budgets (msg/byte quotas) and drift guard thresholds are **jointly configured** in profile JSONs and `EMERGENCE_CONFIG.json`.
   - When budgets are tightened (smaller quotas), drift guard thresholds may need adjustment to avoid false positives.

3. **Testbed visibility:**
   - Drift guard activations appear as events in TSVs, and the resulting behaviour must cause `drift_guard_ok` and `back_pressure_ok` to be TRUE in appropriate scenarios.

4. **Artefact:**
   - `spec/md/umx_drift_and_budget_coupling_v1.md` will:
     - Document the joint configuration surface.  
     - Provide examples where budget changes and drift thresholds must be co-tuned.  
     - Link to NAP bus contract and emergence bands.

I-26 is now concretely tied to the MAX test suite and EMERGENCE_CONFIG.json rather than being an abstract warning.

---

### 2.6 I-27 — Paper Testbed ↔ Runtime Equivalence

**Baseline (Complement Doc I/H)**  
I-27 demanded a **bridge between paper testbed and runtime**, ensuring that:

- The code-free testbed scenarios truly reflect runtime behaviour.  
- Implementers can derive runtime checks from paper assertions.

**Aether Full Clean evidence**  
From MASTER README:

> "This bundle contains a **deterministic, code-free testbed** for Aether pillars & protocols.\nIt uses **tabular TSVs and Excel formulas only** (no macros, no scripts) to validate invariants,\nprotocol semantics, and emergence-tolerant behavior."

From TEST_PLAN_MAX:

> "All logic remains inside **Excel formulas**; TSVs are editable for scenario crafting."

From GO_NO_GO:

> "If **NO-GO**, open the Dashboard workbook → Details tabs to find mismatches.\n- Adjust scenario Assertions or numeric fields to correct behavior, then regenerate this roll-up."

Interpretation:

- Paper testbed is *definitive* for invariants (“code-free” and “deterministic”).  
- Runtime must be adjusted to match the paper testbed, not vice versa.

**Pass-5 resolution for UMX**  
UMX v1 defines a clear equivalence principle:

1. **Paper-first semantics:**
   - The paper testbed (TSVs + Excel formulas) defines the **intended UMX behaviour**.  
   - UMX JS or other implementations are considered correct only if they reproduce these results for all scenarios.

2. **Scenario crosswalk:**
   - Each UMX scenario has a unique ID `Sxx` that is used in both paper testbed and runtime integration tests.
   - Runtime test harnesses load the same TSVs used by the paper testbed and check that UMX outputs match the assertions.

3. **Mismatches and NO-GO:**
   - If runtime diverges from paper results, the system is NO-GO until either:
     - runtime is fixed, or  
     - the paper scenario is updated and re-validated via GO_NO_GO.

4. **Artefact:**
   - `spec/md/umx_paper_runtime_equivalence_v1.md` will:
     - Define the equivalence principle.  
     - Describe the scenario ID convention.  
     - Explain how UMX integration tests must be wired to the paper TSVs.

With this, I-27 is fully bound to the Aether Full Clean testbed and GO/NO-GO loop.

---

## 3. Secondary refinements to earlier gaps

### 3.1 I-7 — Profile Calibration (GO/HOLD/KILL) revisited

Pass 4 already tied profile calibration to GO/HOLD/KILL discipline. Aether Full Clean strengthens this:

- GO/NO-GO.md shows that **Overall verdicts** are computed from Base + MAX suites.  
- README and TEST_PLAN_MAX confirm that **every pillar & protocol claim** must be covered by boolean assertions.

UMX profile artefacts (`umx_profile_v1.schema.json`) should therefore include:

- A **test coverage manifest** (list of Sxx scenarios the profile has passed).  
- A **GO/NO-GO flag** and timestamp tied to a specific version of the paper testbed.

### 3.2 I-9 / I-15 / I-20 — Residuals, reversibility and budgets

The presence of MAX properties like `reversible_ok`, `checkpoint_spacing_ok`, `skip_ahead_ok`, `skip_back_ok` reinforces earlier decisions:

- I-15 (reversibility windows) must be tested explicitly via scenarios that check skip-ahead and skip-back correctness.
- I-9 (residual behaviour) and I-20 (budget and drift policies) must produce metrics that drive `reversible_ok`, `entropy_bound_ok`, `budget`-related checks.

UMX verification artefacts (`tbp_umx_verification_test_plan_v_1.md`, `tbp_umx_golden_fixtures_pack_v_1.md`) must include explicit references to these MAX properties and scenarios.

---

## 4. Gap Status After Pass 5

After integrating the Aether Full Clean master pack:

- **Now strongly specified / v1-ready, structurally pinned:**
  - I-22 — Stress & Overload Test Matrix.  
  - I-23 — ε-Layer Metrics & Instrumentation.  
  - I-24 — Emergence Tolerance Bands.  
  - I-25 — Kill-Switch, Quarantine & Safety Cut-Through.  
  - I-26 — Drift Guards & Budget Interplay.  
  - I-27 — Paper Testbed ↔ Runtime Equivalence.

- **Refined and constrained further:**  
  - I-7 — Profile calibration (GO/NO-GO and coverage manifest).  
  - I-9 — Residual norms tied to entropy and orthogonality checks.  
  - I-15 — Reversibility windows tied to checkpoint spacing and skip-ahead/back checks.  
  - I-20 — Budgets expressed as paper-mode parameters and tied into drift guards.

- **Overall:**
  - With Passes 1–5, the I-series gap families now have:
    - Clear **math definitions** (from genesis + Trinity math packs).  
    - Explicit **integration contracts** (from UMX/NAP/Bridge specs).  
    - Concrete **testbed hooks and properties** (from Aether Full Clean).
  - UMX v1 is now positioned to be:
    - **Buildable** (devs have artefact names and behaviours).  
    - **Testable** in the existing Aether Paper Testbed.  
    - **Auditable** via U-Ledger, commit manifests and emergence bands.

The next phase is to **actually write out the named artefact docs** (e.g. `umx_stress_test_matrix_v1.md`, `umx_epsilon_layers_and_drift_metrics_v1.md`, `umx_emergence_bands_v1.md`, etc.) and then consolidate them into a **UMX Implementation & Verification Pack** ready for developer hand-off.

### Source: `umx_spec_artifacts_bundle_1_2025_11_16.md` (verbatim)

# UMX Spec Artifacts — Bundle 1

This bundle contains the first batch of **normative UMX v1 artefact documents** derived from the gap-closure passes.

Included in this bundle:

1. `umx_mdl_objective_v1.md`  
2. `umx_layers_policy_v1.md`  
3. `anchor_map_v1.md`  
4. `subtick_semantics_v1.md`  
5. `umx_profile_v1.md`

Each document is written so it can be split into its own file without modification.

---

---
id: umx_mdl_objective_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX MDL Objective v1

## 1. Purpose and Scope

This document defines the **Minimum Description Length (MDL) objective** used by the Universal Matrix (UMX) pillar for:

- **Topology and SLP learning** (when to accept structural changes),
- **Evaluating matrix configurations** against incoming data and internal dynamics,
- **Integrating with the global Aether MDL story** used by Press, NAP and other pillars.

The objective is defined in a way that:

- Can be executed **entirely on paper** (no code required),
- Takes UMX traces as input and delegates codelength calculations to the same MDL machinery used by Press,
- Surfaces the quantities needed by the Aether paper testbed (e.g. `delta_mdl`, `accepted`) as **simple numerics**.

This is a **normative v1 spec**: all UMX implementations must behave as if they are following this document.

## 2. Normative References

The following project materials are treated as defining context for this document:

- Aether / Uroboros genesis and MDL framing (canonical chat logs).  
- UMX Complement Doc I — Gap Closure & Profile Specs (MDL gap family I-1 / I-17).  
- UMX Gap Closure — Pass 2 and Pass 3 (Bridge/Gate cross-cut).  
- Aether Testbed MASTER docs describing `SLL_accept` and `delta_mdl` assertions.

Where there is any tension, this document **overrides** earlier informal descriptions for UMX v1 behaviour.

## 3. Core Concepts and Definitions

### 3.1 Trace and Canonical Encoding

For each UMX tick \(t\), we define a **UMX trace** \(T_t\) as the minimal data needed to reconstruct:

- The active node set and their local state,
- The active edges/bonds and their parameters (including SLP ley strengths),
- Residual metrics used by conservation and drift checks,
- Any external inputs applied to the matrix during tick \(t\).

The trace is encoded into a **canonical representation** `canon(T_t)` using the same principles as the Aether stack:

- A single, stable ordering of fields and records,
- No randomness in encoding,
- Values expressed as **bounded integers or fixed-point integers**, not IEEE floats.

This guarantees that the same UMX state produces the same `canon(T_t)` bitstring.

### 3.2 Codelength Functional \(\mathcal{L}\)

We assume the existence of a **global MDL functional** \(\mathcal{L}\) that, given a bitstring or a structured object with a fixed encoding, returns a **non-negative integer codelength**:

- \(\mathcal{L}(X) \in \mathbb{N}\),
- Smaller values represent more economical descriptions,
- \(\mathcal{L}\) is shared conceptually across UMX, NAP and Press (but applied to different objects).

For UMX, \(\mathcal{L}\) is applied to **traces and models** that describe UMX structure and behaviour.

### 3.3 Models, Residuals and Windows

At any time, UMX maintains an implicit **model** \(M\) of its structure and dynamics (node types, connectivity, SLP parameters, etc.).

Given a window of ticks \(W = \{t_0, t_0+1, \dots, t_0+K-1\}\), we define:

- \(\mathcal{L}_\text{model}(M)\): codelength to describe the model itself,
- \(\mathcal{L}_\text{data}(T_W \mid M)\): codelength to describe the trace sequence \(T_W\) given the model, including residuals,
- Total description length:
  \[
    L(M; W) = \mathcal{L}_\text{model}(M) + \mathcal{L}_\text{data}(T_W \mid M).
  \]

This is evaluated using the same encoding discipline as Press/CE, but with UMX-specific structures.

### 3.4 Proposal and Threshold \(\tau\)

A **proposal** is any change that alters the model \(M\):

- Topology changes (add/remove edges or nodes, rewire layers),
- SLP changes (ley strengths, growth/prune actions, pattern reuse),
- Parameter changes that affect how traces are predicted.

Each UMX profile defines a **non-negative integer threshold** \(\tau\), and a **window length** \(K\) used to evaluate proposals. These are part of the `umx_profile_v1` artefact.

## 4. MDL Objective Definition

### 4.1 Baseline Description Length

Given a current model \(M_0\) and a window \(W\), we define the **baseline codelength** as:

\[
  L_0 = L(M_0; W) = \mathcal{L}_\text{model}(M_0) + \mathcal{L}_\text{data}(T_W \mid M_0).
\]

This is computed once per evaluation window.

### 4.2 Proposed Model and New Description Length

A proposal yields a candidate model \(M_1\). The **candidate codelength** is:

\[
  L_1 = L(M_1; W) = \mathcal{L}_\text{model}(M_1) + \mathcal{L}_\text{data}(T_W \mid M_1).
\]

The **MDL gain** of the proposal is:

\[
  \Delta L = L_1 - L_0.
\]

By convention, **negative** \(\Delta L\) means improvement (shorter description).

### 4.3 Acceptance Rule

For UMX v1, the **acceptance rule** for any structural or SLP proposal is:

- Define \(\tau \ge 0\) from the active profile,
- Compute \(\Delta L\) over the configured window \(W\),
- The proposal is **accepted** only if:

\[
  \Delta L \le -\tau.
\]

- If \(\Delta L > -\tau\), the proposal is **rejected** and the model remains \(M_0\).

This mirrors the Aether Testbed property often written as:

> If `accepted = TRUE`, require `delta_mdl < 0`.

UMX generalises this to a tunable margin \(\tau\).

### 4.4 Separation of Concerns (UMX vs Press/CE)

- **UMX** decides *when to consider a proposal* and *how to interpret its effect on structure and SLP*.
- **Press/CE** is responsible for computing the **codelengths** \(\mathcal{L}_\text{model}\) and \(\mathcal{L}_\text{data}\) from canonical encodings.

UMX must treat \(\mathcal{L}\) as a **black-box numeric oracle** that maps canonical encodings to integers. The same oracle is used across the system to keep MDL semantics unified.

## 5. Windowing and Sampling

### 5.1 Window Selection

Each profile specifies a **window length** \(K\) (in ticks). For a proposal evaluated at tick \(t\):

- The default window is \(W = \{t-K+1, \dots, t\}\),
- If fewer than \(K\) ticks exist (early in a run), use whatever ticks are available.

### 5.2 Overlapping Windows and Caching

To minimise repeated work, the system may reuse intermediate codelength computations across overlapping windows, as long as:

- The final \(L_0\) and \(L_1\) values are identical to what a **fresh computation** would produce,
- No approximations are introduced.

This is an implementation detail; the specification only requires that the numeric results obey the definitions.

## 6. Profile Parameters and Roles

The following parameters are owned by `umx_profile_v1` but interpreted by this document:

- `mdl.window_ticks` — the window length \(K\),
- `mdl.tau` — the acceptance threshold \(\tau\),
- Optional flags controlling how aggressively proposals are generated (e.g. maximum proposals per tick).

Profiles may define different \(\tau\) and \(K\) for different use cases (sandbox vs production), but all must obey the same acceptance rule.

## 7. Invariants and Constraints

Any UMX implementation claiming conformance to this spec must satisfy:

1. **Monotonic Improvement for Accepted Proposals**  
   For every accepted proposal, \(\Delta L \le -\tau\). There are no accepted proposals with \(\Delta L > -\tau\).

2. **No Silent Model Changes**  
   Every change that affects \(M\) must be treated as a proposal, evaluated via this MDL objective.

3. **Deterministic Evaluation**  
   Given the same window \(W\), the same starting model \(M_0\) and the same proposal, all runs must produce the same \(L_0\), \(L_1\) and \(\Delta L\).

4. **Auditability**  
   For each evaluated proposal, the following values must be recorded in a ledger/testbed-friendly form:  
   - tick index at evaluation,  
   - identifiers for \(M_0\) and \(M_1\),  
   - window \(W\) (range of ticks),  
   - \(L_0\), \(L_1\), \(\Delta L\),  
   - `accepted` boolean.

These values must be sufficient for a human or the Aether paper testbed to reconstruct the decision path.

## 8. Testbed Integration

For each scenario where UMX learning is exercised, the Aether Testbed will:

- Read per-proposal records from TSVs mirroring the ledger,
- Compute `delta_mdl = L1 - L0` and check that:
  - If `accepted = TRUE`, then `delta_mdl ≤ -tau`,
  - If `accepted = FALSE`, then either `delta_mdl > -tau` or no proposal was present.

UMX must therefore expose `L0`, `L1`, `delta_mdl` and `accepted` as simple numeric/boolean columns in the relevant tables.

---

---
id: umx_layers_policy_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Layers Policy v1

## 1. Purpose and Scope

This document defines the semantics of **layers** in the Universal Matrix (UMX) pillar, including:

- The meaning of `layerId`,
- Allowed connectivity between layers, and
- Update cadence across layers.

It is grounded in the **multi-layer world stack** concept introduced in the Aether genesis conversation, where multiple planes share a single coordinate system and update at different macro tick rates.

UMX v1 deployments are allowed to be **single-layer**, but they must still conform to this policy so that multi-layer profiles can be introduced without structural changes.

## 2. Layer Concept

### 2.1 Shared Coordinate Frame

All UMX layers share a **single coordinate system**:

- Spatial coordinates (or abstract node identifiers) are defined once,
- Each layer \(\ell\) provides an additional plane of state over the same set of positions or node IDs,
- This matches the idea of "planes stacked" over the same grid.

### 2.2 Layer Index

The layer index is an integer:

- \(\ell \in \mathbb{Z}_{\ge 0}\),
- \(\ell = 0\) is the **base layer** (micro level),
- \(\ell > 0\) are derived layers (meso/macro, residual or aggregate views).

Each node is tagged with a `layerId = ℓ`.

## 3. Connectivity Policy

### 3.1 Intra-layer Edges

Edges between nodes on the **same layer** (\(\Delta\ell = 0\)) are always permitted, subject only to other UMX constraints (degree limits, budgets, etc.).

### 3.2 Inter-layer Edges

UMX v1 allows edges only between **adjacent layers**:

- Allowed: \(|\Delta\ell| = 1\),
- Forbidden: \(|\Delta\ell| > 1\).

This yields two types of inter-layer edges:

- Upward edges: from \(\ell\) to \(\ell+1\) (e.g., aggregation or influence upwards),
- Downward edges: from \(\ell\) to \(\ell-1\) (e.g., feedback or refinement).

All inter-layer edges must be explicitly marked as such in manifests and logs.

## 4. Update Cadence

Each layer \(\ell\) has an associated **integer cadence** \(k_\ell \ge 1\) measured in base-layer ticks:

- The base layer has \(k_0 = 1\): it updates every tick.
- A higher layer \(\ell > 0\) updates only on ticks \(t\) where:

\[
  t \equiv 0 \pmod{k_\ell}.
\]

This mirrors the intuitive picture:

- Base layer (e.g., villages) updates every tick,
- Next layer (e.g., towns) updates every \(k_1\) base ticks,
- Next layer (e.g., cities) updates every \(k_2\) base ticks, and so on.

Cadence values \(k_\ell\) are configured via the UMX profile.

## 5. v1 Reference Profile

The UMX v1 reference profile is explicitly **single-layer**:

- `max_layers = 1`,
- Only layer \(\ell = 0\) is instantiated,
- Any configuration that attempts to create \(\ell > 0\) is invalid for that profile.

Despite this, all data structures and logs must be layer-aware, so that multi-layer profiles can be introduced later without changing formats.

## 6. Manifests and Observability

The UMX Node Manifest and SLP snapshot IR must:

- Include `layerId` for each node, and
- Preserve enough information to:
  - Reconstruct which layers were active at each tick, and
  - Verify that cadence rules were followed.

Violations (e.g., a layer updating when \(t \not\equiv 0 \pmod{k_\ell}\)) must appear as explicit events in logs and be detectable by the paper testbed.

---

---
id: anchor_map_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# Anchor Map v1

## 1. Purpose and Scope

This document defines the **Anchor Map** for UMX, which ties together:

- Base-layer node identities and positions,
- Time ledger indices (I-blocks and P-blocks),
- Residual and ε-layer records that attach to base states.

The Anchor Map ensures that:

- Every residual or epsilon correction can be traced back to a **unique base anchor**,
- Reconstruction from the time ledger plus residuals is **unambiguous**,
- Paper-mode tools can follow these links using only IDs and integers.

## 2. Anchor Types

### 2.1 Base Anchors

A **base anchor** identifies a node on the base layer at a particular time reference:

- `node_id` — identifier for the node,
- `layer = 0` — base layer,
- `tick_ref` — reference to a ledger index (e.g., I-block index and optional offset),
- Optional `coord` — spatial coordinate if used.

We write this tuple as:

\[
  A_\text{base} = (\text{node\_id}, \ell = 0, \text{tick\_ref}, \text{coord}).
\]

### 2.2 Residual Anchors

A **residual anchor entry** \(R\) attaches a residual payload to a base anchor:

- `anchor_ref` — a pointer to a specific base anchor,  
- `layer = ℓ_residual > 0` — the residual or derived layer where this record lives,  
- `delta` — an integer payload representing the residual or correction.

### 2.3 Epsilon Anchors

An **epsilon anchor** is structurally identical to a residual anchor but specifically encodes **epsilon-level corrections** used to maintain bit-exact replay or tight drift control. These are sparse and should be rare under normal operation.

## 3. Mapping Rules

### 3.1 One-to-One Mapping for v1

For UMX v1, each residual or epsilon anchor must map to **exactly one** base anchor:

- There is no residual entry that simultaneously refers to multiple base nodes,
- Aggregation over multiple base nodes is represented by a separate aggregated node with its own base anchor.

This simplifies reconstruction and audit.

### 3.2 Time Reference

`tick_ref` must be expressed in terms of the Aevum-style time ledger:

- A base frame index (I-block), and
- An optional offset into the subsequent P-block sequence.

This ensures compatibility with the I/P-block press model and time-travel semantics.

## 4. Reconstruction Guarantee

Given:

- A base-layer state at a reference time (from initial state + I/P-block stream), and
- All residual and epsilon anchors with `anchor_ref.tick_ref ≤ t`,

it must be possible to reconstruct uniquely:

- The state of residual layers at tick \(t\),
- Any epsilon corrections that affect observables at tick \(t\).

The reconstruction procedure is conceptually:

1. Restore base-layer state at the target tick using the ledger,
2. For each residual anchor with `tick_ref ≤ t`, apply its `delta` to the appropriate derived layer value,
3. Apply epsilon anchors similarly, interpreting `delta` as minimal corrections.

UMX implementations must behave as if this conceptual procedure were followed, even if they use more efficient internal representations.

## 5. Logging and Testbed Integration

The Anchor Map must be visible to the paper testbed via:

- Node manifests (including `node_id`, `layerId`, and references to time indices),
- Events/ledger TSVs that list residual and epsilon entries as records containing the required fields.

The testbed must be able to:

- Trace any observed anomaly back to one or more anchors,
- Verify that each residual or epsilon entry has a unique, valid base anchor.

---

---
id: subtick_semantics_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# Sub-Tick Semantics v1

## 1. Purpose and Scope

This document defines **sub-tick semantics** for UMX in a way that is compatible with:

- The Aevum time ledger model (I-blocks and P-blocks), and
- The requirement that the system be **deterministic and replayable** from the ledger alone.

Sub-ticks are treated as internal structure inside a macro tick and must not change the external behaviour when viewed at the macro tick level.

## 2. Tick as Input Window

A macro tick \(T\) corresponds to a contiguous **input window** in the time ledger:

- Between two checkpoints (I-blocks), or
- Between an I-block and the next I-block.

All perturbations, messages and inputs that are considered part of tick \(T\) are contained in this window.

## 3. Sub-Ticks as Partitions

When sub-ticks are used, the input window for tick \(T\) is partitioned into \(M\) ordered segments:

\[
  W_T = W_T^0 \mathbin{\Vert} W_T^1 \mathbin{\Vert} \dots \mathbin{\Vert} W_T^{M-1},
\]

where ``\(\Vert\)" denotes concatenation.

Each segment \(W_T^m\) is applied as the input batch for **one sub-tick**.

## 4. Equivalence Requirement

UMX v1 must satisfy the following equivalence property:

- Let `UMX_step` denote the macro tick update, and `UMX_substep` denote the sub-tick update.
- Applying `UMX_step` once with the entire window \(W_T\) must yield the **same final state** (up to epsilon corrections) as applying `UMX_substep` sequentially over the partitioned segments \(W_T^0, ..., W_T^{M-1}\).

Formally:

\[
  \text{UMX\_step}(S_0, W_T) \approx \text{UMX\_substep}(\dots \text{UMX\_substep}(\text{UMX\_substep}(S_0, W_T^0), W_T^1) \dots, W_T^{M-1}),
\]

where \(S_0\) is the starting state and \(\approx\) indicates equality up to epsilon-layer corrections that are explicitly recorded.

## 5. Deterministic Ordering

The order of events inside \(W_T\) and within each \(W_T^m\) must be **fixed and deterministic**:

- Events are sorted according to a canonical ordering (e.g. by source, timestamp, or a composite key),
- The partitioning into \(W_T^m\) respects this ordering.

No permitted implementation may rely on uncontrolled thread scheduling or non-deterministic ordering to define sub-tick behaviour.

## 6. Profile Controls

Profiles control sub-ticks via parameters such as:

- Maximum number of sub-ticks per macro tick,
- Whether sub-ticks are enabled at all (M = 1 always),
- How sub-ticks map to real-world time or external sampling rates.

Profiles must not alter the equivalence requirement; they only constrain how sub-ticks are used.

## 7. Testbed Visibility

Sub-tick structure may or may not be visible in the paper testbed, depending on scenario design. At minimum, the testbed must be able to:

- Verify that macro-level results match expectations,
- Confirm that enabling/disabling sub-ticks does not change macro-level outcomes for the same input window.

This is achieved by using the same I/P-block ledger and comparing final states and drift metrics.

---

---
id: umx_profile_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Profile v1

## 1. Purpose and Scope

This document defines the structure and semantics of a **UMX profile** — a configuration object that collects all tunable parameters relevant to the UMX pillar:

- Tick and capacity limits,
- MDL thresholds,
- Residual and epsilon tolerances,
- NAP budgets and drift-guard thresholds,
- Ledger and reversibility settings,
- Calibration and coverage metadata.

UMX profiles are expressed as simple key–value structures (e.g., JSON or TSV rows) that can be edited and audited by humans without code.

## 2. High-Level Structure

Conceptually, a `umx_profile_v1` object contains the following sections:

- `tick` — basic size and capacity constraints,
- `mdl` — MDL window and threshold parameters,
- `residual` — bounds on residual norms and warning bands,
- `nap` — message and byte budgets and tolerances,
- `ledger` — retention and snapshot intervals,
- `layers` — maximum layer count and cadences (if used),
- `emergence` — ε values and drift bands,
- `calibration` — GO/HOLD/KILL and coverage information.

Each field is a bounded integer or small string identifier.

## 3. Sections and Fields

### 3.1 Tick Section

Defines structural limits per tick:

- `max_nodes` — maximum number of active nodes,
- `max_degree` — maximum number of edges per node,
- `max_layers` — allowed number of layers (at least 1).

These are hard constraints; attempts to exceed them must be treated as violations and logged.

### 3.2 MDL Section

Parameters for the MDL objective:

- `window_ticks` — window length \(K\) in ticks,
- `tau` — acceptance threshold \(\tau\) (integer),
- Optional: separate thresholds for different proposal types.

These feed directly into the MDL objective defined in `umx_mdl_objective_v1.md`.

### 3.3 Residual Section

Controls residual norms and warnings:

- `max_norm` — maximum permitted residual norm under normal operation,
- `warning_ratio` — fraction of `max_norm` at which warnings are emitted,
- Optional: parameters controlling epsilon-layer frequency or size.

### 3.4 NAP Section

NAP and bus-related budgets:

- `msg_budget` — maximum number of NAP messages per tick per node/region,
- `byte_budget` — maximum bytes per tick,
- `soft_tolerance` — fraction of budget beyond which behaviour changes (e.g. deferring non-critical work),
- `hard_tolerance` — absolute limit beyond which stricter actions are taken.

### 3.5 Ledger Section

Ledger and reversibility controls:

- `retention_ticks` — how many ticks of detailed ledger history must be retained,
- `snapshot_interval` — spacing between full snapshots or checkpoints,
- `reversibility_window` — number of ticks within which rollback is allowed.

### 3.6 Layers Section

Multi-layer controls (even if `max_layers = 1`):

- `max_layers` — restated here for convenience,
- `cadences` — mapping from layer indices to cadences \(k_\ell\) (e.g., simple list or table).

### 3.7 Emergence Section

Emergence and epsilon-tolerance parameters:

- `epsilon_drift` — ε tolerance for drift bands,
- Optional separate ε values for different metrics,
- References or links to `EMERGENCE_CONFIG` where shared values are stored.

These fields define the PASS / INVESTIGATE / FAIL thresholds for drift.

### 3.8 Calibration Section

Metadata for GO/HOLD/KILL and coverage:

- `status` — one of `GO`, `HOLD`, `KILL`,
- `testbed_version` — identifier for the Aether Testbed bundle used for calibration,
- `scenarios_passed` — list or count of scenarios in the paper testbed that this profile satisfies,
- `last_reviewed` — timestamp or tick index when calibration was last confirmed.

Profiles are only considered **GO** when coverage and status indicate that all required scenarios (Base + MAX suites) have passed for this profile.

## 4. Profile Lifecycle

Profiles are expected to move through states:

- Draft (under construction),
- HOLD (needs further proof/checks),
- GO (meets all current requirements),
- KILL (superseded or found unsafe).

The calibration section must track these states and provide enough context for auditors to understand why a profile is in a given state.

## 5. Conformance Requirements

A UMX implementation claiming to support profiles must:

- Read and enforce the numeric constraints defined here,
- Reflect these values in behaviour (e.g. budgets, thresholds),
- Expose profile identifiers in logs and testbed TSVs so that results can be tied back to a specific profile configuration.

Profiles must **not** introduce behaviour that contradicts other normative UMX specs (e.g. sub-tick equivalence, MDL acceptance rule, determinism).

### Source: `umx_spec_artifacts_bundle_2_2025_11_16.md` (verbatim)

# UMX Spec Artifacts — Bundle 2

This bundle contains the second batch of **normative UMX v1 artefact documents** derived from the gap-closure passes.

Included in this bundle:

1. `umx_epsilon_layers_and_drift_metrics_v1.md`  
2. `umx_emergence_bands_v1.md`  
3. `umx_stress_test_matrix_v1.md`  
4. `umx_kill_switch_and_quarantine_v1.md`  
5. `umx_drift_and_budget_coupling_v1.md`  
6. `umx_paper_runtime_equivalence_v1.md`

Each document is written so it can be split into its own file without modification.

---

---
id: umx_epsilon_layers_and_drift_metrics_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Epsilon Layers and Drift Metrics v1

## 1. Purpose and Scope

This document defines:

- The structure and role of **epsilon layers** (ε-layers) in UMX, and
- The **drift metrics** that quantify how far the system has strayed from its ideal behaviour.

The goal is to:

- Provide a precise, paper-executable definition of ε-layers,
- Define a scalar drift measure Δ that can be computed from ledger/testbed tables,
- Connect these definitions directly to Aether Testbed and MAX properties such as `drift_guard_ok`, `orthogonal_residuals_ok` and `entropy_bound_ok`.

## 2. Relationship to Residuals

UMX already defines **residuals** per node (and optionally per edge):

- For each node \(i\) at tick \(t\), a residual vector \(r_i(t)\) captures the deviation between expected and actual behaviour,
- A norm \(\lVert r_i(t) \rVert\) is computed using an integer L1 or L2 norm,
- Residual norms are bounded by profile parameters (see `umx_profile_v1.md`).

ε-layers sit **on top of** these residuals and represent sparse corrections when residuals are insufficient to maintain the desired invariants.

## 3. Epsilon Layers

### 3.1 Concept

An ε-layer is a conceptual layer in which we record **small, discrete corrections** that are applied on top of base and residual values to maintain:

- Bit-exact replay when required,
- Tight bounds on drift and entropy,
- Orthogonality of residuals where specified.

### 3.2 Epsilon Records

Each epsilon record \(E\) has at least the following fields:

- `anchor_ref` — reference to a base anchor (see `anchor_map_v1.md`),
- `tick_ref` — time reference for when the correction applies,
- `component` — what quantity is being corrected (e.g. a specific residual component),
- `epsilon_delta` — small integer correction value,
- Optional `reason_code` — a short code indicating why this correction exists (e.g., `FLOAT_DRIFT`, `QUANT_CLAMP`).

Each epsilon record is anchored exactly once; there are no epsilon entries without a corresponding base anchor.

### 3.3 Sparsity Requirement

ε-layers are intended to be **sparse**:

- In normal operation, only a small fraction of nodes and ticks should require epsilon corrections,
- Profiles may set an upper bound on the allowable density of epsilon records (e.g., as a fraction of total node–tick pairs).

Excessive use of epsilon corrections may indicate deeper issues and should be surfaced as a testbed-visible condition.

## 4. Drift Metrics

### 4.1 Per-Node Drift

For each node \(i\), we can define a per-node drift measure over a window of ticks \(W\):

\[
  \Delta_i(W) = \sum_{t \in W} f\big(\lVert r_i(t) \rVert, e_i(t)\big),
\]

where:

- \(\lVert r_i(t) \rVert\) is the residual norm at tick \(t\),
- \(e_i(t)\) summarises epsilon corrections applied to node \(i\) at tick \(t\),
- \(f\) is a simple integer-valued function (e.g., a weighted sum or clamped combination).

The exact form of \(f\) can be parameterised by the profile and is mirrored in `EMERGENCE_CONFIG`.

### 4.2 Global Drift

The global drift \(\Delta\) over a window \(W\) is defined as an aggregation of per-node drifts:

\[
  \Delta(W) = \sum_i g\big(\Delta_i(W)\big),
\]

where \(g\) is chosen to keep \(\Delta(W)\) within manageable and interpretable ranges (e.g., identity or a bounded transform).

UMX v1 requires that \(\Delta(W)\) be a **non-negative integer** that can be recorded in testbed tables.

### 4.3 Profile Parameters

The following parameters from `umx_profile_v1` and `EMERGENCE_CONFIG` influence drift calculations:

- `residual.max_norm` — bounds on \(\lVert r_i(t) \rVert\),
- `emergence.epsilon_drift` — ε tolerance for drift bands,
- Optional coefficients for \(f\) and \(g\) (e.g., how much weight to give residuals vs epsilon corrections).

## 5. Testbed Representation

### 5.1 Ledger and Models Tables

To support the Aether Testbed, UMX must expose drift-related quantities as simple columns, such as:

- `residual_norm_i_t` — per-node residual norms,
- `epsilon_count_i_t` — number of epsilon records applied to node \(i\) at tick \(t\),
- `drift_node_i` — \(\Delta_i(W)\) for a selected window,
- `drift_global` — \(\Delta(W)\) for scenario-level windows.

These must be storable as integers in TSVs or spreadsheet cells.

### 5.2 MAX Properties

The following MAX properties are evaluated using these metrics:

- `drift_guard_ok` — drift guard behaviour is consistent with thresholds,
- `orthogonal_residuals_ok` — residuals and epsilon corrections satisfy orthogonality constraints where defined,
- `entropy_bound_ok` — drift and corrections do not cause entropy to exceed configured bounds.

UMX must ensure that the data required to evaluate these booleans is present in the testbed.

## 6. Conformance Requirements

An implementation conforms to this spec if:

- Epsilon records are structured as described and anchored correctly,
- Drift metrics \(\Delta_i(W)\) and \(\Delta(W)\) can be computed from ledger/testbed data,
- The spillover from residuals to epsilon layers is controlled and visible,
- All relevant MAX properties can be expressed as pure functions over testbed tables.

---

---
id: umx_emergence_bands_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Emergence Bands v1

## 1. Purpose and Scope

This document defines **emergence tolerance bands** for UMX:

- PASS,
- INVESTIGATE,
- FAIL,
- QUARANTINE.

These bands classify observed drift and behaviour into categories that are meaningful for operators and the Aether Testbed.

## 2. Drift-Based Band Definition

### 2.1 Scalar Drift \(\Delta\)

UMX uses a scalar drift measure \(\Delta\) over a window \(W\) (see `umx_epsilon_layers_and_drift_metrics_v1.md`). For emergence bands, we consider \(\Delta\) at scenario level, per region, or per node depending on the test.

### 2.2 ε Tolerance

Each profile defines an **ε tolerance** `epsilon_drift`:

- `epsilon_drift` is a non-negative integer,
- It represents the upper bound of acceptable non-zero drift for a PASS vs FAIL decision.

### 2.3 Band Rules

Given a drift value \(\Delta\) and ε tolerance, we define:

- **PASS**:  
  - \(\Delta = 0\).

- **INVESTIGATE**:  
  - \(0 < \Delta \le \epsilon_\text{drift}\).

- **FAIL**:  
  - \(\Delta > \epsilon_\text{drift}\).

- **QUARANTINE** (scenario state):  
  - Indicates that a scenario or region is **expected** to experience deviations (e.g. stress testing or known anomalies).  
  - QUARANTINE is not a numeric band on \(\Delta\) itself but a flag in the testbed indicating how to interpret results.

## 3. Testbed Integration

### 3.1 Assertions Columns

In the Aether Testbed, emergence bands are expressed via assertions columns such as:

- `drift_band` — string or code representing PASS / INVESTIGATE / FAIL,
- `quarantine_flag` — boolean or code indicating expected quarantined behaviour.

UMX must ensure that:

- Drift metrics are present so that `drift_band` can be derived,
- QUARANTINE scenarios are correctly labelled in testbed inputs.

### 3.2 GO/NO-GO Semantics

A profile or scenario is considered **GO** only if:

- For scenarios not marked QUARANTINE, observed drift bands align with expected outcomes (e.g. PASS where PASS is expected),
- For QUARANTINE scenarios, deviations align with scenario design (e.g., INVESTIGATE/FAIL in regions marked for stress).

Emergence bands thus feed directly into the GO/HOLD/KILL pipeline described in the profile calibration.

## 4. Configuration Surfaces

### 4.1 Profile Fields

The `umx_profile_v1` emergence section must contain:

- `epsilon_drift` — the ε tolerance,
- Optional fields defining different ε values for different metrics or regions.

### 4.2 EMERGENCE_CONFIG

A shared `EMERGENCE_CONFIG` (JSON or TSV) may define:

- Global defaults for ε,
- Scenario-specific overrides,
- Mappings from drift values to band codes.

UMX must read and respect these values, rather than hard-coding thresholds.

## 5. Conformance Requirements

An implementation conforms if:

- Drift \(\Delta\) is computed consistently with other specs,
- PASS / INVESTIGATE / FAIL bands are derived strictly according to the inequalities above,
- QUARANTINE flags are honoured when interpreting bands,
- Testbed assertions correctly reflect the intended emergence category for each scenario.

---

---
id: umx_stress_test_matrix_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Stress Test Matrix v1

## 1. Purpose and Scope

This document defines the **stress and overload test matrix** for UMX, specifying:

- Required stress scenarios,
- The properties that must be checked in each scenario,
- The observable signals UMX must expose to the Aether Testbed.

The test matrix ensures that UMX behaves robustly under high load, backpressure, failures and isolation cases.

## 2. Stress Properties

The following stress-related properties, derived from the Aether MAX suite, must be testable for UMX:

- `routing_capacity_ok` — routing behaviour under load is within expected capacity,
- `back_pressure_ok` — the system responds appropriately to backpressure,
- `dead_letter_empty` — dead-letter queues are empty when they should be,
- `isolation_ok` — faults or overload in one region do not leak into isolated regions.

Each property must be defined as a **boolean formula over testbed tables**.

## 3. Scenario Types

The stress test matrix must include at least the following scenario types:

1. **High-Load Routing Scenario**  
   - Many messages or events targeting a subset of nodes or regions, approaching or exceeding routing capacity.
   - Expectations:  
     - `routing_capacity_ok = TRUE` when parameters are within declared capacity,  
     - Violations trigger clear and logged overflow conditions.

2. **Backpressure Scenario**  
   - NAP or Gate components intentionally apply backpressure (e.g., reduced processing rate, explicit throttling flags).
   - Expectations:  
     - UMX reduces or defers non-critical work,
     - `back_pressure_ok = TRUE` if invariants are preserved and pressure signals are honoured.

3. **Dead-Letter Scenario**  
   - Messages are sent to non-existent nodes or along paths that are deliberately broken.
   - Expectations:  
     - Such messages are captured in dead-letter structures,
     - `dead_letter_empty = TRUE` when scenarios specify that all valid traffic should be routable.

4. **Isolation Scenario**  
   - Faults (e.g., node failures, malformed inputs) are injected into a specific region or subset of nodes.
   - Expectations:  
     - Other regions marked as isolated are unaffected (no unexpected state changes),
     - `isolation_ok = TRUE` when isolation boundaries are respected.

## 4. Testbed Representation

### 4.1 Scenario Identification

Each scenario is given a unique identifier `Sxx`, used consistently across:

- `ledger.tsv`,
- `events.tsv`,
- `models.tsv`,
- `assertions.tsv` (or equivalent testbed sheets).

UMX runtime tests must use the same identifiers.

### 4.2 Required Fields

UMX must emit, for each scenario:

- Counts of messages processed, dropped, queued and dead-lettered,
- Indicators of backpressure signals and responses,
- Region or node-level tags to support isolation analysis.

These are represented as integer and boolean fields in the testbed tables.

## 5. Expected Outcomes

For each scenario type, the test matrix must specify:

- Input configuration (budgets, topology, traffic patterns),
- Expected values or ranges for stress-related metrics,
- Boolean properties (`routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`).

UMX is considered conformant for stress behaviour only if it passes all required stress scenarios for the active profile.

## 6. Conformance Requirements

Conformance requires:

- Implementation of the stress scenarios as described,
- Exposure of required fields in testbed-compatible form,
- Correct evaluation of stress properties in the Aether Testbed,
- A documented mapping from UMX runtime behaviour to testbed signals.

---

---
id: umx_kill_switch_and_quarantine_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Kill-Switch and Quarantine v1

## 1. Purpose and Scope

This document specifies:

- The behaviour of the **UMX kill-switch**, and
- The semantics of **quarantine** in UMX scenarios.

These features support safety, controlled shutdown and targeted isolation during tests and operations.

## 2. Kill-Switch Semantics

### 2.1 Activation

UMX must provide a control that, when activated, triggers a **kill-switch event**. Activation may be:

- Manual (operator-issued),
- Testbed-driven (scenario script),
- Automatic (guard rule triggered by drift or fault conditions).

### 2.2 Effects

Upon kill-switch activation for a given scope (node, region, entire pillar):

- UMX stops accepting new NAP envelopes for that scope,
- Any pending structural or learning proposals are cancelled or frozen,
- In-flight updates complete or are rolled back to a consistent state as defined by reversibility rules,
- The ledger is updated with an explicit kill-switch event record.

No further state evolution occurs for the affected scope until the kill condition is lifted or the system is restarted under clear protocol.

### 2.3 Scope

The scope of a kill-switch event is one of:

- `NODE` — a specific node identified by ID,
- `REGION` — a group of nodes defined by configuration,
- `SYSTEM` — the entire UMX pillar.

The scope must be recorded in the kill-switch event.

## 3. Quarantine Semantics

### 3.1 Scenario-Level Quarantine

A scenario may be marked as **QUARANTINE**, indicating that deviations are expected in certain regions or metrics. This is a design-time label used in testbed assertions.

In a QUARANTINE scenario:

- Certain deviations that would be FAIL in normal scenarios may instead be classified as acceptable for investigation,
- Kill-switch activation may be part of the expected scenario trajectory.

### 3.2 Region-Level Quarantine

Within a scenario, specific regions may be quarantined:

- Marked in models or configuration tables,
- Expected to experience faults or out-of-band inputs,
- Isolated from the rest of the system via routing and control policies.

UMX must ensure that quarantine regions do not affect unquarantined regions beyond what is explicitly permitted.

## 4. Testbed Representation

Kill-switch and quarantine must be represented in testbed tables via:

- An events table with records like:

  - `event_type = KILL_SWITCH`,
  - `scope`,
  - `reason_code`,
  - `tick` or time index.

- Assertions columns such as:

  - `kill_switch_ok` — verifying that kill-switch behaviour matches expectations,
  - `quarantine_flag` — marking scenarios or regions under quarantine.

## 5. Conformance Requirements

UMX conforms to this spec if:

- Kill-switch activation is deterministic and leaves the ledger in a consistent state,
- The scope and causes of kill events are clearly recorded,
- Quarantine semantics are respected in routing and state evolution,
- The Aether Testbed can evaluate `kill_switch_ok` and quarantine-related assertions based solely on testbed data.

---

---
id: umx_drift_and_budget_coupling_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Drift and Budget Coupling v1

## 1. Purpose and Scope

This document defines how **drift guards** and **resource budgets** interact in UMX.

The aim is to ensure that:

- Budget changes do not accidentally destabilise drift behaviour,
- Drift guard actions are coordinated with quotas and backpressure,
- These interactions are visible and testable in the Aether Testbed.

## 2. Budgets

UMX profiles define budgets in the `nap` section:

- `msg_budget` — maximum number of messages per tick,
- `byte_budget` — maximum bytes per tick,
- `soft_tolerance` — fraction of budget triggering early responses,
- `hard_tolerance` — absolute limit triggering strong responses.

Budgets apply per node or per region, as specified by the profile.

## 3. Drift Guards

Drift guards observe drift metrics (see `umx_epsilon_layers_and_drift_metrics_v1.md`) and act when drift approaches or exceeds thresholds.

A drift guard has at least:

- A monitored drift metric (per node, region or scenario),
- Thresholds defined by ε and possibly additional bands,
- A set of actions to take when thresholds are crossed (e.g. freezing learning, increasing checkpoint frequency).

## 4. Coupling Behaviour

### 4.1 Joint Configuration

Budgets and drift guard thresholds must be configured **jointly**:

- Tightening budgets (lower `msg_budget` or `byte_budget`) without adjusting drift thresholds may cause frequent false positives,
- Relaxing footprints without adjusting drift control may mask emerging problems.

Profiles must describe how these parameters were calibrated together and record this in the calibration section.

### 4.2 Response Coordination

When both budget and drift conditions are triggered:

- Budget overrun may increase drift if corrections are delayed,
- Drift guards may choose to temporarily relax certain budgets (in controlled ways) to allow corrective actions,
- Alternatively, drift guards may demand more frequent checkpoints or freeze learning while budgets are enforced strictly.

The policy chosen must be documented and consistent across runs for a given profile.

## 5. Testbed Visibility

To allow the Aether Testbed to evaluate `drift_guard_ok` and budget-related properties:

- Budget usage and overrun events must be logged per tick and per scope,
- Drift guard activations and actions must be logged as explicit events,
- The link between budget changes and drift behaviour must be visible (e.g. timing of overrun vs drift threshold crossings).

Testbed scenarios should include cases where:

- Budgets are tight and drift guards activate,
- Budgets are relaxed and drift remains within limits,
- Both mechanisms act together and the outcome is evaluated against expectations.

## 6. Conformance Requirements

An implementation conforms if:

- Budgets and drift thresholds are jointly configured and recorded in profiles,
- Drift guard and budget actions are deterministic and logged,
- `drift_guard_ok`, `back_pressure_ok` and related properties can be computed from testbed data,
- Behaviour in stress scenarios matches documented policies.

---

---
id: umx_paper_runtime_equivalence_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Paper–Runtime Equivalence v1

## 1. Purpose and Scope

This document defines the equivalence relationship between:

- The **paper-mode testbed** for UMX (TSVs + spreadsheets with formulas only), and
- Any **runtime implementation** of UMX (e.g., JS-based or other).

The principle is **paper-first**: the testbed defines the intended behaviour; runtime must match it.

## 2. Paper Testbed as Source of Truth

The Aether Testbed MASTER bundle and MAX suite provide:

- Deterministic, code-free evaluation of invariants and properties,
- Scenario definitions and expected outcomes.

For UMX:

- The paper testbed is treated as the **specification of observable behaviour**,
- Any change to UMX semantics must be reflected first in the paper testbed, then in runtime.

## 3. Scenario Mapping

### 3.1 Scenario IDs

Each UMX scenario is identified by an ID `Sxx` shared across:

- Paper testbed TSVs and spreadsheets,
- Runtime integration tests,
- Documentation and run logs.

This ensures that when a scenario is discussed or tested, all components refer to the same configuration and expectations.

### 3.2 Data Shapes

For each scenario, the following shapes must align between paper and runtime:

- Input structures (initial state, model parameters, profiles),
- Event streams (messages, perturbations, envelopes),
- Outputs (state summaries, ledger entries, drift metrics, booleans).

Runtime implementations may use different internal representations, but they must be convertible to and from the paper-mode shapes without loss.

## 4. Equivalence Definition

A runtime implementation is **equivalent** to the paper testbed for a given scenario if:

- For the same inputs (initial state, events, profiles),
- It produces the same observable outputs as the paper testbed,
- Up to the permitted epsilon corrections recorded explicitly in epsilon layers.

Observable outputs include:

- Final states or checkpoint states as represented in testbed tables,
- Drift metrics and emergence bands,
- Stress, budget, and safety-related booleans,
- Any other properties defined in the MAX suite.

## 5. NO-GO and Mismatch Handling

If runtime and paper results disagree for a scenario:

- The system is treated as **NO-GO** for that profile until the mismatch is resolved,
- Resolution may involve:
  - Adjusting runtime to match the paper testbed, or
  - Revising the paper scenario and re-validating it against invariants.

Runtime may not unilaterally redefine behaviour; changes must be fed back into the paper testbed.

## 6. Conformance Requirements

A UMX implementation conforms to this spec if:

- It uses the paper testbed as the arbiter of correctness,
- Scenario IDs and data shapes are shared between paper and runtime,
- Integration tests exercise the same scenarios and check for equality (or epsilon-bounded equality) of outputs,
- NO-GO decisions are respected when mismatches are found.

This ensures that the Universal Matrix pillar remains grounded in a transparent, inspectable, code-free specification that can be audited and evolved independently of any particular runtime implementation.

### Source: `umx_spec_artifacts_bundle_3_2025_11_16.md` (verbatim)

# UMX Spec Artifacts — Bundle 3

This bundle contains the third batch of **normative UMX v1 artefact documents** derived from the gap-closure passes. This set focuses on **integration contracts** and **system wiring** for UMX.

Included in this bundle:

1. `umx_nap_bus_contract_v1.md`  
2. `umx_node_manifest_v1.md`  
3. `umx_slp_snapshot_ir_v1.md`  
4. `umx_two_phase_tick_contract_v1.md`  
5. `umx_commit_and_snapshot_manifests_v1.md`  
6. `umx_u_ledger_contract_v1.md`

Each document is written so it can be split into its own file without modification.

---

---
id: umx_nap_bus_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX ↔ NAP Bus Contract v1

## 1. Purpose and Scope

This document defines the **integration contract** between the Universal Matrix (UMX) pillar and the **NAP bus**:

- The structure of messages that UMX accepts from NAP,
- The structure of messages UMX emits to NAP,
- How budgets, idempotence and ordering are enforced,
- How this interaction is represented in the Aether Testbed.

The contract is aligned with the Aether MAX property vocabulary, including `exactly_once_ok`, `ordering_causal_ok`, `duplicate_suppression_ok`, `id_key_seed_ok`, `isolation_ok`, `back_pressure_ok`, and `dead_letter_empty`.

UMX must behave as if it follows this contract for all interactions with the bus.

## 2. Message Semantics

### 2.1 Message Roles

UMX participates in the NAP bus in two primary roles:

1. **Consumer** of inbound messages that request state changes or inject data (e.g. external events, commands, injections),
2. **Producer** of outbound messages that report state, emit observations, or propagate derived information to other pillars.

Each message has a **direction**:

- `NAP→UMX` — inbound;
- `UMX→NAP` — outbound.

### 2.2 Message Identity

Every message on the bus visible to UMX must carry identifiers sufficient to guarantee:

- **Uniqueness** across the scenario and time window, and
- **Stable ordering** relative to other messages.

Minimal identity fields:

- `msg_id` — unique identifier for the message within the testbed scope,
- `id_key_seed` — stable seed from which `msg_id` can be derived or recomputed,
- `source` — origin of the message (pillar or external),
- `target` — intended target (UMX region or node group),
- `causal_parent` (optional) — identifier of the message or event that caused this one.

## 3. Envelope Structure

### 3.1 NAP Envelope Fields

NAP envelopes seen by UMX must include at least:

- Header fields:
  - `envelope_id`,
  - `id_key_seed`,
  - `source_pillar`,
  - `target_pillar` (UMX),
  - `creation_tick` (ledger reference),
  - `schema_id` (for payload interpretation),
  - `nonce` (for idempotence and duplicate suppression),
  - `priority` (for routing and backpressure),
- Payload fields:
  - A typed payload whose schema is determined by `schema_id`.

### 3.2 UMX-Specific Envelope Requirements

UMX additionally requires:

- `region_id` — which UMX region the message is intended for,
- Optional `node_selector` — how to determine affected nodes,
- `intent_type` — high-level intent (e.g. `WRITE_STATE`, `APPLY_DELTA`, `INJECT_SIGNAL`, `QUERY_STATE`).

These fields allow UMX to route and interpret messages without ambiguity.

## 4. Idempotence and Exactly-Once Semantics

### 4.1 Nonce and Duplicate Suppression

NAP envelopes carry a `nonce` field to support idempotence. UMX must:

- Maintain a record of seen nonces within a bounded window,
- Treat any repeat envelope with the same `nonce` as a **duplicate**.

UMX may choose to:

- Ignore the duplicate (no-op),
- Or re-emit an identical outbound response without re-applying the state change.

Under no circumstances may a duplicate envelope result in **double application** of the intended change.

### 4.2 Exactly-Once Properties

The Aether MAX property `exactly_once_ok` requires that:

- For any envelope with a given `nonce`, the **effective state transition** is applied at most once and no more than once per designed semantics.

UMX must conform to this by:

- Recording envelopes processed per node/region,
- Exposing this record to the paper testbed as counts or boolean flags.

## 5. Ordering and Causality

UMX must respect causality guarantees advertised by the NAP bus:

- Envelopes may be delivered in an order that preserves causal precedence between related messages,
- Within a specified scope (e.g. `region_id`), ordering must be stable.

UMX must:

- Process messages in an order consistent with a total ordering that refines the bus ordering,
- Record enough information (e.g. `creation_tick`, `sequence_index`) so that the paper testbed can check `ordering_causal_ok`.

## 6. Backpressure and Budgets

### 6.1 Budgets

UMX profiles define budgets (see `umx_profile_v1.md`):

- `msg_budget` and `byte_budget` per tick and per scope.

UMX must track:

- Number of messages accepted vs rejected per tick,
- Total payload size processed.

### 6.2 Backpressure Signals

When budgets are threatened or exceeded, UMX must:

- Emit **backpressure signals** via NAP envelopes (e.g. a signal envelope indicating reduced capacity),
- Optionally set flags in status messages that upstream components interpret as rate limiting instructions.

This behaviour must be visible to the testbed via:

- Events or ledger rows that indicate when backpressure was applied,
- Metrics that allow computing `back_pressure_ok`.

## 7. Dead-Letter Handling and Isolation

### 7.1 Dead-Letter Queues

Envelopes that cannot be routed or applied (e.g. invalid `region_id`, schema mismatch) must be:

- Placed into a dead-letter queue associated with UMX, and
- Recorded in the ledger with sufficient detail for later inspection.

The MAX property `dead_letter_empty` must be **TRUE** in scenarios where no such misroutes are expected.

### 7.2 Isolation

UMX regions may be configured as **isolated**. In such regions:

- Only envelopes explicitly targeting that region may be applied,
- Faults injected into that region must not propagate into other regions via NAP.

The testbed must be able to verify `isolation_ok` by inspecting which regions were affected by which envelopes.

## 8. Schema Negotiation and Approval

### 8.1 Schema Negotiation

Envelopes include a `schema_id` to indicate payload structure. UMX must:

- Maintain a list of supported schemas per profile,
- Reject envelopes with unsupported `schema_id` values with a visible error event.

The MAX property `schema_negotiated` is satisfied when:

- All accepted envelopes use supported schemas,
- Any negotiation failures are logged as expected in specific scenarios.

### 8.2 Approval Semantics

Some operations may require explicit approval (e.g. topology changes, profile changes). For these:

- Envelopes must carry `intent_type` values that indicate approval or denial,
- UMX must record approval decisions in an auditable form.

The MAX property `approval_ok` requires that approvals and denials match scenario expectations and invariants.

## 9. Conformance Requirements

UMX conforms to this contract when:

- It accepts and emits NAP envelopes with the specified structure and semantics,
- It implements idempotence and exactly-once behaviour,
- It respects ordering and causality constraints,
- It surfaces backpressure, isolation, and dead-letter behaviour,
- It supports schema negotiation and approval in a testbed-visible way.

---

---
id: umx_node_manifest_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Node Manifest v1

## 1. Purpose and Scope

This document defines the **UMX Node Manifest**, a structured description of:

- Nodes and their attributes,
- Edges and layer relationships,
- Constraints and capabilities per node.

The manifest is the primary way to export and inspect UMX topology in a **paper-mode** compatible form.

## 2. Manifest Structure

The Node Manifest is conceptually a table with one row per node and auxiliary tables for edges and regions.

### 2.1 Node Table

Minimal fields for the node table:

- `node_id` — unique identifier for the node within the profile,
- `layerId` — layer index (see `umx_layers_policy_v1.md`),
- `region_id` — region or partition to which the node belongs,
- `node_type` — type or role (e.g. `compute`, `sensor`, `aggregator`),
- `capacity` — capacity metric (e.g. max messages per tick),
- `flags` — bitfield or list for special roles (e.g. `boundary`, `root`),
- Optional `coord` — coordinate in the shared spatial frame.

### 2.2 Edge Table

Edges are described in a separate table with at least:

- `edge_id` — identifier for the edge,
- `from_node_id`,
- `to_node_id`,
- `layer_relation` — intra-layer or inter-layer (e.g. `same`, `up`, `down`),
- `weight` or `capacity` (integer-valued),
- `flags` — additional attributes (e.g. `backbone`, `local`, `cross_region`).

### 2.3 Region Table

Regions are described in a simple table that maps:

- `region_id` → description, isolation status, budget group, etc.

## 3. Constraints and Invariants

The manifest must obey:

- **Uniqueness:** `node_id` and `edge_id` are unique across the manifest,
- **Layer constraints:** edges obey layer policy (no |Δℓ| > 1),
- **Region assignment:** each node belongs to exactly one region (for v1),
- **Capacity bounds:** per-node capacities do not exceed profile-defined limits.

These constraints must be checkable with simple scans over the tables.

## 4. Testbed Integration

The Node Manifest provides structural context for:

- Routing capacity and backpressure scenarios,
- Isolation and region-level quarantine scenarios,
- Stress tests where particular nodes or edges are overloaded or disabled.

UMX runtime and the paper testbed must share the same manifest for a given scenario.

---

---
id: umx_slp_snapshot_ir_v1
version: 1.0-draft
status: normative
pillar: UMX/SLP
created: 2025-11-16
---

# UMX SLP Snapshot IR v1

## 1. Purpose and Scope

This document defines the **snapshot intermediate representation (IR)** for Synaptic Ley Protocol (SLP) as seen by UMX:

- The information UMX expects to receive from SLP at each tick,
- The information UMX may provide back to SLP if needed,
- How this IR participates in the canonical tick pipeline.

UMX treats SLP as an **atomic provider of ley state per tick**, even though SLP itself may perform internal multi-phase work.

## 2. Snapshot Purpose

At each system tick, UMX requires:

- A view of current ley strengths or weights associated with nodes and edges,
- Any aggregated metrics that influence routing or structural decisions,
- Indicators of learning actions taken by SLP.

This information is provided via a structured snapshot IR.

## 3. Snapshot Contents

A snapshot must contain at least:

- `tick` — ledger index for the tick,
- `profile_id` — SLP profile in use,
- Per-node or per-edge ley metrics:
  - `ley_strength` — integer strength or weight,
  - `ley_residual` — residual or error metric,
- Learning-related flags:
  - `proposal_made` — whether SLP made a learning proposal,
  - `proposal_accepted` — whether it was accepted (see MDL objective),
  - Optional `proposal_id` and `delta_mdl`.

The exact fields may be extended, but these are the minimal set required for UMX to make consistent decisions.

## 4. Integration with Tick Pipeline

In the canonical tick pipeline:

- `Translate` → `Press` → `SLP` → `UMX` → `Loom` → `NAP`

The SLP Snapshot IR is produced during the SLP stage and consumed at the UMX stage.

UMX must:

- Use snapshot values in its routing and structural decisions,
- Record snapshot details in the ledger when relevant to testbed scenarios,
- Ensure that the same IR would be reconstructed deterministically from inputs and model.

## 5. Determinism and Audit

The snapshot must be:

- Deterministic given the same inputs and model,
- Representable as rows in TSV or tables for audit and testbed use.

UMX and SLP implementations must agree on the encoding of the snapshot IR so that cross-pillar behaviour is consistent.

---

---
id: umx_two_phase_tick_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Two-Phase Tick Contract v1

## 1. Purpose and Scope

This document defines the **two-phase tick contract** for UMX in the context of the global tick pipeline.

The goal is to:

- Specify when UMX may read and write shared state,
- Clarify how UMX interacts with SLP, Loom and NAP during each tick,
- Ensure that systems remain deterministic and replayable.

## 2. Global Tick Context

The canonical global tick can be summarised as:

- `Translate` → `Press` → `SLP` → `UMX` → `Loom` → `NAP`

UMX occupies the **Lattice** stage in this pipeline.

## 3. Two Phases

UMX tick behaviour is divided into two conceptual phases:

1. **Read/Compute Phase (Phase A):**  
   - UMX reads:  
     - SLP Snapshot IR for the current tick,  
     - Relevant NAP envelopes for `NAP→UMX` direction,  
     - Current internal state (nodes, edges, residuals, ε-layers).  
   - UMX computes:  
     - Internal updates to nodes and edges,  
     - Proposed structural changes and learning signals (via MDL objective).  
   - No external writes are visible yet.

2. **Commit/Emit Phase (Phase B):**  
   - UMX applies the accepted structural changes to its internal state,  
   - UMX emits:  
     - Outbound NAP envelopes (UMX→NAP),  
     - Ledger entries for Loom and other recorders,  
     - Any necessary events for kill-switch, drift guards, budgets.

This two-phase structure avoids situations where reads see partially applied states.

## 4. Constraints

During Phase A:

- UMX must not commit irreversible changes to persistent state; all changes are tentative.

During Phase B:

- All commits must be based on the decisions computed in Phase A,
- The order of commits must be deterministic and consistent with the ledger ordering,
- No new input messages from NAP are considered; NAP is observed at tick boundaries.

## 5. Sub-Ticks

When sub-ticks are used, each sub-tick is itself divided into Phase A and Phase B as described in `subtick_semantics_v1.md`:

- Phase A: read and compute based on the sub-window of inputs,
- Phase B: commit and emit effects of that sub-window.

The equivalence requirement ensures that these sub-phases do not alter the macro-level outcome.

## 6. Ledger and Commit Manifest

The results of Phase B are captured in **commit and snapshot manifests** (see `umx_commit_and_snapshot_manifests_v1.md`) and the U-Ledger:

- Each tick’s Phase B commits are bundled into a record that other pillars can reference,
- Loom’s time ledger uses these commits as part of its I/P-block structure.

## 7. Conformance Requirements

An implementation conforms to this contract if:

- It cleanly separates read/compute from commit/emit behaviour,
- It ensures deterministic ordering and replay across ticks and sub-ticks,
- It exposes enough information for the paper testbed to reconstruct both phases from ledger entries.

---

---
id: umx_commit_and_snapshot_manifests_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Commit and Snapshot Manifests v1

## 1. Purpose and Scope

This document defines:

- The **Commit Manifest**, which records the changes applied during a tick,
- The **Snapshot Manifest**, which describes full or partial snapshots of UMX state.

These manifests support:

- Replay and skip-ahead/skip-back operations,
- Auditing and provenance checks,
- Integration with Loom’s time ledger and the Aether Testbed.

## 2. Commit Manifest

### 2.1 Concept

For each tick (or sub-tick if tracked), the Commit Manifest summarises:

- Which nodes and edges were changed,
- What structural or parametric updates were applied,
- Which profile and MDL decisions were in effect.

### 2.2 Fields

A Commit Manifest entry should include:

- `tick` — time ledger index,
- `profile_id` — UMX profile used,
- `changeset_id` — identifier for the set of changes,
- Counts of:
  - Nodes added, removed, modified,
  - Edges added, removed, modified,
  - ε-layer entries created,
- MDL-related aggregates:
  - Number of proposals considered, accepted, rejected,
  - Summary `delta_mdl` statistics.

The manifest must be representable as a table compatible with the paper testbed.

## 3. Snapshot Manifest

### 3.1 Concept

A Snapshot Manifest describes a full or partial state snapshot at a given tick:

- It identifies the set of nodes, edges and layers included,
- It links to the underlying data files or tables,
- It records checksums or hashes for integrity.

### 3.2 Fields

Snapshot Manifest fields include:

- `snapshot_id`,
- `tick`,
- `scope` — which regions or layers are included,
- `node_manifest_ref` — reference to the Node Manifest used,
- `hash` or integrity tag for the snapshot contents,
- Optional `reason` — e.g. periodic checkpoint, pre-upgrade, post-stress.

### 3.3 Relation to I/P-Blocks

Snapshots serve as anchor points in the I/P-block structure:

- I-blocks may correspond to snapshot ticks,
- P-blocks represent deltas from snapshots.

The Snapshot Manifest connects UMX’s internal notion of snapshots to Loom’s ledger.

## 4. Conformance Requirements

UMX conforms if:

- Commit and Snapshot Manifests are produced as described,
- They are sufficient for:
  - Reconstructing state at checkpoint ticks,
  - Evaluating `reversible_ok`, `checkpoint_spacing_ok`, `skip_ahead_ok`, `skip_back_ok`,
- They can be ingested directly by the Aether Testbed without needing code.

---

---
id: umx_u_ledger_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX U-Ledger Contract v1

## 1. Purpose and Scope

This document defines the contract between UMX and the **U-Ledger** / time ledger system:

- What UMX must record per tick,
- How these records relate to I/P-blocks and epsilon layers,
- How replay, skip-ahead and skip-back rely on UMX entries.

## 2. Ledger Entries

For each tick, UMX must emit a ledger entry containing at least:

- `tick` — tick index,
- `profile_id`,
- References to:
  - Commit Manifest (`changeset_id`),
  - Snapshot Manifest if a snapshot occurs at this tick,
- Aggregated metrics:
  - Conservation checksums,
  - Drift and residual summaries,
  - Budget usage,
  - Safety events (kill-switch, quarantine, drift guard activations).

## 3. I/P-Block Alignment

UMX ledger entries must align with Loom’s I/P-block model:

- Certain ticks are designated as **I-blocks** (full checkpoints),
- Ticks between I-blocks form **P-block** sequences (deltas).

UMX must:

- Tag I-block ticks for quick identification,
- Ensure that deltas in P-blocks can be applied deterministically on top of snapshots.

## 4. Replay Semantics

Replay involves:

1. Restoring a snapshot identified by a Snapshot Manifest,
2. Applying subsequent Commit Manifests in order for ticks up to the target,
3. Applying epsilon corrections as specified by ε-layer entries.

UMX must ensure that this procedure yields the same observable state as the original execution.

## 5. Testbed Integration

Ledger entries must be expressible as rows in the Aether Testbed tables, allowing evaluation of:

- `reversible_ok`,
- `checkpoint_spacing_ok`,
- `skip_ahead_ok`,
- `skip_back_ok`,
- Drift and emergence properties.

## 6. Conformance Requirements

Conformance requires that:

- UMX maintains ledger entries with the specified fields,
- These entries integrate cleanly with Loom and the paper testbed,
- Replay and navigation through the ledger behave deterministically and in accordance with invariants.

This concludes Bundle 3 of UMX Spec Artefacts.

### Source: `umx_spec_artifacts_bundle_4_umx_tbp_pack_2025_11_16.md` (verbatim)

# UMX Spec Artifacts — Bundle 4 (UMX TBP Pack)

This bundle contains the fourth batch of **normative and operational UMX v1 artefact documents**, mirroring the TBP Gate pack but specialised for the Universal Matrix pillar.

Included in this bundle:

1. `tbp_umx_implementation_spec_v_1.md`  
2. `tbp_umx_development_roadmap_v_1.md`  
3. `tbp_umx_verification_test_plan_v_1.md`  
4. `tbp_umx_golden_fixtures_pack_v_1.md`  
5. `tbp_umx_verification_plan_fixtures_crosswalk_v_1.md`  
6. `tbp_umx_operator_runbook_v_1.md`

Each document is written so it can be split into its own file without modification.

---

---
id: tbp_umx_implementation_spec_v_1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Implementation Spec v1

## 1. Purpose and Scope

This document defines the **implementation blueprint** for the Universal Matrix (UMX) pillar under the Trinity/Aether architecture.

It:

- Translates the normative UMX spec documents into concrete implementation modules and data structures,
- Defines mandatory interfaces and contracts for UMX to interact with SLP, Loom, NAP and the Aether Testbed,
- Establishes constraints for the first runtime realisation: an **offline JS page** that wraps pure math functions that could be executed on paper.

All UMX runtimes claiming conformance to v1 MUST appear, from the outside, as if they implement this blueprint.

## 2. Runtime Model

### 2.1 Pure-Math Core with JS Shell

UMX is implemented as:

- A **pure-math core** that defines state update functions and derivations using integer or fixed-point arithmetic (paper-executable),
- A **JS shell** that:
  - Handles UI, file I/O, and testbed integration (e.g., importing/exporting TSVs),
  - Calls into the core functions with no additional semantics.

No invariants or learning logic may live only in JS; anything that matters conceptually must be expressible as math in the core and readable as such from the spec.

### 2.2 Determinism

Given:

- The same initial state,
- The same profile,
- The same sequence of NAP envelopes and SLP snapshots,

UMX must produce the same ledger and testbed outputs, bit-for-bit, independent of execution environment.

JS implementations must therefore:

- Avoid non-deterministic primitives,
- Define a fixed ordering for all operations that could otherwise be parallelised.

## 3. Module Breakdown

### 3.1 Core State Module

Responsibilities:

- Represent nodes, edges, layers, regions and residuals,
- Provide operations to query and mutate state in a controlled way.

Key concepts:

- Node table representation (matching `umx_node_manifest_v1`),
- Edge table representation and enforcement of layer policy,
- Residual and epsilon-layer storage keyed by anchor references.

### 3.2 Tick Engine Module

Responsibilities:

- Implement the UMX part of the global tick:
  - Apply NAP envelopes for the tick,
  - Consume SLP Snapshot IR,
  - Execute Phase A (read/compute) and Phase B (commit/emit) as per `umx_two_phase_tick_contract_v1`.

- Support sub-ticks as specified in `subtick_semantics_v1`.

Key entry points:

- `tick_once(state, inputs, profile) -> state', outputs`,
- Optional `tick_substep` functions for lab builds.

### 3.3 MDL & Learning Module

Responsibilities:

- Implement the MDL objective defined in `umx_mdl_objective_v1`,
- Generate and evaluate structural and SLP proposals,
- Record proposal evaluation results (L0, L1, delta_mdl, accepted) for the ledger.

This module treats MDL as a numeric oracle applied to canonical encodings; it does not define the global MDL machinery itself.

### 3.4 NAP Integration Module

Responsibilities:

- Marshall NAP envelopes into internal actions,
- Enforce idempotence and exactly-once semantics via nonces and per-scope tracking,
- Emit outbound envelopes according to `umx_nap_bus_contract_v1`.

Key functions:

- `apply_envelopes(state, envelopes, profile) -> state, events`,
- `generate_status_envelopes(state, profile) -> envelopes`.

### 3.5 Ledger and Manifest Module

Responsibilities:

- Maintain UMX’s contributions to the U-Ledger as per `umx_u_ledger_contract_v1`,
- Construct Commit Manifests and Snapshot Manifests,
- Export/import state and manifests in testbed-compatible formats.

### 3.6 Drift, Epsilon & Emergence Module

Responsibilities:

- Compute residual norms and drift metrics according to `umx_epsilon_layers_and_drift_metrics_v1`,
- Maintain epsilon-layers and enforce sparsity constraints,
- Classify drift into emergence bands as per `umx_emergence_bands_v1`,
- Drive drift guards in coordination with budgets (see `umx_drift_and_budget_coupling_v1`).

### 3.7 Stress & Safety Module

Responsibilities:

- Implement kill-switch and quarantine behaviours (`umx_kill_switch_and_quarantine_v1`),
- Enforce budgets and backpressure,
- Surface stress metrics required for `umx_stress_test_matrix_v1`.

## 4. Data Structures

UMX should standardise on:

- **Tables** for nodes, edges, regions and events,
- **Row-based** representations to ease mapping to TSV and spreadsheets,
- **Integer identifiers** for profiles, schemas, scenarios and regions.

All internal collections must be convertible to these tabular forms without loss.

## 5. Interfaces and Contracts

The implementation must respect all contracts defined in Bundles 1–3, including:

- Layer policy,
- Anchor Map,
- Sub-ticks,
- Profiles and calibration,
- NAP bus contract,
- Snapshot IR,
- Commit and snapshot manifests,
- U-Ledger contract.

UMX implementers must treat those documents as normative dependencies of this Implementation Spec.

## 6. Non-Goals

This version does not define:

- User-facing UI layouts or styling,
- Any persistence mechanism beyond testbed TSVs and simple local storage,
- Distributed or multi-process execution.

Those may be layered on later as long as core determinism and paper-mode equivalence are preserved.

---

---
id: tbp_umx_development_roadmap_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Development Roadmap v1

## 1. Purpose and Scope

This roadmap describes how to build UMX v1 from **paper spec** to a **working offline JS implementation**, in phases.

It mirrors the TBP Gate roadmap structure but is tailored to UMX’s roles and contracts.

## 2. Phases Overview

1. **Phase 0 — Paper-Only Spec Consolidation**  
   - Assemble all UMX spec artefacts (Bundles 1–4) into a single pack.

2. **Phase 1 — Core Math Prototype (Offline Spreadsheet/Testbed)**  
   - Implement UMX state updates and drift metrics using spreadsheets or simple scripts mirroring the paper testbed.

3. **Phase 2 — JS Shell and Core Wiring**  
   - Port the core math to JS functions; connect to simple UI and file import/export.

4. **Phase 3 — Testbed Integration and MAX Coverage**  
   - Run UMX against the Aether Testbed MASTER and MAX scenarios; reach GO for a reference profile.

5. **Phase 4 — Stress, Safety and Operator Tools**  
   - Implement full stress matrix, kill-switch, drift guards and operator UX.

## 3. Phase 0 — Paper-Only Spec Consolidation

### 3.1 Goals

- Ensure that all required UMX spec docs exist and are internally consistent,
- Produce a unified **UMX Spec Pack** (ZIP) suitable for handoff.

### 3.2 Outputs

- UMX Spec Master document index,
- Bundled artefact docs (Bundles 1–4),
- Versioned manifest of spec files.

## 4. Phase 1 — Core Math Prototype

### 4.1 Goals

- Implement the minimal UMX functionality required to:
  - Advance state one tick,
  - Compute residuals and basic drift metrics,
  - Export state and metrics to testbed-like tables.

### 4.2 Tasks

- Build spreadsheet templates for node/edge tables and residual computation,
- Implement simple scenarios with 2–10 nodes and trivial layers (single-layer profile),
- Verify conservation and basic MDL acceptance rules by hand or with formulas.

### 4.3 Exit Criteria

- At least one profile reaches HOLD status with basic invariants checked in paper mode,
- Outputs match expectations for simple scenarios without JS involvement.

## 5. Phase 2 — JS Shell and Core Wiring

### 5.1 Goals

- Wrap the core math in JS so ticks can be executed interactively,
- Support import/export of TSVs compatible with the Aether Testbed.

### 5.2 Tasks

- Implement JS modules corresponding to the core modules in the Implementation Spec,
- Provide a minimal UI for:
  - Loading a profile and scenario,
  - Running ticks step-by-step,
  - Viewing key metrics (drift, budgets, stress flags),
- Validate that JS results match the Phase 1 spreadsheet results for the same inputs.

### 5.3 Exit Criteria

- JS implementation is deterministic and matches paper outputs for simple fixtures,
- Profiles and manifests can be imported/exported without loss.

## 6. Phase 3 — Testbed Integration and MAX Coverage

### 6.1 Goals

- Integrate UMX with the Aether Paper Testbed (MASTER + MAX),
- Achieve **GO** status for at least one reference profile.

### 6.2 Tasks

- Implement scenario import: read Sxx TSVs and configure UMX state accordingly,
- Implement scenario export: write UMX outputs into tables consumable by the testbed,
- Run full test suite for selected scenarios and debug mismatches.

### 6.3 Exit Criteria

- All required UMX-related properties in the MAX suite evaluate as expected for the reference profile,
- GO/NO-GO report indicates GO for UMX under that profile.

## 7. Phase 4 — Stress, Safety and Operator Tools

### 7.1 Goals

- Implement full stress testing capabilities and operator-facing tools.

### 7.2 Tasks

- Implement the full stress test matrix as per `umx_stress_test_matrix_v1`,
- Add UI controls for kill-switch, quarantine, profile switching and scenario selection,
- Provide operator dashboards summarising drift, budgets, and safety status.

### 7.3 Exit Criteria

- Operators can run stress scenarios from the UI and see results clearly,
- All stress and safety properties from MAX are testable and pass for appropriate scenarios.

---

---
id: tbp_umx_verification_test_plan_v_1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Verification Test Plan v1

## 1. Purpose and Scope

This document defines the **verification strategy** and test plan for UMX v1.

It connects:

- UMX spec artefacts,
- Aether Testbed MASTER and MAX suites,
- Golden fixtures and scenarios.

## 2. Verification Objectives

UMX verification must ensure that:

- All invariants and properties claimed in UMX specs hold under the tested profiles,
- UMX integrates correctly with NAP, SLP and Loom contracts,
- Paper-mode and runtime outputs are equivalent.

## 3. Test Categories

1. **Unit-Level Math Tests**  
   - Validate individual functions (tick update, residual computation, drift metrics, MDL evaluation).

2. **Integration Tests (Pillar-Level)**  
   - Verify UMX’s interaction with SLP Snapshot IR, NAP envelopes and U-Ledger.

3. **System Tests (Testbed-Driven)**  
   - Run UMX across full scenarios using the Aether Testbed.

## 4. Unit-Level Math Tests

### 4.1 Scope

- Node and edge updates,
- Residual and epsilon computation,
- MDL objective computation and acceptance rule,
- Drift and emergence band classification.

### 4.2 Artifacts

- Small hand-crafted fixtures encoded as JSON/TSV,
- Expected outputs recorded either inline or in golden tables.

### 4.3 Criteria

- All unit tests must pass for the reference profile,
- Edge cases (e.g. zero residuals, maximum residuals, boundary epsilon) must be exercised.

## 5. Integration Tests

### 5.1 SLP–UMX Integration

Tests to ensure that:

- UMX consumes SLP Snapshot IR correctly,
- Learning signals and MDL outcomes are consistent across ticks,
- Misconfigured or missing SLP fields are handled gracefully.

### 5.2 NAP–UMX Integration

Tests to ensure that:

- Envelopes are applied according to `umx_nap_bus_contract_v1`,
- Idempotence and exactly-once guarantees hold,
- Dead-letter and isolation behaviour are correctly surfaced.

### 5.3 Ledger and Manifests

Tests to ensure that:

- Commit and Snapshot Manifests are created and linked,  
- Replay using those manifests reproduces original results,
- U-Ledger entries expose the required metrics for testbed use.

## 6. System Tests (Testbed-Driven)

### 6.1 Scenario Selection

Select a subset of Aether Testbed scenarios where UMX participates explicitly. For each scenario `Sxx`:

- Identify which UMX properties are under test,
- Prepare UMX-specific expectations if not already in the testbed docs.

### 6.2 Execution

- Run the paper testbed with UMX outputs injected,
- Run the JS implementation with the same inputs,
- Compare testbed assertions (PASS/FAIL/INVESTIGATE/QUARANTINE) and numeric outputs.

### 6.3 Exit Criteria

- All selected scenarios behave as expected according to the MAX suite for at least one GO profile,
- No unexplained divergences between paper and JS remain.

---

---
id: tbp_umx_golden_fixtures_pack_v_1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Golden Fixtures Pack v1

## 1. Purpose and Scope

This document describes the **Golden Fixtures Pack** for UMX:

- A small set of canonical scenarios and states,
- With fully specified inputs and outputs,
- Used as a regression baseline for both paper-mode and runtime implementations.

## 2. Fixture Types

At minimum, the pack includes fixtures from four families:

1. **Minimal Topology Fixture**  
   - 2–3 nodes, 1 layer, simple edges, no residuals.

2. **Residual and Epsilon Fixture**  
   - A slightly larger graph with controlled residuals and epsilon corrections.

3. **Profile and MDL Fixture**  
   - A scenario where learning proposals are evaluated and accepted/rejected.

4. **Stress and Safety Fixture**  
   - A small scenario with budget and kill-switch events.

## 3. Fixture Format

Fixtures are stored as:

- JSON or TSV descriptions of:
  - Node Manifest,
  - Edge table,
  - Profile fields,
  - Initial state (residuals, epsilon entries, ledger indices).

- Expected outputs after:
  - One tick,
  - A small number of ticks,
  - Specific events (e.g. a kill-switch activation).

All expected values must be fully enumerated for Golden Fixtures (no unspecified behaviour).

## 4. Usage

Golden fixtures are used to:

- Validate early implementations during development,
- Serve as regression tests whenever code or specs change,
- Provide examples in documentation and training materials.

Implementations must not be tuned only to pass Golden Fixtures; they are a baseline, not exhaustive coverage.

---

---
id: tbp_umx_verification_plan_fixtures_crosswalk_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Verification Plan / Fixtures Crosswalk v1

## 1. Purpose and Scope

This document provides a **crosswalk** between:

- The UMX verification test plan,
- The Golden Fixtures Pack,
- The Aether Testbed scenarios.

It ensures that:

- Each verification objective is backed by specific fixtures and scenarios,
- No important property is left untested.

## 2. Crosswalk Structure

The crosswalk is a table where each row includes:

- `objective_id` — reference to a verification objective,
- `fixture_id` — which Golden Fixture(s) address it,
- `scenario_id` — which testbed scenario(s) exercise it,
- `properties` — which invariants or MAX properties are checked,
- `status` — coverage status (e.g. `covered`, `partial`, `gap`).

## 3. Maintaining the Crosswalk

As new fixtures or scenarios are added:

- Insert new rows mapping them to existing objectives,
- Add new objectives as required,
- Use the crosswalk to identify coverage gaps.

This document is living; it must be updated as part of any significant change to the UMX implementation or spec.

---

---
id: tbp_umx_operator_runbook_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Operator Runbook v1

## 1. Purpose and Scope

This runbook provides **operator-facing guidance** for running UMX in the Aether environment:

- Starting and stopping UMX runs,
- Loading profiles and scenarios,
- Monitoring key metrics and responding to alerts,
- Capturing logs and artefacts for analysis.

It assumes the existence of a basic UI and command interface, but remains agnostic about implementation details.

## 2. Pre-Run Checklist

Before running UMX:

1. Confirm that the correct **UMX profile** is selected (and has GO status),
2. Confirm that the desired **scenario** (or Golden Fixture) is loaded,
3. Ensure that the Aether Testbed bundle version matches the profile’s calibration record,
4. Verify that logging and export paths are configured.

## 3. Running a Scenario

### 3.1 Starting the Run

- Select profile and scenario,
- Initialise UMX state and ledger according to Snapshot Manifest or initial state tables,
- Start ticking either:
  - Step-by-step (manual tick), or
  - In batch mode (run N ticks).

### 3.2 Monitoring During Run

Operators should watch:

- Drift metrics and emergence bands,
- Budget usage and backpressure flags,
- Stress indicators and kill-switch status,
- Error and warning logs.

The runbook should define threshold values or states that require intervention (e.g., sustained INVESTIGATE bands, approaching FAIL thresholds).

### 3.3 Applying Controls

Operators may:

- Trigger a kill-switch for a node, region or entire system,
- Adjust budgets within allowed ranges,
- Place regions into quarantine (for investigation or stress testing),
- Pause or resume the run.

All such actions must be recorded in the ledger and run logs.

## 4. Post-Run Tasks

After a scenario completes or is stopped:

- Export logs, manifests and ledger snapshots,
- Run the Aether Testbed to evaluate properties and generate GO/NO-GO reports,
- Archive artefacts with clear identifiers (profile, scenario, time, testbed version).

## 5. Incident Response

For runs that encounter unexpected behaviour:

- Tag the run as an incident,
- Preserve all artefacts,
- Use the crosswalk and testbed outputs to identify which properties were violated,
- Decide whether the issue is due to:
  - Scenario configuration,
  - Profile tuning,
  - Implementation bugs,
  - Spec gaps.

This Runbook should be updated as operational experience accumulates.

## Part 3 — Topology Substrate, Conservation Engine, and Core UMX Model

### Source: `Universal Matrix Pillar — Topology Substrate & Conservation Engine.pdf` (PDF, extracted text)

--- Page 1 ---

Universal Matrix Pillar — Topology Substrate &
Conservation Engine
Title & Abstract
Universal Matrix (UMX)  is the Aether architecture’s  spatial topology pillar , acting as the all-connecting
substrate that defines how components are arranged and interact in the simulation. It imposes strict
physical-like rules: interactions are  local  (neighbor-to-neighbor only) and all transfers conserve globally
measurable quantities. In essence, UMX ensures that no matter how nodes connect or exchange values,
nothing is created or destroyed  – the total “mass” or quantity in the system remains constant at all times
. This pillar provides a deterministic lattice or network for the Aether system, guaranteeing reproducible
placement of nodes, symmetric exchange between them, and enforcement of global invariants on every
update. By maintaining a stable connective fabric with built-in conservation laws, the Universal Matrix
enables higher-level behaviors (like energy flow, signal propagation, or agent communication) to unfold in a
controlled, reversible manner analogous to a physical law within the simulation . The pillar integrates
seamlessly with other components (Gate, Loom, Press, etc.) via the system’s messaging bus, ensuring that
all inter-pillar interactions respect the same deterministic and invariant-preserving rules.
Scope & Responsibilities
The Universal Matrix pillar is responsible for the  structure and integrity of the simulation’s internal
network . Its scope includes defining how nodes are embedded in a space or graph, how they connect, and
how they exchange quantities under strict rules. Key responsibilities are: 
Deterministic Node Placement:  Deciding where and how new nodes are anchored in the network
in a reproducible way. Given the same initial state and random seed, UMX will place and wire a node
identically  every time . This ensures the topology is not subject to uncontrolled randomness – a
critical feature for reproducibility. Placement algorithms may use a coordinate anchoring scheme
(the PFNA system, assigning each node a tuple like (layer ℓ, grid g) ) to position nodes in a layered
lattice deterministically . In advanced implementations, placement and wiring might be guided
by an optimization (e.g. minimizing a description-length or “MDL” objective) to yield an efficient
network structure , but  always  with deterministic rules and tie-breakers (e.g. using a SHA-256
hash of candidate coordinates for consistent randomness) to ensure consistency across runs.
Maintaining Topology & Adjacency:  UMX defines the allowable topologies  (network shapes) and
ensures connections between nodes follow these rules. Admissible patterns can include radial, ring,
mesh, or lattice connectivity , but any topology that is instantiated must obey UMX’s constraints:
no  forbidden  links  appear  and  no  required  link  is  missing .  The  pillar  enforces  admission
constraints  like preventing closed causal loops or oscillatory cycles (the network of dependencies
must form an effective directed acyclic graph for state updates) . In practice, this means UMX can
refuse or adjust a connection that would violate causality or stability. Every node’s connections are
mediated by a  membrane interface  that upholds these rules, so when one node transfers some1
2
• 
3
4
5
• 
6
7
8
1


--- Page 2 ---

quantity to another , the Matrix ensures the transfer is local  (only to immediate neighbors as defined
by the topology) and allowed by the current network policy .
Conservation of Quantities:  The  global continuity law  is built into UMX – any quantity moving
through the network obeys strict conservation . If a node sends out some amount of a conserved
property (e.g. “mass”, energy, or information tokens), that exact amount is received by its neighbors
(distributed according to defined ratios), and nothing is lost to the void or spontaneously created.
Mathematically, UMX enforces that the sum over all nodes’ state remains constant each tick , i.e.
.  This  is  achieved  by  balanced  updates:  whenever  a  node
exports  a value to neighbors, that value is subtracted from its state and added to those neighbors in
equal measure . The pillar’s update rule thus naturally upholds a key invariant: the global sum of
whatever  is  being  exchanged  does  not  change .  This  effectively  simulates  a  physical  law  of
conservation inside the simulation. It also means every interaction is symmetric and reversible – if
Node A loses X and Node B gains X, one could conceptually reverse time and get X back to A .
Such symmetry is crucial for later enabling time-reversible execution and exact audit trails.
Routing & Flow Management:  The Universal Matrix provides mechanisms for routing  messages or
flows through the network while respecting locality and policy constraints. If one component needs
to  reach  another  not  directly  connected,  UMX  computes  a  path  (sequence  of  neighbor  hops)
between source and destination that adheres to all rules (no traversal through disallowed nodes or
layers, and not exceeding any link capacity limits) . UMX’s routing algorithm will find a valid
route if one exists that meets the specified policy; otherwise it will report that no route is possible
without violation. This ensures  isolation and sandboxing : for example, if certain nodes are in an
isolated  zone  or  a  link  can  carry  at  most  N  units  of  flow,  the  routing  will  never  breach  those
conditions .  In  implementation,  a  greedy  layered  routing  strategy  is  suggested,  where  routes
prefer to move upward or downward layer by layer and are bounded by a maximum number of hops
(a causal barrier c that prevents routes from becoming arbitrarily long) . Each hop or link may
consume budget (like bandwidth or time), and the routing respects these budgets. UMX can thus be
seen as not just a static graph, but an active routing fabric  that moves conserved quantities around
under tight governance.
Global Synchronization & Integration:  As a pillar in the Aether system, UMX must integrate with
other pillars  without breaking determinism. It works closely with the  Nexus Aternus Protocol
(NAP)  – the inter-system communication layer – to send and receive state updates or structural
changes as formal messages (see Nexus Aternus Protocol  below). Any change in the network (like
adding a node, or a node transferring a quantity) can generate a transaction on the Nexus bus so
that other pillars (e.g., the Gate or Loom) are aware and can log or act on it . UMX is also aware of
timeline control via the  Aevum Loom  (the ledger/timeline pillar): for instance, the Loom might
dictate a “tick” or epoch boundary at which all pending flows are committed and checkpointed. UMX
will honor such sync points, applying its propagation updates in discrete deterministic time-steps (τ
increments) and handing off a snapshot of the network state to Loom for hashing and record-
keeping each tick. Additionally, UMX can interface with  Astral Press  (the compression pillar) – for
example,  Press  might  compress  the  structure  or  changes  of  the  lattice  for  efficient  storage  or
transmission. The matrix provides data such as adjacency or flow logs to Press, and may itself
leverage  Press’s  outputs  (like  using  a  compressed  motif  of  connections  if  it  helps  minimize
description length). Overall, Universal Matrix operates as the  substrate that binds all nodes , and
through NAP and other protocols it remains in sync with the rest of the system (ensuring, say, that9
• 
1
state(t+ ∑i i 1)= state(t) ∑i i10
11
12
• 
1314
14
5
• 
15
2


--- Page 3 ---

an external input through Trinity Gate that adds a node is properly placed in the matrix, or that a
learned pattern from Codex Eterna doesn’t violate topology rules).
Components (Named & Implied)
The Universal Matrix pillar comprises both explicit components and implied mechanisms that together
realize its function in the Aether system. The major components and features include:
Universal Matrix Node (UMX Node):  This pillar manifests in the system as a core module (or node)
that  runs  the  Matrix  logic  each  tick.  In  the  simulation’s  node  manifest,  it  appears  with  a  type
identifier (e.g., "type": "universal_matrix"  or an equivalent code) alongside other core nodes
like LOOM (ledger), PRESS (compression), and the Gate . The UMX node maintains the data
structures for the network: e.g. lists of nodes and their coordinates, an adjacency matrix or neighbor
list, and per-connection weights or capacities. Each simulation step, the UMX node is invoked to
update the state of the network – propagating flows, applying any structural changes, and enforcing
invariants. It essentially serves as the “physics engine” of the Aether world, but for information/
energy flow rather than physical particles.
Synaptic Ley Protocol (SLP):  This is the  topology and adaptation protocol  that governs how
connections (leys) form, strengthen, or dissipate over time within the Universal Matrix. SLP defines
the deterministic rules of synaptic plasticity  in the network – in other words, which pathways become
reinforced  and  which  are  pruned,  based  on  usage  patterns,  while  still  conserving  totals  and
respecting layer structure . Concretely, SLP is responsible for operations like growing a new link
between nodes when there is sustained activity or “intention” between them, increasing the weight
(capacity) of frequently used connections, and trimming away links that fall into disuse. It provides
routines such as  SLP_GROW ,  SLP_POTENTIATE ,  SLP_PRUNE , and  SLP_CONDUCT  (detailed in
the  next  section)  to  manipulate  the  network  topology  in  a  controlled  fashion.  Importantly,  SLP
changes  are  fully  deterministic  –  given  the  same  history  of  usage,  it  will  make  the  same
adjustments every time (no random pruning or growth). This protocol ensures the lattice can evolve
and self-optimize (much like neural connections in a brain)  without  ever violating conservation or
determinism. SLP works in tandem with the base UMX propagation: UMX handles the immediate
neighbor  exchanges  each  tick,  and  SLP  periodically  updates  the  network  structure  (weights  or
presence of edges) based on the longer-term statistics of those exchanges.
Membrane Interfaces & Conservation Law (Implied):  Every node-to-node interaction in the Matrix
is mediated by a membrane interface  that enforces local actions yielding equal and opposite global
reactions . This implied component means that whenever Node A sends something to Node B,
the membrane at A’s boundary subtracts that quantity from A (as if “emitting” through a membrane),
and the membrane at B’s side adds the quantity to B (as if “absorbing” it) with no loss. These
interfaces also can impose translation or filtering rules – for example, if Node A’s output is in units
that Node B uses differently, the membrane might convert units or ensure the transfer is allowable
(similar to how Trinity Gate’s membrane handles external data, but here for internal links). The
membranes  effectively  guarantee  locality  (no  action  can  skip  directly  beyond  a  neighbor)  and
conservation  at  each  link.  They  are  “invisible”  in  implementation  (one  typically  just  codes  the
transfer rules), but conceptually they are the reason the Matrix can treat every connection as a tiny
reversible gate that obeys the sum-zero rule. They also help implement node isolation : if a policy
says Node X cannot directly affect Node Y, the membrane between them will block any transfer• 
1617
• 
• 
2
3


--- Page 4 ---

(making the adjacency zero). In summary, this component is the per-connection enforcement of
UMX’s physics.
Anchoring & Addressing Scheme (PFNA Anchors):  To place nodes deterministically, UMX uses a
coordinate anchoring scheme sometimes referred to as PFNA (layer, grid)  coordinates . Each
node when created is assigned an anchor  (ℓ, g) – for example, a layer index ℓ (which could
correspond to a logical level or zone in the network) and a grid location g (an address within that
layer). The placement function UMX_PLACE(item, matrix, seed)  uses the current network state
and a given seed to compute an appropriate anchor for the new node . The scheme ensures that
if you re-run the same scenario, each new node gets the  exact same coordinates . In more
advanced usage, the PFNA scheme may incorporate an objective function: it attempts to place nodes
such that some  description-length  or encoding cost of the overall network is minimized .
This essentially means the network organizes itself to be as “compressible” or regular as possible
(which ties into the Press pillar’s goals). For now, in a basic implementation, PFNA could be as simple
as layering nodes in order of insertion (layer 0,1,2,…) and giving each a sequential grid number , or
embedding them in a fixed lattice pattern. The anchor coordinates not only help with placement but
also addressing : the Nexus Aternus Protocol can use (ℓ,g) as an address to target messages to a
particular node or group of nodes in the lattice (like all nodes in layer ℓ). This anchoring system is
fundamental to UMX’s ability to reference and manage nodes without ambiguity.
Nexus  Aternus  Interface  (NAP  Bus): (Implied  support  component)  The  Universal  Matrix  pillar
interfaces with the Nexus Aternus Protocol  for any inter-node or inter-pillar messaging. While NAP
is a system-wide protocol (detailed later), from UMX’s perspective it functions as the communication
bus that carries any proposals, commits, or data frames related to topology and state changes. For
example, if a new node is to be added to the matrix, that might come as a PROPOSE  message via
NAP (with details of the node) which UMX will accept and commit, logging the new anchor . Similarly,
UMX might emit a message on the bus when a link’s weight changes (so that Loom can record it or
Gate  can  be  informed).  The  NAP  interface  ensures  that  all  such  exchanges  are  done  in  a
transactional, deterministic manner  – UMX never directly alters shared state without a commit on
the  bus,  and  it  can  replay  or  rollback  changes  as  needed  via  NAP’s  semantics .  In
implementation terms, the UMX node will have access to send/receive queues of the bus. The Nexus
also provides  address discovery  (UMX can find nodes by their anchor addresses through the bus
directory) and  backpressure  (if one part of the network is overloaded, NAP can signal UMX to
throttle propagation or growth rates). Though not a standalone component of UMX, the NAP bus
integration is crucial for  multi-pillar synchronization  – it keeps Universal Matrix in lockstep with
Trinity Gate, Loom, Press, and others by conveying state updates and ensuring everyone agrees on
the order of events.
Global Invariants & Test Suite (Implied):  Built into the pillar are various invariants (as discussed)
and a suite of validation tests that the system can run to verify everything is working as expected.
For instance, Deterministic Placement  is verified by attempting to place the same set of items twice
with the same seed and checking the resulting positions match . Flow Conservation  is tested
by letting a sample quantity diffuse through the network for one tick and asserting the global sum
remains unchanged .  Routing constraints  are tested by finding a path under restrictive
policies and confirming the path doesn’t violate capacity or isolation rules . These tests are
not user-facing features but are important internally. They can be run in an offline mode (or as unit
tests in a JS implementation) to ensure the pillar’s logic is correct. Having this test suite is part of the• 
18 4
19
3
2021
• 
2223
• 
24 3
2511
2614
4


--- Page 5 ---

pillar’s  component  list  in  that  it  embodies  the  guarantees  UMX  upholds.  It’s  also  useful  for
development: after implementing UMX and SLP in code, one would use these tests to confirm
determinism and conservation properties before integrating fully with the rest of the system.
(With the core components outlined above, we now detail the two main protocols associated with the Universal
Matrix: the Synaptic Ley Protocol, which governs internal network dynamics, and the Nexus Aternus Protocol,
which governs the external communications and integration.)
Synaptic Ley Protocol (SLP) — Topology Adaptation & Plasticity
Synaptic Ley Protocol  is the formal set of rules that allow the Universal Matrix’s topology to adapt over
time in response to usage , analogous to synapses strengthening with repeated use or “ley lines” forming
where energy flows. SLP runs on top of the static lattice defined by UMX, introducing a controlled form of
dynamics to the network structure itself. Its guiding philosophy can be summarized as:  “Where intention
flows,  a  ley  forms;  strengthen  what  compresses,  prune  what  does  not” .  In  plainer  terms,  whenever  a
particular path in the network is heavily used and contributes to efficient overall behavior (e.g. helps
compress information or reduce some cost), SLP will reinforce that path. Conversely, if a connection isn’t
pulling its weight (unused or redundant), SLP will eventually trim it away to keep the structure efficient. All
of this occurs while preserving the total conserved quantities and the layered structure  of the network
–  SLP  never  violates  the  conservation  enforced  by  UMX,  it  only  adjusts  how  that  conserved  flow  is
distributed.
SLP Components & Operations:  The protocol provides a handful of deterministic operations to manage
connections:
Ley  Formation  (GROW):  When  two  nodes  frequently  exchange  information  or  “desire”  a  direct
connection, SLP can establish a new link (or activate  a previously zero-weight link) between them.
The  operation  SLP_GROW(path)  creates  or  reifies  a  path  when  a  certain  usage  threshold  is
exceeded . For example, if nodes A and C often communicate via a multi-hop route A–B–C, SLP
might decide to add a direct A–C link to streamline this, once usage passes a threshold θ_plus. This is
done deterministically: the protocol monitors usage counts or flow magnitudes on potential paths,
and if usage(path) > θ_plus , it increments the weight of that connection (or adds it if it was
absent) by a fixed amount α . This rule ensures that frequently used routes become stronger/easier
over time, reflecting a form of learning or optimization of the topology. Importantly, θ_plus and α
are  design  parameters  (constants  or  functions)  chosen  such  that  the  process  is  stable  and
deterministic – e.g., θ_plus might be “10 units of flow in the last 100 ticks” and α could be a small
weight increment. Once the condition is met, the growth is applied in a single, atomic step (often at
tick boundaries or checkpoint events to remain synchronous system-wide).
Potentiation (Adjust Weights):  In some designs, a distinction is made between simply creating a
path and  potentiating  it continuously. The snippet above references  SLP_POTENTIATE(path, 
gain), which suggests that beyond the initial creation, the protocol can adjust the strength  of a ley.
For instance, each time a path is used heavily, its weight might be increased by a factor (gain). In our
current SLP rules, this potentiation is effectively folded into SLP_GROW  (increase weight by α when
usage exceeds θ_plus). The idea is that repeated high usage will trigger multiple GROW increments,
thus gradually increasing capacity. This  plasticity  is deterministic because it’s purely a function of27
• 
28
28
• 
5


--- Page 6 ---

measurable usage statistics – if the usage pattern repeats, the weight adjustments repeat in the
same way. There’s no random variation, so two simulations with identical inputs will potentiate the
same connections by the same amounts at the same times.
Ley Conduction (CONDUCT):  This refers to the actual act of carrying a delta  (change or flow) along
an  existing  path.  SLP_CONDUCT(Δ along path)  essentially  leverages  the  UMX  propagation
mechanism to send a specific amount of some quantity along a specified route . While the base
UMX propagation typically distributes flows to all neighbors according to the kernel, SLP_CONDUCT
can be thought of as focusing a flow along a particular chosen path (for example, if a higher-layer
logic says “send 5 units from X to Y”, the SLP conduction will handle that targeted transfer). The key
rule enforced here is conservation at every hop : as the Δ moves from node to node along the
path,  SLP  ensures  that  what  leaves  one  node  arrives  at  the  next  with  no  leakage.  Essentially,
SLP_CONDUCT is a deterministic routing of a packet/flow that rides on top of the UMX neighbor
exchange rules. If any node along the path were missing or the path weight was zero (pruned), the
conduct would fail or be deferred – thus SLP_CONDUCT might also include logic to only operate on
active paths. In an offline JS implementation, this could correspond to a function that, given a
sequence of node indices [A, B, C, ... Z] and an amount Δ, subtracts Δ from A, adds it to B, then
subtracts from B, add to C, etc., and finally delivers Δ to Z, all within one tick, logging the transfer .
Ley Pruning (PRUNE):  To prevent the network from bloating with unused connections, SLP also
defines a pruning rule. SLP_PRUNE(path)  will reduce the weight of a connection if its usage falls
below  a  low  threshold  θ_minus  for  a  sustained  period .  Concretely,  if  a  link  hasn’t  carried
meaningful flow for M consecutive ticks and usage(path) < θ_minus  during that time, SLP will
decrement its weight by some amount β or even cut it to zero (removing the link) . The protocol
might implement a graceful decay: e.g., each evaluation interval, reduce weight = max(0, weight – β).
Eventually,  if  the  link  remains  idle,  its  weight  goes  to  0,  effectively  pruning  it  from  the  active
topology. Like growth, pruning is deterministic – it’s triggered by specific, measurable inactivity
patterns and uses fixed decrement values. There’s a hysteresis implied by having two thresholds
(θ_plus for growth vs θ_minus for prune) and a memory of M ticks of inactivity; this prevents flapping
(rapid add/remove of a link). A link will only be removed after consistent low use, ensuring stability.
All prunes happen under the hood of the simulation tick and are recorded (so Loom’s ledger would
note that at tick T, link (X–Y) weight dropped to 0). Because pruning can change connectivity, UMX’s
adjacency rules come into play: when a weight hits zero, effectively that edge is no longer in the
adjacency matrix, and UMX will treat those nodes as no longer neighbors (ensuring subsequent
flows don’t go that way).
Stacking & Layer Integrity:  The one-liner for SLP mentioned  “conserving totals and layers” . This
highlights that SLP not only conserves the numeric totals (which we covered) but also respects the
layer structure (nest geometry)  of the lattice. For example, if the network is layered (layer 0,1,2,...
as per PFNA anchors), SLP might restrict that certain connections can only form between specific
layers  or  that  a  “residual”  from  one  layer  is  handled  in  a  particular  way.  A  routine  like
SLP_STACK(residual, layer)  suggests that SLP can take a residual  (an unallocated remainder
from some process, perhaps from Press compression or from a partial flow) and assign it to a
particular layer or stack for later processing. This is speculative, but it aligns with the idea of layer-
wise conservation : each layer might have to account for any leftover quantities. In practical terms,
this could mean if a high-level process leaves an error term, SLP ensures that error is stored in a
specific place (like an adjustment node) so that the total in each layer is still trackable. For a first• 
29
30
• 
29
29
• 
6


--- Page 7 ---

implementation, we may not need to delve deeply into this, but it’s good to design with layered
integrity in mind. The network should maintain consistency not just globally but per layer , if that’s
part of the invariant (i.e., each layer’s sum or some property is also conserved, which could be a rule
for certain types of flows).
To illustrate the SLP behavior , consider a simple example : suppose we have four nodes A, B, C, D in a lattice.
Initially A–B–C–D form a chain. If A frequently sends a lot of data to D (meaning the chain A→B→C→D is
always busy), SLP might decide to create a shortcut from A to D directly. That is SLP_GROW(A–D)  triggers
when it sees usage high. Now A→D is a direct link with some small weight. Over time, every tick A uses both
the direct link and the indirect path; as use remains high,  SLP_POTENTIATE  effectively increases A–D’s
weight. Meanwhile, maybe the middle link B–C was hardly used (perhaps most flows go A->B, then A->D
direct, bypassing C). SLP notices B–C usage is near zero for a long period; it triggers SLP_PRUNE(B–C)  and
cuts that link. The end result is a topology that adapted: A connected to D strongly, and the weak unused
link between B and C was removed. Throughout all this, at no point did the total amount of “stuff” in the
system change unexpectedly; flows rerouted but every unit leaving A still ended up in D, etc., and the ledger
can show exactly when the topology changed due to what conditions. The determinism  means that if we
replay the simulation from the start, the exact same topology changes happen at the exact same ticks,
given the same inputs.
Mathematical Summary:  The core equations/rules of SLP can be summarized in pseudocode as follows:
# Propagation step (from UMX, included for context)
UMX_PROPAGATE(state_t, kernel K):
    for each node i:
        out_i = Σ_j K[i→j] * state_t[i]       # distribute i's state to 
neighbors j
    in_i = Σ_j K[j→i] * state_t[j]            # gather incoming from neighbors
    state_{t+1} = state_t + (in - out)        # apply net changes (conservation)
    assert Σ_i state_{t+1}[i] == Σ_i state_t[i]   # total conserved
# Synaptic Ley adjustments
SLP_GROW(path):
    if usage(path) > θ_plus:
       w(path) = w(path) + α                 # increase weight of that path
SLP_PRUNE(path):
    if usage(path) < θ_minus for M ticks:
       w(path) = max(0, w(path) - β)         # decrement weight or remove link
SLP_CONDUCT(path, Δ):
    for each hop (u->v) in path:
       transfer Δ from u to v
    (enforce conservation at every hop)
(The propagate part above shows how the base UMX neighbor exchange works, maintaining a global sum ,
and the SLP parts show how weights w(path) are tuned based on usage thresholds . All of these rules are10
28
7


--- Page 8 ---

deterministic  and  reversible  in  effect.  The  use  of  thresholds  θ_plus/θ_minus  provides  hysteresis  to  avoid
oscillation.)
Explanation:  The pseudocode above illustrates that each simulation tick’s update preserves
the total sum of state across all nodes (no loss or gain) . On top of that, the Synaptic Ley
Protocol deterministically adjusts connection weights: when a path’s usage exceeds a high
threshold,  its  weight  is  incremented  (strengthened),  and  when  usage  falls  below  a  low
threshold  for  long  enough,  its  weight  is  decreased  or  set  to  zero  (weakened) .  All
adjustments happen in a controlled way, with no random chance involved – given the same
usage  pattern,  the  same  links  will  grow  or  prune  at  the  same  time.  Conservation  is
maintained at every step, meaning even as the network changes shape, any flow conducted
along a path still obeys the rule that whatever leaves one node appears in the next node
without loss .
Integration with UMX & Other Pillars:  SLP is essentially an internal protocol  of the Universal Matrix pillar ,
so  it  operates  during  the  simulation  loop  as  part  of  UMX’s  duties.  Typically,  one  might  run  UMX’s
propagation every tick, and run the SLP structural update less frequently (say every N ticks or on certain
events) to avoid too frequent changes. Because SLP changes the topology, it will interface with the Nexus
Aternus  Protocol  to  formally  commit  these  topology  changes.  For  example,  when  a  link  is  grown  or
pruned, that could be emitted as a NAP message like “TOPOLOGY_UPDATE: link X–Y weight = w” which all
pillars see. The Loom ledger would log the change (so that on replay, the exact same link change is applied),
and Trinity Gate could be informed if needed (though usually Gate cares more about external interfaces, it
might still need to know if the internal structure drastically changes, e.g., to update an external observer).
The Codex Eterna  (learning pillar) might also tie in: it could analyze patterns of usage and confirm that a
new link indeed shortened the description length of the system’s state transitions (which would reinforce
that the growth was beneficial). In turn, Codex might provide feedback to SLP (like adjusting thresholds or
identifying candidate motifs of connectivity). But those are advanced interactions. In our scope, the main
integration is:  UMX + SLP together manage the evolving lattice , and they communicate any changes
through NAP to the rest of the system, ensuring consistency. Since SLP never introduces randomness, it
does not conflict with Trinity Gate’s determinism guarantee; the Gate can trust that when it feeds the
simulation identical sequences, even the topology will evolve identically thanks to SLP’s fixed rules.
Nexus Aternus Protocol (NAP) — Inter-System Communication
The Nexus Aternus Protocol  is the overarching communication and synchronization protocol that knits all
pillars of Aether together into a single coherent system. While not exclusive to the Universal Matrix, it is
listed among UMX’s protocols because the Matrix heavily relies on NAP to interact with other parts (and
indeed, NAP was conceived as one of the “three umbrella protocols” alongside the Trinity Gate and Lattice
protocols ).  NAP’s  role  is  essentially  to  ensure  that  all  subsystems  “talk”  to  each  other  in  a
deterministic, orderly, and verifiable way . In simpler terms, it’s the rules of the road for messaging: how
data is packaged, how it’s routed, how consistency is maintained, and how evidence of actions is shared.
Core Functions of NAP:
-  Membrane-Boundary Messaging:  NAP requires that any communication between components goes
through well-defined membrane boundaries . Each pillar or node has a membrane (its interface), and
messages must pass through these, undergoing any necessary translation or checks. This prevents direct
uncontrolled access to a node’s core; instead, everything is funneled through gates/channels that can10
28
30
3132
33
8


--- Page 9 ---

enforce constraints. These channels are reversible  and deterministic. For the Universal Matrix, this means if
an external system (or another pillar) wants to, say, inject a new node or query the state of a node, it does
so via the matrix’s interface procedures (not by poking the matrix’s internal data directly). The membrane
semantics ensure, for example, that if Trinity Gate sends in data, UMX only accepts it if it fits the expected
schema and will convert it into internal state changes in a controlled manner . Likewise, any data leaving
UMX for external consumption is filtered (no sensitive or invalid info escapes). This concept mirrors Trinity
Gate’s membrane (which isolates Aether’s core from outside); here it isolates each node or subsystem from
others in the inside  communications.
Aether  Bus  (Routing  Fabric):  The  Nexus  Aternus  introduces  the  Aether  Bus ,  a  logical
communication fabric that connects all nodes (and even multiple instances of the Aether system, if
distributed) . You can think of it as a deterministic message bus or network overlay that sits on
top of (or alongside) the Universal Matrix’s physical connections. While UMX’s topology handles
physical  adjacency  and  flow ,  the  Aether  Bus  handles  logical  message  passing  which  might  span
multiple hops. It provides features like address discovery  (finding where to deliver a message based
on some ID or coordinate), partitioning  (it can segment communications so that certain groups of
nodes only talk among themselves if needed), and backpressure  (if too many messages are in flight,
the bus can signal senders to slow down). Importantly, this bus is still governed by deterministic
rules – for example, the routing algorithm on the bus, if needed, can be deterministic and could even
utilize the UMX topology for physical path but with additional logic to guarantee ordering (we’ll get
to ordering soon). In implementation, one might model the bus as a global event queue or a
network layer that all nodes subscribe to. Because UMX ensures no cycles and preserves causality,
NAP can leverage that to simplify global ordering of events (no contradictory loops).
Message Frame Schema:  All data exchanged via NAP is encapsulated in a standard message/frame
format , typically a JSON-like structure . Each frame includes fields like a unique identifier , source
and destination addresses (which could be PFNA anchors, node IDs, etc.), a payload (which might be
a command or data), and references to  manifests/hashes  for integrity. The mention of manifest
and hash means that whenever a message carries some piece of state or result, it often includes a
cryptographic hash or reference to a manifest (a manifest could be a summary of a state, like a
content-addressable hash of a dataset, or a pointer to a ledger entry). This way, the receiver can
verify that, say, the “state ID 0xABC” attached to a message actually matches the state it expects (it
could fetch from Loom or check its own records). Additionally, for any public or logged copies of
messages, endpoint placeholders  are used  – this is a security measure meaning if a message is
recorded in a context visible outside the system, actual addresses or sensitive data are redacted or
replaced with placeholders. For example, an external log might show “Node [REDACTED] committed
update” instead of the actual node name, to avoid leaking details. In sum, the frame schema ensures
every message is self-describing, tamper-evident, and sanitized for audit.
Transactional Verbs & Control Signals:  NAP defines a set of allowed verb actions  for messages.
Transactional verbs include QUERY , PROPOSE , COMMIT , ROLLBACK . These correspond to a two-
phase commit style interaction: e.g., a component can PROPOSE an action (like “add node X”), other
components can respond or the same component can check conditions, then a COMMIT finalizes it
(making it official in the system state and ledger), or a ROLLBACK aborts it. This mechanism is crucial
for consistency: it ensures that changes to the simulation (like adding a node or transferring a large
quantity) are done in a way that either happen fully or not at all, and everyone sees them in the
same order . For instance, UMX might get a PROPOSE message to add a link between A and B; it• 
33
• 
34
34
• 
22
9


--- Page 10 ---

checks topology rules, and if okay, it will send a COMMIT which all nodes accept, thereby the link is
added universally. Control signals include  ANNOUNCE  (e.g., a node advertising its presence or a
heartbeat),  HEARTBEAT  (periodic  signals  to  indicate  liveness  or  sync  timing),  and  PROBE  (a
diagnostic  or  sync  check) .  These  are  not  state-changing  but  help  manage  the  system’s
distributed operation. For example, Trinity Gate might ANNOUNCE a new external input is ready, or
Loom might send a HEARTBEAT every second to coordinate ticks. All such verbs are part of the
protocol specification and are processed in a deterministic way by each pillar .
Residual Layering & Budgets:  NAP also carries the concept of  residual layering semantics .
This is a bit abstract: it refers to how the system handles multi-layer outputs and errors. In layered
processing (like Press compressing data then Gate outputting it), there are often residuals or errors
at each layer (for example, Press might not perfectly compress and leaves a residual; Gate might
approximate something and leave an error term). NAP’s job is to ensure these residuals are tracked
and reduced in an orderly fashion – monotonic reduction  means each successive layer or step should
not increase the error , only same or reduce it. NAP messages can carry a notion of  layer order
(which layer of processing the message belongs to) and residual budgets  (how much error or slack
is allowed) . For instance, a NAP frame might say “Layer=2, residual_budget=0.01” indicating this
message is part of layer 2 processing and the allowed error so far is 0.01 units. All components then
know how to treat it. By enforcing these budgets, NAP ensures that, say, a later stage doesn’t
accidentally double-count an error or overshoot some tolerance. In implementation, this could be as
simple as including a field in messages and having each pillar check/adjust it. For now, if we’re
focusing  on  offline  JS  demo,  we  might  not  simulate  complex  residual  budgeting,  but  it’s  a
placeholder for hooking in more advanced error-control logic.
Determinism Rules (Freeze-sets):  A critical responsibility of NAP is to maintain determinism across
the whole system . We’ve discussed each pillar being deterministic; NAP ensures when they work
together , no hidden nondeterminism creeps in. The concept of a freeze set  is mentioned  – this
typically means the set of conditions that must be fixed to ensure determinism: random seeds,
operation ordering, timeline alignment, periodic triggers, etc. NAP enforces these by standardized
means. For example, seeding : at the start of each run or each new component, NAP might generate
or distribute a hash-based seed (like using SHA-256 on some combination of run ID, component ID,
time window) to use for any pseudo-random choices . This way, if the run is repeated, the
seed can be the same and all pseudo-random aspects replay exactly. Ordering : NAP ensures a global
order of commits – even if messages are handled concurrently, they are assigned a deterministic
total order (possibly via a Lamport clock or vector clock scheme, see below) so that every pillar
processes events in the same sequence . Timeline sync : NAP might inject periodic sync pulses
(like the Loom’s heartbeat) to coordinate ticks, and everyone agrees on when tick boundaries occur .
And no background nondeterminism  means that nothing happens “behind the scenes” – e.g., no
thread or process is altering state without going through NAP. In a single-threaded JS environment,
this is naturally satisfied; in a distributed or multi-threaded environment, NAP’s rules act like a single-
threaded scheduler for the whole system. By freezing these aspects, we can guarantee that running
the simulation on two different machines or two different times yields identical results, provided
they both adhere to NAP’s sequence of messages.
Evidence Hooks & Auditability:  Every communication in NAP comes with  evidence  that can be
used to verify and audit the correctness of the system . These evidence hooks include attaching
MANIFEST_REF  (a  reference  to  a  manifest  of  the  current  state  or  action),  HASH_PROOF  (a22
• 35
35
• 
36
3738
39
• 
40
10


--- Page 11 ---

cryptographic hash chain or Merkle proof that the message is consistent with the ledger history),
CHECKPOINT  indicators (linking to a Loom checkpoint if this message finalizes a checkpoint), and
acceptance results  (for example, a Pillar might include a boolean or a confidence value that a
certain test passed). This design ensures that any observer or any part of the system can later check
that nothing fishy happened: The state after applying a series of messages can be recalculated and
the hashes compared to ensure no tampering. For Universal Matrix, this means whenever the matrix
evolves (like adding a node, or total energy moved), those changes are reflected in the evidence. For
instance, a COMMIT message for adding a node might include the hash of the new adjacency matrix
or new global sum, so that others can verify the matrix’s integrity post-addition. These hooks turn
the whole system into a verifiable ledger of events  (much like a blockchain, though permissioned
and internal). In practice, the Loom pillar is the one storing these hashes and manifests, but NAP is
the carrier that transports them with each action.
Idempotence & Exactly-Once Delivery:  NAP guarantees that each intended action in the system
has an effect once and only once , no matter how many times messages might be sent or resent. This
is vital in any distributed system to avoid duplicates from causing double execution. The protocol
achieves this by tagging each message with a unique identifier (UID) , usually a cryptographic hash
of its content and some key, via an operation like: uid = H256(key ∥ serialize(msg)) .
Each participant keeps a store of seen UIDs. When a message arrives, NAP_DEDUP(store, uid)
checks if the UID was seen before; if yes, it drops the message (as it’s a duplicate) . If not, it
processes it and adds the UID to the store. This makes message delivery idempotent  – sending the
same message twice has the same effect as once. The “key” in the hash might be a secret or a run-
specific token to prevent malicious replays from other contexts. In an offline single-run, you might
not see duplicates, but it’s still wise to implement this check for completeness. Additionally, state
changes are isolated to COMMIT events – nothing should permanently change state on a PROPOSE
(until commit) – which means even if a PROPOSE is sent multiple times, it won’t matter unless a
commit follows. This separation plus deduplication ensures exactly-once semantics .
Causal Ordering (Logical Clocks):  To maintain a consistent order of events across all components,
NAP uses a form of logical timestamping. The design allows using a Lamport clock or vector clock
approach . In simpler terms, every message has a tag or timestamp, and each time a message is
processed, the clock is advanced such that a happened-before relationship is respected. A possible
implementation:  maintain  a  global  Lamport  counter;  each  new  message  gets
counter = counter + 1  and that number is the message’s timestamp. Also, when a message
from  another  source  comes  with  a  timestamp,  set  your  counter  to  max(local_counter,  
msg_timestamp)  then +1 for the next. This ensures if message X happened before Y in the system,
all  nodes  will  eventually  see  X’s  timestamp  <  Y’s  timestamp,  so  they  agree  on  order .  In  code,
NAP_ORDER(tag, clock)  could  update  a  structure  like  a  Lamport  clock  with  event  tag  and
produce a new clock value . A vector clock is more complex (it tracks an array of counters for each
node) but offers even stronger ordering (detecting concurrent events). For our use, a Lamport clock
suffices to impose a deterministic sequence. The outcome is that even if messages are flying around
concurrently, the protocol will serialize them in a defined order when applying to state. The Universal
Matrix might receive multiple commands in a tick (e.g., add a node, then transfer something); NAP
ordering ensures that if “add node” is timestamped before “transfer”, all pillars will add the node first
then do the transfer , never the opposite, avoiding race conditions. This property is referred to as
causal consistency  – if an event could causally affect another , their order is preserved system-wide.• 
41
42
• 
43
44
11


--- Page 12 ---

# NAP core helpers
NAP_ENVELOPE(msg, key):
    uid = H256(key ∥ SER(msg))      # unique message ID as hash of key + 
serialized content
    return { uid: uid, payload: msg }
NAP_DEDUP(store, uid):
    if uid ∈ store:
       drop msg                    # duplicate detected, ignore
    else:
       store.add(uid)              # record this message UID as seen
NAP_ORDER(global_clock, msg_timestamp):
    global_clock = max(global_clock, msg_timestamp)
    global_clock = global_clock + 1
    return global_clock            # returns updated logical clock value to tag 
new outgoing events
Explanation:  The pseudocode above (for illustration) shows how NAP might wrap messages
with a unique hash-based UID and filter out any duplicates to enforce exactly-once delivery
. It also sketches a logical clock update rule: each time an event occurs, advance the clock
(taking into account any incoming timestamp) to impose a global order . In practice, this
means every message in the system is uniquely identified and processed only a single time,
and  all  components  agree  on  a  single  sequence  of  events.  Even  in  an  offline  JS
implementation, including these mechanisms (though simple) will align the code with the
intended architecture – e.g., you might simulate messages as objects with an uid property
and maintain a Set of processed UIDs to ignore repeats.
NAP and Trinity Gate / UMX Synchronization:  Now, critically, the Nexus Aternus Protocol is what enables
Trinity Gate Pillar and Universal Matrix Pillar to work in tandem  without issues. Trinity Gate is the pillar
handling external I/O, and it uses a special protocol (the Triune Bridge Protocol) at its boundary to translate
external signals. But once those signals are inside Aether , they are carried as NAP messages. For example,
suppose an external user toggles a switch that should add energy to the simulation. Trinity Gate would
translate that into an internal action (maybe “add 10 units to node X”) and send it as a NAP  PROPOSE
message  into  the  system.  The  Nexus  ensures  this  propose  is  delivered  to  UMX  (or  whichever  pillar
responsible)  exactly  once  and  in  order .  UMX’s  membrane  sees  it,  checks  that  adding  10  units  obeys
conservation (perhaps it requires taking 10 units from an external reservoir node to keep total zero), and
then UMX would COMMIT the change – which goes back through NAP to Trinity Gate (so the Gate knows the
action is completed and can, say, send an acknowledgment externally) and to Loom (to record the new state
and that a user input was applied). The synchronization  here is that Trinity Gate and Universal Matrix do
not  directly  call  each  other’s  functions;  instead,  they  exchange  messages  via  NAP,  and  because  NAP
enforces determinism, it doesn’t matter if the Gate and Matrix are on the same thread or across a network,
the outcome is the same. This also means the timing  of interactions is controlled. If the Gate sends multiple
inputs quickly, NAP’s ordering might queue them such that UMX processes them one per tick, or according
to timestamps, thus the simulation doesn’t get ahead of itself. 45
44
12


--- Page 13 ---

From a development standpoint, using NAP for sync means when implementing the offline JS, we might
simulate the message passing simply by calling functions in sequence (since all is within one process). But
we should still conceptually structure it as: Gate puts a message in a queue -> Matrix reads from queue ->
Matrix does stuff -> Matrix (or Loom) puts response message -> etc. This will make it easier later to
distribute or expand.
Cross-Pillar Integration Highlights:
- The Trinity Gate Pillar  outputs and inputs go through NAP. Gate’s Trinity Bridge Protocol defines what  can
cross (ensuring the content is valid), but NAP defines how it crosses (the envelope, commit semantics, etc.)
. For example, Trinity Gate might package a quantum measurement result as a JSON frame with a
manifest hash and send it via NAP to Loom and others – the Nexus adds UID, orders it, and by the time UMX
sees it, it knows exactly when it happened relative to all else. - The Aevum Loom (ledger)  ties in by logging
NAP events. Every COMMIT message effectively becomes a record. Loom might also inject periodic NAP
messages (heartbeats or checkpoint announcements) that signal UMX and others to mark a new epoch.
Because Loom and NAP are tightly linked, the entire history of NAP traffic can be replayed to reconstruct
the simulation – proving determinism. - The Astral Press (compression)  uses NAP to ship compressed state
frames between pillars. For instance, Press may produce an APX capsule (a compressed state) and include it
in a NAP message to Gate for external output . Conversely, Gate might send a capsule via NAP to Press
to  decompress  into  internal  state.  NAP  ensures  the  capsule’s  hash  matches  manifest,  etc.,  so  these
exchanges are reliable. - The Codex Eterna (learning)  likely also communicates via NAP, perhaps proposing
new motifs or patterns as transactions that must be accepted by the system (e.g., “I propose adding this
learned rule to the library” as a PROPOSE, then commit after validation). - Finally,  the Universal Matrix
itself uses NAP  to enforce that if the simulation were distributed (say split across multiple machines each
simulating  part  of  the  lattice),  the  outcome  is  the  same  as  if  it  ran  on  one  machine .  NAP’s
distribution invariance principle states that as long as message envelopes and ordering are respected, it
doesn’t matter if two nodes talk via in-memory call or via network message – the result will match . So,
the Matrix can be sharded but NAP holds it together logically.
In summary, the Nexus Aternus Protocol is the glue  that allows the Universal Matrix pillar and the Trinity
Gate pillar (and others) to function together consistently. By implementing NAP in our design (even if
minimally at first), we guarantee that adding the Universal Matrix into the existing Trinity Gate setup will
not break determinism or consistency. Both pillars will speak the same “language” of PROPOSE/COMMIT
messages, sequence numbers, and hash-verified frames. This means from the perspective of the overall
Aether system, we are simply adding a new capability (the UMX topology engine) that plugs into the old one
via NAP – they can run in tandem with no conflicts.
Development Plan & Next Steps
Now that we have described the Universal Matrix pillar , the Synaptic Ley Protocol, and the Nexus Aternus
Protocol in detail, it’s important to outline a clear path to implement these in code (initially targeting an
offline browser-based JavaScript  environment, as requested). The development will proceed in stages,
each building compatibility with the existing Trinity Gate module and ensuring that the combined system
remains deterministic and verifiable. We will also note any gaps or open questions along the way, to be
addressed as needed:
1. Align with Existing Architecture:  Start by reviewing the  aether-gate-main  repository (the Trinity
Gate implementation and Triune Bridge) to understand its structure. Identify how pillars and protocols are4647
48
4950
51
13


--- Page 14 ---

represented in code. Likely, Trinity Gate was implemented as a class or module (with its node manifest entry
"type": "trinity_gate" ). The first step is to mirror this structure for the Universal Matrix pillar . For
example, define a UniversalMatrix  class or object that will hold the lattice state and provide methods
corresponding  to  UMX  operations  (place,  route,  propagate,  etc.),  and  ensure  it  can  be  instantiated
alongside the Gate in the simulation initialization. We should also verify how the main loop is orchestrated –
possibly there is a tick loop that calls each pillar’s update. We’ll want to hook the UMX update into that loop.
Essentially, the goal is to make adding UMX as seamless as adding another node  in the manifest, so
that the Gate code can remain largely unchanged and just start interacting with UMX via NAP messages.
2. Data Structures for the Lattice:  Implement the core data representation for the Universal Matrix. This
includes: - A list or registry of node objects in the simulation (or at least their essential state values). Each
node  could  be  an  object  with  properties  like  state (amount  of  conserved  quantity  currently  held),
layer and  grid (for  address/placement),  and  perhaps  a  unique  ID.  -  An  adjacency  structure  to
represent connections. A simple approach is an adjacency list: e.g., neighbors[nodeID] = array of 
{neighborID, weight} . Alternatively, an adjacency matrix (2D array) if number of nodes is small. Since
our initial offline demo might not have too many nodes, either is fine; adjacency list is more flexible if nodes
are dynamic. We also need a quick way to lookup a connection’s weight and update it (for SLP). - Storage for
usage statistics for each path, to decide SLP grow/prune. This could be a counter or moving average of how
much flow passed through each edge over the last M ticks. We might maintain a usage count per edge and
a tick counter to reset or decay it over time. - A random seed or deterministic pseudo-random generator for
placement. Since we want deterministic placement, we might use a PRNG seeded by e.g. a global seed
combined  with  current  network  state  hash.  In  a  simple  implementation,  we  might  not  even  need
randomness: we can place new nodes in the next available slot (or increment layer by 1 each time) to
guarantee determinism. But to follow spec, perhaps incorporate a hash function for tie-breaks as noted (like
if multiple equal-cost positions, pick the one with smallest SHA-256 hash of coordinates). - Data for global
invariants, like totalQuantity  to track sum of all node states (we can compute this on the fly or maintain
it incrementally to assert conservation after each tick).
3. Deterministic Placement ( UMX_PLACE ): Implement the node addition routine. This function takes an
“item” (which could be a new node or an agent to insert) and places it into the matrix given a seed. For now,
we can implement a straightforward rule: e.g., assign the new node layer = maxLayer + 1  (place it
one layer deeper than any existing node) and grid = 0  initially, or if layering isn’t needed in the demo,
place all nodes in layer 0 and just increment a position counter . The key is that if we call this function again
with the same seed and same current state, it returns the same (ℓ,g). For testing, we can simulate by
calling it twice and verifying the position is identical . In future, we can refine this to the full PFNA
approach (minimize description length): that would involve evaluating a cost function for possible positions
and choosing the best. We’ll leave that complexity for later , but we keep the interface such that we could
plug in an optimization later . We also generate any needed tie-breaker: e.g., if two positions are equally
good, compute a hash of (layer ,grid plus maybe nodeID) and pick the smaller hash as recommended .
Initially, we might not encounter such ties with a naive scheme. After determining position, we update our
data structures: add the node to registry, possibly connect it to existing nodes (wiring). If we are doing a
fixed topology (like a lattice grid or chain), we might connect the new node with some predetermined
neighbors (like connect it to a “hub” or to the previous node). Alternatively, we could start with no auto-
connections and rely on some external instruction or SLP to form them. A simple demo approach: connect
each new node to the first node (forming a star topology) or to the last node (forming a line). Remember to
log or announce the new node via NAP (a PROPOSE new-node, then COMMIT).24
5
14


--- Page 15 ---

4. Propagation Update ( UMX_PROPAGATE ): This is the function executed each tick to perform neighbor-to-
neighbor transfer while conserving totals. We implement this exactly as given: for each node, calculate
out[i] = Σ_j K[i→j] * state[i] , where K is some kernel matrix defining what fraction of node i’s
state goes to neighbor j. For now, we can define K in a simple way: if each neighbor gets an equal share,
and we want to move, say, 10% of the state each tick, then for each neighbor j of i, set ,
where  is number of neighbors of i and  is some small flow factor (like 0.1). This ensures not all state
moves at once, just a portion. Alternatively, K could be the identity of weights (normalized): we could use
the w(path)  from SLP as how much can flow. For simplicity, maybe treat w(i→j) as a capacity and send
a proportion of state through it. The key is to keep it deterministic and conservative. Then we compute the
incoming for each node i: that’s either just sum of out from neighbors that point to i (if K is symmetric or we
separately compute incoming flows). We update each node’s state: state[i] = state[i] + in[i] - 
out[i]. After doing this for all i, we can assert that the sum of  state hasn’t changed (floating-point
precision aside). If using JS, we need to be mindful of numerical precision, but since this is deterministic
simulation, slight float differences might not matter as long as consistent (for identical runs on same
engine). Optionally, we could use integer arithmetic scaled (if states are small integers or fixed point) to
avoid floating diffs. We’ll verify conservation by summing states and comparing to a stored total (perhaps
allow a tiny epsilon for float error). This propagation step corresponds to one tick of “physical” simulation in
the lattice.
5. Synaptic Ley Updates (SLP operations):  Decide how and when to trigger SLP adjustments. We could do
it  every  tick  after  propagation,  or  every  N  ticks,  or  on-demand  when  thresholds  are  crossed.  A
straightforward approach: at each tick end, update usage stats for each edge (e.g., add the amount of flow
that went through that edge this tick to a counter). Then, every tick (or every few ticks), check all edges: - If
an edge’s usage counter > θ_plus, increase its weight. If it was a non-existent edge but we are tracking
potential edges, perhaps if two nodes had repeated indirect interactions, we create a new edge. (Creating
entirely new edges might require identifying candidate pairs that aren’t directly connected but frequently
have multi-hop traffic. That’s more complex; we might skip new edge creation in the first demo, focusing on
adjusting existing edges’ weights which we initialize somehow. Or we can limit to creating edges between
already neighboring nodes with weight 0 that can be turned on.) - If an edge’s usage < θ_minus and it’s
been low for M ticks, decrement its weight. If weight goes to zero, remove the edge from neighbor lists. -
Reset or decay the usage counters (e.g., subtract some amount or zero them if using a moving window). - If
any edges changed, possibly output a NAP message about topology update (for logging).
For initial simplicity, we can define θ_plus and θ_minus as some constants. For instance, if we interpret
usage as “units of state transferred”, set θ_plus = 1 (meaning any transfer at all triggers growth) and
θ_minus = 0 (meaning if nothing transferred, prune). But that would be too aggressive (you’d add and
remove links constantly if one tick has vs. not). Better , accumulate usage over a window: say we check every
10 ticks; if in the last 10 ticks usage was > X, then grow. Or , simpler: use a boolean flag per edge: “was used
in last N ticks”. If yes for several intervals -> grow; if no for several intervals -> prune. We should choose
values such that behavior is stable in our test. Perhaps: require say 3 consecutive intervals of high use to
grow (θ_plus = 3 events) and 5 consecutive intervals of no use to prune (M=5). These are arbitrary but can
demonstrate effect.
Implement functions growEdge(i,j)  and pruneEdge(i,j)  to adjust weights arrays accordingly. Also,
we  might  want  to  visually  or  textually  output  when  a  link  is  grown  or  pruned  for  debugging  (e.g.,
console.log or accumulate in a log). This helps confirm determinism in repeated runs. K[i→j]= ∗Ni1η
Ni η
15


--- Page 16 ---

6. Nexus Aternus Messaging Layer:  Implement a minimal NAP simulation  in the JS environment. Since
all pillars are in one process, we don’t need actual network messaging, but we will simulate the protocol
steps: - Create a central message queue (or just an ordered sequence of function calls) that acts as the bus.
For example, we might have a function sendMessage(sender, receiver, payload)  that in reality just
directly calls a handler on the receiver . But we will still wrap the payload in a NAP envelope: generate a UID
(we can use a simple hash function or a global incrementing ID as a stand-in for H256) . Keep a set of
seen UIDs globally (for dedup). - The sendMessage function will check the seen set: if not seen, mark it seen
and deliver the payload (call receiver .handleMessage(payload)). If seen, ignore. - We will incorporate a
logical  clock:  maintain  a  globalClock  variable.  Each  time  we  send  a  message,  attach  timestamp = 
globalClock + 1  then update globalClock = that timestamp (Lamport). If receiving a message with a
timestamp (not needed in single thread, but just in case we simulate out-of-order), on receive, update
globalClock = max(globalClock, msg.timestamp). This ensures if later we introduced concurrency, we have
the  mechanism  in  place.  -  Define  message  types:  for  example,  we  can  make  payload  an  object  like
{verb:"PROPOSE", action:"ADD_NODE", data:{...}, uid, timestamp} . And similarly COMMIT,
etc. Then implement handlers in UniversalMatrix and TrinityGate (and possibly Loom stub) that switch
based on verb. - For initial offline run, we might not need a full two-phase commit if it’s all internal. But to
stick to design, we can simulate it: e.g., when adding a node, TrinityGate could send PROPOSE_ADD_NODE,
UMX on receiving can immediately respond with COMMIT_ADD_NODE (since presumably it will always
accept if it passes checks). Or we could bypass propose and directly commit if simpler , but showing the flow
is educational. - Other examples: TrinityGate might send a  QUERY_STATE  message to UMX asking for
some state, UMX replies with a message containing the requested info. Or Loom might broadcast a TICK
or CHECKPOINT  announce. - Ensure that every message and state change goes through these functions so
that, if needed, we could log them or apply dedup/ordering uniformly.
In code, this might look like a small event loop where at each iteration of simulation tick, we process all
pending messages in queue before moving to next tick logic, to simulate synchronous behavior .
7. Integrate Pillars via NAP:  With the NAP layer in place, tie Trinity Gate and Universal Matrix together: -
Example  integration  point  –  External  input:  If  Trinity  Gate  (from  previous  implementation)  has  a
mechanism to inject or simulate external input, have it create a NAP message to UMX. For instance, an
external script could call gate.inject("energy", amount, targetNode)  and then Gate would craft a
NAP PROPOSE message to UMX like {verb:"PROPOSE", action:"INJECT_ENERGY", data:{target: 
nodeId, amount: X}} . UMX’s handler upon receiving this would check the target exists and maybe
create  a  new  “environment”  node  if  needed,  or  directly  add  to  that  node’s  state  (but  then  to  keep
conservation, perhaps subtract from a special environment node or global zero). If all good, UMX responds
(or just internally does it and Loom logs it via a COMMIT). - Example – Node addition:  If an external event
or a high-level logic says add a new node (maybe representing a new entity), similar flow: Gate or some
orchestrator  sends  PROPOSE_ADD_NODE,  UMX  does  placement,  updates  its  data,  and  sends
COMMIT_ADD_NODE confirming with the assigned coordinates. Gate could then know the new node’s ID
and possibly create a representation for it if needed (though Gate might not need to, unless it visualizes
state). - Tick coordination:  We likely have a global loop. But if we simulate distributed, Loom could send a
HEARTBEAT(tick_number)  message each iteration. Instead of complicating, we can simply structure our
JS loop as: for tick in 1..N: 1. Gate processes any external input for this tick (maybe none). 2. Gate or Loom
triggers any scheduled events (like every 10 ticks maybe a checkpoint message). 3. UniversalMatrix executes
propagation  ( UMX_PROPAGATE ).  4.  UniversalMatrix  executes  SLP  adjustments  (maybe  every  tick  or
occasionally). 5. After state changes, if any important commit to log, send those messages (e.g., if a link
pruned, or if a significant state changed that others care about). 6. Press (if implemented) compresses state45
16


--- Page 17 ---

– not needed in first round likely. 7. Loom would record the state and any message (we might simply output
to console or store in an array). 8. End of tick. This sequence ensures deterministic order: e.g., if Gate
injection and UMX propagation happen in same tick, decide which goes first. Possibly external input should
be applied at the  start  of a tick (so that propagation that tick includes it). That means Gate’s PROPOSE
comes,  UMX  commits  and  updates  state,  then  propagation  runs  including  that  change.  This  needs
consistency: perhaps easier is to define tick as: apply all inputs, then propagate. We should document this
decision and ensure both modules follow it. For now, let’s choose: At tick boundary, process all incoming
NAP messages (inputs/commands) then run UMX propagation and internal updates, then finalize tick
by logging.  This matches a model where messages are processed as a transaction at the boundary of ticks.
Testing integration:  Once the pillars can exchange messages, test a simple scenario: - Add 2–3
nodes via NAP (simulate as if external commands). - Set initial states (maybe give node0 state 100,
others 0). - Run propagation for several ticks – watch the state values equalize or flow as expected,
verify the sum stays 100. - Trigger an SLP event artificially (e.g., force usage count on an edge) to see
a weight change, ensure that weight change affects subsequent propagation (if weight increases,
more flow goes through that edge). - If Trinity Gate has an output mechanism (like gather state
snapshot and output), use it to verify that simulation can output final state or logs. - Confirm that
repeating the test with same initial conditions yields exactly the same states and link changes at
each tick (determinism check). - Also ensure that the presence of UMX didn’t break Gate’s earlier
standalone behavior – if Gate had self-tests, run them with UMX included (they should still pass,
because UMX will just sit idle if not used).
8. Address Gaps and Tune Parameters:  During implementation and testing, we might encounter some
open  questions  that  require  decisions:  -  Choosing  thresholds  (θ_plus,  θ_minus,  M,  α,  β):  These  are
currently abstract. We should set them to something plausible for demonstration. As noted, maybe α
(increment) and β (decrement) are fixed small steps (like 1 unit of weight or 10% of current weight). θ_plus
could be defined in terms of baseline usage – for instance, if one full unit (100%) of a node’s state has
flowed through an edge in a given window, that’s significant usage. Or simply, if any flow at all in 3
consecutive windows, grow (this may be too sensitive). For now, pick easy values and be ready to adjust
after seeing behavior . Document these in the code as constants for easy tweaking. - Initial weights and
topology:  We need to decide how to initialize connection weights. Perhaps all direct neighbor links start
with weight 1 by default (meaning normal capacity), and non-neighbor (absent links) have weight 0. If a link
is weight 0, treat it as non-existent for propagation. Then SLP can raise it from 0 to 1 to “create” a link.
Alternatively,  start  with  a  fully  connected  lattice  of  small  weights?  But  that  would  violate  “only  local
connections” if fully connected. Better , start sparse (maybe a ring or line). Our test examples in planning
assume something like a line or star . - Conservation vs External Input:  How to handle injection or removal
of quantity from outside. If we strictly hold global sum constant, adding 10 units via Gate must come from
somewhere. One approach: have a special “Outside/Environment” node in UMX that represents external
world, which starts with an infinite (or large) reservoir . When Gate injects 10 to a node, we subtract 10 from
the environment node’s state. This keeps totals balanced. The environment node could be layer -1 or some
designated ID. Similarly, if something is extracted (Gate reading out some energy), we add it back to
environment. Implement this if external transfer is in scope. If not, we can assume the simulation is mostly
closed or that any injection is accounted as a known exception (but that weakens the purity, so environment
node is cleaner). -  Loom Logging:  While a full Loom implementation might be overkill for first round, at
least mimic it by printing out or storing key events: tick boundaries, state snapshots, link changes with their
UIDs/hashes. We could create a simple hash of state (like sum or JSON stringify state and hash) each tick to
simulate checkpoint hash. Then if needed, verify no divergence on re-run. These logs serve as proof-of-
concept that the ledger aspect is working. - UI/Visualization:  If this is in a browser , maybe set up a simple• 
17


--- Page 18 ---

HTML display of nodes and links updating each tick. Not mandatory, but helpful to see flows. Even a text log
output is fine initially. - Performance and Scalability:  For a small offline demo, performance is no issue.
But note that an O(N^2) adjacency matrix is fine for tens of nodes but won’t scale to thousands. As system
grows, we’d move to adjacency lists and more efficient event handling (only compute flows on active edges,
etc.). Also, in a distributed scenario, not everything can be global at each tick. But those considerations can
be left for later development once functionality is confirmed. - Concurrency Concerns:  In JS single-thread,
concurrency is not an issue. If moving to multi-thread or network, ensure that the logical ordering (Lamport
clock, etc.) is robust. This ties to an open design question: vector clocks vs. Lamport – vector clocks give a
partial order where concurrent events can be recognized as such. The design note  mentions either . For
now, Lamport is simpler and probably sufficient because we desire a total order anyway (for simplicity). -
Complete vs Partial Implementation:  Some advanced features described (like MDL-based placement,
skip-ahead protocol for Loom, etc.) will likely not be implemented in the first iteration. We should explicitly
acknowledge which ones are stubbed or simplified: - MDL placement: not implemented fully , using simple
deterministic placement instead. - Residual budgets: not enforced yet , just placeholders in message schema.
- Governance/verification packs: probably not relevant for code, more a procedural thing (we won't simulate
NDA or external auditors in code). - Multi-layer detailed addressing (like the  <ring, stack, slot>
addressing mentioned in the spec) – we may simply use layer , id for addressing now. - Mode switches and
other special features from spec (R, D*, etc.) – omitted in initial version, since those seem like fine-tuning
controls or specific algorithms. The plan should mention these so that developers and stakeholders know
what to expect in v1 vs future.
9. Testing & Validation:  After implementation, thorough testing should be done: -  Unit Tests:  for each
function (e.g., placement function returns same result for same seed, propagation conserves total, grow
increases weight appropriately, prune removes link after inactivity). - Integration Tests:  simulate scenarios
combining features: 1. Deterministic Placement Test: add two nodes with same seed in separate runs,
compare positions (should match) . 2. Conservation Test: initialize some distribution of quantity, run
many ticks, check that the sum of all node states remains constant every tick (within rounding error) . 3.
Flow/Adjacency Test: set up a known topology, ensure that disallowed links indeed carry no flow (e.g., if we
remove a link, verify nothing goes between those two nodes afterwards) . 4. Routing/Isolation Test: if we
impose a rule (perhaps simulate via policy input) that a certain node cannot reach another , verify that any
attempt to route fails or finds alternate route, and that an announcement is made if no route (maybe we log
“no route” case). 5. SLP Growth/Prune Test: deliberately cause heavy usage on one link (e.g., by biasing K for
that link) and inactivity on another , run enough ticks to trigger threshold, confirm weight changes occur
exactly when expected and are logged. Then ensure that affects propagation (the increased weight link
carries more share or if weight to 0, that edge no longer carries flow). 6. Idempotence Test: send a duplicate
message intentionally (if we can simulate that easily), confirm that the second one is ignored and doesn’t
double-apply changes (the state remains correct). 7. Order determinism: possibly simulate out-of-order
arrival by manually calling a handler out of intended order (if that’s possible internally) and see if our
ordering mechanism corrects it (this is harder to simulate in single thread, might skip). 8. Replay test: if
feasible, capture the sequence of NAP messages and state snapshots from a run, reinitialize and play them
back to see if final state matches original (this would test Loom/ledger concept). - We should automate
these as much as possible or at least do them manually and document results. Given it’s an offline browser
context, some tests might just be checking console output or internal variables after running a scenario.
10. Documentation and Compatibility Check:  Finally, ensure we update documentation and manifest
definitions. For compatibility with Trinity Gate’s system, confirm that: - The manifest or configuration file
includes an entry for the Universal Matrix pillar and that it’s loaded in the right order (most likely, Pillars52
3
11
7
18


--- Page 19 ---

Press, Loom, Gate, Matrix, etc. all get initialized). - The Trinity Gate’s expectations of the Nexus protocol are
met. For instance, if Gate expects a certain acknowledgment format on commit, our UMX should send that.
Check the Trinity Gate code for any hard-coded references (like looking for specific protocol names or keys
in messages). We might need to ensure our NAP integration uses the same keys or call Gate’s provided
functions for sending messages rather than rolling our own (depending on how modular it is). - If Trinity
Gate used any global objects for bus or clock, use the same rather than duplicate. - Run a scenario where
Trinity Gate was involved (for example, if Gate had a demo of interfacing with an external system, run it
again with UMX present and see that nothing breaks). - Prepare to unify logging: The output from our UMX
should be in line with Gate’s logging format if any, so that if someone inspects the logs, they see a coherent
combined log rather than two disjoint ones. - Check performance in browser: with a handful of nodes and
messages  it  should  be  fine,  but  if  using  heavy  loops,  ensure  not  blocking  UI  etc.  Possibly  use
requestAnimationFrame  or similar for tick loop if visualizing, or a web worker for heavy calc – but for
now, small scale, not needed. - Confirm that all  source citations and references  from this report are
understood and either implemented or intentionally deferred. (Since the user specifically wanted a full
coverage from all source material, we should verify we didn’t miss anything crucial: e.g., the concept of
“Skip-Ahead Protocol”  in Loom for foresight isn’t directly relevant to UMX/SLP, so probably okay to omit; the
mention of  “Galactic Connectome (GCX)”  was a naming alternative not chosen, we stuck to UMX;  “Codex
Eterna”  integration only lightly referenced since that pillar is separate; “crush without regret” checks refer to
Press verifying compression doesn’t break determinism – not our focus now; “Energy symmetry & information
causality”* envelope probably tied to Press and Loom interplay – beyond UMX scope for now.)
By following this plan, we will create an  initial implementation of the Universal Matrix pillar and its
protocols  that is directly compatible with the existing Trinity Gate pillar . The system will be able to run both
pillars together in an offline browser environment, demonstrating deterministic topology management
alongside deterministic I/O handling. Future iterations can expand on this foundation by refining placement
with MDL optimization, introducing more complex topologies, integrating the Self-Learning (Codex Eterna)
pillar once that’s developed, and scaling up the Nexus Aternus messaging for distributed operation. But
even the first version should clearly show the promised behavior: a reproducible “universal matrix” where
everything is connected and conserved, and a robust protocol ensuring that no matter how we combine or
distribute these components, they function as one cohesive, law-abiding system. 
7 ChatGPT-
development ant testing v2.md
file://file-R6QLhV5TURrzzXEaWUf1fY
6 ChatGPT-
development and testing v1.md
file://file-3J1ZEUB2HFtrWfDDk5VTWE
8 ChatGPT-Build new computing paradigm.md
file://file-TMtQ82QktMqvHxN77fmmgW1 2 3 7 910 11 12 13 14 19 24 25 26 27 28 29 30 37 38 41 42 43 44 45 52
4 6 815 16 17 18 20 21 22 23 31 32 33 34 35 36 39 40 46 47 48 49 50 51
5
19

### Source: `core/anchor_map_v1.md` (verbatim)

---
id: anchor_map_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# Anchor Map v1

Base anchors for layer-0 nodes; residual/epsilon anchors referencing base anchors; reconstruction guarantees for derived layers.

### Source: `core/subtick_semantics_v1.md` (verbatim)

---
id: subtick_semantics_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# Sub-Tick Semantics v1

Defines macro ticks vs sub-ticks; partitioning of input windows; equivalence requirement between macro and sub-tick execution (up to explicit epsilons).

### Source: `core/umx_layers_policy_v1.md` (verbatim)

---
id: umx_layers_policy_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Layers Policy v1

Layers, allowed inter-layer edges, per-layer cadences, and profile constraints for layer counts and frequencies.

### Source: `core/umx_mdl_objective_v1.md` (verbatim)

---
id: umx_mdl_objective_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX MDL Objective v1

Defines canonical traces, codelength functional L, ΔL computation and the acceptance rule ΔL ≤ −τ for proposals.
UMX treats MDL as parameterised and wired to the MDL Placement & Motif companion; placeholders are allowed until that spec is final.

### Source: `core/umx_profile_v1.md` (verbatim)

---
id: umx_profile_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Profile v1

Profile schema: fields for tick limits, MDL window and τ, residual bounds, NAP budgets, ledger parameters, layer caps, emergence thresholds and calibration status.

## Part 4 — Complement Docs: Zero Layer, Invariants, LLP→SLP, Profile Specs

### Source: `umx_complement_docs_a_d_zero_layer_a_1.md` (verbatim)

---

# Complement Doc A — Node, Anchors & Layer Model (UMX v1 Addendum)

### A.1 UMX Node & Role

The Topology report defines the **Universal Matrix Node (UMX Node)** as the pillar’s runtime instance and the “physics engine” for network state:

> “Universal Matrix pillar comprises… Universal Matrix Node (UMX Node)… a core module… that runs the Matrix logic each tick… maintains the data structures for the network… and per-connection weights or capacities… invoked to update the state of the network – propagating flows, applying any structural changes, and enforcing invariants.”

**Normative v1 stance (JS implementation-compatible):**

- There is exactly **one UMX Node** per simulation instance.
- That node owns:
  - The UMX integer lattice (your `AetherSubstrateCore` state arrays).
  - The topology metadata (PFNA anchors, adjacency/weights, degree caps).
  - The SLP statistics and structural metadata (even if in v1 some operators are disabled).
- On each tick:
  - UMX Node executes the **flux kernel** (SLP\_CONDUCT base) that your current spec already covers.
  - Optionally (v2+), it executes structural SLP passes (GROW/PRUNE etc.) over a longer horizon.

---

### A.2 Anchors & PFNA Addressing

The Topology doc formalises **PFNA** as the anchor system:

> “Anchoring & Addressing Scheme (PFNA Anchors): To place nodes deterministically, UMX uses a coordinate anchoring scheme sometimes referred to as PFNA (layer, grid) coordinates. Each node when created is assigned an anchor (ℓ, g)… The placement function `UMX_PLACE(item, matrix, seed)` uses the current network state and a given seed to compute an appropriate anchor… ensures that if you re-run the same scenario, each new node gets the exact same coordinates.”

Luminous Lattice frames anchors the same way:

> “Anchor (Node Anchor): The fixed coordinate of a node within the lattice, given as ((ℓ\_i, g\_i)) for layer and cell position… Anchors serve as addresses for placement and are used in distance calculations (d(a\_i,a\_j))… Changing a node’s anchor = moving it to a different layer or cell. The system deterministically selects anchors to minimize coding length + penalties.”

**Canonical v1 anchor model:**

- **Anchor type**:
  `Anchor = { layer: number; grid: IntVector }`
  where:
  - `layer = ℓ ∈ ℤ` (logical layer index; in v1 JS, we treat it as `0` or small integers).
  - `grid = g ∈ ℤ^d` (grid coordinate; in the current JS core this is flattened to `addrKey = y*W + x` for a 2D grid).
- **PFNA invariants (v1):**
  - For a given `(initial state, seed)`, `UMX_PLACE` **must be deterministic** and produce the same `(ℓ,g)` assignment on every replay.
  - `UMX_PLACE` **must not** violate topology constraints (no forbidden edges, no causal cycles).
- **Basic PFNA implementation (what v1 *************actually does*************):**
  The Topology doc explicitly blesses a simple base scheme:
  > “For now, in a basic implementation, PFNA could be as simple as layering nodes in order of insertion… and giving each a sequential grid number, or embedding them in a fixed lattice pattern.”
  > For JS v1 we can pin this as **normative**:
  - `layer` is fixed to `0`.
  - `grid` is implicitly `addrKey` from the UMX spec (`addrKey = y*W + x`).
  - Nodes / tiles are allocated in deterministic order: row-major over `(y,x)`.

---

### A.3 Zero Layer & Multi-layer Interpretation

The older reading of the docs treated “Zero Layer” as the same thing as the current UMX grid. That’s now superseded by Complement Doc A1 (see end of this file), which clarifies that “Zero Layer” is a *hardware thought experiment*, not a formal part of the UMX spec.

For purposes of this v1 addendum:

- The **UMX ************`layer`************ index** is purely logical (PFNA), not hardware-bound.
- Multi-layer distance penalties and stack routing (Δℓ costs) still exist in the theory, but are not implemented in JS v1.

---

### A.4 Node Fields & Internal “Stacks”

The Luminous report describes each node as carrying multiple **fields/stacks** across layers:

> “The spatial network of nodes (each running Trinity stacks) coupled via their middle-layer fields, enabling coherent energy and state translation across the whole.”

Your JS UMX config exposes **multiple fields per layer**:

> “Each layer i has `stateWidthsPerLayer[i]` integer fields… base config uses `[1]`.”

**v1 implementation stance:**

- One UMX cell at `(layer, addrKey)` is the *projection* of a richer “Trinity stack” into a fixed finite set of integer fields:
  - `stateWidthsPerLayer[layer] = N_fields`, each an `Int32Array(H*W)`.
- At v1 we only **require**:
  - At least one field (the “base conserved field” your spec already defines).
  - Optional extra fields may be used as:
    - residual / accumulator fields (for Press/Loom hooks),
    - separate conserved measures (e.g. different “mass” channels),
    - feature channels for Codex.

The detailed mapping from “Trinity stack state → fields[0..N-1]” is **deliberately not specified in current sources** — it’s treated as a higher-level binding decision (Trinity / Codex side), not a UMX concern. The Topology doc only cares that flows across membranes **conserve each measure** per field.

---

# Complement Doc B — Topology, Membranes, Routing & Flow

### B.1 UMX Responsibilities as Topology Pillar

The Topology report spells out what UMX is responsible for:

> “Universal Matrix (UMX) is… the spatial topology pillar… defines how components are arranged and interact… interactions are local (neighbor-to-neighbor only) and all transfers conserve globally measurable quantities… provides a deterministic lattice… guaranteeing reproducible placement of nodes, symmetric exchange between them, and enforcement of global invariants on every update.”

> “Maintaining Topology & Adjacency: UMX defines the allowable topologies… Admissible patterns can include radial, ring, mesh, or lattice connectivity… must obey UMX’s constraints: no forbidden links appear and no required link is missing. The pillar enforces admission constraints like preventing closed causal loops or oscillatory cycles… UMX can refuse or adjust a connection that would violate causality or stability.”

**Normative v1 stance for JS:**

- The **underlying graph** for v1 is a **2D lattice mesh**:
  - grid = ℤ², Manhattan neighbourhood, capped by `r` and degree `D★` as in your current spec.
- This mesh is *one* admissible topology out of the wider set (ring, radial, etc.), but it’s the canonical v1 implementation.
- UMX must:
  - maintain the invariant that connectivity obeys the mesh definition (or chosen topology),
  - prevent adjacency changes that introduce forbidden long-range edges or causal cycles.

---

### B.2 Membranes & Conservation

The Topology report gives the conceptual **membrane interface**:

> “Every node’s connections are mediated by a membrane interface that upholds these rules, so when one node transfers some quantity to another, the Matrix ensures the transfer is local… and allowed by the current network policy.”

> “Membrane Interfaces & Conservation Law… whenever Node A sends something to Node B, the membrane at A’s boundary subtracts that quantity from A… and the membrane at B’s side adds the quantity to B… no leak or creation… interfaces… impose translation or filtering rules… The membranes effectively guarantee locality… and conservation at each link.”

Luminous nails the conservation equation:

> “Membrane Conservation: Δμ = 0 – each lattice coupling conserves the measure μ… Any amount that leaves one node enters the other; there is no leak or creation… This invariant implements at the network level the Core theorem of measure conservation.”

**How this maps to your current integer kernel:**

- Your SLP step already does:
  - `S[u] -= flux; S[v] += flux` per edge, with ∑S constant.
- In this language, each edge `(u,v)` **is a membrane** enforcing Δμ = 0.
- Node isolation (“zero adjacency if policy forbids contact”) is achieved by:
  - either not including `(u,v)` in the `edges` list at all, or
  - giving it effective weight 0 (flux = 0 along that membrane).

This is already fully implemented: your flux kernel is the membrane law.

---

### B.3 Routing & Flow Management

The Topology report:

> “UMX provides mechanisms for routing messages or flows… If one component needs to reach another not directly connected, UMX computes a path (sequence of neighbor hops)… respecting… link capacity limits… routing algorithm will find a valid route if one exists… otherwise report no route… A greedy layered routing strategy is suggested, where routes prefer to move upward or downward layer by layer and are bounded by a maximum number of hops (a causal barrier c).”

Luminous describes the same routing policy:

> “Routing & Flow Constraints… routing strategy is greedy layered routing: a message… will first attempt to go straight up or down to reach the target’s layer… then around radially… embodied by the rule ‘greedy on (|Δstack|, ring hops), prefer lower σ estimate’… bounded by the causal speed limit c.”

**Normative v1 JS-level definition (no extra magic):**

- **UMX\_ROUTE(srcAnchor, dstAnchor, policy)**:
  - Works in PFNA coordinate space (anchors `(ℓ,g)`).
  - For v1, if you only use a single layer, routing degenerates to shortest Manhattan path in the 2D grid, bounded by `c`.
  - Path selection is deterministic:
    - always prefer minimal |Δℓ| (trivial in single-layer v1),
    - then minimal Manhattan distance in grid,
    - break ties with a deterministic rule (e.g. fixed direction ordering or anchor hash).
- **Separation of concerns:**
  - UMX\_ROUTE **plans** a path (sequence of node indices).
  - SLP\_CONDUCT (see Complement Doc C) **executes** the path as a conserved packet flow on top of the normal neighbor flux.

At the moment, your JS core does **not** expose an explicit routing API, but the Topology document treats this as a conceptual feature of UMX. Implementation-wise, this can be layered on top of the existing edge list with standard deterministic shortest-path search constrained by `c`.

---

# Complement Doc C — Structural Learning & SLP Plasticity (Design-Level)

This addendum is “design-accurate but not yet fully implemented” — i.e. this is where we know what it *should* do from the docs, but your JS core doesn’t yet implement it. I’ll mark that clearly.

### C.1 SLP as Structural Plasticity

Topology report:

> “Synaptic Ley Protocol (SLP)… governs how connections (leys) form, strengthen, or dissipate… SLP defines the deterministic rules of synaptic plasticity… responsible for operations like growing a new link… increasing the weight… trimming away links that fall into disuse. It provides routines such as **SLP\_GROW**, **SLP\_POTENTIATE**, **SLP\_PRUNE**, and **SLP\_CONDUCT**… SLP works in tandem with the base UMX propagation: UMX handles… neighbor exchanges each tick, and SLP periodically updates the network structure… based on longer-term statistics.”

Luminous describes the MDL-driven selection mechanism:

> “At each tick, it chooses connections and anchors to minimize total description length (code bits + penalties)… links that most reduce predictive residuals, keep the graph sparse, favor local connections, limit each node’s degree, and only move a node’s anchor if it’s worth it… candidate edges are evaluated in a fixed hashed order and accepted greedily if they improve the objective.”

### C.2 MDL Objective & Anchor Score

From Luminous:

> “Anchor Score (Re-anchoring Criterion): A\_i(a) = L\_i(a) + μ Σ\_{j∈N(i)} d(a,a\_j) + δ 1[a ≠ a\_i^prev]… The lattice chooses a\_i^\* = argmin\_a A\_i(a)… only switches anchor if it beats the current one by a margin (hysteresis threshold).”

> “Self-Learning Integration… every structural change has a clear cost ΔL and reward (residual reduction)… MDL objective… penalty weights λ, μ, γ, δ… not fully fleshed, but designed to be compatible with self-learning… deterministic nature means any learning can be evaluated safely.”

**What is concrete:**

- There **is** an MDL-style cost functional with at least:
  - a coding length term `L_i(a)`,
  - neighbour distance penalty `μ Σ d(a,a_j)`,
  - movement penalty `δ 1[a ≠ a_prev]`.
- Anchor tie-break uses a deterministic hash over anchor and indices.
- Edges/connections are chosen by a greedy, hashed order pass that accepts any candidate edge with ΔL < 0 (i.e. improves description length).

**What is NOT concretely specified yet:**

- Exact formula for `L_i(a)` (coding length) — the documents reference it but don’t freeze the exact encoding scheme.
- Exact values or recommended ranges for λ, μ, γ, δ, thresholds for ΔL, or hysteresis margins.
- Concrete sampling strategy for anchor candidates and edge candidates in JS.

So: the MDL objective is solid **conceptually**, but the numbers / encoding scheme are still **open design choices**.

---

### C.3 SLP Operations (Conceptual)

The Topology doc gives detailed behaviour for SLP\_CONDUCT and PRUNE and alludes to others:

> “SLP\_CONDUCT… focusing a flow along a particular chosen path… key rule… conservation at every hop… deterministic routing of a packet/flow… given [A, B, C, … Z] and an amount Δ, subtract Δ from A, add to B, … finally deliver Δ to Z… logging the transfer.”

> “Ley Pruning (PRUNE)… reduce the weight… if its usage falls below a low threshold θ\_minus for a sustained period… usage(path)<θ\_minus… decrement its weight by β or cut to zero… with two thresholds (θ\_plus for growth vs θ\_minus for prune)… memory of M ticks of inactivity… prevents flapping…”

**Concrete logic we can lift:**

- **SLP\_CONDUCT(path, Δ)**:
  - Takes a list of node indices `[n₀,…,n_k]` and an integer Δ.
  - Applies a conserved walk: subtract Δ at source, add Δ at next, etc, within one tick.
  - Fails or is deferred if any hop is missing or pruned.
- **SLP\_PRUNE(path)**:
  - Maintains per-link usage history over `M` ticks.
  - If usage < θ\_minus for M ticks, decrement weight by fixed β; if weight hits 0, drop the edge from adjacency.

**Again, missing for direct implementation:**

- Concrete definitions for `usage(path)`, θ\_plus, θ\_minus, M, β.
- Frequency of SLP evaluation (per tick, per N ticks, etc.).
- Exact data structure for SLP’s usage counters in the JS core.

---

### C.4 Implementation Status vs Design

- **Your current JS UMX core** (Aether\_Substrate\_v1) implements:
  - The flux kernel (base SLP conduct as a bulk neighbour exchange).
  - No explicit SLP\_GROW/PRUNE/etc. APIs, no MDL-driven structural changes.
- **The docs define** SLP as the long-horizon structural brain **on top of** that kernel.

So for now, your main spec is complete for the **static topology / conservation engine**. This complement doc marks out the **future structural learning layer** as design-specified but **not yet concretely parameterised or implemented**.

---

# Complement Doc D — NAP, Aether Bus & Cross-Pillar Coupling

### D.1 Nexus Aeternus Protocol (NAP) Role

Topology report:

> “Nexus Aeternus Protocol (NAP)… overarching communication and synchronization protocol… knits all pillars… ensures that all subsystems ‘talk’… deterministically… listed among UMX’s protocols because the Matrix heavily relies on NAP to interact with other parts… one of the ‘three umbrella protocols’ alongside Trinity Gate and Lattice protocols.”

> “Global Synchronization & Integration… Any change in the network… can generate a transaction on the Nexus bus so that other pillars (Gate, Loom, Press) are aware… UMX… applies its propagation updates in discrete deterministic time-steps (τ increments) and hands off a snapshot… to Loom for hashing and record-keeping each tick.”

### D.2 Aether Bus

> “Aether Bus (Routing Fabric): The Nexus Aeternus introduces the Aether Bus, a logical communication fabric… While UMX’s topology handles physical adjacency and flow, the Aether Bus handles logical message passing which might span multiple hops… provides address discovery, partitioning, backpressure… still governed by deterministic rules… routing algorithm on the bus… could even utilize the UMX topology… for physical path.”

**Normative v1 stance:**

- **Message path**:
  - Logical: NAP/Aether Bus chooses a route between anchors.
  - Physical: that route is realised as a UMX path of PFNA neighbours.
- NAP frames include:
  - IDs, PFNA source/destination, payload, hash references to Loom/Press manifests.
- UMX does **not** parse the payload semantics; it only:
  - enforces that state changes coming from NAP are translated into valid Gate writes,
  - optionally uses NAP to broadcast adjacency changes and node placement.

Your existing `nap.js` envelope format from the Gate repo is already described in the main spec and is compatible with this.

---

# Gap Map v1 — Holes, Ambiguities & Next Investigation Targets

Here’s the “everything we’re missing” list from the perspective of **full, hand-off-to-dev** implementation. Each bullet = (a) what sources say, (b) what’s missing.

---

### 1. MDL / Description-Length Objective (Topology & SLP)

- **Sources say:**
  - UMX and SLP choose edges and anchors to **minimise description length** under penalties for distance, degree, movement etc.
  - There are penalty weights λ, μ, γ, δ and an anchor score A\_i(a) as given.
- **Missing / open:**
  - Exact definition of `L_i(a)` (coding scheme).
  - Explicit MDL objective for *edges* (what is the cost of a link, in bits?).
  - Concrete numeric defaults / ranges for λ, μ, γ, δ, hysteresis margins, thresholds.
- **Next step:**
  We need either:
  - A dedicated **MDL spec** doc (even if high-level) that pins one canonical coding scheme for v1, or
  - A “minimal viable MDL” profile: e.g. use simple bit-length approximations for weights, plus L1 distance penalty and movement penalty, with explicit example numbers.

---

### 2. SLP APIs & Data Structures

- **Sources say:**
  - There are deterministic routines SLP\_GROW, SLP\_POTENTIATE, SLP\_PRUNE, SLP\_CONDUCT, SLP\_STACK, etc., with behaviour described in English and some inequalities.
- **Missing:**
  - Concrete **function signatures** for JS (inputs, outputs, tick cadence).
  - Storage layout for usage counters, weights, aggregated statistics.
  - Precise definitions of thresholds (θ\_plus, θ\_minus, M, β, growth increments, etc.).
- **Next step:**
  - Extract from your existing code/tests (if any) or write a **“SLP v1 API & Param Sheet”** with explicit TypeScript types and a single recommended evaluation cadence (e.g. every N ticks).

---

### 3. Multi-Layer UMX

- **Sources say:**
  - Anchors are (ℓ,g), layers can represent different scales, abstraction levels, or partitions.
  - Greedy routing uses Δℓ as a first priority.
- **Missing:**
  - Exact encoding of ℓ in JS structures (where is layer index stored per node/cell?).
  - Rules for which layer pairs can connect (e.g. ℓ and ℓ±1 only, or more?).
  - How `stateWidthsPerLayer` ties into PFNA layers vs “internal fields”.
- **Next step:**
  - Decide whether the first gate-compatible implementation stays **single-layer** or introduces at least ℓ ∈ {0,1}.
  - If multi-layer is desired, write a minimal **Layer Policy Table**: allowed ℓ→ℓ connections, distance penalty function in Δℓ, etc.

---

### 4. Node Manifest & Actor Slots

- **Sources say:**
  - Each node is effectively “a Trinity stack mapped into the lattice”, with middle-layer coupling, and PFNA anchors.
  - UMX Node manages “lists of nodes and their coordinates” and per-connection capacities.
- **Missing:**
  - Explicit **node manifest schema** (what exactly is stored per node beyond anchor and fields: actor slots, IDs, capacities, policies).
  - Mapping from “actor slots / Trinity stacks” to UMX integer fields.
- **Next step:**
  - Draft a **UMX Node Manifest v1**: minimally `{ id, anchor, fieldOffsets, topologyMeta, policyFlags }`, without overcommitting to Trinity internals.

---

### 5. NAP Bus Details & Backpressure

- **Sources say:**
  - NAP provides membrane-boundary messaging, address discovery, partitioning, backpressure.
  - It ensures exactly-once semantics and deterministic ordering. (Your spec already covers the envelope & ordering basics.)
- **Missing:**
  - Concrete JS implementation in the Gate repo for **backpressure** & **partitioning** hooks from NAP → UMX (e.g. how UMX throttles SLP growth when bus says “too busy”).
  - Any normative timeouts and queue size limits.
- **Next step:**
  - Extend the existing `nap.js` with a small **NAP Flow Control profile**: message queue limits, deterministic dropping/throttling rules, and explicit mapping to UMX tick rate.

---

### 6. Integration with Loom & Press (Beyond Hash + P-deltas)

- **Sources say:**
  - Loom logs hash-chains, P-blocks, and can reconstruct exact state.
  - Press may compress adjacency, flow logs, or motifs for storage/transfer.
- **Your UMP spec already covers:**
  - `rootHash`, P-deltas, I-block cadence and how they flow out to Loom-like components.
- **Missing:**
  - A **formal manifest schema** joining UMX TickLedger ↔ Loom records ↔ Press compression units (what’s the canonical “tile delta” format, what exactly gets hashed).
- **Next step:**
  - Write a **“UMX–Loom–Press Interop v1”** doc defining:
    - tick record shape,
    - allowed compression transforms,
    - how to validate equality on replay.

---

### 7. Parameter Calibration & Profiles

Across UMX + SLP + PFNA we now have a bunch of knobs:

- r, c, D★, SC, k per layer (already in your spec).
- MDL penalties (λ, μ, γ, δ).
- SLP thresholds (θ\_plus, θ\_minus, M, β).

**Missing:**

- Any **canonical parameter set(s)** (“Low-res dev profile”, “Production profile”, etc.) in the docs.

**Next step:**

- Create a **Profiles Annex** listing a few named parameter sets, with explicit values, so devs can just pick one.

---

## How to use these addenda with the main spec

- Think of **your current spec** as **“Core UMX/SLP Kernel + Gate Integration”**.
- These docs add:
  - **A**: Node/anchor/layer semantics.
  - **B**: Topology, membranes, routing semantics.
  - **C**: Structural learning & MDL (design, currently unimplemented).
  - **D**: NAP/Aether-Bus coupling details.

Next round, when you feed in more material (e.g. any raw Trinity or Aether gate code, or more notes on MDL/SLP thresholds), we can:

- turn the Gap Map bullets into **concrete API/param tables**, and
- fold A–D into a single “v1.1 Combined Spec” that’s closer to a *drop-in implementation pack* for devs.

---

Perfect, that helps a *lot*. I’ll treat what you just said as canon and adjust everything around it.

Here’s a **small, bolt-on doc** you can treat as an addendum / errata to the spec and the previous complements.

---

# Complement Doc A1 — “Zero Layer” Clarification & Scope

### A1.1 Source vs. Intent

In the Luminous / topology material, “Zero layer” is described like this:

> “The Zero-layer often refers to the baseline physical layer (ℓ=0) in which actual devices/nodes run; higher ℓ might be virtual overlays or aggregations… In some descriptions, ‘Zero layer’ is equated with the entire lattice when instantiated in hardware – essentially the substrate proving the Core equations.”

Your clarification:

> zero in most places refers to conceptual hardware that would natively run the aether system and not really a part of the universal matrix. it was more of a thought exercise around whether it would be possible and feasible as hardware.

So we lock this in:

- **Chat is the final source of truth.**
- “Zero layer” is **not** a formal part of the Universal Matrix spec; it is a **hardware thought experiment**:
  > “what if we had physical silicon/analog fabric that implements Aether natively?”

---

### A1.2 Normative stance for the UMX spec

For the **Universal Matrix Pillar spec**:

1. **No built-in “Zero Layer” index.**

   - UMX’s `layer` index (ℓ in PFNA) is purely a **logical lattice layer**, *not* a hardware layer.
   - The spec MUST NOT assume that `layer = 0` means “physical Zero layer”.

2. **UMX is hardware-agnostic.**

   - The spec for the Universal Matrix Pillar describes:
     - integer state model,
     - SLP flux and structural rules,
     - topology constraints,
     - Nexus / Gate contracts,
   - but **does not** dictate whether it runs:
     - in JS in a browser,
     - on a CPU cluster,
     - or on a future “Zero layer” custom substrate.

3. **Zero Layer is external to UMX.**

   - If/when we explore dedicated Aether hardware:
     - that will be a **separate doc** (e.g. “Zero Layer Hardware Notes” or “Aether Native Fabric v1”),
     - which **implements** the UMX math at a lower level,
     - but is not part of the UMX normative interface for devs.

4. **PFNA anchors are purely logical.**

   - `Anchor = { layer: number; grid: … }` should be read as:
     - “logical layer within the lattice model”,
     - “logical grid position in the simulation space”.
   - Any mapping from these logical coordinates to hardware (including a hypothetical Zero substrate) sits *outside* the UMX spec.

---

### A1.3 Corrections to prior complement docs

Relative to what was written earlier:

- Anywhere it implied:

  > “Zero Layer = your current UMX integer grid”

  treat that as **retracted**.

- The corrected view:

  - “Zero layer” is **conceptual hardware substrate** you were thinking about.
  - The **current UMX implementation** is a *software* lattice that could one day be hosted on such hardware, but doesn’t know or care about it.

So when devs read the combined spec:

- They should see **only**:
  - PFNA layers as logical indices,
  - UMX lattice as a software model,
  - no obligation to model or emulate a Zero hardware layer.

### Source: `umx_complement_doc_e_invariants_layout.md` (verbatim)

---

# Complement Doc E — Global Invariants, Bandwidth, Reversibility & Node Layout

This doc captures **extra features and constraints** that show up in the older UMX / symbolic-node reports but weren’t fully spelled out in the v1 spec + A–D.

Where possible I mark:

* **v1 normative** — things the current UMX/SLP kernel already satisfies or can trivially satisfy.
* **v2 / design-level** — things clearly described but not yet wired into the JS core.

---

## E.1 Global Invariants Beyond “Sum of Field” Conservation

The v1 spec already says UMX conserves the global sum of each integer field (SLP flux, ∑S constant). The older docs broaden this into a **family** of invariants:

### E.1.1 Conservation of Abstract Measure (μ)

The symbolic node paper defines a conserved “measure” μ at system level:

> “There is an abstract measure (or several measures)… nodes can exchange these tokens but cannot create or destroy them… membranes enforce this by requiring any outgoing token from a node to be received by another… ensuring a zero-sum dynamic: what leaves one part enters another.”

This is exactly what your **base UMX integer field** is already doing:

* **v1 normative:**

  * Each UMX conserved field = one such measure μ.
  * SLP’s `S[u] -= flux; S[v] += flux` per edge enforces Δμ = 0 across each “membrane” edge.

* **Design implication:**

  * If you decide to treat additional fields as separate measures (e.g. “mass”, “charge”, “bandwidth tokens”), **each field should have its own conservation equation**:

    * For each field f: `Σ_cells S_f` = constant, except when explicitly coupled to the environment (e.g. “system boundary” nodes).

> **Plain words:** What your SLP already does for the base field is *exactly* the abstract “conserved tokens” law. Extra fields can be treated as extra conserved measures if you want.

---

### E.1.2 Bandwidth Conservation / Token-Bucket Model

The symbolic node paper elevates **bandwidth** itself to a conserved resource:

> “We impose a limit on communication throughput… viewed as a conserved resource in time… a fixed number of bandwidth tokens are in circulation; a node must acquire a token… to send a message… The total number of tokens limits how many messages can be simultaneously in flight.”

> “Membrane… can throttle the rate of outgoing or incoming messages to respect a global bandwidth limit… information throughput… is bounded by the number of interface channels… membranes throttle communication to respect a global invariance (bandwidth conservation).”

**This is not yet in the v1 UMX spec.** It’s a distinct capability:

* **Design-level feature:**

  * Treat “bandwidth tokens” as **another conserved measure**:

    * Finite total number B of bandwidth tokens in the whole system.
    * To send a message or SLP_CONDUCT path, a membrane must hold ≥1 token, attach it, then get it back on ack.
  * Globally, number of active messages ≤ B.

* **Implementation hooks (future v2):**

  At UMX/NAP boundary:

  * A NAP / membrane layer keeps per-node **bandwidth token counters**.
  * UMX routing / SLP_CONDUCT checks token availability before launching a long-range flow.
  * Tokens themselves can be stored in a UMX integer field (e.g. field #1) with ∑ tokens constant.

* **v1 normative:**

  * v1 spec does **not** require bandwidth conservation, only field-sum conservation. This doc marks bandwidth as a **future invariant** to integrate.

---

### E.1.3 Symmetry, Time-Reversibility & DAG-Style Causality

The older docs go further than “conservation”: they talk about **symmetry** and **time-reversibility**:

> “Every interaction is symmetric and reversible – if Node A loses X and Node B gains X, one could conceptually reverse time and get X back to A.”

> “Membrane-mediated channels… reversible… each membrane-mediated exchange is an invertible primitive… by composition, the entire network… is invertible.”

And for **causality / no cycles**:

> “The network of dependencies must form an effective directed acyclic graph for state updates… dynamic feedback is achieved through stored state and new iterations, thereby aligning with a causal time progression.”

**v1 implications:**

* Your SLP flux update is already:

  * Pairwise symmetric (u↔v) and sum-zero → conceptually reversible per tick (given full state history or inverse step).
  * Driven in discrete ticks τ with no instantaneous cycles beyond the pre-built undirected mesh.

* **Normative v1 tightening (optional add to main spec):**

  1. **Static causality constraint:**

     * The **logical dependency graph** used for updates in a tick must be acyclic.
     * UMX’s update graph per tick is effectively the undirected lattice plus Gate writes → no directed feedback edges inside a single τ-step.

  2. **Reversible-step guarantee (design-level but realistic):**

     * Given `state(τ)` and full record of Gate writes at τ, UMX’s SLP step should be an injective mapping (no information lost).
     * Practically: the combination (state at τ, writes, edge list) should be sufficient to recover `state(τ+1)` and vice versa.

> **Plain words:** The old docs basically say: “UMX update graph per tick behaves like an acyclic circuit with reversible wires.” Your integer flux rule already behaves that way; we’re just making it explicit as a property.

---

## E.2 Membrane-Level Protocols: Acks, Retries, Rollback, Fault Handling

The symbolic-node report is full of **channel-level behaviours** that weren’t fully called out in the UMX spec but align strongly with NAP and membrane semantics.

### E.2.1 Acknowledgement & Retries

> “Each membrane might have a timeout – if it sent something and got no ack, it can retry… If a message appears malformed, a membrane can request a resend… If a message is duplicated… B’s membrane could detect a duplicate (two messages with same ID) and discard the extra… the lattice doesn’t break invariant constraints despite these faults.”

This maps directly onto **NAP** and Gate:

* NAP envelopes already have content hashes and IDs; Gate is the layer that can:

  * detect duplicates (same payload_ref, same nonce),
  * refuse to commit if ack fails or timeout triggers,
  * request resend.

* **v1 UMX stance:**

  * UMX core **never sees** multiple applications of the same logical write:

    * NAP + Gate enforce exactly-once semantics before calling `enqueue*`.
  * UMX spec can **explicitly depend on this contract**:

    * “All deduplication, retries, and malformed message handling are performed by NAP/Gate before UMX writes are enqueued.”

> **Plain words:** The “ack/timeout/retry” stuff is real, but it lives in NAP+Gate. For UMX spec we just say: “I only see clean, deduped writes; everything else is NAP’s job.”

---

### E.2.2 Rollback & Anti-Messages (Reversible Channels)

The older paper talks about each membrane retaining enough info to **undo** a message:

> “The membrane could tag outgoing messages with… state to undo the operation… allowing an ‘anti-message’… if something goes wrong or if a rollback is needed… by composition, the entire network of communications is invertible.”

UMX v1 has no explicit “anti-message” API, but **Loom + NAP provide a path**:

* Loom stores tick-by-tick `TickLedger` with hashes; you can:

  * roll back to earlier I-block snapshots,
  * re-run a segment with different choices.

* NAP ensures that **commits are transactional** and traceable; if a commit is rolled back, you simply discard all subsequent ticks in the log and replay from snapshot.

**v1 normative clarification:**

* **UMX does not implement internal rollback;** rollback is:

  * a **system-level operation**:

    * choose a prior snapshot in Loom,
    * re-instantiate the UMX node at that state,
    * replay NAP/Gate events.

* However, the SLP/UMX step rules are **pure and deterministic**, so rollback + replay is always possible in principle.

> **Plain words:** The spec doesn’t need anti-messages inside UMX; we rely on Loom snapshots + deterministic ticks to get effective rollback.

---

### E.2.3 Fault-Tolerance & Localisation of Errors

The symbolic system emphasises **graceful degradation**:

> “The system should exhibit graceful degradation or self-stabilization under imperfect propagation… local disruptions remain local – due to encapsulation… one node’s link is flakey, it should not corrupt the state of distant nodes except by omission… the test is successful if… after introducing 10% message loss, the system still conserved all tokens, and all nodes eventually synchronized on a common state.”

For UMX:

* **v1 normative** (already true if Gate is sane):

  * Dropped or delayed Gate writes **do not** violate SLP invariants:

    * If a write never arrives at UMX → sum of fields stays consistent (no “half transfers”).
    * If a write arrives later → it is applied at a later τ; determinism is still maintained.

* **Design-level behaviour (optional):**

  * NAP / Gate may add:

    * per-node error logs,
    * local “circuit breaker” behaviours (throttle writes if repeated failures seen),
    * but these don’t change UMX mathematics.

---

## E.3 Vertical & Radial Node Layout (Stacks & Nests)

The abstract node system defines a **two-dimensional arrangement** of nodes:

> “Nodes are arranged in two modes simultaneously: vertical (stacked) arrangement and radial (nested) arrangement.”

* **Vertical (stacked):** DAG-style pipelines of nodes; projection of one feeds membrane/core of another.
* **Radial (nested):** nodes contained within other nodes; parent node’s membrane wraps inner lattice; children’s interactions with outside world go through **two** membranes.

Your **Luminous** report further ties this to **Nexus addressing**:

> “Address = ⟨ radial ring , vertical stack , local slot ⟩ … e.g. 2.0#5 meaning radial ring 2, stack level 0, slot 5.”

**UMX v1 implications:**

* v1 PFNA anchors are currently `(layer, grid)` for the 2D substrate. The older reports show a richer 3-part address for the **Nexus-side view**.

* **Normative v1 (safe interpretation):**

  * **UMX** only needs `(layer, grid)`; any mapping from `(radial ring, stack level, slot)` to `(layer, grid)` is a **NAP/Gate-level concern**.
  * Vertical/radial semantics are **logical**:

    * vertical stack → path constraints / routing rules,
    * radial nesting → scope / visibility & extra membrane hops.

* **Design-level for future v2:**

  * Provide an **address mapping table**:

    * e.g. map `(ring, stack, slot)` into a single PFNA layer index and grid coordinate.
    * enforce that vertical edges respect DAG ordering; radial edges go through parent’s membrane.

> **Plain words:** The old docs say “nodes can be in stacks and nests, and addresses look like ring.stack#slot”. For UMX v1 we just keep PFNA `(layer,grid)` and let NAP/Gate decide how to encode that richer address into PFNA coordinates.

---

## E.4 Emergent Geometry (Metric Tensor from Link Weights)

Luminous has a mathematically explicit “emergent metric”:

> “A19 (Emergent Metric Tensor):
> ( g^{\mu\nu}(X) \propto \sum_{j \in \mathcal{N}(i)} w_{ij}, \Delta X^\mu_{ij}, \Delta X^\nu_{ij} ) – The lattice defines a metric from link weights… heavier connections contract distance along that dimension… in continuum limit, this leads to field equations analogous to General Relativity (geometry follows distribution of residual energy).”

This is **purely interpretive**: you can treat the graph of nodes + weights as defining a geometry.

* **v1 status:**

  * There is **no requirement** that UMX compute / expose `g^{μν}`.
  * The **data to compute it** *are there*:

    * adjacency (edges),
    * weights or coupling strengths `kℓ` (and any SLP weights you add).

* **Design-level feature:**

  * An optional introspection module (e.g. in Press or a debug mode) could:

    * map node indices to coordinates `X_i` (embedding),
    * compute `g^{μν}` as above for visualisation/analysis.

> **Plain words:** The metric tensor is a nice “view” of UMX’s connectivity, not a required part of the core. Good future feature; no changes to UMX math needed.

---

## E.5 Convergence, Ergodicity & “No Runaway” Behaviour

The multi-layer node paper spends a lot of time on **convergence tests**:

> The system either “finds a fixed point or a limit cycle… any divergence scenario (like infinite escalation) is structurally prevented… we aim for the network to be ergodic or convergent to an attractor in state-space, rather than chaotic.”

Test scenarios include:

* Extreme recursion depth; ensure recursion is cut off gracefully.
* Unbounded message storms; ensure **bandwidth limits** throttle them.
* Lost/duplicated messages; ensure no invariants are broken.

**UMX v1 reality check:**

* Your **integer SLP** on a finite lattice has:

  * Global conservation,
  * Bounded integer ranges (Int32),
  * Tick-bounded propagation.

  So in practice, SLP + fixed topology will produce some bounded evolution (often diffusive smoothing → equilibrium), but **UMX does not enforce a guarantee** like “must converge to fixed point or limit cycle” in the spec.

* **Design-level future tightening:**

  * Add **optional convergence monitors** outside UMX:

    * e.g. Press / Loom modules that inspect trajectories of hashes or norms of state vectors to detect:

      * equilibrium (no changes),
      * periodic cycles (repeating hash sequence),
      * or persistent “high activity” that could be flagged.

  * Use **bandwidth tokens** and recursion depth limits (at the protocol / NAP level) to prevent system-level runaway, as per the symbolic-node paper.

> **Plain words:** The math suggests UMX won’t blow up, but the “it always converges or cycles” statement lives at the whole-system level (UMX + NAP + stack logic). v1 spec doesn’t promise that; this doc marks it as a design goal.

---

## E.6 Hardware “Machine Zero” Notes (Non-Normative)

The `umx v2.pdf` note basically says:

* each **physical machine-zero** behaves like a symbolic node (core/membrane/projection),
* a mesh of such zeros, running Aether, also satisfies the conservation/causality rules.

You already clarified:

> zero in most places refers to conceptual hardware… not really a part of the universal matrix.

So:

* **Explicit non-normative stance:**

  * All machine-zero / hardware references are **illustrative only**.
  * The Universal Matrix Pillar spec stays **hardware-agnostic**:

    * UMX may run in JS, on CPUs, or on future Zero hardware—doesn’t matter.

This matches Complement Doc A1 and keeps UMX’s obligations clean.

---

## Gap Map v2 — New Gaps/Exposures from Older Docs

Building on the earlier Gap Map, here are **new or refined gaps** exposed by the older reports.

### G8. Bandwidth Token System & Per-Membrane Throttling

* **Docs:** symbolic node system — bandwidth conservation, token bucket model.
* **Gap:** No field or API for bandwidth tokens in UMX v1; no NAP/Gate spec for token allocation.
* **Need:** Decide:

  * which field (or external registry) represents bandwidth tokens,
  * how tokens attach to NAP messages / SLP_CONDUCT paths,
  * how per-node limits map to global B.

---

### G9. Membrane Handshake, Acks & Rollback Semantics (Formal API)

* **Docs:** symbolic node → acks, retries, sequence tagging, rollback via reversible channels.

* **Gap:** No explicit spec for:

  * NAP-level ack/timeout semantics,
  * error codes,
  * mapping from “failed commit” to UMX/loom rollback rituals.

* **Need:** A **NAP/UMX Channel Protocol v1** document:

  * ack types,
  * retry rules,
  * when to escalate to rollback vs ignore.

---

### G10. Vertical/Radial Address Mapping & Policy

* **Docs:** vertical stacks, radial nests, and `⟨ring, stack, slot⟩` addresses.
* **Gap:** No standard mapping from `(ring,stack,slot)` to PFNA `(layer,grid)`.
* **Need:** A small **Address Mapping Annex**:

  * e.g. encode `ring` in part of `layer`, `stack` in another, `slot` → grid,
  * define which topologies require which mapping.

---

### G11. Emergent Metric Tensor Exposure

* **Docs:** A19 metric tensor from link weights.
* **Gap:** No spec for how (or if) UMX exposes this metric.
* **Need:** Decide:

  * Is this purely a Press/Loom analysis view?
  * If yes, document that UMX only guarantees adjacency + weights; metric computation is external.

---

### G12. Convergence / Ergodicity Guarantees

* **Docs:** guarantee system avoids divergence, aims at fixed point or limit cycle, with tests at extreme recursion depth and high traffic.
* **Gap:** UMX v1 spec doesn’t guarantee overall convergence; only conservation & locality.
* **Need:** Either:

  * explicitly **downgrade** this to “system-level design goal, not pillar-level guarantee”, or
  * add a minimal convergence test or constraint set for production profiles.

---

### G13. Explicit DAG Constraint & Feedback via Delay

* **Docs:** static connectivity must be effectively acyclic; feedback via delayed messages, not direct cycles.
* **Gap:** v1 mentions causality/hop caps but doesn’t formalize “no directed cycles in update graph”.
* **Need:** Clarify:

  * For UMX: update graph per tick is undirected SLP flux → fine.
  * For higher-level routing/stack flows: specify how to enforce DAG-ness when building vertical stacks.

---

### G14. Node Manifest vs. Symbolic Node Triplet (Core/Membrane/Projection)

* **Docs:** three-layer node architecture, membrane as only interface, projection as external view.
* **Gap:** Node manifest for UMX v1 doesn’t yet annotate which state belongs to core vs membrane vs projection.
* **Need:** Add **non-breaking tags** to node manifest schema to mark:

  * which UMX fields are “core state”,
  * which represent “projection” (externally exposed),
  * and which are implicitly membrane-managed.

---

### Source: `umx_complement_doc_f_llp_slp_propagation.md` (verbatim)

---

# Complement Doc F — LLP→SLP Propagation Semantics & Temporal Behaviour

This doc treats **Luminous Lattice Protocol (LLP)** as the earlier name (and slightly wider framing) of what is now **Synaptic Ley Protocol (SLP)** inside UMX. It pulls in everything LLP says about **how propagation actually behaves** and compares it to your current UMX+SLP v1 spec.

---

## F.1 LLP Scope vs SLP v1 Core

LLP defines itself as the substrate propagation layer:

> “LLP governs how accepted state changes propagate across Aether’s internal state lattice… enforcing continuity and conservation at every step… responsibilities include local propagation & global consistency, deterministic state evolution, continuity & stability.”

Your UMX/SLP v1 spec already covers:

* integer-only state,
* conservative flux per edge,
* deterministic ordering,
* per-tick tickOnce() pipeline.

**Refinement:** LLP makes explicit that SLP/LLP is responsible for the **full “shape” of propagation over time**, not just individual flux updates:

* Must be **equilibrium-seeking** (tends toward balanced states under no new input).
* Must provide enough structure for **time compression and replay** (Loom) and **space/time compression** (Press).

For v1 we can treat this as:

* **Normative:** deterministic, conservative, local, replayable.
* **Design-level goal:** equilibrium-seeking and “nice” behaviour (no runaway, diffusive-like).

---

## F.2 Propagation Handshake: Merge → Propagate → Resolve

LLP describes propagation as a **multi-phase handshake**, not just “run flux once”:

> “Every propagation step respects deterministic rules… often described as ‘every node agrees on the same handshake’… protocol defines a fixed sequence of **merge → propagate → resolve** steps that all nodes follow to minimize any residual difference.”

And:

> “Each transfer reduces a discrepancy… propagation behaves akin to physical relaxations (diffusion of heat)… a mathematical handshake where each transfer reduces a discrepancy.”

**How this relates to your current spec:**

* UMX/SLP v1 defines one flux step per tick:

  * `du = Su − Sv; flux = floor(k * du / SC); S[u] -= flux; S[v] += flux`.

* LLP adds conceptual structure:

  1. **Merge:** gather local inputs/residuals for each node.
  2. **Propagate:** calculate neighbour exchanges (flux).
  3. **Resolve:** commit the new state and residuals for next tick.

**Normative v1 tightening (safe to add to spec):**

* The SLP step per tick MUST be implementable as a **three-phase pipeline** (even if the current JS core fuses them):

  * we can document it as “conceptual phases” over the same integer update.

* The implementation MUST still be:

  * deterministic in phase order,
  * free of data races (no ambiguous read/write overlaps inside a tick).

---

## F.3 Equilibrium-Seeking & Structural Inertia

LLP spends a lot of time on how the lattice behaves over time:

> “Propagation is typically conservative and diffusive, so over time nodes exchange values until reaching equilibrium (if no further inputs)… the lattice inherently seeks a minimal residual state… every process ‘seeks minimal |R| (residual)’.”

> “Structural Inertia: LLP imbues the lattice with a form of structural inertia – it resists sudden arbitrary changes and prefers gradual transitions… each node’s state is constrained by neighbors and global invariants, the lattice cannot change in one spot without affecting others… stable global behavior, resistance to perturbations, sometimes emergent phenomena (like waves or solitons…).”

Your current UMX spec notes conservation + locality but doesn’t **call out**:

* equilibrium-seeking as an expected emergent behaviour;
* “structural inertia” as a design property.

**Suggested wording (v1 normative, but light):**

* SLP v1 MUST be:

  * **monotone residual-reducing** in the sense that, absent new inputs, repeated ticks do not increase a simple residual norm (e.g. L1 or L2 difference across neighbours).
  * **global-sum-preserving** and **locally smoothing** (diffusive-like).

No new code needed; it’s already implied by the integer diffusion rule, but making it explicit matches LLP.

---

## F.4 Continuity & “Irreducible Deltas” over Time

LLP is very explicit about **continuity in time** and the idea of storing only deltas:

> “Instead of storing full state snapshots each tick, the system keeps only the delta per step… often uses only ‘irreducible deltas’ and ‘unpredictable information per step,’ not whole re-states… enough to record the initial state and all input perturbations; LLP will faithfully reproduce intermediate states via its propagation rules.”

> “LLP operates in lockstep with Aevum Loom… At each Loom tick, every lattice node updates according to LLP rules… Frame Compression & Replay: initial state + inputs/perturbations → deterministic update rule → all states.”

Your UMX spec already has:

* P-deltas and I-blocks (TickLedger with `pBlock` and periodic `iBlock`).
* “Initial seeds applied as Gate writes; replay = initial state + write log.”

**New clarifications we can fold into the main spec:**

1. **Irreducible P-deltas:**

   * `pBlock` SHOULD only record **cells whose state actually changed** and by how much; not full fields.
   * This matches “irreducible deltas / unpredictable info per step.”

2. **Replay contract:**

   * UMX+Loom MUST guarantee:
     **(Initial state at τ₀ + ordered Gate writes + deterministic SLP) ⇒ all intermediate states τ ≥ τ₀**.
   * That’s already true; we just state it explicitly.

3. **Continuity constraint:**

   * No “teleport” operations that skip neighbour hops; any change between `τ` and `τ+1` must still be explainable as a **local SLP update + Gate writes** (no hidden global rewrites).

---

## F.5 Residual Layers, Anchor-in-Layer & No Free Lunch

LLP gives more detail on layered residual handling than the current UMX spec:

> “Base layer handles most of the state, and higher layers (NAP layers) capture finer residuals… LLP governs these residual layers with the same lattice rules… residuals… treated as another field… propagate locally… with their own coupling… residuals are not thrown away – they flow until corrected or remain steady.”

> “Layering works at scale… base layer + first residual + second residual + … = full state… ‘Layering works at scale… driving the error down ~100× to near machine precision’… anchor-in-layer convention ensures each residual value tied to a specific base node… ‘residual round-trips are guaranteed’.”

> “Reuse Constraints: no double counting or free reuse of bits… if it moves or is copied, it is accounted for (original cleared or residual tracked)… there is no ‘free lunch’ – no state can appear without cause or vanish without effect.”

**Normative v1 additions we can safely state:**

* **Residual fields as first-class citizens:**

  * Any field used as a residual layer MUST:

    * obey the same conservation law (sum over that field constant, unless explicitly coupled with a parent layer),
    * be **anchored** to base-layer positions (one-to-one or clearly defined mapping).

* **Anchor-in-layer invariant:**

  * For each residual entry, there MUST be an unambiguous target in the base or previous layer so reconstruction is well-defined.

* **No free copy invariant (reuse constraints):**

  * Gate + SLP MUST guarantee:

    * Any “copy” of information is either:

      * modeled as a **move** (subtract from source, add to dest), or
      * accompanied by an explicit **residual / error term** so the original can be reconstructed.

  * In UMX terms:

    * no “duplicate state” writes that bypass conservation; if `mode: "set"` is used to clone, the old content must be accounted for (e.g. via residual fields or an upstream Press transform).

This is more about **how higher layers and Gate should behave** than about the pure SLP kernel, but it’s strongly implied by LLP.

---

## F.6 Determinism & Hardware Independence: Order + Rounding

LLP restates determinism with some concrete implementation requirements:

> “LLP mandates fixed update ordering and uniform rounding rules so outcomes do not depend on hardware or timing quirks (no nondeterministic drift or wrap-around)… every run of the lattice yields identical results given the same initial state and inputs.”

And:

> “They established things like the need for fixed update ordering, single rounding rules, and explicit anchoring of residuals… without stating module eval order, a different execution could break determinism.”

Your UMX spec already:

* fixes edge order,
* uses pure integer arithmetic,
* claims determinism.

**Newly explicit requirements (already true in spirit but good to spell out):**

1. **Single rounding rule**:

   * For any operation that could involve division/scale (like `flux = floor(k * du / SC)`), the rounding/overflow behaviour MUST be unique and explicitly specified (e.g. “integer truncation toward zero; no saturation; 32-bit wrap is forbidden”).

2. **No wrap-around**:

   * Values MUST be kept in a safe range or prevented from overflowing Int32; wrap-around is considered a protocol violation (tests should detect it).

3. **Frozen update schedule**:

   * Implementation MUST NOT parallelize or reorder edge updates unless it can *provably* preserve the same result as the canonical single-threaded order.

---

## F.7 Fault Tolerance & “Web Re-tensioning”

LLP talks about fault behaviour quite directly:

> “Even extreme recursive processes cannot ‘run away’ because LLP’s invariants impose global balance (no unbounded amplification)… local failures or drops don\'t break consistency: if a message is lost or a node isolated, the protocol\'s handshakes ensure no double-counting or leakage (e.g. a token not acknowledged is not subtracted)… if one link fails, tension redistributes and the web remains intact.”

We already partially captured this in Complement Doc E as a NAP/Gate responsibility. From LLP, the **UMX/SLP-facing contract** is:

* UMX assumes:

  * Gate/NAP will only present **committed writes** (acknowledged, deduped).
  * A failed or lost message **never results** in a half-applied transfer (e.g. subtract without add).

* In return:

  * UMX/SLP conserves sums rigorously, so even if some writes never happen, **no internal invariant is broken**; the system just evolves with fewer perturbations.

We don’t need a new kernel feature for this; it’s mostly a clearer statement of the **boundary between SLP and NAP/Gate**.

---

## F.8 Cross-Pillar Coupling: SLP’s Constraints on TGP, Press, Loom, NAP

Most of this is already echoed in Complement Docs D & E, but LLP adds a few sharpened points:

* **Press:** LLP must deliver **highly structured, deterministic** states so Press can exceed ordinary Shannon-style compression for time-series logs.
* **TGP (Trinity Gate):** LLP must handle **multi-layer integer encodings of quantum states** (e.g. separate layers for expectation values and phases), and maintain addressing consistency so TGP knows where each component lives.
* **Loom:** LLP must support **sub-ticks / variable tick lengths** (Loom may request multiple sub-steps within one larger temporal frame). LLP must behave identically regardless of how ticks are “batched.”
* **NAP:** LLP must be **agnostic to physical distribution**; as long as numeric state arrives in order, it behaves “as if the lattice were whole.”

For the UMX/SLP spec, the key addition is:

* SLP MUST treat each tick as a pure, stateless function of:

  * previous state,
  * Gate writes for that tick,
  * static configuration.

So re-chunking ticks or running remote segments over NAP does not change the results.

---

## Gap Map F — LLP/SLP-Specific Gaps & To-Do Items

New / sharpened gaps exposed by LLP, relative to the current spec + docs A–E:

---

### F1. Explicit Merge–Propagate–Resolve Phases

* **Docs:** LLP describes a fixed “merge → propagate → resolve” handshake per tick.
* **Current spec:** tickOnce() is one black-box step; no internal phases documented.
* **Need:** Decide if we:

  * just document these phases conceptually (no API change), or
  * expose them as separate hooks in the core (for debugging, instrumentation, or alternate implementations).

---

### F2. Structural Inertia / Residual Norm Behaviour

* **Docs:** LLP claims the lattice “seeks minimal |R| (residual)” and behaves like diffusive relaxation.
* **Current spec:** no formal residual norm or inequality.
* **Need:** Either:

  * add a simple **monotonicity property** (e.g. define residual = neighbour differences, and say SLP shall not increase some norm in absence of inputs), or
  * explicitly mark equilibrium-seeking as **emergent**, not guaranteed.

---

### F3. Anchor-in-Layer Rule Formalization

* **Docs:** anchor-in-layer convention is critical to guarantee residual round-trips.
* **Current spec:** we talk about anchors and residual fields, but no formal “anchor map” schema.
* **Need:** A small **Anchor Map spec**:

  * how residual fields index back to base nodes,
  * what invariants are enforced at encode/decode time.

---

### F4. No-Free-Copy / Reuse Constraints Interface

* **Docs:** no double counting or free reuse; copies must be accounted for (clear source or track residual).
* **Current spec:** Gate has `set` and `add`, but there’s no normative rule about copying semantics.
* **Need:** Clarify at Gate/UMX boundary:

  * when `set` is allowed vs when `add`+residual is required,
  * how higher-level components (Press, TGP) must behave to respect reuse constraints.

---

### F5. Determinism Edge Cases (Overflow & Parallelism)

* **Docs:** LLP explicitly bans wrap-around and hardware-dependent rounding.
* **Current spec:** implies determinism, but doesn’t explicitly forbid overflow/parallel reorder.
* **Need:** Tighten spec language to:

  * forbid overflow or define clear saturation behaviour,
  * require that any parallel execution be provably equivalent to the canonical single-thread order.

---

### F6. Sub-tick Semantics (Loom-Driven Substeps)

* **Docs:** Loom can request multiple sub-ticks within its own frame; LLP must support that seamlessly.
* **Current spec:** tickOnce() is one tick; no notion of sub-ticks.
* **Need:** Decide if:

  * sub-ticks are just “multiple tickOnce() calls with smaller Δτ” and no extra semantics (probably easiest), and
  * write this explicitly so Loom profiles know how to do sub-stepping.

---

### Source: `umx_complement_doc_f_llp→slp_propagation_temporal_behaviour.md` (verbatim)

---

# Complement Doc F — LLP→SLP Propagation Semantics & Temporal Behaviour

This doc treats **Luminous Lattice Protocol (LLP)** as the earlier name (and slightly wider framing) of what is now **Synaptic Ley Protocol (SLP)** inside UMX. It pulls in everything LLP says about **how propagation actually behaves** and compares it to your current UMX+SLP v1 spec.

---

## F.1 LLP Scope vs SLP v1 Core

LLP defines itself as the substrate propagation layer:

> “LLP governs how accepted state changes propagate across Aether’s internal state lattice… enforcing continuity and conservation at every step… responsibilities include local propagation & global consistency, deterministic state evolution, continuity & stability.”

Your UMX/SLP v1 spec already covers:

* integer-only state,
* conservative flux per edge,
* deterministic ordering,
* per-tick tickOnce() pipeline.

**Refinement:** LLP makes explicit that SLP/LLP is responsible for the **full “shape” of propagation over time**, not just individual flux updates:

* Must be **equilibrium-seeking** (tends toward balanced states under no new input).
* Must provide enough structure for **time compression and replay** (Loom) and **space/time compression** (Press).

For v1 we can treat this as:

* **Normative:** deterministic, conservative, local, replayable.
* **Design-level goal:** equilibrium-seeking and “nice” behaviour (no runaway, diffusive-like).

---

## F.2 Propagation Handshake: Merge → Propagate → Resolve

LLP describes propagation as a **multi-phase handshake**, not just “run flux once”:

> “Every propagation step respects deterministic rules… often described as ‘every node agrees on the same handshake’… protocol defines a fixed sequence of **merge → propagate → resolve** steps that all nodes follow to minimize any residual difference.”

And:

> “Each transfer reduces a discrepancy… propagation behaves akin to physical relaxations (diffusion of heat)… a mathematical handshake where each transfer reduces a discrepancy.”

**How this relates to your current spec:**

* UMX/SLP v1 defines one flux step per tick:

  * `du = Su − Sv; flux = floor(k * du / SC); S[u] -= flux; S[v] += flux`.

* LLP adds conceptual structure:

  1. **Merge:** gather local inputs/residuals for each node.
  2. **Propagate:** calculate neighbour exchanges (flux).
  3. **Resolve:** commit the new state and residuals for next tick.

**Normative v1 tightening (safe to add to spec):**

* The SLP step per tick MUST be implementable as a **three-phase pipeline** (even if the current JS core fuses them):

  * we can document it as “conceptual phases” over the same integer update.

* The implementation MUST still be:

  * deterministic in phase order,
  * free of data races (no ambiguous read/write overlaps inside a tick).

---

## F.3 Equilibrium-Seeking & Structural Inertia

LLP spends a lot of time on how the lattice behaves over time:

> “Propagation is typically conservative and diffusive, so over time nodes exchange values until reaching equilibrium (if no further inputs)… the lattice inherently seeks a minimal residual state… every process ‘seeks minimal |R| (residual)’.”

> “Structural Inertia: LLP imbues the lattice with a form of structural inertia – it resists sudden arbitrary changes and prefers gradual transitions… each node’s state is constrained by neighbors and global invariants, the lattice cannot change in one spot without affecting others… stable global behavior, resistance to perturbations, sometimes emergent phenomena (like waves or solitons…).”

Your current UMX spec notes conservation + locality but doesn’t **call out**:

* equilibrium-seeking as an expected emergent behaviour;
* “structural inertia” as a design property.

**Suggested wording (v1 normative, but light):**

* SLP v1 MUST be:

  * **monotone residual-reducing** in the sense that, absent new inputs, repeated ticks do not increase a simple residual norm (e.g. L1 or L2 difference across neighbours).
  * **global-sum-preserving** and **locally smoothing** (diffusive-like).

No new code needed; it’s already implied by the integer diffusion rule, but making it explicit matches LLP.

---

## F.4 Continuity & “Irreducible Deltas” over Time

LLP is very explicit about **continuity in time** and the idea of storing only deltas:

> “Instead of storing full state snapshots each tick, the system keeps only the delta per step… often uses only ‘irreducible deltas’ and ‘unpredictable information per step,’ not whole re-states… enough to record the initial state and all input perturbations; LLP will faithfully reproduce intermediate states via its propagation rules.”

> “LLP operates in lockstep with Aevum Loom… At each Loom tick, every lattice node updates according to LLP rules… Frame Compression & Replay: initial state + inputs/perturbations → deterministic update rule → all states.”

Your UMX spec already has:

* P-deltas and I-blocks (TickLedger with `pBlock` and periodic `iBlock`).
* “Initial seeds applied as Gate writes; replay = initial state + write log.”

**New clarifications we can fold into the main spec:**

1. **Irreducible P-deltas:**

   * `pBlock` SHOULD only record **cells whose state actually changed** and by how much; not full fields.
   * This matches “irreducible deltas / unpredictable info per step.”

2. **Replay contract:**

   * UMX+Loom MUST guarantee:
     **(Initial state at τ₀ + ordered Gate writes + deterministic SLP) ⇒ all intermediate states τ ≥ τ₀**.
   * That’s already true; we just state it explicitly.

3. **Continuity constraint:**

   * No “teleport” operations that skip neighbour hops; any change between `τ` and `τ+1` must still be explainable as a **local SLP update + Gate writes** (no hidden global rewrites).

---

## F.5 Residual Layers, Anchor-in-Layer & No Free Lunch

LLP gives more detail on layered residual handling than the current UMX spec:

> “Base layer handles most of the state, and higher layers (NAP layers) capture finer residuals… LLP governs these residual layers with the same lattice rules… residuals… treated as another field… propagate locally… with their own coupling… residuals are not thrown away – they flow until corrected or remain steady.”

> “Layering works at scale… base layer + first residual + second residual + … = full state… ‘Layering works at scale… driving the error down ~100× to near machine precision’… anchor-in-layer convention ensures each residual value tied to a specific base node… ‘residual round-trips are guaranteed’.”

> “Reuse Constraints: no double counting or free reuse of bits… if it moves or is copied, it is accounted for (original cleared or residual tracked)… there is no ‘free lunch’ – no state can appear without cause or vanish without effect.”

**Normative v1 additions we can safely state:**

* **Residual fields as first-class citizens:**

  * Any field used as a residual layer MUST:

    * obey the same conservation law (sum over that field constant, unless explicitly coupled with a parent layer),
    * be **anchored** to base-layer positions (one-to-one or clearly defined mapping).

* **Anchor-in-layer invariant:**

  * For each residual entry, there MUST be an unambiguous target in the base or previous layer so reconstruction is well-defined.

* **No free copy invariant (reuse constraints):**

  * Gate + SLP MUST guarantee:

    * Any “copy” of information is either:

      * modeled as a **move** (subtract from source, add to dest), or
      * accompanied by an explicit **residual / error term** so the original can be reconstructed.

  * In UMX terms:

    * no “duplicate state” writes that bypass conservation; if `mode: "set"` is used to clone, the old content must be accounted for (e.g. via residual fields or an upstream Press transform).

This is more about **how higher layers and Gate should behave** than about the pure SLP kernel, but it’s strongly implied by LLP.

---

## F.6 Determinism & Hardware Independence: Order + Rounding

LLP restates determinism with some concrete implementation requirements:

> “LLP mandates fixed update ordering and uniform rounding rules so outcomes do not depend on hardware or timing quirks (no nondeterministic drift or wrap-around)… every run of the lattice yields identical results given the same initial state and inputs.”

And:

> “They established things like the need for fixed update ordering, single rounding rules, and explicit anchoring of residuals… without stating module eval order, a different execution could break determinism.”

Your UMX spec already:

* fixes edge order,
* uses pure integer arithmetic,
* claims determinism.

**Newly explicit requirements (already true in spirit but good to spell out):**

1. **Single rounding rule**:

   * For any operation that could involve division/scale (like `flux = floor(k * du / SC)`), the rounding/overflow behaviour MUST be unique and explicitly specified (e.g. “integer truncation toward zero; no saturation; 32-bit wrap is forbidden”).

2. **No wrap-around**:

   * Values MUST be kept in a safe range or prevented from overflowing Int32; wrap-around is considered a protocol violation (tests should detect it).

3. **Frozen update schedule**:

   * Implementation MUST NOT parallelize or reorder edge updates unless it can *provably* preserve the same result as the canonical single-threaded order.

---

## F.7 Fault Tolerance & “Web Re-tensioning”

LLP talks about fault behaviour quite directly:

> “Even extreme recursive processes cannot ‘run away’ because LLP’s invariants impose global balance (no unbounded amplification)… local failures or drops don’t break consistency: if a message is lost or a node isolated, the protocol’s handshakes ensure no double-counting or leakage (e.g. a token not acknowledged is not subtracted)… if one link fails, tension redistributes and the web remains intact.”

We already partially captured this in Complement Doc E as a NAP/Gate responsibility. From LLP, the **UMX/SLP-facing contract** is:

* UMX assumes:

  * Gate/NAP will only present **committed writes** (acknowledged, deduped).
  * A failed or lost message **never results** in a half-applied transfer (e.g. subtract without add).

* In return:

  * UMX/SLP conserves sums rigorously, so even if some writes never happen, **no internal invariant is broken**; the system just evolves with fewer perturbations.

We don’t need a new kernel feature for this; it’s mostly a clearer statement of the **boundary between SLP and NAP/Gate**.

---

## F.8 Cross-Pillar Coupling: SLP’s Constraints on TGP, Press, Loom, NAP

Most of this is already echoed in Complement Docs D & E, but LLP adds a few sharpened points:

* **Press:** LLP must deliver **highly structured, deterministic** states so Press can exceed ordinary Shannon-style compression for time-series logs.
* **TGP (Trinity Gate):** LLP must handle **multi-layer integer encodings of quantum states** (e.g. separate layers for expectation values and phases), and maintain addressing consistency so TGP knows where each component lives.
* **Loom:** LLP must support **sub-ticks / variable tick lengths** (Loom may request multiple sub-steps within one larger temporal frame). LLP must behave identically regardless of how ticks are “batched.”
* **NAP:** LLP must be **agnostic to physical distribution**; as long as numeric state arrives in order, it behaves “as if the lattice were whole.”

For the UMX/SLP spec, the key addition is:

* SLP MUST treat each tick as a pure, stateless function of:

  * previous state,
  * Gate writes for that tick,
  * static configuration.

So re-chunking ticks or running remote segments over NAP does not change the results.

---

## Gap Map F — LLP/SLP-Specific Gaps & To-Do Items

New / sharpened gaps exposed by LLP, relative to the current spec + docs A–E:

---

### F1. Explicit Merge–Propagate–Resolve Phases

* **Docs:** LLP describes a fixed “merge → propagate → resolve” handshake per tick.
* **Current spec:** tickOnce() is one black-box step; no internal phases documented.
* **Need:** Decide if we:

  * just document these phases conceptually (no API change), or
  * expose them as separate hooks in the core (for debugging, instrumentation, or alternate implementations).

---

### F2. Structural Inertia / Residual Norm Behaviour

* **Docs:** LLP claims the lattice “seeks minimal |R| (residual)” and behaves like diffusive relaxation.
* **Current spec:** no formal residual norm or inequality.
* **Need:** Either:

  * add a simple **monotonicity property** (e.g. define residual = neighbour differences, and say SLP shall not increase some norm in absence of inputs), or
  * explicitly mark equilibrium-seeking as **emergent**, not guaranteed.

---

### F3. Anchor-in-Layer Rule Formalization

* **Docs:** anchor-in-layer convention is critical to guarantee residual round-trips.
* **Current spec:** we talk about anchors and residual fields, but no formal “anchor map” schema.
* **Need:** A small **Anchor Map spec**:

  * how residual fields index back to base nodes,
  * what invariants are enforced at encode/decode time.

---

### F4. No-Free-Copy / Reuse Constraints Interface

* **Docs:** no double counting or free reuse; copies must be accounted for (clear source or track residual).
* **Current spec:** Gate has `set` and `add`, but there’s no normative rule about copying semantics.
* **Need:** Clarify at Gate/UMX boundary:

  * when `set` is allowed vs when `add`+residual is required,
  * how higher-level components (Press, TGP) must behave to respect reuse constraints.

---

### F5. Determinism Edge Cases (Overflow & Parallelism)

* **Docs:** LLP explicitly bans wrap-around and hardware-dependent rounding.
* **Current spec:** implies determinism, but doesn’t explicitly forbid overflow/parallel reorder.
* **Need:** Tighten spec language to:

  * forbid overflow or define clear saturation behaviour,
  * require that any parallel execution be provably equivalent to the canonical single-thread order.

---

### F6. Sub-tick Semantics (Loom-Driven Substeps)

* **Docs:** Loom can request multiple sub-ticks within its own frame; LLP must support that seamlessly.
* **Current spec:** tickOnce() is one tick; no notion of sub-ticks.
* **Need:** Decide if:

  * sub-ticks are just “multiple tickOnce() calls with smaller Δτ” and no extra semantics (probably easiest), and
  * write this explicitly so Loom profiles know how to do sub-stepping.

---

### Source: `umx_complement_doc_i_gap_closure_profile_specs.md` (verbatim)

---

# Complement Doc I — Gap Closure & Profile Specs (UMX + SLP + NAP v1.x)

This doc sweeps all the **explicit gap maps** and "missing pieces" from:

- **Universal Matrix Pillar Spec v1** (UMX core)
- **Complement Docs A–D (+ A1)** — Node/anchors/topology/SLP design-level
- **Complement Doc F** — LLP → SLP temporal behaviour
- **Complement Doc G** — NAP integration
- **Complement Doc H** — Legacy NAP / nesting / stress-test reports

and rolls them into a single **gap-closure plan** for the Matrix stack.

For each gap family we clarify:

- **Summary** — what’s missing / underspecified.
- **Normative v1 target** — what MUST be true for UMX+SLP+NAP v1.x.
- **Spec artefacts** — concrete docs/tables/schemas to write.
- **Implementation sketch** — how it likely lands in Matrix JS / Gate / NAP.
- **Phase** —
  - **P1** = needed for Matrix JS + Gate to feel “complete enough”.
  - **P2** = post-Matrix hardening / ergonomics.
  - **P3** = researchy / longer-horizon.

---

## I.1 Gap Family Index (by source)

From **Complement Docs A–D (+A1)**:

1. **I-1 — MDL / Description-Length Objective (Topology & SLP)**  
2. **I-2 — SLP APIs & Data Structures**  
3. **I-3 — Multi-Layer UMX**  
4. **I-4 — UMX Node Manifest & Actor Slots**  
5. **I-5 — NAP Bus Backpressure & Flow-Control Hooks**  
6. **I-6 — Loom/Press Interop (beyond hash + P-deltas)**  
7. **I-7 — Global Parameter Calibration & Profiles**  

From **Complement Doc F (LLP→SLP)**:

8. **I-8 — Merge → Propagate → Resolve Phasing**  
9. **I-9 — Structural Inertia & Residual Norm Behaviour**  
10. **I-10 — Anchor-in-Layer Rule Formalisation**  
11. **I-11 — No-Free-Copy / Reuse-Constraints Interface**  
12. **I-12 — Determinism Edge Cases (Overflow & Parallelism)**  
13. **I-13 — Sub-Tick Semantics (Loom-Driven Substeps)**  

From **Complement Doc G (NAP Integration)**:

14. **I-14 — Concrete JS NAP API (Beyond nap.js Envelope)**  
15. **I-15 — Reversibility Window Parameters**  
16. **I-16 — Mapping Between NAP’s c and UMX’s c**  
17. **I-17 — MDL Consensus ↔ UMX MDL (Unification)**  
18. **I-18 — Commit Manifest Schema & SEAL Semantics**  
19. **I-19 — U-Ledger Storage & Universal Integer Indexing**  
20. **I-20 — Quotas & Budget-Drift Policies**  
21. **I-21 — Two-Phase Tick Hooks for UMX**  

From **Complement Doc H (Legacy NAP / Nesting / Stress)**:

22. **I-22 — Summary Packet Schema for Stacked Sims**  
23. **I-23 — ε-Layer Profile & Scaling Factor R**  
24. **I-24 — Over-Coupling Detection & Resonance Guards**  
25. **I-25 — Integer vs Float Budget Discipline (Cross-Pillar)**  
26. **I-26 — Relational NAP Profile (Cadence & Permissions)**  
27. **I-27 — Nesting Profile & Tick Ratios**  

---

## I.2 Gap Families (Details)

Below, one section per gap family.

---

### I-1 — MDL / Description-Length Objective (Topology & SLP)

**Summary**  
Docs say both UMX and SLP choose anchors and edges to minimise description length (MDL), with penalties for distance, degree, movement, etc. The shape of the objective is described, but **no canonical coding scheme or parameter set** is frozen.

**Normative v1 target**  
For v1.x we want a **minimal, explicit MDL core**:

- A documented scalar objective **L_total** over:
  - per-node anchor choices, and
  - optional candidate edges.
- Clear terms:
  - coding cost for node/edge parameters (bit-length proxy is fine),
  - L1 distance penalty over PFNA anchors,
  - movement penalty for re-anchoring,
  - degree penalty per node.
- A deterministic greedy update rule:
  - evaluate candidate changes in a fixed hashed order,
  - accept any with ΔL_total < 0.

**Spec artefacts**

- `spec/md/mdl_objective_v1.md`  
  - Defines L_total, terms, and update rule.  
- `spec/md/mdl_parameters_v1.md`  
  - Recommended λ, μ, γ, δ and hysteresis margins for dev usage.

**Implementation sketch**

- Start as a **pure analysis tool**:
  - separate MDL evaluator over a frozen UMX snapshot.
- Later, wire slowly into SLP plasticity passes once parameters feel sane.

**Phase**: **P3** (conceptually important, but not required for Matrix JS static-core demo).

---

### I-2 — SLP APIs & Data Structures

**Summary**  
Docs name SLP_GROW, SLP_POTENTIATE, SLP_PRUNE, SLP_CONDUCT, etc., with behaviour sketched in English, but there is **no public JS/TS API** for plasticity, no standard data structures for usage counters, and no numeric thresholds.

**Normative v1 target**  
Expose a clear **SLP v1 structural API**, even if most of it is stubbed initially:

- Canonical TS interfaces for:
  - edge weights, usage counters, candidate queues, MDL scores.
- Public methods on a “SLP manager” object:
  - `growEdges()`, `pruneEdges()`, `updateUsage()`, `runPlasticityPass()`.
- A documented **evaluation cadence** (e.g. every N ticks).

**Spec artefacts**

- `spec/md/slp_api_v1.md` (English + TS-ish signatures).
- `spec/md/slp_thresholds_v1.md` (θ_plus, θ_minus, M, β etc., even if just recommended ranges).

**Implementation sketch**

- Implement SLP as an **overlay**:
  - store adjacency/weights in a side structure that can rebuild the UMX edge list.
- First implementation can be conservative: only prune/grow between ticks, only re-run edges occasionally.

**Phase**: **P2** (not required to run Matrix JS, but needed for “self-shaping” demos).

---

### I-3 — Multi-Layer UMX

**Summary**  
PFNA allows layers ℓ; routing depends on Δℓ; NAP talks about stack_delta. Current JS core effectively runs a **single layer**, and there is no clear rule-set for multi-layer connectivity.

**Normative v1 target**  
Define a minimal **multi-layer policy**, even if v1 deployments stay single-layer:

- Explicit meaning of `layerId` in UMXConfig and fields.
- Allowed layer-to-layer connections: e.g. ℓ only connects to ℓ and ℓ±1.
- Clear note that v1 reference profile uses a **single UMX layer** (ℓ=0) but the spec anticipates more.

**Spec artefacts**

- `spec/md/umx_layers_policy_v1.md`  
  - includes a table: layer pairs, allowed edges, Δℓ penalties.

**Implementation sketch**

- Adjust edge builder to include `(layer, addrKey)` pairs if/when multi-layer is activated.
- Keep the default Matrix JS config single-layer for now, with multi-layer behind a flag.

**Phase**: **P2**.

---

### I-4 — UMX Node Manifest & Actor Slots

**Summary**  
Docs treat each cell as projecting a Trinity stack; talk about “actor slots” and per-node metadata, but there is no **formal manifest schema** for what lives at a node beyond integer fields.

**Normative v1 target**  
Define a **UMX Node Manifest** with the minimal fields needed by Gate/NAP/Codex:

- `id`, `anchor`, `layer`, `gridIndex`.
- `fieldOffsets` / `fieldCount`.
- optional `policyFlags` (e.g. frozen, boundary, membrane type).
- optional `tags` for Codex / UI.

**Spec artefacts**

- `spec/md/umx_node_manifest_v1.md` (schema + examples).

**Implementation sketch**

- Represent manifest as a **parallel array-of-structs** to the integer fields.
- Start with static manifests generated at init; add mutation later as SLP grows/prunes nodes.

**Phase**: **P2**.

---

### I-5 — NAP Bus Backpressure & Flow-Control Hooks

**Summary**  
Docs say NAP does backpressure and partitioning; Matrix JS currently has **no explicit backpressure handshake** between NAP and UMX.

**Normative v1 target**  
Define how NAP can signal UMX/Gate when the bus is overloaded:

- Limit per-tick outgoing envelopes per node.
- If NAP drops/defer messages, it reports this via a clear status.
- UMX/Gate react by throttling Gate writes or pausing non-critical flows.

**Spec artefacts**

- `spec/md/nap_flow_control_v1.md` (semantics + state machine diagrams).

**Implementation sketch**

- Extend nap.js with:
  - queue-size checks and drop/defer decisions,
  - a simple `NapStatus` object the Gate can poll each tick.
- Gate passes this status into any high-volume emitters.

**Phase**: **P2** (Matrix JS can run without it, but real systems want it).

---

### I-6 — Loom/Press Interop (Beyond Hash + P-deltas)

**Summary**  
UMX exposes TickLedger (rootHash, pBlock, iBlock). Loom & Press need a **canonical schema** for:

- what exactly gets hashed,
- how P-deltas and I-blocks are packaged,
- which minimal data Press can compress.

**Normative v1 target**  
Lock in a **TickRecord v1** schema:

- envelope-level metadata (tau, config hash, etc.),
- UMX TickLedger body (exact shape),
- optional Press summary (compressed variant),
- Loom hash-chain arrangement.

**Spec artefacts**

- `spec/md/umx_loom_press_interop_v1.md`  
- `spec/json/tick_record_v1.schema.json`

**Implementation sketch**

- Have Gate wrap each TickLedger into TickRecord; Loom/Press only ever see that.
- Press’s early implementations can simply re-encode P-deltas and drop I-block details if needed.

**Phase**: **P1** (needed to have a clean story for logs, replay and the NAP payloads you’re already emitting).

---

### I-7 — Global Parameter Calibration & Profiles

**Summary**  
Many knobs: r, c, D★, SC, k, MDL weights, SLP thresholds, NAP quotas, etc. Docs mention them but there is **no set of named parameter profiles** a dev can just pick.

**Normative v1 target**  
Ship a small set of named profiles, e.g.:

- `dev_low_res` — small grid, forgiving parameters.
- `matrix_demo_default` — your current 64×64 S1-style config.
- `nested_sim_dense` — tuned for deeper stacks / higher fan-out.

Each profile pins **every relevant parameter** to a concrete value.

**Spec artefacts**

- `spec/md/profiles_overview_v1.md`  
- `spec/json/profile_matrix_demo_default.json` etc.

**Implementation sketch**

- Provide a helper in JS: `createUMX(configProfileId: string)`.
- Profiles also reference NAP and Loom/Press settings, not just UMX core.

**Phase**: **P1** (ergonomics + repeatability).

---

### I-8 — Merge → Propagate → Resolve Phasing (SLP)

**Summary**  
LLP/SLP docs describe each tick as a **three-phase handshake**: merge, propagate, resolve. Current JS exposes just a monolithic `tickOnce()` / `stepIntegerFlux()`.

**Normative v1 target**  
Clarify and, if possible, optionally expose phase boundaries:

- Conceptually: define what belongs to **Merge** (apply writes / gather residuals), **Propagate** (flux step), **Resolve** (commit new state & residuals).
- Implementation: either keep phases internal, or optionally surface them via debug hooks.

**Spec artefacts**

- `spec/md/slp_phases_v1.md` (conceptual + optional API like `tickMerge`, `tickPropagate`, `tickResolve`).

**Implementation sketch**

- Internally reframe `tickOnce()` to call three internal functions.
- Add debug/instrumentation mode that can record snapshots at each phase for tests.

**Phase**: **P2** (conceptually important; not essential for current engine behaviour).

---

### I-9 — Structural Inertia & Residual Norm Behaviour

**Summary**  
Docs say the lattice “seeks minimal |R|” and behaves diffusive; but **no explicit inequality** is given for how a residual norm behaves over time.

**Normative v1 target**  
Define a simple **reference norm and monotonicity property**:

- For the base field, define residual norm e.g.:
  - `R(τ) = Σ_edges |S[u] - S[v]|` or similar.
- In absence of new Gate writes, SLP should **not systematically increase** R over long runs for standard profiles.
- Mark clearly where this is **design goal vs hard invariant**.

**Spec artefacts**

- `spec/md/slp_residual_behaviour_v1.md` (residual definition, expected behaviour, test ideas).

**Implementation sketch**

- Add test scenarios that measure R(τ) over time from random seeds.
- Use results to tune k / SC defaults and detect broken cases.

**Phase**: **P3** (behavioural QA, not core correctness).

---

### I-10 — Anchor-in-Layer Rule Formalisation

**Summary**  
Residual layers must be anchored to base-layer nodes so reconstruction is well-defined. Current spec mentions anchors conceptually but no **formal anchor map schema** is given for residual layers.

**Normative v1 target**  
Define an **Anchor Map**:

- For each residual entry: a deterministic pointer to its base anchor.
- Rules for one-to-one vs many-to-one mapping across layers.
- Guarantee that reconstruction is unambiguous given base + residuals.

**Spec artefacts**

- `spec/md/anchor_map_v1.md` (text)  
- `spec/json/anchor_map_v1.schema.json`

**Implementation sketch**

- Represent Anchor Map as either:
  - direct indexing (residual grid aligned 1:1 with base), or
  - a small lookup table when residual resolutions differ.
- Keep v1 simple: 1:1 mapping for same-size grids.

**Phase**: **P1** if residual layers are used; **P2** otherwise.

---

### I-11 — No-Free-Copy / Reuse-Constraints Interface

**Summary**  
Docs assert strict “no free lunch” rules: copies must be accounted for as moves or residuals. Gate supports `set` vs `add` modes, but there is no **normative rule** for when `set` is allowed.

**Normative v1 target**  
Define a **reuse discipline**:

- `mode: "add"` is the default for budget-respecting updates.
- `mode: "set"` only allowed in:
  - initialisation / seeding phases, or
  - explicit structural events where the old content is captured as residual or logged as destroyed/created.

**Spec artefacts**

- `spec/md/reuse_constraints_v1.md` (rules + examples).

**Implementation sketch**

- Gate enforces a simple policy:
  - warns or rejects `set` writes outside allowed windows unless an attached reason code is present.

**Phase**: **P1** for conceptual cleanliness; implementation can start permissive and tighten.

---

### I-12 — Determinism Edge Cases (Overflow & Parallelism)

**Summary**  
Docs forbid wrap-around and hardware-dependent rounding. The spec says “integer-only and deterministic” but does not **explicitly ban overflow** or define allowed parallelisation.

**Normative v1 target**  
Lock down arithmetic semantics:

- State fields must stay within a documented safe integer range.
- Overflow is either **forbidden** (tests assert it never happens) or a **defined failure mode** (hard crash / protocol break).
- Parallelisation, if used, must reproduce the canonical single-threaded edge order result exactly.

**Spec artefacts**

- `spec/md/determinism_constraints_v1.md`.

**Implementation sketch**

- For JS/TS, rely on Int32Array semantics and add range-checking in debug builds.
- For future native implementations, require 64-bit internal accumulators or formal proofs of non-overflow for chosen ranges.

**Phase**: **P1** (core correctness + replayability).

---

### I-13 — Sub-Tick Semantics (Loom-Driven Substeps)

**Summary**  
Loom/NAP can request “sub-ticks” inside a larger frame; docs say LLP must behave identically regardless of how ticks are batched. Current spec doesn’t mention sub-ticks.

**Normative v1 target**  
Clarify that **sub-ticks are just multiple calls to tickOnce()** with appropriately scaled Gate inputs:

- Define how input timestamps map to sub-ticks.
- Guarantee that splitting a tick into M sub-ticks with scaled inputs is equivalent to one macro-tick.

**Spec artefacts**

- `spec/md/subtick_semantics_v1.md`.

**Implementation sketch**

- Provide Loom with a helper: given a desired physical time step, compute how many logical sub-ticks are needed and how to distribute Gate writes.

**Phase**: **P2**.

---

### I-14 — Concrete JS NAP API (Beyond nap.js Envelope)

**Summary**  
We have nap.js for envelope canonicalisation, but no **typed JS/TS API** for message families (HELLO/BIND/SYNC/CAST/BRIDGE/SEAL/ECHO) or ports M.in/M.out/M.audit.

**Normative v1 target**  
Expose a small, usable **NAP client API** for Gate and other pillars:

- TS interfaces for `NapEnvelope`, `NapPort`, `NapMessage`, etc.
- Functions:
  - `napSendSync`, `napSendCast`, `napBridge`, `napSeal`, `napEcho`.
- Clear semantics for how these call into the lower transport.

**Spec artefacts**

- `spec/md/nap_js_api_v1.md`  
- `spec/ts/nap_api_v1.d.ts`

**Implementation sketch**

- Wrap nap.js canonicalisation in higher-level helpers that construct well-typed envelopes and manage nonces.

**Phase**: **P1** for a clean Gate + Matrix JS story.

---

### I-15 — Reversibility Window Parameters

**Summary**  
Docs define a reversibility window (in ticks) after which unacknowledged messages are rolled back. No default value or interface is specified.

**Normative v1 target**  
Define a **default window profile** and how to configure it:

- e.g. `windowTicks = 8` for local demos.
- Accessors:
  - `getReversibilityWindow()`, `setReversibilityWindow()`.
- Observability: stats on how often rollbacks occur.

**Spec artefacts**

- `spec/md/nap_reversibility_window_v1.md`.

**Implementation sketch**

- NAP keeps a small per-message state; if no SEAL/ACK by `τ + windowTicks`, it cancels intent and emits an audit event.

**Phase**: **P2** (important for robustness; not needed for single-process demos).

---

### I-16 — Mapping Between NAP’s c and UMX’s c

**Summary**  
NAP has a network-level causal barrier c; UMX has lattice hop bound c. There is no explicit alignment rule.

**Normative v1 target**  
Define **Causality Alignment rules**:

- For single-cluster Matrix JS:
  - `c_NAP = c_UMX = 1` recommended.
- For multi-scale deployments:
  - `c_NAP ≥ c_UMX` must hold; suggestions on multi-hop network paths.

**Spec artefacts**

- `spec/md/causality_alignment_v1.md`.

**Implementation sketch**

- Encode this as simple config assertions at startup: reject configs with incompatible c values.

**Phase**: **P1** (guards against subtle “arrive too early” bugs later).

---

### I-17 — MDL Consensus ↔ UMX MDL (Unification)

**Summary**  
NAP uses MDL to pick which incoming messages to trust; UMX/SLP uses MDL for topology learning. It’s unclear whether they share one objective or use separate ones.

**Normative v1 target**  
Clarify relationship between MDL layers:

- Either: define a **shared ℒ** with shared weights.
- Or: state explicitly that:
  - NAP’s MDL is **transport-level consensus** with its own weights,
  - UMX’s MDL is **structural learning** with a different objective.

**Spec artefacts**

- `spec/md/mdl_unification_note_v1.md`.

**Implementation sketch**

- For v1, likely simplest to keep them logically separate but conceptually consistent, and only unify if a strong need appears.

**Phase**: **P3**.

---

### I-18 — Commit Manifest Schema & SEAL Semantics

**Summary**  
Docs say every multi-step interaction ends in a SEAL message with a manifest; participants sign it before committing. There is **no JSON/binary schema** for that manifest.

**Normative v1 target**  
Define a **Commit Manifest v1**:

- Fields:
  - `tick`, `participants`, `hashList`, `budgetBefore`, `budgetAfter`, `timestamp`, `nonce`, `signatures[]`.
- SEAL semantics:
  - Manifest only considered committed when all participants provide valid signatures.

**Spec artefacts**

- `spec/md/commit_manifest_v1.md`  
- `spec/json/commit_manifest_v1.schema.json`

**Implementation sketch**

- Gate produces manifests for any multi-node operation that affects UMX.
- NAP carries SEAL messages wrapping these manifests; U-Ledger logs them as atomic events.

**Phase**: **P1** for any serious multi-node scenario; **P2** for single-node demos.

---

### I-19 — U-Ledger Storage & Universal Integer Indexing

**Summary**  
Docs define per-node U-Ledgers and a global Universal Integer stream U, but there is **no storage/index spec**.

**Normative v1 target**  
Define a minimal **U-Ledger record** and indexing strategy:

- Record fields:
  - `tick`, `nodeId`, `eventType`, `envelopeRef`, `rootHash`, `budgets`, `manifestRef`.
- Global U stream:
  - a concatenation of hash-chained U-Ledger entries.

**Spec artefacts**

- `spec/md/u_ledger_format_v1.md`  
- `spec/json/u_ledger_record_v1.schema.json`

**Implementation sketch**

- For Matrix JS, U-Ledger can simply be a JSONL file or in-memory array.
- Index by `(nodeId, tick)` and by `rootHash` for replay lookups.

**Phase**: **P1** if you want audit/replay; otherwise **P2**.

---

### I-20 — Quotas & Budget-Drift Policies

**Summary**  
NAP enforces quotas and checks μ drift; specs don’t give concrete thresholds or required reactions.

**Normative v1 target**  
Define **Budget Profiles**:

- Per-node quota:
  - max messages per tick,
  - max payload bytes per tick,
  - max μ change per tick.
- Drift tolerance τ:
  - allowed deviation between global μ sum and expected.
- Reactions:
  - log-only, graceful degradation, or hard fail.

**Spec artefacts**

- `spec/md/budget_profiles_v1.md`.

**Implementation sketch**

- Implement simple counters per node per tick.
- If quotas exceeded, NAP logs a warning and may drop lower-priority messages.

**Phase**: **P2**.

---

### I-21 — Two-Phase Tick Hooks for UMX

**Summary**  
NAP uses a two-phase tick (compute → sync). UMX currently exposes only `tickOnce()`.

**Normative v1 target**  
Define an explicit **tick barrier contract**:

- Phase 1 (compute): Gate/engine calls `umx.tickOnce()`.
- Phase 2 (sync): NAP handles message exchange, SEAL, and only then increments global τ.

**Spec artefacts**

- `spec/md/tick_phase_contract_v1.md`.

**Implementation sketch**

- In single-node Matrix JS, Phase 2 can be a no-op stub, but the structure is still present in the engine loop.

**Phase**: **P1** (even if Phase 2 is trivial at first).

---

### I-22 — Summary Packet Schema for Stacked Sims

**Summary**  
Legacy nesting reports define Village/Town/City summary vectors (counts, means, variances, production, synergy scores, event counts). There is no canonical **Summary Packet v1** schema in the main spec.

**Normative v1 target**  
Define a **Summary Packet v1** for cross-stack coupling:

- Core fields (all integer / rational encodings):
  - `N` (count),
  - means/variances of a small set of key fields,
  - aggregated production vectors over a tick window,
  - synergy/interaction scores,
  - event counts.
- Explicit tick window semantics: how many logical ticks each packet covers.

**Spec artefacts**

- `spec/md/summary_packet_v1.md`  
- `spec/json/summary_packet_v1.schema.json`

**Implementation sketch**

- Build helper functions to summarise blocks of UMX state into summary packets.
- Outer stacks consume packets instead of raw cell data.

**Phase**: **P2**.

---

### I-23 — ε-Layer Profile & Scaling Factor R

**Summary**  
Sub-Planck stacking uses integer residuals scaled by R, but v1 spec doesn’t pin R values or maximum residual depth.

**Normative v1 target**  
Define **ε-layer profiles**:

- Per profile:
  - scaling factor R (e.g. 10³, 10⁶),
  - max depth of residual stacks,
  - policies for when residuals must be folded back down.

**Spec artefacts**

- `spec/md/epsilon_layer_profiles_v1.md`.

**Implementation sketch**

- For Matrix JS, start with a single ε profile and at most one extra residual layer.
- Expose conversion helpers between base layer values and ε residuals.

**Phase**: **P2**.

---

### I-24 — Over-Coupling Detection & Resonance Guards

**Summary**  
Stress tests show over-dense NAP coupling can create resonance loops and low-amplitude oscillations. No formal health-check exists.

**Normative v1 target**  
Add **over-coupling heuristics and diagnostics**:

- Max NAP degree/fan-out per node per layer.
- Health checks that watch μ variance or energy spectra over time.
- Warnings when over-coupling patterns are detected.

**Spec artefacts**

- `spec/md/overcoupling_diagnostics_v1.md`.

**Implementation sketch**

- Implement simple counters and rolling statistics.
- Dev-console panes can visualise oscillation patterns.

**Phase**: **P3** (observability / tuning).

---

### I-25 — Integer vs Float Budget Discipline (Cross-Pillar)

**Summary**  
Legacy float prototypes suffered precision-floor drift. UMX is now integer-only, but there is no explicit **cross-pillar ban** on floats for authoritative budgets.

**Normative v1 target**  
State clearly:

> All budget / μ-like quantities shared across pillars (UMX/NAP/Loom/Press/TGP) MUST be represented as integers or exact rational encodings. Floats may be used for approximations but never as the authoritative source of truth.

**Spec artefacts**

- `spec/md/integer_budget_discipline_v1.md`.

**Implementation sketch**

- Make config schemas reject float-typed budget fields.
- Where floats are unavoidable (e.g. UI charts), always derive them from integer sources.

**Phase**: **P1**.

---

### I-26 — Relational NAP Profile (Cadence & Permissions)

**Summary**  
Relational PoC uses summary exchange every N ticks, with read-only monitors. There is no spec’d **Relational Profile** for NAP.

**Normative v1 target**  
Define a **Relational NAP Profile**:

- Fixed cadences (e.g. every 5 ticks) for summary messages.
- Allowed payload shapes (means, variances, counts, norms only).
- Permission model:
  - default: relational nodes are read-only,
  - opt-in: they may propose writes via SEAL.

**Spec artefacts**

- `spec/md/relational_nap_profile_v1.md`.

**Implementation sketch**

- Provide a default relational-monitor component in Gate that subscribes to Summary Packets and renders dashboards.

**Phase**: **P2**.

---

### I-27 — Nesting Profile & Tick Ratios

**Summary**  
Nesting reports refer to inner/outer tick ratios (k_VT, k_TC) but there is no canonical **Nesting Profile** describing allowed ratios and alignment rules.

**Normative v1 target**  
Define **Nesting Profiles**:

- Allowed tick ratios (e.g. inner = 4× outer, 8× outer).
- When inner stacks may “run ahead” vs must stay locked.
- How NAP enforces alignment (e.g. only send summary packets on outer ticks).

**Spec artefacts**

- `spec/md/nesting_profiles_v1.md`.

**Implementation sketch**

- Implement a small scheduler that runs inner tick loops and issues summary packets to outer stacks according to the profile.

**Phase**: **P2**.

---

## I.3 P1 Closure Plan (Matrix JS-Oriented)

Here’s a suggested **first closure slice** that gives you a solid, end-to-end Matrix JS story without biting off all 27 gaps at once.

**Priority P1 items to draft and wire first**

1. **Integer Budget Discipline**  
   - (I-12, I-25) — lock in integer ranges and explicitly ban float budgets.
2. **Tick-Phase Contract**  
   - (I-8, I-21, I-13) — document Merge/Propagate/Resolve conceptually and define the NAP two-phase tick barrier.
3. **NAP JS API + Commit/U-Ledger Basics**  
   - (I-14, I-18, I-19) — TS-level NAP helpers, Commit Manifest v1, and a simple U-Ledger record format.
4. **Loom/Press Interop & TickRecord v1**  
   - (I-6) — agree on the canonical TickRecord that Gate/Press/Loom will use.
5. **Global Profiles**  
   - (I-7, plus ε/relational/nesting later) — at least one `matrix_demo_default` profile with concrete values.
6. **Reuse Constraints & Anchor Map (if residual layers are used)**  
   - (I-10, I-11) — light but explicit rules so nothing “teleports” or duplicates silently.
7. **Causality Alignment**  
   - (I-16) — simple assertions tying NAP.c and UMX.c for the demo setups.

Once those are in place, Matrix JS has a:

- crisp integer-core story,
- deterministic tick loop with a NAP-compatible outer shell,
- replay/audit path (TickRecord + U-Ledger),
- and at least one named profile you can point devs at (
  “run this and you’re in canon territory”).

Everything else (MDL details, plasticity, nesting, over-coupling diagnostics) can then iterate as **P2/P3 annexes** without destabilising the working demo.

---

### Source: `stress_emergence/umx_epsilon_layers_and_drift_metrics_v1.md` (verbatim)

---
id: umx_epsilon_layers_and_drift_metrics_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Epsilon Layers & Drift Metrics v1

Defines epsilon-layer representation, residual norms, per-node drift Δ_i(W) and global Δ(W), and how these appear in `residual_epsilon.tsv` and `drift_metrics.tsv`.

## Part 5 — Stress, Emergence Bands, Budgets, Kill-Switch & Safety

### Source: `stress_emergence/umx_drift_and_budget_coupling_v1.md` (verbatim)

---
id: umx_drift_and_budget_coupling_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Drift & Budget Coupling v1

Defines how drift guards and NAP budgets interact; how budget usage and drift are recorded in the ledger.

### Source: `stress_emergence/umx_emergence_bands_v1.md` (verbatim)

---
id: umx_emergence_bands_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Emergence Bands v1

PASS / INVESTIGATE / FAIL numeric bands from drift metrics and the quarantine flag semantics used by the testbed.

### Source: `stress_emergence/umx_kill_switch_and_quarantine_v1.md` (verbatim)

---
id: umx_kill_switch_and_quarantine_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Kill-Switch & Quarantine v1

Kill-switch scopes (NODE/REGION/SYSTEM), effects, logging, and quarantine semantics for scenarios/regions.

### Source: `stress_emergence/umx_paper_runtime_equivalence_v1.md` (verbatim)

---
id: umx_paper_runtime_equivalence_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Paper–Runtime Equivalence v1

The paper testbed is the behavioural spec; runtime must match outputs up to explicit epsilon corrections.

### Source: `stress_emergence/umx_stress_test_matrix_v1.md` (verbatim)

---
id: umx_stress_test_matrix_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Stress Test Matrix v1

Stress scenario families (routing, backpressure, dead-letter, isolation) and required metrics to evaluate them.

## Part 6 — NAP Integration, Trinity Gate, Bus Contracts and Ledgers

### Source: `umx_complement_doc_g_nap_integration.md` (verbatim)

---

# Complement Doc G — Nexus Aeternus Protocol (NAP) & Full Matrix Integration

This doc pulls everything relevant from **“Nexus Aeternus Protocol (NAP) – Intersystem Synchrony & Audit Layer (Internal Technical Report)”** and pins it against the existing **UMX + SLP + Gate** spec.

Where useful I’ll distinguish:

- **v1 normative** — what UMX **must** rely on from NAP right now.
- **v2 / design-level** — things that are clearly specified, but not yet wired into the JS core or UMX spec.

---

## G.1 NAP Scope & Responsibilities (What It Actually Does)

NAP defines itself as the **meta-communication layer**:

> “NAP is the umbrella protocol for all inter-node and inter-layer communication in the Trinity architecture. Its core responsibilities include maintaining global synchrony (a universal tick alignment with no drift), enforcing reliable delivery semantics… and providing idempotence via cryptographic nonces and content-addressing… It… upholds full auditability by logging every structural change in an append-only ledger (the ‘U-Ledger’).”【python†L1-L8】

And at the high-level:

> “NAP ensures temporal continuity, energetic balance, topological neutrality, and reproducibility across all simulations – e.g. no time drift between layers, no runaway feedback, independence of network shape, and identical outcomes given the same seed.”【python†L1-L7】

**UMX-facing interpretation:**

- NAP is the **bus + clock + auditor** for the whole system.
- UMX/SLP is the **physics engine**; NAP guarantees that, even when UMX runs on multiple machines, it behaves like **one** synchronous lattice:
  - same tick `τ` everywhere,
  - same ordered writes,
  - same final state given the same seed and Gate inputs.

**v1 normative (for UMX):**

- UMX can assume:
  1. A **global tick** `τ` aligned across all nodes.
  2. All incoming writes are **deduped, ordered, and exactly-once** from UMX’s point of view.
  3. Every structural change relevant to UMX is **audited** in U-Ledger / Universal Integer stream.

---

## G.2 Message Model — Envelopes, “Just Numbers & Hashes”, Ports

### G.2.1 Envelope & Payload Ref

NAP never ships big blobs of raw state; it ships **hashes + stats**:

> “NAP packets are defined to carry ‘just numbers and hashes’ – e.g. tick τ, layer index ℓ, node IDs, a seed Ξ, summary stats (reuse ratio ρ, compression gain κ, code length ℒ) and content hashes. By design, payloads are never transmitted directly, only their content-addressed hashes and statistical descriptors.”【python†L2-L7】

And:

> “Every NAP message is encapsulated in a standard envelope with a header, payload reference, and an attestation signature… The header includes routing fields like stack\_delta ∈ {−1,0,+1}… and ring\_hops… Each envelope carries a unique nonce and deterministic identifiers so that duplicates can be recognized… The payload section… contains only compressed state deltas or hashes.”【python†L1-L7】

**UMX-facing consequences:**

- UMX **never** reads raw NAP payloads. Gate/Loom/Press resolve `payload_ref` into actual data, then convert to **UMX-native writes** (`GateWrite`, etc).
- For UMX, the key envelope fields are:
  - `tick τ` — which tick these writes belong to,
  - logical address (stack / ring / PFNA),
  - `payload_ref` — content-address to ledger entries,
  - `nonce` + hashes — for idempotence.

### G.2.2 Ports & Channels (M.in / M.out / M.audit)

NAP runs through **middle-layer ports** on each node:

> “NAP operates through the Trinity stack’s middle-layer ports on each node. Each node exposes a trio of logical ports: M.in (ingress), M.out (egress), and M.audit (read-only monitor). Outgoing messages are placed on M.out and incoming on peer nodes’ M.in… The M.audit port on each node collects a tamper-evident log of message events (send, receive, drop) for later verification.”【python†L2-L9】

And NAP guarantees **no silent vanish**:

> “Every outbound message must be matched by either a peer’s receipt or a local audit cancellation; no message is allowed to vanish silently.”【python†L2-L7】

**UMX-facing interpretation:**

- Gate + UMX live “behind” those ports:

  - **UMX → NAP:** Gate submits state summaries, P-deltas, TickLedgers via M.out.
  - **NAP → UMX:** Gate receives content-addressed updates via M.in, turns them into `GateWrite`s.

- **v1 normative:** UMX can assume that **if a write appears**, NAP has either:

  - matched it with a real receipt, or
  - explicitly cancelled it in M.audit so UMX never sees a half-transfer.

---

## G.3 Delivery, Idempotence, Rollback

### G.3.1 Exactly-Once Semantics

NAP is explicit about application-level **exactly-once**:

> “NAP delivers messages with effectively exactly-once semantics. Physically, it may employ retries and acknowledgments (at-least-once delivery at the transport level), but the idempotence tokens ensure that duplicates have no effect beyond the first application… Thus, from the application viewpoint, a message is applied exactly once or not at all.”【python†L3-L10】

NAP uses **nonces and content hashes** per envelope:

> “Each envelope’s nonce and content hash allow receivers to detect and discard duplicate messages deterministically.”【python†L3-L8】

**UMX contract:**

- UMX/SLP **must not** try to dedupe; it just assumes:
  - each logical `GateWrite` derived from NAP is either:
    - applied exactly once in the correct tick, or
    - never applied (if cancelled).

### G.3.2 Retries, Reversibility Window, Backpressure

NAP includes explicit retry + rollback logic:

> “If a sender gets no acknowledgement for a message within a timeout, it will retry a finite number of times, since reversibility and idempotence make re-sends safe… Should a message appear malformed… the receiver can NACK… and request a resend.”【python†L9-L15】

And:

> “To avoid indefinite blocking, each node employs a reversibility window: if an expected response does not arrive within a certain number of ticks, the protocol rolls back its intended effects on the sender side… a token send that wasn’t received is as if it never happened.”【python†L9-L16】

Also:

> “This mechanism provides back-pressure: if an M.out message is not acknowledged by a peer, the sending node’s audit port will flag and eventually annul it to keep budgets consistent.”【python†L2-L8】

**UMX-facing consequences:**

- NAP + Gate are responsible for:

  - **retries** (UMX just sees final committed effect),
  - **rollback of failed sends** before they become UMX writes,
  - **backpressure**: if the network is overloaded, some candidate writes will **never reach UMX** but the invariants (conservation, budgets) remain intact.

- **v1 normative:** UMX can treat all NAP-induced writes as **already consistent with budgets** and free of half-transfers.

---

## G.4 Ordering, Causality & Tick Alignment

### G.4.1 Global Ordering & Causal Barrier

NAP defines a global, partially ordered event stream:

> “All NAP messages include a logical timestamp (tick number τ) and are processed in a globally consistent order. The scheduler imposes a topologically sorted order by layer and tick – for a given tick τ, lower-layer (inner) messages are resolved before higher-layer ones, ties broken by node ID.”【python†L10-L18】

And:

> “The protocol imposes a causal barrier constant c (analogous to a speed-of-light): no message can affect another node in less than a certain tick interval… even if a network is fast, NAP will not allow an update to be visible to a distant node until at least the next tick.”【python†L10-L18】

**UMX connection:**

- UMX already has a **causality cap** `c` at the lattice level (how many hops effects can move per tick).
- NAP adds a **network-level** causal barrier:
  - cross-node / cross-layer messages cannot “arrive early” — they are aligned to tick boundaries.

**v1 normative:** UMX’s `tau` is the **same** `τ` NAP uses in envelopes; and UMX’s own hop-cap `c` must not conflict with NAP’s `c` (system-level design: typically both set to 1 for local cluster).

### G.4.2 Two-Phase Tick & Loom Integration

NAP runs on a **two-phase tick**:

> “Through its sidecar architecture, NAP often runs in a two-phase tick: first, each node performs its local compute for tick T; then NAP opens a synchronization window… during which nodes exchange their M.out state deltas and receive M.in updates. The engine (Aether) does not advance to tick T+1 until NAP signals that all nodes have the required updates (or the window timed out). This ensures no partial progress – either all nodes move forward together, or none do.”【python†L15-L23】

And combined with Loom:

> “Using Loom integration, if the sync window finishes early, Loom can compress the idle time; if it’s delayed, Loom can stretch the frame so that the next tick still starts aligned… NAP in concert with Loom provides a deterministic global clock: all nodes tick in unison, and causal order of events is preserved across the entire multi-machine system.”【python†L15-L23】

**UMX-facing contract:**

- UMX’s `tickOnce()` is always called in the **“local compute” phase** for tick `T`.
- NAP/ Loom:
  - control **whether UMX is allowed to advance** to `T+1`,
  - can pause, compress, or stretch wall-clock time, but not change the discrete τ sequence.

**v1 normative:** UMX must treat `tau` as purely **logical**; it never infers real time from it. NAP + Loom own the mapping “tick → wall-clock”.

---

## G.5 Aether Bus, Addressing & Topology Neutrality

NAP sits on top of UMX topology as a logical fabric:

> “The Nexus Aeternus introduces the Aether Bus, a logical communication fabric… While UMX’s topology handles physical adjacency and flow, the Aether Bus handles logical message passing which might span multiple hops… provides address discovery, partitioning, backpressure… still governed by deterministic rules.”【python†L1-L7】

And addresses:

> “NAP handles network addressing and routing for Trinity nodes (using a three-part address scheme radial.stack.local with deterministic node IDs).”【python†L1-L8】

Plus stack/nest routing hints in the envelope header:

> “The header includes routing fields like stack\_delta ∈ {−1,0,+1} (to indicate upward, same-level, or downward travel in the stack) and ring\_hops (distance in radial nest rings) which NAP uses to enforce layer and nest boundaries.”【python†L1-L7】

**UMX link:**

- PFNA `(layer,grid)` is the **physical anchor**; NAP’s `radial.stack.local` is the **logical address**.
- Aether Bus chooses a **logical route** (stack & ring transitions), then realises it as:
  - a sequence of NAP envelopes,
  - optionally corresponding UMX neighbour paths (via UMX\_ROUTE/SLP\_CONDUCT).

**v1 normative:**

- UMX itself doesn’t know about `radial.stack.local`, but:
  - it may expose PFNA anchors and adjacency as metadata so NAP can build bus routes.
  - it must tolerate NAP using the lattice for physical paths while keeping SLP/UMX invariants intact.

---

## G.6 Audit, U-Ledger, Universal Integer Stream & MDL Consensus

### G.6.1 U-Ledger & Universal Integer Stream U

NAP defines a **node-local ledger** and a global composite stream:

> “Each node maintains a local append-only ledger (the U-Ledger) of all send/receive events and resulting state hashes. These per-node logs feed into the global Universal Integer stream U, which is a single tamper-evident timeline of the simulation’s structural changes.”【python†L7-L14】

And:

> “NAP ensures that all structural events (node spawns, merges, edge additions) are recorded in U as hash-chained entries… when a new node spawns, its deterministic ID… is logged along with the event.”【python†L7-L14】

**UMX integration:**

- UMX’s **TickLedger** (root hash, P-deltas, I-block info) is exactly the kind of thing that gets:

  - logged in U-Ledger per node,
  - rolled up into the global Universal Integer stream.

- This is how you get **offline replay & audit** of UMX behaviour.

### G.6.2 MDL-Based Consensus on Inputs

NAP uses **MDL (Minimum Description Length)** as a consensus rule:

> “For inter-node state sync, NAP uses a consensus via MDL… when multiple nodes offer input to one node, that node chooses the subset that yields the best compression (smallest total code length ℒ)… If adding an input makes the explanation length worse… NAP’s rule is to drop it. This guarantees a deterministic choice without arbitrary tie-breaks.”【python†L20-L28】

**UMX-facing implications:**

- If several neighbours try to push different updates to the same UMX state:

  - NAP chooses the **MDL-best subset**,
  - only that subset is turned into Gate writes for UMX.

- That gives you:

  - deterministic resolution of conflicts,
  - no “random” input ordering effects.

**v1 status:** UMX doesn’t need to know about ℒ directly; it just gets a cleaned, MDL-filtered input stream.

### G.6.3 Commit Manifests & SEAL Messages

NAP terminates multi-step interactions with signed manifests:

> “Every multi-step interaction in NAP concludes with a manifest or commit message summarizing the agreed change… All involved nodes sign this manifest. Only upon verifying all signatures does each node incorporate the change into its ledger (U-Ledger)… This functions as an implicit consensus protocol for the Trinity cluster.”【python†L20-L28】

**UMX contract:**

- UMX is only updated by writes that are part of a **sealed commit**.
- If a multi-step interaction fails to reach SEAL:
  - UMX must not see a partial series of writes that leave budgets/invariants broken.

---

## G.7 Resource Budgets, Quotas & “Energetic Balance”

NAP is also responsible for **global budgets**:

> “NAP ensures temporal continuity, energetic balance, topological neutrality… energy or measure budgets are tracked and reconciled so that no resource imbalance persists unaccounted.”【python†L1-L8】

And:

> “Quota policies (like maximum message rate or size per node) are also enforced at the NAP layer… Any message exceeding defined quotas can be dropped or deferred by NAP’s scheduler, and such events are logged via the audit port.”【python†L7-L14】

Plus a hard check on measure drift:

> “Nodes explicitly include any budget drift: if the summed μ… across nodes is off by even a tolerance τ, NAP flags a protocol break.”【python†L7-L14】

**UMX consequences:**

- The **sum of conserved measures across the whole cluster** (not just within one UMX instance) is monitored by NAP.
- If UMX’s internal sum and the global budget disagree, NAP will:
  - treat that as a protocol break (bug or data corruption),
  - surface it via audit for investigation.

**v1 normative:** UMX must maintain exact integer conservation locally so NAP’s global budget checks remain valid.

---

## G.8 Message Types Relevant to UMX

NAP defines a set of general-purpose message types:

> “Message Types & Families: NAP defines several message families for node interaction… HELLO, BIND, SYNC precede normal traffic. Operational message types include CALL (function or data call), CAST (radial broadcast), BRIDGE (cross-layer invocation), SEAL (close out an exchange and reconcile budgets), and ECHO (round-trip test for reversibility)… They simply move numeric state or control signals under NAP’s rules.”【python†L1-L8】

For UMX, the most relevant:

- **SYNC** — aligns ticks and seeds before state exchange; ensures UMX ticks match NAP’s.
- **CAST** — broadcast of system-wide announcements (e.g. new global profile, parameter update).
- **BRIDGE** — cross-layer (or cross-pillar) invocations, e.g. UMX ↔ Press or UMX ↔ Gate joint operations.
- **SEAL** — commit of multi-step interactions that include UMX changes.
- **ECHO** — test that channels preserve reversibility; indirectly certifies that UMX ↔ NAP wiring hasn’t broken conservation.

**v1 status:** The exact mapping “message type → UMX action” lives in Gate/driver code, but the spec now clearly tells you **which message families you must support** for full Matrix–NAP integration.

---

## Gap Map G — NAP-Specific Gaps & Open Items

Relative to the current UMX spec + docs A–F, NAP introduces or sharpens these gaps.

---

### G1. Concrete JS NAP API (Beyond nap.js Envelope)

**Docs say:**

- We have envelopes, ports, M.in/M.out/M.audit, ID/nonce rules, retries, reversibility window, etc.【python†L2-L9】【python†L9-L16】

**Gap:**

- We only have a **partial** JS implementation (envelope canonicalisation). No full TypeScript-level API for:
  - HELLO/BIND/SYNC/CAST/BRIDGE/SEAL/ECHO,
  - M.in/M.out/M.audit port objects,
  - reversibility window and timeout configuration.

**Need:**

- A **NAP JS API spec**:
  - Types for envelopes, ports, message families.
  - Functions like `napSendCast`, `napBridge`, `napSeal`, each with explicit tick and budget semantics.

---

### G2. Reversibility Window Parameters

**Docs say:**

- There is a “reversibility window” measured in ticks; after that, unacknowledged messages are rolled back.【python†L9-L16】

**Gap:**

- No concrete value or formula for window length, nor a standard way to expose it to UMX/Gate.

**Need:**

- Define a **default window profile** (e.g. in ticks or wall-time) and an interface for:
  - tuning it,
  - reporting when rollbacks happen (so UMX/Gate can react).

---

### G3. Mapping Between NAP’s `c` and UMX’s `c`

**Docs say:**

- NAP has a causal barrier `c` (min ticks for an effect between nodes).【python†L10-L18】
- UMX has a hop-bound `c` for propagation per tick.

**Gap:**

- No explicit rule linking them (e.g. must they be equal? `c_NAP ≥ c_UMX`?).

**Need:**

- A **Causality Alignment note** in the spec:
  - e.g. for single-cluster deployments, set `c_NAP = c_UMX = 1`.
  - For multi-scale or remote deployments, define safe constraints.

---

### G4. MDL Consensus ↔ UMX MDL (Unification)

**Docs say:**

- NAP uses MDL to pick which node inputs to trust.【python†L20-L28】
- UMX/SLP has its own MDL-based structural learning design.

**Gap:**

- No unified view of **whether these MDL objectives are the same or separate layers**.

**Need:**

- A short **MDL Unification doc** that:
  - either defines a shared ℒ and penalty weights, or
  - explicitly treats NAP’s MDL as “transport-level consensus” and UMX’s MDL as “topology-level learning”, with different parameters.

---

### G5. Commit Manifest Schema & SEAL Semantics

**Docs say:**

- SEAL messages carry commit manifests with hashes, participant IDs, and timestamps; all participants sign before committing.【python†L20-L28】

**Gap:**

- No JSON / binary schema for commit manifests or signature layout in the current JS-facing docs.

**Need:**

- A **Commit Manifest v1 schema** with:
  - fields (tick, participants, hash list, budgets),
  - signing rules,
  - how UMX TickLedger hashes are plugged in.

---

### G6. U-Ledger Storage & Universal Integer Indexing

**Docs say:**

- Each node keeps U-Ledger; all nodes feed a global Universal Integer stream U.【python†L7-L14】

**Gap:**

- No on-disk format, no index scheme, no retention policy documented for U-Ledger / U.

**Need:**

- A **U-Ledger / U format doc**:
  - record structure (envelope ref, tick, root hash, event type),
  - index keys (by node, tick, hash),
  - how to reconstruct UMX state from U.

---

### G7. Quotas & Budget Drift Policies

**Docs say:**

- NAP enforces quotas, tracks μ drift, and flags protocol breaks on mismatch.【python†L7-L14】

**Gap:**

- No concrete rules for:
  - what counts as “tolerance τ” for drift,
  - how strict quotas are, and what UMX/Gate should do when NAP drops or defers messages.

**Need:**

- A **Budget Profile Annex**:
  - default quota per node / per pillar,
  - drift tolerances,
  - required reactions (e.g. degrade gracefully vs hard fail).

---

### G8. Two-Phase Tick Hooks for UMX

**Docs say:**

- NAP runs ticks in “compute phase → sync phase”, and Aether must not move to T+1 before NAP is done.【python†L15-L23】

**Gap:**

- UMX spec currently just exposes `tickOnce()`; no explicit hook for “sync phase complete”.

**Need:**

- A simple integration contract like:
  - Gate calls `umx.tickOnce()` during **Phase 1**, then only after NAP’s sync window/SEAL completes does it increment τ and call it again.
  - Optionally a “tick barrier” callback for more complex engines.

---

### Source: `umx_complement_doc_h_nap_integration_full.md` (verbatim)

---

# Complement Doc H — Legacy NAP Reports: Stress Tests, Nesting & Precision

This doc folds in everything **extra** the **older NAP / stacking reports** say that isn’t already covered in Complement Doc G.

Sources used here:

- *Trinity NAP Stress Test Report* (both versions).
- *Sub-Planck Simulation Through Hierarchical Stacking*.
- *Nesting Protocol (1)*.
- *early nap v1* (Village/Town/City bridge set).
- *Trinity Relational Proof-of-Concept Report*.
- *trinity\_layer\_precision\_report*.
- (Plus light confirmation from the “Successful Test 01” docx.)

Where useful I mark:

- **v1 normative** — safe to treat as required behaviour now.
- **v2 / design-level** — clearly intended, but not yet wired into JS/UMX.

---

## H.1 Stress Tests — Scaling, Failure Modes & What “Breaks” Look Like

The **NAP stress-test reports** push the architecture to large grids and deep stacks and then poke at where it breaks.

### H.1.1 Tested setups

The reports describe (examples):

- **Stable regime:** 50×50 grid, **3 Trinity layers**, full NAP + Loom + Press, modest lateral NAP fan-out → stays numerically stable.
- **Edge regime:** 100×100 grid, **5 Trinity layers**, heavy lateral NAP broadcast between layers (dense bus) → still mostly stable but reveals **rounding noise and resonance**.

### H.1.2 Identified failure modes

1. **Precision floor (float underflow):**
   - In the original float-based prototypes, some budgets are tracked with **64-bit floats**.
   - Near extreme scales, **very small residuals** get crushed below machine epsilon → “phantom” budget drift appears.
   - This manifests as **tiny but systematic** μ drift over long runs.
2. **Over-coupling / resonance loops:**
   - When **too many lateral NAP links** connect layers (e.g. every node in layer L broadcasting to every peer in L+1 and back), the system can form **feedback loops**.
   - These loops **amplify rounding noise** (even if each step is conservative in expectation) and show up as low-frequency “breathing” oscillations in measures.
3. **Entropy aliasing in compressed channels:**
   - When Press/Loom compress time-series or summary packets aggressively and NAP re-injects them frequently, **pseudo-periodic noise** can appear:
     - repeated pattern of compressed residues that never fully die out,
     - looks like a “ringing” after a strong disturbance.

### H.1.3 Interpretation for UMX/SLP v1

Because UMX v1 is **integer-only**, the **precision floor** issue is mostly a **historical cautionary tale**:

- **v1 normative:**
  - UMX/SLP/NAP/Press **must not rely on IEEE float semantics** for conserved budgets.
  - Any budget/μ tracked at NAP level that must be exact **must be represented in integers or rational encodings** (e.g. scaled integers), not raw doubles.
- **Design-level / future guards:**
  - Add stress-test hooks:
    - detect if cross-pillar compression + NAP routing are introducing **persistent low-amplitude oscillations** in μ,
    - flag over-coupling patterns (e.g. “too many” bus links between the same layers) as a **health warning**.

---

## H.2 Nesting Protocol & Stacked Simulations (Cross-Stack NAP Use)

The **Nesting\_Protocol (1)** and **Social Mod Stacking** reports treat NAP as the glue between **stacked simulations**:

- One “outer” Trinity stack supervises **many inner stacks** (or sims), each with its own UMX/SLP lattice.
- NAP is used to **exchange only summary information**, not raw full state, between these stacked layers.

### H.2.1 Summary vectors / packets

From *early nap v1* and the Nesting material:

- Each lower-level region (e.g. Village / Town / City, or sub-sim) periodically outputs a **packet**:
  - Example (Village packet (O\_V)) contents:
    - Counts (N\_V).
    - Mean and variance of some feature (F): (\mu\_F^V, \sigma\_F^{2,V}).
    - Mean of another variable (R): (\mu\_R^V).
    - Aggregated production vector over window: (\text{Prod}\_V).
    - A synergy / interaction score (e.g. average over pairwise σ(α − distance)).
    - Event counts by type over the tick window.
- The outer layer (Town/City or top sim) forms **weighted aggregations** of these packets (e.g. population-weighted sums) and uses them to update its own state.

**v1 normative (as a *************pattern*************):**

- When NAP is used for **stacked sim coupling**, the **default contract** is:
  - Lower layers send **summary packets**, not raw fields,
  - Packets contain **counts, means, variances, and aggregates**, all in integer / rational form,
  - Outer layers **never directly mutate inner lattice cells**; they only change:
    - their own state, and/or
    - the parameters / boundary conditions that inner layers see on the next step.

### H.2.2 NAP’s role in nesting

- NAP is the carrier of these packets, enforcing:
  - **tick alignment** between inner and outer layers (inner tick ratios (k\_{VT}, k\_{TC}) etc.),
  - **budget and μ conservation** when information or resources cross stack boundaries,
  - deterministic idempotence (no double-applying the same packet).

**Design-level tightening:**

- Define a **“Nesting Profile”** on NAP that:
  - standardises summary packet structure (core fields like N, means, variances, windowed sums),
  - sets **minimum tick ratio rules** (e.g. inner runs (k) ticks per outer tick),
  - guarantees that **only summaries** are exposed; raw cell values never leave UMX via NAP in nested modes.

---

## H.3 Sub-Planck Stacking & Integer Scaling (ε Layers)

The **Sub\_Planck\_Simulation\_Through\_Hierarchical\_Stacking** report explains how **sub-grid (“sub-Planck”) detail** is represented by **extra layers + residual scaling**.

### H.3.1 Cross-layer relation

Core equation (paraphrased):

- Each higher-level layer (L+1) gets state:

  [\
  s\_{L+1} = f\_L(s\_L) + \varepsilon\_L\
  ]

  where:
  - (f\_L) is a **coarse summarisation** (e.g. block mean or other aggregator),
  - (\varepsilon\_L = R(s\_L - \hat{s}\_L)) is a **scaled integer residual**,
    - (R) is a **fixed integer scaling factor** (e.g. 10⁶), ensuring the residual is integer-encoded,
    - (\hat{s}\_L) is the predicted/coarse reconstruction at layer L.
- NAP ensures that these ε terms are passed **conservatively**, so stacked sims preserve total μ.

### H.3.2 What this adds for UMX/NAP

We already had **residual layering** in Complement Docs E & F. The sub-Planck report adds:

- **v1 normative (safe, matches architecture):**
  - Any “sub-grid” or “precision” layer that crosses stack boundaries via NAP **must be:**
    - expressed as **integer residuals** (using a fixed R), and
    - tied to a clear **anchor map** down to base UMX cells.
- **Design-level:**
  - Define an explicit **“ε-layer profile”**:
    - R values per profile (e.g. 10³ for coarse, 10⁶ for fine),
    - maximum depth of residual stacks (how many ε levels are allowed),
    - rules for when ε\_L is allowed to persist vs when it must be “folded back down” and re-normalised.

---

## H.4 Layer Precision & Error Behaviour (Legacy Float Prototype)

The **trinity\_layer\_precision\_report** gives a toy error table across 1–4 layers, showing:

- Single layer: higher mean squared error (MSE) when approximating some target dynamics.
- 2–4 layers: progressively lower error, roughly exponential improvement.
- At deeper stacks, error flattening as compression & rounding combine.

In the legacy system this was based on **float arithmetic**, but the **shape** of the results is what matters:

- **Layered residuals** drastically reduce error,
- But error never completely vanishes — there is always some residual “noise” that moves around.

**Implications for v1 integer UMX/NAP:**

- **v1 normative (already aligned):**
  - Treat each extra residual layer as a **refinement of approximation**, not as a guarantee of exactness.
  - UMX + NAP should **never claim** “perfect reconstruction” beyond the integer lattice resolution; they claim **perfect replay** of whatever was encoded, not perfect modelling of the external world.
- **Design-level:**
  - Add optional **precision profiles** that:
    - give recommended depth of residual stacks for given tasks,
    - define budget thresholds where extra layers offer diminishing returns.

---

## H.5 Relational Proof-of-Concept — Summary Exchange Cadence

The **Trinity Relational Proof-of-Concept Report** shows a small system:

- One “relational” node watches two or more UMX domains,
- It doesn’t see raw state; instead, **every 5 ticks** each domain sends:
  - mean state of selected fields,
  - residual magnitudes or other simple stats.

NAP coupling behaviour:

- Mean & residual summaries are exchanged on a **fixed cadence** (e.g. every 5 ticks),
- Nodes update based only on these aggregates, preserving deterministic reproducibility.

**v1 normative pattern:**

- When NAP is used for **relational supervision** (e.g. meta-monitors, dashboards, Codex watchers):
  - Exchanges should happen on **fixed, declared cadences** (e.g. every N ticks), not on ad-hoc events,
  - Payloads should be **simple aggregates** (mean, variance, counts, norms), not arbitrary scripts,
  - These exchanges **must not inject new μ**; they’re read-only from the perspective of the budget.
- This gives you a clean separation:
  - UMX/SLP = physics,
  - NAP relational monitors = “read the physics by summary” without perturbing it, unless a specific write is agreed via SEAL.

---

## H.6 How H Relates to Complement Doc G

Complement Doc G already covered:

- NAP’s envelope model, ports, idempotence, global tick, causal barrier, MDL consensus, SEAL, U-Ledger, budgets.

This **Doc H** adds:

- **Scaling constraints:** why we insist on integer budgets and how over-coupling / compression loops can cause resonance.
- **Nesting semantics:** summary-packet-only coupling between stacked sims (Village/Town/City pattern).
- **Sub-Planck ε layers:** explicit integer-scaled residual layers crossing stacks via NAP.
- **Relational cadence:** fixed-cadence summary exchange patterns for relational monitors.
- **Design-level profiles:** suggestions for Nesting Profile, ε-layer profile, and precision/stress profiles that haven’t yet been formalised.

---

## Gap Map H — New Gaps Exposed by Legacy NAP / Stacking Reports

Relative to A–G, these older reports introduce a few extra holes.

---

### H1. Summary Packet Schema for Stacked Sims

- **Docs:** early nap v1, Nesting Protocol, social stacking reports.
- **Gap:** No **canonical schema** for cross-stack summary packets (O\_V, O\_T, etc.) in the main spec.
- **Need:** A **Summary Packet v1** definition:
  - core fields (counts, mean/variance of key fields, windowed production vectors, synergy scores, event counts),
  - encoding rules (all integer / rational),
  - tick window semantics (how many ticks each packet covers).

---

### H2. ε-Layer Profile & Scaling Factor R

- **Docs:** Sub-Planck stacking report.
- **Gap:** No explicit **R** values or max residual depth in spec; ε layers are conceptually described but not parameterised.
- **Need:** An **ε-Layer Profile Annex**:
  - recommended R values,
  - maximum ε depth per profile,
  - rules for folding residuals back into base layers or rescaling when they get too large.

---

### H3. Over-Coupling Detection & Resonance Guards

- **Docs:** NAP stress tests (resonance loops with too many lateral links).
- **Gap:** No spec’d **diagnostic or guardrails** for NAP over-coupling (bus too dense between certain layers).
- **Need:**
  - A simple **over-coupling heuristic** (e.g. max NAP degree / fan-out per node per layer),
  - optional **health checks**: watch μ variance over time; flag persistent oscillation at small amplitudes.

---

### H4. Integer vs Float Budget Discipline at NAP Level

- **Docs:** Stress tests and layer precision report (legacy floats).
- **Gap:** Main spec doesn’t explicitly **ban floats** for budgets; it just says UMX is integer.
- **Need:** A norm like:
  > “All budget / μ-like quantities shared across pillars (UMX/NAP/Loom/Press/TGP) MUST be represented as integers or exact rational encodings. Float representations may be used for internal approximations but not as the authoritative source of truth.”

---

### H5. Relational Monitor Cadence & Permissions

- **Docs:** Relational PoC report (summary exchange every N ticks, no direct mutation).
- **Gap:** No explicit rule on **cadence** for relational NAP traffic or on mutation rights.
- **Need:** A small **Relational NAP Profile**:
  - fixed cadences,
  - allowed payload types,
  - whether monitor nodes are read-only vs allowed to submit SEAL’d writes.

---

### H6. Nesting Profile & Tick Ratios

- **Docs:** early nap v1 (Village/Town/City ratios k\_VT, k\_TC), Nesting report.
- **Gap:** UMX/NAP spec doesn’t mandate how **inner/outer tick ratios** are wired for nested sims.
- **Need:**
  - A **Nesting Profile** that:
    - states allowable ratios,
    - defines when inner stacks are allowed to “run ahead” vs must stay tightly coupled,
    - clarifies how NAP enforces tick alignment in presence of different step sizes.

---

### Source: `umx_trinity_gate_integration_spec_v_1_2025_11_17.md` (verbatim)

# UMX–Trinity Gate Integration Spec v1  
**Status:** Draft v1 (implementation-ready)  
**Scope:** Wire up compatibility so the **Universal Matrix (UMX)** pillar mounts cleanly onto **Trinity Gate** and exposes its matrix features through Gate’s scene + I/O layer.

---

## 0) Canon anchors (short quotes)

These are the **only** authorities this spec leans on.

### 0.1 Pillar & protocol names

From the Aether canon name changes:

> "Pillar: Luminous Lattice → **Universal Matrix (UMX)** — locked"  
> "Protocol: Luminous Lattice Protocol → **Synaptic Ley Protocol (SLP)** — locked"  
> "Pillar: Trinity Gate → **Trinity Gate** — unchanged"  
> "Protocol: Trinity Gate Protocol → **Triune Bridge Protocol (TBP)** — locked"  
> — `Aether_Name_Changes_2025-11-01.md`

### 0.2 Trinity Gate identity

From the features/components report:

> "Defined as Aether’s **interface engine and universal translator** between quantum descriptions, classical probabilities, and deterministic classical computation in a common relational framework."  
> "Operates as a **standalone execution engine** that converts between these descriptions with near‑lossless fidelity and negligible computational cost."  
> — `trinity_gate_features_components_capabilities 1.md`, §1.1

From the TBP / Gate implementation spec:

> "Gate is the **scene I/O layer** on a 2D plane; exports structured scenes (JSON/CSV/images)."  
> — `tbp_gate_implementation_spec_v_1.md`, §3.2 "Gate scene (export projection)"

From the long development narrative:

> "**Internal (Aether) Interfaces:** Trinity Gate communicates with internal Aether pillars and publishes a consolidated state snapshot into the ledger pipeline."  
> — `6 ChatGPT-development and testing v1.md`, Interfaces & Bindings section

### 0.3 UMX identity

From the UMX dev README:

> "You are holding the **Universal Matrix (UMX) v1** pack."  
> "UMX = **graph substrate + tick engine + drift/emergence + NAP + ledger**"  
> "Paper‑first, pure‑math core, JS shell around it, offline."  
> — `UMX_README_FOR_DEVS_v1.md`

From the UMX spec master index:

> "Maintains a **graph‑structured substrate** of nodes and edges over one or more layers."  
> — `umx_spec_master_index_readme_2025_11_16.md`

From the pillar spec:

> "Role: **Deterministic integer substrate for state storage and conservative propagation.**"  
> "Invariants – Conservation: Σ cells constant for SLP updates. – Determinism: Same inputs ⇒ identical root hashes per tick. – Causality: No effect beyond `c` hops per tick. – Integer‑only: No floats, no randomness."  
> — `universal_matrix_pillar_spec_v_1.md`, role & invariants sections

From the UMX TBP bundle:

> "This bundle contains the fourth batch of **normative and operational TBP–UMX artifacts**, mirroring the TBP Gate pack but specialised for the Universal Matrix pillar."  
> "# TBP–UMX Implementation Spec v1"  
> "Establishes constraints for the first runtime realisation: an **offline JS page that wraps pure math functions that could be executed on paper**."  
> — `umx_spec_artifacts_bundle_4_umx_tbp_pack_2025_11_16.md`

---

## 1) Integration intent

Given the canon above, we interpret the desired relationship as:

- **Trinity Gate** is the **interface engine and universal translator**, and the **scene I/O layer** that communicates with internal pillars and publishes consolidated snapshots into the ledger pipeline.
- **UMX** is the **deterministic integer substrate** and **graph‑structured matrix** that holds and propagates state using SLP, with conservation, causality and determinism guarantees.
- The TBP–UMX bundle explicitly mirrors the TBP Gate pack, so UMX is already framed as a **TBP‑aware pillar** intended to sit alongside Gate in the Aether stack.

**Goal of this spec:** make that relationship concrete by defining **contracts and data flows** so that:

1. UMX’s matrix is treated as a **first‑class internal pillar** behind Gate.
2. Gate’s **scene** becomes a projection of UMX (plus other pillars), not a separate topology.
3. NAP / Loom / U see a **single, consistent story** through the TBP lens, even though matrix logic lives in UMX.

Where this spec suggests new structures, it treats them as **v1 integration decisions** layered on top of the canon, not replacements.

---

## 2) Execution order and roles (tick contract)

### 2.1 Canon‑aligned roles

From the Gate features report and dev narrative we have:

> "Serves as the **perceptual interface** of the Aether stack – effectively *how you see and talk to* Aether processes."  
> — `trinity_gate_features_components_capabilities 1.md`, §1.2

> "Trinity Gate communicates with internal Aether pillars and publishes a consolidated state snapshot into the ledger pipeline."  
> — `6 ChatGPT-development and testing v1.md`, Interfaces & Bindings

From the UMX pillar spec:

> "Role: Deterministic integer substrate for state storage and conservative propagation."  
> — `universal_matrix_pillar_spec_v_1.md`

**Interpretation:**

- UMX is a **substrate pillar** — it owns a graph‑structured, integer‑only state and conservative propagation.
- Gate is an **interface + aggregation pillar** — it talks to pillars like UMX and publishes a consolidated scene.

### 2.2 Tick‑level execution contract (v1 decision)

For each tick `τ`, this spec defines the following order:

1. **UMX update phase**
   - UMX applies:
     - any pending NAP envelopes destined for the matrix,
     - any topology or signal updates routed from Gate via TBP channels,
     - its own internal propagation (SLP) as per the invariants:

   > "Conservation: Σ cells constant for SLP updates.  
   > Determinism: Same inputs ⇒ identical root hashes per tick.  
   > Causality: No effect beyond `c` hops per tick.  
   > Integer‑only: No floats, no randomness."  
   > — `universal_matrix_pillar_spec_v_1.md`

   - UMX computes its per‑tick metrics (residuals, drift, budgets, etc.) per the TBP–UMX Implementation Spec modules.

2. **Gate aggregation phase**
   - Gate queries UMX for a **Matrix State Frame** (defined in §3) and merges it with other pillar outputs (if present) to form its **scene**.
   - Gate then applies TBP to produce a structured, integer‑only scene export:

   > "Gate is the **scene I/O layer** on a 2D plane; exports structured scenes (JSON/CSV/images)."  
   > — `tbp_gate_implementation_spec_v_1.md`

3. **Loom / Press / U phase**
   - Loom, Press and the U‑ledger operate on Gate’s exported scene and its hash, exactly as already described in the Gate/TBP runbook and UMX U‑ledger contracts.

This order is deliberately **substrate → interface → log**: UMX stabilises its internal matrix, Gate snapshots and translates it, Loom/Press/U persist it.

---

## 3) UMX → Gate: Matrix State Frame

### 3.1 Canon basis

From the UMX master index and pillar spec:

> "Maintains a **graph‑structured substrate** of nodes and edges over one or more layers."  
> — `umx_spec_master_index_readme_2025_11_16.md`

> "Role: Deterministic integer substrate for state storage and conservative propagation."  
> — `universal_matrix_pillar_spec_v_1.md`

From the Gate implementation spec:

> "Gate is the scene I/O layer on a 2D plane; exports structured scenes (JSON/CSV/images)."  
> — `tbp_gate_implementation_spec_v_1.md`

**Interpretation:** UMX owns the **matrix topology and conservative propagation**, while Gate owns the **scene view and I/O**. The integration point is a per‑tick **Matrix State Frame** which Gate consumes and projects into its scene.

### 3.2 Matrix State Frame structure (v1 definition)

For each tick `τ`, UMX MUST expose a **Matrix State Frame** to Gate with three logical parts:

1. **Node table** (topology + placement)

   One row per active matrix node, all integer fields, e.g.:

   - `node_id` — integer node identifier (local to UMX but stable over a run),
   - `layer_id` — integer layer index (aligned with SLP layers),
   - `x`, `y` — integer lattice coordinates for Gate’s 2D scene plane,
   - `anchor_id` — integer code for the underlying anchor or source shard,
   - `zone_id` — optional integer for cluster/region grouping,
   - `flags` — bitfield for roles (boundary, source, sink, fixed, etc.).

   This respects the idea of a **graph‑structured substrate over one or more layers** while giving Gate a direct mapping into its 2D lattice.

2. **Edge table** (graph connectivity)

   One row per active edge, e.g.:

   - `edge_id` — integer edge identifier,
   - `src_node_id`, `dst_node_id` — integer endpoints,
   - `layer_id` — layer index where the edge lives,
   - `capacity` — integer capacity/weight,
   - `policy_id` — integer policy code for routing semantics,
   - `flags` — bitfield (unidirectional, bidirectional, SLP‑active, etc.).

3. **Invariant summary** (conservation, causality, determinism)

   A compact integer vector whose entries correspond to UMX invariants, for example:

   - `UMX_SUM_BEFORE`, `UMX_SUM_AFTER`, `UMX_DELTA` — global sum and per‑tick delta for the conserved quantity,
   - `UMX_DAG_OK` — 1 if the active topology passes the acyclicity / nest‑geometry checks defined in the complement docs, 0 otherwise,
   - `UMX_CAUSAL_RADIUS` — maximum number of hops `c` allowed per tick,
   - `UMX_INT_ONLY_OK` — 1 if all matrix updates obey the integer‑only constraint.

   These reflect and externalise the invariants quoted earlier from the pillar spec.

### 3.3 Gate’s obligations

When consuming a Matrix State Frame, Gate MUST:

- Treat UMX’s node + edge tables as the **authoritative topology** for any matrix‑backed actors and bonds in its scene.
- Map `x,y` directly into its 2D plane when placing actors.
- Embed the invariant summary into its `summary` / `metrics` fields inside the export scene schema, keeping them **integer‑only** to comply with TBP.

This ensures that **Gate’s scene is a projection of UMX** (plus any other pillars), not an independent, conflicting topology.

---

## 4) Gate → UMX: TBP channels

### 4.1 Canon basis

From the Gate features and TGP focus docs we know Gate is responsible for:

> "Schema Registry … maintains canonical data definitions … so that every external input is validated against known schemas."  
> — `trinity_gate_tgp_focus_expansions.md`, §1.1

> "Serves as the perceptual interface of the Aether stack – effectively how you see and talk to Aether processes."  
> — `trinity_gate_features_components_capabilities 1.md`, §1.2

From the TBP–UMX implementation spec:

> "Defines mandatory interfaces and contracts for UMX to interact with SLP, Loom, NAP and the Aether Testbed."  
> — `umx_spec_artifacts_bundle_4_umx_tbp_pack_2025_11_16.md`

**Interpretation:** All external inputs are **TBP‑normalised** by Gate and routed inward via schemas. UMX should only see the subset of these inputs that are explicitly addressed to the matrix.

### 4.2 UMX‑targeted channel families (v1 definition)

We define two **families of TBP channels** in Gate’s schema registry that target UMX:

1. **Topology channels** (UMX_TOPOLOGY_UPDATE)

   - Purpose: change matrix layout (create/delete/move nodes, edges, layers) in response to external intent.
   - External payload (pre‑TBP): descriptive, human‑ or app‑friendly structure (IDs, roles, maybe coordinates).
   - TBP normalisation: map everything into **integer IDs and coordinates**, with units normalised as necessary.
   - Internal contract: Gate converts each normalised envelope into one or more UMX operations such as `PLACE`, `ROUTE`, or related actions defined in the UMX complement docs.

2. **Signal channels** (UMX_SIGNAL_INJECTION)

   - Purpose: inject signals, resources or disturbances into the matrix (boundary conditions, source terms, etc.).
   - External payload: numeric or symbolic descriptions of inputs.
   - TBP normalisation: convert to integer magnitudes and addresses, ensuring conservation rules are compatible with UMX’s invariants.
   - Internal contract: Gate converts normalised signal envelopes into UMX edge/node updates and/or SLP boundary conditions.

### 4.3 NAP envelopes and UMX integration

The TBP and TBP–UMX specs both describe NAP as the envelope layer:

> "NAP Integration Module … Marshall NAP envelopes into internal actions … Enforce idempotence and exactly‑once semantics via nonces and per‑scope tracking … Emit outbound envelopes according to `umx_nap_bus_contract_v1`."  
> — `UMX_README_FOR_DEVS_v1.md`, §3.4

This spec aligns with that by requiring:

- All UMX‑targeted TBP channels be wrapped in **NAP envelopes** with the usual nonces and scopes.
- UMX’s NAP integration module to interpret those envelopes and update the matrix accordingly at the next tick.

Gate remains responsible for **schema correctness and external policy**, while UMX remains responsible for **matrix semantics**.

---

## 5) Cross‑pillar invariants & tests

UMX and Gate each bring their own invariants. The integration must expose combined checks that can be exercised by the existing **verification/test plans** on both sides.

### 5.1 Conservation & continuity

From the UMX pillar spec invariants:

> "Conservation: Σ cells constant for SLP updates."  
> — `universal_matrix_pillar_spec_v_1.md`

From the Gate features and math/bridge work (via continuity equations and conservation language in the Trinity Gate docs):

> "Conservation of measures … any external value injected via Gate that would violate conservation laws (mass, energy, etc.) must be counter‑balanced or rejected."  
> — `trinity_gate_features_components_capabilities 1.md`, conservation section

**Integration rule (v1):**

- For any tick `τ` where UMX reports `UMX_DELTA ≠ 0` in its invariant summary, Gate MUST:
  - Log the corresponding external Δ as a TBP‑normalised contribution in its ingress ledger, **or**
  - Treat the condition as a policy violation and roll back / quarantine the tick.

This combines UMX’s **internal conservation** with Gate’s **external conservation policy**.

### 5.2 Causality & routing

From the UMX invariants and SLP semantics:

> "Causality: No effect beyond `c` hops per tick."  
> — `universal_matrix_pillar_spec_v_1.md`

This spec requires that:

- Any Gate scene elements that correspond to UMX routes must not show effects propagating faster than `c` hops per tick.
- Cross‑pillar tests should:
  - Configure UMX with a known causal radius `c`,
  - Inject a signal via a UMX_SIGNAL_INJECTION channel,
  - Verify via Gate’s scene and Loom’s replay that no actor beyond `c` hops shows an updated state at tick `τ+1`.

### 5.3 Replay & determinism

UMX guarantees deterministic propagation for a given sequence of envelopes, and Gate/TBP guarantees deterministic scene exports and replayability.

This spec requires:

- The Matrix State Frame be **reconstructable from Loom/Press logs** by:
  - Replaying NAP envelopes into UMX,
  - Rebuilding the matrix state for tick `τ`,
  - Re‑exporting the Matrix State Frame and comparing it to the one embedded in the original Gate scene.

Passing this check means **UMX and Gate are jointly deterministic and replayable** under TBP.

---

## 6) Dev handoff checklist

This section is for implementers. It assumes the code and packs already returned by the devs and focuses only on integration glue.

1. **Expose the Matrix State Frame**
   - Implement a UMX API that returns the Node table, Edge table and invariant summary described in §3 for a given tick `τ`.
   - Ensure all values are integers and consistent with the UMX invariants.

2. **Wire Gate’s scene builder to UMX**
   - In the Gate scene builder, add a UMX integration step that:
     - Calls the UMX Matrix State Frame export,
     - Creates/updates scene actors and bonds from the Node/Edge tables,
     - Injects the invariant summary into the scene’s `summary/metrics`.

3. **Register UMX TBP channels in the Schema Registry**
   - Add schemas for `UMX_TOPOLOGY_UPDATE` and `UMX_SIGNAL_INJECTION` envelopes.
   - Ensure they follow TBP’s integer‑only and unit‑normalisation rules.

4. **Route UMX‑targeted NAP envelopes into UMX**
   - Configure the NAP integration layer so that envelopes matching UMX channel schemas are dispatched to UMX’s NAP Integration Module.

5. **Augment existing test suites**
   - Add at least one **golden scenario** where:
     - UMX runs a small, known topology,
     - Gate consumes its Matrix State Frames to render a scene,
     - Loom/Press replay reconstructs both the scene and the matrix invariants.
   - Plug this into both the TBP Gate and TBP–UMX verification packs.

6. **Document the integration**
   - Add a short "UMX Integration" subsection to the Trinity Gate implementation spec and operator runbook referencing this document.
   - Add a reciprocal note in the UMX TBP bundle indicating that Gate is the canonical consumer of Matrix State Frames.

Once these steps are done, the **matrix is effectively mounted on the Gate**: UMX owns the topology and conservative propagation; Gate owns the interface and scene; and TBP/NAP/Loom/Press/U see a single, coherent, integer‑first story across both pillars.

---

## 7) Gate → UMX capability delegation (hand‑off)

The user has explicitly requested that **Gate hand off its appropriate functions and capabilities to the Matrix** so that fully integrated functionality is achieved in both directions.

Canon already hints at this split:

> "Lattice/UMX as substrate & placement/routing substrate."  
> "UMX/SLP & NAP carry/propagate these translated states deterministically across the lattice and message fabric."  
> — `8 ChatGPT-Build new computing paradigm.md`

and for Gate:

> "Defined as Aether’s "interface engine and universal translator" between quantum descriptions, classical probabilities, and deterministic classical computation in a common relational framework."  
> — `trinity_gate_features_components_capabilities 1.md`

> "Gate explicitly functions as: Membrane (controls all external ingress/egress of state). Projection layer (presents internal state as external scenes)."  
> — `trinity_gate_features_components_capabilities 1.md`, §2.4

### 7.1 Principle

- **UMX/SLP + NAP** own **substrate, placement, routing, propagation and conservative transport** across the lattice/message fabric.
- **Gate/TBP** owns **external description mapping, membrane, projection, and schema/policy**.

Whenever there is overlap, this spec resolves it by **delegating substrate‑level responsibilities down into UMX** and keeping Gate as a thin, deterministic shell around those capabilities.

### 7.2 Capabilities handed off to UMX

The following functional areas SHOULD be treated as UMX responsibilities, with Gate acting only as caller/consumer:

1. **Adjacency & topology**
   - UMX is the **placement/routing substrate**; any adjacency, neighbourhood or routing graph that Gate needs for matrix‑backed actors MUST come from UMX’s Matrix State Frame (§3), not from a separate Gate‑owned graph.

2. **Routing and path selection**
   - UMX/SLP are responsible for how signals move over the lattice, subject to conservation and causal radius.
   - Gate MUST NOT implement its own routing heuristics for matrix state; it may only request routes or observe results exported by UMX.

3. **Conservative propagation**
   - UMX/SLP & NAP "carry/propagate these translated states deterministically across the lattice and message fabric" (canon quote above).
   - Gate MUST treat matrix‑related deltas as outputs of UMX propagation, not as a place to inject extra numeric adjustments.

4. **Region/zone and coordinate frames**
   - UMX is responsible for defining region/zone masks and coordinate frames for the matrix.
   - Gate may render these as scene layers, overlays or groupings but should not re‑assign coordinates independently.

5. **Matrix‑level residuals and backfill**
   - Where residuals, epsilon fields or BACKFILL() behaviour are defined for UMX/SLP, Gate should surface them as metrics/diagnostics.
   - All logic about when/how to apply residuals across the lattice stays inside UMX.

### 7.3 Capabilities retained by Gate

Gate retains and continues to own:

1. **Membrane & projection**
   - Gate remains the **semi‑permeable membrane** and **projection layer** around the core, controlling ingress/egress and presenting scenes.

2. **Schema registry & TBP mapping**
   - All external inputs are still normalised, validated and quantised under TBP in Gate before any UMX‑targeted channels are formed.

3. **Scene composition & export formats**
   - Gate composes the overall scene from UMX plus other pillars and chooses the external export form (JSON/CSV/images/frames).

4. **Policy enforcement & quarantine**
   - Gate remains the place where policy decisions, quarantine of invalid ticks, and external conservation checks are enforced based on UMX invariants and TBP rules.

### 7.4 Practical implication for implementers

- Where existing Gate code calculates adjacency, neighbourhoods or propagation internally, those paths SHOULD be refactored so that:
  - For matrix‑backed entities, Gate calls into UMX or consumes UMX exports instead of maintaining its own parallel structures.
- Where Gate previously performed conservation checks directly on raw scene data, it SHOULD instead:
  - Use UMX’s invariant summary (Σ before/after, Δ, causal radius, etc.) as primary signals, and
  - Apply TBP/ledger policy based on those invariants.

In short: **UMX becomes the substrate brain for anything matrix‑like**; **Gate becomes the disciplined mouth and eyes** that translate between that substrate and the outside world.

---

## 8) Before / After guide for devs

This section is a quick refactor guide so implementers can see exactly what changes.

### 8.1 Gate responsibilities – BEFORE

**Topology & routing**
- Gate may maintain its own adjacency structures for scene actors.
- Gate may compute neighbourhoods ("which actors are near this one?") using its own data.
- Gate may implement routing or influence propagation directly in the scene layer.

**Conservation & invariants**
- Gate may enforce conservation by inspecting raw scene values and comparing them directly between ticks.
- UMX invariants, if present, are not the primary signal.

**Inputs to UMX**
- UMX may be called as a helper or used only in tests.
- There may be no clear distinction between generic Gate inputs and UMX‑targeted inputs.

### 8.2 Gate responsibilities – AFTER (with UMX integration)

**Topology & routing**
- Gate **removes** any matrix‑like adjacency, neighbourhood and routing logic of its own.
- For matrix‑backed actors:
  - Gate calls UMX (Matrix State Frame API) to obtain nodes, edges and invariants.
  - Gate builds scene actors and bonds directly from that data.
- UMX/SLP + NAP own the actual movement of values across the lattice.

**Conservation & invariants**
- Gate’s conservation checks for matrix‑backed state become:
  - Read `UMX_SUM_BEFORE`, `UMX_SUM_AFTER`, `UMX_DELTA`, and other invariant integers from UMX.
  - Compare `UMX_DELTA` to TBP‑logged external Δ in the ingress ledger.
  - Quarantine/rollback ticks where invariants and TBP logs disagree.
- Gate no longer tries to reconstruct global conservation directly from ad‑hoc scene fields.

**Inputs to UMX**
- All UMX‑relevant input paths are explicitly labelled and schema‑checked as:
  - `UMX_TOPOLOGY_UPDATE`
  - `UMX_SIGNAL_INJECTION`
- Gate:
  - normalises them under TBP into integer‑only payloads,
  - wraps them in NAP envelopes,
  - dispatches them to UMX’s NAP Integration Module.

**What stays the same**
- Gate still:
  - acts as the membrane and projection layer,
  - owns the schema registry and TBP mapping for all external inputs,
  - composes the final scene and decides export formats,
  - enforces policy and quarantine decisions based on invariants and TBP rules.

This before/after view is intentionally narrow: it only affects Gate’s internal logic where it overlaps with matrix behaviour. Everywhere else (non‑UMX pillars, generic UI, logging), Gate’s behaviour remains as defined in the existing TBP/Gate packs.

### Source: `Umx Complement Doc H — Nap Integration (full).pdf` (PDF, extracted text)

--- Page 1 ---

Complement Doc H — Legacy NAP Reports: Stress
Tests, Nesting & Precision
This doc folds in everything  extra  the  older NAP / stacking reports  say that isn’t already covered in
Complement Doc G.
Sources used here:
Trinity NAP Stress Test Report  (both versions).
Sub-Planck Simulation Through Hierarchical Stacking .
Nesting Protocol (1) .
early nap v1  (Village/Town/City bridge set).
Trinity Relational Proof-of-Concept Report .
trinity_layer_precision_report .
(Plus light confirmation from the “Successful Test 01” docx.)
Where useful I mark:
v1 normative  — safe to treat as required behaviour now.
v2 / design-level  — clearly intended, but not yet wired into JS/UMX.
H.1 Stress Tests — Scaling, Failure Modes & What “Breaks” Look
Like
The NAP stress-test reports  push the architecture to large grids and deep stacks and then poke at where it
breaks.
H.1.1 Tested setups
The reports describe (examples):
Stable regime:  50×50 grid, 3 Trinity layers , full NAP + Loom + Press, modest lateral NAP fan-out →
stays numerically stable.
Edge regime:  100×100 grid, 5 Trinity layers , heavy lateral NAP broadcast between layers (dense
bus) → still mostly stable but reveals rounding noise and resonance .
H.1.2 Identified failure modes
Precision floor (float underflow):
In the original float-based prototypes, some budgets are tracked with 64-bit floats .• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
1. 
2. 
1


--- Page 2 ---

Near extreme scales, very small residuals  get crushed below machine epsilon → “phantom” budget
drift appears.
This manifests as tiny but systematic  μ drift over long runs.
Over-coupling / resonance loops:
When too many lateral NAP links  connect layers (e.g. every node in layer L broadcasting to every
peer in L+1 and back), the system can form feedback loops .
These loops amplify rounding noise  (even if each step is conservative in expectation) and show up
as low-frequency “breathing” oscillations in measures.
Entropy aliasing in compressed channels:
When Press/Loom compress time-series or summary packets aggressively and NAP re-injects them
frequently, pseudo-periodic noise  can appear:
repeated pattern of compressed residues that never fully die out,
looks like a “ringing” after a strong disturbance.
H.1.3 Interpretation for UMX/SLP v1
Because UMX v1 is integer-only , the precision floor  issue is mostly a historical cautionary tale :
v1 normative:
UMX/SLP/NAP/Press must not rely on IEEE float semantics  for conserved budgets.
Any budget/μ tracked at NAP level that must be exact must be represented in integers or rational
encodings  (e.g. scaled integers), not raw doubles.
Design-level / future guards:
Add stress-test hooks:
detect if cross-pillar compression + NAP routing are introducing persistent low-amplitude
oscillations  in μ,
flag over-coupling patterns (e.g. “too many” bus links between the same layers) as a health
warning .
H.2 Nesting Protocol & Stacked Simulations (Cross-Stack NAP Use)
The  Nesting_Protocol  (1)  and  Social  Mod  Stacking  reports  treat  NAP  as  the  glue  between  stacked
simulations :
One “outer” Trinity stack supervises many inner stacks  (or sims), each with its own UMX/SLP lattice.
NAP is used to exchange only summary information , not raw full state, between these stacked
layers.
H.2.1 Summary vectors / packets
From early nap v1  and the Nesting material:
Each lower-level region (e.g. Village / Town / City, or sub-sim) periodically outputs a packet :
Example (Village packet (O_V)) contents:
Counts (N_V).
Mean and variance of some feature (F): (\mu_F^V, \sigma_F^{2,V}).3. 
4. 
5. 
6. 
7. 
8. 
9. 
◦ 
◦ 
• 
• 
• 
• 
• 
◦ 
◦ 
• 
• 
• 
• 
◦ 
◦ 
2


--- Page 3 ---

Mean of another variable (R): (\mu_R^V).
Aggregated production vector over window: (\text{Prod}_V).
A synergy / interaction score (e.g. average over pairwise σ(α − distance)).
Event counts by type over the tick window.
The outer layer (Town/City or top sim) forms weighted aggregations  of these packets (e.g.
population-weighted sums) and uses them to update its own state.
v1 normative (as a **pattern **):
When NAP is used for stacked sim coupling , the default contract  is:
Lower layers send summary packets , not raw fields,
Packets contain counts, means, variances, and aggregates , all in integer / rational form,
Outer layers never directly mutate inner lattice cells ; they only change:
their own state, and/or
the parameters / boundary conditions that inner layers see on the next step.
H.2.2 NAP’s role in nesting
NAP is the carrier of these packets, enforcing:
tick alignment  between inner and outer layers (inner tick ratios (k_{VT}, k_{TC}) etc.),
budget and μ conservation  when information or resources cross stack boundaries,
deterministic idempotence (no double-applying the same packet).
Design-level tightening:
Define a “Nesting Profile”  on NAP that:
standardises summary packet structure (core fields like N, means, variances, windowed sums),
sets minimum tick ratio rules  (e.g. inner runs (k) ticks per outer tick),
guarantees that only summaries  are exposed; raw cell values never leave UMX via NAP in nested
modes.
H.3 Sub-Planck Stacking & Integer Scaling (ε Layers)
The Sub_Planck_Simulation_Through_Hierarchical_Stacking  report explains how sub-grid (“sub-Planck”)
detail  is represented by extra layers + residual scaling .
H.3.1 Cross-layer relation
Core equation (paraphrased):
Each higher-level layer (L+1) gets state:
[
s_{L+1} = f_L(s_L) + \varepsilon_L
]◦ 
◦ 
◦ 
◦ 
• 
• 
• 
• 
• 
◦ 
◦ 
• 
• 
• 
• 
• 
• 
• 
• 
• 
3


--- Page 4 ---

where: - (f_L) is a coarse summarisation  (e.g. block mean or other aggregator), - (\varepsilon_L = R(s_L -
\hat{s}_L)) is a  scaled integer residual , - (R) is a  fixed integer scaling factor  (e.g. 10⁶), ensuring the
residual is integer-encoded, - (\hat{s}_L) is the predicted/coarse reconstruction at layer L. - NAP ensures that
these ε terms are passed conservatively , so stacked sims preserve total μ.
H.3.2 What this adds for UMX/NAP
We already had residual layering  in Complement Docs E & F. The sub-Planck report adds:
v1 normative (safe, matches architecture):
Any “sub-grid” or “precision” layer that crosses stack boundaries via NAP must be:
expressed as integer residuals  (using a fixed R), and
tied to a clear anchor map  down to base UMX cells.
Design-level:
Define an explicit “ε-layer profile” :
R values per profile (e.g. 10³ for coarse, 10⁶ for fine),
maximum depth of residual stacks (how many ε levels are allowed),
rules for when ε_L is allowed to persist vs when it must be “folded back down” and re-
normalised.
H.4 Layer Precision & Error Behaviour (Legacy Float Prototype)
The trinity_layer_precision_report  gives a toy error table across 1–4 layers, showing:
Single layer: higher mean squared error (MSE) when approximating some target dynamics.
2–4 layers: progressively lower error , roughly exponential improvement.
At deeper stacks, error flattening as compression & rounding combine.
In the legacy system this was based on float arithmetic , but the shape  of the results is what matters:
Layered residuals  drastically reduce error ,
But error never completely vanishes — there is always some residual “noise” that moves around.
Implications for v1 integer UMX/NAP:
v1 normative (already aligned):
Treat each extra residual layer as a refinement of approximation , not as a guarantee of exactness.
UMX + NAP should never claim  “perfect reconstruction” beyond the integer lattice resolution; they
claim perfect replay  of whatever was encoded, not perfect modelling of the external world.
Design-level:
Add optional precision profiles  that:
give recommended depth of residual stacks for given tasks,
define budget thresholds where extra layers offer diminishing returns.• 
• 
◦ 
◦ 
• 
• 
◦ 
◦ 
◦ 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
◦ 
◦ 
4


--- Page 5 ---

H.5 Relational Proof-of-Concept — Summary Exchange Cadence
The Trinity Relational Proof-of-Concept Report  shows a small system:
One “relational” node watches two or more UMX domains,
It doesn’t see raw state; instead, every 5 ticks  each domain sends:
mean state of selected fields,
residual magnitudes or other simple stats.
NAP coupling behaviour:
Mean & residual summaries are exchanged on a fixed cadence  (e.g. every 5 ticks),
Nodes update based only on these aggregates, preserving deterministic reproducibility.
v1 normative pattern:
When NAP is used for relational supervision  (e.g. meta-monitors, dashboards, Codex watchers):
Exchanges should happen on fixed, declared cadences  (e.g. every N ticks), not on ad-hoc events,
Payloads should be simple aggregates  (mean, variance, counts, norms), not arbitrary scripts,
These exchanges must not inject new μ ; they’re read-only from the perspective of the budget.
This gives you a clean separation:
UMX/SLP = physics,
NAP relational monitors = “read the physics by summary” without perturbing it, unless a specific
write is agreed via SEAL.
H.6 How H Relates to Complement Doc G
Complement Doc G already covered:
NAP’s envelope model, ports, idempotence, global tick, causal barrier , MDL consensus, SEAL, U-
Ledger , budgets.
This Doc H  adds:
Scaling constraints:  why we insist on integer budgets and how over-coupling / compression loops
can cause resonance.
Nesting semantics:  summary-packet-only coupling between stacked sims (Village/Town/City
pattern).
Sub-Planck ε layers:  explicit integer-scaled residual layers crossing stacks via NAP.
Relational cadence:  fixed-cadence summary exchange patterns for relational monitors.
Design-level profiles:  suggestions for Nesting Profile, ε-layer profile, and precision/stress profiles
that haven’t yet been formalised.• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
5


--- Page 6 ---

Gap Map H — New Gaps Exposed by Legacy NAP / Stacking Reports
Relative to A–G, these older reports introduce a few extra holes.
H1. Summary Packet Schema for Stacked Sims
Docs:  early nap v1, Nesting Protocol, social stacking reports.
Gap:  No canonical schema  for cross-stack summary packets (O_V, O_T, etc.) in the main spec.
Need:  A Summary Packet v1  definition:
core fields (counts, mean/variance of key fields, windowed production vectors, synergy scores, event
counts),
encoding rules (all integer / rational),
tick window semantics (how many ticks each packet covers).
H2. ε-Layer Profile & Scaling Factor R
Docs:  Sub-Planck stacking report.
Gap:  No explicit R values or max residual depth in spec; ε layers are conceptually described but not
parameterised.
Need:  An ε-Layer Profile Annex :
recommended R values,
maximum ε depth per profile,
rules for folding residuals back into base layers or rescaling when they get too large.
H3. Over-Coupling Detection & Resonance Guards
Docs:  NAP stress tests (resonance loops with too many lateral links).
Gap:  No spec’d diagnostic or guardrails  for NAP over-coupling (bus too dense between certain
layers).
Need:
A simple over-coupling heuristic  (e.g. max NAP degree / fan-out per node per layer),
optional health checks : watch μ variance over time; flag persistent oscillation at small amplitudes.
H4. Integer vs Float Budget Discipline at NAP Level
Docs:  Stress tests and layer precision report (legacy floats).
Gap:  Main spec doesn’t explicitly ban floats  for budgets; it just says UMX is integer .
Need:  A norm like:
“All budget / μ-like quantities shared across pillars (UMX/NAP/Loom/Press/TGP) MUST
be represented as integers or exact rational encodings. Float representations may be
used for internal approximations but not as the authoritative source of truth.”• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
6


--- Page 7 ---

H5. Relational Monitor Cadence & Permissions
Docs:  Relational PoC report (summary exchange every N ticks, no direct mutation).
Gap:  No explicit rule on cadence  for relational NAP traffic or on mutation rights.
Need:  A small Relational NAP Profile :
fixed cadences,
allowed payload types,
whether monitor nodes are read-only vs allowed to submit SEAL’d writes.
H6. Nesting Profile & Tick Ratios
Docs:  early nap v1 (Village/Town/City ratios k_VT, k_TC), Nesting report.
Gap:  UMX/NAP spec doesn’t mandate how inner/outer tick ratios  are wired for nested sims.
Need:
A Nesting Profile  that:
states allowable ratios,
defines when inner stacks are allowed to “run ahead” vs must stay tightly coupled,
clarifies how NAP enforces tick alignment in presence of different step sizes.• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
◦ 
◦ 
◦ 
7

### Source: `integration/umx_commit_and_snapshot_manifests_v1.md` (verbatim)

---
id: umx_commit_and_snapshot_manifests_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Commit & Snapshot Manifests v1

Per-tick commit manifests and periodic snapshot manifests, and their relation to I/P-blocks.

### Source: `integration/umx_nap_bus_contract_v1.md` (verbatim)

---
id: umx_nap_bus_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX NAP Bus Contract v1

Envelope schema, idempotence, exactly-once, ordering/causality, budgets, backpressure, dead-letter, isolation, and testbed properties.

### Source: `integration/umx_node_manifest_v1.md` (verbatim)

---
id: umx_node_manifest_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Node Manifest v1

Node, edge and region tables and invariants for UMX substrate topology.

### Source: `integration/umx_slp_snapshot_ir_v1.md` (verbatim)

---
id: umx_slp_snapshot_ir_v1
version: 1.0-draft
status: normative
pillar: UMX/SLP
created: 2025-11-16
---

# UMX SLP Snapshot IR v1

Defines per-tick snapshot content produced by SLP and consumed by UMX.

### Source: `integration/umx_two_phase_tick_contract_v1.md` (verbatim)

---
id: umx_two_phase_tick_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX Two-Phase Tick Contract v1

Read/compute (Phase A) and commit/emit (Phase B) behaviour for UMX within the global pipeline, including sub-tick considerations.

### Source: `integration/umx_u_ledger_contract_v1.md` (verbatim)

---
id: umx_u_ledger_contract_v1
version: 1.0-draft
status: normative
pillar: UMX
created: 2025-11-16
---

# UMX U-Ledger Contract v1

Ledger row fields, I/P alignment, and replay properties (reversible_ok, checkpoint_spacing_ok, etc.).

## Part 7 — TBP: Implementation Spec, Roadmap, Verification, Golden Fixtures, Runbook

### Source: `tbp/tbp_umx_development_roadmap_v_1.md` (verbatim)

---
id: tbp_umx_development_roadmap_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Development Roadmap v1

Phases P0..P4 with goals, key tasks, and exit criteria, aligned with the Full Buildplan.

### Source: `tbp/tbp_umx_golden_fixtures_pack_v_1.md` (verbatim)

---
id: tbp_umx_golden_fixtures_pack_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Golden Fixtures Pack v1

Describes fixture families F01..F04, their intent, and how Golden TSVs are produced and maintained for regression.

### Source: `tbp/tbp_umx_implementation_spec_v_1.md` (verbatim)

---
id: tbp_umx_implementation_spec_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Implementation Spec v1

Runtime model: pure-math core + JS shell; deterministic; paper-first; TSV-based I/O. Modules M1–M9 map to implementation units.

### Source: `tbp/tbp_umx_operator_runbook_v_1.md` (verbatim)

---
id: tbp_umx_operator_runbook_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Operator Runbook v1

Operator workflows: pre-run checks, running scenarios, kill/quarantine controls, exporting TSVs, and handling failed properties.

### Source: `tbp/tbp_umx_verification_plan_fixtures_crosswalk_v_1.md` (verbatim)

---
id: tbp_umx_verification_plan_fixtures_crosswalk_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Verification Plan / Fixtures Crosswalk v1

Template for linking verification objectives to fixtures/scenarios and MAX test properties.

### Source: `tbp/tbp_umx_verification_test_plan_v_1.md` (verbatim)

---
id: tbp_umx_verification_test_plan_v_1
version: 1.0-draft
status: guiding
pillar: UMX
created: 2025-11-16
---

# TBP–UMX Verification Test Plan v1

Defines unit, integration and system test categories mapped to UMX fixtures and MAX properties.

### Source: `umx_fixtures_testbed_integration_pack_2025_11_17.md` (verbatim)

---
id: umx_fixtures_and_testbed_pack_v1
version: 1.0-draft
status: normative-shell
pillar: UMX
created: 2025-11-17
---

# UMX Fixtures & Testbed Integration Pack v1

## 0. Purpose and Scope

This document defines the **Golden Fixtures** and **testbed integration layout** for the Universal Matrix (UMX) pillar.

It:

- Specifies the **fixture families** and individual fixture IDs for UMX v1.
- Defines the **table schemas** and file layout used to represent UMX fixtures and scenario outputs in the Aether Paper Testbed.
- Describes how fixtures map to **scenario IDs (Sxx)** and to **MAX properties**.
- Provides enough detail for an engineer to assemble the fixtures and wire them into the existing Testbed MASTER bundle without guessing.

This pack is designed to sit under the `fixtures/` and `testbed/` directories of the `UMX_Spec_Pack_v1_YYYY-MM-DD.zip` described in the UMX Spec Master Index.

---

## 1. Directory and File Layout

### 1.1 Top-Level Layout

Within the UMX Spec Pack ZIP, fixtures and testbed integration are laid out as:

- `fixtures/UMX/`
  - `fixtures_index.tsv`
  - `golden/`
    - `F01_MINIMAL_TOPOLOGY/`
    - `F02_RESIDUAL_EPSILON/`
    - `F03_PROFILE_MDL/`
    - `F04_STRESS_SAFETY/`
- `testbed/UMX/`
  - `S01_UMX_MINIMAL/`
  - `S02_UMX_RESIDUAL_EPSILON/`
  - `S03_UMX_PROFILE_MDL/`
  - `S04_UMX_STRESS_SAFETY/`

Fixtures under `fixtures/UMX/golden/` are **small, self-contained** configurations that can be loaded directly by a developer or by the Testbed harness. The corresponding `testbed/UMX/Sxx_...` directories define the **scenario-level tables** that the Aether Testbed consumes when running property checks.

### 1.2 Naming Conventions

- Fixture IDs follow the pattern `FNN_NAME`, where `NN` is a two-digit integer starting at `01` and `NAME` is a short descriptor.
- Scenario IDs follow the pattern `SNN_UMX_NAME`, where `NN` matches the fixture index for Golden Fixtures.
- File names under each fixture or scenario directory are **fixed** as described in the schemas below. No additional arbitrary files are included in v1.

---

## 2. Common Table Schemas

This section defines **shared table schemas** used across all UMX fixtures and scenarios. These are deliberately simple and closely mirror the structures described in the UMX spec artefacts.

All tables are assumed to be TSV (tab-separated values) encoded as plain text, with a header row naming columns exactly as specified.

### 2.1 `fixtures_index.tsv`

The `fixtures_index.tsv` file in `fixtures/UMX/` lists all Golden Fixtures.

Columns:

1. `fixture_id` — string; for Golden Fixtures: `F01_MINIMAL_TOPOLOGY`, `F02_RESIDUAL_EPSILON`, `F03_PROFILE_MDL`, `F04_STRESS_SAFETY`.
2. `family` — string; one of `minimal`, `residual_epsilon`, `profile_mdl`, `stress_safety`.
3. `scenario_id` — string; matching the scenario in `testbed/UMX/` (for v1: `S01_UMX_MINIMAL`, `S02_UMX_RESIDUAL_EPSILON`, `S03_UMX_PROFILE_MDL`, `S04_UMX_STRESS_SAFETY`).
4. `description` — short human-readable description of the fixture.
5. `status` — string; one of `draft`, `ready`, `deprecated`. For initial Golden Fixtures v1 this is `ready`.

No additional columns are present in v1.

### 2.2 Node Table Schema

Used in both fixtures and testbed scenarios to describe the node set.

Filename pattern:

- For fixture: `nodes.tsv` under `fixtures/UMX/golden/FNN_.../`.
- For scenario: `nodes.tsv` under `testbed/UMX/SNN_.../`.

Columns:

1. `scenario_id` — string; scenario identifier (e.g. `S01_UMX_MINIMAL`).
2. `node_id` — string; unique node identifier within the scenario (e.g. `N1`, `N2`).
3. `layerId` — integer; layer index as per `umx_layers_policy_v1.md` (v1 Golden Fixtures use `0` only).
4. `region_id` — string; region identifier (e.g. `R_MAIN`, `R_ISO1`).
5. `node_type` — string; role of the node (e.g. `compute`, `sensor`, `aggregator`).
6. `capacity` — integer; maximum number of messages per tick this node is intended to handle under normal conditions.
7. `flags` — string; comma-separated tags such as `boundary`, `root`, `stress_target`. Empty string if no flags.
8. `coord_x` — integer; x-coordinate in the shared spatial frame (or abstract index). For v1 fixtures, may be small integers such as `0`, `1`, `2`.
9. `coord_y` — integer; y-coordinate in the shared spatial frame. For v1 fixtures, may be small integers such as `0`, `0`, `0` for a line.

No other columns are defined for v1 Golden Fixtures.

### 2.3 Edge Table Schema

Edges describe connectivity between nodes.

Filename pattern:

- For fixture: `edges.tsv`.
- For scenario: `edges.tsv`.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `edge_id` — string; unique identifier for the edge within the scenario (e.g. `E1`, `E2`).
3. `from_node_id` — string; node_id of the source node.
4. `to_node_id` — string; node_id of the target node.
5. `layer_relation` — string; one of `same`, `up`, `down`, indicating relationship between `layerId` of the nodes.
6. `weight` — integer; weight or ley strength proxy for routing decisions (v1 fixtures use small integers such as `1` or `2`).
7. `capacity` — integer; message capacity for this edge per tick.
8. `flags` — string; tags such as `backbone`, `local`, `cross_region`, `stress_target`.

### 2.4 Profile Table Schema

Profiles control UMX behaviour in fixtures and scenarios. For Golden Fixtures, we provide a compact profile table that aligns with `umx_profile_v1.md`.

Filename pattern:

- `profile.tsv` under each fixture and scenario directory.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `profile_id` — string; profile identifier (e.g. `P_UMX_MINIMAL_V1`).
3. `tick_max_nodes` — integer; maps to `tick.max_nodes` in `umx_profile_v1.md`.
4. `tick_max_degree` — integer; maps to `tick.max_degree`.
5. `mdl_window_ticks` — integer; maps to `mdl.window_ticks`.
6. `mdl_tau` — integer; maps to `mdl.tau`.
7. `residual_max_norm` — integer; maps to `residual.max_norm`.
8. `residual_warning_ratio_num` — integer numerator for `residual.warning_ratio`.
9. `residual_warning_ratio_den` — integer denominator for `residual.warning_ratio` (for rational representation, e.g. `3/4`).
10. `nap_msg_budget` — integer; maps to `nap.msg_budget`.
11. `nap_byte_budget` — integer; maps to `nap.byte_budget`.
12. `nap_soft_tolerance_num` — integer numerator for `nap.soft_tolerance`.
13. `nap_soft_tolerance_den` — integer denominator for `nap.soft_tolerance`.
14. `nap_hard_tolerance` — integer; absolute threshold for `nap.hard_tolerance`.
15. `ledger_retention_ticks` — integer; maps to `ledger.retention_ticks`.
16. `ledger_snapshot_interval` — integer; maps to `ledger.snapshot_interval`.
17. `ledger_reversibility_window` — integer; maps to `ledger.reversibility_window`.
18. `layers_max_layers` — integer; maps to `layers.max_layers`.
19. `layers_cadences` — string; e.g. `0:1` for a single layer with `k_0 = 1`.
20. `emergence_epsilon_drift` — integer; maps to `emergence.epsilon_drift`.
21. `calibration_status` — string; one of `GO`, `HOLD`, `KILL`.

This compact profile table is sufficient for Golden Fixtures and scenarios; real profiles may be expanded into dedicated profile documents as needed.

### 2.5 Residual and Epsilon Table Schema

Residual and epsilon entries are represented in a combined table for simplicity.

Filename pattern:

- `residual_epsilon.tsv`.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `tick` — integer; tick index.
3. `node_id` — string; node to which this entry applies.
4. `anchor_tick_ref` — integer; reference tick for the base anchor.
5. `anchor_layer` — integer; usually `0` for base layer.
6. `component` — string; component name or index (e.g. `v`, `w`, `r1`).
7. `residual_value` — integer; residual value at this tick for the component.
8. `epsilon_delta` — integer; epsilon correction for this component at this tick. Zero if no epsilon is applied.
9. `reason_code` — string; reason for epsilon (e.g. `NONE`, `FLOAT_DRIFT`, `QUANT_CLAMP`).

### 2.6 Drift Metrics Table Schema

Drift metrics summarise behaviour over windows.

Filename pattern:

- `drift_metrics.tsv`.

Columns:

1. `scenario_id` — string.
2. `window_id` — string; identifier for the window (e.g. `W1_TICKS_1_10`).
3. `window_start_tick` — integer.
4. `window_end_tick` — integer.
5. `node_id` — string or special value `GLOBAL` for global drift.
6. `delta_value` — integer; \(\Delta_i(W)\) or \(\Delta(W)\) depending on `node_id`.
7. `band` — string; one of `PASS`, `INVESTIGATE`, `FAIL` (for convenience). For `node_id = GLOBAL`, this matches the emergence band definitions.

### 2.7 Events Table Schema

Events capture noteworthy occurrences such as kill-switch activation, drift guard triggers, budget overruns and backpressure signals.

Filename pattern:

- `events.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer.
3. `event_id` — string; unique per event.
4. `event_type` — string; examples include `KILL_SWITCH`, `DRIFT_GUARD_ACTIVATED`, `BUDGET_SOFT_OVERRUN`, `BUDGET_HARD_OVERRUN`, `BACKPRESSURE_SIGNAL_SENT`.
5. `scope_type` — string; one of `NODE`, `REGION`, `SYSTEM`.
6. `scope_id` — string; node_id, region_id or `GLOBAL` depending on `scope_type`.
7. `reason_code` — string; short code explaining the cause (e.g. `OPERATOR`, `AUTOMATIC_DRIFT`, `AUTOMATIC_BUDGET`).

### 2.8 NAP Envelopes Table Schema

For scenarios that involve NAP interaction, envelopes are described explicitly.

Filename pattern:

- `nap_envelopes.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer; tick when the envelope is visible to UMX.
3. `envelope_id` — string; unique identifier for the envelope.
4. `id_key_seed` — string; seed from which envelope identity can be derived.
5. `source_pillar` — string (e.g. `EXTERNAL`, `UMX`, `OTHER_PILLAR`).
6. `target_pillar` — string (here always `UMX` or occasionally other pillars for outbound rows).
7. `region_id` — string; target region.
8. `intent_type` — string; e.g. `WRITE_STATE`, `APPLY_DELTA`, `INJECT_SIGNAL`, `QUERY_STATE`, `STATUS_UPDATE`.
9. `schema_id` — string; payload schema identifier.
10. `nonce` — string; idempotence token.
11. `priority` — integer; relative priority for routing.
12. `payload_bytes` — integer; size of payload in bytes to support budget calculations.
13. `applied` — boolean; `TRUE` if applied, `FALSE` if rejected or dead-lettered.
14. `dead_letter` — boolean; `TRUE` if this envelope was placed in dead-letter store.

### 2.9 Ledger Table Schema

The ledger table records per-tick summary metrics and references to manifests.

Filename pattern:

- `ledger.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer.
3. `profile_id` — string.
4. `changeset_id` — string; reference to Commit Manifest entry.
5. `snapshot_id` — string; reference to Snapshot Manifest if a snapshot occurs at this tick, otherwise empty.
6. `is_I_block` — boolean; `TRUE` if this tick corresponds to an I-block.
7. `drift_global` — integer; global drift value for this tick or cumulative up to this tick (fixture-specific definition must be documented).
8. `budget_usage_msg` — integer; number of messages processed in this tick.
9. `budget_usage_bytes` — integer; total payload bytes processed in this tick.
10. `kill_switch_flag` — boolean; `TRUE` if kill-switch is active at end of this tick.
11. `quarantine_flag` — boolean; `TRUE` if scenario or region is under quarantine at this tick.

### 2.10 Assertions Table Schema

The assertions table expresses MAX properties as expected vs actual values for each scenario.

Filename pattern:

- `assertions.tsv`.

Columns:

1. `scenario_id` — string.
2. `property_name` — string; property code such as `drift_guard_ok`, `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `kill_switch_ok`, `reversible_ok`, `skip_ahead_ok`, `skip_back_ok`.
3. `expected` — string; expected result, usually `TRUE`, `FALSE`, `PASS`, `INVESTIGATE` or `FAIL` depending on property type.
4. `actual` — string; actual result produced when the scenario is run and evaluated.
5. `result` — string; one of `PASS`, `FAIL`, `INVESTIGATE`. For Golden Fixtures this is usually `PASS`.
6. `notes` — string; short comment, may be empty.

---

## 3. Golden Fixtures Definitions

This section defines the four Golden Fixtures for UMX v1. Each fixture description specifies:

- Fixture ID and scenario ID,
- Intent and properties under test,
- Tables that must be populated,
- Qualitative structure of the data (without fixing every numeric value, which is left to concrete fixture files).

### 3.1 Fixture F01 — Minimal Topology

- `fixture_id`: `F01_MINIMAL_TOPOLOGY`
- `scenario_id`: `S01_UMX_MINIMAL`
- Family: `minimal`

#### 3.1.1 Intent

Provide a **smallest useful UMX configuration** to validate:

- Node and edge tables,
- Basic tick operation without residuals or epsilon layers,
- Conservation and determinism for a trivial case.

#### 3.1.2 Structure

- Node count: 3 nodes (`N1`, `N2`, `N3`).
- Layer configuration: single layer (`layerId = 0` for all nodes).
- Regions: single region (`R_MAIN`).
- Edges: at least two edges forming a simple path (`N1 → N2 → N3`).
- Capacities: small integer capacities (for example, `capacity = 10` for nodes and `capacity = 10` for edges), within `tick_max_nodes` and `tick_max_degree` constraints.

#### 3.1.3 Tables

Populate at minimum:

- `nodes.tsv` — three rows for `N1`, `N2`, `N3` with `layerId = 0`, `region_id = R_MAIN`, simple coordinates such as `(0,0)`, `(1,0)`, `(2,0)`.
- `edges.tsv` — rows for `E1: N1→N2`, `E2: N2→N3` with `layer_relation = same`.
- `profile.tsv` — a profile `P_UMX_MINIMAL_V1` with:
  - `tick_max_nodes` ≥ 3,
  - `tick_max_degree` ≥ 2,
  - `mdl_window_ticks` set to a small value such as 5,
  - residual and emergence settings that allow trivial drift (for example, `residual_max_norm = 0`, `emergence_epsilon_drift = 0`).
- `residual_epsilon.tsv` — all zeros; no residuals or epsilon corrections.
- `drift_metrics.tsv` — drift values of zero for all nodes and for global drift, band `PASS`.
- `ledger.tsv` — a short sequence of ticks (for example, ticks 1–5) with stable metrics and no kill-switch or quarantine flags.
- `assertions.tsv` — at minimum, properties:
  - `reversible_ok` expected `TRUE`,
  - `drift_guard_ok` expected `TRUE`,
  - `routing_capacity_ok` expected `TRUE` (since traffic is below capacity).

### 3.2 Fixture F02 — Residual and Epsilon

- `fixture_id`: `F02_RESIDUAL_EPSILON`
- `scenario_id`: `S02_UMX_RESIDUAL_EPSILON`
- Family: `residual_epsilon`

#### 3.2.1 Intent

Demonstrate **non-zero residuals and sparse epsilon corrections** in a controlled, small graph, and validate drift metrics and emergence bands.

#### 3.2.2 Structure

- Node count: 3–4 nodes in a slightly more connected graph (for example, a triangle or a small hub).
- Residual behaviour: at least one node experiences deterministic non-zero residuals over a defined window.
- Epsilon behaviour: a small number of epsilon corrections are applied to keep drift within bounds or to enforce bit-exact replay.

#### 3.2.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — as for F01, but with a topology that produces more interesting residual patterns.
- `profile.tsv` — a profile `P_UMX_RESIDUAL_EPSILON_V1` with:
  - `residual_max_norm` set to a small integer such as 5,
  - `emergence_epsilon_drift` set to a non-zero value such as 2,
  - other fields chosen to exercise drift computations.
- `residual_epsilon.tsv` — multiple ticks with:
  - non-zero `residual_value` for at least one node and component,
  - non-zero `epsilon_delta` entries for a subset of those residuals.
- `drift_metrics.tsv` — per-node and global drift values that:
  - include both zero and non-zero drift windows,
  - produce at least one `INVESTIGATE` band according to `umx_emergence_bands_v1.md`.
- `ledger.tsv` — ticks that show how residuals and epsilon corrections evolve over time.
- `assertions.tsv` — properties including:
  - `drift_guard_ok` expected `TRUE` (drift guards behave according to configuration),
  - `orthogonal_residuals_ok` expected `TRUE` where applicable,
  - `entropy_bound_ok` expected `TRUE`.

### 3.3 Fixture F03 — Profile and MDL

- `fixture_id`: `F03_PROFILE_MDL`
- `scenario_id`: `S03_UMX_PROFILE_MDL`
- Family: `profile_mdl`

#### 3.3.1 Intent

Exercise **profile-controlled MDL behaviour** by defining structural or SLP proposals that are accepted or rejected according to the MDL objective.

#### 3.3.2 Structure

- Node and edge topology: small graph where adding or removing an edge has a measurable effect on the MDL codelength.
- Proposals: at least two proposals over a window:
  - One that improves MDL sufficiently and should be accepted (\(\Delta L \le -\tau\)).
  - One that does not (\(\Delta L > -\tau\)) and should be rejected.

#### 3.3.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — as needed for the MDL scenario.
- `profile.tsv` — a profile `P_UMX_PROFILE_MDL_V1` with:
  - `mdl_window_ticks` chosen to include the proposal window (for example, 10),
  - `mdl_tau` chosen so that one proposal meets the threshold and one does not.
- `residual_epsilon.tsv` — traces sufficient to compute MDL codelengths for baseline and candidate models.
- `ledger.tsv` — ticks where MDL proposals are evaluated, with `changeset_id` and MDL summary metrics.
- `events.tsv` — entries for proposal evaluations if they are treated as explicit events.
- `assertions.tsv` — properties including:
  - MDL-related property (for example, `mdl_acceptance_ok`) expected `TRUE`,
  - Checks that for accepted proposals `delta_mdl ≤ -tau` and for rejected proposals `delta_mdl > -tau`.

### 3.4 Fixture F04 — Stress and Safety

- `fixture_id`: `F04_STRESS_SAFETY`
- `scenario_id`: `S04_UMX_STRESS_SAFETY`
- Family: `stress_safety`

#### 3.4.1 Intent

Exercise **stress, budgets, backpressure, kill-switch and quarantine** behaviours in a compact scenario.

#### 3.4.2 Structure

- Node and edge topology: small network with at least two regions:
  - Main region (`R_MAIN`) where high load is applied.
  - Isolated region (`R_ISO1`) used to test isolation and quarantine.
- NAP envelopes: traffic configured to approach and exceed budget thresholds in `R_MAIN`, while leaving `R_ISO1` within normal bounds.
- Kill-switch: at least one kill-switch activation event (scope `REGION` or `SYSTEM`).
- Quarantine: at least one region or scenario-level quarantine flag.

#### 3.4.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — describing regions `R_MAIN` and `R_ISO1` and their connectivity.
- `profile.tsv` — profile `P_UMX_STRESS_SAFETY_V1` with budgets configured to make overruns likely under the chosen envelopes.
- `nap_envelopes.tsv` — a sequence of envelopes that:
  - cause soft budget overruns (trigger backpressure but not kill-switch),
  - cause hard budget overruns,
  - include at least one envelope routed to a non-existent target to exercise dead-letter behaviour.
- `events.tsv` — entries for:
  - budget soft and hard overruns,
  - backpressure signals,
  - kill-switch activation,
  - quarantine activation.
- `ledger.tsv` — ticks showing budget usage, drift, kill-switch flag and quarantine flag.
- `assertions.tsv` — properties including:
  - `routing_capacity_ok` expected `TRUE` or `FALSE` depending on scenario design,
  - `back_pressure_ok` expected `TRUE` (backpressure behaves as configured),
  - `dead_letter_empty` expected `FALSE` for this fixture (since misrouted messages are deliberately injected),
  - `isolation_ok` expected `TRUE` (issues in `R_MAIN` do not corrupt `R_ISO1`),
  - `kill_switch_ok` expected `TRUE`,
  - `quarantine_flag` used as expected.

---

## 4. Mapping Fixtures to MAX Properties

This section provides a high-level mapping from Golden Fixtures to MAX properties for UMX.

### 4.1 Fixture F01 — Minimal Topology

Primarily covers:

- `reversible_ok` — simple replay and rollback over a small number of ticks.
- `checkpoint_spacing_ok` — if snapshots are included.
- `drift_guard_ok` — in the trivial case where drift is zero.

### 4.2 Fixture F02 — Residual and Epsilon

Primarily covers:

- `drift_guard_ok` — non-trivial drift and epsilon usage.
- `orthogonal_residuals_ok` — where orthogonality definitions are applied.
- `entropy_bound_ok` — ensuring residuals and epsilon corrections do not violate entropy constraints.

### 4.3 Fixture F03 — Profile and MDL

Primarily covers:

- MDL acceptance behaviour and any derived property such as `mdl_acceptance_ok`.
- Correct consumption of `umx_profile_v1` fields controlling MDL.

### 4.4 Fixture F04 — Stress and Safety

Primarily covers:

- `routing_capacity_ok` — under high load.
- `back_pressure_ok` — under soft and hard overruns.
- `dead_letter_empty` — expected `FALSE` for this fixture.
- `isolation_ok` — isolation between regions.
- `kill_switch_ok` — scope and determinism of kill-switch.
- `drift_guard_ok` — interaction between stress and drift guards.

---

## 5. Usage in Aether Paper Testbed

### 5.1 Loading Fixtures

For each Golden Fixture:

1. Load `nodes.tsv`, `edges.tsv` and `profile.tsv` into the testbed scenario configuration.
2. Load `residual_epsilon.tsv`, `drift_metrics.tsv`, `nap_envelopes.tsv`, `events.tsv` and `ledger.tsv` as the corresponding data tables for that scenario.
3. Load `assertions.tsv` as the list of properties to evaluate.

### 5.2 Running Properties

The Testbed evaluates each property in `assertions.tsv` by:

- Reading the required tables as specified in the UMX spec artefacts and MAX definitions.
- Computing expected booleans or bands.
- Comparing against `expected` and populating `actual` and `result` fields.

Golden Fixtures v1 are expected to pass all listed properties for their scenarios under a conformant UMX implementation.

### 5.3 Runtime Integration

When a runtime UMX implementation is integrated with the testbed:

1. The runtime loads the same `nodes.tsv`, `edges.tsv` and `profile.tsv` as initial configuration.
2. The runtime executes the scenario (either by reading `nap_envelopes.tsv` as input or by generating equivalent envelopes).
3. The runtime exports its own `residual_epsilon.tsv`, `drift_metrics.tsv`, `events.tsv`, `nap_envelopes.tsv` (for outbound messages) and `ledger.tsv`.
4. The Testbed compares runtime outputs against the Golden Fixture expectations where applicable, and then evaluates properties.

A runtime is considered conformant for a fixture when there are no unexplained differences in the tables that affect property evaluation and when all properties in `assertions.tsv` have `result = PASS`.

---

## 6. Versioning and Extension

This pack defines **UMX Golden Fixtures v1** and the associated testbed integration layout.

Future versions may:

- Add new fixtures (for example F05 for multi-layer behaviour),
- Add additional properties to `assertions.tsv`,
- Refine table schemas with extra columns while keeping existing columns stable.

All such changes must:

- Increment the `version` in this document and in any affected fixture manifests,
- Preserve backwards compatibility for existing v1 fixtures whenever possible,
- Be reflected in the UMX Spec Master Index and TBP verification crosswalk.

This completes the UMX Fixtures & Testbed Integration Pack v1 specification.

### Source: `testbed/UMX/UMX_Fixtures_and_Testbed_Integration_Pack_v1.md` (verbatim)

---
id: umx_fixtures_and_testbed_pack_v1
version: 1.0-draft
status: normative-shell
pillar: UMX
created: 2025-11-17
---

# UMX Fixtures & Testbed Integration Pack v1

## Layout

- fixtures/UMX/fixtures_index.tsv
- fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/…
- fixtures/UMX/golden/F02_RESIDUAL_EPSILON/…
- fixtures/UMX/golden/F03_PROFILE_MDL/… (provisional_mdl)
- fixtures/UMX/golden/F04_STRESS_SAFETY/…
- testbed/UMX/S01_UMX_MINIMAL/… (and S02..S04)

## Common TSV Schemas

- nodes.tsv: scenario_id, node_id, layerId, region_id, node_type, capacity, flags, coord_x, coord_y
- edges.tsv: scenario_id, edge_id, from_node_id, to_node_id, layer_relation, weight, capacity, flags
- profile.tsv: scenario_id, profile_id, tick_max_nodes, tick_max_degree, mdl_window_ticks, mdl_tau, residual_max_norm, residual_warning_ratio_num, residual_warning_ratio_den, nap_msg_budget, nap_byte_budget, nap_soft_tolerance_num, nap_soft_tolerance_den, nap_hard_tolerance, ledger_retention_ticks, ledger_snapshot_interval, ledger_reversibility_window, layers_max_layers, layers_cadences, emergence_epsilon_drift, calibration_status
- residual_epsilon.tsv: scenario_id, tick, node_id, anchor_tick_ref, anchor_layer, component, residual_value, epsilon_delta, reason_code
- drift_metrics.tsv: scenario_id, window_id, window_start_tick, window_end_tick, node_id, delta_value, band
- events.tsv: scenario_id, tick, event_id, event_type, scope_type, scope_id, reason_code
- nap_envelopes.tsv: scenario_id, tick, envelope_id, id_key_seed, source_pillar, target_pillar, region_id, intent_type, schema_id, nonce, priority, payload_bytes, applied, dead_letter
- ledger.tsv: scenario_id, tick, profile_id, changeset_id, snapshot_id, is_I_block, drift_global, budget_usage_msg, budget_usage_bytes, kill_switch_flag, quarantine_flag
- assertions.tsv: scenario_id, property_name, expected, actual, result, notes

## Golden Fixtures Intent

- F01 Minimal: 3 nodes, line graph, single region, zero residuals/epsilon; PASS bands; reversible & checkpoints validated.
- F02 Residual/Epsilon: non-zero residuals, sparse epsilon; INVESTIGATE window.
- F03 Profile/MDL: two proposals (accept/reject) — provisional_mdl until companion spec.
- F04 Stress/Safety: budgets, backpressure, dead-letter, isolation, kill-switch & quarantine; properties exercised.

## Part 8 — Testbed Scenarios and TSV Fixture Schemas

The following TSV fixtures are included in the UMX maximal pack. For each file we list its path, header columns, total rows (excluding header), and a small sample to make the schema fully explicit.

### Fixture: `fixtures/UMX/fixtures_index.tsv`

- **Header columns (5)**: `fixture_id`, `family`, `scenario_id`, `description`, `status`
- **Data rows**: 4

Sample rows:

| fixture_id | family | scenario_id | description | status |
| --- | --- | --- | --- | --- |
| F01_MINIMAL_TOPOLOGY | minimal | S01_UMX_MINIMAL | 3-node, single-layer, single-region minimal topology with zero residuals/epsilon; drift PASS. | ready |
| F02_RESIDUAL_EPSILON | residual_epsilon | S02_UMX_RESIDUAL_EPSILON | Small graph with non-zero residuals and sparse epsilon; drift includes INVESTIGATE. | ready |
| F03_PROFILE_MDL | profile_mdl | S03_UMX_PROFILE_MDL | MDL proposals: one accepted, one rejected; provisional_mdl until MDL companion spec is final. | provisional |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/assertions.tsv`

- **Header columns (6)**: `scenario_id`, `property_name`, `expected`, `actual`, `result`, `notes`
- **Data rows**: 8

Sample rows:

| scenario_id | property_name | expected | actual | result | notes |
| --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | reversible_ok | TRUE | TRUE | PASS | F01 minimal reversible |
| S01_UMX_MINIMAL | checkpoint_spacing_ok | TRUE | TRUE | PASS | Snapshots at ticks 1 and 5 |
| S01_UMX_MINIMAL | drift_guard_ok | TRUE | TRUE | PASS | Zero drift |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/drift_metrics.tsv`

- **Header columns (7)**: `scenario_id`, `window_id`, `window_start_tick`, `window_end_tick`, `node_id`, `delta_value`, `band`
- **Data rows**: 4

Sample rows:

| scenario_id | window_id | window_start_tick | window_end_tick | node_id | delta_value | band |
| --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | GLOBAL | 0 | PASS |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | N1 | 0 | PASS |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | N2 | 0 | PASS |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/edges.tsv`

- **Header columns (8)**: `scenario_id`, `edge_id`, `from_node_id`, `to_node_id`, `layer_relation`, `weight`, `capacity`, `flags`
- **Data rows**: 2

Sample rows:

| scenario_id | edge_id | from_node_id | to_node_id | layer_relation | weight | capacity | flags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | E1 | N1 | N2 | same | 1 | 10 | local |
| S01_UMX_MINIMAL | E2 | N2 | N3 | same | 1 | 10 | local |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/events.tsv`

- **Header columns (7)**: `scenario_id`, `tick`, `event_id`, `event_type`, `scope_type`, `scope_id`, `reason_code`
- **Data rows**: 0

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/ledger.tsv`

- **Header columns (11)**: `scenario_id`, `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`
- **Data rows**: 5

Sample rows:

| scenario_id | tick | profile_id | changeset_id | snapshot_id | is_I_block | drift_global | budget_usage_msg | budget_usage_bytes | kill_switch_flag | quarantine_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | 1 | P_UMX_MINIMAL_V1 | C001 | SNP001 | True | 0 | 0 | 0 | False | False |
| S01_UMX_MINIMAL | 2 | P_UMX_MINIMAL_V1 | C002 |  | False | 0 | 0 | 0 | False | False |
| S01_UMX_MINIMAL | 3 | P_UMX_MINIMAL_V1 | C003 |  | False | 0 | 0 | 0 | False | False |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/nap_envelopes.tsv`

- **Header columns (14)**: `scenario_id`, `tick`, `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`, `applied`, `dead_letter`
- **Data rows**: 0

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/nodes.tsv`

- **Header columns (9)**: `scenario_id`, `node_id`, `layerId`, `region_id`, `node_type`, `capacity`, `flags`, `coord_x`, `coord_y`
- **Data rows**: 3

Sample rows:

| scenario_id | node_id | layerId | region_id | node_type | capacity | flags | coord_x | coord_y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | N1 | 0 | R_MAIN | compute | 10 |  | 0 | 0 |
| S01_UMX_MINIMAL | N2 | 0 | R_MAIN | compute | 10 |  | 1 | 0 |
| S01_UMX_MINIMAL | N3 | 0 | R_MAIN | aggregator | 10 | boundary | 2 | 0 |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/profile.tsv`

- **Header columns (21)**: `scenario_id`, `profile_id`, `tick_max_nodes`, `tick_max_degree`, `mdl_window_ticks`, `mdl_tau`, `residual_max_norm`, `residual_warning_ratio_num`, `residual_warning_ratio_den`, `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance_num`, `nap_soft_tolerance_den`, `nap_hard_tolerance`, `ledger_retention_ticks`, `ledger_snapshot_interval`, `ledger_reversibility_window`, `layers_max_layers`, `layers_cadences`, `emergence_epsilon_drift`, `calibration_status`
- **Data rows**: 1

Sample rows:

| scenario_id | profile_id | tick_max_nodes | tick_max_degree | mdl_window_ticks | mdl_tau | residual_max_norm | residual_warning_ratio_num | residual_warning_ratio_den | nap_msg_budget | nap_byte_budget | nap_soft_tolerance_num | nap_soft_tolerance_den | nap_hard_tolerance | ledger_retention_ticks | ledger_snapshot_interval | ledger_reversibility_window | layers_max_layers | layers_cadences | emergence_epsilon_drift | calibration_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | P_UMX_MINIMAL_V1 | 10 | 3 | 5 | 1 | 0 | 3 | 4 | 100 | 10000 | 8 | 10 | 120 | 100 | 5 | 10 | 1 | 0:1 | 0 | GO |

### Fixture: `fixtures/UMX/golden/F01_MINIMAL_TOPOLOGY/residual_epsilon.tsv`

- **Header columns (9)**: `scenario_id`, `tick`, `node_id`, `anchor_tick_ref`, `anchor_layer`, `component`, `residual_value`, `epsilon_delta`, `reason_code`
- **Data rows**: 15

Sample rows:

| scenario_id | tick | node_id | anchor_tick_ref | anchor_layer | component | residual_value | epsilon_delta | reason_code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | 1 | N1 | 1 | 0 | r | 0 | 0 | NONE |
| S01_UMX_MINIMAL | 1 | N2 | 1 | 0 | r | 0 | 0 | NONE |
| S01_UMX_MINIMAL | 1 | N3 | 1 | 0 | r | 0 | 0 | NONE |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/assertions.tsv`

- **Header columns (6)**: `scenario_id`, `property_name`, `expected`, `actual`, `result`, `notes`
- **Data rows**: 8

Sample rows:

| scenario_id | property_name | expected | actual | result | notes |
| --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | reversible_ok | TRUE | TRUE | PASS | F01 minimal reversible |
| S01_UMX_MINIMAL | checkpoint_spacing_ok | TRUE | TRUE | PASS | Snapshots at ticks 1 and 5 |
| S01_UMX_MINIMAL | drift_guard_ok | TRUE | TRUE | PASS | Zero drift |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/drift_metrics.tsv`

- **Header columns (7)**: `scenario_id`, `window_id`, `window_start_tick`, `window_end_tick`, `node_id`, `delta_value`, `band`
- **Data rows**: 4

Sample rows:

| scenario_id | window_id | window_start_tick | window_end_tick | node_id | delta_value | band |
| --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | GLOBAL | 0 | PASS |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | N1 | 0 | PASS |
| S01_UMX_MINIMAL | W1_TICKS_1_5 | 1 | 5 | N2 | 0 | PASS |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/edges.tsv`

- **Header columns (8)**: `scenario_id`, `edge_id`, `from_node_id`, `to_node_id`, `layer_relation`, `weight`, `capacity`, `flags`
- **Data rows**: 2

Sample rows:

| scenario_id | edge_id | from_node_id | to_node_id | layer_relation | weight | capacity | flags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | E1 | N1 | N2 | same | 1 | 10 | local |
| S01_UMX_MINIMAL | E2 | N2 | N3 | same | 1 | 10 | local |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/events.tsv`

- **Header columns (7)**: `scenario_id`, `tick`, `event_id`, `event_type`, `scope_type`, `scope_id`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/ledger.tsv`

- **Header columns (11)**: `scenario_id`, `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`
- **Data rows**: 5

Sample rows:

| scenario_id | tick | profile_id | changeset_id | snapshot_id | is_I_block | drift_global | budget_usage_msg | budget_usage_bytes | kill_switch_flag | quarantine_flag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | 1 | P_UMX_MINIMAL_V1 | C001 | SNP001 | True | 0 | 0 | 0 | False | False |
| S01_UMX_MINIMAL | 2 | P_UMX_MINIMAL_V1 | C002 |  | False | 0 | 0 | 0 | False | False |
| S01_UMX_MINIMAL | 3 | P_UMX_MINIMAL_V1 | C003 |  | False | 0 | 0 | 0 | False | False |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/nap_envelopes.tsv`

- **Header columns (14)**: `scenario_id`, `tick`, `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`, `applied`, `dead_letter`
- **Data rows**: 0

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/nodes.tsv`

- **Header columns (9)**: `scenario_id`, `node_id`, `layerId`, `region_id`, `node_type`, `capacity`, `flags`, `coord_x`, `coord_y`
- **Data rows**: 3

Sample rows:

| scenario_id | node_id | layerId | region_id | node_type | capacity | flags | coord_x | coord_y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | N1 | 0 | R_MAIN | compute | 10 |  | 0 | 0 |
| S01_UMX_MINIMAL | N2 | 0 | R_MAIN | compute | 10 |  | 1 | 0 |
| S01_UMX_MINIMAL | N3 | 0 | R_MAIN | aggregator | 10 | boundary | 2 | 0 |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/profile.tsv`

- **Header columns (21)**: `scenario_id`, `profile_id`, `tick_max_nodes`, `tick_max_degree`, `mdl_window_ticks`, `mdl_tau`, `residual_max_norm`, `residual_warning_ratio_num`, `residual_warning_ratio_den`, `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance_num`, `nap_soft_tolerance_den`, `nap_hard_tolerance`, `ledger_retention_ticks`, `ledger_snapshot_interval`, `ledger_reversibility_window`, `layers_max_layers`, `layers_cadences`, `emergence_epsilon_drift`, `calibration_status`
- **Data rows**: 1

Sample rows:

| scenario_id | profile_id | tick_max_nodes | tick_max_degree | mdl_window_ticks | mdl_tau | residual_max_norm | residual_warning_ratio_num | residual_warning_ratio_den | nap_msg_budget | nap_byte_budget | nap_soft_tolerance_num | nap_soft_tolerance_den | nap_hard_tolerance | ledger_retention_ticks | ledger_snapshot_interval | ledger_reversibility_window | layers_max_layers | layers_cadences | emergence_epsilon_drift | calibration_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | P_UMX_MINIMAL_V1 | 10 | 3 | 5 | 1 | 0 | 3 | 4 | 100 | 10000 | 8 | 10 | 120 | 100 | 5 | 10 | 1 | 0:1 | 0 | GO |

### Fixture: `testbed/UMX/S01_UMX_MINIMAL/residual_epsilon.tsv`

- **Header columns (9)**: `scenario_id`, `tick`, `node_id`, `anchor_tick_ref`, `anchor_layer`, `component`, `residual_value`, `epsilon_delta`, `reason_code`
- **Data rows**: 15

Sample rows:

| scenario_id | tick | node_id | anchor_tick_ref | anchor_layer | component | residual_value | epsilon_delta | reason_code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01_UMX_MINIMAL | 1 | N1 | 1 | 0 | r | 0 | 0 | NONE |
| S01_UMX_MINIMAL | 1 | N2 | 1 | 0 | r | 0 | 0 | NONE |
| S01_UMX_MINIMAL | 1 | N3 | 1 | 0 | r | 0 | 0 | NONE |

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/assertions.tsv`

- **Header columns (6)**: `scenario_id`, `property_name`, `expected`, `actual`, `result`, `notes`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/drift_metrics.tsv`

- **Header columns (7)**: `scenario_id`, `window_id`, `window_start_tick`, `window_end_tick`, `node_id`, `delta_value`, `band`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/edges.tsv`

- **Header columns (8)**: `scenario_id`, `edge_id`, `from_node_id`, `to_node_id`, `layer_relation`, `weight`, `capacity`, `flags`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/events.tsv`

- **Header columns (7)**: `scenario_id`, `tick`, `event_id`, `event_type`, `scope_type`, `scope_id`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/ledger.tsv`

- **Header columns (11)**: `scenario_id`, `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/nap_envelopes.tsv`

- **Header columns (14)**: `scenario_id`, `tick`, `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`, `applied`, `dead_letter`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/nodes.tsv`

- **Header columns (9)**: `scenario_id`, `node_id`, `layerId`, `region_id`, `node_type`, `capacity`, `flags`, `coord_x`, `coord_y`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/profile.tsv`

- **Header columns (21)**: `scenario_id`, `profile_id`, `tick_max_nodes`, `tick_max_degree`, `mdl_window_ticks`, `mdl_tau`, `residual_max_norm`, `residual_warning_ratio_num`, `residual_warning_ratio_den`, `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance_num`, `nap_soft_tolerance_den`, `nap_hard_tolerance`, `ledger_retention_ticks`, `ledger_snapshot_interval`, `ledger_reversibility_window`, `layers_max_layers`, `layers_cadences`, `emergence_epsilon_drift`, `calibration_status`
- **Data rows**: 0

### Fixture: `testbed/UMX/S02_UMX_RESIDUAL_EPSILON/residual_epsilon.tsv`

- **Header columns (9)**: `scenario_id`, `tick`, `node_id`, `anchor_tick_ref`, `anchor_layer`, `component`, `residual_value`, `epsilon_delta`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/assertions.tsv`

- **Header columns (6)**: `scenario_id`, `property_name`, `expected`, `actual`, `result`, `notes`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/drift_metrics.tsv`

- **Header columns (7)**: `scenario_id`, `window_id`, `window_start_tick`, `window_end_tick`, `node_id`, `delta_value`, `band`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/edges.tsv`

- **Header columns (8)**: `scenario_id`, `edge_id`, `from_node_id`, `to_node_id`, `layer_relation`, `weight`, `capacity`, `flags`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/events.tsv`

- **Header columns (7)**: `scenario_id`, `tick`, `event_id`, `event_type`, `scope_type`, `scope_id`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/ledger.tsv`

- **Header columns (11)**: `scenario_id`, `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/nap_envelopes.tsv`

- **Header columns (14)**: `scenario_id`, `tick`, `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`, `applied`, `dead_letter`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/nodes.tsv`

- **Header columns (9)**: `scenario_id`, `node_id`, `layerId`, `region_id`, `node_type`, `capacity`, `flags`, `coord_x`, `coord_y`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/profile.tsv`

- **Header columns (21)**: `scenario_id`, `profile_id`, `tick_max_nodes`, `tick_max_degree`, `mdl_window_ticks`, `mdl_tau`, `residual_max_norm`, `residual_warning_ratio_num`, `residual_warning_ratio_den`, `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance_num`, `nap_soft_tolerance_den`, `nap_hard_tolerance`, `ledger_retention_ticks`, `ledger_snapshot_interval`, `ledger_reversibility_window`, `layers_max_layers`, `layers_cadences`, `emergence_epsilon_drift`, `calibration_status`
- **Data rows**: 0

### Fixture: `testbed/UMX/S03_UMX_PROFILE_MDL/residual_epsilon.tsv`

- **Header columns (9)**: `scenario_id`, `tick`, `node_id`, `anchor_tick_ref`, `anchor_layer`, `component`, `residual_value`, `epsilon_delta`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/assertions.tsv`

- **Header columns (6)**: `scenario_id`, `property_name`, `expected`, `actual`, `result`, `notes`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/drift_metrics.tsv`

- **Header columns (7)**: `scenario_id`, `window_id`, `window_start_tick`, `window_end_tick`, `node_id`, `delta_value`, `band`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/edges.tsv`

- **Header columns (8)**: `scenario_id`, `edge_id`, `from_node_id`, `to_node_id`, `layer_relation`, `weight`, `capacity`, `flags`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/events.tsv`

- **Header columns (7)**: `scenario_id`, `tick`, `event_id`, `event_type`, `scope_type`, `scope_id`, `reason_code`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/ledger.tsv`

- **Header columns (11)**: `scenario_id`, `tick`, `profile_id`, `changeset_id`, `snapshot_id`, `is_I_block`, `drift_global`, `budget_usage_msg`, `budget_usage_bytes`, `kill_switch_flag`, `quarantine_flag`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/nap_envelopes.tsv`

- **Header columns (14)**: `scenario_id`, `tick`, `envelope_id`, `id_key_seed`, `source_pillar`, `target_pillar`, `region_id`, `intent_type`, `schema_id`, `nonce`, `priority`, `payload_bytes`, `applied`, `dead_letter`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/nodes.tsv`

- **Header columns (9)**: `scenario_id`, `node_id`, `layerId`, `region_id`, `node_type`, `capacity`, `flags`, `coord_x`, `coord_y`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/profile.tsv`

- **Header columns (21)**: `scenario_id`, `profile_id`, `tick_max_nodes`, `tick_max_degree`, `mdl_window_ticks`, `mdl_tau`, `residual_max_norm`, `residual_warning_ratio_num`, `residual_warning_ratio_den`, `nap_msg_budget`, `nap_byte_budget`, `nap_soft_tolerance_num`, `nap_soft_tolerance_den`, `nap_hard_tolerance`, `ledger_retention_ticks`, `ledger_snapshot_interval`, `ledger_reversibility_window`, `layers_max_layers`, `layers_cadences`, `emergence_epsilon_drift`, `calibration_status`
- **Data rows**: 0

### Fixture: `testbed/UMX/S04_UMX_STRESS_SAFETY/residual_epsilon.tsv`

- **Header columns (9)**: `scenario_id`, `tick`, `node_id`, `anchor_tick_ref`, `anchor_layer`, `component`, `residual_value`, `epsilon_delta`, `reason_code`
- **Data rows**: 0

## Part 9 — Companion Pending Docs (Annexes / TODO Specs)

### Source: `companions_pending/MDL_Placement_and_Motif_Spec_UMX_Press_Codex_todo.md` (verbatim)

# MDL Placement & Motif Spec — UMX + Press + Codex (TODO)

- Shared MDL objective (coding scheme, priors, penalties).
- Mapping between Press motifs / transform-graph IDs and UMX structures.
- Codex feedback lanes and deterministic tie-breakers.
- Gates finalisation of M3 and F03 fixtures.

### Source: `companions_pending/PFNA_Universal_Commit_Record_Spec_todo.md` (verbatim)

# PFNA / Universal Commit v1 Record Spec (TODO)

- Exact record layout for ⟦E_t⟧ (fields, sizes, order).
- Hash chaining rule and seeding.
- Validation test vectors.

### Source: `companions_pending/UMX_Profiles_and_Budgets_Annex_todo.md` (verbatim)

# UMX Profiles & Budget / Policy Annex (TODO)

- Full schema for profile fields (types, ranges, defaults).
- Policy DSL for budgets/quotas and actions.
- Example profiles for sandbox vs production.

## Part 10 — Additional Root-Level Markdown Specs (not classified above)

### Source: `umx_fixtures_testbed_integration_pack_2025_11_17.md` (verbatim)

---
id: umx_fixtures_and_testbed_pack_v1
version: 1.0-draft
status: normative-shell
pillar: UMX
created: 2025-11-17
---

# UMX Fixtures & Testbed Integration Pack v1

## 0. Purpose and Scope

This document defines the **Golden Fixtures** and **testbed integration layout** for the Universal Matrix (UMX) pillar.

It:

- Specifies the **fixture families** and individual fixture IDs for UMX v1.
- Defines the **table schemas** and file layout used to represent UMX fixtures and scenario outputs in the Aether Paper Testbed.
- Describes how fixtures map to **scenario IDs (Sxx)** and to **MAX properties**.
- Provides enough detail for an engineer to assemble the fixtures and wire them into the existing Testbed MASTER bundle without guessing.

This pack is designed to sit under the `fixtures/` and `testbed/` directories of the `UMX_Spec_Pack_v1_YYYY-MM-DD.zip` described in the UMX Spec Master Index.

---

## 1. Directory and File Layout

### 1.1 Top-Level Layout

Within the UMX Spec Pack ZIP, fixtures and testbed integration are laid out as:

- `fixtures/UMX/`
  - `fixtures_index.tsv`
  - `golden/`
    - `F01_MINIMAL_TOPOLOGY/`
    - `F02_RESIDUAL_EPSILON/`
    - `F03_PROFILE_MDL/`
    - `F04_STRESS_SAFETY/`
- `testbed/UMX/`
  - `S01_UMX_MINIMAL/`
  - `S02_UMX_RESIDUAL_EPSILON/`
  - `S03_UMX_PROFILE_MDL/`
  - `S04_UMX_STRESS_SAFETY/`

Fixtures under `fixtures/UMX/golden/` are **small, self-contained** configurations that can be loaded directly by a developer or by the Testbed harness. The corresponding `testbed/UMX/Sxx_...` directories define the **scenario-level tables** that the Aether Testbed consumes when running property checks.

### 1.2 Naming Conventions

- Fixture IDs follow the pattern `FNN_NAME`, where `NN` is a two-digit integer starting at `01` and `NAME` is a short descriptor.
- Scenario IDs follow the pattern `SNN_UMX_NAME`, where `NN` matches the fixture index for Golden Fixtures.
- File names under each fixture or scenario directory are **fixed** as described in the schemas below. No additional arbitrary files are included in v1.

---

## 2. Common Table Schemas

This section defines **shared table schemas** used across all UMX fixtures and scenarios. These are deliberately simple and closely mirror the structures described in the UMX spec artefacts.

All tables are assumed to be TSV (tab-separated values) encoded as plain text, with a header row naming columns exactly as specified.

### 2.1 `fixtures_index.tsv`

The `fixtures_index.tsv` file in `fixtures/UMX/` lists all Golden Fixtures.

Columns:

1. `fixture_id` — string; for Golden Fixtures: `F01_MINIMAL_TOPOLOGY`, `F02_RESIDUAL_EPSILON`, `F03_PROFILE_MDL`, `F04_STRESS_SAFETY`.
2. `family` — string; one of `minimal`, `residual_epsilon`, `profile_mdl`, `stress_safety`.
3. `scenario_id` — string; matching the scenario in `testbed/UMX/` (for v1: `S01_UMX_MINIMAL`, `S02_UMX_RESIDUAL_EPSILON`, `S03_UMX_PROFILE_MDL`, `S04_UMX_STRESS_SAFETY`).
4. `description` — short human-readable description of the fixture.
5. `status` — string; one of `draft`, `ready`, `deprecated`. For initial Golden Fixtures v1 this is `ready`.

No additional columns are present in v1.

### 2.2 Node Table Schema

Used in both fixtures and testbed scenarios to describe the node set.

Filename pattern:

- For fixture: `nodes.tsv` under `fixtures/UMX/golden/FNN_.../`.
- For scenario: `nodes.tsv` under `testbed/UMX/SNN_.../`.

Columns:

1. `scenario_id` — string; scenario identifier (e.g. `S01_UMX_MINIMAL`).
2. `node_id` — string; unique node identifier within the scenario (e.g. `N1`, `N2`).
3. `layerId` — integer; layer index as per `umx_layers_policy_v1.md` (v1 Golden Fixtures use `0` only).
4. `region_id` — string; region identifier (e.g. `R_MAIN`, `R_ISO1`).
5. `node_type` — string; role of the node (e.g. `compute`, `sensor`, `aggregator`).
6. `capacity` — integer; maximum number of messages per tick this node is intended to handle under normal conditions.
7. `flags` — string; comma-separated tags such as `boundary`, `root`, `stress_target`. Empty string if no flags.
8. `coord_x` — integer; x-coordinate in the shared spatial frame (or abstract index). For v1 fixtures, may be small integers such as `0`, `1`, `2`.
9. `coord_y` — integer; y-coordinate in the shared spatial frame. For v1 fixtures, may be small integers such as `0`, `0`, `0` for a line.

No other columns are defined for v1 Golden Fixtures.

### 2.3 Edge Table Schema

Edges describe connectivity between nodes.

Filename pattern:

- For fixture: `edges.tsv`.
- For scenario: `edges.tsv`.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `edge_id` — string; unique identifier for the edge within the scenario (e.g. `E1`, `E2`).
3. `from_node_id` — string; node_id of the source node.
4. `to_node_id` — string; node_id of the target node.
5. `layer_relation` — string; one of `same`, `up`, `down`, indicating relationship between `layerId` of the nodes.
6. `weight` — integer; weight or ley strength proxy for routing decisions (v1 fixtures use small integers such as `1` or `2`).
7. `capacity` — integer; message capacity for this edge per tick.
8. `flags` — string; tags such as `backbone`, `local`, `cross_region`, `stress_target`.

### 2.4 Profile Table Schema

Profiles control UMX behaviour in fixtures and scenarios. For Golden Fixtures, we provide a compact profile table that aligns with `umx_profile_v1.md`.

Filename pattern:

- `profile.tsv` under each fixture and scenario directory.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `profile_id` — string; profile identifier (e.g. `P_UMX_MINIMAL_V1`).
3. `tick_max_nodes` — integer; maps to `tick.max_nodes` in `umx_profile_v1.md`.
4. `tick_max_degree` — integer; maps to `tick.max_degree`.
5. `mdl_window_ticks` — integer; maps to `mdl.window_ticks`.
6. `mdl_tau` — integer; maps to `mdl.tau`.
7. `residual_max_norm` — integer; maps to `residual.max_norm`.
8. `residual_warning_ratio_num` — integer numerator for `residual.warning_ratio`.
9. `residual_warning_ratio_den` — integer denominator for `residual.warning_ratio` (for rational representation, e.g. `3/4`).
10. `nap_msg_budget` — integer; maps to `nap.msg_budget`.
11. `nap_byte_budget` — integer; maps to `nap.byte_budget`.
12. `nap_soft_tolerance_num` — integer numerator for `nap.soft_tolerance`.
13. `nap_soft_tolerance_den` — integer denominator for `nap.soft_tolerance`.
14. `nap_hard_tolerance` — integer; absolute threshold for `nap.hard_tolerance`.
15. `ledger_retention_ticks` — integer; maps to `ledger.retention_ticks`.
16. `ledger_snapshot_interval` — integer; maps to `ledger.snapshot_interval`.
17. `ledger_reversibility_window` — integer; maps to `ledger.reversibility_window`.
18. `layers_max_layers` — integer; maps to `layers.max_layers`.
19. `layers_cadences` — string; e.g. `0:1` for a single layer with `k_0 = 1`.
20. `emergence_epsilon_drift` — integer; maps to `emergence.epsilon_drift`.
21. `calibration_status` — string; one of `GO`, `HOLD`, `KILL`.

This compact profile table is sufficient for Golden Fixtures and scenarios; real profiles may be expanded into dedicated profile documents as needed.

### 2.5 Residual and Epsilon Table Schema

Residual and epsilon entries are represented in a combined table for simplicity.

Filename pattern:

- `residual_epsilon.tsv`.

Columns:

1. `scenario_id` — string; scenario identifier.
2. `tick` — integer; tick index.
3. `node_id` — string; node to which this entry applies.
4. `anchor_tick_ref` — integer; reference tick for the base anchor.
5. `anchor_layer` — integer; usually `0` for base layer.
6. `component` — string; component name or index (e.g. `v`, `w`, `r1`).
7. `residual_value` — integer; residual value at this tick for the component.
8. `epsilon_delta` — integer; epsilon correction for this component at this tick. Zero if no epsilon is applied.
9. `reason_code` — string; reason for epsilon (e.g. `NONE`, `FLOAT_DRIFT`, `QUANT_CLAMP`).

### 2.6 Drift Metrics Table Schema

Drift metrics summarise behaviour over windows.

Filename pattern:

- `drift_metrics.tsv`.

Columns:

1. `scenario_id` — string.
2. `window_id` — string; identifier for the window (e.g. `W1_TICKS_1_10`).
3. `window_start_tick` — integer.
4. `window_end_tick` — integer.
5. `node_id` — string or special value `GLOBAL` for global drift.
6. `delta_value` — integer; \(\Delta_i(W)\) or \(\Delta(W)\) depending on `node_id`.
7. `band` — string; one of `PASS`, `INVESTIGATE`, `FAIL` (for convenience). For `node_id = GLOBAL`, this matches the emergence band definitions.

### 2.7 Events Table Schema

Events capture noteworthy occurrences such as kill-switch activation, drift guard triggers, budget overruns and backpressure signals.

Filename pattern:

- `events.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer.
3. `event_id` — string; unique per event.
4. `event_type` — string; examples include `KILL_SWITCH`, `DRIFT_GUARD_ACTIVATED`, `BUDGET_SOFT_OVERRUN`, `BUDGET_HARD_OVERRUN`, `BACKPRESSURE_SIGNAL_SENT`.
5. `scope_type` — string; one of `NODE`, `REGION`, `SYSTEM`.
6. `scope_id` — string; node_id, region_id or `GLOBAL` depending on `scope_type`.
7. `reason_code` — string; short code explaining the cause (e.g. `OPERATOR`, `AUTOMATIC_DRIFT`, `AUTOMATIC_BUDGET`).

### 2.8 NAP Envelopes Table Schema

For scenarios that involve NAP interaction, envelopes are described explicitly.

Filename pattern:

- `nap_envelopes.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer; tick when the envelope is visible to UMX.
3. `envelope_id` — string; unique identifier for the envelope.
4. `id_key_seed` — string; seed from which envelope identity can be derived.
5. `source_pillar` — string (e.g. `EXTERNAL`, `UMX`, `OTHER_PILLAR`).
6. `target_pillar` — string (here always `UMX` or occasionally other pillars for outbound rows).
7. `region_id` — string; target region.
8. `intent_type` — string; e.g. `WRITE_STATE`, `APPLY_DELTA`, `INJECT_SIGNAL`, `QUERY_STATE`, `STATUS_UPDATE`.
9. `schema_id` — string; payload schema identifier.
10. `nonce` — string; idempotence token.
11. `priority` — integer; relative priority for routing.
12. `payload_bytes` — integer; size of payload in bytes to support budget calculations.
13. `applied` — boolean; `TRUE` if applied, `FALSE` if rejected or dead-lettered.
14. `dead_letter` — boolean; `TRUE` if this envelope was placed in dead-letter store.

### 2.9 Ledger Table Schema

The ledger table records per-tick summary metrics and references to manifests.

Filename pattern:

- `ledger.tsv`.

Columns:

1. `scenario_id` — string.
2. `tick` — integer.
3. `profile_id` — string.
4. `changeset_id` — string; reference to Commit Manifest entry.
5. `snapshot_id` — string; reference to Snapshot Manifest if a snapshot occurs at this tick, otherwise empty.
6. `is_I_block` — boolean; `TRUE` if this tick corresponds to an I-block.
7. `drift_global` — integer; global drift value for this tick or cumulative up to this tick (fixture-specific definition must be documented).
8. `budget_usage_msg` — integer; number of messages processed in this tick.
9. `budget_usage_bytes` — integer; total payload bytes processed in this tick.
10. `kill_switch_flag` — boolean; `TRUE` if kill-switch is active at end of this tick.
11. `quarantine_flag` — boolean; `TRUE` if scenario or region is under quarantine at this tick.

### 2.10 Assertions Table Schema

The assertions table expresses MAX properties as expected vs actual values for each scenario.

Filename pattern:

- `assertions.tsv`.

Columns:

1. `scenario_id` — string.
2. `property_name` — string; property code such as `drift_guard_ok`, `routing_capacity_ok`, `back_pressure_ok`, `dead_letter_empty`, `isolation_ok`, `kill_switch_ok`, `reversible_ok`, `skip_ahead_ok`, `skip_back_ok`.
3. `expected` — string; expected result, usually `TRUE`, `FALSE`, `PASS`, `INVESTIGATE` or `FAIL` depending on property type.
4. `actual` — string; actual result produced when the scenario is run and evaluated.
5. `result` — string; one of `PASS`, `FAIL`, `INVESTIGATE`. For Golden Fixtures this is usually `PASS`.
6. `notes` — string; short comment, may be empty.

---

## 3. Golden Fixtures Definitions

This section defines the four Golden Fixtures for UMX v1. Each fixture description specifies:

- Fixture ID and scenario ID,
- Intent and properties under test,
- Tables that must be populated,
- Qualitative structure of the data (without fixing every numeric value, which is left to concrete fixture files).

### 3.1 Fixture F01 — Minimal Topology

- `fixture_id`: `F01_MINIMAL_TOPOLOGY`
- `scenario_id`: `S01_UMX_MINIMAL`
- Family: `minimal`

#### 3.1.1 Intent

Provide a **smallest useful UMX configuration** to validate:

- Node and edge tables,
- Basic tick operation without residuals or epsilon layers,
- Conservation and determinism for a trivial case.

#### 3.1.2 Structure

- Node count: 3 nodes (`N1`, `N2`, `N3`).
- Layer configuration: single layer (`layerId = 0` for all nodes).
- Regions: single region (`R_MAIN`).
- Edges: at least two edges forming a simple path (`N1 → N2 → N3`).
- Capacities: small integer capacities (for example, `capacity = 10` for nodes and `capacity = 10` for edges), within `tick_max_nodes` and `tick_max_degree` constraints.

#### 3.1.3 Tables

Populate at minimum:

- `nodes.tsv` — three rows for `N1`, `N2`, `N3` with `layerId = 0`, `region_id = R_MAIN`, simple coordinates such as `(0,0)`, `(1,0)`, `(2,0)`.
- `edges.tsv` — rows for `E1: N1→N2`, `E2: N2→N3` with `layer_relation = same`.
- `profile.tsv` — a profile `P_UMX_MINIMAL_V1` with:
  - `tick_max_nodes` ≥ 3,
  - `tick_max_degree` ≥ 2,
  - `mdl_window_ticks` set to a small value such as 5,
  - residual and emergence settings that allow trivial drift (for example, `residual_max_norm = 0`, `emergence_epsilon_drift = 0`).
- `residual_epsilon.tsv` — all zeros; no residuals or epsilon corrections.
- `drift_metrics.tsv` — drift values of zero for all nodes and for global drift, band `PASS`.
- `ledger.tsv` — a short sequence of ticks (for example, ticks 1–5) with stable metrics and no kill-switch or quarantine flags.
- `assertions.tsv` — at minimum, properties:
  - `reversible_ok` expected `TRUE`,
  - `drift_guard_ok` expected `TRUE`,
  - `routing_capacity_ok` expected `TRUE` (since traffic is below capacity).

### 3.2 Fixture F02 — Residual and Epsilon

- `fixture_id`: `F02_RESIDUAL_EPSILON`
- `scenario_id`: `S02_UMX_RESIDUAL_EPSILON`
- Family: `residual_epsilon`

#### 3.2.1 Intent

Demonstrate **non-zero residuals and sparse epsilon corrections** in a controlled, small graph, and validate drift metrics and emergence bands.

#### 3.2.2 Structure

- Node count: 3–4 nodes in a slightly more connected graph (for example, a triangle or a small hub).
- Residual behaviour: at least one node experiences deterministic non-zero residuals over a defined window.
- Epsilon behaviour: a small number of epsilon corrections are applied to keep drift within bounds or to enforce bit-exact replay.

#### 3.2.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — as for F01, but with a topology that produces more interesting residual patterns.
- `profile.tsv` — a profile `P_UMX_RESIDUAL_EPSILON_V1` with:
  - `residual_max_norm` set to a small integer such as 5,
  - `emergence_epsilon_drift` set to a non-zero value such as 2,
  - other fields chosen to exercise drift computations.
- `residual_epsilon.tsv` — multiple ticks with:
  - non-zero `residual_value` for at least one node and component,
  - non-zero `epsilon_delta` entries for a subset of those residuals.
- `drift_metrics.tsv` — per-node and global drift values that:
  - include both zero and non-zero drift windows,
  - produce at least one `INVESTIGATE` band according to `umx_emergence_bands_v1.md`.
- `ledger.tsv` — ticks that show how residuals and epsilon corrections evolve over time.
- `assertions.tsv` — properties including:
  - `drift_guard_ok` expected `TRUE` (drift guards behave according to configuration),
  - `orthogonal_residuals_ok` expected `TRUE` where applicable,
  - `entropy_bound_ok` expected `TRUE`.

### 3.3 Fixture F03 — Profile and MDL

- `fixture_id`: `F03_PROFILE_MDL`
- `scenario_id`: `S03_UMX_PROFILE_MDL`
- Family: `profile_mdl`

#### 3.3.1 Intent

Exercise **profile-controlled MDL behaviour** by defining structural or SLP proposals that are accepted or rejected according to the MDL objective.

#### 3.3.2 Structure

- Node and edge topology: small graph where adding or removing an edge has a measurable effect on the MDL codelength.
- Proposals: at least two proposals over a window:
  - One that improves MDL sufficiently and should be accepted (\(\Delta L \le -\tau\)).
  - One that does not (\(\Delta L > -\tau\)) and should be rejected.

#### 3.3.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — as needed for the MDL scenario.
- `profile.tsv` — a profile `P_UMX_PROFILE_MDL_V1` with:
  - `mdl_window_ticks` chosen to include the proposal window (for example, 10),
  - `mdl_tau` chosen so that one proposal meets the threshold and one does not.
- `residual_epsilon.tsv` — traces sufficient to compute MDL codelengths for baseline and candidate models.
- `ledger.tsv` — ticks where MDL proposals are evaluated, with `changeset_id` and MDL summary metrics.
- `events.tsv` — entries for proposal evaluations if they are treated as explicit events.
- `assertions.tsv` — properties including:
  - MDL-related property (for example, `mdl_acceptance_ok`) expected `TRUE`,
  - Checks that for accepted proposals `delta_mdl ≤ -tau` and for rejected proposals `delta_mdl > -tau`.

### 3.4 Fixture F04 — Stress and Safety

- `fixture_id`: `F04_STRESS_SAFETY`
- `scenario_id`: `S04_UMX_STRESS_SAFETY`
- Family: `stress_safety`

#### 3.4.1 Intent

Exercise **stress, budgets, backpressure, kill-switch and quarantine** behaviours in a compact scenario.

#### 3.4.2 Structure

- Node and edge topology: small network with at least two regions:
  - Main region (`R_MAIN`) where high load is applied.
  - Isolated region (`R_ISO1`) used to test isolation and quarantine.
- NAP envelopes: traffic configured to approach and exceed budget thresholds in `R_MAIN`, while leaving `R_ISO1` within normal bounds.
- Kill-switch: at least one kill-switch activation event (scope `REGION` or `SYSTEM`).
- Quarantine: at least one region or scenario-level quarantine flag.

#### 3.4.3 Tables

Populate at minimum:

- `nodes.tsv` and `edges.tsv` — describing regions `R_MAIN` and `R_ISO1` and their connectivity.
- `profile.tsv` — profile `P_UMX_STRESS_SAFETY_V1` with budgets configured to make overruns likely under the chosen envelopes.
- `nap_envelopes.tsv` — a sequence of envelopes that:
  - cause soft budget overruns (trigger backpressure but not kill-switch),
  - cause hard budget overruns,
  - include at least one envelope routed to a non-existent target to exercise dead-letter behaviour.
- `events.tsv` — entries for:
  - budget soft and hard overruns,
  - backpressure signals,
  - kill-switch activation,
  - quarantine activation.
- `ledger.tsv` — ticks showing budget usage, drift, kill-switch flag and quarantine flag.
- `assertions.tsv` — properties including:
  - `routing_capacity_ok` expected `TRUE` or `FALSE` depending on scenario design,
  - `back_pressure_ok` expected `TRUE` (backpressure behaves as configured),
  - `dead_letter_empty` expected `FALSE` for this fixture (since misrouted messages are deliberately injected),
  - `isolation_ok` expected `TRUE` (issues in `R_MAIN` do not corrupt `R_ISO1`),
  - `kill_switch_ok` expected `TRUE`,
  - `quarantine_flag` used as expected.

---

## 4. Mapping Fixtures to MAX Properties

This section provides a high-level mapping from Golden Fixtures to MAX properties for UMX.

### 4.1 Fixture F01 — Minimal Topology

Primarily covers:

- `reversible_ok` — simple replay and rollback over a small number of ticks.
- `checkpoint_spacing_ok` — if snapshots are included.
- `drift_guard_ok` — in the trivial case where drift is zero.

### 4.2 Fixture F02 — Residual and Epsilon

Primarily covers:

- `drift_guard_ok` — non-trivial drift and epsilon usage.
- `orthogonal_residuals_ok` — where orthogonality definitions are applied.
- `entropy_bound_ok` — ensuring residuals and epsilon corrections do not violate entropy constraints.

### 4.3 Fixture F03 — Profile and MDL

Primarily covers:

- MDL acceptance behaviour and any derived property such as `mdl_acceptance_ok`.
- Correct consumption of `umx_profile_v1` fields controlling MDL.

### 4.4 Fixture F04 — Stress and Safety

Primarily covers:

- `routing_capacity_ok` — under high load.
- `back_pressure_ok` — under soft and hard overruns.
- `dead_letter_empty` — expected `FALSE` for this fixture.
- `isolation_ok` — isolation between regions.
- `kill_switch_ok` — scope and determinism of kill-switch.
- `drift_guard_ok` — interaction between stress and drift guards.

---

## 5. Usage in Aether Paper Testbed

### 5.1 Loading Fixtures

For each Golden Fixture:

1. Load `nodes.tsv`, `edges.tsv` and `profile.tsv` into the testbed scenario configuration.
2. Load `residual_epsilon.tsv`, `drift_metrics.tsv`, `nap_envelopes.tsv`, `events.tsv` and `ledger.tsv` as the corresponding data tables for that scenario.
3. Load `assertions.tsv` as the list of properties to evaluate.

### 5.2 Running Properties

The Testbed evaluates each property in `assertions.tsv` by:

- Reading the required tables as specified in the UMX spec artefacts and MAX definitions.
- Computing expected booleans or bands.
- Comparing against `expected` and populating `actual` and `result` fields.

Golden Fixtures v1 are expected to pass all listed properties for their scenarios under a conformant UMX implementation.

### 5.3 Runtime Integration

When a runtime UMX implementation is integrated with the testbed:

1. The runtime loads the same `nodes.tsv`, `edges.tsv` and `profile.tsv` as initial configuration.
2. The runtime executes the scenario (either by reading `nap_envelopes.tsv` as input or by generating equivalent envelopes).
3. The runtime exports its own `residual_epsilon.tsv`, `drift_metrics.tsv`, `events.tsv`, `nap_envelopes.tsv` (for outbound messages) and `ledger.tsv`.
4. The Testbed compares runtime outputs against the Golden Fixture expectations where applicable, and then evaluates properties.

A runtime is considered conformant for a fixture when there are no unexplained differences in the tables that affect property evaluation and when all properties in `assertions.tsv` have `result = PASS`.

---

## 6. Versioning and Extension

This pack defines **UMX Golden Fixtures v1** and the associated testbed integration layout.

Future versions may:

- Add new fixtures (for example F05 for multi-layer behaviour),
- Add additional properties to `assertions.tsv`,
- Refine table schemas with extra columns while keeping existing columns stable.

All such changes must:

- Increment the `version` in this document and in any affected fixture manifests,
- Preserve backwards compatibility for existing v1 fixtures whenever possible,
- Be reflected in the UMX Spec Master Index and TBP verification crosswalk.

This completes the UMX Fixtures & Testbed Integration Pack v1 specification.

