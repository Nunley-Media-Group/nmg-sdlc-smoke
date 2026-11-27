import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import greet, greeting_alnum_count

scenarios("../add_greeting_alnum_count_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_adler32",
    "greeting_ascii85",
    "greeting_ascii_count",
    "greeting_average_word_length",
    "greeting_base32",
    "greeting_base64",
    "greeting_base85",
    "greeting_blake2b",
    "greeting_blake2s",
    "greeting_bytes",
    "greeting_capitalize",
    "greeting_casefold",
    "greeting_char_frequency",
    "greeting_codepoints",
    "greeting_crc32",
    "greeting_digit_count",
    "greeting_ends_with_exclamation",
    "greeting_ends_with_name",
    "greeting_first_word",
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
    "greeting_json",
    "greeting_last_word",
    "greeting_length",
    "greeting_letter_count",
    "greeting_longest_word",
    "greeting_lowercase",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_nfc",
    "greeting_nfd",
    "greeting_nfkc",
    "greeting_nfkd",
    "greeting_non_ascii_count",
    "greeting_punctuation_count",
    "greeting_quoted_printable",
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
    "greeting_shake_128",
    "greeting_shake_256",
    "greeting_shortest_word",
    "greeting_slug",
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_swapcase",
    "greeting_titlecase",
    "greeting_unique_char_count",
    "greeting_uppercase",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_utf16_length",
    "greeting_vowel_count",
    "greeting_word_count",
    "greeting_word_frequency",
    "greeting_word_lengths",
    "greeting_words",
)
PROSE = (
    "`greeting_alnum_count` counts the characters in the complete greeting (not the name alone) "
    "for which `str.isalnum()` is true, including the five letters of `Hello`, so `Ada` gives `8` "
    "and `R2-D2` gives `9`; non-ASCII letters such as `\N{LATIN SMALL LETTER E WITH DIAERESIS}` and "
    "Unicode digits such as U+0663 are counted, while spaces, punctuation, combining marks, and emoji "
    "are not, no Unicode normalization is applied, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.'
)
PLAIN_NAMES = (
    "Ada",
    "Zo\N{LATIN SMALL LETTER E WITH DIAERESIS}",
    "\N{CJK UNIFIED IDEOGRAPH-674E}\N{CJK UNIFIED IDEOGRAPH-96F7}",
    "R2-D2",
)
NORMALIZATION_NAMES = (
    "Zoe\N{COMBINING DIAERESIS}",
    "Ada \N{GRINNING FACE}",
    "Agent \N{ARABIC-INDIC DIGIT THREE}",
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(greeting_alnum_count)


@when("greeting_alnum_count is called with Ada, Zo U+00EB, U+674E U+96F7, and R2-D2")
def call_alnum_count_for_plain_names(context: dict[str, object]) -> None:
    context["results"] = [greeting_alnum_count(name) for name in PLAIN_NAMES]


@then("the results are 8, then 8, then 7, then 9")
def results_are_counts(context: dict[str, object]) -> None:
    assert context["results"] == [8, 8, 7, 9]


@then("each result is an int")
def results_are_int(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert type(result) is int


@when("greeting_alnum_count is called with Zoe U+0308, Ada space U+1F600, and Agent space U+0663")
def call_alnum_count_for_normalization(context: dict[str, object]) -> None:
    context["results"] = [
        greeting_alnum_count(name) for name in NORMALIZATION_NAMES
    ]


@then("the results are 8, then 8, then 11")
def results_are_eight_eight_eleven(context: dict[str, object]) -> None:
    assert context["results"] == [8, 8, 11]


@then("each result equals the number of isalnum code points in greet of the same name")
def results_match_isalnum_count() -> None:
    for name in PLAIN_NAMES + NORMALIZATION_NAMES:
        expected = sum(character.isalnum() for character in greet(name))
        assert greeting_alnum_count(name) == expected


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_alnum_count is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_alnum_count(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_alnum_count of R2-D2")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_alnum_count("R2-D2"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then("it prints 9 and greeting_alnum_count is listed in nmg_sdlc_smoke.__all__")
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "9\n", "")
    assert "greeting_alnum_count" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("the README documents the isalnum counting rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
