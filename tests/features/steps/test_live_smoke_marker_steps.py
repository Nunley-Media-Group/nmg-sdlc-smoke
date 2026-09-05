import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

scenarios("../add_live_smoke_362_a_verification_marker.feature")

ROOT = Path(__file__).parents[3]
NESTED_VERIFICATION = "NMG_SDLC_82_NESTED_VERIFICATION"


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


@given("the issue 82 marker exists")
def marker_exists() -> None:
    if os.environ.get(NESTED_VERIFICATION) == "1":
        pytest.skip("outer SCN002 owns recursive verification")
    assert (ROOT / "LIVE_SMOKE_362_A.txt").is_file()


@when("pytest, feature pytest, and Ruff run for issue 82")
def run_verification_commands(context: dict[str, object]) -> None:
    env = os.environ.copy()
    env[NESTED_VERIFICATION] = "1"
    commands = (
        (sys.executable, "-m", "pytest"),
        (sys.executable, "-m", "pytest", "tests/features"),
        (sys.executable, "-m", "ruff", "check", "."),
    )
    context["verification_results"] = [
        subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        for command in commands
    ]


@then("each issue 82 verification command exits zero")
def verification_commands_pass(context: dict[str, object]) -> None:
    results = context["verification_results"]
    assert isinstance(results, list)
    failures = [
        f"{result.args}: {result.stdout}\n{result.stderr}"
        for result in results
        if result.returncode != 0
    ]
    assert not failures, "\n".join(failures)


@given("the completed issue 82")
def completed_issue() -> None:
    assert (ROOT / "LIVE_SMOKE_362_A.txt").is_file()


@when("changed product paths for issue 82 are inspected")
def inspect_product_paths(context: dict[str, object]) -> None:
    addition = subprocess.run(
        (
            "git",
            "log",
            "--diff-filter=A",
            "--format=%H",
            "--",
            "LIVE_SMOKE_362_A.txt",
        ),
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    assert addition, "marker addition commit was not found"
    changed_paths = subprocess.run(
        (
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            addition[-1],
        ),
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    context["product_paths"] = [
        path
        for path in changed_paths
        if not path.startswith(("specs/", "tests/"))
    ]


@then("only LIVE_SMOKE_362_A.txt is added as an issue 82 product change")
def only_marker_is_product_change(context: dict[str, object]) -> None:
    assert context["product_paths"] == ["LIVE_SMOKE_362_A.txt"]
