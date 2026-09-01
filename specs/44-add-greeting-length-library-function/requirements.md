# Requirements: Add greeting_length library function

**Issue**: #44
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_length(name)` library function that returns the number of characters in `greet(name)`
**So that** callers can observe greeting size from the existing greeting contract without changing `greet` or the CLI

---

## Background

The smoke host already exposes a pure `greet(name)` library function and a thin `nmg-smoke` CLI adapter. Maintainers need a length helper that reuses that greeting contract so the reported size always matches the current greeting string, including validation of blank, whitespace-only, and non-string names.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Valid name returns the greeting character count

**Given** the library is importable
**When** `greeting_length("Ada")` is called
**Then** it returns `10`
**And** that value equals the Python `len()` of `greet("Ada")` (`Hello, Ada`)

### AC2: A different valid name returns a matching different count

**Given** the library is importable
**When** `greeting_length("Jo")` is called
**Then** it returns `9`
**And** that value equals the Python `len()` of `greet("Jo")` (`Hello, Jo`)
**And** the result is not hardcoded to the Ada count

### AC3: Invalid names raise the existing greet validation error

**Given** the library is importable
**When** `greeting_length` is called with a blank, whitespace-only, or non-string name
**Then** it raises `ValueError` with message `name must not be blank`
**And** that error is the existing `greet` validation error, not a wrapped or renamed error

### AC4: Existing greet and CLI behavior is unchanged

**Given** the distribution is installed
**When** `greet("Ada")` is called
**Then** it returns `Hello, Ada`
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline
**And** blank names still raise `ValueError` from `greet` and still cause the CLI to exit non-zero without a stdout greeting

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `greeting_length(name)` returns the Python `len()` of the full `greet(name)` string (Unicode code points of the whole greeting, including the `Hello, ` prefix) | Must | Implement as `return len(greet(name))`; do not count `name` alone or UTF-8 bytes |
| FR2 | `greeting_length` is importable from the existing public package surface (`from nmg_sdlc_smoke import greeting_length`) | Must | Append it to `__all__`; do not drop `greet` or any already-exported names |
| FR3 | Invalid names (blank, whitespace-only, non-string) raise the existing `greet` `ValueError("name must not be blank")` | Must | Do not catch, wrap, or rename that `ValueError` |
| FR4 | `greet` and `nmg-smoke` behavior remain unchanged | Must | Do not edit `cli.py` |
| FR5 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR6 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | |
| FR7 | Update README library usage only as needed to document a concise `greeting_length` example | Should | Keep the existing `greet("Ada")` example |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Adding or changing CLI flags or `nmg-smoke` arguments
- UTF-8 byte counting (count is Python `len()` of the greeting string)
- `greet_many` or any batch API
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #44 | 2026-09-01 | Initial feature spec |
