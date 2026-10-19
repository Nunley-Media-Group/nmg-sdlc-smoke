import hashlib
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_sha256_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_DIGEST = "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"
PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_bytes",
    "greeting_casefold",
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
    "greeting_reversed",
    "greeting_starts_with_hello",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_sha256` encodes the complete greeting (not the name alone) as UTF-8 "
    "and returns its SHA-256 digest as 64 lowercase hexadecimal characters; no "
    "Unicode normalization is applied, so precomposed and decomposed spellings of a "
    "name produce different digests, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_sha256)


@when("greeting_sha256 is called with Ada")
def hash_ada(context: dict[str, object]) -> None:
    context["result"] = library.greeting_sha256("Ada")


@then(
    "the result is the Python str "
    "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"
)
def ada_digest(context: dict[str, object]) -> None:
    result = context["result"]
    assert type(result) is str
    assert result == ADA_DIGEST


@then(
    "it is the SHA-256 digest of the 10 UTF-8 bytes of Hello, Ada written as 64 "
    "lowercase hexadecimal characters"
)
def ada_digest_format(context: dict[str, object]) -> None:
    result = context["result"]
    greeting = "Hello, Ada"
    encoded = greeting.encode("utf-8")
    assert len(encoded) == 10
    assert result == hashlib.sha256(encoded).hexdigest()
    assert len(result) == 64
    assert all(character in "0123456789abcdef" for character in result)


@when(
    "greeting_sha256 is called with Zo followed by precomposed U+00EB and with Zoe "
    "followed by combining U+0308"
)
def hash_unnormalized(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_sha256(name) for name in ("Zo\u00eb", "Zoe\u0308")
    ]


@then(
    "the results are aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524 "
    "and af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064"
)
def unnormalized_digests(context: dict[str, object]) -> None:
    assert context["results"] == [
        "aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524",
        "af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064",
    ]


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_sha256 is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_sha256(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_sha256 of Ada, and "
    "nmg-smoke Ada runs"
)
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_sha256("Ada"))\n'],
        capture_output=True,
        text=True,
        check=False,
    )
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["cli"] = subprocess.run(
        [str(executable), "Ada"], capture_output=True, text=True, check=False
    )


@then(
    "the example prints "
    "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"
)
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_DIGEST + "\n",
        "",
    )


@then(
    "greeting_sha256 is listed in nmg_sdlc_smoke.__all__ alongside every "
    "previously listed export"
)
def exports_listed() -> None:
    assert "greeting_sha256" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("nmg-smoke prints Hello, Ada with one newline and exit status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then(
    "the README documents the 64-character lowercase hex format, UTF-8 encoding of "
    "the complete greeting, absence of Unicode normalization, and the inherited "
    "invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
