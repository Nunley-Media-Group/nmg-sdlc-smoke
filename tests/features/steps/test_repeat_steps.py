import pytest
from pytest_bdd import scenarios, then, when

from nmg_sdlc_smoke.cli import main

pytest_plugins = ["test_greeting_steps", "test_uppercase_steps"]

scenarios("../add_nmg_smoke_repeat_count_option.feature")


@pytest.fixture
def context() -> dict[str, object]:
    return {}


@when("nmg-smoke --repeat 3 Ada is run")
def invoke_repeat_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--repeat", "3", "Ada"])
    context["captured"] = capsys.readouterr()


@then(
    "the process exits 0 and prints Hello, Ada exactly three times, each "
    "followed by a newline"
)
def exact_repeat_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "Hello, Ada\nHello, Ada\nHello, Ada\n"


@then("stderr is empty")
def stderr_is_empty(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.err == ""


@when(
    "nmg-smoke --repeat is run with a missing COUNT, a non-integer COUNT, 0, "
    "or a negative COUNT"
)
def invoke_invalid_repeat_counts(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    outcomes: list[tuple[object, str, str]] = []
    for argv in (
        ["--repeat"],
        ["--repeat", "abc", "Ada"],
        ["--repeat", "0", "Ada"],
        ["--repeat", "-1", "Ada"],
    ):
        with pytest.raises(SystemExit) as exit_info:
            main(argv)
        captured = capsys.readouterr()
        outcomes.append((exit_info.value.code, captured.out, captured.err))
    context["outcomes"] = outcomes


@then(
    "each invocation exits non-zero with no greeting on stdout and "
    "argparse-style usage or error text on stderr"
)
def invalid_repeat_counts_fail(context: dict[str, object]) -> None:
    outcomes = context["outcomes"]
    assert isinstance(outcomes, list)
    assert len(outcomes) == 4
    for exit_code, stdout, stderr in outcomes:
        assert exit_code != 0
        assert stdout == ""
        assert stderr
        assert "usage:" in stderr or "error:" in stderr


@when("nmg-smoke --repeat 2 is invoked with that name")
def invoke_repeat_with_blank_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--repeat", "2", str(context["blank_name"])])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@when("nmg-smoke --repeat 2 is run with no name argument")
def invoke_repeat_without_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--repeat", "2"])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()
