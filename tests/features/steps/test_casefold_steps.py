import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_casefolded_greeting_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed greeting library")
@given("the installed package")
def installed_library() -> None:
    assert callable(library.greeting_casefold)


@when("greeting_casefold is called for Straße and Ada")
def casefold_greetings(context: dict[str, object]) -> None:
    context["results"] = [library.greeting_casefold(name) for name in ("Straße", "Ada")]


@then("the results are hello, strasse and hello, ada")
def normalized_greetings(context: dict[str, object]) -> None:
    assert context["results"] == ["hello, strasse", "hello, ada"]


@given("blank, whitespace-only, and non-string names")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_casefold is called")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_casefold(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("the existing greet ValueError is raised")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@when("greet and nmg-smoke greet Ada")
def existing_surfaces(context: dict[str, object]) -> None:
    context["greeting"] = library.greet("Ada")
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then("the existing Hello, Ada outputs and CLI newline are unchanged")
def unchanged_outputs(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then("existing public exports remain available")
def existing_exports() -> None:
    assert library.greet_many(["Ada", "Bob"]) == ["Hello, Ada", "Hello, Bob"]
    assert library.greeting_bytes("É") == 9
    assert library.greeting_length("É") == 8
    assert library.greeting_is_ascii("É") is False
    assert library.greeting_starts_with_hello("Ada") is True
    assert library.greeting_ends_with_name("Ada") is True
    assert library.greeting_ends_with_exclamation("Ada") == "Hello, Ada!"
