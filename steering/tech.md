# Technology Steering

## Runtime and Packaging

- Python 3.12 or newer.
- setuptools with a `src` package layout.
- Distribution `nmg-sdlc-smoke-python`; import package `nmg_sdlc_smoke`.
- Root `VERSION` is the source of truth; `[tool.setuptools.dynamic]` reads it from `pyproject.toml`.
- No runtime dependencies for the greeting library or CLI.

## Code

- Use the standard library and straightforward typed functions.
- `greet(name: str) -> str` is pure. Reject non-string, blank, or whitespace-only values with `ValueError("name must not be blank")`.
- `nmg_sdlc_smoke.cli:main` uses `argparse`, prints one greeting line on success, and returns/exits 1 without stdout greeting on invalid input.
- Keep paths cross-platform with `pathlib`; never embed machine-specific absolute paths.
- Use UTF-8 and one trailing LF for text files, including `VERSION`.

## Verification

Install development dependencies in an isolated environment:

```console
python -m pip install -e ".[dev]"
```

Required checks:

```console
python -m pytest
python -m pytest tests/features
python -m ruff check .
```

Unit tests live in `tests/test_*.py`. Every approved acceptance criterion has an independent pytest-bdd scenario under `tests/features/`. Tests must be deterministic and full-suite safe.

GitHub Actions uses Python 3.12 and runs the same install, pytest, pytest-bdd, and Ruff commands on pull requests and pushes to `main`.

## Release and Compatibility

Keep the project on the 3.x VERSION line unless an approved issue says otherwise. Update `VERSION`, package behavior, public docs, and CHANGELOG together when applicable. Preserve released CHANGELOG headings and LICENSE.
