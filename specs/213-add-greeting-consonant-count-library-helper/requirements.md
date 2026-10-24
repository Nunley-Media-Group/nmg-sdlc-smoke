# Requirements: Add greeting_consonant_count library helper

**Issue**: #213
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_consonant_count(name)` helper that returns the number of ASCII consonant letters in the completed greeting
**So that** I can measure a greeting's consonant content without re-implementing the greeting or the consonant set

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The sibling helper `greeting_vowel_count` counts the ten ASCII vowels `a e i o u A E I O U` in the completed greeting. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts consonants.

## Acceptance Criteria

### AC1: Count ASCII consonants in the completed greeting

**Given** the valid names `Ada` and `BCDFGHJKLMNPQRSTVWXYZ bcdfghjklmnpqrstvwxyz`
**When** a caller invokes `greeting_consonant_count` with each name
**Then** it returns the Python `int` `4` for `Ada` (`Hello, Ada` contains `H`, `l`, `l`, `d`)
**And** it returns `45` for the all-consonants name (3 from `Hello, ` plus all 42 ASCII consonants)

### AC2: Treat `y`/`Y` as consonants and ignore every other character

**Given** the valid names `Ady`, `Yy`, `Bob 42!`, `Émile` (precomposed `É`, U+00C9), and `Ｂｃｄ` (fullwidth U+FF22 U+FF43 U+FF44)
**When** a caller invokes `greeting_consonant_count` with each name
**Then** it returns `5`, `5`, `5`, `5`, and `3` respectively
**And** this holds because only the 42 ASCII letters outside `a e i o u A E I O U` are counted (including `y` and `Y`). Vowels, digits, spaces, punctuation, accented letters, and fullwidth letters are not counted.

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_consonant_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_consonant_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_consonant_count("Ada")` returns `4`
**And** `"greeting_consonant_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- the 42-letter ASCII consonant set, with `y`/`Y` included
- that the count covers the complete greeting, not the name alone
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_consonant_count(name: str) -> int`. It returns the number of characters in the completed `greet(name)` that are ASCII letters (`A`–`Z`, `a`–`z`) other than `a e i o u A E I O U`. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. In the README Library section, document its import, an example result, the consonant set including `y`/`Y`, the complete-greeting scope, and the inherited validation. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change
- Counting accented, other non-ASCII, or fullwidth letters as consonants
- Counting consonants in the name alone, or per-letter breakdowns
- Changing `greet`, `greeting_vowel_count`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #213 | 2026-10-24 | Initial feature spec |
