from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

scenarios("../add_live_smoke_362_a_verification_marker.feature")

ROOT = Path(__file__).parents[3]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the repository root for issue 82")
def repository_root(context: dict[str, object]) -> None:
    context["root"] = ROOT


@when("LIVE_SMOKE_362_A.txt is read")
def read_marker(context: dict[str, object]) -> None:
    root = context["root"]
    assert isinstance(root, Path)
    marker = root / "LIVE_SMOKE_362_A.txt"
    context["marker_is_file"] = marker.is_file()
    context["marker_bytes"] = marker.read_bytes()


@then("it contains exactly LIVE_SMOKE_362_A followed by one newline")
def marker_has_exact_content(context: dict[str, object]) -> None:
    assert context["marker_is_file"] is True
    assert context["marker_bytes"] == b"LIVE_SMOKE_362_A\n"
