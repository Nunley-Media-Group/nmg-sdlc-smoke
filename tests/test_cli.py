import importlib.metadata

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
        ["--version"],
        ["--version", "Ada"],
        ["Ada", "--version"],
    ],
)
def test_cli_prints_installed_version(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)

    assert exit_info.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == (
        importlib.metadata.version("nmg-sdlc-smoke-python") + "\n"
    )
    assert "Hello," not in captured.out
    assert captured.err == ""


def test_cli_requires_name_without_version(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([])

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
