import html
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_html_escaped_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_BO_ESCAPED = "Hello, &lt;Ada &amp; Bo&gt;"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_adler32",
    "greeting_ascii85",
    "greeting_base32",
    "greeting_base64",
    "greeting_base85",
    "greeting_blake2b",
    "greeting_blake2s",
    "greeting_bytes",
    "greeting_casefold",
    "greeting_crc32",
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
    "greeting_letter_count",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_punctuation_count",
    "greeting_reversed",
    "greeting_rot13",
    "greeting_sha1",
    "greeting_sha3_224",
    "greeting_sha3_256",
    "greeting_sha3_384",
    "greeting_sha3_512",
    "greeting_sha224",
    "greeting_sha256",
    "greeting_sha384",
    "greeting_sha512",
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_html_escaped` escapes the complete greeting (not the name alone), "
    "including the `Hello, ` prefix, with `html.escape` and its default "
    "`quote=True`, so `&`, `<`, `>`, `\"`, and `'` become `&amp;`, `&lt;`, `&gt;`, "
    "`&quot;`, and `&#x27;` while every other character, including non-ASCII, is "
    "unchanged; it inherits `greet`'s `ValueError(\"name must not be blank\")` for "
    "empty, whitespace-only, and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_html_escaped)


@when("greeting_html_escaped is called with Ada and Zo plus U+00EB")
def escape_plain_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Zoë")
    context["results"] = [
        library.greeting_html_escaped(name) for name in context["names"]
    ]


@then("the results are the strings Hello, Ada and Hello, Zo plus U+00EB")
def plain_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert all(type(result) is str for result in results)
    assert results == ["Hello, Ada", "Hello, Zoë"]


@when(
    "greeting_html_escaped is called with names containing ampersand, angle "
    "brackets, apostrophe, and double quotes"
)
def escape_special_names(context: dict[str, object]) -> None:
    context["names"] = ("<Ada & Bo>", 'O\'Brien "Jr"')
    context["results"] = [
        library.greeting_html_escaped(name) for name in context["names"]
    ]


@then(
    "the results are Hello, &lt;Ada &amp; Bo&gt; and Hello, O&#x27;Brien &quot;Jr&quot;, "
    "each equal to html.escape of the greeting"
)
def special_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == [ADA_BO_ESCAPED, "Hello, O&#x27;Brien &quot;Jr&quot;"]
    assert results == [
        html.escape(library.greet(name)) for name in context["names"]
    ]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_html_escaped is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_html_escaped(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_html_escaped of <Ada & Bo>"
)
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_html_escaped("<Ada & Bo>"))\n',
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@then(
    "it prints Hello, &lt;Ada &amp; Bo&gt; and greeting_html_escaped is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_BO_ESCAPED + "\n",
        "",
    )
    assert "greeting_html_escaped" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the html.escape quote=True result, completed-greeting "
    "scope, and inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
