"""Codex context for ingesting run artefacts and counting patterns.

This observer-only context consumes UMX tick ledgers, Loom blocks,
APX manifests, and optional NAP envelopes to build lightweight
statistics that later Codex phases can use to identify motifs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

from gate import NAPEnvelopeV1
from loom.loom import LoomIBlockV1, LoomPBlockV1
from press import APXManifestV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1


@dataclass(frozen=True)
class CodexLibraryEntryV1:
    """Skeleton Codex library entry as sketched in the contracts."""

    library_id: str
    motif_id: str
    profile: str
    source_gid: str
    source_window_id: str
    pattern_descriptor: dict
    mdl_stats: dict
    usage_stats: dict
    created_at_tick: int
    last_updated_tick: int
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("library_id", self.library_id),
            ("motif_id", self.motif_id),
            ("profile", self.profile),
            ("source_gid", self.source_gid),
            ("source_window_id", self.source_window_id),
        ):
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be a non-empty string")

        for name, value in (
            ("created_at_tick", self.created_at_tick),
            ("last_updated_tick", self.last_updated_tick),
        ):
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer")


@dataclass(frozen=True)
class CodexProposalV1:
    """Observer-only proposal record constructed from learned motifs."""

    proposal_id: str
    library_id: str
    gid: str
    action: str
    expected_effect: dict
    created_at_tick: int
    status: str
    motif_id: Optional[str] = None
    target_window_id: Optional[str] = None
    target_location: dict = field(default_factory=dict)
    budget_effect: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("proposal_id", self.proposal_id),
            ("library_id", self.library_id),
            ("gid", self.gid),
        ):
            if not isinstance(value, str) or not value:
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.action, str) or self.action not in {
            "ADD",
            "PLACE",
            "MERGE",
            "RETIRE",
            "TUNE",
        }:
            raise ValueError("action must be one of ADD, PLACE, MERGE, RETIRE, TUNE")

        if not isinstance(self.status, str) or self.status not in {
            "PENDING",
            "ACCEPTED",
            "REJECTED",
        }:
            raise ValueError("status must be PENDING, ACCEPTED, or REJECTED")

        if not isinstance(self.created_at_tick, int) or self.created_at_tick < 0:
            raise ValueError("created_at_tick must be a non-negative integer")

        if self.motif_id is not None and (not isinstance(self.motif_id, str) or not self.motif_id):
            raise ValueError("motif_id, when provided, must be a non-empty string")

        if self.target_window_id is not None and (
            not isinstance(self.target_window_id, str) or not self.target_window_id
        ):
            raise ValueError("target_window_id, when provided, must be a non-empty string")


@dataclass
class CodexRuntimeStats:
    """Runtime ingestion counters and lightweight pattern tallies."""

    total_ticks: int = 0
    total_p_blocks: int = 0
    total_i_blocks: int = 0
    total_manifests: int = 0
    total_envelopes: int = 0
    ingested_runs: list[str] = field(default_factory=list)
    edge_pattern_counts: Dict[Tuple[int, int, int], int] = field(default_factory=dict)
    ledger_pattern_counts: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int] = field(
        default_factory=dict
    )
    ledger_pattern_ticks: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], list[int]] = (
        field(default_factory=dict)
    )
    ledger_pattern_edge_ids: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], Tuple[int, ...]] = (
        field(default_factory=dict)
    )

    def note_run(self, run_id: str) -> None:
        if run_id not in self.ingested_runs:
            self.ingested_runs.append(run_id)

    def _record_edge_patterns(self, edges: Sequence[EdgeFluxV1]) -> None:
        for edge in edges:
            key = (edge.e_id, edge.du, edge.f_e)
            self.edge_pattern_counts[key] = self.edge_pattern_counts.get(key, 0) + 1

    def _record_ledger_signature(self, edges: Sequence[EdgeFluxV1], tick: int) -> None:
        ordered = sorted(edges, key=lambda edge: edge.e_id)
        du_sig = tuple(edge.du for edge in ordered)
        f_e_sig = tuple(edge.f_e for edge in ordered)
        key = (du_sig, f_e_sig)
        self.ledger_pattern_counts[key] = self.ledger_pattern_counts.get(key, 0) + 1
        self.ledger_pattern_ticks.setdefault(key, []).append(tick)
        self.ledger_pattern_edge_ids.setdefault(key, tuple(edge.e_id for edge in ordered))

    def record_tick(self, edges: Sequence[EdgeFluxV1], tick: int) -> None:
        self.total_ticks += 1
        self._record_edge_patterns(edges)
        self._record_ledger_signature(edges, tick)


class CodexContext:
    """Observer-only Codex context for ingesting run traces."""

    def __init__(
        self,
        *,
        library_id: str,
        profile: str = "CMP-0",
        entries: Optional[Iterable[CodexLibraryEntryV1]] = None,
    ) -> None:
        if not isinstance(library_id, str) or not library_id:
            raise ValueError("library_id must be a non-empty string")
        if not isinstance(profile, str) or not profile:
            raise ValueError("profile must be a non-empty string")

        self.library_id = library_id
        self.profile = profile
        self.library: list[CodexLibraryEntryV1] = list(entries) if entries else []
        self.proposals: list[CodexProposalV1] = []
        self.runtime_stats = CodexRuntimeStats()
        self._last_ingest_window: Optional[str] = None
        self._last_ingest_gid: Optional[str] = None

    def ingest(
        self,
        *,
        gid: str,
        run_id: str,
        ledgers: Sequence[UMXTickLedgerV1],
        p_blocks: Sequence[LoomPBlockV1],
        i_blocks: Optional[Sequence[LoomIBlockV1]] = None,
        manifests: Optional[Mapping[str, APXManifestV1] | Sequence[APXManifestV1]] = None,
        envelopes: Optional[Sequence[NAPEnvelopeV1]] = None,
        window_id: Optional[str] = None,
    ) -> None:
        """Consume run artefacts and tally lightweight patterns.

        The ingest is tolerant of missing optional artefacts but enforces
        basic alignment (e.g., tick count must match the number of P-blocks).
        """

        if not gid or not isinstance(gid, str):
            raise ValueError("gid must be a non-empty string")
        if not run_id or not isinstance(run_id, str):
            raise ValueError("run_id must be a non-empty string")
        if not ledgers:
            raise ValueError("ledgers must be provided for ingestion")
        if len(ledgers) != len(p_blocks):
            raise ValueError("ledgers and p_blocks must have matching lengths")

        if envelopes is not None and len(envelopes) not in (0, len(ledgers)):
            raise ValueError("envelopes, when provided, must match tick count or be empty")

        self.runtime_stats.note_run(run_id)

        for ledger, p_block in zip(ledgers, p_blocks):
            if ledger.tick != p_block.tick:
                raise ValueError("ledger and p_block ticks must align")
            self.runtime_stats.record_tick(ledger.edges, ledger.tick)
            self.runtime_stats.total_p_blocks += 1

        if i_blocks:
            self.runtime_stats.total_i_blocks += len(i_blocks)

        if manifests:
            manifest_count = len(manifests) if isinstance(manifests, Mapping) else len(list(manifests))
            self.runtime_stats.total_manifests += manifest_count

        if envelopes:
            self.runtime_stats.total_envelopes += len(envelopes)

        ticks = [ledger.tick for ledger in ledgers]
        start_tick, end_tick = min(ticks), max(ticks)
        resolved_window_id = window_id or f"{gid}_ticks_{start_tick}_{end_tick}"
        if not isinstance(resolved_window_id, str) or not resolved_window_id:
            raise ValueError("window_id must resolve to a non-empty string")

        self._last_ingest_gid = gid
        self._last_ingest_window = resolved_window_id

    def learn_edge_flux_motifs(self, *, threshold: int = 2) -> list[CodexLibraryEntryV1]:
        """Detect repeated ledger signatures as simple edge-flux motifs."""

        if self._last_ingest_gid is None or self._last_ingest_window is None:
            raise ValueError("ingest must be called before learning motifs")

        accepted_entries: list[CodexLibraryEntryV1] = []
        existing_keys = {
            (
                tuple(entry.pattern_descriptor.get("edge_ids", [])),
                tuple(entry.pattern_descriptor.get("du_signature", [])),
                tuple(entry.pattern_descriptor.get("f_e_signature", [])),
            )
            for entry in self.library
            if entry.pattern_descriptor.get("type") == "edge_flux_pattern_v1"
        }
        motif_index = len(self.library) + 1
        for key in sorted(self.runtime_stats.ledger_pattern_counts.keys()):
            count = self.runtime_stats.ledger_pattern_counts[key]
            if count < threshold:
                continue

            du_sig, f_e_sig = key
            edge_ids = self.runtime_stats.ledger_pattern_edge_ids[key]
            ticks = self.runtime_stats.ledger_pattern_ticks[key]
            created_at = min(ticks)
            last_updated = max(ticks)

            mdl_self = len(edge_ids) + len(du_sig)
            mdl_usage = count
            mdl_total = mdl_self + mdl_usage
            delta_vs_baseline = -count

            motif_id = f"MOTIF_{motif_index:04d}"
            motif_index += 1

            entry = CodexLibraryEntryV1(
                library_id=self.library_id,
                motif_id=motif_id,
                profile=self.profile,
                source_gid=self._last_ingest_gid,
                source_window_id=self._last_ingest_window,
                pattern_descriptor={
                    "type": "edge_flux_pattern_v1",
                    "edge_ids": list(edge_ids),
                    "du_signature": list(du_sig),
                    "f_e_signature": list(f_e_sig),
                },
                mdl_stats={
                    "L_self": mdl_self,
                    "L_usage": mdl_usage,
                    "L_total": mdl_total,
                    "delta_vs_baseline": delta_vs_baseline,
                },
                usage_stats={
                    "usage_count": count,
                    "first_tick": created_at,
                    "last_tick": last_updated,
                },
                created_at_tick=created_at,
                last_updated_tick=last_updated,
                meta={"runs": list(self.runtime_stats.ingested_runs)},
            )
            descriptor_key = (tuple(edge_ids), tuple(du_sig), tuple(f_e_sig))
            if descriptor_key not in existing_keys:
                self.library.append(entry)
                existing_keys.add(descriptor_key)
                accepted_entries.append(entry)

        return accepted_entries

    def emit_proposals(self, *, usage_threshold: int = 2, default_action: str = "PLACE") -> list[CodexProposalV1]:
        """Emit CodexProposalV1 records for motifs that meet a usage threshold."""

        if self._last_ingest_gid is None or self._last_ingest_window is None:
            raise ValueError("ingest must be called before emitting proposals")

        proposals: list[CodexProposalV1] = []
        existing_keys = {
            (
                proposal.motif_id,
                proposal.target_window_id,
                proposal.action,
                tuple(proposal.target_location.get("edge_ids", [])),
            )
            for proposal in self.proposals
        }

        if default_action not in {"ADD", "PLACE", "MERGE", "RETIRE", "TUNE"}:
            raise ValueError("default_action must be a supported proposal action")

        proposal_index = len(self.proposals) + 1
        for entry in sorted(self.library, key=lambda item: item.motif_id):
            usage_count = int(entry.usage_stats.get("usage_count", 0))
            if usage_count < usage_threshold:
                continue

            descriptor = entry.pattern_descriptor
            edge_ids = descriptor.get("edge_ids", []) if isinstance(descriptor, dict) else []
            key = (entry.motif_id, entry.source_window_id, default_action, tuple(edge_ids))
            if key in existing_keys:
                continue

            proposal = CodexProposalV1(
                proposal_id=f"PROPOSAL_{proposal_index:04d}",
                library_id=self.library_id,
                motif_id=entry.motif_id,
                gid=self._last_ingest_gid,
                target_window_id=entry.source_window_id,
                target_location={
                    "edge_ids": list(edge_ids),
                    "profile": entry.profile,
                },
                action=default_action,
                expected_effect={
                    "delta_L_total": entry.mdl_stats.get("delta_vs_baseline", 0),
                    "notes": "edge_flux_pattern_v1",
                },
                budget_effect={},
                created_at_tick=entry.last_updated_tick,
                status="PENDING",
                meta={"runs": list(self.runtime_stats.ingested_runs)},
            )

            self.proposals.append(proposal)
            proposals.append(proposal)
            proposal_index += 1
            existing_keys.add(key)

        return proposals

