from pathlib import Path

from ops.snapshots import compare_snapshots

CONFIG_PATH = Path("docs/fixtures/configs/gov_codex_demo_run_config.json")
SNAPSHOT_PATH = Path("tests/fixtures/snapshots/governance_codex_demo/run_snapshot.json")


def test_governance_codex_demo_matches_snapshot_and_applies_actions():
    diffs, candidate = compare_snapshots(
        baseline_path=SNAPSHOT_PATH, run_config=CONFIG_PATH, max_diffs=20
    )

    assert diffs == []

    proposals = candidate["tick_result"].get("codex_proposals", [])
    assert proposals, "Expected codex proposals to be present in the demo run"
    assert any(proposal["status"] == "ACCEPTED" for proposal in proposals)

    budget = candidate["tick_result"].get("governance_budget_usage", {})
    assert budget.get("actions_accepted") == 1
    assert budget.get("proposals_seen") == len(proposals)
