import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import (
    greet,
    greet_many,
    greeting_bytes,
    greeting_casefold,
    greeting_ends_with_exclamation,
    greeting_ends_with_name,
    greeting_has_ampersand,
    greeting_has_at_sign,
    greeting_has_colon,
    greeting_has_equal,
    greeting_has_hash,
    greeting_has_percent,
    greeting_has_plus,
    greeting_has_question_mark,
    greeting_has_semicolon,
    greeting_is_ascii,
    greeting_length,
    greeting_starts_with_hello,
    greeting_word_count,
)

scenarios("../add_public_greeting_has_ampersand_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada& and the public greeting library")
def name_with_ampersand(context: dict[str, object]) -> None:
    context["name"] = "Ada&"


@when("greeting_has_ampersand is called with that name")
def call_ampersand_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_ampersand(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada& and the result is True")
def ampersand_present(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada&"
    assert context["result"] is True


@given("valid names Ada and Ada＆ and the public greeting library")
def names_without_ampersand(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada＆")


@when("greeting_has_ampersand is called with each name")
def call_for_names_without_ampersand(context: dict[str, object]) -> None:
    names = context["names"]
    context["greetings"] = [greet(name) for name in names]  # type: ignore[union-attr]
    context["results"] = [greeting_has_ampersand(name) for name in names]  # type: ignore[union-attr]


@then("each completed greeting lacks ASCII ampersand and each result is False")
def ampersand_absent(context: dict[str, object]) -> None:
    assert context["greetings"] == ["Hello, Ada", "Hello, Ada＆"]
    assert all("&" not in greeting for greeting in context["greetings"])  # type: ignore[union-attr]
    assert all(result is False for result in context["results"])  # type: ignore[union-attr]


@given("invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_ampersand is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_ampersand(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the previously public package exports and the installed nmg-smoke script")
def public_exports_and_script(context: dict[str, object]) -> None:
    context["exports"] = (
        greet, greet_many, greeting_bytes, greeting_casefold,
        greeting_ends_with_exclamation, greeting_ends_with_name,
        greeting_has_at_sign, greeting_has_colon, greeting_has_equal,
        greeting_has_hash, greeting_has_percent, greeting_has_plus,
        greeting_has_question_mark, greeting_has_semicolon,
        greeting_is_ascii, greeting_length, greeting_starts_with_hello,
        greeting_word_count, greeting_has_ampersand,
    )
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when("those exports and greeting_has_ampersand are imported and greet Ada, greeting_has_equal Ada=, and nmg-smoke Ada are invoked")
def invoke_public_interfaces(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")
    context["equal"] = greeting_has_equal("Ada=")
    context["cli"] = subprocess.run(
        [str(context["executable"]), "Ada"],
        capture_output=True,
        text=True,
        check=False,
    )


@then("all imports succeed, the library returns Hello, Ada and True, and the CLI exits zero with one Hello, Ada newline on stdout and empty stderr")
def public_interfaces_preserved(context: dict[str, object]) -> None:
    assert all(callable(export) for export in context["exports"])  # type: ignore[union-attr]
    assert context["greeting"] == "Hello, Ada"
    assert context["equal"] is True
    cli = context["cli"]
    assert (cli.returncode, cli.stdout, cli.stderr) == (0, "Hello, Ada\n", "")
