"""Integrity tooling for Loom P-/I-blocks.

This module canonicalizes blocks, computes hash-chain/Merkle roots, and
optionally persists serialized blocks for replay/rollback windows. The goal is
to provide authenticated replay hooks required by the Loom portion of the
master spec while keeping the implementation small and deterministic.
"""
from __future__ import annotations

import json
import os
import pathlib
import hashlib
import struct
import zlib
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from .loom import LoomIBlockV1, LoomPBlockV1


def _stable_dumps(payload: Mapping) -> str:
    """Serialize mappings deterministically for hashing."""

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _hash_payload(payload: Mapping) -> str:
    return hashlib.sha256(_stable_dumps(payload).encode("utf-8")).hexdigest()


def _hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonicalize_p_block(p_block: LoomPBlockV1, prev_hash: Optional[str]) -> Dict:
    """Return a deterministic mapping for a P-block including the prev hash."""

    fluxes = sorted(
        (
            {
                "e_id": flux.e_id,
                "f_e": flux.f_e,
            }
            for flux in p_block.edge_flux_summary
        ),
        key=lambda item: item["e_id"],
    )

    return {
        "gid": p_block.gid,
        "tick": p_block.tick,
        "seq": p_block.seq,
        "s_t": p_block.s_t,
        "C_t": p_block.C_t,
        "topology_version": p_block.topology_version,
        "edge_flux_summary": fluxes,
        "prev_hash": prev_hash,
    }


def canonicalize_i_block(
    i_block: LoomIBlockV1, merkle_root: str, prev_hash: Optional[str]
) -> Dict:
    """Return a deterministic mapping for an I-block including Merkle and prev hash."""

    topo_snapshot = sorted(
        (
            {
                "e_id": edge.e_id,
                "i": edge.i,
                "j": edge.j,
                "k": edge.k,
                "cap": edge.cap,
                "SC": edge.SC,
                "c": edge.c,
            }
            for edge in i_block.topology_snapshot
        ),
        key=lambda item: item["e_id"],
    )

    return {
        "gid": i_block.gid,
        "tick": i_block.tick,
        "W": i_block.W,
        "C_t": i_block.C_t,
        "profile_version": i_block.profile_version,
        "topology_version": i_block.topology_version,
        "post_u": list(i_block.post_u),
        "topology_snapshot": topo_snapshot,
        "merkle_root": merkle_root,
        "prev_hash": prev_hash,
    }


def merkle_root(leaves: Iterable[str]) -> str:
    """Compute a simple SHA-256 Merkle root from an iterable of leaf hashes."""

    layer = [leaf for leaf in leaves]
    if not layer:
        return hashlib.sha256(b"").hexdigest()

    while len(layer) > 1:
        next_layer: List[str] = []
        for idx in range(0, len(layer), 2):
            left = layer[idx]
            right = layer[idx + 1] if idx + 1 < len(layer) else layer[idx]
            joined = (left + right).encode("utf-8")
            next_layer.append(hashlib.sha256(joined).hexdigest())
        layer = next_layer
    return layer[0]


MAGIC = b"LMB1"
VERSION = 1
FLAG_COMPRESS = 0x01
_HEADER_STRUCT = struct.Struct(">4sBBBII")


def _encode_block(canonical: Mapping, block_type: str, compress: bool = True) -> bytes:
    """Encode a canonical Loom block into a binary envelope.

    The envelope is Press-ready: stable JSON bytes are optionally compressed and
    preceded by a fixed header.

    Header layout (big endian):
        - 4s: magic ``b"LMB1"``
        - B: version (currently ``1``)
        - B: block type (``ord('P')`` or ``ord('I')``)
        - B: flags (bit 0 == compressed)
        - I: uncompressed length
        - I: stored length
    """

    if block_type not in {"P", "I"}:
        raise ValueError("block_type must be 'P' or 'I'")

    raw = _stable_dumps(canonical).encode("utf-8")
    flags = 0
    payload = raw
    if compress:
        payload = zlib.compress(raw)
        flags |= FLAG_COMPRESS

    header = _HEADER_STRUCT.pack(MAGIC, VERSION, ord(block_type), flags, len(raw), len(payload))
    return header + payload


