import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_ends_with_exclamation
from nmg_sdlc_smoke.cli import main

scenarios("../add_greeting_ends_with_exclamation_library_function.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the library is importable for the exclamation helper")
def library_is_importable() -> None:
    assert callable(greeting_ends_with_exclamation)


@when("greeting_ends_with_exclamation is called with Ada")
def call_with_ada(context: dict[str, object]) -> None:
    context["result"] = greeting_ends_with_exclamation("Ada")


@then("it returns exactly Hello, Ada!")
def returns_exact_greeting(context: dict[str, object]) -> None:
    assert context["result"] == "Hello, Ada!"


@given("a valid name contains leading and trailing spaces")
def spaced_name(context: dict[str, object]) -> None:
    context["name"] = " Ada "


@when("greeting_ends_with_exclamation is called with that name")
def call_with_spaced_name(context: dict[str, object]) -> None:
    name = context["name"]
    assert isinstance(name, str)
    context["result"] = greeting_ends_with_exclamation(name)


@then("every name character is preserved before the final exclamation mark")
def preserves_name(context: dict[str, object]) -> None:
    assert context["result"] == "Hello,  Ada !"


@given("the exclamation helper is imported from the public package")
def helper_is_public() -> None:
    assert callable(greeting_ends_with_exclamation)


@when("greeting_ends_with_exclamation receives invalid names")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors: list[ValueError] = []
    for name in ("", " ", "\t", "\n", None, 42):
        with pytest.raises(ValueError) as error:
            greeting_ends_with_exclamation(name)  # type: ignore[arg-type]
        errors.append(error.value)
    context["errors"] = errors


@then(
    "each exclamation helper call raises ValueError with message name must not be blank"
)
def raises_existing_validation_error(context: dict[str, object]) -> None:
    errors = context["errors"]
    assert isinstance(errors, list)
    assert len(errors) == 6
    assert all(type(error) is ValueError for error in errors)
    assert all(str(error) == "name must not be blank" for error in errors)


@given("the distribution is installed for exclamation regression coverage")
def distribution_is_installed() -> None:
    assert callable(greet)
    assert callable(main)


@when("greet and nmg-smoke are used with Ada")
def use_existing_interfaces(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["greeting"] = greet("Ada")
    context["exit_code"] = main(["Ada"])
    context["captured"] = capsys.readouterr()


@then("greet returns Hello, Ada unchanged")
def greet_is_unchanged(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"


@then("the CLI exits 0 and prints Hello, Ada followed by one newline")
def cli_is_unchanged(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""
