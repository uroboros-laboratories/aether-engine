# codex module

Codex is the observer-only learning pillar. The initial implementation adds a
`CodexContext` that can ingest CMP-0 run artefacts (UMX tick ledgers, Loom
blocks, APX manifests, optional NAP envelopes) and build lightweight pattern
and motif tallies. Motif discovery currently uses a deterministic edge-flux
pattern heuristic: repeated ledger signatures are converted into
`CodexLibraryEntryV1` motifs with simple MDL/usage stats. Motifs that meet
usage thresholds can be turned into `CodexProposalV1` records (e.g. PLACE
actions) while keeping Codex in observer-only mode.

See `docs/specs/spec_005_Phase_2_Pillar_V1_Implementation_Plan.md` and
`docs/contracts/CodexContracts_v1.md` for the surrounding design goals.
