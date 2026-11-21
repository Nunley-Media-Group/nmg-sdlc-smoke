# Requirements: Add greeting_longest_word library helper

**Issue**: #335
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_longest_word(name)` helper that returns the longest whitespace-separated word of the completed greeting
**So that** I can get the greeting's longest word without re-implementing the greeting, the word-splitting rule, or the tie rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_longest_word` returns one `str` taken from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- Length is the number of Unicode code points (`len(word)`). No normalization is applied. Punctuation that is part of a word counts toward its length, so `Hello,` has length 6.
- When several words share the greatest length, the first one in greeting order is returned. The greeting always contains `Hello,`, so the result is never shorter than 6 code points.

## Acceptance Criteria

### AC1: Return the longest word for simple and multi-word greetings

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_longest_word` with each name
**Then** they return `"Hello,"`, `"Lovelace"`, and `"Hello,"` respectively
**And** `type(result) is str` for each result

### AC2: Return the first word on a length tie

**Given** the valid name `Bertha`, whose greeting words `Hello,` and `Bertha` are both 6 code points long
**When** a caller invokes `greeting_longest_word("Bertha")`
**Then** it returns `"Hello,"`

### AC3: Split on any whitespace

**Given** the valid names `"Ada\tLovelace"`, `" Ada "`, and `"Ada  Lovelace"`
**When** a caller invokes `greeting_longest_word` with each name
**Then** they return `"Lovelace"`, `"Hello,"`, and `"Lovelace"` respectively

### AC4: Measure code points without normalization

**Given** the valid names `"Chlo\u00e9e"` (precomposed, 6 code points) and `"Chloe\u0301e"` (decomposed, 7 code points)
**When** a caller invokes `greeting_longest_word` with each name
**Then** `greeting_longest_word("Chlo\u00e9e")` returns `"Hello,"` (because of the tie rule)
**And** `greeting_longest_word("Chloe\u0301e")` returns `"Chloe\u0301e"` unchanged

### AC5: Agree with the existing word helpers

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `Bertha`, `O'Brien-Smith`, and `"Chloe\u0301e"`
**When** a caller invokes `greeting_longest_word` with each name
**Then** the result is an element of `greeting_words(name)`
**And** `len(result)` equals `max(greeting_word_lengths(name))`

### AC6: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_longest_word` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC7: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_longest_word` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** the README example `greeting_longest_word("Ada")` prints `Hello,`
**And** `"greeting_longest_word"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, the code-point length rule, the first-wins tie rule, and the inherited `ValueError("name must not be blank")`
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_longest_word(name: str) -> str` that returns the longest `str.split()` word of `greet(name)`, measured by `len` with no normalization, choosing the first word on a tie | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_longest_word` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, the other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A shortest-word helper, an average-word-length helper, or a helper that returns all tied words
- Byte, UTF-16, or grapheme-cluster word lengths
- Stripping punctuation from words before measuring them
- Measuring the name alone instead of the complete greeting
- Any new or changed `nmg-smoke` CLI option

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #335 | 2026-11-20 | Initial feature spec |
