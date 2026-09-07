import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_word_count_lifecycle_fixture.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given(parsers.parse('the name "{name}"'))
def name_input(context: dict[str, object], name: str) -> None:
    context["name"] = name


@when("I call the exported greeting_word_count helper")
def count_words(context: dict[str, object]) -> None:
    context["count"] = library.greeting_word_count(context["name"])


@then(parsers.parse("the word count is {count:d}"))
def expected_count(context: dict[str, object], count: int) -> None:
    assert context["count"] == count


@given("blank, whitespace-only, or non-string input")
def invalid_input(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t\n", None, 42)


@when("I call greeting_word_count for invalid input")
def invalid_counts(context: dict[str, object]) -> None:
    errors = []
    for name in context["invalid_names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_word_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("it raises the existing greet ValueError")
def validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@then("existing greeting and CLI contracts remain unchanged")
def existing_outputs() -> None:
    assert library.greet("Ada") == "Hello, Ada"
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    result = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@given("the documented public helper example")
def documented_example(context: dict[str, object]) -> None:
    root = Path(__file__).resolve().parents[3]
    readme = (root / "README.md").read_text(encoding="utf-8")
    context["example"] = readme.split("```python\n", 1)[1].split("```", 1)[0]


@when("I execute the README library example")
def run_example(context: dict[str, object]) -> None:
    code = context["example"] + (
        '\nprint(greeting_word_count("Ada"), greeting_word_count("Ada Lovelace"))\n'
    )
    context["example_result"] = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )


@then("the documented word counts are reproducible")
def documented_counts(context: dict[str, object]) -> None:
    result = context["example_result"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "2 3\n", "")
