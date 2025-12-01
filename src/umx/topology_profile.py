"""Topology and profile records for CMP-0.

Implements `TopologyProfile_v1`, `NodeProfile_v1`, and `EdgeProfile_v1`
as described in the contracts. Includes a helper for the GF-01 topology
card so tests can consume a single canonical definition.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Union


@dataclass(frozen=True)
class NodeProfileV1:
    """Per-node profile information.

    Follows the `NodeProfile_v1` contract under `TopologyProfile_v1`.
    """

    node_id: int
    label: str = ""
    attrs: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class EdgeProfileV1:
    """Per-edge profile information matching the CMP-0 contract."""

    e_id: int
    i: int
    j: int
    k: int
    cap: int
    SC: int
    c: int = 0
    causal_radius: int | None = None
    attrs: Dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class TopologyProfileV1:
    """Static graph structure used by the UMX engine."""

    gid: str
    profile: str
    N: int
    nodes: List[NodeProfileV1]
    edges: List[EdgeProfileV1]
    SC: int
    causal_radius: int = 0
    max_edge_cap: int | None = None
    nap_ref: str | None = None
    meta: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_nodes()
        self._validate_edges()
        if self.SC <= 0:
            raise ValueError("SC must be a positive integer")
        if self.causal_radius < 0:
            raise ValueError("causal_radius must be non-negative")
        if self.max_edge_cap is not None and (
            not isinstance(self.max_edge_cap, int) or self.max_edge_cap <= 0
        ):
            raise ValueError("max_edge_cap must be a positive integer when provided")

    def _validate_nodes(self) -> None:
        node_ids = [_ensure_int(node.node_id, "node.node_id") for node in self.nodes]
        expected = list(range(1, self.N + 1))
        if node_ids != expected:
            raise ValueError("Nodes must be contiguous from 1..N in ascending order")

    def _validate_edges(self) -> None:
        edge_ids = [edge.e_id for edge in self.edges]
        expected_ids = list(range(1, len(self.edges) + 1))
        if edge_ids != expected_ids:
            raise ValueError("Edges must be contiguous from 1..E in ascending order")
        for edge in self.edges:
            _ensure_int(edge.e_id, "edge.e_id")
            if not (1 <= edge.i <= self.N) or not (1 <= edge.j <= self.N):
                raise ValueError("Edge endpoints must reference valid node IDs")
            for field_name, value in {
                "k": edge.k,
                "cap": edge.cap,
                "SC": edge.SC,
                "c": edge.c,
            }.items():
                _ensure_int(value, f"edge.{field_name}")
            if edge.SC <= 0:
                raise ValueError("Edge SC must be positive")
            if edge.SC != self.SC:
                raise ValueError("Each edge SC must match the topology SC")
            if edge.causal_radius is not None and (
                not isinstance(edge.causal_radius, int) or edge.causal_radius <= 0
            ):
                raise ValueError("edge.causal_radius must be a positive integer when provided")


def gf01_topology_profile() -> TopologyProfileV1:
    """Return the canonical GF-01 topology for CMP-0.

    The edge ordering and k-values match the GF-01 topology card
    in the worked examples PDF. Caps are effectively unbounded in the
    paper example, represented here with a large sentinel integer.
    """

    fixture_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "fixtures"
        / "topologies"
        / "gf01_topology_profile.json"
    )
    return load_topology_profile(fixture_path)


def _ensure_int(value: Any, field_name: str) -> int:
    """Validate integer fields and reject booleans explicitly.

    The contract expects integers for all numeric fields. ``bool`` is an
    ``int`` subclass in Python, so we guard against that to catch malformed
    profiles.
    """

    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    return value


def _load_node(entry: Mapping[str, Any]) -> NodeProfileV1:
    node_id = _ensure_int(entry.get("node_id"), "node.node_id")
    label = entry.get("label", "")
    if not isinstance(label, str):
        raise ValueError("node.label must be a string")
    attrs = entry.get("attrs", {})
    if not isinstance(attrs, Mapping):
        raise ValueError("node.attrs must be an object if provided")
    return NodeProfileV1(node_id=node_id, label=label, attrs=dict(attrs))


def _load_edge(entry: Mapping[str, Any]) -> EdgeProfileV1:
    e_id = _ensure_int(entry.get("e_id"), "edge.e_id")
    i = _ensure_int(entry.get("i"), "edge.i")
    j = _ensure_int(entry.get("j"), "edge.j")
    k = _ensure_int(entry.get("k"), "edge.k")
    cap = _ensure_int(entry.get("cap"), "edge.cap")
    sc = _ensure_int(entry.get("SC"), "edge.SC")
    c = _ensure_int(entry.get("c", 0), "edge.c")
    causal_radius = entry.get("causal_radius")
    if causal_radius is not None:
        causal_radius = _ensure_int(causal_radius, "edge.causal_radius")
        if causal_radius <= 0:
            raise ValueError("edge.causal_radius must be positive when provided")
    attrs = entry.get("attrs", {})
    if not isinstance(attrs, Mapping):
        raise ValueError("edge.attrs must be an object if provided")
    return EdgeProfileV1(
        e_id=e_id,
        i=i,
        j=j,
        k=k,
        cap=cap,
        SC=sc,
        c=c,
        causal_radius=causal_radius,
        attrs=dict(attrs),
    )


def topology_profile_from_dict(data: Mapping[str, Any]) -> TopologyProfileV1:
    """Construct a :class:`TopologyProfileV1` from a mapping.

    The loader is strict and will raise ``ValueError`` with descriptive
    messages when required fields are missing or contain the wrong type. The
    resulting dataclass runs the built-in structural validation to ensure
    contiguity and endpoint correctness.
    """

    if not isinstance(data, Mapping):
        raise ValueError("TopologyProfile data must be a mapping")

    try:
        gid = str(data["gid"])
        profile = str(data["profile"])
        N = _ensure_int(data["N"], "N")
        SC = _ensure_int(data["SC"], "SC")
        causal_radius = _ensure_int(data.get("causal_radius", 0), "causal_radius")
    except KeyError as exc:  # pragma: no cover - explicit message for clarity
        raise ValueError(f"Missing required field: {exc.args[0]}") from exc

    nodes_raw = data.get("nodes")
    edges_raw = data.get("edges")
    if not isinstance(nodes_raw, list):
        raise ValueError("nodes must be a list")
    if not isinstance(edges_raw, list):
        raise ValueError("edges must be a list")

    nodes = [_load_node(entry) for entry in nodes_raw]
    edges = [_load_edge(entry) for entry in edges_raw]

    meta = data.get("meta", {})
    if meta is None:
        meta = {}
    if not isinstance(meta, Mapping):
        raise ValueError("meta must be an object if provided")

    max_edge_cap = data.get("max_edge_cap")
    if max_edge_cap is not None:
        max_edge_cap = _ensure_int(max_edge_cap, "max_edge_cap")
        if max_edge_cap <= 0:
            raise ValueError("max_edge_cap must be a positive integer when provided")

    nap_ref = data.get("nap_ref")
    if nap_ref is not None and not isinstance(nap_ref, str):
        raise ValueError("nap_ref must be a string when provided")

    return TopologyProfileV1(
        gid=gid,
        profile=profile,
        N=N,
        nodes=nodes,
        edges=edges,
        SC=SC,
        causal_radius=causal_radius,
        max_edge_cap=max_edge_cap,
        nap_ref=nap_ref,
        meta=dict(meta),
    )


def load_topology_profile(path: Union[str, Path]) -> TopologyProfileV1:
    """Load ``TopologyProfile_v1`` from a JSON file.

    JSON is used to keep the loader dependency-free. If a YAML file is
    provided, a ``ValueError`` is raised with guidance to convert it.
    """

    file_path = Path(path)
    if file_path.suffix.lower() in {".yaml", ".yml"}:
        raise ValueError("Topology loader only supports JSON; please convert YAML to JSON")
    raw_data = json.loads(file_path.read_text())
    return topology_profile_from_dict(raw_data)
