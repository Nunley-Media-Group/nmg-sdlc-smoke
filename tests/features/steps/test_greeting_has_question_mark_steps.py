import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greeting_has_question_mark

scenarios("../add_greeting_has_question_mark_library_probe.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("a valid name containing a question mark")
def name_with_question_mark(context: dict[str, object]) -> None:
    context["name"] = "Ada?"


@given("a valid name without a question mark")
def name_without_question_mark(context: dict[str, object]) -> None:
    context["name"] = "Ada"


@when("I call the exported greeting_has_question_mark helper")
def call_helper(context: dict[str, object]) -> None:
    context["result"] = greeting_has_question_mark(context["name"])


@then("the result is true")
def reports_question_mark(context: dict[str, object]) -> None:
    assert context["result"] is True


@then("the result is false")
def reports_no_question_mark(context: dict[str, object]) -> None:
    assert context["result"] is False


@given("a blank, whitespace-only, or non-string name")
def invalid_names(context: dict[str, object]) -> None:
    context["invalid_names"] = ("", " \t\n", None, 42)


@when("I call the exported greeting_has_question_mark helper with each invalid name")
def call_helper_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["invalid_names"]:
        with pytest.raises(ValueError) as error:
            greeting_has_question_mark(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("the existing greet ValueError is raised")
def reports_validation_errors(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4
