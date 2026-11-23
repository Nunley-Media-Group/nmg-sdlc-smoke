import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke
from nmg_sdlc_smoke import greeting_last_word, greeting_words

scenarios("../add_greeting_last_word_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_adler32",
    "greeting_ascii85",
    "greeting_average_word_length",
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
    "`greeting_last_word` returns the last whitespace-separated word of the complete "
    "greeting (not the name alone) as a `str`, using the same `str.split()` words as "
    "`greeting_words` and returning that word unchanged with punctuation attached and "
    "no case change or Unicode normalization (for example `Ada` gives `Ada` and "
    "`Ada Lovelace` gives `Lovelace`), and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)
DECOMPOSED = "Chloe\N{COMBINING ACUTE ACCENT}"


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def last_word_all(context: dict[str, object], names: tuple[str, ...]) -> None:
    context["names"] = names
    context["results"] = [greeting_last_word(name) for name in names]


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(greeting_last_word)


@when("greeting_last_word is called with Ada, Ada Lovelace, and Agent 007")
def call_last_word_for_word_names(context: dict[str, object]) -> None:
    last_word_all(context, ("Ada", "Ada Lovelace", "Agent 007"))


@then("the results are Ada, then Lovelace, then 007")
def results_for_word_names(context: dict[str, object]) -> None:
    assert context["results"] == ["Ada", "Lovelace", "007"]


@then("each result is a str")
def results_are_str(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert type(result) is str


@when(
    "greeting_last_word is called with Ada tab Lovelace, space Ada space, and Bo "
    "two-spaces Al newline"
)
def call_last_word_for_whitespace_names(context: dict[str, object]) -> None:
    last_word_all(context, ("Ada\tLovelace", " Ada ", "Bo  Al\n"))


@then("the results are Lovelace, then Ada, then Al")
def results_for_whitespace_names(context: dict[str, object]) -> None:
    assert context["results"] == ["Lovelace", "Ada", "Al"]


@when("greeting_last_word is called with Ada!, O'Brien-Smith, and Chloe plus U+0301")
def call_last_word_for_unchanged_words(context: dict[str, object]) -> None:
    last_word_all(context, ("Ada!", "O'Brien-Smith", DECOMPOSED))


@then(
    "the results are Ada!, then O'Brien-Smith, then Chloe plus U+0301 with 6 code points"
)
def results_for_unchanged_words(context: dict[str, object]) -> None:
    assert context["results"] == ["Ada!", "O'Brien-Smith", DECOMPOSED]
    assert len(context["results"][2]) == 6


@when(
    "greeting_last_word is called with Ada, Ada Lovelace, Agent 007, Ada tab Lovelace, "
    "O'Brien-Smith, and Chloe plus U+0301"
)
def call_last_word_for_greeting_words_agreement(context: dict[str, object]) -> None:
    last_word_all(
        context,
        (
            "Ada",
            "Ada Lovelace",
            "Agent 007",
            "Ada\tLovelace",
            "O'Brien-Smith",
            DECOMPOSED,
        ),
    )


@then("each result equals the last element of greeting_words of the same name")
def results_equal_greeting_words_last(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert result == greeting_words(name)[-1]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_last_word is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_last_word(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_last_word of Ada Lovelace")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_last_word("Ada Lovelace"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then("it prints Lovelace and greeting_last_word is listed in nmg_sdlc_smoke.__all__")
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Lovelace\n", "")
    assert "greeting_last_word" in nmg_sdlc_smoke.__all__
    assert set(PRIOR_EXPORTS) <= set(nmg_sdlc_smoke.__all__)


@then("the README documents the last-word rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
