# Metrics_v1

Phase 3 governance metrics contract describing how runs expose small, structured
counters without affecting determinism. Metrics are intentionally minimal for
this phase and are expected to remain backwards compatible as new fields are
added.

## Purpose

Provide basic visibility into run progress and artefacts so operators and CI
pipelines can assert high-level health without inspecting full snapshots.

## MetricsConfig_v1

| Field | Type | Description |
| --- | --- | --- |
| `enabled` | bool | Toggle collection. Defaults to `false` to avoid extra work unless explicitly requested. |

Configurable via `RunConfig_v1.metrics` or programmatically via `SessionConfig_v1.metrics_config`.

## MetricsSnapshot_v1

A deterministic JSON-friendly view of core counts. Collected at end-of-run when
metrics are enabled.

| Field | Type | Description |
| --- | --- | --- |
| `gid` | string | Topology gid for the run. |
| `run_id` | string | Run identifier. |
| `total_ticks` | int | Number of ticks executed. |
| `window_count` | int | Number of Press/APX windows registered for the run. |
| `nap_total` | int | Total NAP envelopes observed (CTRL/INGRESS/DATA/EGRESS). |
| `nap_ingress` | int | Count of INGRESS layer envelopes. |
| `nap_data` | int | Count of DATA layer envelopes. |
| `nap_egress` | int | Count of EGRESS layer envelopes. |
| `uledger_entries` | int | Number of U-ledger entries produced. |
| `uledger_last_hash` | string\|null | Hash of the final U-ledger entry, if any. |
| `apx_manifests` | int | Number of APX manifests emitted. |
| `apxi_views` | int | Number of APXi views produced. |
| `codex_motif_counts` | object | Optional map of Codex motif counts when Codex is enabled. |

## Notes

- Metrics capture counts only; they do not change runtime determinism.
- Additional metrics can be added in later phases without breaking the v1
  envelope shape.

