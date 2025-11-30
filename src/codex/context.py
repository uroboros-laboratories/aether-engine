"""Codex context for ingesting run artefacts and counting patterns.

This observer-only context consumes UMX tick ledgers, Loom blocks,
APX manifests, and optional NAP envelopes to build lightweight
statistics that later Codex phases can use to identify motifs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

from gate import NAPEnvelopeV1
from core.slp import SLPEventV1
from loom.loom import LoomIBlockV1, LoomPBlockV1
from press import APXManifestV1, APXiViewV1
from press.aeon import AEONWindowGrammarV1, AEONWindowRegistry
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
    """Proposal record constructed from learned motifs and governance evaluation."""

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
    governance_status: str = "UNEVALUATED"
    violated_policies: tuple[str, ...] = field(default_factory=tuple)
    governance_scores: dict = field(default_factory=dict)
    governance_notes: dict = field(default_factory=dict)
    evaluated_at_tick: Optional[int] = None
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

        if self.governance_status not in {"UNEVALUATED", "OK", "SOFT_FAIL", "HARD_FAIL"}:
            raise ValueError(
                "governance_status must be one of UNEVALUATED, OK, SOFT_FAIL, HARD_FAIL"
            )
        if not isinstance(self.violated_policies, tuple):
            object.__setattr__(self, "violated_policies", tuple(self.violated_policies))
        for policy_id in self.violated_policies:
            if not isinstance(policy_id, str) or not policy_id:
                raise ValueError("violated_policies entries must be non-empty strings")
        if not isinstance(self.governance_scores, dict):
            raise ValueError("governance_scores must be a dictionary")
        if not isinstance(self.governance_notes, dict):
            raise ValueError("governance_notes must be a dictionary")
        if self.evaluated_at_tick is not None and (
            not isinstance(self.evaluated_at_tick, int) or self.evaluated_at_tick < 0
        ):
            raise ValueError("evaluated_at_tick must be a non-negative integer when provided")


@dataclass
class CodexRuntimeStats:
    """Runtime ingestion counters and lightweight pattern tallies."""

    total_ticks: int = 0
    total_p_blocks: int = 0
    total_i_blocks: int = 0
    total_manifests: int = 0
    total_envelopes: int = 0
    total_aeon_windows: int = 0
    total_apxi_views: int = 0
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
    slp_sequences: Dict[Tuple[str, Tuple[str, ...]], int] = field(default_factory=dict)
    slp_sequence_ticks: Dict[Tuple[str, Tuple[str, ...]], list[int]] = field(
        default_factory=dict
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

    def record_slp_sequence(
        self, *, gid: str, op_types: Sequence[str], ticks: Sequence[int]
    ) -> None:
        key = (gid, tuple(op_types))
        self.slp_sequences[key] = self.slp_sequences.get(key, 0) + 1
        self.slp_sequence_ticks.setdefault(key, []).extend(ticks)


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
        self._last_ingest_tick_range: Optional[tuple[int, int]] = None
        self._last_aeon_windows: Optional[AEONWindowGrammarV1] = None
        self._last_apxi_views: tuple[APXiViewV1, ...] = ()

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
        aeon_windows: Optional[AEONWindowGrammarV1 | AEONWindowRegistry] = None,
        apxi_views: Optional[Mapping[str, APXiViewV1] | Sequence[APXiViewV1]] = None,
        window_id: Optional[str] = None,
        slp_events: Optional[Sequence[SLPEventV1]] = None,
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

        if slp_events:
            op_types = [evt.op_type.value if hasattr(evt.op_type, "value") else str(evt.op_type) for evt in slp_events]
            ticks = [evt.tick_effective for evt in slp_events]
            self.runtime_stats.record_slp_sequence(gid=gid, op_types=op_types, ticks=ticks)

        if aeon_windows is not None:
            grammar = (
                aeon_windows.grammar if isinstance(aeon_windows, AEONWindowRegistry) else aeon_windows
            )
            self.runtime_stats.total_aeon_windows += len(grammar.base_windows) + len(grammar.derived_windows)
            self._last_aeon_windows = grammar

        if apxi_views is not None:
            if isinstance(apxi_views, Mapping):
                view_list = tuple(apxi_views.values())
            else:
                view_list = tuple(apxi_views)
            self.runtime_stats.total_apxi_views += len(view_list)
            self._last_apxi_views = view_list

        ticks = [ledger.tick for ledger in ledgers]
        start_tick, end_tick = min(ticks), max(ticks)
        resolved_window_id = window_id or f"{gid}_ticks_{start_tick}_{end_tick}"
        if not isinstance(resolved_window_id, str) or not resolved_window_id:
            raise ValueError("window_id must resolve to a non-empty string")

        self._last_ingest_gid = gid
        self._last_ingest_window = resolved_window_id
        self._last_ingest_tick_range = (start_tick, end_tick)

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

    def learn_slp_event_motifs(self, *, threshold: int = 1) -> list[CodexLibraryEntryV1]:
        """Emit observer-only motifs from ingested SLP event sequences."""

        if self._last_ingest_gid is None or self._last_ingest_window is None:
            raise ValueError("ingest must be called before learning motifs")

        accepted: list[CodexLibraryEntryV1] = []
        motif_index = len(self.library) + 1
        existing_keys = {
            tuple(entry.pattern_descriptor.get("op_types", []))
            for entry in self.library
            if entry.pattern_descriptor.get("type") == "slp_event_pattern_v1"
        }

        for key, count in sorted(self.runtime_stats.slp_sequences.items()):
            gid, op_types = key
            if count < threshold:
                continue

            ticks = self.runtime_stats.slp_sequence_ticks.get(key, [])
            created_at = min(ticks) if ticks else 0
            last_updated = max(ticks) if ticks else 0
            if tuple(op_types) in existing_keys:
                continue

            entry = CodexLibraryEntryV1(
                library_id=self.library_id,
                motif_id=f"MOTIF_{motif_index:04d}",
                profile=self.profile,
                source_gid=gid,
                source_window_id=self._last_ingest_window,
                pattern_descriptor={"type": "slp_event_pattern_v1", "op_types": list(op_types)},
                mdl_stats={
                    "L_self": len(op_types),
                    "L_usage": count,
                    "L_total": len(op_types) + count,
                    "delta_vs_baseline": -count,
                },
                usage_stats={"usage_count": count},
                created_at_tick=created_at,
                last_updated_tick=last_updated,
                meta={"runs": list(self.runtime_stats.ingested_runs)},
            )

            self.library.append(entry)
            accepted.append(entry)
            existing_keys.add(tuple(op_types))
            motif_index += 1

        return accepted

    def learn_apxi_descriptor_motifs(self) -> list[CodexLibraryEntryV1]:
        """Surface APXi descriptor motifs from the last ingest."""

        if self._last_ingest_gid is None or self._last_ingest_window is None:
            raise ValueError("ingest must be called before learning motifs")

        if not self._last_apxi_views:
            return []

        start_tick, end_tick = self._last_ingest_tick_range or (0, 0)

        accepted: list[CodexLibraryEntryV1] = []
        existing_keys = {
            (
                entry.pattern_descriptor.get("descriptor", {}).get("descriptor_id"),
                entry.pattern_descriptor.get("descriptor", {}).get("window_id"),
                entry.pattern_descriptor.get("descriptor", {}).get("stream_id"),
                entry.pattern_descriptor.get("residual_scheme"),
            )
            for entry in self.library
            if entry.pattern_descriptor.get("type") == "apxi_descriptor_v1"
        }

        motif_index = len(self.library) + 1
        for view in sorted(self._last_apxi_views, key=lambda v: v.view_id):
            for stream_name, breakdowns in sorted(view.descriptors_by_stream.items()):
                for breakdown in breakdowns:
                    descriptor = breakdown.descriptor
                    key = (
                        descriptor.descriptor_id,
                        descriptor.window_id,
                        descriptor.stream_id,
                        breakdown.residual_scheme,
                    )
                    if key in existing_keys:
                        continue

                    entry = CodexLibraryEntryV1(
                        library_id=self.library_id,
                        motif_id=f"MOTIF_{motif_index:04d}",
                        profile=self.profile,
                        source_gid=self._last_ingest_gid,
                        source_window_id=view.aeon_window_id or view.window_id,
                        pattern_descriptor={
                            "type": "apxi_descriptor_v1",
                            "descriptor": descriptor.to_dict(),
                            "residual_scheme": breakdown.residual_scheme,
                            "stream_id": stream_name,
                            "apx_name": view.apx_name,
                            "aeon_window_id": descriptor.window_id,
                        },
                        mdl_stats={
                            "L_self": breakdown.L_model,
                            "L_usage": breakdown.L_residual,
                            "L_total": breakdown.L_total,
                            "delta_vs_baseline": -breakdown.L_residual,
                        },
                        usage_stats={"usage_count": 1},
                        created_at_tick=start_tick,
                        last_updated_tick=end_tick,
                        meta={"runs": list(self.runtime_stats.ingested_runs)},
                    )

                    self.library.append(entry)
                    accepted.append(entry)
                    existing_keys.add(key)
                    motif_index += 1

        return accepted

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

