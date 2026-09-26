import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke
from nmg_sdlc_smoke import greeting_has_exclamation_or_question

scenarios("../add_public_greeting_has_exclamation_or_question_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given('the public greeting package and valid name "Ada!"')
def exclamation_name(context: dict[str, object]) -> None:
    context["name"] = "Ada!"


@given('the public greeting package and valid name "Ada?"')
def question_name(context: dict[str, object]) -> None:
    context["name"] = "Ada?"


@when("I call the combined punctuation helper")
def call_helper(context: dict[str, object]) -> None:
    context["result"] = greeting_has_exclamation_or_question(context["name"])  # type: ignore[arg-type]


@then("the result is Python True")
def result_true(context: dict[str, object]) -> None:
    assert context["result"] is True


@given('valid names "Ada", "Ada！？", and "Ada!?"')
def valid_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada\uff01\uff1f", "Ada!?")


@when("I call the combined punctuation helper for each name")
def call_for_each_name(context: dict[str, object]) -> None:
    context["results"] = [greeting_has_exclamation_or_question(name) for name in context["names"]]  # type: ignore[union-attr]


@then("the results are Python False, False, and True respectively")
def absence_and_combined(context: dict[str, object]) -> None:
    results = context["results"]
    assert len(results) == 3  # type: ignore[arg-type]
    assert results[0] is False  # type: ignore[index]
    assert results[1] is False  # type: ignore[index]
    assert results[2] is True  # type: ignore[index]


@given('invalid names "", " \\t", None, and 42')
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("I call the combined punctuation helper for each invalid name")
def call_for_each_invalid_name(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_exclamation_or_question(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then('each call raises ValueError with exact message "name must not be blank"')
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the combined punctuation helper imported from nmg_sdlc_smoke")
def public_import(context: dict[str, object]) -> None:
    assert "greeting_has_exclamation_or_question" in nmg_sdlc_smoke.__all__
    context["helper"] = nmg_sdlc_smoke.greeting_has_exclamation_or_question


@when('I call it with "Ada!", "Ada?", and "Ada"')
def call_readme_examples(context: dict[str, object]) -> None:
    helper = context["helper"]
    context["results"] = [helper(name) for name in ("Ada!", "Ada?", "Ada")]  # type: ignore[operator]


@then("the results are Python True, True, and False respectively")
def readme_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert len(results) == 3  # type: ignore[arg-type]
    assert results[0] is True  # type: ignore[index]
    assert results[1] is True  # type: ignore[index]
    assert results[2] is False  # type: ignore[index]
