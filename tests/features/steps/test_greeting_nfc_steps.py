import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_nfc_library_helper.feature")

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
    "`greeting_nfc` returns the complete greeting (not the name alone), including the "
    "`Hello, ` prefix, in Unicode Normalization Form C using "
    '`unicodedata.normalize("NFC", ...)`, so a base character followed by combining '
    "marks is composed into its precomposed form where one exists (for example "
    "`Chloe` plus U+0301 gives `Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}`) and "
    "already-composed text is unchanged; only canonical composition is applied, so "
    "compatibility characters such as `\N{LATIN SMALL LIGATURE FI}` are kept and no "
    "case, whitespace, or accent stripping change is made, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and non-string '
    "names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_nfc)


@when(
    "greeting_nfc is called with Chloe plus U+0301 and A plus U+030A ngstro plus U+0308 m"
)
def call_nfc_composition(context: dict[str, object]) -> None:
    context["names"] = (
        "Chloe\N{COMBINING ACUTE ACCENT}",
        "A\N{COMBINING RING ABOVE}ngstro\N{COMBINING DIAERESIS}m",
    )
    context["results"] = [library.greeting_nfc(name) for name in context["names"]]


@then(
    "the results are Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE} with 12 code points, "
    "then Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr"
    "\N{LATIN SMALL LETTER O WITH DIAERESIS}m with 15 code points"
)
def composed_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == [
        "Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}",
        (
            "Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr"
            "\N{LATIN SMALL LETTER O WITH DIAERESIS}m"
        ),
    ]
    assert [len(result) for result in results] == [12, 15]


@then("each result is a str")
def results_are_str(context: dict[str, object]) -> None:
    assert all(type(result) is str for result in context["results"])


@when(
    "greeting_nfc is called with Ada, Ada Lovelace, and precomposed "
    "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"
)
def call_nfc_composed_names(context: dict[str, object]) -> None:
    context["names"] = (
        "Ada",
        "Ada Lovelace",
        "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}",
    )
    context["results"] = [library.greeting_nfc(name) for name in context["names"]]


@then("each result equals greet of the same name")
def results_equal_greet(context: dict[str, object]) -> None:
    assert context["results"] == [library.greet(name) for name in context["names"]]


@when("greeting_nfc is called with U+FB01 ona and Ada two-spaces Lovelace")
def call_nfc_compatibility(context: dict[str, object]) -> None:
    context["names"] = ("\N{LATIN SMALL LIGATURE FI}ona", "Ada  Lovelace")
    context["results"] = [library.greeting_nfc(name) for name in context["names"]]


@then(
    "the results are Hello, U+FB01 ona with 11 code points, "
    "then Hello, Ada two-spaces Lovelace"
)
def compatibility_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert results == ["Hello, \N{LATIN SMALL LIGATURE FI}ona", "Hello, Ada  Lovelace"]
    assert len(results[0]) == 11


@when(
    "greeting_nfc is called with Ada, Chloe plus U+0301, U+FB01 ona, and O'Brien-Smith"
)
def call_nfc_agreement(context: dict[str, object]) -> None:
    context["names"] = (
        "Ada",
        "Chloe\N{COMBINING ACUTE ACCENT}",
        "\N{LATIN SMALL LIGATURE FI}ona",
        "O'Brien-Smith",
    )
    context["results"] = [library.greeting_nfc(name) for name in context["names"]]


@then("each result equals unicodedata NFC normalization of greet of the same name")
def results_match_unicodedata(context: dict[str, object]) -> None:
    assert context["results"] == [
        unicodedata.normalize("NFC", library.greet(name)) for name in context["names"]
    ]


@then("each result is NFC-normalized")
def results_are_nfc(context: dict[str, object]) -> None:
    assert all(unicodedata.is_normalized("NFC", result) for result in context["results"])


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_nfc is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_nfc(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_nfc of Chloe plus U+0301")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_nfc("Chloe\\u0301"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE} and "
    "greeting_nfc is listed in nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}\n",
        "",
    )
    assert "greeting_nfc" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("the README documents the NFC rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
