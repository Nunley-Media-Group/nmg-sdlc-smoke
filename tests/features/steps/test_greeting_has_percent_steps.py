import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_percent

scenarios("../add_greeting_has_percent_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("a valid name Ada%")
def name_with_percent(context: dict[str, object]) -> None:
    context["name"] = "Ada%"


@given("a valid name Ada")
def name_without_percent(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@given("a blank, whitespace-only, or non-string name")
def invalid_names(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t\n", None, 42)


@when("I ask whether its completed greeting contains a literal percent sign")
def check_greeting(context: dict[str, object]) -> None:
    if "invalid_names" in context:
        errors = []
        for name in context["invalid_names"]:
            with pytest.raises(ValueError) as error:
                greeting_has_percent(name)  # type: ignore[arg-type]
            errors.append(str(error.value))
        context["errors"] = errors
    else:
        name = context["name"]
        context["greeting"] = greet(name)  # type: ignore[arg-type]
        context["result"] = greeting_has_percent(name)  # type: ignore[arg-type]


@then("the result is True")
def percent_present(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada%"
    assert context["result"] is True


@then("the result is False")
def percent_absent(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["result"] is False


@then("it raises the same ValueError as greet")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4
