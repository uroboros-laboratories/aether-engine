"""Tests for optional UMX diagnostics and invariants."""
from __future__ import annotations

import pytest

from src.umx import (
    UMXDiagnosticsConfig,
    UMXRunContext,
    gf01_profile_cmp0,
    gf01_topology_profile,
)


def test_diagnostics_do_not_change_outputs():
    topo = gf01_topology_profile()
    profile = gf01_profile_cmp0()
    u0 = [3, 1, 0, 0, 0, 0]

    ctx_plain = UMXRunContext(topo=topo, profile=profile)
    ctx_plain.init_state(u0)
    ledgers_plain = ctx_plain.run_until(3)

    diag_config = UMXDiagnosticsConfig(enabled=True)
    ctx_diag = UMXRunContext(topo=topo, profile=profile, diag_config=diag_config)
    ctx_diag.init_state(u0)
    ledgers_diag = ctx_diag.run_until(3)

    assert ledgers_plain == ledgers_diag
    assert len(ctx_diag.diagnostics) == 3
    assert all(record.conservation_ok for record in ctx_diag.diagnostics)
    assert all(record.violations == [] for record in ctx_diag.diagnostics)
    assert all(record.min_pre == 0 for record in ctx_diag.diagnostics)
    assert all(record.max_pre == 3 for record in ctx_diag.diagnostics)


def test_diagnostics_flag_violations_and_optionally_raise():
    config = UMXDiagnosticsConfig(
        enabled=True,
        check_conservation=True,
        allow_negative=False,
        overflow_limit=5,
        raise_on_violation=False,
    )

    record = config.evaluate_tick(
        tick=1,
        pre_u=[10, -1],
        post_u=[9, 1],
        sum_pre_u=9,
        sum_post_u=10,
        z_check=9,
    )

    assert not record.conservation_ok
    assert record.has_negative_pre is True
    assert record.overflow_pre is True
    assert len(record.violations) == 3

    raising_config = UMXDiagnosticsConfig(
        enabled=True,
        check_conservation=True,
        allow_negative=False,
        overflow_limit=5,
        raise_on_violation=True,
    )

    with pytest.raises(ValueError):
        raising_config.evaluate_tick(
            tick=2,
            pre_u=[-2, 7],
            post_u=[-1, 8],
            sum_pre_u=5,
            sum_post_u=7,
            z_check=5,
        )
