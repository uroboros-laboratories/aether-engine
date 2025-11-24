"""Topology and profile records for CMP-0.

Implements `TopologyProfile_v1`, `NodeProfile_v1`, and `EdgeProfile_v1`
as described in the contracts. Includes a helper for the GF-01 topology
card so tests can consume a single canonical definition.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


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
    meta: Dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate_nodes()
        self._validate_edges()
        if self.SC <= 0:
            raise ValueError("SC must be a positive integer")

    def _validate_nodes(self) -> None:
        node_ids = [node.node_id for node in self.nodes]
        expected = list(range(1, self.N + 1))
        if node_ids != expected:
            raise ValueError("Nodes must be contiguous from 1..N in ascending order")

    def _validate_edges(self) -> None:
        edge_ids = [edge.e_id for edge in self.edges]
        expected_ids = list(range(1, len(self.edges) + 1))
        if edge_ids != expected_ids:
            raise ValueError("Edges must be contiguous from 1..E in ascending order")
        for edge in self.edges:
            if not (1 <= edge.i <= self.N) or not (1 <= edge.j <= self.N):
                raise ValueError("Edge endpoints must reference valid node IDs")
            if edge.SC <= 0:
                raise ValueError("Edge SC must be positive")


def gf01_topology_profile() -> TopologyProfileV1:
    """Return the canonical GF-01 topology for CMP-0.

    The edge ordering and k-values match the GF-01 topology card
    in the worked examples PDF. Caps are effectively unbounded in the
    paper example, represented here with a large sentinel integer.
    """

    nodes = [NodeProfileV1(node_id=i, label=f"n{i}") for i in range(1, 7)]
    global_sc = 32
    cap_unbounded = 2_147_483_647  # Sentinel for "no binding cap" in CMP-0/GF-01.
    edges = [
        EdgeProfileV1(e_id=1, i=1, j=2, k=1, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=2, i=1, j=4, k=2, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=3, i=1, j=6, k=1, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=4, i=2, j=3, k=1, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=5, i=2, j=5, k=2, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=6, i=3, j=4, k=1, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=7, i=4, j=5, k=1, cap=cap_unbounded, SC=global_sc, c=0),
        EdgeProfileV1(e_id=8, i=5, j=6, k=1, cap=cap_unbounded, SC=global_sc, c=0),
    ]

    return TopologyProfileV1(
        gid="GF01",
        profile="CMP-0",
        N=6,
        nodes=nodes,
        edges=edges,
        SC=global_sc,
        meta={
            "description": "GF-01 CMP-0 baseline topology",
            "source": "docs/fixtures/gf01/GF01_Ticks_1_8_Worked_Examples.pdf",
        },
    )
