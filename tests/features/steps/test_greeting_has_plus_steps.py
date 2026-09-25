import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_plus

scenarios("../add_public_greeting_has_plus_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada+ and the public greeting library")
def name_with_plus(context: dict[str, object]) -> None:
    context["name"] = "Ada+"


@given("the valid name Ada and the public greeting library")
def name_without_plus(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("greeting_has_plus is called with that name")
def call_plus_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_plus(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada+ and the result is True")
def plus_present(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada+"
    assert context["result"] is True


@then("the completed greeting is Hello, Ada and the result is False")
def plus_absent(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@given("the invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t\n", None, 42)


@when("greeting_has_plus is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:
        with pytest.raises(ValueError) as error:
            greeting_has_plus(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4
