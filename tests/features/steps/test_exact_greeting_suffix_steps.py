import pytest
from pytest_bdd import given, scenarios, then, when

from nmg_sdlc_smoke.cli import main

scenarios("../exact_greeting_suffix.feature")


@given("a valid name and an exact mixed-case suffix", target_fixture="suffix_args")
def suffix_args() -> list[str]:
    return ["Ada", "--suffix", " dOnE \t"]


@when(
    "the CLI combines suffix with uppercase prefix repetition and no-newline",
    target_fixture="rendered",
)
def render_suffix(
    suffix_args: list[str], capsys: pytest.CaptureFixture[str]
) -> dict[bool, str]:
    outputs = {}
    for no_newline in (False, True):
        args = suffix_args + ["--uppercase", "--prefix", "ok: ", "--repeat", "2"]
        if no_newline:
            args.append("--no-newline")
        assert main(args) == 0
        captured = capsys.readouterr()
        assert captured.err == ""
        outputs[no_newline] = captured.out
    return outputs


@then("each completed greeting has the verbatim suffix")
def exact_suffix(rendered: dict[bool, str]) -> None:
    assert rendered[True].split("\n") == ["ok: HELLO, ADA dOnE \t"] * 2


@then("repetition separators and final-newline behavior are preserved")
def newline_semantics(rendered: dict[bool, str]) -> None:
    expected = "ok: HELLO, ADA dOnE \t\nok: HELLO, ADA dOnE \t"
    assert rendered == {False: expected + "\n", True: expected}


@given(
    "an omitted or empty suffix and an invalid-name case",
    target_fixture="boundary_args",
)
def boundary_args() -> dict[str, list[str]]:
    return {
        "omitted": ["Ada"],
        "empty": ["Ada", "--suffix", ""],
        "blank": ["", "--suffix", " dOnE "],
        "whitespace": [" \t\n", "--suffix", " dOnE "],
        "help": ["--help"],
    }


@when("the CLI is invoked", target_fixture="boundary_results")
def invoke_boundaries(
    boundary_args: dict[str, list[str]], capsys: pytest.CaptureFixture[str]
) -> dict[str, tuple[int, str, str]]:
    results = {}
    for case, args in boundary_args.items():
        try:
            code = main(args)
        except SystemExit as error:
            code = error.code
        captured = capsys.readouterr()
        results[case] = (code, captured.out, captured.err)
    return results


@then("omitted and empty suffix preserve current successful output")
def unchanged_success(boundary_results: dict[str, tuple[int, str, str]]) -> None:
    assert boundary_results["omitted"] == (0, "Hello, Ada\n", "")
    assert boundary_results["empty"] == boundary_results["omitted"]


@then("invalid names exit one without any stdout greeting or suffix")
def unchanged_errors(boundary_results: dict[str, tuple[int, str, str]]) -> None:
    for case in ("blank", "whitespace"):
        code, out, err = boundary_results[case]
        assert code == 1
        assert out == ""
        assert "name must not be blank" in err


@then("help documents the optional suffix")
def suffix_help(boundary_results: dict[str, tuple[int, str, str]]) -> None:
    code, out, err = boundary_results["help"]
    assert code == 0
    assert "--suffix TEXT" in out
    assert err == ""
