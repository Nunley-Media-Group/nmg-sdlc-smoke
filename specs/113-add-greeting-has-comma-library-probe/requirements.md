# Requirements: Add greeting_has_comma library probe

**Issue**: #113
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_has_comma(name)` library probe
**So that** the installed nmg-sdlc candidate for issue 383 can be live-smoked through approved specification, implementation, verification, and delivery without changing `greet` or the CLI

## Background

This is a disposable fixture for live-smoking nmg-sdlc #383, not independent smoke-application backlog. The host already exposes `greet(name)` and several pure derived helpers. Maintainers need one more boolean probe that reports whether the complete default greeting contains the literal comma separator, reusing the existing name-validation contract, so the candidate’s pre-dispatch File(s) boundary can be exercised on a real consumer issue.

`greet(name)` in `src/nmg_sdlc_smoke/greet.py` rejects blank, whitespace-only, and non-string names with `ValueError("name must not be blank")` and otherwise returns `Hello, {name}` (example: `greet("Ada")` is `Hello, Ada`). Derived helpers such as `greeting_starts_with_hello` and `greeting_word_count` call `greet` for validation and results, and are exported from `nmg_sdlc_smoke` via `__all__`. There is no `greeting_has_comma` symbol. The CLI adapter `src/nmg_sdlc_smoke/cli.py` (`nmg-smoke`) calls `greet` only and must stay unchanged.

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Default Ada greeting reports the comma separator

**Given** the library is importable
**When** `greeting_has_comma("Ada")` is called
**Then** it returns the Python bool `True`
**And** that value matches whether the complete default greeting `greet("Ada")` (`Hello, Ada`) contains the literal comma separator

### AC2: A second valid name is also true and is not hardcoded to Ada

**Given** the library is importable
**When** `greeting_has_comma("Jo")` is called
**Then** it returns the Python bool `True`
**And** that value matches whether the complete default greeting `greet("Jo")` contains the literal comma separator
**And** `greet("Jo")` is not the same string as `greet("Ada")`

### AC3: Invalid names reuse existing validation

**Given** the library is importable
**When** `greeting_has_comma` is called with a blank, whitespace-only, or non-string name
**Then** it raises `ValueError` with message `name must not be blank`
**And** that error is the existing `greet` validation error, not a wrapped or renamed error

### AC4: Existing greet and CLI behavior is unchanged

**Given** the distribution is installed
**When** `greet("Ada")` or `nmg-smoke Ada` is used
**Then** both retain their existing output and error behavior
**And** no new CLI flag or CLI output path is added

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `greeting_has_comma(name)` returns true when the complete default greeting for that name contains the literal comma separator | Must |
| FR2 | The helper reuses existing `greet` name validation; invalid names raise `ValueError("name must not be blank")` without wrapping or renaming | Must |
| FR3 | The helper is importable from the existing public package surface (`from nmg_sdlc_smoke import greeting_has_comma`) without dropping already-exported names | Must |
| FR4 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must |
| FR5 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass | Must |
| FR6 | Document a concise README library example for `greeting_has_comma` without changing CLI documentation | Should |

## Out of Scope

- Any CLI flag, argument, or output change to `nmg-smoke`
- Changing `greet` format, validation, or signature
- Adding other punctuation or separator probes
- New modules, runtime dependencies, HTTP, UI, or database
- Repairing unrelated smoke backlog
- Bumping `VERSION`

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #113 | 2026-09-13 | Initial feature spec |
