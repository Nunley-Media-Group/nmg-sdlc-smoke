import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_tilde

scenarios("../add_greeting_has_tilde_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed greeting library and a valid name containing a tilde")
def name_with_tilde(context: dict[str, object]) -> None:
    context["name"] = "Ada~"


@given("the installed greeting library and a valid name without a tilde")
def name_without_tilde(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_tilde is called with Ada~")
@when("greeting_has_tilde is called with Ada")
def call_helper(context: dict[str, object]) -> None:
    context["result"] = greeting_has_tilde(context["name"])  # type: ignore[arg-type]


@then("it returns True for the completed greeting Hello, Ada~")
def reports_tilde(context: dict[str, object]) -> None:
    assert greet(context["name"]) == "Hello, Ada~"  # type: ignore[arg-type]
    assert context["result"] is True


@then("it returns False for the completed greeting Hello, Ada")
def reports_no_tilde(context: dict[str, object]) -> None:
    assert greet(context["name"]) == "Hello, Ada"  # type: ignore[arg-type]
    assert context["result"] is False


@given("empty, whitespace-only, and non-string names")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_tilde is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_has_tilde(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def reports_validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4
