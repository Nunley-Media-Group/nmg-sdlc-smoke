# Requirements: Add greeting_uppercase_count library helper

**Issue**: #221
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_uppercase_count(name)` helper that returns the number of ASCII uppercase letters in the completed greeting
**So that** I can measure a greeting's capitalization without re-implementing the greeting or the uppercase letter set

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The sibling helper `greeting_vowel_count` counts a fixed ASCII letter set in the completed greeting and ignores accented and fullwidth letters. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts uppercase letters.

## Acceptance Criteria

### AC1: Count ASCII uppercase letters in the completed greeting

**Given** the valid names `Ada` and `ABC XYZ`
**When** a caller invokes `greeting_uppercase_count` with each name
**Then** it returns the Python `int` `2` for `Ada` (`H` and `A` in `Hello, Ada`)
**And** it returns `7` for `ABC XYZ` (`H` plus the six capitals in the name)

### AC2: Count only the 26 ASCII capitals A–Z

**Given** the valid names `bob 42!`, `Émile` (precomposed `É`, U+00C9), and `ＢＣ` (fullwidth U+FF22 U+FF23)
**When** a caller invokes `greeting_uppercase_count` with each name
**Then** it returns `1` for each name, because only the `H` in `Hello, ` is counted
**And** lowercase letters, digits, spaces, punctuation, accented letters, and fullwidth letters are never counted

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_uppercase_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_uppercase_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_uppercase_count("Ada")` returns `2`
**And** `"greeting_uppercase_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- the ASCII `A`–`Z` set, with accented and fullwidth letters excluded
- that the count covers the complete greeting, not the name alone
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_uppercase_count(name: str) -> int` returning the number of characters in `greet(name)` that are ASCII `A`–`Z` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_uppercase_count` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section | Must |

## Out of Scope

- A lowercase-count or Unicode-aware uppercase-count helper
- A CLI flag or option exposing the uppercase count
- Changes to `greet`, existing helpers, or `nmg-smoke` output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #221 | 2026-10-24 | Initial feature spec |
