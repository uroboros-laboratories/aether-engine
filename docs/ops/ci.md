# Continuous Integration (Phase 3)

This repository uses a single GitHub Actions workflow to enforce the Phase 3 regression and determinism guarantees. The workflow lives at `.github/workflows/ci.yml` and runs automatically on every push and pull request.

## What runs

- Python 3.11 on `ubuntu-latest` runners.
- `python -m pip install --upgrade pip` followed by `python -m pip install pytest` to ensure pytest is available without additional dependencies.
- `PYTHONPATH=src python -m pytest` to execute all unit, integration, and snapshot regression tests. The test suite already exercises:
  - Scenario-driven regressions (GF-01, line, ring, AEON/APXi demos).
  - PFNA ingress/egress behaviour and APXi manifest handling.
  - Snapshot tooling, introspection CLI, logging/metrics, and config loaders.

## Expectations

- The workflow fails on any test or snapshot regression, keeping `main` green for all registered scenarios.
- Contributors should run the same command locally before opening a PR:

```bash
PYTHONPATH=src python -m pytest
```

This mirrors CI and ensures deterministic outputs match the checked-in snapshots.
