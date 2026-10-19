import base64
import subprocess
import sys
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_base64_library_helper.feature")

README = Path(__file__).resolve().parents[3] / "README.md"
ADA_BASE64 = "SGVsbG8sIEFkYQ=="
LONG_BASE64 = (
    "SGVsbG8sIEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
    "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQQ=="
)
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
    "greeting_sha256",
    "greeting_starts_with_hello",
    "greeting_vowel_count",
    "greeting_word_count",
)
PROSE = (
    "`greeting_base64` encodes the complete greeting (not the name alone) as UTF-8 "
    "and returns its standard Base64 encoding as a `str`, using the RFC 4648 "
    "alphabet with `+` and `/`, `=` padding, and no line breaks; no Unicode "
    "normalization is applied, so precomposed and decomposed spellings of a name "
    "produce different results, and it inherits `greet`'s "
    '`ValueError("name must not be blank")` for empty, whitespace-only, and '
    "non-string names."
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed nmg_sdlc_smoke package")
def installed_package() -> None:
    assert callable(library.greeting_base64)


@when("greeting_base64 is called with Ada")
def encode_ada(context: dict[str, object]) -> None:
    context["result"] = library.greeting_base64("Ada")


@then("the result is the Python str SGVsbG8sIEFkYQ==")
def ada_base64(context: dict[str, object]) -> None:
    result = context["result"]
    assert type(result) is str
    assert result == ADA_BASE64


@then(
    "decoding it with the standard Base64 alphabet yields exactly the 10 UTF-8 "
    "bytes of Hello, Ada"
)
def ada_decodes(context: dict[str, object]) -> None:
    encoded = b"Hello, Ada"
    assert len(encoded) == 10
    assert base64.b64decode(context["result"], validate=True) == encoded


@when("greeting_base64 is called with a?>, a>>, Bo, and Bob~")
def encode_alphabet_cases(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_base64(name) for name in ("a?>", "a>>", "Bo", "Bob~")
    ]


@then(
    "the results are SGVsbG8sIGE/Pg==, SGVsbG8sIGE+Pg==, SGVsbG8sIEJv, and "
    "SGVsbG8sIEJvYn4="
)
def alphabet_results(context: dict[str, object]) -> None:
    assert context["results"] == [
        "SGVsbG8sIGE/Pg==",
        "SGVsbG8sIGE+Pg==",
        "SGVsbG8sIEJv",
        "SGVsbG8sIEJvYn4=",
    ]


@then("no result uses the URL-safe characters _ or -")
def no_url_safe(context: dict[str, object]) -> None:
    for result in context["results"]:
        assert "_" not in result
        assert "-" not in result


@when(
    "greeting_base64 is called with Zo followed by precomposed U+00EB, with Zoe "
    "followed by combining U+0308, and with A repeated 60 times"
)
def encode_code_points(context: dict[str, object]) -> None:
    context["results"] = [
        library.greeting_base64(name) for name in ("Zo\u00eb", "Zoe\u0308", "A" * 60)
    ]


@then(
    "the results for the precomposed and decomposed names are SGVsbG8sIFpvw6s= "
    "and SGVsbG8sIFpvZcyI"
)
def unnormalized_results(context: dict[str, object]) -> None:
    assert context["results"][:2] == ["SGVsbG8sIFpvw6s=", "SGVsbG8sIFpvZcyI"]


@then(
    "the result for A repeated 60 times is the single 92-character line "
    + LONG_BASE64
    + " with no line breaks"
)
def unwrapped_result(context: dict[str, object]) -> None:
    result = context["results"][2]
    assert result == LONG_BASE64
    assert len(result) == 92
    assert "\n" not in result
    assert "\r" not in result


@given("the invalid names empty, space-tab, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_base64 is called with each invalid name")
def reject_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_base64(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def existing_validation(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the README Library section")
def readme_library(context: dict[str, object]) -> None:
    context["readme"] = README.read_text(encoding="utf-8")


@when(
    "the README Library example runs and prints greeting_base64 of Ada, and "
    "nmg-smoke Ada runs"
)
def run_readme_example_and_cli(context: dict[str, object]) -> None:
    readme = context["readme"]
    start = readme.index("```python\n") + len("```python\n")
    example = readme[start : readme.index("```", start)]
    context["run"] = subprocess.run(
        [sys.executable, "-c", example + 'print(greeting_base64("Ada"))\n'],
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


@then("the example prints SGVsbG8sIEFkYQ==")
def example_output(context: dict[str, object]) -> None:
    result = context["run"]
    assert (result.returncode, result.stdout, result.stderr) == (
        0,
        ADA_BASE64 + "\n",
        "",
    )


@then(
    "greeting_base64 is listed in nmg_sdlc_smoke.__all__ alongside every "
    "previously listed export"
)
def exports_listed() -> None:
    assert "greeting_base64" in library.__all__
    assert set(PRIOR_EXPORTS) <= set(library.__all__)


@then("nmg-smoke prints Hello, Ada with one newline and exit status 0")
def cli_unchanged(context: dict[str, object]) -> None:
    result = context["cli"]
    assert (result.returncode, result.stdout, result.stderr) == (0, "Hello, Ada\n", "")


@then(
    "the README documents UTF-8 encoding of the complete greeting, the standard "
    "padded unwrapped Base64 alphabet, the str result without Unicode "
    "normalization, and the inherited invalid-name error"
)
def readme_prose(context: dict[str, object]) -> None:
    assert PROSE in context["readme"].splitlines()
