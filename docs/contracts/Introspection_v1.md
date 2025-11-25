# Introspection_v1 — Phase 3 artefact queries

Introspection_v1 defines **read-only accessors** for internal Aether artefacts so
tools can query run results without scraping raw files. The APIs are designed to
be deterministic and side-effect free.

## Scope

- Covers Phase 3 governance/ops “introspection” work (SPEC-006 P3.2.3).
- Applies to Gate/TBP + TickLoop_v1 runs that emit CMP-0 style outputs.

## IntrospectionViewV1

An `IntrospectionViewV1` is a lightweight wrapper built from a completed run
(`SessionRunResult` or `GF01RunResult`) plus optional Codex artefacts. It
collects references to existing run objects; callers **must not mutate** them.

- `gid` — graph ID for the run.
- `run_id` — run identifier.
- `total_ticks` — number of ticks executed.
- `window_ids` — tuple of APX window IDs present in the run.
- `ledgers_by_tick` — mapping `tick -> UMXTickLedger_v1`.
- `p_blocks_by_tick` — mapping `tick -> LoomPBlock_v1`.
- `i_blocks_by_tick` — mapping `tick -> LoomIBlock_v1` (may be empty).
- `manifests_by_window` — mapping `window_id -> APXManifest_v1`.
- `apxi_views_by_window` — mapping `window_id -> APXiView_v1` (may be empty).
- `envelopes` — tuple of `NAPEnvelope_v1` across CTRL/INGRESS/DATA/EGRESS
  layers for the run (ordered).
- `uledger_by_tick` — mapping `tick -> ULedgerEntry_v1`.
- `codex_motifs` — tuple of `CodexLibraryEntry_v1` if provided.
- `codex_proposals` — tuple of `CodexProposal_v1` if provided.

## Accessor APIs

All accessors are **read-only** and return existing artefact objects:

- `get_umx_ledger(tick: int) -> UMXTickLedger_v1`
- `get_loom_p_block(tick: int) -> LoomPBlock_v1`
- `get_loom_i_block(tick: int) -> LoomIBlock_v1` (raises if none exists)
- `get_apx_manifest(window_id: str) -> APXManifest_v1`
- `get_apxi_view(window_id: str) -> APXiView_v1` (raises if none exists)
- `get_nap_envelopes(*, tick: int | None = None, layer: str | None = None)
  -> tuple[NAPEnvelope_v1, ...]`
- `get_uledger_entry(tick: int) -> ULedgerEntry_v1`
- `list_codex_motifs() -> tuple[CodexLibraryEntry_v1, ...]`
- `list_codex_proposals() -> tuple[CodexProposal_v1, ...]`

### Invariants

- Accessors **never** mutate underlying artefacts.
- Missing artefacts raise deterministic `ValueError` messages.
- Envelope filtering respects layer names (`CTRL`, `INGRESS`, `DATA`, `EGRESS`).
- Returned objects correspond exactly to the run outputs (no recomputation).

## Determinism

- `IntrospectionViewV1` is derived from immutable run results in tick order.
- Accessors always return the same objects for repeated calls.
- Ordering of envelope and Codex sequences is stable (tick/layer order for
  NAP, insertion order for Codex).

## Usage

```python
from ops.introspection import build_introspection_view
from gate import run_session

session = run_session(session_config)
view = build_introspection_view(session)
ledger = view.get_umx_ledger(1)
ctrl_envelopes = view.get_nap_envelopes(layer="CTRL")
```

Codex motifs/proposals can be passed in when available; otherwise they default
to empty tuples.
