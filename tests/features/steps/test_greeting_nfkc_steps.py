import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import greeting_nfkc

scenarios("../add_greeting_nfkc_library_helper.feature")

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
    "greeting_last_word",
    "greeting_length",
    "greeting_letter_count",
    "greeting_longest_word",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_nfc",
    "greeting_nfd",
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
    "`greeting_nfkc` returns the complete greeting (not the name alone), including the "
    "`Hello, ` prefix, in Unicode Normalization Form KC using "
    '`unicodedata.normalize("NFKC", ...)`, so compatibility characters are replaced by '
    "their standard equivalents (for example `\N{LATIN SMALL LIGATURE FI}ona` gives "
    "`Hello, fiona`, full-width `\N{FULLWIDTH LATIN CAPITAL LETTER A}"
    "\N{FULLWIDTH LATIN SMALL LETTER D}\N{FULLWIDTH LATIN SMALL LETTER A}` gives "
    "`Hello, Ada`, and a no-break space becomes a regular space) and the result is "
    "canonically composed (for example `Chloe` plus U+0301 gives "
    "`Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}`); already-normalized text is "
    "unchanged, no case change, whitespace collapsing, or accent stripping is made, and "
    "it inherits `greet`'s `ValueError(\"name must not be blank\")` for empty, "
    "whitespace-only, and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_nfkc)


@when(
    "greeting_nfkc is called with U+FB01 ona, full-width Ada, and Ada no-break-space Lovelace"
)
def call_nfkc_compatibility_names(context: dict[str, object]) -> None:
    context["names"] = (
        "\N{LATIN SMALL LIGATURE FI}ona",
        (
            "\N{FULLWIDTH LATIN CAPITAL LETTER A}"
            "\N{FULLWIDTH LATIN SMALL LETTER D}"
            "\N{FULLWIDTH LATIN SMALL LETTER A}"
        ),
        "Ada\N{NO-BREAK SPACE}Lovelace",
    )
    context["results"] = [library.greeting_nfkc(name) for name in context["names"]]


@then(
    "the results are Hello, fiona with 12 code points, "
    "then Hello, Ada with 10 code points, then Hello, Ada Lovelace with 19 code points"
)
def compatibility_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == ["Hello, fiona", "Hello, Ada", "Hello, Ada Lovelace"]
    assert [len(result) for result in results] == [12, 10, 19]


@then("each result is a str")
def results_are_str(context: dict[str, object]) -> None:
    assert all(type(result) is str for result in context["results"])


@when("greeting_nfkc is called with Chloe plus U+0301")
def call_nfkc_decomposed_name(context: dict[str, object]) -> None:
    context["name"] = "Chloe\N{COMBINING ACUTE ACCENT}"
    context["result"] = library.greeting_nfkc(context["name"])


@then(
    "the result is Hello, precomposed Chlo\N{LATIN SMALL LETTER E WITH ACUTE} "
    "with 12 code points"
)
def composed_result(context: dict[str, object]) -> None:
    result = context["result"]
    assert result == "Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"
    assert len(result) == 12


@when("greeting_nfkc is called with Ada, Ada two-spaces Lovelace, and O'Brien-Smith")
def call_nfkc_unchanged_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada  Lovelace", "O'Brien-Smith")
    context["results"] = [library.greeting_nfkc(name) for name in context["names"]]


@then("each result equals greet of the same name")
def results_equal_greet(context: dict[str, object]) -> None:
    assert context["results"] == [library.greet(name) for name in context["names"]]


@when(
    "greeting_nfkc is called with Ada, Chloe plus U+0301, U+FB01 ona, and O'Brien-Smith"
)
def call_nfkc_agreement(context: dict[str, object]) -> None:
    context["names"] = (
        "Ada",
        "Chloe\N{COMBINING ACUTE ACCENT}",
        "\N{LATIN SMALL LIGATURE FI}ona",
        "O'Brien-Smith",
    )
    context["results"] = [library.greeting_nfkc(name) for name in context["names"]]


@then("each result equals unicodedata NFKC normalization of greet of the same name")
def results_match_unicodedata(context: dict[str, object]) -> None:
    assert context["results"] == [
        unicodedata.normalize("NFKC", library.greet(name)) for name in context["names"]
    ]


@then("each result is NFKC-normalized")
def results_are_nfkc(context: dict[str, object]) -> None:
    assert all(
        unicodedata.is_normalized("NFKC", result) for result in context["results"]
    )


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_nfkc is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_nfkc(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_nfkc of U+FB01 ona"
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
            example + 'print(greeting_nfkc("\\N{LATIN SMALL LIGATURE FI}ona"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints Hello, fiona and greeting_nfkc is listed in nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "Hello, fiona\n",
        "",
    )
    assert callable(greeting_nfkc)
    assert "greeting_nfkc" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("the README documents the NFKC rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
