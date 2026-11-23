import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import greeting_nfd

scenarios("../add_greeting_nfd_library_helper.feature")

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
    "`greeting_nfd` returns the complete greeting (not the name alone), including the "
    "`Hello, ` prefix, in Unicode Normalization Form D using "
    '`unicodedata.normalize("NFD", ...)`, so a precomposed character is decomposed into '
    "its base character followed by combining marks (for example "
    "`Chlo\N{LATIN SMALL LETTER E WITH ACUTE}` gives `Hello, Chloe` plus U+0301, "
    "13 code points) and text with no decomposable characters is unchanged; only "
    "canonical decomposition is applied, so compatibility characters such as "
    "`\N{LATIN SMALL LIGATURE FI}` are kept and no case, whitespace, or accent stripping "
    "change is made, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and non-string '
    "names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_nfd)


@when(
    "greeting_nfd is called with precomposed Chlo\N{LATIN SMALL LETTER E WITH ACUTE} "
    "and precomposed \N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr"
    "\N{LATIN SMALL LETTER O WITH DIAERESIS}m"
)
def call_nfd_composed_names(context: dict[str, object]) -> None:
    context["names"] = (
        "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}",
        (
            "\N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr"
            "\N{LATIN SMALL LETTER O WITH DIAERESIS}m"
        ),
    )
    context["results"] = [library.greeting_nfd(name) for name in context["names"]]


@then(
    "the results are Hello, Chloe plus U+0301 with 13 code points, "
    "then Hello, A plus U+030A ngstro plus U+0308 m with 17 code points"
)
def decomposed_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == [
        "Hello, Chloe\N{COMBINING ACUTE ACCENT}",
        "Hello, A\N{COMBINING RING ABOVE}ngstro\N{COMBINING DIAERESIS}m",
    ]
    assert [len(result) for result in results] == [13, 17]


@then("each result is a str")
def results_are_str(context: dict[str, object]) -> None:
    assert all(type(result) is str for result in context["results"])


@when("greeting_nfd is called with Ada, Ada Lovelace, and Chloe plus U+0301")
def call_nfd_unchanged_names(context: dict[str, object]) -> None:
    context["names"] = (
        "Ada",
        "Ada Lovelace",
        "Chloe\N{COMBINING ACUTE ACCENT}",
    )
    context["results"] = [library.greeting_nfd(name) for name in context["names"]]


@then("each result equals greet of the same name")
def results_equal_greet(context: dict[str, object]) -> None:
    assert context["results"] == [library.greet(name) for name in context["names"]]


@when("greeting_nfd is called with U+FB01 ona and Ada two-spaces Lovelace")
def call_nfd_compatibility(context: dict[str, object]) -> None:
    context["names"] = ("\N{LATIN SMALL LIGATURE FI}ona", "Ada  Lovelace")
    context["results"] = [library.greeting_nfd(name) for name in context["names"]]


@then(
    "the results are Hello, U+FB01 ona with 11 code points, "
    "then Hello, Ada two-spaces Lovelace"
)
def compatibility_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == ["Hello, \N{LATIN SMALL LIGATURE FI}ona", "Hello, Ada  Lovelace"]
    assert len(results[0]) == 11


@when(
    "greeting_nfd is called with Ada, precomposed "
    "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}, U+FB01 ona, and O'Brien-Smith"
)
def call_nfd_agreement(context: dict[str, object]) -> None:
    context["names"] = (
        "Ada",
        "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}",
        "\N{LATIN SMALL LIGATURE FI}ona",
        "O'Brien-Smith",
    )
    context["results"] = [library.greeting_nfd(name) for name in context["names"]]


@then("each result equals unicodedata NFD normalization of greet of the same name")
def results_match_unicodedata(context: dict[str, object]) -> None:
    assert context["results"] == [
        unicodedata.normalize("NFD", library.greet(name)) for name in context["names"]
    ]


@then("each result is NFD-normalized")
def results_are_nfd(context: dict[str, object]) -> None:
    assert all(unicodedata.is_normalized("NFD", result) for result in context["results"])


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_nfd is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_nfd(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints the length of greeting_nfd of precomposed "
    "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"
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
            example + 'print(len(greeting_nfd("Chlo\\u00e9")))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then("it prints 13 and greeting_nfd is listed in nmg_sdlc_smoke.__all__")
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "13\n", "")
    assert callable(greeting_nfd)
    assert "greeting_nfd" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("the README documents the NFD rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
