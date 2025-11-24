# Aether Artifact Index (Chat Session) — v1

This file lists the key files present in this chat’s `/mnt/data` space and suggests where they should live in the eventual **`aether-engine`** repo.

It’s mainly a **checklist** so you can drag/drop everything into place without hunting through the conversation.

---

## 1. Specs & Planning Docs

### 1.1 Master Index & Roadmap

| Local filename                                                     | Recommended repo path                                                             | Notes |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|-------|
| `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`             | `docs/specs/SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`                 | Top-level spec index & roadmap (SPEC-000). |

### 1.2 Full System Build Plan

| Local filename                                                     | Recommended repo path                                                             | Notes |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|-------|
| `spec_001_aether_full_system_build_plan_medium_agnostic.md`       | `docs/specs/spec_001_aether_full_system_build_plan_medium_agnostic.md`           | SPEC-001 full system build plan (medium-agnostic). |

### 1.3 Pillar Master Specs

| Local filename                                                     | Recommended repo path                                                             | Notes |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|-------|
| `UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`    | `docs/specs/UNIVERSAL_MATRIX_PILLAR_UMX_Master_Implementation_Spec_v1.md`        | UMX master implementation spec. |
| `astral_press_master_implementation_spec_combined_v1.md`          | `docs/specs/astral_press_master_implementation_spec_combined_v1.md`              | Astral Press/APX master spec. |
| `trinity gate full spec.txt`                                      | `docs/specs/trinity_gate_full_spec.txt`                                           | Trinity Gate/TBP master spec (text). |
| `Aevum Loom Pillar — Master spec.txt`                             | `docs/specs/Aevum_Loom_Pillar_Master_spec.txt`                                    | Aevum Loom pillar master spec (rename on import). |
| `Codex Eterna — Master spec.txt`                                  | `docs/specs/Codex_Eterna_Master_spec.txt`                                         | Codex Eterna master spec (rename on import). |

*(Renames are optional but recommended for filesystem friendliness.)*

### 1.4 Phase / SPEC Issue Packs

| Local filename                                | Recommended repo path                                      | Phase / scope |
|-----------------------------------------------|------------------------------------------------------------|---------------|
| `SPEC_003_Phase_3_Issue_Pack_v1.md`          | `docs/specs/SPEC_003_Phase_3_Issue_Pack_v1.md`            | Phase 3 — Gate/TBP & PFNA V0 / IO. |
| `SPEC_004_Phase_3_Issue_Pack_v1.md`          | `docs/specs/SPEC_004_Phase_3_Issue_Pack_v1.md`            | Phase 3 — Press AEON/APXi. |
| `SPEC_006_Phase_4_Issue_Pack_v1.md`          | `docs/specs/SPEC_006_Phase_4_Issue_Pack_v1.md`            | Phase 4 — Multi-graph & SLP V1. |
| `SPEC_007_Phase_5_Issue_Pack_v1.md`          | `docs/specs/SPEC_007_Phase_5_Issue_Pack_v1.md`            | Phase 5 — Governance & Codex actioning V1. |

*(SPEC-002 and SPEC-005 issue packs exist in the chat text but were not written to `/mnt/data` in this session. We can regenerate them as files later if you want.)*

### 1.5 Repo Bootstrap Guide

| Local filename                                | Recommended repo path                                      | Notes |
|-----------------------------------------------|------------------------------------------------------------|-------|
| `Aether_Repo_Bootstrap_Guide_v1.md`          | `docs/Aether_Repo_Bootstrap_Guide_v1.md`                   | Practical guide for setting up repo structure, milestones, labels, and GPT usage. |

---

## 2. Paper Artefacts & Fixtures

These are the PDFs and raw packs that mirror your paper system.

### 2.1 GF-01 Worked Examples & APX Sheets

| Local filename                                  | Recommended repo path                                  | Notes |
|-------------------------------------------------|--------------------------------------------------------|-------|
| `GF01_Ticks_1_8_Worked_Examples.pdf`            | `docs/fixtures/gf01/GF01_Ticks_1_8_Worked_Examples.pdf` | GF-01 ticks 1–8 worked examples. |
| `GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf`  | `docs/fixtures/gf01/GF01_Ticks_1_8_Envelopes_With_PayloadRef.pdf` | GF-01 NAP envelopes with payload refs. |
| `GF01_Ticks_1_8_APX_Press_Prefilled.pdf`        | `docs/fixtures/gf01/GF01_Ticks_1_8_APX_Press_Prefilled.pdf` | GF-01 APX prefilled sheet for ticks 1–8. |
| `GF01_Ticks_1_2_Worked_Examples.pdf`            | `docs/fixtures/gf01/GF01_Ticks_1_2_Worked_Examples.pdf` | GF-01 ticks 1–2 worked examples. |
| `GF01_Ticks_1_2_APX_Press_Prefilled.pdf`        | `docs/fixtures/gf01/GF01_Ticks_1_2_APX_Press_Prefilled.pdf` | GF-01 APX prefilled sheet for ticks 1–2. |
| `GF01_V0_Binder_Packet.pdf`                     | `docs/fixtures/gf01/GF01_V0_Binder_Packet.pdf`          | Binder pack for GF-01 V0. |

