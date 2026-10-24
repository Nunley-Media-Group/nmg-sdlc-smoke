# Requirements: Add greeting_lowercase_count library helper

**Issue**: #224
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/221-add-greeting-uppercase-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_lowercase_count(name)` helper that returns the number of ASCII lowercase letters in the completed greeting
**So that** I can measure a greeting's lowercase content without re-implementing the greeting or the lowercase letter set

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The sibling helpers `greeting_vowel_count` and `greeting_uppercase_count` each count a fixed ASCII letter set in the completed greeting and ignore accented and fullwidth letters. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts lowercase letters.

## Acceptance Criteria

### AC1: Count ASCII lowercase letters in the completed greeting

**Given** the valid names `Ada` and `abc xyz`
**When** a caller invokes `greeting_lowercase_count` with each name
**Then** it returns the Python `int` `6` for `Ada` (`e`, `l`, `l`, `o` in `Hello` plus `d`, `a`)
**And** it returns `10` for `abc xyz` (`ello` plus the six lowercase letters in the name)

### AC2: Count only the 26 ASCII lowercase letters a–z

**Given** the valid names `BOB 42!`, `é` (precomposed U+00E9), and `ｂｃ` (fullwidth U+FF42 U+FF43)
**When** a caller invokes `greeting_lowercase_count` with each name
**Then** it returns `4` for each name, because only the `ello` in `Hello, ` is counted
**And** uppercase letters, digits, spaces, punctuation, accented letters, and fullwidth letters are never counted

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_lowercase_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_lowercase_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_lowercase_count("Ada")` returns `6`
**And** `"greeting_lowercase_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- the ASCII `a`–`z` set, with accented and fullwidth letters excluded
- that the count covers the complete greeting, not the name alone
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_lowercase_count(name: str) -> int` returning the number of characters in `greet(name)` that are ASCII `a`–`z` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_lowercase_count` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section | Must |

## Out of Scope

- A Unicode-aware lowercase-count helper
- A CLI flag or option exposing the lowercase count
- Changes to `greet`, existing helpers, or `nmg-smoke` output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #224 | 2026-10-24 | Initial feature spec |
