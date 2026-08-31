# Requirements: Convert smoke repository to a Python SDLC host

**Issue**: #35
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** nmg-sdlc operator exercising the toolkit against a disposable host repository
**I want** this repository converted from copied Node.js plugin contents into a minimal production-shaped Python project
**So that** the complete nmg-sdlc issue → spec → execute workflow can be run against a deterministic, cross-platform, independently verifiable Python host

---

## Background

This repository is a disposable smoke host currently filled with a copy of the nmg-sdlc Oh My Pi plugin. That plugin surface cannot exercise nmg-sdlc as a Python consumer: there is no pyproject.toml, no installable Python package, and verification is Node/Jest/plugin-contract based. A clean cutover is required so later issues implement real Python behavior through the normal SDLC path.

The converted host is not a growing product. It must be production-shaped enough to install, test, lint, and run in CI, then stay out of the way of future issue delivery.

VERSION is currently `3.13.0`. This issue is an `enhancement` on the 3.x line. Implementation sets `VERSION` to `3.14.0` (minor) so the managed repository-rewrite exception sees `VERSION` among changed paths, and synchronizes `pyproject.toml` from `VERSION`.

The implementation pull request is a working-tree rewrite and must use `feat!:` plus `SDLC-Exception: repository-rewrite — Pre-cutover plugin files predate this host's singular issue/spec workflow.` Do not put `BREAKING` in the issue or spec title or body, and do not declare `**Version bump**: major`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Installable greeting happy path

**Given** the repository is an installable Python distribution `nmg-sdlc-smoke-python` with import package `nmg_sdlc_smoke` requiring Python 3.12+
**When** a caller invokes `greet("Ada")`
**Then** the function returns exactly `Hello, Ada`

### AC2: Console script happy path

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Blank name is rejected

**Given** a blank or whitespace-only name
**When** `greet` is called or `nmg-smoke` is invoked with that name
**Then** the library raises `ValueError` and the CLI exits non-zero without printing a greeting

### AC4: Independent Python verification

**Given** a clean checkout on macOS, Linux, or Windows
**When** pytest, pytest-bdd features under `tests/features/`, and Ruff are run
**Then** every acceptance criterion has a Gherkin scenario, those commands exit 0, and results do not depend on machine-specific paths

### AC5: Python CI replaces plugin verification

**Given** a pull request or a push to `main`
**When** GitHub Actions Python CI runs on Python 3.12
**Then** it installs the project, runs pytest (including `tests/features/`), and runs Ruff, and the Node plugin workflows `nmg-sdlc-verify.yml`, `skill-inventory-audit.yml`, and `sync-marketplace-pointer.yml` are absent

### AC6: Clean cutover preserves SDLC delivery contracts

**Given** the converted working tree
**When** it is inspected
**Then** copied plugin runtime (`workflows/`, `agents/`, `commands/`, Node `scripts/`, OMP `package.json` / `src/extension.ts`, plugin `specs/` other than `specs/35-convert-smoke-repository-to-a-python-sdlc-host/`, live smoke marker files) is gone, and LICENSE, 3.x `VERSION` (synced to `pyproject.toml`), CHANGELOG history, the managed contribution gate, the managed issue form, and the AGENTS.md spec-context markers remain

### AC7: Python-focused steering and contribution guidance

**Given** a contributor opening README, CONTRIBUTING, AGENTS, and steering
**When** they read current guidance
**Then** the documents describe this Python SDLC smoke host (src layout, pytest, pytest-bdd, Ruff, VERSION synchronized with pyproject.toml) and do not describe an Oh My Pi plugin as the current product

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Ship `pyproject.toml` plus `src/nmg_sdlc_smoke` layout for distribution `nmg-sdlc-smoke-python` on Python 3.12+ | Must | setuptools; version from `VERSION` |
| FR2 | Expose `greet(name: str) -> str` returning `Hello, {name}` and raising `ValueError("name must not be blank")` on blank, whitespace-only, or non-str input | Must | |
| FR3 | Provide console script `nmg-smoke` with the same greeting behavior | Must | stdout greeting+LF on success; no stdout greeting and exit 1 on ValueError |
| FR4 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR5 | Gate the tree with Ruff and with GitHub Actions Python CI on pull requests and `main` | Must | Python 3.12 |
| FR6 | Keep `VERSION` as the 3.x source of truth, set it to `3.14.0`, and synchronize `pyproject.toml` from it | Must | enhancement → minor; not 0.x or 1.0.0 |
| FR7 | Remove copied plugin/runtime artifacts from the working tree; keep Git history as the archive | Must | Retain only `specs/35-convert-smoke-repository-to-a-python-sdlc-host/` under `specs/` |
| FR8 | Preserve LICENSE, CHANGELOG history, managed contribution gate, managed issue form, and AGENTS.md spec-context markers | Must | Contribution gate evaluator stays version 6 |
| FR9 | Rewrite steering, README, CONTRIBUTING (keeping the managed contribution-workflow contract), and AGENTS project overview for the Python host | Must | |
| FR10 | Use UTF-8 text and path-agnostic commands so verification is cross-platform | Should | |
| FR11 | Satisfy the managed `SDLC-Exception: repository-rewrite` path on the implementation PR | Must | `feat!:` title; all rewrite-required paths changed |

---

## Out of Scope

- Publishing the distribution to PyPI
- Adding type checkers, coverage quotas, or extra frameworks not named above
- Remaining an Oh My Pi / nmg-sdlc plugin
- Changing LICENSE, GitHub ownership, or the v3 VERSION line to 0.x or 1.0.0
- Authoring follow-on exercise issues beyond this cutover
- Keeping copied plugin specs, workflows, agents, commands, or Node contract scripts in the working tree
- Declaring a major version bump or putting `BREAKING` in this spec

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #35 | 2026-08-31 | Initial feature spec |
