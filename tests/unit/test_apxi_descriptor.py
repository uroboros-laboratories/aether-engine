import json

import pytest

from press import (
    APXI_PRIMITIVE_CONST,
    APXI_PRIMITIVE_LINEAR,
    APXI_PRIMITIVE_RUN,
    APXiDescriptorV1,
)


def test_const_segment_round_trip() -> None:
    descriptor = APXiDescriptorV1(
        descriptor_id="d1",
        descriptor_type=APXI_PRIMITIVE_CONST,
        window_id="ticks_1_8",
        stream_id="S1_post_u_deltas",
        params={"value": 7},
        labels=("gf01", "cmp0"),
    )

    raw = descriptor.to_dict()
    assert raw["params"] == {"value": 7}
    restored = APXiDescriptorV1.from_dict(raw)
    assert restored == descriptor
    assert json.loads(descriptor.to_json()) == raw


def test_run_segment_validation_and_serialisation() -> None:
    descriptor = APXiDescriptorV1(
        descriptor_id="run1",
        descriptor_type=APXI_PRIMITIVE_RUN,
        window_id="ticks_1_4",
        stream_id="S2_fluxes",
        params={"pattern": [1, -1], "repeats": 3},
    )

    assert descriptor.params == {"pattern": (1, -1), "repeats": 3}
    encoded = descriptor.to_json()
    decoded = APXiDescriptorV1.from_json(encoded)
    assert decoded == descriptor


def test_linear_trend_defaults_and_validation() -> None:
    descriptor = APXiDescriptorV1(
        descriptor_id="trend1",
        descriptor_type=APXI_PRIMITIVE_LINEAR,
        window_id="ticks_1_8",
        stream_id="S1_post_u_deltas",
        params={"intercept": 5, "slope": -1},
    )

    assert descriptor.params == {"intercept": 5, "slope": -1, "start_tick": 0}
    assert descriptor.to_dict()["params"]["start_tick"] == 0


@pytest.mark.parametrize(
    "descriptor_type,params,expected",
    [
        (APXI_PRIMITIVE_CONST, {}, ValueError),
        (APXI_PRIMITIVE_CONST, {"value": 1, "extra": 2}, ValueError),
        (APXI_PRIMITIVE_RUN, {"pattern": [], "repeats": 1}, ValueError),
        (APXI_PRIMITIVE_RUN, {"pattern": [1, 2], "repeats": 0}, ValueError),
        (APXI_PRIMITIVE_RUN, {"pattern": [1, "x"], "repeats": 1}, TypeError),
        (APXI_PRIMITIVE_LINEAR, {"intercept": 1}, ValueError),
        (APXI_PRIMITIVE_LINEAR, {"intercept": 1, "slope": 2, "unknown": 3}, ValueError),
    ],
)
def test_invalid_params_raise(descriptor_type, params, expected) -> None:
    with pytest.raises(expected):
        APXiDescriptorV1(
            descriptor_id="bad",
            descriptor_type=descriptor_type,
            window_id="w1",
            stream_id="s1",
            params=params,
        )


def test_invalid_descriptor_type() -> None:
    with pytest.raises(ValueError):
        APXiDescriptorV1(
            descriptor_id="badtype",
            descriptor_type="UNKNOWN",
            window_id="w1",
            stream_id="s1",
            params={"value": 1},
        )
