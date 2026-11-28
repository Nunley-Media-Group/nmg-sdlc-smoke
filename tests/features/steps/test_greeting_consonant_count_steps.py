import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_consonant_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
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
    "greeting_reversed",
    "greeting_sha256",
    "greeting_starts_with_hello",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_consonant_count` counts the 42 ASCII consonant letters (every letter "
    "`A`–`Z` and `a`–`z` except `a e i o u A E I O U`, so `y` and `Y` count) in the "
    "complete greeting (not the name alone); vowels, digits, spaces, punctuation, "
    "accented, and fullwidth letters are not counted, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when("greeting_consonant_count is called with Ada and with all 42 ASCII consonants")
def count_ada_and_all_consonants(context: dict[str, object]) -> None:
    names = ("Ada", "BCDFGHJKLMNPQRSTVWXYZ bcdfghjklmnpqrstvwxyz")
    context["results"] = [library.greeting_consonant_count(name) for name in names]


@then("the results are the Python int values 4 and 45")
def ada_and_all_consonant_counts(context: dict[str, object]) -> None:
    assert context["results"] == [4, 45]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_consonant_count is called with Ady, Yy, Bob 42!, Émile spelled with "
    "precomposed U+00C9, and fullwidth U+FF22 U+FF43 U+FF44"
)
def count_y_and_non_consonants(context: dict[str, object]) -> None:
    names = ("Ady", "Yy", "Bob 42!", "Émile", "Ｂｃｄ")
    context["results"] = [library.greeting_consonant_count(name) for name in names]


@then("the results are 5, 5, 5, 5, and 3")
def y_and_non_consonant_counts(context: dict[str, object]) -> None:
    assert context["results"] == [5, 5, 5, 5, 3]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_consonant_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_consonant_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_consonant_count of Ada, and "
    "nmg-smoke Ada runs"
)
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_consonant_count("Ada"))\n'],
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


@then(
    "the example prints 4 and greeting_consonant_count is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_exports(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "4\n", "")
    assert "greeting_consonant_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("nmg-smoke prints Hello, Ada with one newline and exit status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then(
    "the README documents the 42-letter ASCII consonant set including y and Y, "
    "completed-greeting scope, and inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
