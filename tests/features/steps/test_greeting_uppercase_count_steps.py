import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_uppercase_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PROSE = (
    "`greeting_uppercase_count` counts the 26 ASCII capitals `A`\u2013`Z` in the "
    "complete greeting (not the name alone), including the `H` in `Hello`; "
    "lowercase, accented, and fullwidth letters are not counted, and it inherits "
    '`greet`\'s `ValueError("name must not be blank")` for empty, whitespace-only, '
    "and non-string names."
)
PRIOR_EXPORTS = [name for name in library.__all__ if name != "greeting_uppercase_count"]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when("greeting_uppercase_count is called with Ada and with ABC XYZ")
def count_ascii_capitals(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_uppercase_count(name) for name in ("Ada", "ABC XYZ")
    ]


@then("the results are the Python int values 2 and 7")
def ascii_capital_counts(context: dict[str, object]) -> None:
    assert context["results"] == [2, 7]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_uppercase_count is called with bob 42!, \u00c9mile spelled with "
    "precomposed U+00C9, and fullwidth U+FF22 U+FF23"
)
def count_non_capitals(context: dict[str, object]) -> None:
    names = ("bob 42!", "\u00c9mile", "\uff22\uff23")
    context["results"] = [library.greeting_uppercase_count(name) for name in names]


@then("the results are 1, 1, and 1")
def non_capital_counts(context: dict[str, object]) -> None:
    assert context["results"] == [1, 1, 1]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_uppercase_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_uppercase_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_uppercase_count of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_uppercase_count("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )


@then("it prints 2 and greeting_uppercase_count is listed in nmg_sdlc_smoke.__all__")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\n", "")
    assert "greeting_uppercase_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the ASCII A-Z set, completed-greeting scope, and "
    "inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
