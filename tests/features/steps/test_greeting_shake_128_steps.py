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

scenarios("../add_greeting_shake_128_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_DIGEST = "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774"
ZOE_DIGEST = "8479a68098ec2f7e622cd2c40a917d3a8b79221a308ebde33c5825dc6f0b4b3f"
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
    "greeting_length",
    "greeting_letter_count",
    "greeting_lowercase_count",
    "greeting_md5",
    "greeting_punctuation_count",
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
    "greeting_space_count",
    "greeting_starts_with_hello",
    "greeting_unique_char_count",
    "greeting_uppercase_count",
    "greeting_url_encoded",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_shake_128` encodes the complete greeting (not the name alone), "
    "including the `Hello, ` prefix, as UTF-8 and returns its SHAKE-128 output "
    "from `hashlib.shake_128` with a fixed 32-byte length as 64 lowercase "
    "hexadecimal characters; no Unicode normalization is applied, so precomposed "
    "and decomposed spellings of a name produce different digests, and it inherits "
    "`greet`'s `ValueError(\"name must not be blank\")` for empty, whitespace-only, "
    "and non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_shake_128)


@when("greeting_shake_128 is called with Ada and Zo plus U+00EB")
def digests_ada_and_zoe(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Zoë")
    context["results"] = [
        library.greeting_shake_128(name) for name in context["names"]
    ]


@then(
    "the results are "
    "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774 and "
    "8479a68098ec2f7e622cd2c40a917d3a8b79221a308ebde33c5825dc6f0b4b3f"
)
def expected_digests(context: dict[str, object]) -> None:
    assert context["results"] == [ADA_DIGEST, ZOE_DIGEST]


@then(
    "each result is 64 lowercase hexadecimal characters equal to the 32-byte "
    "SHAKE-128 hex digest of the UTF-8 greeting"
)
def digest_shape(context: dict[str, object]) -> None:
    for name, result in zip(context["names"], context["results"], strict=True):
        assert type(result) is str
        assert len(result) == 64
        assert set(result) <= set("0123456789abcdef")
        assert result == hashlib.shake_128(
            library.greet(name).encode("utf-8")
        ).hexdigest(32)


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t", None, 42)


@when("greeting_shake_128 is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["invalid_names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_shake_128(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when("the README Library example runs and prints greeting_shake_128 of Ada")
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_shake_128("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = StringIO()
    with redirect_stdout(stdout):
        status = main(["Ada"])
    context["cli"] = (status, stdout.getvalue())


@then(
    "it prints a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774 and "
    "greeting_shake_128 is listed in nmg_sdlc_smoke.__all__"
)
def example_output_and_exports(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_DIGEST + "\n",
        "",
    )
    assert "greeting_shake_128" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then(
    "the README documents the fixed 32-byte SHAKE-128 hex output over the UTF-8 "
    "greeting and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()


@then("nmg-smoke Ada still prints exactly Hello, Ada and exits with status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    assert context["cli"] == (0, "Hello, Ada\n")
