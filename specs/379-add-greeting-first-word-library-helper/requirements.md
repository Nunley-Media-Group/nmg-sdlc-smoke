# Requirements: Add greeting_first_word library helper

**Issue**: #379
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_first_word(name)` helper that returns the first whitespace-separated word of the completed greeting
**So that** I can get the greeting's opening word without re-implementing the greeting or the word-splitting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_first_word` returns one `str` taken from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- The result is the first of those words, returned unchanged: the attached comma is kept, and no case change or Unicode normalization is applied.
- The greeting always begins with `Hello, `, so for every valid name the result is `"Hello,"`.

## Acceptance Criteria

### AC1: Return the first word for single- and multi-word names

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_first_word` with each name
**Then** each returns `"Hello,"`
**And** `type(result) is str` for each result

### AC2: Split on any whitespace and keep the word unchanged

**Given** the valid names `"Ada\tLovelace"`, `" Ada "`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_first_word` with each name
**Then** each returns `"Hello,"` (6 code points, comma kept)

### AC3: Agree with greeting_words

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `"Ada\tLovelace"`, `" Ada "`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_first_word` with each name
**Then** the result equals `greeting_words(name)[0]`

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_first_word` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC5: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_first_word` and follows the README example
**Then** the import succeeds and the README example `greeting_first_word("Ada Lovelace")` prints `Hello,`
**And** `"greeting_first_word"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, the unchanged first word, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_first_word(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning the first `str.split()` word of `greet(name)` unchanged | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_first_word` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_first_word` in the README Library section (import list, usage example, behavior sentence) consistent with the other word helpers | Should |

## Out of Scope

- A new `nmg-smoke` CLI flag or option for the first word
- Changes to `greet`, `greeting_words`, `greeting_last_word`, or other existing helpers
- Any other new word helper (for example nth-word lookup)

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #379 | 2026-11-25 | Initial feature spec |
