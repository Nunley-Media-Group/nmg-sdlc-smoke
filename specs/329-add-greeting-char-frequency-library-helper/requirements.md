# Requirements: Add greeting_char_frequency library helper

**Issue**: #329
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_char_frequency(name)` helper that returns how many times each character occurs in the completed greeting
**So that** I can inspect the greeting's character distribution without re-implementing the greeting or the counting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_char_frequency` returns a plain `dict[str, int]` built from the complete greeting (not the name alone):

- Each key is one character (one Unicode code point) of the greeting. Its value is how many times that character occurs.
- Keys are case-sensitive: `A` and `a` are separate keys.
- Keys appear in the order each character first occurs in the greeting.
- No Unicode normalization is applied. A precomposed `"\u00eb"` and a decomposed `"e\u0308"` are each counted as their own code points.
- Every character counts, including the comma, spaces, punctuation, and digits.

Because of these rules, the values always sum to `greeting_length(name)`, and the number of keys always equals `greeting_unique_char_count(name)`.

## Acceptance Criteria

### AC1: Count characters of simple and multi-word greetings in first-seen order

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_char_frequency` with each name
**Then** `greeting_char_frequency("Ada")` returns `{"H": 1, "e": 1, "l": 2, "o": 1, ",": 1, " ": 1, "A": 1, "d": 1, "a": 1}`
**And** `greeting_char_frequency("Ada Lovelace")` returns `{"H": 1, "e": 3, "l": 3, "o": 2, ",": 1, " ": 2, "A": 1, "d": 1, "a": 2, "L": 1, "v": 1, "c": 1}`
**And** `list(result)` matches the keys in exactly the order listed
**And** `type(result) is dict`

### AC2: Keep case and non-ASCII characters distinct without normalization

**Given** the valid names `"Zo\u00eb"` (precomposed) and `"Zoe\u0308"` (decomposed)
**When** a caller invokes `greeting_char_frequency` with each name
**Then** the first result has `"\u00eb": 1` and `"e": 1`
**And** the second result has `"e": 2` and `"\u0308": 1`, with no `"\u00eb"` key
**And** in both results `"H"` and `"h"` are counted separately (`"H": 1`, no `"h"` key)

### AC3: Agree with the existing length and unique-count helpers

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `O'Brien`, `"Zo\u00eb"`, and `"Ada\u674eLee"`
**When** a caller invokes `greeting_char_frequency` with each name
**Then** `sum(result.values())` equals `greeting_length(name)`
**And** `len(result)` equals `greeting_unique_char_count(name)`
**And** every value is a positive `int`

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_char_frequency` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC5: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_char_frequency` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** the README example `greeting_char_frequency("Ada")` returns the AC1 result
**And** `"greeting_char_frequency"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents case-sensitive keys, first-seen key order, no normalization, counting every character of the complete greeting, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_char_frequency(name: str) -> dict[str, int]` that returns a plain `dict` mapping each code point of `greet(name)` to its occurrence count, case-sensitive, keys in first-occurrence order, with no normalization | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_char_frequency` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Case-insensitive, casefolded, or normalized counting modes
- Sorting by count or code point, or top-N / most-common queries
- Counting grapheme clusters or words instead of code points
- Counting the name alone instead of the complete greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #329 | 2026-11-19 | Initial feature spec |
