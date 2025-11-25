"""Canonical serialisation and hashing helpers for the U-ledger.

These utilities provide deterministic JSON output (sorted keys, no whitespace)
and a fixed SHA-256 hash for any supported record composed of primitive Python
types. They are intended to back `ULedgerEntry_v1` and related hashing within
SPEC-005.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from typing import Any, Dict


def _normalize(obj: Any) -> Any:
    """Return a JSON-compatible structure with deterministic ordering.

    Supported primitives:
    - ``dict`` (string keys will be sorted)
    - ``list``/``tuple``
    - ``str``
    - ``int``
    - ``bool``
    - ``None``

    Dataclasses are converted via ``dataclasses.asdict``. Any other type raises
    ``TypeError`` to keep the serialisation predictable.
    """

    if dataclasses.is_dataclass(obj):
        obj = dataclasses.asdict(obj)

    if isinstance(obj, dict):
        normalized: Dict[str, Any] = {}
        for key in sorted(obj.keys()):
            normalized[str(key)] = _normalize(obj[key])
        return normalized

    if isinstance(obj, (list, tuple)):
        return [_normalize(item) for item in obj]

    if isinstance(obj, bool):
        return obj

    if isinstance(obj, int):
        return obj

    if isinstance(obj, str):
        return obj

    if obj is None:
        return None

    raise TypeError(f"Unsupported type for canonical serialisation: {type(obj)!r}")


def canonical_json_dumps(record: Any) -> str:
    """Return canonical JSON for ``record`` using sorted keys and no whitespace."""

    normalized = _normalize(record)
    return json.dumps(normalized, separators=(",", ":"), sort_keys=True, ensure_ascii=False)


def hash_record(record: Any, *, algorithm: str = "sha256") -> str:
    """Return the SHA-256 hash of a canonically serialised ``record``.

    Only ``sha256`` is supported for now; requests for other algorithms raise
    ``ValueError`` to keep the hashing behaviour explicit and spec-aligned.
    """

    algo = algorithm.lower()
    if algo != "sha256":
        raise ValueError("Only sha256 is supported for canonical hashing")

    canonical = canonical_json_dumps(record)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return digest
