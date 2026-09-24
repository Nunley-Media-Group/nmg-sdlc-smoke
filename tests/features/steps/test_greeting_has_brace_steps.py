import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import (
    greet,
    greeting_has_brace,
    greeting_has_hash,
    greeting_has_question_mark,
)

scenarios("../add_greeting_has_brace_library_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the valid name Ada{ and the public greeting library")
def name_with_brace(context: dict[str, object]) -> None:
    context["name"] = "Ada{"


@when("greeting_has_brace is called with that name")
def call_brace_helper(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_brace(name)  # type: ignore[arg-type]


@then("the completed greeting is Hello, Ada{ and the result is True")
def brace_present(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada{"
    assert context["result"] is True


@given("the valid names Ada and Ada} and the public greeting library")
def names_without_opening_brace(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada}")


@when("greeting_has_brace is called with each of those names")
def call_brace_helper_for_names(context: dict[str, object]) -> None:
    names = context["names"]
    context["greetings"] = [greet(name) for name in names]  # type: ignore[union-attr]
    context["results"] = [greeting_has_brace(name) for name in names]  # type: ignore[union-attr]


@then("both results are False and the completed greetings are Hello, Ada and Hello, Ada}")
def brace_absent(context: dict[str, object]) -> None:
    assert context["greetings"] == ["Hello, Ada", "Hello, Ada}"]
    assert context["results"] == [False, False]


@given("the invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " ", None, 42)


@when("greeting_has_brace is called with each invalid name")
def call_brace_helper_for_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_brace(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the public greeting library including greeting_has_brace")
def public_library() -> None:
    assert callable(greeting_has_brace)


@when("greet Ada, greeting_has_hash Ada#, and greeting_has_question_mark Ada? are invoked")
def call_existing_exports(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")
    context["hash"] = greeting_has_hash("Ada#")
    context["question_mark"] = greeting_has_question_mark("Ada?")


@then("they yield Hello, Ada, True, and True respectively")
def existing_exports_preserved(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["hash"] is True
    assert context["question_mark"] is True
