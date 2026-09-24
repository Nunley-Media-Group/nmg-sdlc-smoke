import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_backtick

scenarios("../add_public_greeting_has_backtick_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada followed by ASCII U+0060 and the public greeting library")
def ascii_backtick_name(context: dict[str, object]) -> None:
    context["name"] = "Ada`"


@when("greeting_has_backtick is called with that name")
def call_backtick_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_backtick(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada followed by ASCII U+0060 and the result is Python True")
def ascii_backtick_detected(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada`"
    assert context["result"] is True


@given("valid names Ada and Ada followed by U+FF40")
def names_without_ascii_backtick(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada｀")


@when("greeting_has_backtick is called with each name")
def call_for_names_without_backtick(context: dict[str, object]) -> None:
    names = context["names"]
    context["greetings"] = [greet(name) for name in names]  # type: ignore[union-attr]
    context["results"] = [greeting_has_backtick(name) for name in names]  # type: ignore[union-attr]


@then("their completed greetings are Hello, Ada and Hello, Ada followed by U+FF40 and both results are Python False")
def ascii_backtick_absent(context: dict[str, object]) -> None:
    assert context["greetings"] == ["Hello, Ada", "Hello, Ada｀"]
    assert all(result is False for result in context["results"])  # type: ignore[union-attr]


@given("invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_backtick is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_backtick(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the public greeting library and installed nmg-smoke script")
def public_library_and_script(context: dict[str, object]) -> None:
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when("greet Ada is evaluated and nmg-smoke Ada is run")
def invoke_greeting_and_script(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")
    context["cli"] = subprocess.run(
        [str(context["executable"]), "Ada"],
        capture_output=True,
        text=True,
        check=False,
    )


@then("the library returns Hello, Ada and the CLI exits zero with one Hello, Ada newline on stdout and empty stderr")
def greeting_and_cli_unchanged(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    cli = context["cli"]
    assert (cli.returncode, cli.stdout, cli.stderr) == (0, "Hello, Ada\n", "")
