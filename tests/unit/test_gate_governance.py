import pytest

from gate import NAPEnvelopeV1, apply_governance_to_envelopes
from governance import GovernanceConfigV1
from umx.profile_cmp0 import ProfileCMP0V1


@pytest.fixture
def profile():
    return ProfileCMP0V1()


def _env(layer: str, tick: int, seq: int = 1) -> NAPEnvelopeV1:
    return NAPEnvelopeV1(
        v=1,
        tick=tick,
        gid="G1",
        nid="N1",
        layer=layer,
        mode="P",
        payload_ref=seq * 10,
        seq=seq,
        prev_chain=0,
        sig="",
    )


def test_governance_noop_when_disabled(profile):
    envelopes = [_env("DATA", 1)]
    filtered, gov_envs, decisions = apply_governance_to_envelopes(
        envelopes, governance=None, window_id="W1", profile=profile
    )
    assert filtered == tuple(envelopes)
    assert not gov_envs
    assert not decisions


def test_enforce_drops_envelopes_over_cap(profile):
    governance = GovernanceConfigV1(
        governance_mode="ENFORCE",
        codex_action_mode="ENFORCE",
        meta={"max_envelopes_per_tick": 1},
    )
    env1 = _env("DATA", tick=1, seq=1)
    env2 = _env("DATA", tick=1, seq=2)
    filtered, gov_envs, decisions = apply_governance_to_envelopes(
        (env1, env2), governance=governance, window_id="W1", profile=profile
    )

    assert filtered == (env1,)
    assert len(gov_envs) == 2
    assert decisions[1].status == "REJECTED"
    assert "exceeds cap" in decisions[1].reasons[0]


def test_observe_retains_but_logs_rejections(profile):
    governance = GovernanceConfigV1(
        governance_mode="OBSERVE",
        codex_action_mode="OBSERVE",
        meta={"allowed_layers": ("DATA",)},
    )
    env = _env("EGRESS", tick=2, seq=5)
    filtered, gov_envs, decisions = apply_governance_to_envelopes(
        (env,), governance=governance, window_id="W2", profile=profile
    )

    assert filtered == (env,)
    assert gov_envs[0].layer == "GOV"
    assert decisions[0].status == "REJECTED_OBSERVED"
    assert decisions[0].reasons == ("layer EGRESS not allowed",)
