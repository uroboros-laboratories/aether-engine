from dataclasses import replace

import pytest

from gate import NAPEnvelopeV1
from loom.loom import FluxSummaryV1, LoomPBlockV1
from press.press import APXManifestV1
from uledger import (
    ULedgerEntryV1,
    build_and_validate_uledger,
    validate_uledger_chain,
)
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1


def _ledger(tick: int) -> UMXTickLedgerV1:
    return UMXTickLedgerV1(
        tick=tick,
        sum_pre_u=1,
        sum_post_u=1,
        z_check=1,
        pre_u=[1],
        edges=[EdgeFluxV1(e_id=1, i=0, j=0, du=0, raw=0, cap=0, f_e=0)],
        post_u=[1],
        nap_ref=f"nap_{tick}",
    )


def _p_block(tick: int, chain: int) -> LoomPBlockV1:
    return LoomPBlockV1(
        gid="G",
        tick=tick,
        seq=tick,
        s_t=1,
        C_t=chain,
        topology_version="v1",
        edge_flux_summary=[FluxSummaryV1(e_id=1, f_e=0)],
    )


def _envelope(tick: int, chain: int) -> NAPEnvelopeV1:
    return NAPEnvelopeV1(
        v=1,
        tick=tick,
        gid="G",
        nid="N",
        layer="DATA",
        mode="G",
        payload_ref=tick,
        seq=tick,
        prev_chain=chain,
        sig="",
    )


def _manifest() -> APXManifestV1:
    return APXManifestV1(apx_name="apx", profile="p", manifest_check=123, gid="G", window_id="W")


def test_build_and_validate_uledger_creates_chain_and_checkpoint():
    manifest = _manifest()
    ledgers = [_ledger(1), _ledger(2)]
    p_blocks = [_p_block(1, 10), _p_block(2, 11)]
    envelopes = [_envelope(1, 9), _envelope(2, 10)]

    entries, checkpoint = build_and_validate_uledger(
        gid="G",
        run_id="R",
        window_id="W",
        ledgers=ledgers,
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=manifest,
        policy_set_hash="policy_v1",
    )

    assert len(entries) == 2
    assert isinstance(entries[0], ULedgerEntryV1)
    assert checkpoint.entry_count == 2
    assert checkpoint.start_tick == 1
    assert checkpoint.end_tick == 2
    assert checkpoint.manifest_hash == entries[0].apx_manifest_hash
    assert checkpoint.policy_set_hash == "policy_v1"


def test_validate_uledger_chain_rejects_prev_hash_and_manifest_mismatches():
    manifest = _manifest()
    ledgers = [_ledger(1), _ledger(2)]
    p_blocks = [_p_block(1, 10), _p_block(2, 11)]
    envelopes = [_envelope(1, 9), _envelope(2, 10)]

    entries, _ = build_and_validate_uledger(
        gid="G",
        run_id="R",
        window_id="W",
        ledgers=ledgers,
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=manifest,
    )

    broken_prev = [replace(entries[0], prev_entry_hash="bogus"), *entries[1:]]
    with pytest.raises(ValueError):
        validate_uledger_chain(broken_prev, manifest=manifest, start_prev_hash=None)

    bad_manifest = _manifest()
    bad_manifest = replace(bad_manifest, manifest_check=999)
    with pytest.raises(ValueError):
        validate_uledger_chain(entries, manifest=bad_manifest)


def test_validate_uledger_chain_requires_contiguous_ticks():
    manifest = _manifest()
    ledger1, ledger3 = _ledger(1), _ledger(3)
    p_blocks = [_p_block(1, 10), _p_block(3, 12)]
    envelopes = [_envelope(1, 9), _envelope(3, 11)]

    entries, _ = build_and_validate_uledger(
        gid="G",
        run_id="R",
        window_id="W",
        ledgers=[ledger1, ledger3],
        p_blocks=p_blocks,
        envelopes=envelopes,
        manifest=manifest,
        require_contiguous_ticks=False,
    )

    with pytest.raises(ValueError):
        validate_uledger_chain(entries, manifest=manifest, require_contiguous_ticks=True)

