import os
import subprocess
import sysconfig
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

scenarios("../add_nmg_smoke_lowercase_flag.feature")

SCRIPTS = Path(sysconfig.get_path("scripts"))
NMG_SMOKE = SCRIPTS / "nmg-smoke"
if not NMG_SMOKE.exists():
    NMG_SMOKE = SCRIPTS / "nmg-smoke.exe"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(NMG_SMOKE), *args],
        check=False,
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


@given("the installed nmg-smoke console script", target_fixture="runs")
def cli_runs() -> list[subprocess.CompletedProcess[str]]:
    return []


@when("nmg-smoke --lowercase Ada runs")
def invoke_lowercase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--lowercase", "Ada"))


@when(
    "nmg-smoke --lowercase --prefix OK-colon-space --parentheses "
    "--repeat 2 --no-newline ADA runs"
)
def invoke_composed(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(
        _run(
            "--lowercase",
            "--prefix",
            "OK: ",
            "--parentheses",
            "--repeat",
            "2",
            "--no-newline",
            "ADA",
        )
    )


@when("nmg-smoke --lowercase runs with ÅSA and with Straße")
def invoke_non_ascii(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--lowercase", "ÅSA"))
    runs.append(_run("--lowercase", "Straße"))


@when(
    "nmg-smoke runs with --uppercase --lowercase Ada "
    "and with --lowercase --uppercase Ada"
)
def invoke_both_cases(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--uppercase", "--lowercase", "Ada"))
    runs.append(_run("--lowercase", "--uppercase", "Ada"))


@when("nmg-smoke --lowercase runs with a single-space name")
def invoke_blank(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--lowercase", " "))


@when("nmg-smoke runs with Ada, with --uppercase Ada, and with --help")
def invoke_preserved(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("Ada"))
    runs.append(_run("--uppercase", "Ada"))
    runs.append(_run("--help"))


@then("the process exits 0")
def process_exits_0(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.returncode for run in runs] == [0]


@then("the process exits 1")
def process_exits_1(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.returncode for run in runs] == [1]


@then("every process exits 0")
def every_process_exits_0(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs
    assert all(run.returncode == 0 for run in runs)


@then("every process exits 2")
def every_process_exits_2(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs
    assert all(run.returncode == 2 for run in runs)


@then("stdout is exactly hello-comma-space-ada followed by one newline")
def lowercase_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == "hello, ada\n"


@then(
    "stdout is exactly two parenthesized OK-colon-space hello-comma-space-ada "
    "greetings separated by one newline with no final newline"
)
def composed_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == "(OK: hello, ada)\n(OK: hello, ada)"


@then(
    "the stdouts are exactly hello, åsa and hello, straße respectively, "
    "each followed by one newline"
)
def non_ascii_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs] == ["hello, åsa\n", "hello, straße\n"]


@then("every stderr contains not allowed with argument")
def every_stderr_not_allowed(
    runs: list[subprocess.CompletedProcess[str]],
) -> None:
    assert all("not allowed with argument" in run.stderr for run in runs)


@then("every stdout is empty")
def every_stdout_empty(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert all(run.stdout == "" for run in runs)


@then("stderr contains nmg-smoke: error: name must not be blank")
def stderr_blank_error(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert "nmg-smoke: error: name must not be blank" in runs[0].stderr


@then("stdout is empty")
def stdout_empty(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == ""


@then("stderr is empty")
def stderr_empty(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stderr == ""


@then(
    "the first two stdouts are exactly Hello, Ada and HELLO, ADA, "
    "each followed by one newline"
)
def preserved_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs[:2]] == ["Hello, Ada\n", "HELLO, ADA\n"]


@then("the help stdout lists --lowercase")
def help_lists_lowercase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert "--lowercase" in runs[2].stdout
