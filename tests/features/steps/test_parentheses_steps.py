import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke.cli import main

scenarios("../add_nmg_smoke_parentheses_flag.feature")


@given("the smoke CLI is available", target_fixture="outcomes")
def cli_outcomes() -> list[tuple[int, str, str]]:
    return []


@when(
    "nmg-smoke --parentheses --uppercase --prefix 'ok: ' "
    "--repeat 2 --no-newline Ada is run"
)
def invoke_parentheses(
    outcomes: list[tuple[int, str, str]], capsys: pytest.CaptureFixture[str]
) -> None:
    code = main([
        "--parentheses", "--uppercase", "--prefix", "ok: ",
        "--repeat", "2", "--no-newline", "Ada",
    ])
    captured = capsys.readouterr()
    outcomes.append((code, captured.out, captured.err))


@when(
    "nmg-smoke --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada "
    "and nmg-smoke Ada are run without parentheses"
)
def invoke_without_parentheses(
    outcomes: list[tuple[int, str, str]], capsys: pytest.CaptureFixture[str]
) -> None:
    for argv in (
        ["--uppercase", "--prefix", "ok: ", "--repeat", "2", "--no-newline", "Ada"],
        ["Ada"],
    ):
        code = main(argv)
        captured = capsys.readouterr()
        outcomes.append((code, captured.out, captured.err))


@then("the process exits 0 with empty stderr")
@then("both processes exit 0 with empty stderr")
def successful_processes(outcomes: list[tuple[int, str, str]]) -> None:
    for code, _, stderr in outcomes:
        assert code == 0
        assert stderr == ""


@then(
    r'stdout is exactly "(ok: HELLO, ADA)\n(ok: HELLO, ADA)" '
    r"with each \n denoting one LF and no final LF"
)
def wrapped_output(outcomes: list[tuple[int, str, str]]) -> None:
    assert [stdout for _, stdout, _ in outcomes] == [
        "(ok: HELLO, ADA)\n(ok: HELLO, ADA)"
    ]


@then(
    r'their stdout is respectively "ok: HELLO, ADA\nok: HELLO, ADA" '
    r'and "Hello, Ada\n" with each \n denoting one LF'
)
def unchanged_output(outcomes: list[tuple[int, str, str]]) -> None:
    assert [stdout for _, stdout, _ in outcomes] == [
        "ok: HELLO, ADA\nok: HELLO, ADA", "Hello, Ada\n"
    ]
