# Requirements: Add greeting_vowel_count library helper

**Issue**: #203
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_vowel_count(name)` helper that counts vowels in the completed greeting
**So that** I can get that count without re-implementing the vowel check

## Background

`greet(name)` returns `Hello, {name}` for valid names. For empty, whitespace-only, and non-string names it raises `ValueError("name must not be blank")`. Sibling helpers such as `greeting_length`, `greeting_bytes`, and `greeting_word_count` each derive a number from the completed greeting. Each one calls `greet(name)`, is re-exported from `nmg_sdlc_smoke`, is listed in `nmg_sdlc_smoke.__all__`, and is documented in the README Library section. No helper counts vowels.

## Acceptance Criteria

### AC1: Count ASCII vowels in the completed greeting

**Given** valid names `Ada` and `AEIOU aeiou`
**When** a caller invokes `greeting_vowel_count` with each name
**Then** it returns the Python `int` `4` for `Ada` (`Hello, Ada` contains `e`, `o`, `A`, `a`) and `12` for `AEIOU aeiou`

### AC2: Ignore characters outside the ten ASCII vowels

**Given** valid names `Bcd`, `Ady`, `Émile` (precomposed `É`, U+00C9), and `Ａｄａ` (fullwidth U+FF21 U+FF44 U+FF41)
**When** a caller invokes `greeting_vowel_count` with each name
**Then** it returns `2`, `3`, `4`, and `2` respectively, because only `a e i o u A E I O U` count and `y`/`Y`, accented letters, and fullwidth letters do not

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_vowel_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_vowel_count` from `nmg_sdlc_smoke` and follows the README example
**Then** `greeting_vowel_count("Ada")` returns `4` and `greeting_vowel_count` appears in `nmg_sdlc_smoke.__all__`
**And** the README documents the ten-character ASCII vowel set, the completed-greeting scope, and the inherited invalid-name error

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_vowel_count(name: str) -> int`. It returns the number of characters in the completed `greet(name)` that are one of the ten code points `a e i o u A E I O U`. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke`, including `__all__`. Document its import, example result, vowel set, and inherited validation in the README Library section. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change
- Counting `y`/`Y`, accented or other non-ASCII vowels, or fullwidth letters
- Counting vowels in the name alone, or per-vowel breakdowns
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #203 | 2026-10-18 | Initial feature spec |
