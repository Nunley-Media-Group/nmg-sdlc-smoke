# Requirements: Add greeting_letter_count library helper

**Issue**: #242
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/237-add-greeting-unique-char-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_letter_count(name)` helper that returns the number of alphabetic characters in the completed greeting
**So that** I can count a greeting's letters, including non-ASCII letters, without re-implementing the greeting or the letter rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The fixed `Hello, ` prefix contributes five letters: `H`, `e`, `l`, `l`, and `o`.

A character is a letter when Python's `str.isalpha()` is true for it. That covers Unicode letters such as `ë`. It excludes digits, spaces, punctuation such as `,` and `'`, and other non-letter characters. No Unicode normalization is applied.

`greeting_uppercase_count` and `greeting_lowercase_count` count only the ASCII ranges `A`–`Z` and `a`–`z`. No existing helper counts all alphabetic characters.

The sibling count helpers each have the same four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`;
- a self-aliased re-export from `nmg_sdlc_smoke`;
- an entry in `nmg_sdlc_smoke.__all__`;
- a README Library entry with an import, an example result, and a prose contract line.

## Acceptance Criteria

### AC1: Count alphabetic characters in the completed greeting

**Given** the valid names `Ada`, `Ada Lovelace`, and `R2D2`
**When** a caller invokes `greeting_letter_count` with each name
**Then** it returns the Python `int` `8` for `Ada`, `16` for `Ada Lovelace`, and `7` for `R2D2`

### AC2: Count Unicode letters and exclude non-letters

**Given** the valid names `Zoë` (with precomposed U+00EB) and `O'Brien`
**When** a caller invokes `greeting_letter_count` with each name
**Then** it returns `8` for `Zoë` and `11` for `O'Brien`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_letter_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_letter_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_letter_count("Ada")` returns `8`
**And** `"greeting_letter_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that letters are characters for which `str.isalpha()` is true, including non-ASCII letters
- that the count covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_letter_count(name: str) -> int` returning the number of characters in `greet(name)` for which `str.isalpha()` is true | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_letter_count` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, example, and prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A CLI flag or option exposing the letter count
- ASCII-only letter counting or Unicode normalization
- Counting letters in the name alone rather than the completed greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #242 | 2026-10-24 | Initial feature spec |
