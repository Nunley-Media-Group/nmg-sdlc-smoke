import os
import subprocess
import sysconfig
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

scenarios("../add_nmg_smoke_swapcase_flag.feature")

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


@when("nmg-smoke --swapcase Ada runs")
def invoke_swapcase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--swapcase", "Ada"))


@when(
    "nmg-smoke --swapcase --prefix OK-colon-space --parentheses "
    "--repeat 2 --no-newline ADA runs"
)
def invoke_composed(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(
        _run(
            "--swapcase",
            "--prefix",
            "OK: ",
            "--parentheses",
            "--repeat",
            "2",
            "--no-newline",
            "ADA",
        )
    )


@when("nmg-smoke --swapcase runs with ÅSA and with Straße")
def invoke_non_ascii(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--swapcase", "ÅSA"))
    runs.append(_run("--swapcase", "Straße"))


@when(
    "nmg-smoke runs with --swapcase --uppercase Ada, "
    "--uppercase --swapcase Ada, --swapcase --lowercase Ada, "
    "and --lowercase --swapcase Ada"
)
def invoke_combined_cases(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--swapcase", "--uppercase", "Ada"))
    runs.append(_run("--uppercase", "--swapcase", "Ada"))
    runs.append(_run("--swapcase", "--lowercase", "Ada"))
    runs.append(_run("--lowercase", "--swapcase", "Ada"))


@when("nmg-smoke --swapcase runs with a single-space name")
def invoke_blank(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--swapcase", " "))


@when(
    "nmg-smoke runs with Ada, with --uppercase Ada, with --lowercase Ada, "
    "and with --help"
)
def invoke_preserved(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("Ada"))
    runs.append(_run("--uppercase", "Ada"))
    runs.append(_run("--lowercase", "Ada"))
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


@then("stdout is exactly hELLO-comma-space-aDA followed by one newline")
def swapcase_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == "hELLO, aDA\n"


@then(
    "stdout is exactly two parenthesized OK-colon-space hELLO-comma-space-ada "
    "greetings separated by one newline with no final newline"
)
def composed_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == "(OK: hELLO, ada)\n(OK: hELLO, ada)"


@then(
    "the stdouts are exactly hELLO, åsa and hELLO, sTRASSE respectively, "
    "each followed by one newline"
)
def non_ascii_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs] == ["hELLO, åsa\n", "hELLO, sTRASSE\n"]


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
    "the first three stdouts are exactly Hello, Ada, HELLO, ADA, and hello, ada, "
    "each followed by one newline"
)
def preserved_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs[:3]] == [
        "Hello, Ada\n",
        "HELLO, ADA\n",
        "hello, ada\n",
    ]


@then("the help stdout lists --swapcase")
def help_lists_swapcase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert "--swapcase" in runs[3].stdout
