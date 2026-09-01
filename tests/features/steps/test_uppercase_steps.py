from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke import greet
from nmg_sdlc_smoke.cli import main

pytest_plugins = ["test_greeting_steps"]

scenarios("../add_nmg_smoke_uppercase_flag.feature")

ROOT = Path(__file__).parents[3]


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@when("nmg-smoke --uppercase Ada is run")
def invoke_uppercase_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--uppercase", "Ada"])
    context["captured"] = capsys.readouterr()


@then("the process exits 0 and prints HELLO, ADA followed by a single newline")
def exact_uppercase_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "HELLO, ADA\n"
    assert captured.err == ""


@then("nmg-smoke Ada --uppercase produces the same stdout and exit code")
def positional_before_flag(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["Ada", "--uppercase"]) == context["exit_code"]
    captured = capsys.readouterr()
    assert captured.out == "HELLO, ADA\n"
    assert captured.err == ""


@given("the distribution is installed")
def distribution_installed() -> None:
    assert 'nmg-smoke = "nmg_sdlc_smoke.cli:main"' in (
        ROOT / "pyproject.toml"
    ).read_text()


@when("nmg-smoke --uppercase is run with no name argument")
def invoke_uppercase_without_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--uppercase"])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@then("the process exits non-zero and does not print a greeting")
def missing_name_fails(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] != 0
    assert captured.out == ""


@when("nmg-smoke --uppercase is invoked with that name")
def invoke_uppercase_with_blank_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--uppercase", str(context["blank_name"])])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@then("the CLI exits non-zero without printing a greeting to stdout")
def blank_name_fails(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 1
    assert captured.out == ""
    assert "name must not be blank" in captured.err


@given("the library is importable")
def library_importable() -> None:
    assert callable(greet)


@then(
    "blank, whitespace-only, and non-string names still raise ValueError with "
    "message name must not be blank"
)
def invalid_library_names_unchanged() -> None:
    for name in ("", " ", "\t", "\n", None, 1):
        with pytest.raises(ValueError) as error:
            greet(name)  # type: ignore[arg-type]
        assert str(error.value) == "name must not be blank"
