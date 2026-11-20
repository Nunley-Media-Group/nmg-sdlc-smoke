import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_word_lengths_library_helper.feature")

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
    "greeting_words",
)
PROSE = (
    "`greeting_word_lengths` returns a new `list[int]` with the length in "
    "Unicode code points of each whitespace-separated word of the complete "
    "greeting (not the name alone), in order, using the same `str.split()` "
    "words as `greeting_words` so runs of any whitespace separate words, no "
    "empty words appear, and punctuation stays attached (for example `Ada` "
    "gives `[6, 3]`); no Unicode normalization is applied, its length always "
    "equals `greeting_word_count`, and it inherits `greet`'s "
    "`ValueError(\"name must not be blank\")` for empty, whitespace-only, and "
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def lengths_all(context: dict[str, object], names: tuple[str, ...]) -> None:
    context["names"] = names
    context["results"] = [library.greeting_word_lengths(name) for name in names]


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_word_lengths)


@when("greeting_word_lengths is called with Ada, Ada Lovelace, and Agent 007")
def call_lengths_for_word_names(context: dict[str, object]) -> None:
    lengths_all(context, ("Ada", "Ada Lovelace", "Agent 007"))


@then("the results are [6, 3], [6, 3, 8], and [6, 5, 3]")
def results_for_word_names(context: dict[str, object]) -> None:
    assert context["results"] == [[6, 3], [6, 3, 8], [6, 5, 3]]


@then("each result is a plain list of int")
def results_are_plain_int_lists(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert type(result) is list
        assert all(type(value) is int for value in result)


@when(
    "greeting_word_lengths is called with Ada tab Lee, space Ada space, and "
    "Ada two-spaces Lee"
)
def call_lengths_for_whitespace_names(context: dict[str, object]) -> None:
    lengths_all(context, ("Ada\tLee", " Ada ", "Ada  Lee"))


@then("the results are [6, 3, 3], [6, 3], and [6, 3, 3]")
def results_for_whitespace_names(context: dict[str, object]) -> None:
    assert context["results"] == [[6, 3, 3], [6, 3], [6, 3, 3]]


@then("no result contains 0")
def no_empty_words(context: dict[str, object]) -> None:
    assert all(0 not in result for result in context["results"])


@when(
    "greeting_word_lengths is called with Zo plus U+00EB, Zoe plus U+0308, and "
    "Ada plus U+1F600"
)
def call_lengths_for_non_ascii_names(context: dict[str, object]) -> None:
    lengths_all(context, ("Zo\u00eb", "Zoe\u0308", "Ada\U0001F600"))


@then("the results are [6, 3], [6, 4], and [6, 4]")
def results_for_non_ascii_names(context: dict[str, object]) -> None:
    assert context["results"] == [[6, 3], [6, 4], [6, 4]]


@when(
    "greeting_word_lengths is called with Ada, Ada Lovelace, Agent 007, "
    "O'Brien, Ada tab Lee, and Zoe plus U+0308"
)
def call_lengths_for_consistency_names(context: dict[str, object]) -> None:
    lengths_all(
        context,
        ("Ada", "Ada Lovelace", "Agent 007", "O'Brien", "Ada\tLee", "Zoe\u0308"),
    )


@then("each result equals the lengths of greeting_words of the same name")
def results_match_words(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert result == [len(word) for word in library.greeting_words(name)]


@then("each result has as many values as greeting_word_count of the same name")
def results_match_word_count(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert len(result) == library.greeting_word_count(name)


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_word_lengths is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_word_lengths(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_word_lengths of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_word_lengths("Ada"))\n'],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints [6, 3] and greeting_word_lengths is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "[6, 3]\n", "")
    assert "greeting_word_lengths" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the word-length rule and the inherited invalid-name "
    "error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
