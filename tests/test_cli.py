import pytest

from nmg_sdlc_smoke.cli import main


def test_cli_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\n"
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
