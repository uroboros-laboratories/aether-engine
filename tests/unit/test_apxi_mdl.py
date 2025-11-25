import pytest

from press import (
    APXiDescriptorV1,
    APXI_PRIMITIVE_CONST,
    APXI_PRIMITIVE_LINEAR,
    APXI_PRIMITIVE_RUN,
    compute_apxi_breakdown,
    compute_apxi_lengths,
)
from press.press import compute_id_mode_lengths, compute_r_mode_lengths


def test_const_descriptor_has_lower_total_than_id_and_r_when_perfect_fit():
    values = [(5,), (5,), (5,), (5,)]
    descriptor = APXiDescriptorV1(
        descriptor_id="d_const",
        descriptor_type=APXI_PRIMITIVE_CONST,
        window_id="ticks_1_4",
        stream_id="s1",
        params={"value": 5},
    )

    breakdown = compute_apxi_breakdown(values, descriptor, residual_scheme="R")
    baseline_r = compute_r_mode_lengths(values)
    baseline_id = compute_id_mode_lengths(values)

    assert breakdown.L_residual == 0
    assert breakdown.L_total < baseline_r["L_total"]
    assert breakdown.L_total < baseline_id["L_total"]


def test_run_descriptor_counts_residuals_when_pattern_does_not_perfectly_fit():
    values = [(1,), (2,), (1,), (2,), (2,), (2,)]
    descriptor = APXiDescriptorV1(
        descriptor_id="d_run",
        descriptor_type=APXI_PRIMITIVE_RUN,
        window_id="ticks_1_6",
        stream_id="s1",
        params={"pattern": [1, 2], "repeats": 3},
    )

    lengths = compute_apxi_lengths(values, descriptor, residual_scheme="ID")
    assert lengths["L_model"] > 0
    assert lengths["L_residual"] > 0
    baseline_id = compute_id_mode_lengths(values)
    assert lengths["L_total"] >= lengths["L_residual"]
    assert lengths["L_total"] <= baseline_id["L_total"]


def test_linear_descriptor_is_deterministic_across_calls():
    values = [(3,), (4,), (5,), (6,)]
    descriptor = APXiDescriptorV1(
        descriptor_id="d_linear",
        descriptor_type=APXI_PRIMITIVE_LINEAR,
        window_id="ticks_1_4",
        stream_id="s1",
        params={"intercept": 3, "slope": 1, "start_tick": 0},
    )

    first = compute_apxi_lengths(values, descriptor, residual_scheme="R")
    second = compute_apxi_lengths(values, descriptor, residual_scheme="R")
    assert first == second
    assert first["L_residual"] == 0
    assert first["L_model"] > 0
