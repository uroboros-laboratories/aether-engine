# What Are “Contracts” in the Aether Engine? (v1)

In our Aether context, a **contract** is a small, precise document that defines
*exactly* what a data structure or module boundary looks like and what rules it
must obey.

Think of it as:

> “This is the shape of the thing, these are the fields, these are the types,
> and these are the invariants. Any implementation that claims to produce this
> type has to follow these rules.”

Not legal contracts — **type/data contracts**.

---

## 1. Why we use contracts

We’re doing “paper > pixels”, and we want:

- Multiple pieces of code (or even multiple languages) to agree on the same
  structures.
- Tests that don’t care *how* you implemented something, only that the outputs
  match the spec.
- A clean separation between:
  - **Specs** — high-level behaviour and stories.
  - **Contracts** — concrete types + invariants.
  - **Code** — one particular implementation of those contracts.

So a contract is the **bridge** between the math/specs and the code.

---

## 2. What a contract actually contains

A typical `*_v1` contract doc for Aether will have:

1. **Purpose / scope**
   - What this type represents (e.g. “per-tick UMX ledger”, “per-tick scene frame”).

2. **Fields and types**
   - Exact field names.
   - Types: integer, string, enum, array, etc.
   - Cardinality: single value vs list vs map.

3. **Invariants / rules**
   - Relationships that must always hold.
   - Example: lengths must match, sums must match, IDs in valid ranges.

4. **Versioning notes**
   - This is `*_v1`; later we might add `v2`, but v1 won’t silently change.

You can think of them as “language-agnostic structs” with extra rules attached.

---

## 3. Examples in Aether

Some key contracts we’ve been talking about:

### 3.1 `TopologyProfile_v1`

Describes the graph structure:

- Node count `N`.
- List of edges with:
  - `e_id`
  - `i`, `j`
  - `k`, `cap`, `SC`, `c`
- Invariants like:
  - Node IDs must be in `1..N`.
  - Edge IDs must be consecutive and sorted.

Code that loads a topology must produce something that matches this contract.

### 3.2 `UMXTickLedger_v1` and `EdgeFlux_v1`

Describe the per-tick output of the UMX engine:

- For `UMXTickLedger_v1`, fields like:
  - `gid`, `run_id`, `tick`
  - `pre_u[]`, `post_u[]`
  - `edges[]` (a list of `EdgeFlux_v1`)
  - `sum_pre_u`, `sum_post_u`, `z_check`

- For `EdgeFlux_v1`, fields like:
  - `e_id`
  - `i`, `j`
  - `du`, `raw`, `f_e`

Invariants include:

- `len(pre_u) == len(post_u) == N`
- `sum_pre_u == sum(pre_u)`
- `sum_post_u == sum(post_u)`
- `sum_pre_u == sum_post_u == z_check`

Any UMX implementation that claims to output a `UMXTickLedger_v1` has to satisfy
all of these.

### 3.3 `SceneFrame_v1`

This is the per-tick integration bundle that Gate/TBP / NAP / governance see.

It contains:

- IDs: `gid`, `run_id`, `tick`, `nid`
- UMX state: `pre_u`, `post_u`
- Loom data: `C_prev`, `C_t`
- Press/APX info: window IDs, `manifest_check`, etc.
- Possibly metadata that other layers use.

The contract ensures every pillar sees the same, consistent snapshot of the tick.

---

## 4. Where contracts live in the repo

In the repo layout we’ve been planning, contracts live under:

```text
docs/
  contracts/
    TopologyProfile_v1.md
    Profile_CMP0_v1.md
    UMXTickLedger_v1.md
    LoomBlocks_v1.md
    APXManifest_v1.md
    NAPEnvelope_v1.md
    SceneFrame_v1.md
    ULedgerEntry_v1.md
    CodexContracts_v1.md
    ...
```

Each of these files is a contract: a small, self-contained spec for a type.

- **Specs** (like `SPEC_002` and pillar master specs) reference contracts.
- **Code** implements the contracts.
- **Tests** check that code outputs match the contracts + fixtures.

---

## 5. How this helps you personally

When you sit down to code:

- You don’t have to re-interpret the whole pillar spec each time.
- You just open the relevant contract file and implement exactly that shape,
  then write tests that compare against fixtures (like GF-01 PDFs) and the
  exam doc.

And when future-you (or someone else) comes back later, they can:

- Swap implementation languages,
- Add a new test harness,
- Or refactor code,

without changing what the engine *means*, because the contracts + specs are
the real source of truth.
