# Phase 1-5 Gap Validation

Confirming that the gaps highlighted against the master pillar specs persist after completing the Phase 1–5 issue packs.

## Observations

- **UMX**: Implementation remains limited to the CMP-0 flux rule and basic tick ledger emission; epsilon handling, NAP bus contracts, and extended profiles from the master spec are absent.
- **Loom**: Only deterministic chain value updates and windowed checkpoints are present. There is no ε-ledger, hashing/Merkle integrity, or compression of P-/I-blocks.
- **Press/APX**: The module still contains only manifest types and length estimators for ID/R/GR; no encoding/decoding pipelines, AEON grammars, or policy enforcement layers exist.
- **Gate/TBP**: Gate code is confined to configuration types, PFNA V0 loaders, and Press stream declarations; governed ingress/egress workflows, normalization/integerization math, and NAP envelope orchestration remain unimplemented.
- **Codex Eterna**: Codex provides ingest counters, library/proposal shells, and governance annotations. Motif learning, MDL evaluation, reversible barriers, and governance-aware proposal application are still missing.
- **U-Ledger**: U-ledger builds simple hash links between pillar artefacts but lacks policy-aware or cross-pillar validation hooks described in the master specs.

## Conclusion

Across Phases 1–5, the repository continues to ship only the CMP-0 V1 skeletons. The richer master-spec features (epsilon handling, authenticated ledgers, PFNA normalization, compression grammars, governance workflows beyond policy hashing, motif learning, and comprehensive fixtures/tests) are still not implemented.
