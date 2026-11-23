import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_average_word_length_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
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
    "greeting_char_frequency",
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
    "greeting_longest_word",
    "greeting_lowercase_count",
    "greeting_md5",
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
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_utf16_length",
    "greeting_vowel_count",
    "greeting_word_count",
    "greeting_word_lengths",
    "greeting_words",
)
PROSE = (
    "`greeting_average_word_length` returns the mean length of the "
    "whitespace-separated words of the complete greeting (not the name alone) "
    "as an unrounded `float`, using the same `str.split()` words as "
    "`greeting_words` with punctuation attached and length measured in Unicode "
    "code points with no normalization (for example `Ada` gives `4.5` and "
    "`Bertha` gives `6.0`), and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)
PRECOMPOSED = "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"
DECOMPOSED = "Chloe\N{COMBINING ACUTE ACCENT}"


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def average_all(context: dict[str, object], names: tuple[str, ...]) -> None:
    context["names"] = names
    context["results"] = [library.greeting_average_word_length(name) for name in names]


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_average_word_length)


@when("greeting_average_word_length is called with Ada, Ada Lovelace, and Agent 007")
def call_average_for_word_names(context: dict[str, object]) -> None:
    average_all(context, ("Ada", "Ada Lovelace", "Agent 007"))


@then("the results are 4.5, then 17 / 3, then 14 / 3")
def results_for_word_names(context: dict[str, object]) -> None:
    assert context["results"] == [4.5, 17 / 3, 14 / 3]


@then("each result is a float")
def results_are_float(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert type(result) is float


@when("greeting_average_word_length is called with Bertha")
def call_average_for_whole_mean(context: dict[str, object]) -> None:
    context["result"] = library.greeting_average_word_length("Bertha")


@then("the result is 6.0")
def result_for_whole_mean(context: dict[str, object]) -> None:
    assert context["result"] == 6.0


@then("the result is a float")
def result_is_float(context: dict[str, object]) -> None:
    assert type(context["result"]) is float


@when(
    "greeting_average_word_length is called with Ada tab Lovelace, space Ada "
    "space, and Bo two-spaces Al"
)
def call_average_for_whitespace_names(context: dict[str, object]) -> None:
    average_all(context, ("Ada\tLovelace", " Ada ", "Bo  Al"))


@then("the results are 17 / 3, then 4.5, then 10 / 3")
def results_for_whitespace_names(context: dict[str, object]) -> None:
    assert context["results"] == [17 / 3, 4.5, 10 / 3]


@when(
    "greeting_average_word_length is called with Chlo plus U+00E9, and Chloe plus "
    "U+0301"
)
def call_average_for_non_ascii_names(context: dict[str, object]) -> None:
    average_all(context, (PRECOMPOSED, DECOMPOSED))


@then("the results are 5.5 and 6.0")
def results_for_non_ascii_names(context: dict[str, object]) -> None:
    assert context["results"] == [5.5, 6.0]


@when(
    "greeting_average_word_length is called with Ada, Ada Lovelace, Agent 007, "
    "Bertha, Bo Al, O'Brien-Smith, and Chloe plus U+0301"
)
def call_average_for_consistency_names(context: dict[str, object]) -> None:
    average_all(
        context,
        (
            "Ada",
            "Ada Lovelace",
            "Agent 007",
            "Bertha",
            "Bo Al",
            "O'Brien-Smith",
            DECOMPOSED,
        ),
    )


@then(
    "each result equals the sum of greeting_word_lengths divided by the number of "
    "greeting_words of the same name"
)
def results_equal_word_length_mean(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        expected = sum(library.greeting_word_lengths(name)) / len(
            library.greeting_words(name)
        )
        assert result == expected


@then("each result lies between the shortest and longest word lengths of the same name")
def results_within_word_length_bounds(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        shortest = len(library.greeting_shortest_word(name))
        longest = len(library.greeting_longest_word(name))
        assert shortest <= result <= longest


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_average_word_length is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_average_word_length(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_average_word_length of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_average_word_length("Ada"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints 4.5 and greeting_average_word_length is listed in nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "4.5\n", "")
    assert "greeting_average_word_length" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the average-word-length rule and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
