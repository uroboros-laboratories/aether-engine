from pathlib import Path
import pytest

from config import EngineRuntime
from operator_service import RunRegistry


@pytest.fixture()
def registry() -> RunRegistry:
    runtime = EngineRuntime(repo_root=Path(__file__).resolve().parents[2])
    return RunRegistry(runtime)


def test_run_registry_tracks_completion(registry: RunRegistry) -> None:
    handle = registry.start_run("gf01")
    assert handle.thread is not None

    handle.thread.join(timeout=10)
    assert not handle.thread.is_alive()

    status = registry.get_status(handle.status.run_id)
    assert status.state == "completed"
    assert status.ticks_completed == status.ticks_total == handle.session_config.total_ticks
    assert registry.current is None


def test_run_registry_enforces_single_active_run(registry: RunRegistry) -> None:
    handle = registry.start_run("gf01")
    assert handle.thread is not None

    with pytest.raises(RuntimeError):
        registry.start_run("gf01")

    handle.thread.join(timeout=10)


def test_run_registry_logs_support_cursor_and_filters(registry: RunRegistry) -> None:
    handle = registry.start_run("gf01")
    assert handle.thread is not None

    handle.thread.join(timeout=10)

    entries, cursor = registry.get_logs(handle.status.run_id)
    assert entries
    assert cursor == len(entries)

    empty_entries, empty_cursor = registry.get_logs(handle.status.run_id, cursor=cursor)
    assert empty_entries == []
    assert empty_cursor == cursor

    filtered, filtered_cursor = registry.get_logs(
        handle.status.run_id, cursor=1, event_type=entries[-1]["event"]
    )
    assert filtered_cursor == cursor
    assert all(entry["event"] == entries[-1]["event"] for entry in filtered)

    with pytest.raises(ValueError):
        registry.get_logs(handle.status.run_id, cursor=-1)
    with pytest.raises(KeyError):
        registry.get_logs("missing")


def test_run_registry_exposes_pillars(registry: RunRegistry) -> None:
    handle = registry.start_run("gf01")
    assert handle.thread is not None

    handle.thread.join(timeout=10)

    pillars = registry.get_pillars(handle.status.run_id)

    assert isinstance(pillars, list)
    assert pillars
    assert {pill["status"] for pill in pillars} == {"IDLE"}
    assert all("headline_metric_label" in pill for pill in pillars)
    assert all("headline_metric_value" in pill for pill in pillars)
