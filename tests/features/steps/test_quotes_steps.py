import subprocess
import sysconfig
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

scenarios("../add_nmg_smoke_quotes_flag.feature")

SCRIPTS = Path(sysconfig.get_path("scripts"))
NMG_SMOKE = SCRIPTS / "nmg-smoke"
if not NMG_SMOKE.exists():
    NMG_SMOKE = SCRIPTS / "nmg-smoke.exe"


@given("the installed nmg-smoke console script and a valid name", target_fixture="outcome")
def cli_outcome() -> dict[str, int | str]:
    return {}


@when(
    "nmg-smoke --quotes --uppercase --prefix ok-colon-space --parentheses "
    "--braces --repeat 2 Ada runs"
)
def invoke_with_quotes(outcome: dict[str, int | str]) -> None:
    completed = subprocess.run(
        [
            str(NMG_SMOKE),
            "--quotes",
            "--uppercase",
            "--prefix",
            "ok: ",
            "--parentheses",
            "--braces",
            "--repeat",
            "2",
            "Ada",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    outcome["code"] = completed.returncode
    outcome["stdout"] = completed.stdout
    outcome["stderr"] = completed.stderr


@when("nmg-smoke Ada runs without --quotes")
def invoke_without_quotes(outcome: dict[str, int | str]) -> None:
    completed = subprocess.run(
        [str(NMG_SMOKE), "Ada"],
        check=False,
        capture_output=True,
        text=True,
    )
    outcome["code"] = completed.returncode
    outcome["stdout"] = completed.stdout
    outcome["stderr"] = completed.stderr


@then("the process exits 0")
def process_succeeds(outcome: dict[str, int | str]) -> None:
    assert outcome["code"] == 0


@then(
    "stdout is exactly two individually double-quoted open-brace "
    "open-parenthesis ok-colon-space HELLO-comma-space-ADA close-parenthesis "
    "close-brace greetings, each followed by one newline"
)
def quoted_stdout_is_exact(outcome: dict[str, int | str]) -> None:
    assert outcome["stdout"] == '"{(ok: HELLO, ADA)}"\n"{(ok: HELLO, ADA)}"\n'


@then("stdout is exactly Hello-comma-space-Ada followed by one newline")
def default_stdout_is_exact(outcome: dict[str, int | str]) -> None:
    assert outcome["stdout"] == "Hello, Ada\n"


@then("stderr is empty")
def stderr_is_empty(outcome: dict[str, int | str]) -> None:
    assert outcome["stderr"] == ""
