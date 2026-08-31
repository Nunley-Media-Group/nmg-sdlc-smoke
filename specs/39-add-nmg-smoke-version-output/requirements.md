# Requirements: Add nmg-smoke --version output

**Issue**: #39
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --version` to print the installed package version and exit 0 without a name
**So that** installed version identity is observable independently of the greeting path

---

## Background

The smoke host is an installable Python 3.12+ distribution whose console script currently greets only when a positional name is supplied. Maintainers need a version query that reports the installed package metadata so the running command identifies what is actually installed, without going through the greeting path.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Version flag without a name

**Given** the distribution is installed
**When** `nmg-smoke --version` is run
**Then** the process exits 0
**And** stdout is exactly the installed package version derived through `importlib.metadata` for `nmg-sdlc-smoke-python`, followed by a single newline
**And** a name argument is not required

### AC2: Existing greeting is unchanged

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Missing name still fails when version is not requested

**Given** the distribution is installed
**When** `nmg-smoke` is run with no arguments
**Then** the process exits non-zero and does not print a greeting

### AC4: Version wins when a name is also present

**Given** the distribution is installed
**When** `nmg-smoke --version` is run with a name also present
**Then** the process exits 0
**And** stdout is exactly the installed package version derived through `importlib.metadata` for `nmg-sdlc-smoke-python`, followed by a single newline
**And** the process does not print a greeting

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --version` prints the installed `nmg-sdlc-smoke-python` version from `importlib.metadata` and exits 0 without requiring a name | Must | Bare version string plus one newline; no program or distribution-name prefix |
| FR2 | Existing `nmg-smoke NAME` greeting behavior remains unchanged | Must | |
| FR3 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR4 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | `importlib.metadata` is stdlib on Python 3.12+ |
| FR5 | Update README CLI usage only as needed to document `nmg-smoke --version` | Must | Do not hardcode a VERSION literal |

---

## Out of Scope

- Changing `greet` or adding a public library version export
- Adding a short `-V` flag
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Making the positional `name` optional
- Reading version from the `VERSION` file instead of installed package metadata
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #39 | 2026-08-31 | Initial feature spec |
