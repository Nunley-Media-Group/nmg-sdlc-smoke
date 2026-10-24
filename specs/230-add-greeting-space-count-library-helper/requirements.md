# Requirements: Add greeting_space_count library helper

**Issue**: #230
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/227-add-greeting-digit-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_space_count(name)` helper that returns the number of ASCII space characters in the completed greeting
**So that** I can measure a greeting's spacing without re-implementing the greeting or the space rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The fixed `Hello, ` prefix contains exactly one space (U+0020), so every valid greeting has a space count of at least 1.

The sibling helpers `greeting_vowel_count`, `greeting_uppercase_count`, `greeting_lowercase_count`, and `greeting_digit_count` each count a fixed ASCII character set in the completed greeting and ignore look-alikes. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts spaces. Python's `str.isspace()` returns `True` for tabs, newlines, and no-break spaces, so it cannot define the U+0020-only set.

## Acceptance Criteria

### AC1: Count ASCII spaces in the completed greeting

**Given** the valid names `Ada`, `Ada Lovelace`, and `Grace Brewster Hopper`
**When** a caller invokes `greeting_space_count` with each name
**Then** it returns the Python `int` `1` for `Ada`, `2` for `Ada Lovelace`, and `3` for `Grace Brewster Hopper`

### AC2: Count only U+0020

**Given** the valid names `Ada\tLovelace` (tab U+0009), `Ada\nLovelace` (newline U+000A), and `Ada\u00a0Lovelace` (no-break space U+00A0)
**When** a caller invokes `greeting_space_count` with each name
**Then** it returns `1` for each name, because only the prefix's U+0020 space is counted

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_space_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_space_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_space_count("Ada Lovelace")` returns `2`
**And** `"greeting_space_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that only U+0020 is counted, with tabs, newlines, no-break spaces, and other Unicode whitespace excluded
- that the count covers the complete greeting, including the prefix space
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_space_count(name: str) -> int` returning the number of U+0020 characters in `greet(name)` | Must |
| FR2 | Never count tabs, newlines, no-break spaces, or other Unicode whitespace | Must |
| FR3 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR4 | Export `greeting_space_count` from `nmg_sdlc_smoke`, list it in `__all__`, and document it in the README Library section without removing existing exports | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A Unicode-whitespace-aware count helper
- A boolean space-presence probe
- A CLI flag or option exposing the space count
- Counting spaces in the name alone rather than the completed greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #230 | 2026-10-24 | Initial feature spec |
