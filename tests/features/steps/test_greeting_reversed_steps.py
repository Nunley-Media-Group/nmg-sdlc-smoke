import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_public_greeting_reversed_library_helper.feature")

PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_bytes",
    "greeting_casefold",
    "greeting_ends_with_exclamation",
    "greeting_ends_with_name",
    "greeting_has_apostrophe",
    "greeting_has_ascii_asterisk",
    "greeting_has_asterisk",
    "greeting_has_at_sign",
    "greeting_has_backslash",
    "greeting_has_backtick",
    "greeting_has_colon",
    "greeting_has_dollar",
    "greeting_has_double_quote",
    "greeting_has_equal",
    "greeting_has_exclamation",
    "greeting_has_exclamation_or_question",
    "greeting_has_hash",
    "greeting_has_percent",
    "greeting_has_plus",
    "greeting_has_question_mark",
    "greeting_has_semicolon",
    "greeting_has_slash",
    "greeting_has_underscore",
    "greeting_is_ascii",
    "greeting_length",
    "greeting_starts_with_hello",
    "greeting_word_count",
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when(
    "greeting_reversed is called with Ada and with Zoë spelled with the precomposed "
    "U+00EB code point"
)
def reverse_greetings(context: dict[str, object]) -> None:
    context["results"] = [library.greeting_reversed(name) for name in ("Ada", "Zo\u00eb")]


@then("the results are exactly adA ,olleH and ëoZ ,olleH")
def reversed_greetings(context: dict[str, object]) -> None:
    assert context["results"] == ["adA ,olleH", "\u00eboZ ,olleH"]


@given("the invalid names empty, three spaces, and None")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", "   ", None)


@when("greeting_reversed is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_reversed(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 3


@when(
    "greeting_reversed is imported from nmg_sdlc_smoke, greet is called with Ada, "
    "and nmg-smoke Ada runs"
)
def existing_surfaces(context: dict[str, object]) -> None:
    from nmg_sdlc_smoke import greeting_reversed

    context["imported"] = greeting_reversed
    context["greeting"] = library.greet("Ada")
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then("greeting_reversed is listed in __all__ alongside every previously listed export")
def exports_listed(context: dict[str, object]) -> None:
    assert context["imported"] is library.greeting_reversed
    assert "greeting_reversed" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "greet returns Hello, Ada and nmg-smoke prints Hello, Ada with one newline "
    "and exit status 0"
)
def unchanged_outputs(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")
