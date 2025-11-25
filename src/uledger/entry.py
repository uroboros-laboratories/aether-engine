"""ULedgerEntry construction and hashing helpers."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

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
        )

        prev_hash = hash_record(entry)
        entries.append(entry)

    return entries

