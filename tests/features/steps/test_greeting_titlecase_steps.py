import os
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke import greeting_titlecase

scenarios("../add_greeting_titlecase_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
SCRIPTS = Path(sysconfig.get_path("scripts"))
NMG_SMOKE = SCRIPTS / "nmg-smoke"
if not NMG_SMOKE.exists():
    NMG_SMOKE = SCRIPTS / "nmg-smoke.exe"
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
    "`greeting_titlecase` returns `str.title()` of the complete greeting (not the name "
    "alone), including the `Hello, ` prefix, so each run of letters starts with an "
    "uppercase character followed by lowercase characters, and a letter after a digit "
    "or apostrophe also starts a new run (for example `ada lovelace` gives "
    "`Hello, Ada Lovelace` and `o'brien` gives `Hello, O'Brien`); it matches "
    "`nmg-smoke --titlecase` output without the trailing newline, applies no Unicode "
    "normalization, and inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and non-string '
    "names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(greeting_titlecase)


@when("greeting_titlecase is called with ada, ADA LOVELACE, and ada lovelace")
def call_titlecase_names(context: dict[str, object]) -> None:
    context["names"] = ("ada", "ADA LOVELACE", "ada lovelace")
    context["results"] = [greeting_titlecase(name) for name in context["names"]]


@then(
    "the results are Hello, Ada, then Hello, Ada Lovelace, then Hello, Ada Lovelace"
)
def titlecase_results(context: dict[str, object]) -> None:
    assert context["results"] == ["Hello, Ada", "Hello, Ada Lovelace", "Hello, Ada Lovelace"]


@then("each result is a str")
def results_are_str(context: dict[str, object]) -> None:
    assert all(type(result) is str for result in context["results"])


@when(
    "greeting_titlecase is called with o'brien, agent 007x, "
    "and \N{LATIN SMALL LETTER A WITH RING ABOVE}sa"
)
def call_titlecase_punctuation(context: dict[str, object]) -> None:
    context["names"] = ("o'brien", "agent 007x", "\N{LATIN SMALL LETTER A WITH RING ABOVE}sa")
    context["results"] = [greeting_titlecase(name) for name in context["names"]]


@then(
    "the results are Hello, O'Brien, then Hello, Agent 007X, "
    "then Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}sa"
)
def titlecase_punctuation_results(context: dict[str, object]) -> None:
    assert context["results"] == [
        "Hello, O'Brien",
        "Hello, Agent 007X",
        "Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}sa",
    ]


@when("greeting_titlecase is called with ada, ADA LOVELACE, o'brien, and Ada tab Lovelace")
def call_titlecase_agreement(context: dict[str, object]) -> None:
    context["names"] = ("ada", "ADA LOVELACE", "o'brien", "Ada\tLovelace")
    context["results"] = [greeting_titlecase(name) for name in context["names"]]


@then("each result equals str.title() of greet of the same name")
def results_equal_greet_title(context: dict[str, object]) -> None:
    assert context["results"] == [
        library.greet(name).title() for name in context["names"]
    ]


@then(
    "nmg-smoke --titlecase ada prints the greeting_titlecase result "
    "for ada followed by one newline"
)
def cli_titlecase_stdout(context: dict[str, object]) -> None:
    run = subprocess.run(
        [str(NMG_SMOKE), "--titlecase", "ada"],
        check=False,
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert (run.returncode, run.stdout, run.stderr) == (
        0,
        greeting_titlecase("ada") + "\n",
        "",
    )


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_titlecase is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_titlecase(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def invalid_name_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_titlecase of ada lovelace")
def run_readme_example(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    context["run"] = subprocess.run(
        [
            sys.executable,
            "-c",
            example + 'print(greeting_titlecase("ada lovelace"))\n',
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


@then(
    "it prints Hello, Ada Lovelace and greeting_titlecase is listed in nmg_sdlc_smoke.__all__"
)
def example_output_and_export(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        "Hello, Ada Lovelace\n",
        "",
    )
    assert callable(greeting_titlecase)
    assert "greeting_titlecase" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("the README documents the str.title() rule and the inherited invalid-name error")
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
