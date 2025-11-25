# RunConfig_v1 — File-driven run configuration

## Purpose

`RunConfig_v1` defines a canonical, file-based way to describe CMP-style
runs. It links together the topology graph, numeric profile (e.g. CMP-0,
CMP-1 placeholders), Press/APX window definitions, and runtime toggles such
as Codex or PFNA.

- **TopologyConfig**: references a `TopologyProfile_v1` document (JSON).
- **ProfileConfig**: references a numeric profile document compatible with
  `Profile_CMP0_v1` (JSON).
- **RunConfig**: binds topology, profile, windows, and runtime knobs for a
  single run.

All configs are JSON to preserve determinism and avoid extra dependencies.

---

## Record Shapes

### TopologyConfig (alias of `TopologyProfile_v1`)

Reuse the existing `TopologyProfile_v1` contract. Config files are identical to
that contract and can be loaded with the existing topology loader.

### ProfileConfig (CMP-style)

Aligns with `Profile_CMP0_v1` field names for Phase 3. Required fields:

- `name` (must be present and start with `"CMP-"`; CMP-0, CMP-1, etc.),
- `modulus_M`, `C0`, `SC`, `I_block_spacing_W` (positive integers),
- `flux_rule`, `chain_rule`, `s_t_rule` (objects, see contract),
- Optional `nap_defaults`, `press_defaults`.

### RunConfig_v1

Top-level run description:

- **v**: integer version, must be `1`.
- **gid**: graph ID string.
- **run_id**: run identifier string.
- **topology_path**: path to a `TopologyProfile_v1` JSON document.
- **profile_path**: path to a CMP-style profile JSON document.
- **ticks**: positive integer tick count.
- **initial_state**: non-empty integer vector matching the topology `N`.
- **windows**: array of `RunWindow` records (see below).
- **primary_window_id**: ID of the window considered primary for manifests.
- **nap**: optional object for NAP defaults (layer/mode/v overrides).
- **enable_codex**: boolean toggle for Codex ingestion.
- **enable_pfna**: boolean toggle indicating PFNA inputs should be loaded.
- **pfna_path**: optional path to a PFNA V0 document.
- **diagnostics**: optional object for debug/trace flags.

#### RunWindow

- **window_id**: string identifier.
- **apx_name**: APX window/manifest name.
- **start_tick** / **end_tick**: inclusive tick range (start >= 1, end >= start).
- **streams**: array of `RunWindowStream` entries. May be empty to inherit
  defaults.
- **aeon_window_id**: optional AEON grammar ID when AEON/APXi is linked.

#### RunWindowStream

- **name**: stream name (e.g. `"S1_post_u_deltas"`).
- **source**: one of `post_u_deltas`, `fluxes`, `pre_u`, `post_u`, `prev_chain`.
- **scheme_hint**: optional APX scheme hint (`R`, `GR`, or `ID`).
- **description**: optional free-form description.

---

## Canonical Serialization

- **Format:** JSON only for all three config types.
- **Encoding:** UTF-8, no BOM.
- **Ordering:** Field order is not significant, but examples use a consistent
  ordering for readability.

---

## Examples

Example config files live under `docs/fixtures/configs/`:

- `gf01_run_config.json` — GF-01 baseline using CMP-0 defaults.
- `line_4_run_config.json` — 4-node line toy scenario.
- `line_4_run_config_cmp1.json` — line scenario selecting the CMP-1 placeholder profile.
- `ring_5_run_config.json` — 5-node ring toy scenario.

Profile documents live under `docs/fixtures/profiles/` (e.g. `profile_cmp0.json`, `profile_cmp1.json`).
Each run config references a topology fixture under `docs/fixtures/topologies/`.
