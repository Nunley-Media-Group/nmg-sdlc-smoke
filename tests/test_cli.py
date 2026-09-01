import pytest

from nmg_sdlc_smoke.cli import main


def test_cli_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["Ada"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, Ada\n"
    assert captured.err == ""


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
