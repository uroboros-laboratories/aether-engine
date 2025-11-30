"""U-ledger utilities.

This module collects canonical serialisation and hashing helpers used by
`ULedgerEntry_v1` construction and validation. The helpers are intentionally
minimal and deterministic so they can be reused across pillars without pulling
in extra dependencies.
"""

from .canonical import canonical_json_dumps, hash_record

__all__ = [
    "canonical_json_dumps",
    "hash_record",
    "ULedgerEntryV1",
    "build_uledger_entries",
]


def __getattr__(name):  # pragma: no cover - thin lazy import helper
    if name in {"ULedgerEntryV1", "build_uledger_entries"}:
        from .entry import ULedgerEntryV1, build_uledger_entries

        return {"ULedgerEntryV1": ULedgerEntryV1, "build_uledger_entries": build_uledger_entries}[
            name
        ]
    raise AttributeError(f"module 'uledger' has no attribute {name!r}")
