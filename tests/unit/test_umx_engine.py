"""Unit tests for the CMP-0 UMX engine."""
from __future__ import annotations

from src.umx import EdgeFluxV1, UMXTickLedgerV1, gf01_profile_cmp0, gf01_topology_profile, step


def test_step_runs_gf01_ticks_deterministically():
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    state = [3, 1, 0, 0, 0, 0]

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

    ledgers = []
    for tick in range(1, 9):
        ledger = step(tick, state, topo, profile)
        ledgers.append(ledger)
        state = ledger.post_u

    for tick, ledger in enumerate(ledgers, start=1):
        assert ledger.tick == tick
        assert ledger.pre_u == [3, 1, 0, 0, 0, 0]
        assert ledger.post_u == [3, 1, 0, 0, 0, 0]
        assert ledger.edges == expected_fluxes
        assert ledger.sum_pre_u == 4
        assert ledger.sum_post_u == 4
        assert ledger.z_check == 4


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
