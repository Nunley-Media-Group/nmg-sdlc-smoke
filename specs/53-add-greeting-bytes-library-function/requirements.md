# Requirements: Add greeting_bytes library function

**Issue**: #53
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_bytes(name)` library function that returns the UTF-8 byte length of `greet(name)`
**So that** callers can observe greeting size in bytes from the existing greeting contract without changing `greet` or the CLI

---

## Background

The smoke host already exposes a pure `greet(name)` library function, a `greeting_length(name)` character-count helper, and a thin `nmg-smoke` CLI adapter. Maintainers need a byte-count helper that reuses that greeting contract so the reported size is the UTF-8 encoding of the full greeting string, including validation of blank, whitespace-only, and non-string names.

Neighboring delivered contract: issue #44 (`specs/44-add-greeting-length-library-function/`). Public package currently exports `greet` and `greeting_length` (`from nmg_sdlc_smoke import greet, greeting_length`). `greet(name)` returns `Hello, {name}` and raises `ValueError("name must not be blank")` for blank, whitespace-only, or non-string names. `greeting_length(name)` returns the Python character count of that greeting (`Ada` → 10, `É` → 8). `nmg-smoke` is a thin argparse CLI and does not expose length or byte helpers. No `greeting_bytes` symbol exists.

UTF-8 byte length of `Hello, É` is 9 because `É` encodes as two bytes; Python `len("Hello, É")` / `greeting_length("É")` remains 8.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Valid ASCII name returns the greeting UTF-8 byte count

**Given** the library is importable
**When** `greeting_bytes("Ada")` is called
**Then** it returns `10`
**And** that value equals `len(greet("Ada").encode("utf-8"))` (`Hello, Ada`)

### AC2: A non-ASCII name returns UTF-8 bytes, not character count

**Given** the library is importable
**When** `greeting_bytes("É")` is called
**Then** it returns `9`
**And** that value equals `len(greet("É").encode("utf-8"))` (`Hello, É`)
**And** that value is not equal to `greeting_length("É")`, which is `8`
**And** the result is not hardcoded to the Ada count

### AC3: Invalid names raise the existing greet validation error

**Given** the library is importable
**When** `greeting_bytes` is called with a blank, whitespace-only, or non-string name
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
| FR1 | `greeting_bytes(name)` returns the UTF-8 byte length of the full `greet(name)` string, including the `Hello, ` prefix: `len(greet(name).encode("utf-8"))` | Must | Implement as `return len(greet(name).encode("utf-8"))`; do not count `name` alone or Python `len()` of the greeting string |
| FR2 | `greeting_bytes` is importable from the existing public package surface (`from nmg_sdlc_smoke import greeting_bytes`); append it to `__all__` and do not drop `greet` or `greeting_length` | Must | `__all__` becomes `["greet", "greeting_length", "greeting_bytes"]` |
| FR3 | Invalid names (blank, whitespace-only, non-string) raise the existing `greet` `ValueError("name must not be blank")` without catching, wrapping, or renaming that error | Must | Do not re-validate `name` inside `greeting_bytes` |
| FR4 | `greet`, `greeting_length`, and `nmg-smoke` behavior remain unchanged | Must | Do not edit `cli.py` or the `greet` / `greeting_length` bodies |
| FR5 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR6 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | `str.encode` is stdlib |
| FR7 | Update README library usage only as needed to document a concise `greeting_bytes` example; keep the existing `greet("Ada")` and `greeting_length("Ada")` examples | Should | CLI section does not mention `greeting_bytes` |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Changing `greeting_length` character-count behavior
- Adding or changing CLI flags or `nmg-smoke` arguments
- Counting Unicode code points (that remains `greeting_length`)
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #53 | 2026-09-01 | Initial feature spec |
