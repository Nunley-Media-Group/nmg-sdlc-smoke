import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_has_digit_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed greeting library with a digit helper")
def installed_library() -> None:
    assert callable(library.greeting_has_digit)


@when("I check Ada7, Ada٣, and Ada for decimal digits")
def check_names(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_has_digit(name) for name in ("Ada7", "Ada٣", "Ada")
    ]


@then("the results are True, True, and False")
def digit_results(context: dict[str, object]) -> None:
    assert context["results"] == [True, True, False]


@given("blank, whitespace-only, and non-string digit-helper inputs")
def invalid_inputs(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("I check each invalid name for decimal digits")
def check_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_has_digit(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each raises the existing greet ValueError")
def validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the installed package with its existing public exports")
def public_exports() -> None:
    assert callable(library.greeting_has_digit)


@when("greet and nmg-smoke greet Ada")
def greet_ada(context: dict[str, object]) -> None:
    context["greeting"] = library.greet("Ada")
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then("both return the existing Hello, Ada output with the CLI newline")
def existing_output(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then("all existing public exports remain available")
def existing_exports() -> None:
    for name in (
        "greet",
        "greet_many",
        "greeting_bytes",
        "greeting_casefold",
        "greeting_ends_with_exclamation",
        "greeting_ends_with_name",
        "greeting_is_ascii",
        "greeting_length",
        "greeting_starts_with_hello",
        "greeting_word_count",
    ):
        assert name in library.__all__
        assert callable(getattr(library, name))
