import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_punctuation_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PROSE = (
    "`greeting_punctuation_count` counts the 32 ASCII punctuation characters in "
    "Python's `string.punctuation` in the complete greeting (not the name alone), "
    "including the comma after `Hello`; non-ASCII punctuation and look-alikes such "
    "as `！`, `’`, and `、` are not counted, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_base64",
    "greeting_bytes",
    "greeting_casefold",
    "greeting_digit_count",
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
    "greeting_lowercase_count",
    "greeting_reversed",
    "greeting_sha256",
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_uppercase_count",
    "greeting_vowel_count",
    "greeting_word_count",
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_punctuation_count)


@when("greeting_punctuation_count is called with Ada, O'Brien, Ada!?, and a.b-c_d")
def count_ascii_punctuation(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_punctuation_count(name)
        for name in ("Ada", "O'Brien", "Ada!?", "a.b-c_d")
    ]


@then("the results are the Python int values 1, 2, 3, and 4")
def ascii_punctuation_counts(context: dict[str, object]) -> None:
    assert context["results"] == [1, 2, 3, 4]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_punctuation_count is called with Ada plus U+FF01, O U+2019 Brien, "
    "Ada plus U+3001, and Ada Lovelace 42"
)
def count_look_alikes(context: dict[str, object]) -> None:
    names = ("Ada！", "O’Brien", "Ada、", "Ada Lovelace 42")
    context["results"] = [library.greeting_punctuation_count(name) for name in names]


@then("the results are 1, 1, 1, and 1")
def look_alike_counts(context: dict[str, object]) -> None:
    assert context["results"] == [1, 1, 1, 1]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_punctuation_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_punctuation_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_punctuation_count of O'Brien"
)
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    script = example + 'print(greeting_punctuation_count("O\'Brien"))\n'
    context["run"] = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )


@then(
    "it prints 2 and greeting_punctuation_count is listed in nmg_sdlc_smoke.__all__"
)
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\n", "")
    assert "greeting_punctuation_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the ASCII string.punctuation set, completed-greeting scope, "
    "and inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
