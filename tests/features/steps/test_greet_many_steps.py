from collections.abc import Iterator

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greet_many
from nmg_sdlc_smoke.cli import main

scenarios("../add_greet_many_library_api.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@given("the library is importable")
def library_is_importable() -> None:
    assert callable(greet)
    assert callable(greet_many)


@when("greet_many is called with an iterable of valid names such as Ada and Bob")
def greet_many_valid_names(context: dict[str, object]) -> None:
    context["greetings"] = greet_many(["Ada", "Bob"])


@then("it returns Hello, Ada and Hello, Bob")
def ordered_greetings(context: dict[str, object]) -> None:
    assert context["greetings"] == ["Hello, Ada", "Hello, Bob"]


@then(
    "each element is the result of applying the existing greet contract to the "
    "corresponding input name"
)
def each_greeting_uses_greet(context: dict[str, object]) -> None:
    assert context["greetings"] == [greet("Ada"), greet("Bob")]


@then("duplicate names produce duplicate greetings in the same positions")
def duplicate_names_are_preserved() -> None:
    assert greet_many(["Ada", "Ada"]) == ["Hello, Ada", "Hello, Ada"]


@when("greet_many is called with an empty iterable")
def greet_many_empty(context: dict[str, object]) -> None:
    context["greetings"] = greet_many(iter(()))


@then("it returns an empty list")
def empty_greetings(context: dict[str, object]) -> None:
    assert context["greetings"] == []


@when(
    "greet_many is called with an iterable whose first invalid name is blank, "
    "whitespace-only, or non-string"
)
def greet_many_invalid_names(context: dict[str, object]) -> None:
    errors: list[ValueError] = []
    for invalid_name in ("", " ", 42):
        with pytest.raises(ValueError) as error:
            greet_many(["Ada", invalid_name, "Bob"])  # type: ignore[list-item]
        errors.append(error.value)

    iterated: list[str] = []

    def names() -> Iterator[str]:
        for name in ("Ada", " ", "Bob"):
            iterated.append(name)
            yield name

    with pytest.raises(ValueError):
        greet_many(names())

    context["errors"] = errors
    context["iterated"] = iterated


@then("it raises ValueError with message name must not be blank")
def exact_invalid_name_error(context: dict[str, object]) -> None:
    errors = context["errors"]
    assert isinstance(errors, list)
    assert all(str(error) == "name must not be blank" for error in errors)


@then("that error is the existing greet validation error, not a wrapped or renamed error")
def unwrapped_greet_error(context: dict[str, object]) -> None:
    with pytest.raises(ValueError) as direct_error:
        greet(" ")
    errors = context["errors"]
    assert isinstance(errors, list)
    assert all(type(error) is type(direct_error.value) for error in errors)
    assert all(error.args == direct_error.value.args for error in errors)
    assert all(error.__cause__ is None and error.__context__ is None for error in errors)


@then("it does not return greetings for later names")
def later_names_are_not_iterated(context: dict[str, object]) -> None:
    assert context["iterated"] == ["Ada", " "]


@when("greet_many is called with a str as the names argument")
def greet_many_bare_string(context: dict[str, object]) -> None:
    with pytest.raises(TypeError) as error:
        greet_many("Ada")
    context["error"] = error.value


@then("it raises TypeError")
def bare_string_type_error(context: dict[str, object]) -> None:
    error = context["error"]
    assert isinstance(error, TypeError)
    assert str(error) == "names must not be a str"


@then(
    "it does not iterate the string as characters and does not return per-character "
    "greetings"
)
def no_per_character_greetings(context: dict[str, object]) -> None:
    assert "greetings" not in context


@given("the distribution is installed")
def distribution_is_installed() -> None:
    assert callable(main)


@when("greet is called with Ada")
def greet_ada(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")


@then("it returns Hello, Ada")
def greet_ada_result(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"


@when("nmg-smoke Ada is run")
def run_nmg_smoke_ada(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["Ada"])
    context["stdout"] = capsys.readouterr().out


@then("the process exits 0 and prints Hello, Ada followed by a single newline")
def successful_cli_greeting(context: dict[str, object]) -> None:
    assert context["exit_code"] == 0
    assert context["stdout"] == "Hello, Ada\n"


@then(
    "blank names still raise ValueError from greet and still cause the CLI to exit "
    "non-zero without a stdout greeting"
)
def blank_name_behavior_is_unchanged(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ValueError, match="^name must not be blank$"):
        greet(" ")
    with pytest.raises(SystemExit) as exit_info:
        main([" "])

    captured = capsys.readouterr()
    assert exit_info.value.code == 1
    assert captured.out == ""
