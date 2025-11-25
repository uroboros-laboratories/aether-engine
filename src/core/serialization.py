"""Canonical JSON serialisation helpers for GF-01 artefacts.

These functions turn the CMP-0/GF-01 dataclasses into plain Python primitives
so they can be serialised deterministically for regression testing.
"""
from __future__ import annotations

import json
from typing import Dict, List

from core.tick_loop import GF01RunResult
from gate.gate import NAPEnvelopeV1, SceneFrameV1, SessionRunResult
from loom.loom import (
    FluxSummaryV1,
    LoomIBlockV1,
    LoomPBlockV1,
    TopologyEdgeSnapshotV1,
)
from press.apxi import APXiViewV1
from press.press import APXManifestV1, APXStreamV1
from uledger.entry import ULedgerEntryV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1


def _serialize_edge_flux(edge: EdgeFluxV1) -> Dict[str, int]:
    return {
        "e_id": edge.e_id,
        "i": edge.i,
        "j": edge.j,
        "du": edge.du,
        "raw": edge.raw,
        "cap": edge.cap,
        "f_e": edge.f_e,
    }


def serialize_umx_tick_ledger(ledger: UMXTickLedgerV1) -> Dict[str, object]:
    return {
        "tick": ledger.tick,
        "sum_pre_u": ledger.sum_pre_u,
        "sum_post_u": ledger.sum_post_u,
        "z_check": ledger.z_check,
        "pre_u": list(ledger.pre_u),
        "edges": [_serialize_edge_flux(edge) for edge in ledger.edges],
        "post_u": list(ledger.post_u),
    }


def _serialize_flux_summary(summary: FluxSummaryV1) -> Dict[str, int]:
    return {
        "e_id": summary.e_id,
        "f_e": summary.f_e,
    }


def serialize_loom_p_block(block: LoomPBlockV1) -> Dict[str, object]:
    return {
        "tick": block.tick,
        "seq": block.seq,
        "s_t": block.s_t,
        "C_t": block.C_t,
        "edge_flux_summary": [
            _serialize_flux_summary(summary) for summary in block.edge_flux_summary
        ],
    }


def _serialize_topology_edge_snapshot(edge: TopologyEdgeSnapshotV1) -> Dict[str, int]:
    return {
        "e_id": edge.e_id,
        "i": edge.i,
        "j": edge.j,
        "k": edge.k,
        "cap": edge.cap,
        "SC": edge.SC,
        "c": edge.c,
    }


def serialize_loom_i_block(block: LoomIBlockV1) -> Dict[str, object]:
    return {
        "tick": block.tick,
        "W": block.W,
        "C_t": block.C_t,
        "profile_version": block.profile_version,
        "post_u": list(block.post_u),
        "topology_snapshot": [
            _serialize_topology_edge_snapshot(edge) for edge in block.topology_snapshot
        ],
    }


def _serialize_apx_stream(stream: APXStreamV1) -> Dict[str, object]:
    return {
        "stream_id": stream.stream_id,
        "description": stream.description,
        "scheme": stream.scheme,
        "params": stream.params,
        "L_model": stream.L_model,
        "L_residual": stream.L_residual,
        "L_total": stream.L_total,
    }


def serialize_apx_manifest(manifest: APXManifestV1) -> Dict[str, object]:
    payload = {
        "apx_name": manifest.apx_name,
        "profile": manifest.profile,
        "manifest_check": manifest.manifest_check,
        "streams": [_serialize_apx_stream(stream) for stream in manifest.streams],
    }
    if manifest.apxi_view_ref is not None:
        payload["apxi_view_ref"] = manifest.apxi_view_ref
    return payload


def serialize_apxi_view(view: APXiViewV1) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "apx_name": view.apx_name,
        "window_id": view.window_id,
        "aeon_window_id": view.aeon_window_id,
        "residual_scheme": view.residual_scheme,
        "descriptors_by_stream": {},
    }

    for stream_name, breakdowns in sorted(view.descriptors_by_stream.items()):
        payload["descriptors_by_stream"][stream_name] = [
            {
                "descriptor": breakdown.descriptor.to_dict(),
                "residual_scheme": breakdown.residual_scheme,
                "L_model": breakdown.L_model,
                "L_residual": breakdown.L_residual,
                "L_total": breakdown.L_total,
            }
            for breakdown in breakdowns
        ]

    return payload


def serialize_scene_frame(scene: SceneFrameV1) -> Dict[str, object]:
    return {
        "gid": scene.gid,
        "run_id": scene.run_id,
        "tick": scene.tick,
        "nid": scene.nid,
        "pre_u": list(scene.pre_u),
        "post_u": list(scene.post_u),
        "ledger_ref": scene.ledger_ref,
        "C_prev": scene.C_prev,
        "C_t": scene.C_t,
        "window_id": scene.window_id,
        "manifest_check": scene.manifest_check,
        "nap_envelope_ref": scene.nap_envelope_ref,
        "meta": dict(scene.meta),
    }