def _decode_block(blob: bytes, expected_type: str) -> Tuple[Mapping, str]:
    """Decode a binary envelope back to its canonical mapping and hash.

    Returns ``(canonical_mapping, payload_hash)`` where ``payload_hash`` is the
    SHA-256 of the *stored* payload (compressed or raw, matching what was on
    disk). The hash is useful for Press manifests.
    """

    if len(blob) < _HEADER_STRUCT.size:
        raise ValueError("blob too small to contain Loom block header")

    magic, version, block_type, flags, raw_len, stored_len = _HEADER_STRUCT.unpack(
        blob[: _HEADER_STRUCT.size]
    )

    if magic != MAGIC:
        raise ValueError("invalid Loom block magic")
    if version != VERSION:
        raise ValueError(f"unsupported Loom block version: {version}")

    block_chr = chr(block_type)
    if block_chr != expected_type:
        raise ValueError(f"expected block type {expected_type} but found {block_chr}")

    payload = blob[_HEADER_STRUCT.size :]
    if len(payload) != stored_len:
        raise ValueError("payload length does not match header")

    payload_hash = _hash_bytes(payload)
    if flags & FLAG_COMPRESS:
        payload = zlib.decompress(payload)

    if len(payload) != raw_len:
        raise ValueError("decoded payload length does not match header")

    canonical = json.loads(payload.decode("utf-8"))
    return canonical, payload_hash


def _payload_from_blob(blob: bytes) -> bytes:
    return blob[_HEADER_STRUCT.size :]


def encode_p_block_binary(canonical: Mapping, compress: bool = True) -> bytes:
    return _encode_block(canonical, "P", compress=compress)


def encode_i_block_binary(canonical: Mapping, compress: bool = True) -> bytes:
    return _encode_block(canonical, "I", compress=compress)


def decode_p_block_binary(blob: bytes) -> Tuple[Mapping, str]:
    return _decode_block(blob, "P")


def decode_i_block_binary(blob: bytes) -> Tuple[Mapping, str]:
    return _decode_block(blob, "I")


@dataclass(frozen=True)
class LoomChainState:
    """Summary of the chain tip for export to NAP envelopes or diagnostics."""

    height: int
    tip_hash: Optional[str]
    latest_merkle_root: Optional[str]
    latest_iblock_tick: Optional[int]


class LoomChainRecorder:
    """Track P-/I-block hashes and optional persistence for replay/rollback."""

    def __init__(self, store: Optional["LoomBlockStore"] = None):
        self.store = store
        self.p_hashes: List[str] = []
        self.i_blocks: Dict[int, str] = {}
        self._prev_hash: Optional[str] = None

    def record_p_block(self, p_block: LoomPBlockV1) -> str:
        canonical = canonicalize_p_block(p_block, prev_hash=self._prev_hash)
        p_hash = _hash_payload(canonical)
        self.p_hashes.append(p_hash)
        self._prev_hash = p_hash
        if self.store:
            self.store.write_p_block(p_block, canonical, p_hash)
        return p_hash

    def record_i_block(self, i_block: LoomIBlockV1, window_hashes: Iterable[str]) -> str:
        root = merkle_root(list(window_hashes))
        canonical = canonicalize_i_block(i_block, merkle_root=root, prev_hash=self._prev_hash)
        i_hash = _hash_payload(canonical)
        self.i_blocks[i_block.tick] = root
        if self.store:
            self.store.write_i_block(i_block, canonical, i_hash)
        self._prev_hash = i_hash
        return root

    def chain_state(self) -> LoomChainState:
        return LoomChainState(
            height=len(self.p_hashes),
            tip_hash=self._prev_hash,
            latest_merkle_root=self.i_blocks[max(self.i_blocks.keys())] if self.i_blocks else None,
            latest_iblock_tick=max(self.i_blocks.keys()) if self.i_blocks else None,
        )


