# Product Steering

## Mission

Provide a deterministic Python SDLC smoke host that proves an issue can move through approved BDD specification, implementation, verification, and delivery against a real installable project.

## Users

Maintainers exercising nmg-sdlc against a disposable Python repository.

## Product Contract

- Distribution: `nmg-sdlc-smoke-python`, Python 3.12+.
- Import package: `nmg_sdlc_smoke` in a setuptools `src` layout.
- Behavior: `greet(name)` and the `nmg-smoke` console script.
- Verification: pytest, pytest-bdd, Ruff, and Python GitHub Actions CI.
- Versioning: root `VERSION` is the 3.x source synchronized dynamically with `pyproject.toml`.
- Scope: remain minimal; no database, HTTP API, UI, or publication pipeline.

## Principles

1. Observable contracts over framework complexity.
2. Cross-platform, path-agnostic verification.
3. One current approved issue spec per capability change.
4. Git history archives superseded behavior.
5. No copied Oh My Pi plugin runtime in the current product.

## Success

A clean Python 3.12+ checkout installs with `python -m pip install -e ".[dev]"`; `nmg-smoke Ada` prints exactly `Hello, Ada`; pytest, pytest-bdd, and Ruff all pass.
