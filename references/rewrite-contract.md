# Python SDLC Smoke Host Repository Rewrite Contract

**Release**: 3.14.0
**Runtime**: Python 3.12+
**Exception**: `repository-rewrite`
**Issue**: #35

This owner-approved cutover replaces copied Oh My Pi plugin files with the `nmg-sdlc-smoke-python` distribution. The implementation PR uses `SDLC-Exception: repository-rewrite` because the pre-cutover plugin files predate this host's singular issue/spec workflow. Ordinary delivery continues to use `specs/{N}-{slug}/`; Git history archives removed behavior.

## Capabilities

### Greeting library

`nmg_sdlc_smoke.greet("Ada")` returns exactly `Hello, Ada`. Blank, whitespace-only, and non-string values raise `ValueError("name must not be blank")`.

Sources: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`.
Verification: `tests/test_greet.py`, `tests/features/`.

### `nmg-smoke` console script

The installed `nmg-smoke <name>` entry point prints one greeting plus LF and exits 0. Invalid blank input exits 1 without a stdout greeting.

Sources: `src/nmg_sdlc_smoke/cli.py`, `pyproject.toml`.
Verification: `tests/test_cli.py`, `tests/features/`.

### Python verification

pytest covers library and CLI behavior; pytest-bdd provides one independent scenario per AC1–AC7; Ruff checks `src/` and `tests/`; Python CI runs these checks on Python 3.12 for pull requests and pushes to `main`.

Sources: `tests/`, `.github/workflows/python-ci.yml`.
Verification: `python -m pytest`, `python -m pytest tests/features`, `python -m ruff check .`.

## Preserved delivery contracts

The rewrite preserves LICENSE, released CHANGELOG history, 3.x VERSION authority, the managed contribution gate and issue form, CONTRIBUTING evidence rules, AGENTS spec-context markers, and the singular approved spec for issue #35.
