import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke.cli import main

scenarios("../add_nmg_smoke_quotes_flag.feature")


@given("the installed nmg-smoke console script and a valid name", target_fixture="outcome")
def cli_outcome() -> dict[str, int | str]:
    return {}


@when(
    "nmg-smoke --quotes --uppercase --prefix ok-colon-space --parentheses "
    "--braces Ada runs"
)
def invoke_with_quotes(
    outcome: dict[str, int | str], capsys: pytest.CaptureFixture[str]
) -> None:
    outcome["code"] = main([
        "--quotes",
        "--uppercase",
        "--prefix",
        "ok: ",
        "--parentheses",
        "--braces",
        "Ada",
    ])
    captured = capsys.readouterr()
    outcome["stdout"] = captured.out
    outcome["stderr"] = captured.err


@when("nmg-smoke Ada runs without --quotes")
def invoke_without_quotes(
    outcome: dict[str, int | str], capsys: pytest.CaptureFixture[str]
) -> None:
    outcome["code"] = main(["Ada"])
    captured = capsys.readouterr()
    outcome["stdout"] = captured.out
    outcome["stderr"] = captured.err


@then("the process exits 0")
def process_succeeds(outcome: dict[str, int | str]) -> None:
    assert outcome["code"] == 0


@then(
    "stdout is exactly double-quote open-brace open-parenthesis ok-colon-space "
    "HELLO-comma-space-ADA close-parenthesis close-brace double-quote followed "
    "by one newline"
)
def quoted_stdout_is_exact(outcome: dict[str, int | str]) -> None:
    assert outcome["stdout"] == '"{(ok: HELLO, ADA)}"\n'


@then("stdout is exactly Hello-comma-space-Ada followed by one newline")
def default_stdout_is_exact(outcome: dict[str, int | str]) -> None:
    assert outcome["stdout"] == "Hello, Ada\n"


@then("stderr is empty")
def stderr_is_empty(outcome: dict[str, int | str]) -> None:
    assert outcome["stderr"] == ""
