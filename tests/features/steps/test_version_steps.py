import importlib.metadata

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke.cli import main

scenarios("../add_nmg_smoke_version_output.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the distribution is installed")
def distribution_installed() -> None:
    assert importlib.metadata.version("nmg-sdlc-smoke-python")


@given("the distribution is installed with its console script")
def distribution_installed_with_console_script() -> None:
    distribution = importlib.metadata.distribution("nmg-sdlc-smoke-python")
    console_scripts = [
        entry_point
        for entry_point in distribution.entry_points
        if entry_point.group == "console_scripts"
        and entry_point.name == "nmg-smoke"
    ]
    assert len(console_scripts) == 1
    assert console_scripts[0].value == "nmg_sdlc_smoke.cli:main"


def run_cli(
    context: dict[str, object],
    capsys: pytest.CaptureFixture[str],
    *arguments: str,
) -> None:
    try:
        context["exit_code"] = main(list(arguments))
    except SystemExit as error:
        context["exit_code"] = error.code
    context["captured"] = capsys.readouterr()


@when("nmg-smoke --version is run")
def invoke_version(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    run_cli(context, capsys, "--version")


@when("nmg-smoke Ada is run")
def invoke_greeting(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    run_cli(context, capsys, "Ada")


@when("nmg-smoke is run with no arguments")
def invoke_without_arguments(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    run_cli(context, capsys)


@when("nmg-smoke --version is run with a name also present")
def invoke_version_with_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    run_cli(context, capsys, "--version", "Ada")


@then("the process exits 0")
def process_exits_zero(context: dict[str, object]) -> None:
    assert context["exit_code"] == 0


@then(
    "stdout is exactly the installed package version derived through "
    "importlib.metadata for nmg-sdlc-smoke-python, followed by a single newline"
)
def stdout_is_installed_version(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == (
        importlib.metadata.version("nmg-sdlc-smoke-python") + "\n"
    )
    assert captured.err == ""



@then("the process exits 0 and prints Hello, Ada followed by a single newline")
def greeting_is_unchanged(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@then("the process exits non-zero and does not print a greeting")
def missing_name_fails(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] != 0
    assert captured.out == ""


@then("the process does not print a greeting")
def greeting_not_printed(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert "Hello," not in captured.out
