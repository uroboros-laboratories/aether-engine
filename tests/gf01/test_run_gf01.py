from __future__ import annotations

from core import run_gf01
from gate import NAPEnvelopeV1, SceneFrameV1
from loom.loom import LoomIBlockV1, LoomPBlockV1
from press import APXManifestV1
from umx.tick_ledger import EdgeFluxV1, UMXTickLedgerV1
from uledger import build_uledger_entries, hash_record


def test_run_gf01_emits_expected_artefacts():
    result = run_gf01()

    assert result.run_id == "GF01"
    assert len(result.ledgers) == 8
    assert len(result.p_blocks) == 8
    assert len(result.i_blocks) == 1
    assert isinstance(result.i_blocks[0], LoomIBlockV1)

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

    for tick, ledger in enumerate(result.ledgers, start=1):
        assert isinstance(ledger, UMXTickLedgerV1)
        assert ledger.tick == tick
        assert ledger.pre_u == [3, 1, 0, 0, 0, 0]
        assert ledger.post_u == [3, 1, 0, 0, 0, 0]
        assert ledger.edges == expected_fluxes
        assert ledger.sum_pre_u == ledger.sum_post_u == ledger.z_check == 4

    expected_chain = [
        20987847,
        356793608,
        65491504,
        113355772,
        927048329,
        759821701,
        916969047,
        588473909,
    ]
    assert [p.C_t for p in result.p_blocks] == expected_chain
    for tick, p_block in enumerate(result.p_blocks, start=1):
        assert isinstance(p_block, LoomPBlockV1)
        assert p_block.tick == tick
        assert p_block.seq == tick
        assert p_block.s_t == 9

    i_block = result.i_blocks[0]
    assert i_block.tick == 8
    assert i_block.W == result.profile.I_block_spacing_W
    assert i_block.C_t == expected_chain[-1]
    assert i_block.profile_version == result.profile.name
    assert i_block.post_u == result.ledgers[-1].post_u
    assert [edge.e_id for edge in i_block.topology_snapshot] == [edge.e_id for edge in result.topo.edges]

    manifest_full = result.manifests["GF01_APX_v0_full_window"]
    manifest_short = result.manifests["GF01_APX_v0_ticks_1_2"]
    assert isinstance(manifest_full, APXManifestV1)
    assert isinstance(manifest_short, APXManifestV1)
    assert manifest_full.manifest_check == 487809945
    assert manifest_short.manifest_check == 869911338
    assert [s.L_total for s in manifest_full.streams] == [7, 8]
    assert [s.L_total for s in manifest_short.streams] == [1, 2]

    assert len(result.scenes) == 8
    assert len(result.envelopes) == 8
    assert all(isinstance(scene, SceneFrameV1) for scene in result.scenes)
    assert all(isinstance(env, NAPEnvelopeV1) for env in result.envelopes)
    assert [env.tick for env in result.envelopes] == list(range(1, 9))
    assert [env.seq for env in result.envelopes] == list(range(1, 9))
    assert all(env.payload_ref == manifest_full.manifest_check for env in result.envelopes)
    expected_prev_chain = [result.profile.C0] + expected_chain[:-1]
    assert [env.prev_chain for env in result.envelopes] == expected_prev_chain

    assert len(result.u_ledger_entries) == 8
    expected_prev_hashes = [None]
    for entry in result.u_ledger_entries[:-1]:
        expected_prev_hashes.append(hash_record(entry))
    assert [entry.prev_entry_hash for entry in result.u_ledger_entries] == expected_prev_hashes

    rebuilt_entries = build_uledger_entries(
        gid=result.topo.gid,
        run_id=result.run_id,
        window_id="GF01_W1_ticks_1_8",
        ledgers=result.ledgers,
        p_blocks=result.p_blocks,
        envelopes=result.envelopes,
        manifest=manifest_full,
        policy_set_hash=result.u_ledger_entries[0].policy_set_hash,
    )
    assert rebuilt_entries == result.u_ledger_entries


def test_run_gf01_is_deterministic():
    first = run_gf01()
    second = run_gf01()

    assert first == second

