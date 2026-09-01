# Requirements: Add greeting_is_ascii library function

**Issue**: #57
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_is_ascii(name)` library function that returns whether `greet(name)` is ASCII
**So that** callers can observe ASCII-ness of the existing greeting contract without changing `greet` or the CLI

---

## Background

The smoke host already exposes a pure `greet(name)` library function, a `greeting_length(name)` character-count helper, and a thin `nmg-smoke` CLI adapter. Maintainers need an ASCII-check helper that reuses that greeting contract so the result is the Python bool from `greet(name).isascii()`, including validation of blank, whitespace-only, and non-string names.

The `Hello, ` prefix is ASCII, so a valid ASCII name such as `Ada` yields `True` and a valid non-ASCII name such as `É` yields `False`. Invalid names must surface the same `ValueError` `greet` already raises.

Public package currently exports `greet` and `greeting_length` (`from nmg_sdlc_smoke import greet, greeting_length`). `greet(name)` returns `Hello, {name}` and raises `ValueError("name must not be blank")` for blank, whitespace-only, or non-string names. `greeting_length(name)` returns the Python character count of that greeting (`Ada` → 10). `nmg-smoke` is a thin argparse CLI (`--uppercase`, `--repeat`, positional name) and does not expose length or ASCII helpers. No `greeting_is_ascii` symbol exists.

Neighboring contracts: issue #44 (`specs/44-add-greeting-length-library-function/`, present in source) and issue #53 (`specs/53-add-greeting-bytes-library-function/`, approved spec, not a blocker). This issue does not depend on #52 or #53.

Python `str.isascii()` is the observable contract: `Ada` → `True`, `É` → `False`. Returns are the Python bools `True` and `False`, not the strings `"True"` / `"False"`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Valid ASCII name returns True

**Given** the library is importable
**When** `greeting_is_ascii("Ada")` is called
**Then** it returns `True`
**And** that value equals `greet("Ada").isascii()` (`Hello, Ada`)

### AC2: Valid non-ASCII name returns False

**Given** the library is importable
**When** `greeting_is_ascii("É")` is called
**Then** it returns `False`
**And** that value equals `greet("É").isascii()` (`Hello, É`)
**And** the result is not hardcoded to the Ada result

### AC3: Invalid names raise the existing greet validation error

**Given** the library is importable
**When** `greeting_is_ascii` is called with a blank, whitespace-only, or non-string name
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
| FR1 | `greeting_is_ascii(name)` returns the Python bool from `greet(name).isascii()` for the same name, including the `Hello, ` prefix | Must | Implement as `return greet(name).isascii()`; do not check `name.isascii()` |
| FR2 | `greeting_is_ascii` is importable from the existing public package surface (`from nmg_sdlc_smoke import greeting_is_ascii`); append it to the public exports and do not drop `greet`, `greeting_length`, or any already-exported names | Must | Default `__all__` becomes `["greet", "greeting_length", "greeting_is_ascii"]`; if `greeting_bytes` is already exported, keep it |
| FR3 | Invalid names (blank, whitespace-only, non-string) raise the existing `greet` `ValueError("name must not be blank")` without catching, wrapping, or renaming that error | Must | Do not re-validate `name` inside `greeting_is_ascii` |
| FR4 | `greet`, `greeting_length`, and `nmg-smoke` behavior remain unchanged | Must | Do not edit `cli.py` or the `greet` / `greeting_length` bodies |
| FR5 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR6 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | `str.isascii` is stdlib |
| FR7 | Update README library usage only as needed to document a concise `greeting_is_ascii` example such as `greeting_is_ascii("Ada")` → `True`; keep the existing `greet("Ada")` and `greeting_length("Ada")` examples | Should | CLI section does not mention `greeting_is_ascii` |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Changing `greeting_length` character-count behavior
- Adding or changing CLI flags or `nmg-smoke` arguments
- Counting characters or UTF-8 bytes (those remain `greeting_length` / `greeting_bytes`)
- Checking `name.isascii()` instead of `greet(name).isascii()`
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #57 | 2026-09-01 | Initial feature spec |
