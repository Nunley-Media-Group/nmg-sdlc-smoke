from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_live_smoke_marker_has_exact_content() -> None:
    marker = ROOT / "LIVE_SMOKE_362_A.txt"

    assert marker.is_file()
    assert marker.read_text(encoding="utf-8") == "LIVE_SMOKE_362_A\n"
