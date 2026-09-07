import pytest
from pytest_bdd import scenarios, then, when

from nmg_sdlc_smoke.cli import main

pytest_plugins = ["test_greeting_steps", "test_repeat_steps", "test_no_newline_steps"]

scenarios("../add_nmg_smoke_separator_text_option.feature")


@when("nmg-smoke --repeat 2 --separator ' | ' Ada is run")
def invoke_separator_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--repeat", "2", "--separator", " | ", "Ada"])
    context["captured"] = capsys.readouterr()


@then("stdout is exactly Hello, Ada | Hello, Ada followed by a single newline")
def exact_separator_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == "Hello, Ada | Hello, Ada\n"


@when("nmg-smoke --repeat 2 Ada is run")
def invoke_default_separator_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--repeat", "2", "Ada"])
    context["captured"] = capsys.readouterr()


@then("stdout is exactly two lines of Hello, Ada, each followed by a newline")
def exact_default_separator_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == "Hello, Ada\nHello, Ada\n"
