import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_contains_name
from nmg_sdlc_smoke.cli import main

scenarios("../add_greeting_contains_name_library_function.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the library is importable")
def library_importable() -> None:
    assert callable(greet)
    assert callable(greeting_contains_name)


@given("the distribution is installed")
def distribution_installed() -> None:
    assert callable(greet)
    assert callable(main)


@when("greeting_contains_name is called with Ada")
def greeting_contains_name_ada(context: dict[str, object]) -> None:
    context["result"] = greeting_contains_name("Ada")


@then("it returns True")
def returns_true(context: dict[str, object]) -> None:
    assert context["result"] is True


@then("that value equals Ada in greet Ada which is Hello, Ada")
def equals_ada_membership(context: dict[str, object]) -> None:
    assert greet("Ada") == "Hello, Ada"
    assert context["result"] is True
    assert context["result"] == ("Ada" in greet("Ada"))


@then("the return value is the Python bool True, not the string True")
def returns_python_bool(context: dict[str, object]) -> None:
    assert context["result"] is True
    assert context["result"] != "True"


@when("greeting_contains_name is called with Jo")
def greeting_contains_name_jo(context: dict[str, object]) -> None:
    context["result"] = greeting_contains_name("Jo")


@then("that value equals Jo in greet Jo which is Hello, Jo")
def equals_jo_membership(context: dict[str, object]) -> None:
    assert greet("Jo") == "Hello, Jo"
    assert context["result"] is True
    assert context["result"] == ("Jo" in greet("Jo"))


@then("the result is not hardcoded to the Ada call only")
def is_not_ada_only(context: dict[str, object]) -> None:
    assert context["result"] == ("Jo" in greet("Jo"))
    assert "Ada" not in greet("Jo")
    assert greeting_contains_name("Ada") is True


@when("greeting_contains_name is called with a blank, whitespace-only, or non-string name")
def greeting_contains_name_invalid_names(context: dict[str, object]) -> None:
    errors: list[ValueError] = []
    greet_errors: list[ValueError] = []
    for name in ("", " ", "\t", "\n", None, 42):
        with pytest.raises(ValueError) as error:
            greeting_contains_name(name)  # type: ignore[arg-type]
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
    assert all(error.__context__ is None for error in errors)


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


@then("blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting")
def blank_names_still_fail(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet("")
    with pytest.raises(SystemExit) as exit_info:
        main([""])
    captured = capsys.readouterr()
    assert isinstance(exit_info.value.code, int)
    assert exit_info.value.code > 0
    assert captured.out == ""
