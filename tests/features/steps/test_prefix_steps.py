import pytest
from pytest_bdd import scenarios, then, when

from nmg_sdlc_smoke.cli import main

pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]

scenarios("../add_nmg_smoke_prefix_text_option.feature")


@when("nmg-smoke --prefix 'OK: ' Ada is run")
def invoke_prefixed_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--prefix", "OK: ", "Ada"])
    context["captured"] = capsys.readouterr()


@then("the process exits 0 and prints OK: Hello, Ada followed by a single newline")
def exact_prefixed_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "OK: Hello, Ada\n"
    assert captured.err == ""


@then("nmg-smoke Ada --prefix 'OK: ' produces the same stdout and exit code")
def prefix_after_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["Ada", "--prefix", "OK: "]) == context["exit_code"]
    captured = capsys.readouterr()
    assert captured.out == "OK: Hello, Ada\n"
    assert captured.err == ""


@when("nmg-smoke --prefix is run without a TEXT argument")
def invoke_prefix_without_text(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--prefix"])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@then("the process exits non-zero")
def nonzero_exit(context: dict[str, object]) -> None:
    assert context["exit_code"] != 0


@then("stdout contains no greeting")
def stdout_has_no_greeting(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert captured.out == ""


@then("stderr contains argparse-style usage or error text")
def argparse_error_on_stderr(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert "usage:" in captured.err or "error:" in captured.err


@when("nmg-smoke --prefix 'OK: ' is invoked with that name")
def invoke_prefix_with_blank_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--prefix", "OK: ", str(context["blank_name"])])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@when("nmg-smoke --prefix 'OK: ' is run with no name argument")
def invoke_prefix_without_name(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--prefix", "OK: "])
    context["exit_code"] = exit_info.value.code
    context["captured"] = capsys.readouterr()


@when("nmg-smoke --prefix 'ok: ' --uppercase Ada is run")
def invoke_prefixed_uppercase_cli(
    context: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    context["exit_code"] = main(["--prefix", "ok: ", "--uppercase", "Ada"])
    captured = capsys.readouterr()
    context["captured"] = captured
    context["uppercase_stdout"] = captured.out


@then("the process exits 0 and prints ok: HELLO, ADA followed by a single newline")
def exact_prefixed_uppercase_output(context: dict[str, object]) -> None:
    captured = context["captured"]
    assert isinstance(captured, tuple)
    assert context["exit_code"] == 0
    assert captured.out == "ok: HELLO, ADA\n"
    assert captured.err == ""


@then("when nmg-smoke --prefix 'OK: ' --repeat 2 Ada is run, stdout is exactly two lines of OK: Hello, Ada, each followed by a newline")
def prefix_each_repeated_line(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--prefix", "OK: ", "--repeat", "2", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "OK: Hello, Ada\nOK: Hello, Ada\n"
    assert captured.err == ""


@then("the supplied TEXT is not itself uppercased")
def prefix_is_not_uppercased(context: dict[str, object]) -> None:
    uppercase_stdout = context["uppercase_stdout"]
    assert isinstance(uppercase_stdout, str)
    assert uppercase_stdout.startswith("ok: ")
