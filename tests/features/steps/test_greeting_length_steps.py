import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_length
from nmg_sdlc_smoke.cli import main

scenarios("../add_greeting_length_library_function.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the library is importable")
def library_importable() -> None:
    assert callable(greet)
    assert callable(greeting_length)


@when("greeting_length is called with Ada")
def greeting_length_ada(context: dict[str, object]) -> None:
    context["result"] = greeting_length("Ada")


@then("it returns 10")
def returns_ten(context: dict[str, object]) -> None:
    assert context["result"] == 10


@then("that value equals the Python len of greet Ada which is Hello, Ada")
def equals_ada_greeting_length(context: dict[str, object]) -> None:
    assert greet("Ada") == "Hello, Ada"
    assert context["result"] == len(greet("Ada"))


@when("greeting_length is called with Jo")
def greeting_length_jo(context: dict[str, object]) -> None:
    context["result"] = greeting_length("Jo")


@then("it returns 9")
def returns_nine(context: dict[str, object]) -> None:
    assert context["result"] == 9


@then("that value equals the Python len of greet Jo which is Hello, Jo")
def equals_jo_greeting_length(context: dict[str, object]) -> None:
    assert greet("Jo") == "Hello, Jo"
    assert context["result"] == len(greet("Jo"))


@then("the result is not hardcoded to the Ada count")
def differs_from_ada_count(context: dict[str, object]) -> None:
    assert context["result"] != greeting_length("Ada")


@when("greeting_length is called with a blank, whitespace-only, or non-string name")
def greeting_length_invalid_names(context: dict[str, object]) -> None:
    errors: list[ValueError] = []
    greet_errors: list[ValueError] = []
    for name in ("", " ", "\t", "\n", None, 42):
        with pytest.raises(ValueError) as error:
            greeting_length(name)  # type: ignore[arg-type]
        with pytest.raises(ValueError) as greet_error:
            greet(name)  # type: ignore[arg-type]
        errors.append(error.value)
        greet_errors.append(greet_error.value)
    context["errors"] = errors
    context["greet_errors"] = greet_errors


@then("it raises ValueError with message name must not be blank")
def raises_existing_message(context: dict[str, object]) -> None:
    errors = context["errors"]
    assert isinstance(errors, list)
    assert errors
    assert all(str(error) == "name must not be blank" for error in errors)


@then("that error is the existing greet validation error, not a wrapped or renamed error")
def propagates_greet_error(context: dict[str, object]) -> None:
    errors = context["errors"]
    greet_errors = context["greet_errors"]
    assert isinstance(errors, list)
    assert isinstance(greet_errors, list)
    assert [(type(error), str(error)) for error in errors] == [
        (type(error), str(error)) for error in greet_errors
    ]
    assert all(error.__cause__ is None for error in errors)


@given("the distribution is installed")
def distribution_installed() -> None:
    assert callable(greet)
    assert callable(main)


@when("greet is called with Ada")
def greet_ada(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")


@then("it returns Hello, Ada")
def returns_hello_ada(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"


@then("blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting")
def blank_names_still_fail(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet("")
    with pytest.raises(SystemExit) as exit_info:
        main([""])
    captured = capsys.readouterr()
    assert exit_info.value.code != 0
    assert captured.out == ""
