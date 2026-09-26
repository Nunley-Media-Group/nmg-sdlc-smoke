import importlib

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_has_exclamation

scenarios("../add_public_greeting_has_exclamation_helper.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the installed public greeting package and valid name Ada!")
def exclamation_name(context: dict[str, object]) -> None:
    context["name"] = "Ada!"


@when("greeting_has_exclamation is called with Ada!")
def call_with_exclamation(context: dict[str, object]) -> None:
    name = context["name"]
    context["greeting"] = greet(name)  # type: ignore[arg-type]
    context["result"] = greeting_has_exclamation(name)  # type: ignore[arg-type]


@then("greet returns Hello, Ada! and the helper returns True")
def exclamation_detected(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada!"
    assert context["result"] is True


@given("valid names Ada and Ada！")
def names_without_exclamation(context: dict[str, object]) -> None:
    context["names"] = ("Ada", "Ada\uff01")


@when("greeting_has_exclamation is called with each valid name")
def call_with_valid_names(context: dict[str, object]) -> None:
    names = context["names"]
    context["greetings"] = [greet(name) for name in names]  # type: ignore[union-attr]
    context["results"] = [greeting_has_exclamation(name) for name in names]  # type: ignore[union-attr]


@then("each completed greeting lacks literal ! and each helper result is False")
def exclamation_absent(context: dict[str, object]) -> None:
    assert context["greetings"] == ["Hello, Ada", "Hello, Ada\uff01"]
    assert all("!" not in greeting for greeting in context["greetings"])  # type: ignore[union-attr]
    assert all(result is False for result in context["results"])  # type: ignore[union-attr]
    assert len(context["results"]) == 2  # type: ignore[arg-type]


@given("invalid names empty, whitespace-only, None, and 42")
def invalid_names(context: dict[str, object]) -> None:
    context["names"] = ("", " ", None, 42)


@when("greeting_has_exclamation is called with each invalid name")
def call_with_invalid_names(context: dict[str, object]) -> None:
    errors = []
    for name in context["names"]:  # type: ignore[union-attr]
        with pytest.raises(ValueError) as error:
            greeting_has_exclamation(name)  # type: ignore[arg-type]
        errors.append(str(error.value))
    context["errors"] = errors


@then("each call raises ValueError with message name must not be blank")
def validation_preserved(context: dict[str, object]) -> None:
    assert context["errors"] == ["name must not be blank"] * 4


@given("the installed public package and README Library examples Ada! and Ada")
def documented_examples(context: dict[str, object]) -> None:
    context["examples"] = ("Ada!", "Ada")


@when("greeting_has_exclamation is imported from nmg_sdlc_smoke and called with those names")
def call_public_import(context: dict[str, object]) -> None:
    package = importlib.import_module("nmg_sdlc_smoke")
    helper = package.greeting_has_exclamation
    context["exported"] = "greeting_has_exclamation" in package.__all__
    context["results"] = [helper(name) for name in context["examples"]]  # type: ignore[union-attr]


@then("the imported helper returns True and False respectively")
def documented_results(context: dict[str, object]) -> None:
    assert context["exported"] is True
    assert context["results"][0] is True  # type: ignore[index]
    assert context["results"][1] is False  # type: ignore[index]
