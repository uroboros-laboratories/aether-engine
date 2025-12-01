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
    "build_and_validate_uledger",
    "validate_uledger_chain",
    "ULedgerCheckpointV1",
]


def __getattr__(name):  # pragma: no cover - thin lazy import helper
    if name in {
        "ULedgerEntryV1",
        "build_uledger_entries",
        "build_and_validate_uledger",
        "validate_uledger_chain",
        "ULedgerCheckpointV1",
    }:
        from .entry import (
            ULedgerCheckpointV1,
            ULedgerEntryV1,
            build_and_validate_uledger,
            build_uledger_entries,
            validate_uledger_chain,
        )

        return {
            "ULedgerEntryV1": ULedgerEntryV1,
            "build_uledger_entries": build_uledger_entries,
            "build_and_validate_uledger": build_and_validate_uledger,
            "validate_uledger_chain": validate_uledger_chain,
            "ULedgerCheckpointV1": ULedgerCheckpointV1,
        }[name]
    raise AttributeError(f"module 'uledger' has no attribute {name!r}")
