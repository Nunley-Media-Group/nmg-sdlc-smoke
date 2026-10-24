# Requirements: Add greeting_punctuation_count library helper

**Issue**: #233
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/230-add-greeting-space-count-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_punctuation_count(name)` helper that returns the number of ASCII punctuation characters in the completed greeting
**So that** I can measure a greeting's punctuation without re-implementing the greeting or the punctuation rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The fixed `Hello, ` prefix contains exactly one comma, so every valid greeting has a punctuation count of at least 1.

The punctuation set is exactly the 32 ASCII characters in Python's `string.punctuation`: ``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~``. Non-ASCII look-alikes are not counted, including:
- the fullwidth exclamation mark `！` (U+FF01);
- the right single quotation mark `’` (U+2019);
- the ideographic comma `、` (U+3001).

The sibling helpers `greeting_vowel_count`, `greeting_uppercase_count`, `greeting_lowercase_count`, `greeting_digit_count`, and `greeting_space_count` each count a fixed ASCII character set in the completed greeting. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

The `greeting_has_*` helpers return booleans for single characters. No helper counts punctuation.

## Acceptance Criteria

### AC1: Count ASCII punctuation in the completed greeting

**Given** the valid names `Ada`, `O'Brien`, `Ada!?`, and `a.b-c_d`
**When** a caller invokes `greeting_punctuation_count` with each name
**Then** it returns the Python `int` `1` for `Ada`, `2` for `O'Brien`, `3` for `Ada!?`, and `4` for `a.b-c_d`

### AC2: Ignore non-ASCII look-alikes and non-punctuation characters

**Given** the valid names `Ada！` (U+FF01), `O’Brien` (U+2019), `Ada、` (U+3001), and `Ada Lovelace 42`
**When** a caller invokes `greeting_punctuation_count` with each name
**Then** it returns `1` for each name, because only the prefix comma is counted

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_punctuation_count` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_punctuation_count` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_punctuation_count("O'Brien")` returns `2`
**And** `"greeting_punctuation_count"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that only the 32 ASCII `string.punctuation` characters are counted, with non-ASCII look-alikes excluded
- that the count covers the complete greeting, including the prefix comma
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_punctuation_count(name: str) -> int` returning the number of characters of `greet(name)` that are in Python's `string.punctuation` | Must |
| FR2 | Never count non-ASCII punctuation or look-alikes, letters, digits, or whitespace | Must |
| FR3 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR4 | Export `greeting_punctuation_count` from `nmg_sdlc_smoke`, list it in `__all__`, and document it in the README Library section without removing existing exports | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A Unicode-category-aware punctuation count
- A boolean punctuation-presence probe
- A CLI flag or option exposing the punctuation count
- Counting punctuation in the name alone rather than the completed greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #233 | 2026-10-24 | Initial feature spec |
