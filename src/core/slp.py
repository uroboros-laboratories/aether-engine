"""Contracts and helpers for structural lattice perturbations (SLP)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Mapping, Sequence

from umx.topology_profile import EdgeProfileV1, NodeProfileV1, TopologyProfileV1


class SLPEventType(str, Enum):
    """Supported structural operation types for SLP events."""

    ADD_NODE = "ADD_NODE"
    REMOVE_NODE = "REMOVE_NODE"
    UPDATE_NODE = "UPDATE_NODE"
    ADD_EDGE = "ADD_EDGE"
    REMOVE_EDGE = "REMOVE_EDGE"
    UPDATE_EDGE = "UPDATE_EDGE"
    GRAPH_ENABLE = "GRAPH_ENABLE"
    GRAPH_DISABLE = "GRAPH_DISABLE"


@dataclass(frozen=True)
class SLPEventV1:
    """Serialisable representation of a topology mutation."""

    event_id: str
    gid: str
    tick_effective: int
    op_type: SLPEventType
    payload: Mapping[str, object] = field(default_factory=dict)
    meta: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id must be provided")
        if not self.gid:
            raise ValueError("gid must be provided")
        if self.tick_effective < 1:
            raise ValueError("tick_effective must be >= 1")
        if not isinstance(self.payload, Mapping):
            raise ValueError("payload must be a mapping")
        if not isinstance(self.meta, Mapping):
            raise ValueError("meta must be a mapping")


def apply_slp_events(
    topo: TopologyProfileV1, events: Sequence[SLPEventV1]
) -> TopologyProfileV1:
    """Apply a deterministic batch of SLP events to a topology profile.

    Events are applied in lexicographic order of ``event_id`` to keep behaviour
    stable regardless of input ordering. Only a minimal, CMP-style mutation set
    is supported; operations that would break contiguity or reference missing
    nodes/edges raise ``ValueError``.
    """

    sorted_events = sorted(events, key=lambda evt: evt.event_id)
    nodes: List[NodeProfileV1] = list(topo.nodes)
    edges: List[EdgeProfileV1] = list(topo.edges)
    meta: Dict[str, object] = dict(topo.meta)

    for event in sorted_events:
        if event.gid != topo.gid:
            raise ValueError("SLP event gid must match topology gid")
        payload = dict(event.payload)
        if event.op_type == SLPEventType.ADD_NODE:
            _apply_add_node(nodes, payload)
        elif event.op_type == SLPEventType.REMOVE_NODE:
            _apply_remove_node(nodes, edges, payload)
        elif event.op_type == SLPEventType.UPDATE_NODE:
            _apply_update_node(nodes, payload)
        elif event.op_type == SLPEventType.ADD_EDGE:
            _apply_add_edge(nodes, edges, topo.SC, payload)
        elif event.op_type == SLPEventType.REMOVE_EDGE:
            _apply_remove_edge(edges, payload)
        elif event.op_type == SLPEventType.UPDATE_EDGE:
            _apply_update_edge(nodes, edges, topo.SC, payload)
        elif event.op_type == SLPEventType.GRAPH_ENABLE:
            meta["enabled"] = True
        elif event.op_type == SLPEventType.GRAPH_DISABLE:
            meta["enabled"] = False
        else:  # pragma: no cover - defensive guard for future enums
            raise ValueError(f"Unsupported SLP op_type: {event.op_type}")

    return TopologyProfileV1(
        gid=topo.gid,
        profile=topo.profile,
        N=len(nodes),
        nodes=nodes,
        edges=edges,
        SC=topo.SC,
        meta=meta,
    )


def _apply_add_node(nodes: List[NodeProfileV1], payload: Mapping[str, object]) -> None:
    node_id = int(payload.get("node_id", 0))
    label = str(payload.get("label", ""))
    attrs = payload.get("attrs", {})
    if node_id != len(nodes) + 1:
        raise ValueError("ADD_NODE requires node_id to append contiguously")
    if not isinstance(attrs, Mapping):
        raise ValueError("node attrs must be a mapping")
    nodes.append(NodeProfileV1(node_id=node_id, label=label, attrs=dict(attrs)))


def _apply_remove_node(
    nodes: List[NodeProfileV1], edges: List[EdgeProfileV1], payload: Mapping[str, object]
) -> None:
    node_id = int(payload.get("node_id", 0))
    if node_id != len(nodes):
        raise ValueError("REMOVE_NODE only supports removing the last node to keep contiguity")
    nodes.pop()
    edges[:] = [edge for edge in edges if edge.i != node_id and edge.j != node_id]
    _reindex_edges(edges)


def _apply_update_node(nodes: List[NodeProfileV1], payload: Mapping[str, object]) -> None:
    node_id = int(payload.get("node_id", 0))
    label = payload.get("label")
    attrs = payload.get("attrs")
    if not 1 <= node_id <= len(nodes):
        raise ValueError("UPDATE_NODE must reference an existing node")
    current = nodes[node_id - 1]
    new_label = current.label if label is None else str(label)
    new_attrs = current.attrs if attrs is None else _coerce_attrs(attrs)
    nodes[node_id - 1] = NodeProfileV1(node_id=node_id, label=new_label, attrs=new_attrs)


def _apply_add_edge(
    nodes: Sequence[NodeProfileV1],
    edges: List[EdgeProfileV1],
    sc: int,
    payload: Mapping[str, object],
) -> None:
    e_id = int(payload.get("e_id", 0))
    i = int(payload.get("i", 0))
    j = int(payload.get("j", 0))
    k = int(payload.get("k", 0))
    cap = int(payload.get("cap", 0))
    c = int(payload.get("c", 0))
    if e_id != len(edges) + 1:
        raise ValueError("ADD_EDGE requires e_id to append contiguously")
    _ensure_node_ref(nodes, i)
    _ensure_node_ref(nodes, j)
    edges.append(EdgeProfileV1(e_id=e_id, i=i, j=j, k=k, cap=cap, SC=sc, c=c))


def _apply_remove_edge(edges: List[EdgeProfileV1], payload: Mapping[str, object]) -> None:
    e_id = int(payload.get("e_id", 0))
    if e_id != len(edges):
        raise ValueError("REMOVE_EDGE only supports removing the last edge to keep contiguity")
    edges.pop()


def _apply_update_edge(
    nodes: Sequence[NodeProfileV1],
    edges: List[EdgeProfileV1],
    sc: int,
    payload: Mapping[str, object],
) -> None:
    e_id = int(payload.get("e_id", 0))
    if not 1 <= e_id <= len(edges):
        raise ValueError("UPDATE_EDGE must reference an existing edge")
    i = payload.get("i")
    j = payload.get("j")
    updates: Dict[str, object] = {}
    for key in ("k", "cap", "c"):
        if key in payload:
            updates[key] = int(payload[key])
    if i is not None:
        _ensure_node_ref(nodes, int(i))
        updates["i"] = int(i)
    if j is not None:
        _ensure_node_ref(nodes, int(j))
        updates["j"] = int(j)
    target = edges[e_id - 1]
    edges[e_id - 1] = EdgeProfileV1(
        e_id=e_id,
        i=updates.get("i", target.i),
        j=updates.get("j", target.j),
        k=updates.get("k", target.k),
        cap=updates.get("cap", target.cap),
        SC=sc,
        c=updates.get("c", target.c),
    )


def _ensure_node_ref(nodes: Sequence[NodeProfileV1], node_id: int) -> None:
    if not 1 <= node_id <= len(nodes):
        raise ValueError("edge endpoints must reference existing nodes")


def _reindex_edges(edges: List[EdgeProfileV1]) -> None:
    for idx, edge in enumerate(edges, start=1):
        if edge.e_id != idx:
            edges[idx - 1] = EdgeProfileV1(
                e_id=idx,
                i=edge.i,
                j=edge.j,
                k=edge.k,
                cap=edge.cap,
                SC=edge.SC,
                c=edge.c,
                attrs=edge.attrs,
            )


def _coerce_attrs(attrs: object) -> Dict[str, object]:
    if not isinstance(attrs, Mapping):
        raise ValueError("attrs must be a mapping")
    return dict(attrs)
