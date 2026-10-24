import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_lowercase_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PROSE = (
    "`greeting_lowercase_count` counts the 26 ASCII lowercase letters `a`\u2013`z` in "
    "the complete greeting (not the name alone), including the `ello` in `Hello`; "
    "uppercase, accented, and fullwidth letters are not counted, and it inherits "
    '`greet`\'s `ValueError("name must not be blank")` for empty, whitespace-only, '
    "and non-string names."
)
PRIOR_EXPORTS = [name for name in library.__all__ if name != "greeting_lowercase_count"]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greet)


@when("greeting_lowercase_count is called with Ada and with abc xyz")
def count_ascii_lowercase(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_lowercase_count(name) for name in ("Ada", "abc xyz")
    ]


@then("the results are the Python int values 6 and 10")
def ascii_lowercase_counts(context: dict[str, object]) -> None:
    assert context["results"] == [6, 10]
    assert all(type(result) is int for result in context["results"])


@when(
    "greeting_lowercase_count is called with BOB 42!, precomposed U+00E9, and "
    "fullwidth U+FF42 U+FF43"
)
def count_non_lowercase(context: dict[str, object]) -> None:
    names = ("BOB 42!", "\u00e9", "\uff42\uff43")
    context["results"] = [library.greeting_lowercase_count(name) for name in names]


@then("the results are 4, 4, and 4")
def non_lowercase_counts(context: dict[str, object]) -> None:
    assert context["results"] == [4, 4, 4]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_lowercase_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_lowercase_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_lowercase_count of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_lowercase_count("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )


@then("it prints 6 and greeting_lowercase_count is listed in nmg_sdlc_smoke.__all__")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "6\n", "")
    assert "greeting_lowercase_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the ASCII a-z set, completed-greeting scope, and "
    "inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
