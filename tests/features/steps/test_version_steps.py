import importlib.metadata
import shutil
import subprocess

import pytest
from pytest_bdd import given, scenarios, then, when


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
    assert shutil.which("nmg-smoke") is not None


def run_console_script(context: dict[str, object], *arguments: str) -> None:
    executable = shutil.which("nmg-smoke")
    assert executable is not None
    context["result"] = subprocess.run(
        [executable, *arguments],
        capture_output=True,
        check=False,
        text=True,
    )


@when("nmg-smoke --version is run")
def invoke_version(context: dict[str, object]) -> None:
    run_console_script(context, "--version")


@when("nmg-smoke Ada is run")
def invoke_greeting(context: dict[str, object]) -> None:
    run_console_script(context, "Ada")


@when("nmg-smoke is run with no arguments")
def invoke_without_arguments(context: dict[str, object]) -> None:
    run_console_script(context)


@when("nmg-smoke --version is run with a name also present")
def invoke_version_with_name(context: dict[str, object]) -> None:
    run_console_script(context, "--version", "Ada")


@then("the process exits 0")
def process_exits_zero(context: dict[str, object]) -> None:
    result = context["result"]
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 0


@then(
    "stdout is exactly the installed package version derived through "
    "importlib.metadata for nmg-sdlc-smoke-python, followed by a single newline"
)
def stdout_is_installed_version(context: dict[str, object]) -> None:
    result = context["result"]
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.stdout == (
        importlib.metadata.version("nmg-sdlc-smoke-python") + "\n"
    )
    assert result.stderr == ""



@then("the process exits 0 and prints Hello, Ada followed by a single newline")
def greeting_is_unchanged(context: dict[str, object]) -> None:
    result = context["result"]
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 0
    assert result.stdout == "Hello, Ada\n"
    assert result.stderr == ""


@then("the process exits non-zero and does not print a greeting")
def missing_name_fails(context: dict[str, object]) -> None:
    result = context["result"]
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode != 0
    assert result.stdout == ""


@then("the process does not print a greeting")
def greeting_not_printed(context: dict[str, object]) -> None:
    result = context["result"]
    assert isinstance(result, subprocess.CompletedProcess)
    assert "Hello," not in result.stdout
