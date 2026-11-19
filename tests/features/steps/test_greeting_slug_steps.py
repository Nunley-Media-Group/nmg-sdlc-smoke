import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_slug_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
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
    "greeting_codepoints",
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
    "greeting_html_escaped",
    "greeting_initials",
    "greeting_is_ascii",
    "greeting_is_printable",
    "greeting_is_title",
    "greeting_length",
    "greeting_letter_count",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_punctuation_count",
    "greeting_quoted_printable",
    "greeting_reversed",
    "greeting_rot13",
    "greeting_sha1",
    "greeting_sha224",
    "greeting_sha256",
    "greeting_sha384",
    "greeting_sha3_224",
    "greeting_sha3_256",
    "greeting_sha3_384",
    "greeting_sha3_512",
    "greeting_sha512",
    "greeting_shake_128",
    "greeting_shake_256",
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_swapcase",
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_utf16_length",
    "greeting_vowel_count",
    "greeting_word_count",
    "greeting_words",
)
PROSE = (
    "`greeting_slug` returns a lowercase ASCII slug of the complete greeting "
    "(not the name alone): it applies Unicode NFKD normalization and drops "
    "combining marks (so `Zo\u00eb` gives `hello-zoe`), lowercases, replaces "
    "every run of characters other than `a`\u2013`z` and `0`\u2013`9` with a "
    "single `-`, and trims leading and trailing `-` (for example `Ada "
    "Lovelace` gives `hello-ada-lovelace`); characters with no ASCII base, "
    "such as `\u674e`, act as separators, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, '
    "and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def slug_all(context: dict[str, object], names: tuple[str, ...]) -> None:
    context["results"] = [library.greeting_slug(name) for name in names]


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_slug)


@when(
    "greeting_slug is called with Ada, Ada Lovelace, Ada space-tab-space "
    "Lovelace, and Agent 007"
)
def call_slug_for_word_names(context: dict[str, object]) -> None:
    slug_all(context, ("Ada", "Ada Lovelace", "Ada \t Lovelace", "Agent 007"))


@then(
    "the results are the strings hello-ada, hello-ada-lovelace, "
    "hello-ada-lovelace, and hello-agent-007"
)
def results_are_word_slugs(context: dict[str, object]) -> None:
    results = context["results"]
    assert all(type(result) is str for result in results)
    assert results == [
        "hello-ada",
        "hello-ada-lovelace",
        "hello-ada-lovelace",
        "hello-agent-007",
    ]


@when("greeting_slug is called with O'Brien, Ada!!, --Ada--, and Ada_Lovelace")
def call_slug_for_punctuated_names(context: dict[str, object]) -> None:
    slug_all(context, ("O'Brien", "Ada!!", "--Ada--", "Ada_Lovelace"))


@then(
    "the results are hello-o-brien, hello-ada, hello-ada, and hello-ada-lovelace"
)
def results_are_punctuation_slugs(context: dict[str, object]) -> None:
    assert context["results"] == [
        "hello-o-brien",
        "hello-ada",
        "hello-ada",
        "hello-ada-lovelace",
    ]


@then("no result contains a double hyphen or starts or ends with a hyphen")
def results_have_clean_separators(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert "--" not in result
        assert not result.startswith("-")
        assert not result.endswith("-")


@when(
    "greeting_slug is called with Zo plus U+00EB, U+00C9 plus MILE, U+FF21 "
    "plus da, and Ada plus U+674E plus Lee"
)
def call_slug_for_non_ascii_names(context: dict[str, object]) -> None:
    slug_all(context, ("Zo\u00eb", "\u00c9MILE", "\uff21da", "Ada\u674eLee"))


@then("the results are hello-zoe, hello-emile, hello-ada, and hello-ada-lee")
def results_are_transliterated_slugs(context: dict[str, object]) -> None:
    assert context["results"] == [
        "hello-zoe",
        "hello-emile",
        "hello-ada",
        "hello-ada-lee",
    ]


@then("every result is lowercase ASCII words joined by single hyphens")
def results_match_slug_pattern(context: dict[str, object]) -> None:
    assert all(SLUG_PATTERN.fullmatch(result) for result in context["results"])


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_slug is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_slug(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_slug of Ada Lovelace"
)
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_slug("Ada Lovelace"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints hello-ada-lovelace and greeting_slug is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "hello-ada-lovelace\n",
        "",
    )
    assert "greeting_slug" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the slug rule and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
