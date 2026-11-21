# Requirements: Add greeting_shortest_word library helper

**Issue**: #338
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_shortest_word(name)` helper that returns the shortest whitespace-separated word of the completed greeting
**So that** I can get the greeting's shortest word without re-implementing the greeting, the word-splitting rule, or the tie rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_shortest_word` returns one `str` taken from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- Length is the number of Unicode code points (`len(word)`). No normalization is applied. Punctuation that is part of a word counts toward its length, so `Hello,` has length 6.
- When several words share the smallest length, the first one in greeting order is returned. This is the same tie rule as `greeting_longest_word`. The greeting always contains `Hello,`, so the result is never longer than 6 code points.

## Acceptance Criteria

### AC1: Return the shortest word for simple and multi-word greetings

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_shortest_word` with each name
**Then** they return `"Ada"`, `"Ada"`, and `"007"` respectively
**And** `type(result) is str` for each result

### AC2: Return the first word on a length tie

**Given** the valid names `Bertha` (greeting words `Hello,` and `Bertha`, both 6 code points) and `Bo Al` (greeting words `Hello,`, `Bo`, and `Al`)
**When** a caller invokes `greeting_shortest_word` with each name
**Then** `greeting_shortest_word("Bertha")` returns `"Hello,"`
**And** `greeting_shortest_word("Bo Al")` returns `"Bo"`

### AC3: Return the greeting word when every name word is longer

**Given** the valid name `Lovelace`
**When** a caller invokes `greeting_shortest_word("Lovelace")`
**Then** it returns `"Hello,"`

### AC4: Split on any whitespace

**Given** the valid names `"Ada\tLovelace"`, `" Ada "`, and `"Bo  Al"`
**When** a caller invokes `greeting_shortest_word` with each name
**Then** they return `"Ada"`, `"Ada"`, and `"Bo"` respectively

### AC5: Measure code points without normalization

**Given** the valid names `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` (precomposed, 5 code points) and `"Chloe\N{COMBINING ACUTE ACCENT}"` (decomposed, 6 code points)
**When** a caller invokes `greeting_shortest_word` with each name
**Then** `greeting_shortest_word("Chlo\N{LATIN SMALL LETTER E WITH ACUTE}")` returns `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` unchanged
**And** `greeting_shortest_word("Chloe\N{COMBINING ACUTE ACCENT}")` returns `"Hello,"` (because of the tie rule)

### AC6: Agree with the existing word helpers

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `Bertha`, `Bo Al`, `O'Brien-Smith`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_shortest_word` with each name
**Then** the result is an element of `greeting_words(name)`
**And** `len(result)` equals `min(greeting_word_lengths(name))`

### AC7: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_shortest_word` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC8: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_shortest_word` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** the README example `greeting_shortest_word("Ada")` prints `Ada`
**And** `"greeting_shortest_word"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, the code-point length rule, the first-wins tie rule, and the inherited `ValueError("name must not be blank")`
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_shortest_word(name: str) -> str` that returns the shortest `str.split()` word of `greet(name)`, measured by `len` with no normalization, choosing the first word on a tie | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_shortest_word` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, `greeting_longest_word`, the other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- An average-word-length helper, or a helper that returns all tied words
- Byte, UTF-16, or grapheme-cluster word lengths
- Stripping punctuation from words before measuring them
- Measuring the name alone instead of the complete greeting
- Any new or changed `nmg-smoke` CLI option

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #338 | 2026-11-20 | Initial feature spec |
