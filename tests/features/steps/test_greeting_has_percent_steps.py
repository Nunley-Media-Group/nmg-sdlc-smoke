import pytest
from pytest_bdd import given, parsers, scenarios, then, when

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


@given(parsers.parse("an invalid {kind} name"))
def invalid_name(context: dict[str, object], kind: str) -> None:
    context["name"] = {
        "blank": "",
        "whitespace-only": " \t\n",
        "non-string None": None,
        "non-string int": 42,
    }[kind]


@when("I ask whether its completed greeting contains a literal percent sign")
def check_greeting(context: dict[str, object]) -> None:
    name = context["name"]
    if not isinstance(name, str) or not name.strip():
        with pytest.raises(ValueError) as helper_error:
            greeting_has_percent(name)  # type: ignore[arg-type]
        with pytest.raises(ValueError) as greet_error:
            greet(name)  # type: ignore[arg-type]
        context["errors"] = (helper_error.value, greet_error.value)
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
    helper_error, greet_error = context["errors"]
    assert str(helper_error) == str(greet_error) == "name must not be blank"
