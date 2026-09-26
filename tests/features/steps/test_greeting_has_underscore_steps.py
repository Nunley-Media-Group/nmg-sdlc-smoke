import pytest
from pytest_bdd import given, scenarios, then, when

import nmg_sdlc_smoke
from nmg_sdlc_smoke import greet, greeting_has_underscore

scenarios("../add_public_greeting_has_underscore_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the public greeting package and valid name Ada_")
def underscore_name(context: dict[str, object]) -> None:
    context["name"] = "Ada_"


@when("greeting_has_underscore is called with Ada_")
def call_helper(context: dict[str, object]) -> None:
    context["result"] = greeting_has_underscore(context["name"])  # type: ignore[arg-type]


@then("greet returns Hello, Ada_ and the helper returns True")
def detects_underscore(context: dict[str, object]) -> None:
    assert greet(context["name"]) == "Hello, Ada_"  # type: ignore[arg-type]
    assert context["result"] is True


@given("valid names Ada and Ada＿")
def valid_names(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada\uff3f")


@when("greeting_has_underscore is called with each valid name")
def call_for_each_name(context: dict[str, object]) -> None:
    context["results"] = [greeting_has_underscore(name) for name in context["names"]]  # type: ignore[union-attr]


@then("each completed greeting lacks literal underscore and each helper result is False")
def reports_absence(context: dict[str, object]) -> None:
    for name in context["names"]:  # type: ignore[union-attr]
        assert "_" not in greet(name)
    results = context["results"]
    assert len(results) == 2  # type: ignore[arg-type]
    assert results[0] is False  # type: ignore[index]
    assert results[1] is False  # type: ignore[index]


@given("invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " \t", None, 42)


@when("greeting_has_underscore is called with each invalid name")
def call_for_each_invalid_name(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_underscore(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the installed public package and README Library examples Ada_ and Ada")
def readme_examples(context: dict[str, object]) -> None:
    context["names"] = ("Ada_", "Ada")


@when("greeting_has_underscore is imported from nmg_sdlc_smoke and called with those names")
def call_public_import(context: dict[str, object]) -> None:
    assert "greeting_has_underscore" in nmg_sdlc_smoke.__all__
    helper = nmg_sdlc_smoke.greeting_has_underscore
    context["results"] = [helper(name) for name in context["names"]]  # type: ignore[union-attr]


@then("the imported helper returns True and False respectively")
def readme_results(context: dict[str, object]) -> None:
    results = context["results"]
    assert len(results) == 2  # type: ignore[arg-type]
    assert results[0] is True  # type: ignore[index]
    assert results[1] is False  # type: ignore[index]
