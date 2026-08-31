# Python SDLC Smoke Host Rewrite Verification

**Release**: 3.14.0
**Verified**: 2026-08-31
**Exception**: `repository-rewrite`
**Issue**: #35

## Scope

The working tree is an installable Python 3.12+ distribution with `greet`, the `nmg-smoke` console script, pytest unit coverage, pytest-bdd acceptance coverage, Ruff, and Python GitHub Actions CI. Copied plugin runtime remains available only in Git history.

## Verification commands

- `python -m pytest` — passed: 19 tests.
- `python -m pytest tests/features` — passed: 7 AC1–AC7 pytest-bdd scenarios.
- `python -m ruff check .` — passed.

## Changed-path mapping

- Packaging and runtime: `package.json` removal, `VERSION`, `pyproject.toml`, `src/`.
- Verification: `tests/`, `.github/workflows/python-ci.yml`, removal of the three Node plugin workflows.
- Current product guidance: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `steering/`.
- Rewrite evidence: `.github/workflows/nmg-sdlc-contribution-gate.yml`, `references/rewrite-contract.json`, `references/rewrite-contract.md`, `references/rewrite-verification.md`.
- Current executable contract: `specs/35-convert-smoke-repository-to-a-python-sdlc-host/`.

The implementation PR title and body provide the required `feat!:` title, issue identity, steering alignment, repository-rewrite rationale, exact path evidence, and command outcomes.
