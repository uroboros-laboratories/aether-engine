"""Unit tests for the CMP-0 UMX engine."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.umx import (
    EdgeFluxV1,
    ProfileCMP0V1,
    UMXDiagnosticsConfig,
    UMXRunContext,
    UMXTickLedgerV1,
    gf01_profile_cmp0,
    gf01_topology_profile,
    load_topology_profile,
    step,
    topology_profile_from_dict,
)


def _fixture_path(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "docs" / "fixtures" / "topologies" / name


def test_run_context_runs_gf01_ticks_deterministically():
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    ctx = UMXRunContext(topo=topo, profile=profile)
    ctx.init_state([3, 1, 0, 0, 0, 0])

    expected_fluxes = [
        EdgeFluxV1(e_id=1, i=1, j=2, du=2, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=2, i=1, j=4, du=3, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=3, i=1, j=6, du=3, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=4, i=2, j=3, du=1, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=5, i=2, j=5, du=1, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=6, i=3, j=4, du=0, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=7, i=4, j=5, du=0, raw=0, cap=2_147_483_647, f_e=0),
        EdgeFluxV1(e_id=8, i=5, j=6, du=0, raw=0, cap=2_147_483_647, f_e=0),
    ]

    ledgers = ctx.run_until(8)

    for tick, ledger in enumerate(ledgers, start=1):
        assert ledger.tick == tick
        assert ledger.pre_u == [3, 1, 0, 0, 0, 0]
        assert ledger.post_u == [3, 1, 0, 0, 0, 0]
        assert ledger.edges == expected_fluxes
        assert ledger.sum_pre_u == 4
        assert ledger.sum_post_u == 4
        assert ledger.z_check == 4
    assert ctx.tick == 8
    assert ctx.current_state() == [3, 1, 0, 0, 0, 0]


def test_run_context_rejects_state_length_mismatch():
    ctx = UMXRunContext(topo=gf01_topology_profile(), profile=gf01_profile_cmp0())
    try:
        ctx.init_state([1, 2, 3])
    except ValueError:
        return
    raise AssertionError("Expected ValueError for incorrect state length")


def test_run_until_cannot_rewind_ticks():
    ctx = UMXRunContext(topo=gf01_topology_profile(), profile=gf01_profile_cmp0())
    ctx.init_state([3, 1, 0, 0, 0, 0])
    ctx.run_until(2)
    try:
        ctx.run_until(1)
    except ValueError:
        return
    raise AssertionError("Expected ValueError when requesting t_max behind current tick")


def test_run_context_is_deterministic_on_line_topology():
    topo = load_topology_profile(_fixture_path("line_4_topology_profile.json"))
    profile = gf01_profile_cmp0()
    initial_state = [32, 0, 0, 0]

    ctx1 = UMXRunContext(topo=topo, profile=profile, run_id="run_1")
    ctx1.init_state(initial_state)
    ctx2 = UMXRunContext(topo=topo, profile=profile, run_id="run_2")
    ctx2.init_state(initial_state)

    ledgers_1 = ctx1.run_until(4)
    ledgers_2 = ctx2.run_until(4)

    assert ledgers_1 == ledgers_2
    assert [ledger.post_u for ledger in ledgers_1] == [
        [30, 2, 0, 0],
        [29, 3, 0, 0],
        [28, 4, 0, 0],
        [27, 5, 0, 0],
    ]


def test_step_respects_topology_scale_on_ring_topology():
    topo = load_topology_profile(_fixture_path("ring_5_topology_profile.json"))
    profile = gf01_profile_cmp0()
    ctx = UMXRunContext(topo=topo, profile=profile, run_id="ring")
    ctx.init_state([10, 0, 0, 0, 0])

    ledgers = ctx.run_until(3)

    assert [edge.e_id for edge in ledgers[0].edges] == [1, 2, 3, 4, 5]
    assert [edge.f_e for edge in ledgers[0].edges] == [1, 0, 0, 0, 1]
    assert [edge.f_e for edge in ledgers[1].edges] == [0, 0, 0, 0, 0]
    assert [ledger.post_u for ledger in ledgers] == [
        [8, 1, 0, 0, 1],
        [8, 1, 0, 0, 1],
        [8, 1, 0, 0, 1],
    ]
    assert all(sum(ledger.pre_u) == 10 for ledger in ledgers)


def test_step_respects_topology_scale_on_star_topology():
    topo = load_topology_profile(_fixture_path("star_5_topology_profile.json"))
    profile = gf01_profile_cmp0()
    ctx = UMXRunContext(topo=topo, profile=profile, run_id="star")
    ctx.init_state([50, 0, 0, 0, 0])

    ledgers = ctx.run_until(3)

    assert [edge.e_id for edge in ledgers[0].edges] == [1, 2, 3, 4]
    assert [edge.f_e for edge in ledgers[0].edges] == [6, 6, 6, 6]
    assert [edge.f_e for edge in ledgers[1].edges] == [2, 2, 2, 2]
    assert [edge.f_e for edge in ledgers[2].edges] == [1, 1, 1, 1]
    assert [ledger.post_u for ledger in ledgers] == [
        [26, 6, 6, 6, 6],
        [18, 8, 8, 8, 8],
        [14, 9, 9, 9, 9],
    ]
    assert all(sum(ledger.pre_u) == 50 for ledger in ledgers)


def test_loader_rejects_edge_scale_mismatch():
    data = {
        "gid": "SCALE_MISMATCH",
        "profile": "CMP-0",
        "N": 2,
        "nodes": [
            {"node_id": 1, "label": "n1", "attrs": {}},
            {"node_id": 2, "label": "n2", "attrs": {}},
        ],
        "edges": [
            {"e_id": 1, "i": 1, "j": 2, "k": 1, "cap": 10, "SC": 5, "c": 0, "attrs": {}},
        ],
        "SC": 4,
        "meta": {},
    }

    try:
        topology_profile_from_dict(data)
    except ValueError:
        return
    raise AssertionError("Expected ValueError when edge SC does not match topology SC")


def test_conservation_guard_raises_when_sums_mismatch():
    try:
        UMXTickLedgerV1(
            tick=1,
            sum_pre_u=1,
            sum_post_u=2,
            z_check=1,
            pre_u=[1],
            edges=[],
            post_u=[2],
        )
    except ValueError:
        return
    raise AssertionError("Expected ValueError for mismatched sums")


def test_causal_radius_clamps_flux_and_sets_policy_note():
    topo = topology_profile_from_dict(
        {
            "gid": "CAUSAL_CLAMP",
            "profile": "CMP-0",
            "N": 2,
            "nodes": [
                {"node_id": 1, "label": "a"},
                {"node_id": 2, "label": "b"},
            ],
            "edges": [
                {
                    "e_id": 1,
                    "i": 1,
                    "j": 2,
                    "k": 10,
                    "cap": 50,
                    "SC": 10,
                    "c": 0,
                    "causal_radius": 2,
                }
            ],
            "SC": 10,
        }
    )
    profile = gf01_profile_cmp0()

    ledger = step(1, [20, 0], topo, profile)

    assert ledger.edges[0].raw == 2
    assert ledger.edges[0].f_e == 2
    assert ledger.causal_radius_applied is True
    assert "causal_radius_clamped" in ledger.policy_notes


def test_epsilon_cap_clamps_raw_flux():
    topo = topology_profile_from_dict(
        {
            "gid": "EPSILON_CAP",
            "profile": "CMP-0",
            "N": 2,
            "nodes": [
                {"node_id": 1, "label": "a"},
                {"node_id": 2, "label": "b"},
            ],
            "edges": [
                {"e_id": 1, "i": 1, "j": 2, "k": 10, "cap": 50, "SC": 10, "c": 0}
            ],
            "SC": 10,
        }
    )
    profile = ProfileCMP0V1(epsilon_cap=1)

    ledger = step(1, [20, 0], topo, profile)

    assert ledger.edges[0].raw == 1
    assert ledger.edges[0].f_e == 1
    assert ledger.epsilon_applied is True
    assert "epsilon_cap_applied" in ledger.policy_notes


def test_diagnostics_record_policy_violations_when_enforced():
    topo = topology_profile_from_dict(
        {
            "gid": "POLICY_FLAGS",
            "profile": "CMP-0",
            "N": 2,
            "nodes": [
                {"node_id": 1, "label": "a"},
                {"node_id": 2, "label": "b"},
            ],
            "edges": [
                {
                    "e_id": 1,
                    "i": 1,
                    "j": 2,
                    "k": 10,
                    "cap": 50,
                    "SC": 10,
                    "c": 0,
                    "causal_radius": 3,
                }
            ],
            "SC": 10,
        }
    )
    profile = ProfileCMP0V1(epsilon_cap=2)
    ctx = UMXRunContext(
        topo=topo,
        profile=profile,
        diag_config=UMXDiagnosticsConfig(
            enabled=True,
            enforce_causal_radius=True,
            enforce_epsilon_cap=True,
        ),
    )
    ctx.init_state([50, 0])

    ledger = ctx.step()

    assert ledger.causal_radius_applied is True
    assert ledger.epsilon_applied is True
    diag = ctx.diagnostics[-1]
    assert "causal radius exceeded" in diag.policy_violations
    assert "epsilon cap triggered" in diag.policy_violations
    assert ctx.killed is False


def test_kill_switch_halts_on_violation():
    topo = topology_profile_from_dict(
        {
            "gid": "NEGATIVE_STATE",
            "profile": "CMP-0",
            "N": 1,
            "nodes": [{"node_id": 1, "label": "solo"}],
            "edges": [],
            "SC": 1,
        }
    )
    profile = gf01_profile_cmp0()
    ctx = UMXRunContext(
        topo=topo,
        profile=profile,
        diag_config=UMXDiagnosticsConfig(
            enabled=True,
            allow_negative=False,
            kill_on_violation=True,
        ),
    )
    ctx.init_state([-5])

    with pytest.raises(ValueError):
        ctx.step()

    assert ctx.killed is True
    assert ctx.kill_reason and "negative values detected" in ctx.kill_reason
