# Requirements: Add greeting_starts_with_hello library function

**Issue**: #68
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_starts_with_hello(name)` library function that returns whether `greet(name)` starts with `Hello, `
**So that** callers can observe that prefix from the existing greeting contract without changing `greet` or the CLI

---

## Background

The smoke host already exposes a pure `greet(name)` library function plus `greeting_length(name)` and `greeting_is_ascii(name)`, with a thin `nmg-smoke` CLI adapter. Maintainers need a prefix helper that reuses that greeting contract so the result is the Python bool from `greet(name).startswith("Hello, ")`, including validation of blank, whitespace-only, and non-string names.

With the current greeting format `Hello, {name}`, every valid name yields `True`. The contract is still the prefix check against `greet(name)`, not a hardcoded constant that ignores `greet`. Invalid names must surface the same `ValueError` `greet` already raises.

Public package currently exports `greet`, `greeting_is_ascii`, and `greeting_length` (`from nmg_sdlc_smoke import greet, greeting_is_ascii, greeting_length`). `greet(name)` returns `Hello, {name}` and raises `ValueError("name must not be blank")` for blank, whitespace-only, or non-string names. `greeting_length(name)` returns the Python character count of that greeting (`Ada` → 10). `greeting_is_ascii(name)` returns `greet(name).isascii()`. `nmg-smoke` is a thin argparse CLI (`--uppercase`, `--repeat`, `--prefix`, positional name) and does not expose library helpers. No `greeting_starts_with_hello` symbol exists in `src/nmg_sdlc_smoke/greet.py` or the package `__all__`.

Neighboring contracts: issue #44 (`specs/44-add-greeting-length-library-function/`), issue #57 (`specs/57-add-greeting-is-ascii-library-function/`), and issue #62 (`specs/62-add-greeting-contains-name-library-function/`). Issue #53 (`specs/53-add-greeting-bytes-library-function/`) is an approved spec, not a blocker, and is not exported from the live package.

Python `greet(name).startswith("Hello, ")` is the observable contract. With the current format, `Ada` → `True` and `Jo` → `True`. Returns are the Python bools `True` and `False`, not the strings `"True"` / `"False"`. The checked prefix is the seven-character literal `Hello, ` (capital H, comma, trailing space).

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Valid name returns True

**Given** the library is importable
**When** `greeting_starts_with_hello("Ada")` is called
**Then** it returns `True`
**And** that value equals `greet("Ada").startswith("Hello, ")` (`Hello, Ada`)
**And** the return value is the Python bool `True`, not the string `"True"`

### AC2: A different valid name also returns True from the prefix check

**Given** the library is importable
**When** `greeting_starts_with_hello("Jo")` is called
**Then** it returns `True`
**And** that value equals `greet("Jo").startswith("Hello, ")` (`Hello, Jo`)
**And** the result is not hardcoded to the Ada call only

### AC3: Invalid names raise the existing greet validation error

**Given** the library is importable
**When** `greeting_starts_with_hello` is called with a blank, whitespace-only, or non-string name
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
| FR1 | `greeting_starts_with_hello(name)` returns the Python bool from `greet(name).startswith("Hello, ")` for the same name | Must | Implement as `return greet(name).startswith("Hello, ")`; do not `return True`; do not check `name.startswith("Hello, ")` |
| FR2 | `greeting_starts_with_hello` is importable from the existing public package surface (`from nmg_sdlc_smoke import greeting_starts_with_hello`); append it to the public exports and do not drop `greet`, `greeting_is_ascii`, `greeting_length`, or any already-exported names | Must | Default `__all__` becomes `["greet", "greeting_is_ascii", "greeting_length", "greeting_starts_with_hello"]`; if `greeting_bytes` or `greeting_contains_name` is already exported, keep it |
| FR3 | Invalid names (blank, whitespace-only, non-string) raise the existing `greet` `ValueError("name must not be blank")` without catching, wrapping, or renaming that error | Must | Do not re-validate `name` inside `greeting_starts_with_hello` |
| FR4 | `greet`, `greeting_is_ascii`, `greeting_length`, and `nmg-smoke` behavior remain unchanged | Must | Do not edit `cli.py` or the `greet` / `greeting_length` / `greeting_is_ascii` bodies |
| FR5 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR6 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must | `str.startswith` is stdlib |
| FR7 | Update README library usage only as needed to document a concise `greeting_starts_with_hello` example such as `greeting_starts_with_hello("Ada")` → `True`; keep the existing `greet("Ada")`, `greeting_length("Ada")`, and `greeting_is_ascii("Ada")` examples | Should | CLI section does not mention `greeting_starts_with_hello` |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Changing `greeting_length` or `greeting_is_ascii` behavior
- Adding or changing CLI flags or `nmg-smoke` arguments
- Case-insensitive or substring prefix matching
- Checking `name.startswith("Hello, ")` instead of `greet(name).startswith("Hello, ")`
- Adding runtime dependencies
- Database, HTTP API, UI, or publication pipeline work
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #68 | 2026-09-01 | Initial feature spec |
