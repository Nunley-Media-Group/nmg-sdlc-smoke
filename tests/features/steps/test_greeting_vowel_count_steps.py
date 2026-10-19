import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_vowel_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PROSE = (
    "`greeting_vowel_count` counts the ten ASCII vowels `a e i o u A E I O U` in the "
    "complete greeting (not the name alone); `y`, accented, and fullwidth letters are "
    'not counted, and it inherits `greet`\'s `ValueError("name must not be blank")` '
    "for empty, whitespace-only, and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when("greeting_vowel_count is called with Ada and with AEIOU aeiou")
def count_ascii_vowels(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_vowel_count(name) for name in ("Ada", "AEIOU aeiou")
    ]


@then("the results are the Python int values 4 and 12")
def ascii_vowel_counts(context: dict[str, object]) -> None:
    assert context["results"] == [4, 12]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_vowel_count is called with Bcd, Ady, Émile spelled with precomposed "
    "U+00C9, and fullwidth U+FF21 U+FF44 U+FF41"
)
def count_non_vowels(context: dict[str, object]) -> None:
    names = ("Bcd", "Ady", "\u00c9mile", "\uff21\uff44\uff41")
    context["results"] = [library.greeting_vowel_count(name) for name in names]


@then("the results are 2, 3, 4, and 2")
def non_vowel_counts(context: dict[str, object]) -> None:
    assert context["results"] == [2, 3, 4, 2]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_vowel_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_vowel_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_vowel_count of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_vowel_count("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )


@then("it prints 4 and greeting_vowel_count is listed in nmg_sdlc_smoke.__all__")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "4\n", "")
    assert "greeting_vowel_count" in library.__all__


@then(
    "the README documents the ASCII vowel set, completed-greeting scope, and "
    "inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
