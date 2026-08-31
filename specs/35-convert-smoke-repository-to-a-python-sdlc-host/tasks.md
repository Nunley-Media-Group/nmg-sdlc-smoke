# Tasks: Convert smoke repository to a Python SDLC host

**Issue**: #35
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Setup | 2 | [ ] |
| Library and CLI | 2 | [ ] |
| Verification | 3 | [ ] |
| Cutover | 4 | [ ] |
| **Total** | 11 | |

---

## Phase 1: Setup

### T001: Add Python packaging and VERSION 3.14.0

**File(s)**: `pyproject.toml`, `VERSION`, `.gitignore`
**Type**: Create | Modify
**Depends**: None
**Acceptance**:
- [ ] `VERSION` bytes are UTF-8 `3.14.0` plus one LF
- [ ] `pyproject.toml` matches the Packaging section in `design.md` (distribution `nmg-sdlc-smoke-python`, `requires-python = ">=3.12"`, setuptools src layout, console script `nmg-smoke`, dynamic version from `VERSION`, extras `dev` with pytest, pytest-bdd, ruff)
- [ ] `.gitignore` includes `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.ruff_cache/`, `*.egg-info/`, `dist/`, `build/`, `.venv/`, `.omp/sdlc/` and does not require Node `node_modules/`

### T002: Create import package skeleton

**File(s)**: `src/nmg_sdlc_smoke/__init__.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Package `nmg_sdlc_smoke` is importable after `python -m pip install -e ".[dev]"`
- [ ] `__init__.py` re-exports `greet` once T003 lands

---

## Phase 2: Library and CLI

### T003: Implement greet

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Create | Modify
**Depends**: T002
**Acceptance**:
- [ ] `greet("Ada")` returns exactly `Hello, Ada`
- [ ] blank `""`, whitespace-only (spaces/tabs/newlines), and non-str raise `ValueError("name must not be blank")`

### T004: Implement nmg-smoke CLI

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Create
**Depends**: T003
**Acceptance**:
- [ ] `nmg-smoke Ada` exits 0 and prints `Hello, Ada` plus one newline to stdout
- [ ] blank or whitespace-only name exits 1 and prints no greeting to stdout
- [ ] `main` is the console-script target `nmg_sdlc_smoke.cli:main`

---

## Phase 3: Verification

### T005: Unit tests

**File(s)**: `tests/test_greet.py`, `tests/test_cli.py`
**Type**: Create
**Depends**: T004
**Acceptance**:
- [ ] Unit tests cover AC1–AC3 library and CLI behavior
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0
- [ ] Tests use no machine-specific absolute paths

### T006: pytest-bdd feature and steps

**File(s)**: `tests/features/convert_smoke_repository_to_a_python_sdlc_host.feature`, `tests/features/steps/test_greeting_steps.py`
**Type**: Create
**Depends**: T005
**Acceptance**:
- [ ] Feature file contains one scenario per AC1–AC7 with tags `@SCN001`–`@SCN007`
- [ ] `python -m pytest tests/features` exits 0
- [ ] Scenarios are independent and path-agnostic

### T007: Python CI and Ruff; remove Node plugin workflows

**File(s)**: `.github/workflows/python-ci.yml`; delete `.github/workflows/nmg-sdlc-verify.yml`, `.github/workflows/skill-inventory-audit.yml`, `.github/workflows/sync-marketplace-pointer.yml`
**Type**: Create | Delete
**Depends**: T006
**Acceptance**:
- [ ] `python-ci.yml` triggers on `pull_request` and `push` to `main`
- [ ] Job uses Python 3.12, `python -m pip install -e ".[dev]"`, `python -m pytest`, `python -m pytest tests/features`, `python -m ruff check .`
- [ ] The three named Node plugin workflows are absent
- [ ] `python -m ruff check .` exits 0 locally

---

## Phase 4: Cutover

### T008: Remove copied plugin runtime

**File(s)**: `workflows/`, `agents/`, `commands/`, `scripts/`, `package.json`, `src/extension.ts`, `src/sdlc-commands.mjs`, `src/sdlc-workflows.mjs`, plugin `specs/` except `specs/35-convert-smoke-repository-to-a-python-sdlc-host/`, plugin `references/` except rewrite-contract trio, live smoke markers listed in design.md, `EXECUTE_SMOKE.md`
**Type**: Delete
**Depends**: T007
**Acceptance**:
- [ ] Listed plugin runtime paths are absent
- [ ] `specs/35-convert-smoke-repository-to-a-python-sdlc-host/` remains with singular `**Issue**: #35`
- [ ] `LICENSE` is unchanged
- [ ] CHANGELOG released headings remain
- [ ] `.github/ISSUE_TEMPLATE/nmg-sdlc-ready-issue.yml` remains

