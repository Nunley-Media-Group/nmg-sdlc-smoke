import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_digit_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PROSE = (
    "`greeting_digit_count` counts the ten ASCII digits `0`\u2013`9` in the complete "
    "greeting (not the name alone); fullwidth, other-script, and superscript digits "
    "are not counted, and it inherits "
    '`greet`\'s `ValueError("name must not be blank")` for empty, whitespace-only, '
    "and non-string names."
)
PRIOR_EXPORTS = [name for name in library.__all__ if name != "greeting_digit_count"]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when("greeting_digit_count is called with R2D2, Agent 007, and Ada")
def count_ascii_digits(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_digit_count(name) for name in ("R2D2", "Agent 007", "Ada")
    ]


@then("the results are the Python int values 2, 3, and 0")
def ascii_digit_counts(context: dict[str, object]) -> None:
    assert context["results"] == [2, 3, 0]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_digit_count is called with fullwidth U+FF11 U+FF12, Arabic-Indic "
    "U+0663, and x with superscript U+00B2"
)
def count_non_ascii_digits(context: dict[str, object]) -> None:
    names = ("\uff11\uff12", "\u0663", "x\u00b2")
    context["results"] = [library.greeting_digit_count(name) for name in names]


@then("the results are 0, 0, and 0")
def non_digit_counts(context: dict[str, object]) -> None:
    assert context["results"] == [0, 0, 0]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_digit_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_digit_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_digit_count of R2D2")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_digit_count("R2D2"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )


@then("it prints 2 and greeting_digit_count is listed in nmg_sdlc_smoke.__all__")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\n", "")
    assert "greeting_digit_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the ASCII 0-9 set, completed-greeting scope, and "
    "inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
