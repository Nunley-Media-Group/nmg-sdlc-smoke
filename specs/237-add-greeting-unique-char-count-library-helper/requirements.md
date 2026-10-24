# Requirements: Add greeting_unique_char_count library helper

**Issue**: #237
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/233-add-greeting-punctuation-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_unique_char_count(name)` helper that returns the number of distinct characters in the completed greeting
**So that** I can measure a greeting's character variety without re-implementing the greeting or the distinctness rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The fixed `Hello, ` prefix contributes six distinct characters: `H`, `e`, `l`, `o`, `,`, and the space.

Distinctness is by Unicode code point and is case-sensitive: `A` and `a` are different characters, and no Unicode normalization is applied.

The sibling count helpers (`greeting_vowel_count`, `greeting_uppercase_count`, `greeting_lowercase_count`, `greeting_digit_count`, `greeting_space_count`, `greeting_punctuation_count`) each count a fixed character set in the completed greeting. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper counts distinct characters.

## Acceptance Criteria

### AC1: Count distinct characters in the completed greeting

**Given** the valid names `Ada`, `Bob`, and `Ada Lovelace`
**When** a caller invokes `greeting_unique_char_count` with each name
**Then** it returns the Python `int` `9` for `Ada`, `8` for `Bob`, and `12` for `Ada Lovelace`

### AC2: Count is case-sensitive and per Unicode code point

**Given** the valid names `ADA` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_unique_char_count` with each name
**Then** it returns `8` for `ADA` and `8` for `Zoë`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_unique_char_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_unique_char_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_unique_char_count("Ada")` returns `9`
**And** `"greeting_unique_char_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that distinct characters are counted by Unicode code point, case-sensitively, without normalization
- that the count covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_unique_char_count(name: str) -> int` returning the number of distinct Unicode code points in `greet(name)`, case-sensitive and without normalization | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_unique_char_count` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, example, and prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A CLI flag or option exposing the distinct-character count
- Unicode normalization or grapheme-cluster counting
- Counting distinct characters in the name alone rather than the completed greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #237 | 2026-10-24 | Initial feature spec |
