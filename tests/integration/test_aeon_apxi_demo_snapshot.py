from __future__ import annotations

import json
from pathlib import Path

from core import TickLoopWindowSpec, dumps_session_run, serialize_session_run
from gate import PressStreamSpecV1, SessionConfigV1, run_session
from press.aeon import AEONDerivedWindowV1, AEONWindowDefV1, AEONWindowGrammarV1, AEONWindowRegistry
from press.apxi import APXiDescriptorV1
from press.press import PressWindowContextV1
from umx.profile_cmp0 import gf01_profile_cmp0
from umx.topology_profile import load_topology_profile

SNAPSHOT_PATH = (
    Path(__file__).parent.parent
    / "fixtures"
    / "snapshots"
    / "aeon_apxi_demo"
    / "aeon_apxi_demo_snapshot.json"
)


def _demo_aeon_grammar() -> AEONWindowGrammarV1:
    base_first = AEONWindowDefV1(
        window_id="AEON_LINE4_W1_ticks_1_3",
        tick_start=1,
        tick_end=3,
        labels=("demo", "first-half"),
        press_window_id=None,
    )
    base_second = AEONWindowDefV1(
        window_id="AEON_LINE4_W2_ticks_4_6",
        tick_start=4,
        tick_end=6,
        labels=("demo", "second-half"),
        press_window_id=None,
    )
    derived_all = AEONDerivedWindowV1(
        window_id="AEON_LINE4_W_all",
        source_ids=(base_first.window_id, base_second.window_id),
        aggregation="concat",
        labels=("demo", "aggregate"),
        press_window_id="LINE4_APX_W1_T1_6",
    )
    return AEONWindowGrammarV1(
        base_windows={base_first.window_id: base_first, base_second.window_id: base_second},
        derived_windows={derived_all.window_id: derived_all},
    )


def _demo_streams() -> tuple[PressStreamSpecV1, ...]:
    return (
        PressStreamSpecV1(
            name="S1_post_u_deltas", source="post_u_deltas", description="post_u delta per node"
        ),
        PressStreamSpecV1(name="S2_fluxes", source="fluxes", description="edge flux per edge"),
        PressStreamSpecV1(
            name="S3_prev_chain",
            source="prev_chain",
            description="prev chain checksum per tick",
        ),
    )


def _demo_descriptors() -> dict[str, tuple[APXiDescriptorV1, ...]]:
    aeon_window_id = "AEON_LINE4_W_all"
    return {
        "S1_post_u_deltas": (
            APXiDescriptorV1(
                descriptor_id="apxi_delta_linear",
                descriptor_type="LINEAR_TREND",
                window_id=aeon_window_id,
                stream_id="S1_post_u_deltas",
                params={"intercept": 0, "slope": 1, "start_tick": 1},
            ),
        ),
        "S2_fluxes": (
            APXiDescriptorV1(
                descriptor_id="apxi_flux_const",
                descriptor_type="CONST_SEGMENT",
                window_id=aeon_window_id,
                stream_id="S2_fluxes",
                params={"value": 0},
            ),
        ),
        "S3_prev_chain": (
            APXiDescriptorV1(
                descriptor_id="apxi_chain_const",
                descriptor_type="CONST_SEGMENT",
                window_id=aeon_window_id,
                stream_id="S3_prev_chain",
                params={"value": 0},
            ),
        ),
    }


def _demo_config(*, apxi_enabled: bool) -> SessionConfigV1:
    topo = load_topology_profile("docs/fixtures/topologies/line_4_topology_profile.json")
    profile = gf01_profile_cmp0()

    window_spec = TickLoopWindowSpec(
        window_id="LINE4_W1_T1_6",
        apx_name="LINE4_APX_W1_T1_6",
        start_tick=1,
        end_tick=6,
        streams=_demo_streams(),
        aeon_window_id="AEON_LINE4_W_all",
        apxi_descriptors=_demo_descriptors() if apxi_enabled else {},
        apxi_enabled=apxi_enabled,
        apxi_residual_scheme="R",
    )

    return SessionConfigV1(
        topo=topo,
        profile=profile,
        initial_state=[1, 0, 0, 0],
        total_ticks=6,
        window_specs=(window_spec,),
        primary_window_id=window_spec.window_id,
        run_id="AEON_APXI_DEMO_RUN",
        nid="aeon-apxi-demo-node",
        press_default_streams=_demo_streams(),
    )


def _snapshot_payload(result) -> dict:
    grammar = _demo_aeon_grammar()
    registry = AEONWindowRegistry.from_grammar(grammar)
    return {
        "aeon_grammar": grammar.to_mapping(),
        "windows_covering_tick_2": registry.windows_covering_tick(2),
        "windows_covering_tick_5": registry.windows_covering_tick(5),
        "session": serialize_session_run(result),
    }


def test_aeon_apxi_demo_is_deterministic():
    cfg = _demo_config(apxi_enabled=True)

    first = dumps_session_run(run_session(cfg))
    second = dumps_session_run(run_session(cfg))

    assert first == second


def test_aeon_apxi_demo_matches_snapshot():
    cfg = _demo_config(apxi_enabled=True)
    result = run_session(cfg)
    payload = _snapshot_payload(result)

    with SNAPSHOT_PATH.open("r", encoding="utf-8") as handle:
        snapshot = json.load(handle)

    assert payload == snapshot


def test_aeon_apxi_toggle_preserves_manifest_when_disabled():
    enabled_cfg = _demo_config(apxi_enabled=True)
    disabled_cfg = _demo_config(apxi_enabled=False)

    enabled_result = run_session(enabled_cfg)
    disabled_result = run_session(disabled_cfg)

    enabled_serialized = serialize_session_run(enabled_result)
    disabled_serialized = serialize_session_run(disabled_result)

    enabled_manifest = enabled_serialized["tick_result"]["manifests"]["LINE4_APX_W1_T1_6"]
    disabled_manifest = disabled_serialized["tick_result"]["manifests"]["LINE4_APX_W1_T1_6"]

    # Disabling APXi removes view refs and apxi_views without perturbing manifest_check
    assert "apxi_view_ref" in enabled_manifest
    assert "apxi_view_ref" not in disabled_manifest
    assert enabled_manifest["manifest_check"] == disabled_manifest["manifest_check"]
    assert "apxi_views" in enabled_serialized["tick_result"]
    assert "apxi_views" not in disabled_serialized["tick_result"]

    # Non-APXi payload is stable when APXi is toggled off
    manifest_without_apxi = dict(enabled_manifest)
    manifest_without_apxi.pop("apxi_view_ref", None)
    assert manifest_without_apxi == disabled_manifest

    # Press window buffer reset behaviour unchanged
    assert isinstance(
        PressWindowContextV1(
            gid="G",
            run_id="R",
            window_id="noop",
            start_tick=1,
            end_tick=1,
            profile=gf01_profile_cmp0(),
            apxi_enabled=False,
        ).clear_on_close,
        bool,
    )
