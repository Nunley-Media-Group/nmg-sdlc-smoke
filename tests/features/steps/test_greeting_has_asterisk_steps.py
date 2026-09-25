import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_asterisk

scenarios("../add_public_greeting_has_asterisk_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the public greeting library and valid name Ada followed by ASCII U+002A")
def ascii_asterisk_name(context: dict[str, object]) -> None:
    context["name"] = "Ada*"


@given("the public greeting library and valid name Ada without an asterisk")
def name_without_asterisk(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@given("the public greeting library and valid name Ada followed by U+2217")
def operator_name(context: dict[str, object]) -> None:
    context["name"] = "Ada∗"


@when("greeting_has_asterisk is called with Ada followed by ASCII U+002A")
@when("greeting_has_asterisk is called with Ada")
@when("greeting_has_asterisk is called with Ada followed by U+2217")
def call_asterisk_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_asterisk(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada followed by ASCII U+002A and the result is Python True")
def ascii_asterisk_detected(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada*"
    assert context["result"] is True


@then("the completed greeting is Hello, Ada and the asterisk result is Python False")
def ascii_asterisk_absent(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@then("the completed greeting is Hello, Ada followed by U+2217 and the result is Python False")
def operator_does_not_match(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada∗"
    assert context["result"] is False


@given("invalid names empty, whitespace-only, None, and 42 for the asterisk helper")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_asterisk is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_asterisk(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each asterisk helper call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the public greeting library and installed nmg-smoke script for the asterisk helper")
def public_library_and_script(context: dict[str, object]) -> None:
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when("greeting_has_asterisk is imported, greet Ada is evaluated, and nmg-smoke Ada is run")
def invoke_greeting_and_script(context: dict[str, object]) -> None:
    context["helper"] = greeting_has_asterisk
    context["greeting"] = greet("Ada")
    context["cli"] = subprocess.run(
        [str(context["executable"]), "Ada"],
        capture_output=True,
        text=True,
        check=False,
    )


@then("the import succeeds, the library returns Hello, Ada, and the CLI exits zero with one Hello, Ada newline on stdout and empty stderr")
def greeting_and_cli_unchanged(context: dict[str, object]) -> None:
    assert context["helper"] is greeting_has_asterisk
    assert context["greeting"] == "Hello, Ada"
    cli = context["cli"]
    assert (cli.returncode, cli.stdout, cli.stderr) == (0, "Hello, Ada\n", "")