class LoomBlockStore:
    """Persist Loom blocks to disk with a simple JSON index and rollback pruning."""

    def __init__(self, root: pathlib.Path, rollback_window: Optional[int] = None):
        self.root = pathlib.Path(root)
        self.rollback_window = rollback_window
        self.p_dir = self.root / "pblocks"
        self.i_dir = self.root / "iblocks"
        self.index_path = self.root / "index.json"
        self.root.mkdir(parents=True, exist_ok=True)
        self.p_dir.mkdir(exist_ok=True)
        self.i_dir.mkdir(exist_ok=True)
        if not self.index_path.exists():
            self.index_path.write_text(_stable_dumps({"p": [], "i": []}))

    def _load_index(self) -> Dict[str, List[Dict]]:
        return json.loads(self.index_path.read_text())

    def _write_index(self, data: Dict[str, List[Dict]]) -> None:
        self.index_path.write_text(_stable_dumps(data))

    def write_p_block(self, p_block: LoomPBlockV1, canonical: Mapping, p_hash: str) -> None:
        json_path = self.p_dir / f"tick_{p_block.tick}.json"
        bin_path = self.p_dir / f"tick_{p_block.tick}.bin"

        payload = {
            "type": "P",
            "hash": p_hash,
            "block": canonical,
        }
        json_path.write_text(_stable_dumps(payload))

        bin_blob = encode_p_block_binary(canonical)
        bin_path.write_bytes(bin_blob)
        payload_hash = _hash_bytes(_payload_from_blob(bin_blob))
        envelope_hash = _hash_bytes(bin_blob)

        index = self._load_index()
        index_entry = {
            "tick": p_block.tick,
            "hash": p_hash,
            "path": str(json_path),
            "bin_path": str(bin_path),
            "bin_hash": payload_hash,
            "bin_envelope_hash": envelope_hash,
            "bin_size": len(bin_blob),
        }
        index["p"].append(index_entry)
        index["p"] = sorted(index["p"], key=lambda item: item["tick"])
        index["p"] = self._prune(index["p"], self.rollback_window)
        self._write_index(index)

    def write_i_block(self, i_block: LoomIBlockV1, canonical: Mapping, i_hash: str) -> None:
        json_path = self.i_dir / f"tick_{i_block.tick}.json"
        bin_path = self.i_dir / f"tick_{i_block.tick}.bin"

        payload = {
            "type": "I",
            "hash": i_hash,
            "block": canonical,
        }
        json_path.write_text(_stable_dumps(payload))

        bin_blob = encode_i_block_binary(canonical)
        bin_path.write_bytes(bin_blob)
        payload_hash = _hash_bytes(_payload_from_blob(bin_blob))
        envelope_hash = _hash_bytes(bin_blob)

        index = self._load_index()
        index_entry = {
            "tick": i_block.tick,
            "hash": i_hash,
            "path": str(json_path),
            "bin_path": str(bin_path),
            "bin_hash": payload_hash,
            "bin_envelope_hash": envelope_hash,
            "bin_size": len(bin_blob),
        }
        index["i"].append(index_entry)
        index["i"] = sorted(index["i"], key=lambda item: item["tick"])
        index["i"] = self._prune(index["i"], self.rollback_window)
        self._write_index(index)

    def _prune(self, entries: List[Dict], window: Optional[int]) -> List[Dict]:
        if window is None:
            return entries
        if len(entries) <= window:
            return entries
        # Drop the oldest entries beyond the window and delete their files.
        to_remove = entries[:-window]
        for entry in to_remove:
            try:
                os.remove(entry["path"])
            except FileNotFoundError:
                pass
            bin_path = entry.get("bin_path")
            if bin_path:
                try:
                    os.remove(bin_path)
                except FileNotFoundError:
                    pass
        return entries[-window:]

    def load_p_block(self, tick: int) -> Mapping:
        index = self._load_index()["p"]
        for entry in index:
            if entry["tick"] == tick:
                return json.loads(pathlib.Path(entry["path"]).read_text())
        raise FileNotFoundError(f"No stored P-block for tick {tick}")

    def load_i_block(self, tick: int) -> Mapping:
        index = self._load_index()["i"]
        for entry in index:
            if entry["tick"] == tick:
                return json.loads(pathlib.Path(entry["path"]).read_text())
        raise FileNotFoundError(f"No stored I-block for tick {tick}")

    def load_p_block_binary(self, tick: int) -> Tuple[Mapping, str]:
        index = self._load_index()["p"]
        for entry in index:
            if entry["tick"] == tick:
                blob = pathlib.Path(entry["bin_path"]).read_bytes()
                return decode_p_block_binary(blob)
        raise FileNotFoundError(f"No stored P-block binary for tick {tick}")

    def load_i_block_binary(self, tick: int) -> Tuple[Mapping, str]:
        index = self._load_index()["i"]
        for entry in index:
            if entry["tick"] == tick:
                blob = pathlib.Path(entry["bin_path"]).read_bytes()
                return decode_i_block_binary(blob)
        raise FileNotFoundError(f"No stored I-block binary for tick {tick}")

    def press_pointer(self, block_type: str, tick: int) -> Mapping:
        """Return a Press-ready pointer for the requested block.

        The pointer exposes the deterministic binary path and hash so Press
        manifests can reference the stored Loom block without re-encoding.
        """

        if block_type not in {"P", "I"}:
            raise ValueError("block_type must be 'P' or 'I'")

        key = "p" if block_type == "P" else "i"
        index = self._load_index()[key]
        for entry in index:
            if entry["tick"] == tick:
                return {
                    "tick": entry["tick"],
                    "type": block_type,
                    "hash": entry["hash"],
                    "binary_hash": entry["bin_hash"],
                    "binary_envelope_hash": entry.get("bin_envelope_hash"),
                    "binary_path": entry["bin_path"],
                    "binary_size": entry["bin_size"],
                    "schema_version": VERSION,
                    "compressed": True,
                }
        raise FileNotFoundError(f"No stored {block_type}-block for tick {tick}")

    def replay_index(self) -> Dict[str, List[Dict]]:
        return self._load_index()
