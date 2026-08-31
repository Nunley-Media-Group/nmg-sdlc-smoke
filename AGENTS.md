# AGENTS.md

## Project Overview

`nmg-sdlc-smoke-python` is a minimal Python SDLC smoke host. It is an installable Python 3.12+ distribution with a small greeting library and the `nmg-smoke` console script.

## Repository Structure

```
pyproject.toml                 # setuptools metadata; reads version from VERSION
VERSION                        # 3.x release source of truth
src/nmg_sdlc_smoke/            # library and CLI
 tests/                         # pytest unit tests
 tests/features/                # pytest-bdd acceptance features and steps
specs/                         # current approved issue contracts
steering/                      # product, technology, and structure guidance
.github/workflows/python-ci.yml # Python verification
```

## Engineering Rules

- Support Python 3.12 and newer.
- Keep runtime dependencies at zero unless an approved spec requires otherwise.
- Keep `greet` pure and the CLI adapter thin.
- Use cross-platform paths and UTF-8 text.
- Run `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .`.
- Change `VERSION` for releases; `pyproject.toml` must continue reading it dynamically.
- Update README when user-facing behavior changes.
- Keep CHANGELOG released history intact.

<!-- nmg-sdlc-managed: spec-context -->
## nmg-sdlc Spec Context

For SDLC work, project-root `specs/` is the canonical working-tree BDD archive and contains only current contracts with genuine GitHub issue owners. Specs use directories of the form `specs/{N}-{slug}/` where `N` is the GitHub issue number. Always identify the active spec first (leading directory number must match the issue and every file must declare singular `**Issue**: #N`), then use bounded relevant-spec discovery to load only the neighboring specs that can affect the change. Do not load the full archive by default. Superseded specs remain in Git history. A breaking repository rewrite may document unowned rewrite-only behavior in `references/rewrite-contract.{json,md}` but must not assign it a synthetic issue number or treat it as an executable issue spec. Legacy `.codex/specs/` directories are inputs to `/sdlc-upgrade-project` only.
<!-- /nmg-sdlc-managed -->
