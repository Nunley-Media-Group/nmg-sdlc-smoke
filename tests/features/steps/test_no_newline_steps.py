import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet, greeting_length
from nmg_sdlc_smoke.cli import main

pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]

scenarios("../add_nmg_smoke_no_newline_flag.feature")


@when("nmg-smoke --no-newline Ada is run")
def invoke_no_newline_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--no-newline", "Ada"])
    context["captured"] = capsys.readouterr()


@then("the process exits 0")
def exits_successfully(context: dict[str, object]) -> None:
    assert context["exit_code"] == 0


@then("stdout is exactly Hello, Ada with no trailing newline")
def exact_no_newline_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == "Hello, Ada"


@then("nmg-smoke Ada --no-newline produces the same stdout and exit code")
def flag_after_name_is_equivalent(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["Ada", "--no-newline"]) == context["exit_code"]
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada"
    assert captured.err == ""


@when("nmg-smoke --no-newline --repeat 3 Ada is run")
def invoke_repeated_no_newline_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(
        ["--no-newline", "--repeat", "3", "Ada"]
    )
    context["captured"] = capsys.readouterr()


@then(
    "stdout is exactly three Hello, Ada greetings separated by newlines, "
    "with no newline after the last greeting"
)
def exact_repeated_no_newline_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == "Hello, Ada\nHello, Ada\nHello, Ada"


@when("nmg-smoke --no-newline --uppercase Ada is run")
def invoke_uppercase_no_newline_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(
        ["--no-newline", "--uppercase", "Ada"]
    )
    context["captured"] = capsys.readouterr()


@then("stdout is exactly HELLO, ADA with no trailing newline")
def exact_uppercase_no_newline_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == "HELLO, ADA"


@when("nmg-smoke --no-newline is run with no name argument")
def invoke_no_newline_without_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--no-newline"])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@when("nmg-smoke --no-newline is invoked with that name")
def invoke_no_newline_with_blank_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--no-newline", str(context["blank_name"])])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@given("a caller imports from nmg_sdlc_smoke")
def library_apis_importable() -> None:
    assert callable(greet)
    assert callable(greeting_length)


@when("greet Ada and greeting_length Ada are called")
def invoke_library_apis(context: dict[str, object]) -> None:
    context["greeting"] = greet("Ada")
    context["greeting_length"] = greeting_length("Ada")


@then("greet returns Hello, Ada and greeting_length returns 10")
def library_results_are_unchanged(context: dict[str, object]) -> None:
    assert context["greeting"] == "Hello, Ada"
    assert context["greeting_length"] == 10


@then("invalid names retain the existing name must not be blank ValueError")
def library_validation_is_unchanged() -> None:
    for name in ("", " ", "\t", "\n", None, 42):
        with pytest.raises(ValueError) as error:
            greet(name)  # type: ignore[arg-type]
        assert str(error.value) == "name must not be blank"
