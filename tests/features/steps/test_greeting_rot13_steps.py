import codecs
import string
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_rot13_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_ROT13 = "Uryyb, Nqn"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_base64",
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
    "greeting_reversed",
    "greeting_sha256",
    "greeting_starts_with_hello",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_rot13` applies ROT13 to the complete greeting (not the name alone), "
    "rotating only the ASCII letters `A`–`Z` and `a`–`z` by 13 places within their "
    "case and leaving every other character, including non-ASCII letters, "
    "unchanged; applying ROT13 again restores the greeting, and it inherits "
    "`greet`'s `ValueError(\"name must not be blank\")` for empty, whitespace-only, "
    "and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_rot13)


@when("greeting_rot13 is called with Ada")
def rotate_ada(context: dict[str, object]) -> None:
    context["result"] = library.greeting_rot13("Ada")


@then("the result is the Python str Uryyb, Nqn")
def ada_rot13(context: dict[str, object]) -> None:
    result = context["result"]
    assert type(result) is str
    assert result == ADA_ROT13


@when(
    "greeting_rot13 is called with Mary-Jane O'Neil, with Zo followed by "
    "precomposed U+00EB, and with fullwidth U+FF3A followed by ed 42"
)
def rotate_mixed_names(context: dict[str, object]) -> None:
    context["names"] = ("Mary-Jane O'Neil", "Zoë", "Ｚed 42")
    context["results"] = [library.greeting_rot13(name) for name in context["names"]]


@then(
    "the results are Uryyb, Znel-Wnar B'Arvy and Uryyb, Mb followed by U+00EB "
    "and Uryyb, followed by U+FF3A and rq 42"
)
def mixed_results(context: dict[str, object]) -> None:
    assert context["results"] == [
        "Uryyb, Znel-Wnar B'Arvy",
        "Uryyb, Mbë",
        "Uryyb, Ｚrq 42",
    ]


@then("every character that is not an ASCII letter is unchanged at the same position")
def non_letters_unchanged(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        greeting = library.greet(name)
        assert len(result) == len(greeting)
        for index, character in enumerate(greeting):
            if character not in string.ascii_letters:
                assert result[index] == character


@when(
    "ROT13 is applied again to greeting_rot13 of Ada, Zo followed by U+00EB, "
    "and Mary-Jane O'Neil"
)
def rotate_twice(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Zoë", "Mary-Jane O'Neil")
    context["results"] = [
        codecs.encode(library.greeting_rot13(name), "rot13")
        for name in context["names"]
    ]


@then("each result equals greet of the same name")
def round_trip(context: dict[str, object]) -> None:
    assert context["results"] == [library.greet(name) for name in context["names"]]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_rot13 is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_rot13(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_rot13 of Ada, and "
    "nmg-smoke Ada runs"
)
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_rot13("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then("the example prints Uryyb, Nqn")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_ROT13 + "\n",
        "",
    )


@then(
    "greeting_rot13 is listed in nmg_sdlc_smoke.__all__ alongside every "
    "previously listed export"
)
def exports_listed() -> None:
    assert "greeting_rot13" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("nmg-smoke prints Hello, Ada with one newline and exit status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then(
    "the README documents ASCII-only ROT13 of the complete greeting, unchanged "
    "other characters, and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
