from importlib import import_module

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_bytes, greeting_length
from nmg_sdlc_smoke.cli import main

scenarios("../add_greeting_bytes_library_function.feature")
greet_module = import_module("nmg_sdlc_smoke.greet")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the library is importable")
def library_importable() -> None:
    assert callable(greet)
    assert callable(greeting_bytes)
    assert callable(greeting_length)


@given("the distribution is installed")
def distribution_installed() -> None:
    assert callable(greet)
    assert callable(main)


@when("greeting_bytes is called with Ada")
def greeting_bytes_ada(context: dict[str, object]) -> None:
    context["result"] = greeting_bytes("Ada")


@then("it returns 10")
def returns_ten(context: dict[str, object]) -> None:
    assert context["result"] == 10


@then("that value equals the UTF-8 byte length of greet Ada which is Hello, Ada")
def equals_ada_greeting_byte_length(context: dict[str, object]) -> None:
    assert greet("Ada") == "Hello, Ada"
    assert context["result"] == len(greet("Ada").encode("utf-8"))


@when("greeting_bytes is called with É")
def greeting_bytes_non_ascii(context: dict[str, object]) -> None:
    context["result"] = greeting_bytes("É")


@then("it returns 9")
def returns_nine(context: dict[str, object]) -> None:
    assert context["result"] == 9


@then("that value equals the UTF-8 byte length of greet É which is Hello, É")
def equals_non_ascii_greeting_byte_length(context: dict[str, object]) -> None:
    assert greet("É") == "Hello, É"
    assert context["result"] == len(greet("É").encode("utf-8"))


@then("that value is not equal to greeting_length of É which is 8")
def differs_from_non_ascii_character_count(context: dict[str, object]) -> None:
    assert greeting_length("É") == 8
    assert context["result"] != greeting_length("É")


@then("the result is not hardcoded to the Ada count")
def differs_from_ada_count(context: dict[str, object]) -> None:
    assert context["result"] != greeting_bytes("Ada")


@when("greeting_bytes is called with a blank, whitespace-only, or non-string name")
def greeting_bytes_invalid_names(
    context: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    errors: list[ValueError] = []
    for name in ("", " ", "\t", "\n", None, 42):
        with pytest.raises(ValueError) as error:
            greeting_bytes(name)  # type: ignore[arg-type]
        errors.append(error.value)

    sentinel_error = ValueError("name must not be blank")

    def delegated_greet(name: str) -> str:
        assert name == ""
        raise sentinel_error

    monkeypatch.setattr(greet_module, "greet", delegated_greet)
    with pytest.raises(ValueError) as delegated_error:
        greeting_bytes("")

    context["errors"] = errors
    context["sentinel_error"] = sentinel_error
    context["delegated_error"] = delegated_error.value


@then("it raises ValueError with message name must not be blank")
def raises_existing_message(context: dict[str, object]) -> None:
    errors = context["errors"]
    assert isinstance(errors, list)
    assert errors
    assert all(str(error) == "name must not be blank" for error in errors)


@then(
    "that error is the existing greet validation error, not a wrapped or renamed error"
)
def propagates_greet_error(context: dict[str, object]) -> None:
    assert context["delegated_error"] is context["sentinel_error"]


@when("greet is called with Ada")
def greet_ada(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")


@then("it returns Hello, Ada")
def returns_hello_ada(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"


@when("nmg-smoke Ada is run")
def invoke_cli(context: dict[str, object], capsys: pytest.CaptureFixture[str]) -> None:
    context["exit_code"] = main(["Ada"])
    context["captured"] = capsys.readouterr()


@then("the process exits 0 and prints Hello, Ada followed by a single newline")
def exact_cli_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@then(
    "blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting"
)
def blank_names_still_fail(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet("")
    with pytest.raises(SystemExit) as exit_info:
        main([""])
    captured = capsys.readouterr()
    assert exit_info.value.code != 0
    assert captured.out == ""