def serialize_nap_envelope(envelope: NAPEnvelopeV1) -> Dict[str, object]:
    return {
        "v": envelope.v,
        "tick": envelope.tick,
        "gid": envelope.gid,
        "nid": envelope.nid,
        "layer": envelope.layer,
        "mode": envelope.mode,
        "payload_ref": envelope.payload_ref,
        "seq": envelope.seq,
        "prev_chain": envelope.prev_chain,
        "sig": envelope.sig,
    }


def serialize_uledger_entry(entry: ULedgerEntryV1) -> Dict[str, object]:
    return {
        "gid": entry.gid,
        "run_id": entry.run_id,
        "tick": entry.tick,
        "window_id": entry.window_id,
        "C_t": entry.C_t,
        "manifest_check": entry.manifest_check,
        "nap_envelope_hash": entry.nap_envelope_hash,
        "umx_ledger_hash": entry.umx_ledger_hash,
        "loom_block_hash": entry.loom_block_hash,
        "apx_manifest_hash": entry.apx_manifest_hash,
        "prev_entry_hash": entry.prev_entry_hash,
        "codex_library_hash": entry.codex_library_hash,
        "timestamp_utc": entry.timestamp_utc,
        "meta": dict(entry.meta),
    }


def _serialize_pfna_input(config_entry: object) -> Dict[str, object]:
    from gate.gate import PFNAInputV0

    pfna = config_entry
    if not isinstance(pfna, PFNAInputV0):  # pragma: no cover - defensive
        raise TypeError("serialize_pfna_input expects PFNAInputV0")

    return {
        "pfna_id": pfna.pfna_id,
        "gid": pfna.gid,
        "run_id": pfna.run_id,
        "tick": pfna.tick,
        "nid": pfna.nid,
        "values": list(pfna.values),
        **({"description": pfna.description} if pfna.description else {}),
    }


def serialize_gf01_run(result: GF01RunResult) -> Dict[str, object]:
    payload: Dict[str, object] = {
        "run_id": result.run_id,
        "ledgers": [serialize_umx_tick_ledger(ledger) for ledger in result.ledgers],
        "p_blocks": [serialize_loom_p_block(block) for block in result.p_blocks],
        "i_blocks": [serialize_loom_i_block(block) for block in result.i_blocks],
        "manifests": {
            name: serialize_apx_manifest(result.manifests[name])
            for name in sorted(result.manifests.keys())
        },
        "scenes": [serialize_scene_frame(scene) for scene in result.scenes],
        "envelopes": [serialize_nap_envelope(env) for env in result.envelopes],
        "u_ledger_entries": [serialize_uledger_entry(entry) for entry in result.u_ledger_entries],
    }

    if result.apxi_views:
        payload["apxi_views"] = {
            name: serialize_apxi_view(result.apxi_views[name])
            for name in sorted(result.apxi_views.keys())
        }

    return payload


def serialize_session_run(result: SessionRunResult) -> Dict[str, object]:
    """Canonical serialisation for Gate/TBP session runs with PFNA and NAP layers."""

    tick_payload = serialize_gf01_run(result.tick_result)
    tick_payload["ingress_envelopes"] = [
        serialize_nap_envelope(env) for env in result.tick_result.ingress_envelopes
    ]
    tick_payload["egress_envelopes"] = [
        serialize_nap_envelope(env) for env in result.tick_result.egress_envelopes
    ]

    config = result.config
    return {
        "config": {
            "run_id": config.run_id,
            "gid": config.topo.gid,
            "nid": config.nid,
            "total_ticks": config.total_ticks,
            "primary_window_id": config.primary_window_id,
            "window_ids": sorted(spec.window_id for spec in config.window_specs),
            "press_default_streams": [
                {
                    "name": stream.name,
                    "source": stream.source,
                    "scheme_hint": stream.scheme_hint,
                    "description": stream.description,
                }
                for stream in config.press_default_streams
            ],
            "pfna_inputs": [
                _serialize_pfna_input(pfna) for pfna in sorted(config.pfna_inputs, key=lambda p: (p.tick, p.pfna_id))
            ],
            "initial_state": list(config.initial_state),
        },
        "lifecycle_envelopes": [serialize_nap_envelope(env) for env in result.lifecycle_envelopes],
        "tick_result": tick_payload,
        **(
            {"metrics": result.metrics.to_dict()}
            if result.metrics is not None
            else {}
        ),
    }


def dumps_session_run(result: SessionRunResult) -> str:
    """Return canonical JSON string for a Gate/TBP session run."""

    return json.dumps(serialize_session_run(result), separators=(",", ":"), sort_keys=True)


def dumps_gf01_run(result: GF01RunResult) -> str:
    """Return a canonical JSON string for a GF-01 run result."""

    return json.dumps(serialize_gf01_run(result), separators=(",", ":"), sort_keys=True)