### 2.2 AETHER V0 Lookup & Templates

| Local filename                        | Recommended repo path                                      | Notes |
|---------------------------------------|------------------------------------------------------------|-------|
| `AETHER_V0_Lookup_Booklet.pdf`       | `docs/fixtures/aether_v0/AETHER_V0_Lookup_Booklet.pdf`    | AETHER V0 lookup booklet. |
| `AETHER_V0_Paper_Templates.pdf`      | `docs/fixtures/aether_v0/AETHER_V0_Paper_Templates.pdf`   | AETHER V0 paper templates. |

---

## 3. Pillar Bundles (ZIPs)

These ZIPs are bundles of pillar-related content (paper + text + misc). They don’t have a single “canonical” target folder yet, but a good initial home is under `docs/fixtures/pillars/` or `docs/raw/` so they’re available without polluting the core specs.

| Local filename                 | Suggested repo path                         | Notes |
|--------------------------------|---------------------------------------------|-------|
| `universal matrix pillar.zip`  | `docs/fixtures/pillars/universal_matrix_pillar.zip` | UMX pillar bundle. |
| `trinity gate pillar.zip`      | `docs/fixtures/pillars/trinity_gate_pillar.zip`     | Trinity Gate pillar bundle. |
| `astral press pillar.zip`      | `docs/fixtures/pillars/astral_press_pillar.zip`     | Astral Press pillar bundle. |
| `aevum loom pillar.zip`        | `docs/fixtures/pillars/aevum_loom_pillar.zip`       | Loom pillar bundle. |
| `codex eterna pillar.zip`      | `docs/fixtures/pillars/codex_eterna_pillar.zip`     | Codex pillar bundle. |
| `aether full clean.zip`        | `docs/fixtures/aether_v0/aether_full_clean.zip`     | Full clean Aether pack. |
| `aether paper pairity.zip`     | `docs/fixtures/aether_v0/aether_paper_parity.zip`   | Paper parity pack. |

*(You can rename `pairity`→`parity` on import if you want.)*

---

## 4. Generated Zips (Mirror Packs for Specs & Guides)

These are just convenience zips containing the markdown files above, so you only need to drag one file per artifact if you prefer.

| Local filename                                                     | Contents (primary)                                          | Suggested repo use |
|--------------------------------------------------------------------|--------------------------------------------------------------|--------------------|
| `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1_2025-11-23.zip` | `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md`       | Unzip and put the `.md` into `docs/specs/`. |
| `SPEC_003_Phase_3_Issue_Pack_v1_2025-11-23.zip`                   | `SPEC_003_Phase_3_Issue_Pack_v1.md`                         | Same, into `docs/specs/`. |
| `SPEC_004_Phase_3_Issue_Pack_v1_2025-11-23.zip`                   | `SPEC_004_Phase_3_Issue_Pack_v1.md`                         | Same, into `docs/specs/`. |
| `SPEC_006_Phase_4_Issue_Pack_v1_2025-11-23.zip`                   | `SPEC_006_Phase_4_Issue_Pack_v1.md`                         | Same, into `docs/specs/`. |
| `SPEC_007_Phase_5_Issue_Pack_v1_2025-11-23.zip`                   | `SPEC_007_Phase_5_Issue_Pack_v1.md`                         | Same, into `docs/specs/`. |
| `Aether_Repo_Bootstrap_Guide_v1_2025-11-23.zip`                   | `Aether_Repo_Bootstrap_Guide_v1.md`                         | Unzip and place `.md` into `docs/`. |

The pillar ZIPs (`universal matrix pillar.zip`, etc.) and Aether packs (`aether full clean.zip`, `aether paper pairity.zip`) already appear in the table above.

---

## 5. Quick Import Checklist

When you create the `aether-engine` repo, you can use this abbreviated checklist:

1. **Create directories:**  
   - `docs/specs/`  
   - `docs/contracts/`  
   - `docs/fixtures/gf01/`  
   - `docs/fixtures/aether_v0/`  
   - `docs/fixtures/pillars/` (optional but useful)

2. **Copy specs & guides:**  
   - `SPEC_000_Aether_Master_Spec_Index_and_Roadmap_v1.md` → `docs/specs/`  
   - `spec_001_aether_full_system_build_plan_medium_agnostic.md` → `docs/specs/`  
   - Pillar master specs → `docs/specs/`  
   - All `SPEC_00X_*_Issue_Pack_v1.md` → `docs/specs/`  
   - `Aether_Repo_Bootstrap_Guide_v1.md` → `docs/`

3. **Copy fixtures:**  
   - All `GF01_*` PDFs → `docs/fixtures/gf01/`  
   - `AETHER_V0_*` PDFs → `docs/fixtures/aether_v0/`  
   - Pillar and Aether ZIPs → `docs/fixtures/pillars/` or `docs/fixtures/aether_v0/` as per table.

4. **(Later)** Add contracts, `src/`, `tests/`, and CI as described in `Aether_Repo_Bootstrap_Guide_v1.md`.

---

End of Aether Artifact Index (Chat Session) — v1.
