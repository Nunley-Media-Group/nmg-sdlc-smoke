# Requirements: Add greeting_digit_count library helper

**Issue**: #227
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/224-add-greeting-lowercase-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_digit_count(name)` helper that returns the number of ASCII digits in the completed greeting
**So that** I can measure a greeting's numeric content without re-implementing the greeting or the digit set

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The fixed `Hello, ` prefix contains no digits, so every counted digit comes from the name.

The sibling helpers `greeting_vowel_count`, `greeting_uppercase_count`, and `greeting_lowercase_count` each count a fixed ASCII character set in the completed greeting and ignore non-ASCII look-alikes. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts digits. Python's `str.isdigit()` and `str.isdecimal()` return `True` for fullwidth, Arabic-Indic, and (for `isdigit`) superscript digits, so they cannot define the ASCII-only set.

## Acceptance Criteria

### AC1: Count ASCII digits in the completed greeting

**Given** the valid names `R2D2`, `Agent 007`, and `Ada`
**When** a caller invokes `greeting_digit_count` with each name
**Then** it returns the Python `int` `2` for `R2D2`, `3` for `Agent 007`, and `0` for `Ada`

### AC2: Count only the ten ASCII digits 0–9

**Given** the valid names `１２` (fullwidth U+FF11 U+FF12), `٣` (Arabic-Indic U+0663), and `x²` (superscript U+00B2)
**When** a caller invokes `greeting_digit_count` with each name
**Then** it returns `0` for each name, because only the characters `0` through `9` are counted

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_digit_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_digit_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_digit_count("R2D2")` returns `2`
**And** `"greeting_digit_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- the ASCII `0`–`9` set, with fullwidth, other-script, and superscript digits excluded
- that the count covers the complete greeting, not the name alone
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_digit_count(name: str) -> int` returning the number of characters in `greet(name)` that are ASCII `0`–`9` | Must |
| FR2 | Never count non-ASCII digit characters (fullwidth, other scripts, superscripts) | Must |
| FR3 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR4 | Export `greeting_digit_count` from `nmg_sdlc_smoke`, list it in `__all__`, and document it in the README Library section without removing existing exports | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A boolean digit-presence probe (`greeting_has_digit`)
- A Unicode-aware digit-count helper
- A CLI flag or option exposing the digit count
- Counting digits in the name alone rather than the completed greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #227 | 2026-10-24 | Initial feature spec |
