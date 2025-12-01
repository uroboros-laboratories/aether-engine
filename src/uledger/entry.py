"""ULedgerEntry construction and hashing helpers."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence

from gate import NAPEnvelopeV1
from loom.loom import LoomPBlockV1
from press import APXManifestV1
from umx.tick_ledger import UMXTickLedgerV1

from .canonical import hash_record


def _manifest_hash_payload(manifest: APXManifestV1) -> dict:
    payload = dataclasses.asdict(manifest)
    if payload.get("apxi_view_ref") is None:
        payload.pop("apxi_view_ref", None)
    return payload


@dataclass(frozen=True)
class ULedgerEntryV1:
    """Anchor record linking per-tick pillar outputs into a hash chain."""

    gid: str
    run_id: str
    tick: int
    window_id: str
    C_t: int
    manifest_check: int
    nap_envelope_hash: str
    umx_ledger_hash: str
    loom_block_hash: str
    apx_manifest_hash: str
    prev_entry_hash: Optional[str] = None
    codex_library_hash: Optional[str] = None
    timestamp_utc: Optional[str] = None
    meta: Dict[str, object] = field(default_factory=dict)
    slp_event_refs: tuple[str, ...] = field(default_factory=tuple)
    topology_version: str = ""
    policy_set_hash: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.gid:
            raise ValueError("gid must be provided")
        if not self.run_id:
            raise ValueError("run_id must be provided")
        if self.tick < 1:
            raise ValueError("tick must be >= 1")
        if not self.window_id:
            raise ValueError("window_id must be provided")
        if not isinstance(self.meta, dict):
            raise ValueError("meta must be a dictionary")
        for event_id in self.slp_event_refs:
            if not isinstance(event_id, str) or not event_id:
                raise ValueError("slp_event_refs must be non-empty strings when provided")
        if not isinstance(self.topology_version, str):
            raise ValueError("topology_version must be a string")
        if self.policy_set_hash is not None and (
            not isinstance(self.policy_set_hash, str) or not self.policy_set_hash
        ):
            raise ValueError("policy_set_hash must be a non-empty string when provided")


def _validate_alignment(
    ledgers: Sequence[UMXTickLedgerV1],
    p_blocks: Sequence[LoomPBlockV1],
    envelopes: Sequence[NAPEnvelopeV1],
) -> None:
    if not (len(ledgers) == len(p_blocks) == len(envelopes)):
        raise ValueError("ledgers, p_blocks, and envelopes must align one-to-one")

    for ledger, p_block, envelope in zip(ledgers, p_blocks, envelopes):
        if ledger.tick != p_block.tick or ledger.tick != envelope.tick:
            raise ValueError("ledger, p_block, and envelope ticks must match")


def build_uledger_entries(
    *,
    gid: str,
    run_id: str,
    window_id: str,
    ledgers: Sequence[UMXTickLedgerV1],
    p_blocks: Sequence[LoomPBlockV1],
    envelopes: Sequence[NAPEnvelopeV1],
    manifest: APXManifestV1,
    start_prev_hash: Optional[str] = None,
    slp_events_by_tick: Optional[Mapping[int, Sequence[str]]] = None,
    policy_set_hash: Optional[str] = None,
    governance_meta: Optional[Mapping[str, object]] = None,
) -> List[ULedgerEntryV1]:
    """Construct a ULedgerEntry chain for a run segment.

    Hashes are computed using canonical serialisation for each linked artefact:
    - UMX tick ledger
    - Loom P-block
    - NAP envelope
    - APX manifest (shared across ticks within the window)
    """

    _validate_alignment(ledgers, p_blocks, envelopes)

    manifest_hash = hash_record(_manifest_hash_payload(manifest))
    prev_hash = start_prev_hash
    entries: List[ULedgerEntryV1] = []
    last_tick = 0

    for ledger, p_block, envelope in zip(ledgers, p_blocks, envelopes):
        if ledger.tick <= last_tick:
            raise ValueError("ledgers must be in strictly increasing tick order")
        last_tick = ledger.tick
        slp_refs = tuple(sorted(slp_events_by_tick.get(ledger.tick, ()))) if slp_events_by_tick else tuple()
        entry = ULedgerEntryV1(
            gid=gid,
            run_id=run_id,
            tick=ledger.tick,
            window_id=window_id,
            C_t=p_block.C_t,
            manifest_check=manifest.manifest_check,
            nap_envelope_hash=hash_record(envelope),
            umx_ledger_hash=hash_record(ledger),
            loom_block_hash=hash_record(p_block),
            apx_manifest_hash=manifest_hash,
            prev_entry_hash=prev_hash,
            slp_event_refs=slp_refs,
            topology_version=p_block.topology_version,
            policy_set_hash=policy_set_hash,
            meta=dict(governance_meta or {}),
        )

        prev_hash = hash_record(entry)
        entries.append(entry)

    return entries


@dataclass(frozen=True)
class ULedgerCheckpointV1:
    """Summary checkpoint for a ULedgerEntry chain segment."""

    gid: str
    run_id: str
    window_id: str
    start_tick: int
    end_tick: int
    entry_count: int
    head_hash: str
    manifest_hash: str
    policy_set_hash: Optional[str] = None

    def __post_init__(self) -> None:
        if self.start_tick < 1 or self.end_tick < self.start_tick:
            raise ValueError("start_tick must be >= 1 and <= end_tick")
        if self.entry_count < 1:
            raise ValueError("entry_count must be >= 1")
        if not self.head_hash or not isinstance(self.head_hash, str):
            raise ValueError("head_hash must be a non-empty string")
        if not self.manifest_hash or not isinstance(self.manifest_hash, str):
            raise ValueError("manifest_hash must be a non-empty string")
        if not self.gid or not self.run_id or not self.window_id:
            raise ValueError("gid, run_id, and window_id must be provided")
        if self.policy_set_hash is not None and (
            not isinstance(self.policy_set_hash, str) or not self.policy_set_hash
        ):
            raise ValueError("policy_set_hash must be a non-empty string when provided")


def validate_uledger_chain(
    entries: Sequence[ULedgerEntryV1],
    *,
    expected_gid: Optional[str] = None,
    expected_run_id: Optional[str] = None,
    expected_window_id: Optional[str] = None,
    manifest: Optional[APXManifestV1] = None,
    start_prev_hash: Optional[str] = None,
    require_contiguous_ticks: bool = True,
) -> ULedgerCheckpointV1:
    """Validate a sequence of ULedgerEntryV1 records and return a checkpoint."""

    if not entries:
        raise ValueError("entries must not be empty")

    ticks_seen: List[int] = []
    manifest_hash = None
    last_hash = start_prev_hash
    last_tick = 0

    for idx, entry in enumerate(entries):
        if expected_gid and entry.gid != expected_gid:
            raise ValueError("gid mismatch in ledger entries")
        if expected_run_id and entry.run_id != expected_run_id:
            raise ValueError("run_id mismatch in ledger entries")
        if expected_window_id and entry.window_id != expected_window_id:
            raise ValueError("window_id mismatch in ledger entries")

        if manifest:
            manifest_hash = manifest_hash or hash_record(_manifest_hash_payload(manifest))
            if entry.apx_manifest_hash != manifest_hash:
                raise ValueError("APX manifest hash mismatch in ledger entries")
            if entry.manifest_check != manifest.manifest_check:
                raise ValueError("manifest_check mismatch in ledger entries")

        if require_contiguous_ticks and entry.tick != last_tick + 1:
            raise ValueError("ledger ticks must be contiguous and increasing")
        if entry.tick <= last_tick:
            raise ValueError("ledger ticks must strictly increase")
        last_tick = entry.tick
        ticks_seen.append(entry.tick)

        expected_prev = last_hash
        if expected_prev != entry.prev_entry_hash:
            raise ValueError("prev_entry_hash does not match chain state")

        last_hash = hash_record(entry)

        if idx == 0:
            manifest_hash = manifest_hash or entry.apx_manifest_hash
        else:
            if entry.apx_manifest_hash != manifest_hash:
                raise ValueError("apx_manifest_hash must remain constant across the window")
        if entries[0].policy_set_hash != entry.policy_set_hash:
            raise ValueError("policy_set_hash must be consistent across entries")

    return ULedgerCheckpointV1(
        gid=entries[0].gid,
        run_id=entries[0].run_id,
        window_id=entries[0].window_id,
        start_tick=min(ticks_seen),
        end_tick=max(ticks_seen),
        entry_count=len(entries),
        head_hash=last_hash or hash_record(entries[-1]),
        manifest_hash=manifest_hash or entries[-1].apx_manifest_hash,
        policy_set_hash=entries[0].policy_set_hash,
    )


def build_and_validate_uledger(
    *,
    gid: str,
    run_id: str,
    window_id: str,
    ledgers: Sequence[UMXTickLedgerV1],
    p_blocks: Sequence[LoomPBlockV1],
    envelopes: Sequence[NAPEnvelopeV1],
    manifest: APXManifestV1,
    start_prev_hash: Optional[str] = None,
    slp_events_by_tick: Optional[Mapping[int, Sequence[str]]] = None,
    policy_set_hash: Optional[str] = None,
    governance_meta: Optional[Mapping[str, object]] = None,
    require_contiguous_ticks: bool = True,
) -> tuple[List[ULedgerEntryV1], ULedgerCheckpointV1]:
    """Build ULedger entries then validate them, returning entries + checkpoint."""

    entries = build_uledger_entries(
        gid=gid,
        run_id=run_id,
        window_id=window_id,
        ledgers=ledgers,
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=manifest,
        start_prev_hash=start_prev_hash,
        slp_events_by_tick=slp_events_by_tick,
        policy_set_hash=policy_set_hash,
        governance_meta=governance_meta,
    )

    checkpoint = validate_uledger_chain(
        entries,
        expected_gid=gid,
        expected_run_id=run_id,
        expected_window_id=window_id,
        manifest=manifest,
        start_prev_hash=start_prev_hash,
        require_contiguous_ticks=require_contiguous_ticks,
    )

    return entries, checkpoint

