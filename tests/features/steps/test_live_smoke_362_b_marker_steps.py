import json
import os
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

scenarios("../add_live_smoke_362_b_verification_marker.feature")

ROOT = Path(__file__).parents[3]
MARKER = ROOT / "LIVE_SMOKE_362_B.txt"


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@pytest.fixture
def verification_evidence() -> dict[str, object]:
    # The parent runner records real gates and scope; never spawn pytest here.
    path = os.environ.get("NMG_ISSUE_85_EVIDENCE")
    if path is None:
        pytest.skip("requires parent-run issue 85 verification evidence")
    evidence = json.loads(Path(path).read_text(encoding="utf-8"))
    assert evidence["issue"] == 85
    return evidence


@given("the repository root for issue 85")
def repository_root() -> None:
    assert ROOT.is_dir()


@given("the issue 85 marker exists")
def marker_exists() -> None:
    assert MARKER.is_file()
    assert not MARKER.is_symlink()


@when("LIVE_SMOKE_362_B.txt is read")
def read_marker(context: dict[str, object]) -> None:
    marker_exists()
    context["marker_bytes"] = MARKER.read_bytes()


@then("it contains exactly LIVE_SMOKE_362_B followed by one newline")
def marker_has_exact_content(context: dict[str, object]) -> None:
    assert context["marker_bytes"] == b"LIVE_SMOKE_362_B\n"


@when("the repository verification gates run outside this scenario")
def read_gate_outcomes(
    context: dict[str, object], verification_evidence: dict[str, object]
) -> None:
    context["gates"] = verification_evidence["gates"]


@then("their recorded outcomes are all successful")
def gates_succeeded(context: dict[str, object]) -> None:
    assert context["gates"] == {
        "python -m pytest": 0,
        "python -m pytest tests/features": 0,
        "python -m ruff check .": 0,
    }


@given("the completed issue 85 change")
def completed_change(verification_evidence: dict[str, object]) -> None:
    marker_exists()


@when("changed product paths are inspected")
def inspect_product_paths(
    context: dict[str, object], verification_evidence: dict[str, object]
) -> None:
    context["product_changes"] = verification_evidence["product_changes"]


@then("only LIVE_SMOKE_362_B.txt is added")
def product_change_is_isolated(context: dict[str, object]) -> None:
    assert context["product_changes"] == {"LIVE_SMOKE_362_B.txt": "added"}
