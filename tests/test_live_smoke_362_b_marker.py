from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_live_smoke_362_b_marker_has_exact_content() -> None:
    marker = ROOT / "LIVE_SMOKE_362_B.txt"

    assert marker.is_file()
    assert not marker.is_symlink()
    assert marker.read_bytes() == b"LIVE_SMOKE_362_B\n"