### T009: Rewrite current-product docs and steering

**File(s)**: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `steering/manifest.json`, `steering/modules/product.mjs`, `steering/modules/tech.mjs`, `steering/modules/structure.mjs`, `steering/modules/verification.mjs`, `steering/snippets/project-product.md`, `steering/snippets/project-tech.md`, `steering/snippets/project-structure.md`, `steering/retrospective.md`, `steering/retrospective-state.json`; delete `steering/product.md`, `steering/tech.md`, `steering/structure.md`
**Type**: Create | Modify | Delete
**Depends**: T008
**Acceptance**:
- [ ] README, CONTRIBUTING, AGENTS, and steering snippets describe this Python SDLC smoke host (src layout, pytest, pytest-bdd, Ruff, VERSION synchronized with pyproject.toml)
- [ ] They do not describe an Oh My Pi plugin as the current product
- [ ] CONTRIBUTING keeps the managed contribution-workflow contract (evidence graph and exception table)
- [ ] AGENTS.md keeps `<!-- nmg-sdlc-managed: spec-context -->` / `<!-- /nmg-sdlc-managed -->` and the spec-context rules
- [ ] `steering/manifest.json` registers product, tech, structure, and verification modules plus the three project snippets
- [ ] `steering/product.md`, `steering/tech.md`, and `steering/structure.md` are absent
- [ ] `steering/retrospective-state.json` is `{"version": 1, "specs": {}}`

### T010: Rewrite rewrite-contract artifacts and comment the contribution gate

**File(s)**: `references/rewrite-contract.json`, `references/rewrite-contract.md`, `references/rewrite-verification.md`, `.github/workflows/nmg-sdlc-contribution-gate.yml`
**Type**: Modify
**Depends**: T009
**Acceptance**:
- [ ] Rewrite-contract files document this Python host cutover and keep `exception: repository-rewrite`
- [ ] `rewrite-verification.md` records pytest, pytest-bdd, and Ruff commands as verification
- [ ] Contribution gate file still starts with `# nmg-sdlc-managed: contribution-gate` and `# nmg-sdlc-managed-version: 7` and keeps version-7 `rewriteRequiredPaths` and `steeringFiles` (manifest plus `steering/modules/{product,tech,structure,verification}.mjs`)
- [ ] The gate file has the comment-only line `# This repository is a Python SDLC smoke consumer.` immediately after the version marker so the path appears in the implementation PR changed-path list
- [ ] The evaluator is not restored to version 6 and does not require markdown `steering/product.md`, `steering/tech.md`, or `steering/structure.md`

### T011: Implementation PR evidence

**File(s)**: implementation PR title and body (no extra repo file required)
**Type**: Modify
**Depends**: T010
**Acceptance**:
- [ ] Title is exactly `feat!: convert smoke repository to a Python SDLC host`
- [ ] Body contains `Closes #35`, `**Issue**: #35`, and `SDLC-Exception: repository-rewrite — Pre-cutover plugin files predate this host's singular issue/spec workflow.`
- [ ] PR changed paths include `package.json`, `VERSION`, `README.md`, `CONTRIBUTING.md`, `steering/manifest.json`, `steering/modules/product.mjs`, `steering/modules/tech.mjs`, `steering/modules/structure.mjs`, `.github/workflows/nmg-sdlc-contribution-gate.yml`, `steering/modules/verification.mjs`, `references/rewrite-contract.json`, `references/rewrite-contract.md`, `references/rewrite-verification.md`

---

## Dependency Graph

```
T001 ──▶ T002 ──▶ T003 ──▶ T004 ──▶ T005 ──▶ T006 ──▶ T007 ──▶ T008 ──▶ T009 ──▶ T010 ──▶ T011
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #35 | 2026-08-31 | Initial feature spec |
| #35 | 2026-08-31 | Spec revised before delivery |

---

## Validation Checklist

Before moving to IMPLEMENT phase:

- [x] Each task has single responsibility
- [x] Dependencies are correctly mapped
- [x] Tasks can be completed independently (given dependencies)
- [x] Acceptance criteria are verifiable
- [x] File paths reference the post-cutover Python layout
- [x] Test tasks are included for each layer
- [x] No circular dependencies
- [x] Tasks are in logical execution order
