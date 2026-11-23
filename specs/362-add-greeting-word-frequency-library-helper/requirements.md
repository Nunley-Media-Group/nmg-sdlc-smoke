# Requirements: Add greeting_word_frequency library helper

**Issue**: #362
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_word_frequency(name)` helper that maps each whitespace-separated word of the completed greeting to how many times it occurs
**So that** I can count repeated words in a greeting without re-implementing the greeting or the word-splitting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_word_frequency` returns a new plain `dict[str, int]` built from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- Each key is one word, unchanged: attached punctuation is kept (the first key is always `Hello,`), and no case folding or Unicode normalization is applied. `Bo` and `bo` are separate keys.
- Keys appear in the order each word first occurs in the greeting. Each value is how many times that word occurs.

Because of these rules, the values always sum to `greeting_word_count(name)`.

## Acceptance Criteria

### AC1: Count words in first-seen order

**Given** the valid names `Ada`, `Ada Lovelace`, and `Bo Bo`
**When** a caller invokes `greeting_word_frequency` with each name
**Then** they return `{"Hello,": 1, "Ada": 1}`, `{"Hello,": 1, "Ada": 1, "Lovelace": 1}`, and `{"Hello,": 1, "Bo": 2}` respectively
**And** `list(result)` matches the keys in exactly the order listed
**And** `type(result) is dict`

### AC2: Split on any whitespace

**Given** the valid names `"Bo\tBo"`, `" Ada "`, and `"Bo  Al\nBo"`
**When** a caller invokes `greeting_word_frequency` with each name
**Then** they return `{"Hello,": 1, "Bo": 2}`, `{"Hello,": 1, "Ada": 1}`, and `{"Hello,": 1, "Bo": 2, "Al": 1}` respectively

### AC3: Keep words exact

**Given** the valid names `"Bo bo"`, `"Hello Hello,"`, and `"Chloe\N{COMBINING ACUTE ACCENT} Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`
**When** a caller invokes `greeting_word_frequency` with each name
**Then** they return `{"Hello,": 1, "Bo": 1, "bo": 1}`, `{"Hello,": 2, "Hello": 1}`, and `{"Hello,": 1, "Chloe\N{COMBINING ACUTE ACCENT}": 1, "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}": 1}` respectively

### AC4: Agree with the existing word helpers

**Given** the valid names `Ada`, `Bo Bo`, `"Bo  Al\nBo"`, `O'Brien-Smith`, and `"Hello Hello,"`
**When** a caller invokes `greeting_word_frequency` with each name
**Then** `sum(result.values())` equals `greeting_word_count(name)`
**And** `list(result)` equals the words of `greeting_words(name)` with later duplicates removed, in order

### AC5: Return a new dict on each call

**Given** the valid name `Ada`
**When** a caller invokes `greeting_word_frequency("Ada")` twice and mutates the first result
**Then** the second result is unchanged and is not the same object as the first

### AC6: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_word_frequency` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC7: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_word_frequency` and follows the README example
**Then** the import succeeds and the README example `greeting_word_frequency("Bo Bo")` shows `{"Hello,": 1, "Bo": 2}`
**And** `"greeting_word_frequency"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, exact case-sensitive keys, first-seen ordering, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_word_frequency(name: str) -> dict[str, int]` to `src/nmg_sdlc_smoke/greet.py`, returning a new dict counting each `str.split()` word of `greet(name)`, unchanged and case-sensitive, keyed in first-seen order | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_word_frequency` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_word_frequency` in the README Library section (import list, usage example, behavior sentence) consistent with `greeting_char_frequency` | Should |

## Out of Scope

- Case-insensitive, normalized, or punctuation-stripped word counting
- Sorting by count, top-N results, or returning `collections.Counter`
- Changes to `greet`, `greeting_words`, `greeting_char_frequency`, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for word frequency

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #362 | 2026-11-23 | Initial feature spec |
