# Troubleshooting test failures

## `tests/unit/test_run_registry.py::test_run_registry_enforces_single_active_run`

The failure output

```
E       Failed: DID NOT RAISE <class 'RuntimeError'>
```

means the second `RunRegistry.start_run()` call succeeded instead of raising. The
registry only rejects a new run when it sees an *active* run (state `pending` or
`running`). Because runs execute in a background thread, a fast scenario can
finish and clear the `current` handle before the second `start_run()` call runs,
so no active run is detected and the `pytest.raises(RuntimeError)` assertion
fails. Re-running the test typically passes because the timing race disappears,
but the failure indicates the run completed before the assertion was evaluated.
