import importlib
import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_ascii_asterisk

scenarios("../add_public_greeting_has_ascii_asterisk_helper.feature")

PRIOR_EXPORTS = (
    "greet",
    "greet_many",
    "greeting_bytes",
    "greeting_casefold",
    "greeting_ends_with_exclamation",
    "greeting_ends_with_name",
    "greeting_has_asterisk",
    "greeting_has_at_sign",
    "greeting_has_backtick",
    "greeting_has_colon",
    "greeting_has_equal",
    "greeting_has_hash",
    "greeting_has_percent",
    "greeting_has_plus",
    "greeting_has_question_mark",
    "greeting_has_semicolon",
    "greeting_is_ascii",
    "greeting_length",
    "greeting_starts_with_hello",
    "greeting_word_count",
)


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada* and the public greeting library")
def ascii_asterisk_name(context: dict[str, object]) -> None:
    context["name"] = "Ada*"


@given("the valid name Ada and the public greeting library")
def name_without_asterisk(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_ascii_asterisk is called with that name")
def call_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_ascii_asterisk(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada* and the result is True")
def asterisk_detected(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada*"
    assert context["result"] is True


@then("the completed greeting is Hello, Ada and the result is False")
def asterisk_absent(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@given("invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_ascii_asterisk is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_ascii_asterisk(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the previously public package exports and the installed nmg-smoke script")
def public_library_and_script(context: dict[str, object]) -> None:
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when(
    "those exports and greeting_has_ascii_asterisk are imported and greet Ada, "
    "greeting_has_asterisk Ada*, and nmg-smoke Ada are invoked"
)
def invoke_interfaces(context: dict[str, object]) -> None:
    package = importlib.import_module("nmg_sdlc_smoke")
    exports = {name: getattr(package, name) for name in (*PRIOR_EXPORTS, "greeting_has_ascii_asterisk")}
    context["exports"] = exports
    context["greeting"] = exports["greet"]("Ada")
    context["asterisk"] = exports["greeting_has_asterisk"]("Ada*")
    context["cli"] = subprocess.run(
        [str(context["executable"]), "Ada"],
        capture_output=True,
        text=True,
        check=False,
    )


@then(
    "all imports succeed, the library returns Hello, Ada and True, and the CLI exits zero "
    "with one Hello, Ada newline on stdout and empty stderr"
)
def interfaces_unchanged(context: dict[str, object]) -> None:
    exports = context["exports"]
    assert all(callable(export) for export in exports.values())  # type: ignore[union-attr]
    assert exports["greeting_has_ascii_asterisk"] is greeting_has_ascii_asterisk  # type: ignore[index]
    assert context["greeting"] == "Hello, Ada"
    assert context["asterisk"] is True
    cli = context["cli"]
    assert (cli.returncode, cli.stdout, cli.stderr) == (0, "Hello, Ada\n", "")
