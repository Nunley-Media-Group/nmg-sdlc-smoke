import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import cli

scenarios("../add_greeting_char_frequency_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_FREQUENCY = {
    "H": 1,
    "e": 1,
    "l": 2,
    "o": 1,
    ",": 1,
    " ": 1,
    "A": 1,
    "d": 1,
    "a": 1,
}
ADA_LOVELACE_FREQUENCY = {
    "H": 1,
    "e": 3,
    "l": 3,
    "o": 2,
    ",": 1,
    " ": 2,
    "A": 1,
    "d": 1,
    "a": 2,
    "L": 1,
    "v": 1,
    "c": 1,
}
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
    "`greeting_char_frequency` returns a new plain `dict[str, int]` mapping "
    "each character (Unicode code point) of the complete greeting (not the "
    "name alone), including the `Hello, ` prefix, comma, and spaces, to the "
    "number of times it occurs; keys are case-sensitive and appear in the "
    "order each character first occurs (for example `Ada` gives "
    '`{"H": 1, "e": 1, "l": 2, "o": 1, ",": 1, " ": 1, "A": 1, "d": 1, '
    '"a": 1}`), no Unicode normalization is applied, and it inherits '
    "`greet`'s `ValueError(\"name must not be blank\")` for empty, "
    "whitespace-only, and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


def frequency_all(context: dict[str, object], names: tuple[str, ...]) -> None:
    context["names"] = names
    context["results"] = [library.greeting_char_frequency(name) for name in names]


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_char_frequency)


@when("greeting_char_frequency is called with Ada and Ada Lovelace")
def call_frequency_for_word_names(context: dict[str, object]) -> None:
    frequency_all(context, ("Ada", "Ada Lovelace"))


@then(
    "the results are the exact first-seen-order counts for Hello, Ada and "
    "Hello, Ada Lovelace"
)
def results_are_ordered_counts(context: dict[str, object]) -> None:
    ada, ada_lovelace = context["results"]
    assert ada == ADA_FREQUENCY
    assert list(ada) == list(ADA_FREQUENCY)
    assert ada_lovelace == ADA_LOVELACE_FREQUENCY
    assert list(ada_lovelace) == list(ADA_LOVELACE_FREQUENCY)


@then("each result is a plain dict")
def results_are_plain_dicts(context: dict[str, object]) -> None:
    assert all(type(result) is dict for result in context["results"])


@when(
    "greeting_char_frequency is called with Zo plus U+00EB and Zoe plus U+0308"
)
def call_frequency_for_non_ascii_names(context: dict[str, object]) -> None:
    frequency_all(context, ("Zo\u00eb", "Zoe\u0308"))


@then("the precomposed result counts U+00EB once and e once")
def precomposed_counts(context: dict[str, object]) -> None:
    precomposed = context["results"][0]
    assert precomposed["\u00eb"] == 1
    assert precomposed["e"] == 1


@then("the decomposed result counts e twice and U+0308 once with no U+00EB key")
def decomposed_counts(context: dict[str, object]) -> None:
    decomposed = context["results"][1]
    assert decomposed["e"] == 2
    assert decomposed["\u0308"] == 1
    assert "\u00eb" not in decomposed


@then("both results count H once with no h key")
def case_sensitive_counts(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert result["H"] == 1
        assert "h" not in result


@when(
    "greeting_char_frequency is called with Ada, Ada Lovelace, Agent 007, "
    "O'Brien, Zo plus U+00EB, and Ada plus U+674E plus Lee"
)
def call_frequency_for_consistency_names(context: dict[str, object]) -> None:
    frequency_all(
        context,
        ("Ada", "Ada Lovelace", "Agent 007", "O'Brien", "Zo\u00eb", "Ada\u674eLee"),
    )


@then("each result's counts sum to greeting_length of the same name")
def counts_sum_to_length(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert sum(result.values()) == library.greeting_length(name)


@then("each result has as many keys as greeting_unique_char_count of the same name")
def keys_match_unique_count(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert len(result) == library.greeting_unique_char_count(name)


@then("every count is a positive int")
def counts_are_positive_ints(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert all(type(count) is int and count > 0 for count in result.values())


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_char_frequency is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_char_frequency(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_char_frequency of Ada"
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
            example + 'print(greeting_char_frequency("Ada"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints the Ada counts and greeting_char_frequency is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        repr(ADA_FREQUENCY) + "\n",
        "",
    )
    assert "greeting_char_frequency" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the counting rule and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada\n"
