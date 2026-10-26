import hashlib
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library
from nmg_sdlc_smoke.cli import main

scenarios("../add_greeting_blake2b_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_DIGEST = "dacd0313406557f10115a4268fb435f4452c16872be1455fdf41b27fdcd3d1e6dba61210d8b48f846b7c23c68527c53c13bb10e794168d286a376d63513939d4"
ADA_LOVELACE_DIGEST = "ebd70a8d05430c07e7297ed2b628032e0b795e0c0992d231b3c266f8c84f4b2c90c85ef5ef66c4ce46f821abd5cc39e356339406f1a760e13577e051a30b0e28"
ZOE_DIGEST = "b49235eea9e9b2d59d50adee4a2c9c3a47b147d9667afa992d01399bbe083c6e82273588ae669168438369b25238627d10cd0b1511bb5a4735af1780afd55264"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_adler32",
    "greeting_base32",
    "greeting_base64",
    "greeting_bytes",
    "greeting_casefold",
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
    "greeting_is_ascii",
    "greeting_length",
    "greeting_letter_count",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_punctuation_count",
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
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_blake2b` encodes the complete greeting (not the name alone), including "
    "the `Hello, ` prefix, as UTF-8 and returns its BLAKE2b digest from "
    "`hashlib.blake2b` with default parameters (64-byte digest, no key, salt, or "
    "personalization) as 128 lowercase hexadecimal characters; no Unicode "
    "normalization is applied, so precomposed and decomposed spellings of a name "
    "produce different digests, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_blake2b)


@when("greeting_blake2b is called with Ada and Ada Lovelace")
def digests_ada_names(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_blake2b(name) for name in ("Ada", "Ada Lovelace")
    ]


@then(
    "the results are the 128-character hex strings "
    "dacd0313406557f10115a4268fb435f4452c16872be1455fdf41b27fdcd3d1e6dba61210d8b48f846b7c23c68527c53c13bb10e794168d286a376d63513939d4 and "
    "ebd70a8d05430c07e7297ed2b628032e0b795e0c0992d231b3c266f8c84f4b2c90c85ef5ef66c4ce46f821abd5cc39e356339406f1a760e13577e051a30b0e28"
)
def ada_names_digests(context: dict[str, object]) -> None:
    results = context["results"]
    assert all(type(result) is str and len(result) == 128 for result in results)
    assert results == [ADA_DIGEST, ADA_LOVELACE_DIGEST]


@when("greeting_blake2b is called with Zo plus U+00EB")
def digest_zoe(context: dict[str, object]) -> None:
    context["result"] = library.greeting_blake2b("Zoë")


@then(
    "the result is "
    "b49235eea9e9b2d59d50adee4a2c9c3a47b147d9667afa992d01399bbe083c6e82273588ae669168438369b25238627d10cd0b1511bb5a4735af1780afd55264, "
    "the hashlib BLAKE2b hex digest of the UTF-8 encoded greeting"
)
def zoe_digest(context: dict[str, object]) -> None:
    result = context["result"]
    assert type(result) is str
    assert result == ZOE_DIGEST
    greeting = "Hello, Zoë"
    assert result == hashlib.blake2b(greeting.encode("utf-8")).hexdigest()


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_blake2b is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_blake2b(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_blake2b of Ada")
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_blake2b("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = StringIO()
    with redirect_stdout(stdout):
        status = main(["Ada"])
    context["cli"] = (status, stdout.getvalue())


@then(
    "it prints the Ada BLAKE2b digest and greeting_blake2b is listed in "
    "nmg_sdlc_smoke.__all__"
)
def example_output_and_exports(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_DIGEST + "\n",
        "",
    )
    assert "greeting_blake2b" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the lowercase hex UTF-8 default-parameter BLAKE2b result, "
    "completed-greeting scope, and inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    assert context["cli"] == (0, "Hello, Ada\n")
