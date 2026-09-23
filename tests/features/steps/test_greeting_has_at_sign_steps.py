import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke as library

scenarios("../add_greeting_has_at_sign_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed greeting library and a valid name containing an at sign")
def name_with_at_sign(context: dict[str, object]) -> None:
    context["name"] = "Ada@"


@given("the installed greeting library and a valid name without an at sign")
def name_without_at_sign(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_at_sign is called with Ada@")
@when("greeting_has_at_sign is called with Ada")
def detect_at_sign(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = library.greet(name)
    context["result"] = library.greeting_has_at_sign(name)


@then("it returns True for the completed greeting Hello, Ada@")
def detects_literal_at_sign(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada@"
    assert context["result"] is True


@then("it returns False for the completed greeting Hello, Ada")
def reports_absent_at_sign(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@given("empty, whitespace-only, and non-string names")
def invalid_names(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t\n", None, 42)


@when("greeting_has_at_sign is called with each invalid name")
def detect_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["invalid_names"]:
        with pytest.raises(ValueError) as error:
            library.greeting_has_at_sign(name)
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def reports_validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4
