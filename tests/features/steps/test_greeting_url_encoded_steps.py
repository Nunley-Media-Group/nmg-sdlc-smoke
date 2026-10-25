import subprocess
import sys
import sysconfig
from pathlib import Path
from urllib.parse import unquote

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_url_encoded_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_URL_ENCODED = "Hello%2C%20Ada"
UNRESERVED = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~%"
)
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
    "`greeting_url_encoded` percent-encodes the complete greeting (not the name "
    "alone) as UTF-8 with uppercase hex digits, leaving only `A`–`Z`, `a`–`z`, "
    "`0`–`9`, `-`, `.`, `_`, and `~` unencoded (so a space becomes `%20` and `/` "
    "becomes `%2F`); `urllib.parse.unquote` restores the greeting, and it inherits "
    "`greet`'s `ValueError(\"name must not be blank\")` for empty, whitespace-only, "
    "and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_url_encoded)


@when("greeting_url_encoded is called with Ada")
def encode_ada(context: dict[str, object]) -> None:
    context["result"] = library.greeting_url_encoded("Ada")


@then("the result is the Python str Hello%2C%20Ada")
def ada_url_encoded(context: dict[str, object]) -> None:
    result = context["result"]
    assert type(result) is str
    assert result == ADA_URL_ENCODED


@when(
    "greeting_url_encoded is called with A/B&C~d_e.f and with Zo followed by "
    "precomposed U+00EB"
)
def encode_reserved_cases(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_url_encoded(name) for name in ("A/B&C~d_e.f", "Zoë")
    ]


@then("the results are Hello%2C%20A%2FB%26C~d_e.f and Hello%2C%20Zo%C3%AB")
def reserved_results(context: dict[str, object]) -> None:
    assert context["results"] == ["Hello%2C%20A%2FB%26C~d_e.f", "Hello%2C%20Zo%C3%AB"]


@then("every result character is an unreserved character or a percent sign")
def only_unreserved(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert set(result) <= UNRESERVED


@when(
    "urllib.parse.unquote is applied to greeting_url_encoded of Ada, Zo followed "
    "by U+00EB, and A/B&C~d_e.f"
)
def decode_cases(context: dict[str, object]) -> None:
    names = ("Ada", "Zoë", "A/B&C~d_e.f")
    context["names"] = names
    context["decoded"] = [
        unquote(library.greeting_url_encoded(name)) for name in names
    ]


@then("each result equals greet of the same name")
def decoded_equals_greeting(context: dict[str, object]) -> None:
    assert context["decoded"] == [library.greet(name) for name in context["names"]]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_url_encoded is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_url_encoded(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_url_encoded of Ada, and "
    "nmg-smoke Ada runs"
)
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_url_encoded("Ada"))\n'],
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


@then("the example prints Hello%2C%20Ada")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_URL_ENCODED + "\n",
        "",
    )


@then(
    "greeting_url_encoded is listed in nmg_sdlc_smoke.__all__ alongside every "
    "previously listed export"
)
def exports_listed() -> None:
    assert "greeting_url_encoded" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("nmg-smoke prints Hello, Ada with one newline and exit status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then(
    "the README documents UTF-8 percent-encoding of the complete greeting, the "
    "unreserved set, and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
