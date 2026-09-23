import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_has_semicolon_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed greeting library and a valid name containing a semicolon")
def name_with_semicolon(context: dict[str, object]) -> None:
    context["name"] = "Ada;"


@given("the installed greeting library and a valid name without a semicolon")
def name_without_semicolon(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_semicolon is called with Ada;")
@when("greeting_has_semicolon is called with Ada")
def detect_semicolon(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = library.greet(name)
    context["result"] = library.greeting_has_semicolon(name)


@then("it returns True for the completed greeting Hello, Ada;")
def detects_literal_semicolon(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada;"
    assert context["result"] is True


@then("it returns False for the completed greeting Hello, Ada")
def reports_absent_semicolon(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@given("empty, whitespace-only, and non-string names")
def invalid_names(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t\n", None, 42)


@when("greeting_has_semicolon is called with each invalid name")
def detect_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["invalid_names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_has_semicolon(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def reports_validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the installed package and its console script")
def installed_package(context: dict[str, object]) -> None:
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when("greet and nmg-smoke greet Ada")
def greet_ada(context: dict[str, object]) -> None:
    context["greeting"] = library.greet("Ada")
    executable = context["executable"]
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then("the library returns Hello, Ada and the CLI exits 0 with exactly Hello, Ada and one newline on stdout and empty stderr")
def preserves_greeting_and_cli(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then("all previously exported public helpers remain importable")
def preserves_public_exports() -> None:
    from nmg_sdlc_smoke import (
        greet,
        greet_many,
        greeting_bytes,
        greeting_casefold,
        greeting_ends_with_exclamation,
        greeting_ends_with_name,
        greeting_is_ascii,
        greeting_length,
        greeting_starts_with_hello,
        greeting_word_count,
    )

    assert all(
        callable(helper)
        for helper in (
            greet,
            greet_many,
            greeting_bytes,
            greeting_casefold,
            greeting_ends_with_exclamation,
            greeting_ends_with_name,
            greeting_is_ascii,
            greeting_length,
            greeting_starts_with_hello,
            greeting_word_count,
        )
    )
