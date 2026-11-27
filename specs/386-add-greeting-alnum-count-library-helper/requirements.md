# Requirements: Add greeting_alnum_count library helper

**Issue**: #386
**Date**: 2026-11-27
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_alnum_count(name)` helper that returns how many alphanumeric characters the completed greeting contains
**So that** I can measure letters and digits together without re-implementing the greeting

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The library offers `greeting_letter_count(name)` (`str.isalpha()`) and `greeting_digit_count(name)` (ASCII `0`–`9` only), but nothing counts letters and digits together.

`greeting_alnum_count` counts the code points in the complete greeting (not the name alone) for which `str.isalnum()` is true. This includes the five letters of `Hello`, non-ASCII letters, and Unicode digits. Spaces, punctuation, combining marks, and emoji are not counted, and no Unicode normalization is applied.

## Acceptance Criteria

### AC1: Count alphanumeric characters in a greeting

**Given** the valid names `Ada`, `Zoë` (precomposed U+00EB), `李雷`, and `R2-D2`
**When** a caller invokes `greeting_alnum_count` with each name
**Then** they return `8`, `8`, `7`, and `9` respectively
**And** `type(result) is int` for each result

### AC2: Count Unicode digits, exclude marks and emoji, no normalization

**Given** the valid names `"Zoe\u0308"` (decomposed `e` + U+0308 COMBINING DIAERESIS), `"Ada \U0001F600"` (U+1F600 GRINNING FACE), and `"Agent \u0663"` (U+0663 ARABIC-INDIC DIGIT THREE)
**When** a caller invokes `greeting_alnum_count` with each name
**Then** they return `8`, `8`, and `11` respectively
**And** for every valid name in AC1 and AC2 the result equals `sum(ch.isalnum() for ch in greet(name))`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_alnum_count` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_alnum_count` and follows the README example
**Then** the import succeeds and the README example `greeting_alnum_count("R2-D2")` gives `9`
**And** `"greeting_alnum_count"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README says that it counts `str.isalnum()` code points in the complete greeting without normalization and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_alnum_count(name: str) -> int` to `src/nmg_sdlc_smoke/greet.py`, returning the number of code points in `greet(name)` for which `str.isalnum()` is true | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_alnum_count` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_alnum_count` in the README Library section (import list, usage example, behavior sentence), following the other count helpers | Should |

## Out of Scope

- A CLI flag for `nmg-smoke` exposing the count
- Counting grapheme clusters or UTF-8 bytes, or counting after Unicode normalization
- Any change to `greet`, `greeting_letter_count`, `greeting_digit_count`, or other existing helpers

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #386 | 2026-11-27 | Initial feature spec |
