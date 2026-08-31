# Requirements: Add greet_many library API

**Issue**: #40
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greet_many(names)` library API that applies the existing `greet` contract to each name in an iterable
**So that** batch greetings are observable in input order without changing `greet` or the CLI

---

## Background

The smoke host already exposes a pure `greet(name)` library function and a thin `nmg-smoke` CLI adapter. Maintainers need a batch helper that reuses that greeting contract over many names so library callers can obtain ordered results, including an empty result for empty input, without a new CLI path or a change to single-name validation.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Multiple valid names in input order

**Given** the library is importable
**When** `greet_many` is called with an iterable of valid names such as `["Ada", "Bob"]`
**Then** it returns `["Hello, Ada", "Hello, Bob"]`
**And** each element is the result of applying the existing `greet` contract to the corresponding input name
**And** duplicate names produce duplicate greetings in the same positions

### AC2: Empty iterable

**Given** the library is importable
**When** `greet_many` is called with an empty iterable
**Then** it returns `[]`

### AC3: First invalid name propagates greet's error

**Given** the library is importable
**When** `greet_many` is called with an iterable whose first invalid name is blank, whitespace-only, or non-string
**Then** it raises `ValueError` with message `name must not be blank`
**And** that error is the existing `greet` validation error, not a wrapped or renamed error
**And** it does not return greetings for later names

### AC4: Bare string names argument is rejected

**Given** the library is importable
**When** `greet_many` is called with a `str` as the names argument
**Then** it raises `TypeError`
**And** it does not iterate the string as characters and does not return per-character greetings

### AC5: Existing greet and CLI behavior is unchanged

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
| FR1 | `greet_many(names)` accepts an iterable of names and returns a list of greetings in input order by applying the existing `greet` contract to each name | Must | Return type is `list`, including when the input is a tuple or generator |
| FR2 | Empty iterable input returns `[]` | Must | |
| FR3 | The first invalid name raises the existing `greet` `ValueError("name must not be blank")` and stops | Must | Do not catch, wrap, or rename that `ValueError` |
| FR4 | A bare `str` names argument raises `TypeError` instead of iterating characters | Must | Check `isinstance(names, str)` before iterating; message is `names must not be a str` |
| FR5 | `greet_many` is importable from the existing public package surface (`from nmg_sdlc_smoke import greet_many`) | Must | Add it to `__all__` beside `greet` |
| FR6 | `greet` and `nmg-smoke` behavior remain unchanged | Must | |
| FR7 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR8 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | `collections.abc.Iterable` is stdlib |
| FR9 | Update README library usage only as needed to document a concise `greet_many` example | Must | Keep the existing `greet("Ada")` example |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Adding or changing CLI flags or `nmg-smoke` arguments
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Special-casing `bytes` / `bytearray` (only bare `str` is rejected as a container)
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #40 | 2026-08-31 | Initial feature spec |
