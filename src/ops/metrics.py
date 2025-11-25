"""Metrics collection helpers for Phase 3 governance work."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional


@dataclass(frozen=True)
class MetricsConfigV1:
    """Configuration for metrics collection.

    The Phase 3 surface keeps this intentionally small: a single enable flag
    that callers can toggle via config files or programmatic construction.
    """

    enabled: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")


@dataclass(frozen=True)
class MetricsSnapshotV1:
    """Structured metrics captured for a single run."""

    gid: str
    run_id: str
    total_ticks: int
    window_count: int
    nap_total: int
    nap_ingress: int
    nap_data: int
    nap_egress: int
    uledger_entries: int
    uledger_last_hash: Optional[str]
    apx_manifests: int
    apxi_views: int
    codex_motif_counts: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.total_ticks < 0:
            raise ValueError("total_ticks must be >= 0")
        if self.window_count < 0:
            raise ValueError("window_count must be >= 0")
        if self.nap_total < 0:
            raise ValueError("nap_total must be >= 0")
        if self.nap_ingress < 0 or self.nap_data < 0 or self.nap_egress < 0:
            raise ValueError("NAP layer counts must be >= 0")
        if self.uledger_entries < 0:
            raise ValueError("uledger_entries must be >= 0")
        if self.apx_manifests < 0 or self.apxi_views < 0:
            raise ValueError("manifest/view counts must be >= 0")
        if not isinstance(self.codex_motif_counts, Mapping):
            raise ValueError("codex_motif_counts must be a mapping")

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "gid": self.gid,
            "run_id": self.run_id,
            "total_ticks": self.total_ticks,
            "window_count": self.window_count,
            "nap_total": self.nap_total,
            "nap_ingress": self.nap_ingress,
            "nap_data": self.nap_data,
            "nap_egress": self.nap_egress,
            "uledger_entries": self.uledger_entries,
            "uledger_last_hash": self.uledger_last_hash,
            "apx_manifests": self.apx_manifests,
            "apxi_views": self.apxi_views,
        }
        if self.codex_motif_counts:
            payload["codex_motif_counts"] = dict(self.codex_motif_counts)
        return payload

