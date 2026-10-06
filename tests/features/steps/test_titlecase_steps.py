import os
import subprocess
import sysconfig
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

scenarios("../add_nmg_smoke_titlecase_flag.feature")

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


@when("nmg-smoke --titlecase ada runs")
def invoke_titlecase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--titlecase", "ada"))


@when("nmg-smoke --titlecase runs with ADA LOVELACE, with o'neil, and with åsa")
def invoke_title_semantics(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--titlecase", "ADA LOVELACE"))
    runs.append(_run("--titlecase", "o'neil"))
    runs.append(_run("--titlecase", "åsa"))


@when(
    "nmg-smoke --titlecase --prefix ok-colon-space --quotes "
    "--repeat 2 --no-newline ADA runs"
)
def invoke_composed(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(
        _run(
            "--titlecase",
            "--prefix",
            "ok: ",
            "--quotes",
            "--repeat",
            "2",
            "--no-newline",
            "ADA",
        )
    )


@when(
    "nmg-smoke runs --titlecase together with --uppercase, --lowercase, "
    "and --swapcase in both argument orders"
)
def invoke_combined_cases(runs: list[subprocess.CompletedProcess[str]]) -> None:
    for other in ("--uppercase", "--lowercase", "--swapcase"):
        runs.append(_run("--titlecase", other, "Ada"))
        runs.append(_run(other, "--titlecase", "Ada"))


@when("nmg-smoke --titlecase runs with a single-space name")
def invoke_blank(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("--titlecase", " "))


@when(
    "nmg-smoke runs with Ada, with --uppercase Ada, with --lowercase Ada, "
    "with --swapcase Ada, and with --help"
)
def invoke_preserved(runs: list[subprocess.CompletedProcess[str]]) -> None:
    runs.append(_run("Ada"))
    runs.append(_run("--uppercase", "Ada"))
    runs.append(_run("--lowercase", "Ada"))
    runs.append(_run("--swapcase", "Ada"))
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
    assert len(runs) == 6
    assert all(run.returncode == 2 for run in runs)


@then("stdout is exactly Hello-comma-space-Ada followed by one newline")
def titlecase_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == "Hello, Ada\n"


@then(
    "the stdouts are exactly Hello, Ada Lovelace and Hello, O'Neil and "
    "Hello, Åsa respectively, each followed by one newline"
)
def title_semantics_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs] == [
        "Hello, Ada Lovelace\n",
        "Hello, O'Neil\n",
        "Hello, Åsa\n",
    ]


@then(
    "stdout is exactly two double-quoted ok-colon-space Hello-comma-space-Ada "
    "greetings separated by one newline with no final newline"
)
def composed_stdout(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert runs[0].stdout == '"ok: Hello, Ada"\n"ok: Hello, Ada"'


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
    "the first four stdouts are exactly Hello, Ada and HELLO, ADA and "
    "hello, ada and hELLO, aDA, each followed by one newline"
)
def preserved_stdouts(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert [run.stdout for run in runs[:4]] == [
        "Hello, Ada\n",
        "HELLO, ADA\n",
        "hello, ada\n",
        "hELLO, aDA\n",
    ]


@then("the help stdout lists --titlecase")
def help_lists_titlecase(runs: list[subprocess.CompletedProcess[str]]) -> None:
    assert "--titlecase" in runs[4].stdout
