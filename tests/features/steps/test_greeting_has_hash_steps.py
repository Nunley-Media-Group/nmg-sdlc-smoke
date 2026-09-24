import subprocess
import sysconfig
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_hash, greeting_has_question_mark

scenarios("../add_public_greeting_has_hash_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada# and the public greeting library")
def name_with_hash(context: dict[str, object]) -> None:
    context["name"] = "Ada#"


@given("the valid name Ada and the public greeting library")
def name_without_hash(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_hash is called with that name")
def call_hash_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_hash(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada# and the result is True")
def hash_present(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada#"
    assert context["result"] is True


@then("the completed greeting is Hello, Ada and the result is False")
def hash_absent(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@given("the invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " ", None, 42)


@when("greeting_has_hash is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_has_hash(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the public greeting helpers and the installed nmg-smoke console script")
def installed_script(context: dict[str, object]) -> None:
    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / "nmg-smoke"
    if not executable.exists():
        executable = scripts / "nmg-smoke.exe"
    context["executable"] = executable


@when("greet Ada, greeting_has_question_mark Ada?, and nmg-smoke Ada are invoked")
def invoke_existing_interfaces(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")
    context["question_mark"] = greeting_has_question_mark("Ada?")
    context["cli"] = subprocess.run(
        [str(context["executable"]), "Ada"],
        capture_output=True,
        text=True,
        check=False,
    )


@then("they yield Hello, Ada, True, and one Hello, Ada newline on stdout with exit zero")
def existing_interfaces_preserved(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["question_mark"] is True
    cli = context["cli"]
    assert (cli.returncode, cli.stdout, cli.stderr) == (0, "Hello, Ada\n", "")
