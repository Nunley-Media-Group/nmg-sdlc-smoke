# nmg-sdlc-smoke-python

A disposable Python SDLC smoke host used to exercise issue-to-spec-to-delivery workflows against a small, independently verifiable project.

## Requirements

- Python 3.12 or newer
- `VERSION` is the release source of truth; `pyproject.toml` reads it dynamically

## Install

```console
python -m pip install -e ".[dev]"
```

## Library

```python
from nmg_sdlc_smoke import greet, greeting_length

greet("Ada")  # "Hello, Ada"
greeting_length("Ada")  # 10
```

`greet` rejects blank, whitespace-only, and non-string names with `ValueError("name must not be blank")`.

## CLI

```console
$ nmg-smoke Ada
Hello, Ada
```

Use `--uppercase` to capitalize the complete greeting:

```console
$ nmg-smoke --uppercase Ada
HELLO, ADA
```

Use `--repeat COUNT` to print the greeting once per line:

```console
$ nmg-smoke --repeat 3 Ada
Hello, Ada
Hello, Ada
Hello, Ada
```

Use `--prefix TEXT` to prepend text exactly as supplied:

```console
$ nmg-smoke --prefix 'OK: ' Ada
OK: Hello, Ada
```

A blank name exits 1 and writes no greeting to stdout.

## Verification

```console
python -m pytest
python -m pytest tests/features
python -m ruff check .
```

Unit tests cover the library and CLI. pytest-bdd scenarios under `tests/features/` cover the approved acceptance criteria. Ruff checks `src/` and `tests/`. GitHub Actions runs the same Python checks on pull requests and pushes to `main`.

## Layout

- `src/nmg_sdlc_smoke/` — import package and console entry point
- `tests/` — pytest unit tests
- `tests/features/` — pytest-bdd features and steps
- `specs/` — current approved issue contracts
- `steering/` — product, technology, and structure guidance
- `VERSION` — 3.x version source synchronized into package metadata

This repository is intentionally minimal. Git history, not the working tree, archives the copied plugin that preceded the Python host.
