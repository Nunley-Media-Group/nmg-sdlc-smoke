import pytest

from nmg_sdlc_smoke.cli import main


def test_cli_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    "argv", [["--no-newline", "Ada"], ["Ada", "--no-newline"]]
)
def test_cli_omits_final_newline(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada"
    assert captured.err == ""


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        ("1", "Hello, Ada"),
        ("3", "Hello, Ada\nHello, Ada\nHello, Ada"),
    ],
)
def test_cli_no_newline_preserves_repeat_separators(
    count: str,
    expected: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--no-newline", "--repeat", count, "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""


def test_cli_no_newline_composes_with_uppercase(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--no-newline", "--uppercase", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "HELLO, ADA"
    assert captured.err == ""


def test_cli_rejects_no_newline_without_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--no-newline"])

    assert exit_info.value.code != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err != ""


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_no_newline(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--no-newline", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


@pytest.mark.parametrize(
    "argv",
    [
        ["--prefix", "OK: ", "Ada"],
        ["Ada", "--prefix", "OK: "],
    ],
)
def test_cli_prefixes_greeting(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "OK: Hello, Ada\n"
    assert captured.err == ""


def test_cli_accepts_empty_prefix(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--prefix", "", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@pytest.mark.parametrize("argv", [["--prefix"], ["--prefix", "OK: "]])
def test_cli_rejects_prefix_without_required_argument(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)

    assert exit_info.value.code != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err != ""
    assert "usage:" in captured.err or "error:" in captured.err


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_prefix(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--prefix", "OK: ", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


def test_cli_prefixes_after_uppercase(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--prefix", "OK: ", "--uppercase", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "OK: HELLO, ADA\n"
    assert captured.err == ""


def test_cli_prefixes_each_repeated_greeting(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--prefix", "OK: ", "--repeat", "2", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "OK: Hello, Ada\nOK: Hello, Ada\n"
    assert captured.err == ""

@pytest.mark.parametrize(
    "argv",
    [
        ["--repeat", "3", "Ada"],
        ["Ada", "--repeat", "3"],
    ],
)
def test_cli_repeats_greeting(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\nHello, Ada\nHello, Ada\n"
    assert captured.err == ""


def test_cli_repeat_one_prints_single_greeting(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--repeat", "1", "Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    "argv",
    [
        ["--repeat"],
        ["--repeat", "abc", "Ada"],
        ["--repeat", "0", "Ada"],
        ["--repeat=-1", "Ada"],
        ["--repeat", "-1", "Ada"],
        ["--repeat", "2"],
    ],
)
def test_cli_rejects_invalid_repeat(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)

    assert exit_info.value.code != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err != ""


@pytest.mark.parametrize(
    "argv", [["--uppercase", "Ada"], ["Ada", "--uppercase"]]
)
def test_cli_prints_uppercase_greeting(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "HELLO, ADA\n"
    assert captured.err == ""


def test_cli_rejects_uppercase_without_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--uppercase"])

    assert exit_info.value.code != 0
    captured = capsys.readouterr()
    assert captured.out == ""


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_uppercase(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--uppercase", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


@pytest.mark.parametrize(
    "argv", [["--lowercase", "Ada"], ["Ada", "--lowercase"]]
)
def test_cli_prints_lowercase_greeting(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "hello, ada\n"
    assert captured.err == ""


def test_cli_lowercase_composes_before_prefix_and_wrappers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    argv = [
        "--lowercase",
        "--prefix",
        "OK: ",
        "--parentheses",
        "--repeat",
        "2",
        "--no-newline",
        "ADA",
    ]
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "(OK: hello, ada)\n(OK: hello, ada)"
    assert captured.err == ""


@pytest.mark.parametrize(
    ("name", "expected"),
    [("ÅSA", "hello, åsa\n"), ("Straße", "hello, straße\n")],
)
def test_cli_lowercase_uses_str_lower_semantics(
    name: str, expected: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["--lowercase", name]) == 0
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["--uppercase", "--lowercase", "Ada"],
        ["--lowercase", "--uppercase", "Ada"],
    ],
)
def test_cli_rejects_uppercase_with_lowercase(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)

    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "not allowed with argument" in captured.err


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_lowercase(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--lowercase", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


def test_cli_help_lists_lowercase(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])

    assert exit_info.value.code == 0
    assert "--lowercase" in capsys.readouterr().out


@pytest.mark.parametrize(
    "argv", [["--swapcase", "Ada"], ["Ada", "--swapcase"]]
)
def test_cli_prints_swapcase_greeting(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "hELLO, aDA\n"
    assert captured.err == ""


def test_cli_swapcase_composes_before_prefix_and_wrappers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    argv = [
        "--swapcase",
        "--prefix",
        "OK: ",
        "--parentheses",
        "--repeat",
        "2",
        "--no-newline",
        "ADA",
    ]
    assert main(argv) == 0
    captured = capsys.readouterr()
    assert captured.out == "(OK: hELLO, ada)\n(OK: hELLO, ada)"
    assert captured.err == ""


@pytest.mark.parametrize(
    ("name", "expected"),
    [("ÅSA", "hELLO, åsa\n"), ("Straße", "hELLO, sTRASSE\n")],
)
def test_cli_swapcase_uses_str_swapcase_semantics(
    name: str, expected: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["--swapcase", name]) == 0
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["--swapcase", "--uppercase", "Ada"],
        ["--uppercase", "--swapcase", "Ada"],
        ["--swapcase", "--lowercase", "Ada"],
        ["--lowercase", "--swapcase", "Ada"],
    ],
)
def test_cli_rejects_swapcase_with_other_case_flag(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)

    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "not allowed with argument" in captured.err


@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_swapcase(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--swapcase", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


def test_cli_help_lists_swapcase(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])

    assert exit_info.value.code == 0
    assert "--swapcase" in capsys.readouterr().out



@pytest.mark.parametrize("name", ["", " ", "\t", "\n"])
def test_cli_rejects_blank_name_with_repeat(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--repeat", "2", name])

    assert exit_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "name must not be blank" in captured.err


def test_cli_parentheses_preserve_literal_multiline_content(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--parentheses", "--prefix", "(ok)\n", "Ada (Lovelace)"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "((ok)\nHello, Ada (Lovelace))\n"
    assert captured.err == ""


def test_cli_braces_preserve_literal_multiline_content(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["--braces", "--prefix", "{ok}\n", "Ada {Lovelace}"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "{{ok}\nHello, Ada {Lovelace}}\n"
    assert captured.err == ""


def test_cli_quotes_fully_composed_greeting(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([
        "--quotes",
        "--uppercase",
        "--prefix",
        "ok: ",
        "--parentheses",
        "--braces",
        "Ada",
    ]) == 0
    captured = capsys.readouterr()
    assert captured.out == '"{(ok: HELLO, ADA)}"\n'
    assert captured.err == ""
