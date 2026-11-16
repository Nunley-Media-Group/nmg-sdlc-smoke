import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_words_library_helper.feature")

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
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_swapcase",
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_words` returns a new `list[str]` of the whitespace-separated words "
    "of the complete greeting (not the name alone), using Python's `str.split()` "
    "semantics so runs of any whitespace separate words and punctuation stays "
    "attached (for example `Ada` gives `['Hello,', 'Ada']`); its length always "
    "equals `greeting_word_count`, and it inherits `greet`'s "
    "`ValueError(\"name must not be blank\")` for empty, whitespace-only, and "
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_words)


@when("greeting_words is called with Ada and Zo plus U+00EB")
def call_words_for_single_word_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Zoë")
    context["results"] = [library.greeting_words(name) for name in context["names"]]


@then("the results are Hello, Ada and Hello, Zo plus U+00EB as word lists")
def results_are_word_lists(context: dict[str, object]) -> None:
    results = context["results"]
    assert all(type(result) is list for result in results)
    assert all(type(word) is str for result in results for word in result)
    assert results == [["Hello,", "Ada"], ["Hello,", "Zoë"]]


@then("each result equals the split of the greeting")
def results_match_split(context: dict[str, object]) -> None:
    assert context["results"] == [
        library.greet(name).split() for name in context["names"]
    ]


@when("greeting_words is called with Ada Lovelace and Ada space-tab-space Lovelace")
def call_words_for_multi_word_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada Lovelace", "Ada \t Lovelace")
    context["results"] = [library.greeting_words(name) for name in context["names"]]


@then("both results are the words Hello, Ada, and Lovelace")
def results_are_split_words(context: dict[str, object]) -> None:
    assert context["results"] == [["Hello,", "Ada", "Lovelace"]] * 2


@then("each result length equals greeting_word_count of the same name")
def result_lengths_match_word_count(context: dict[str, object]) -> None:
    assert [len(result) for result in context["results"]] == [
        library.greeting_word_count(name) for name in context["names"]
    ]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_words is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_words(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_words of Ada")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_words("Ada"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints the list Hello, and Ada and greeting_words is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "['Hello,', 'Ada']\n",
        "",
    )
    assert "greeting_words" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the word list of the complete greeting and the "
    "inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
