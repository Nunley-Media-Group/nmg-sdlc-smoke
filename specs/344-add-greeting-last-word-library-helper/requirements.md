# Requirements: Add greeting_last_word library helper

**Issue**: #344
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_last_word(name)` helper that returns the final whitespace-separated word of the completed greeting
**So that** I can get the greeting's last word without re-implementing the greeting or the word-splitting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_last_word` returns one `str` taken from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- The result is the last of those words, returned unchanged: punctuation attached to the word is kept, and no case change or Unicode normalization is applied.
- The greeting always has at least two words, so a last word always exists.

## Acceptance Criteria

### AC1: Return the last word for single- and multi-word names

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_last_word` with each name
**Then** they return `"Ada"`, `"Lovelace"`, and `"007"` respectively
**And** `type(result) is str` for each result

### AC2: Split on any whitespace

**Given** the valid names `"Ada\tLovelace"`, `" Ada "`, and `"Bo  Al\n"`
**When** a caller invokes `greeting_last_word` with each name
**Then** they return `"Lovelace"`, `"Ada"`, and `"Al"` respectively

### AC3: Return the word unchanged

**Given** the valid names `"Ada!"`, `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_last_word` with each name
**Then** they return `"Ada!"`, `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"` (6 code points, not normalized) respectively

### AC4: Agree with greeting_words

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `"Ada\tLovelace"`, `O'Brien-Smith`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_last_word` with each name
**Then** the result equals `greeting_words(name)[-1]`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_last_word` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC6: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_last_word` and follows the README example
**Then** the import succeeds and the README example `greeting_last_word("Ada Lovelace")` prints `Lovelace`
**And** `"greeting_last_word"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, the unchanged last word, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_last_word(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning the last `str.split()` word of `greet(name)` unchanged | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_last_word` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_last_word` in the README Library section (import list, usage example, behavior sentence) consistent with the other word helpers | Should |

## Out of Scope

- A `greeting_first_word` helper or any other new word helper
- Changes to `greet`, `greeting_words`, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for the last word

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #344 | 2026-11-22 | Initial feature spec |
