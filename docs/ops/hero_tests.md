# Hero Test Runbook

This runbook explains how to run the “hero” coverage associated with the Stage 2 spin-chain experiment. The suite exercises the high-qubit PFNA/Gate ingest path that backs the hero scenario.

## Prerequisites
- Python 3.11+
- Dependencies installed (`python -m pip install -r requirements.txt`)
- Worktree root set as the current directory
- Environment points at the source tree: `export PYTHONPATH=src`

## Running all hero-focused tests
Execute the focused unit suite that covers PFNA replay, Gate harness replay, and CLI smoke coverage for the hero ingest flows:

```bash
PYTHONPATH=src pytest -q \
  tests/unit/test_quantum_ingest_pfna.py \
  tests/unit/test_dpi_quantum_gate_cli.py
```

## Running a single hero smoke
To run only the Gate replay CLI smoke (the quickest hero check):

```bash
PYTHONPATH=src pytest -q tests/unit/test_dpi_quantum_gate_cli.py -k gate_replay
```

## Notes
- The tests currently drive 5–7 qubit synthetic statevectors; adjust the `qubits` defaults in the tests if you need a higher-width stress run.
- All commands assume you run them from the repository root.
