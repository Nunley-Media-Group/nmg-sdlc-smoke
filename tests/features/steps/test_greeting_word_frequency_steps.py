import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import greeting_word_frequency

scenarios("../add_greeting_word_frequency_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA = {"Hello,": 1, "Ada": 1}
ADA_LOVELACE = {"Hello,": 1, "Ada": 1, "Lovelace": 1}
BO_BO = {"Hello,": 1, "Bo": 2}
BO_AL = {"Hello,": 1, "Bo": 2, "Al": 1}
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
    "greeting_last_word",
    "greeting_length",
    "greeting_letter_count",
    "greeting_longest_word",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_nfc",
    "greeting_nfd",
    "greeting_nfkc",
    "greeting_nfkd",
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
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_utf16_length",
    "greeting_vowel_count",
    "greeting_word_count",
    "greeting_word_lengths",
    "greeting_words",
)
PROSE = (
    "`greeting_word_frequency` returns a new plain `dict[str, int]` mapping "
    "each whitespace-separated word of the complete greeting (not the name "
    "alone) to the number of times it occurs, using the same `str.split()` "
    "words as `greeting_words`; keys are the words unchanged and "
    "case-sensitive, with punctuation attached and no Unicode normalization, "
    "and appear in the order each word first occurs (for example `Bo Bo` "
    'gives `{"Hello,": 1, "Bo": 2}`), so the values always sum to '
    "`greeting_word_count(name)`, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def frequency_all(context: dict[str, object], names: tuple[object, ...]) -> None:
    context["names"] = names
    context["results"] = [greeting_word_frequency(name) for name in names]


def assert_first_seen(results: list[object], expected: list[dict[str, int]]) -> None:
    for result, counts in zip(results, expected, strict=True):
        assert type(result) is dict
        assert result == counts
        assert list(result) == list(counts)


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(greeting_word_frequency)


@when("greeting_word_frequency is called with Ada, Ada Lovelace, and Bo Bo")
def call_frequency_for_word_counts(context: dict[str, object]) -> None:
    frequency_all(context, ("Ada", "Ada Lovelace", "Bo Bo"))


@then(
    "the results are Hello, 1 Ada 1, then Hello, 1 Ada 1 Lovelace 1, then "
    "Hello, 1 Bo 2"
)
def results_are_word_counts(context: dict[str, object]) -> None:
    assert context["results"] == [ADA, ADA_LOVELACE, BO_BO]


@then("each result is a dict with keys in first-seen order")
def results_have_first_seen_keys(context: dict[str, object]) -> None:
    assert_first_seen(context["results"], [ADA, ADA_LOVELACE, BO_BO])


@when(
    "greeting_word_frequency is called with Bo tab Bo, space Ada space, and "
    "Bo two-spaces Al newline Bo"
)
def call_frequency_for_whitespace_names(context: dict[str, object]) -> None:
    frequency_all(context, ("Bo\tBo", " Ada ", "Bo  Al\nBo"))


@then(
    "the results are Hello, 1 Bo 2, then Hello, 1 Ada 1, then Hello, 1 Bo 2 Al 1"
)
def results_split_on_whitespace(context: dict[str, object]) -> None:
    assert_first_seen(context["results"], [BO_BO, ADA, BO_AL])


@when(
    "greeting_word_frequency is called with Bo bo, Hello Hello comma, and "
    "Chloe plus U+0301 space Chlo plus U+00E9"
)
def call_frequency_for_exact_words(context: dict[str, object]) -> None:
    frequency_all(
        context,
        (
            "Bo bo",
            "Hello Hello,",
            "Chloe\N{COMBINING ACUTE ACCENT} Chlo\N{LATIN SMALL LETTER E WITH ACUTE}",
        ),
    )


@then(
    "the results are Hello, 1 Bo 1 bo 1, then Hello, 2 Hello 1, then Hello, 1 "
    "with each Chloe spelling counted separately"
)
def results_keep_words_exact(context: dict[str, object]) -> None:
    assert_first_seen(
        context["results"],
        [
            {"Hello,": 1, "Bo": 1, "bo": 1},
            {"Hello,": 2, "Hello": 1},
            {
                "Hello,": 1,
                "Chloe\N{COMBINING ACUTE ACCENT}": 1,
                "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}": 1,
            },
        ],
    )


@when(
    "greeting_word_frequency is called with Ada, Bo Bo, Bo two-spaces Al "
    "newline Bo, O'Brien-Smith, and Hello Hello comma"
)
def call_frequency_for_agreement_names(context: dict[str, object]) -> None:
    frequency_all(
        context,
        ("Ada", "Bo Bo", "Bo  Al\nBo", "O'Brien-Smith", "Hello Hello,"),
    )


@then("each result's values sum to greeting_word_count of the same name")
def values_sum_to_word_count(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert sum(result.values()) == library.greeting_word_count(name)


@then(
    "each result's keys equal greeting_words of the same name with later "
    "duplicates removed"
)
def keys_match_word_list(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert list(result) == list(dict.fromkeys(library.greeting_words(name)))


@when(
    "greeting_word_frequency is called twice with Ada and the first result is "
    "mutated"
)
def call_twice_and_mutate_first(context: dict[str, object]) -> None:
    first = greeting_word_frequency("Ada")
    first["Ada"] = 99
    first["x"] = 1
    context["first"] = first
    context["second"] = greeting_word_frequency("Ada")


@then("the second result is Hello, 1 Ada 1 and is a different object")
def second_result_is_fresh(context: dict[str, object]) -> None:
    assert context["second"] == ADA
    assert context["second"] is not context["first"]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_word_frequency is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_word_frequency(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_word_frequency of Bo Bo"
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
            example + 'print(greeting_word_frequency("Bo Bo"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints the Hello, 1 Bo 2 dict and greeting_word_frequency is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "{'Hello,': 1, 'Bo': 2}\n",
        "",
    )
    assert "greeting_word_frequency" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the word-frequency rule and the inherited "
    "invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
