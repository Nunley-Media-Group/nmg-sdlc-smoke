# Requirements: Add greeting_average_word_length library helper

**Issue**: #341
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_average_word_length(name)` helper that returns the mean length of the whitespace-separated words of the completed greeting
**So that** I can get the greeting's average word length without re-implementing the greeting, the word-splitting rule, or the length rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_average_word_length` returns one `float` computed from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`, using `str.split()` with no arguments. Runs of any Unicode whitespace separate words, and no empty words appear.
- Length is the number of Unicode code points (`len(word)`), the same rule as `greeting_word_lengths`. No normalization is applied, and punctuation that is part of a word counts toward its length, so `Hello,` has length 6.
- The result is the total of the word lengths divided by the number of words, returned unrounded as a `float`, even when the mean is a whole number. The greeting always has at least two words, so the division is always defined.

## Acceptance Criteria

### AC1: Return the mean word length for simple and multi-word greetings

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_average_word_length` with each name
**Then** they return `4.5` (`(6 + 3) / 2`), `17 / 3`, and `14 / 3` respectively
**And** `type(result) is float` for each result

### AC2: Return a float when the mean is a whole number

**Given** the valid name `Bertha` (greeting words `Hello,` and `Bertha`, both 6 code points)
**When** a caller invokes `greeting_average_word_length("Bertha")`
**Then** it returns `6.0`
**And** `type(result) is float`

### AC3: Split on any whitespace

**Given** the valid names `"Ada\tLovelace"`, `" Ada "`, and `"Bo  Al"`
**When** a caller invokes `greeting_average_word_length` with each name
**Then** they return `17 / 3`, `4.5`, and `10 / 3` respectively

### AC4: Measure code points without normalization

**Given** the valid names `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` (precomposed, 5 code points) and `"Chloe\N{COMBINING ACUTE ACCENT}"` (decomposed, 6 code points)
**When** a caller invokes `greeting_average_word_length` with each name
**Then** they return `5.5` and `6.0` respectively

### AC5: Agree with the existing word helpers

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `Bertha`, `Bo Al`, `O'Brien-Smith`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_average_word_length` with each name
**Then** the result equals `sum(greeting_word_lengths(name)) / len(greeting_words(name))`
**And** the result is between `len(greeting_shortest_word(name))` and `len(greeting_longest_word(name))` inclusive

### AC6: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_average_word_length` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC7: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_average_word_length` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** the README example `greeting_average_word_length("Ada")` prints `4.5`
**And** `"greeting_average_word_length"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the whitespace split rule, the code-point length rule, the unrounded `float` result, and the inherited `ValueError("name must not be blank")`
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_average_word_length(name: str) -> float` that returns the unrounded mean `len` (no normalization) of the `str.split()` words of `greet(name)` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_average_word_length` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, `greeting_words`, `greeting_word_lengths`, the other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Rounding or formatting the result
- Median, mode, or other word-length statistics
- Byte, UTF-16, or grapheme-cluster word lengths
- Stripping punctuation from words before measuring them
- Measuring the name alone instead of the complete greeting
- Any new or changed `nmg-smoke` CLI option

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #341 | 2026-11-22 | Initial feature spec |
