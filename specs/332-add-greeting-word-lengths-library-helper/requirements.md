# Requirements: Add greeting_word_lengths library helper

**Issue**: #332
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_word_lengths(name)` helper that returns the length of each whitespace-separated word of the completed greeting
**So that** I can inspect the greeting's word sizes without re-implementing the greeting, the word-splitting rule, or the length rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_word_lengths` returns a new plain `list[int]` built from the complete greeting (not the name alone):

- Words are split the same way as `greeting_words`: `str.split()` with no arguments. Any run of Unicode whitespace separates words, and leading or trailing whitespace adds no empty words.
- Each value is the number of Unicode code points in that word (`len(word)`). Punctuation that is part of a word counts toward its length. For example, `Hello,` has length 6.
- Values appear in the same order as the words in the greeting.
- No Unicode normalization is applied. A precomposed `"\u00eb"` counts as one code point. A decomposed `"e\u0308"` counts as two.

Because of these rules, the result always equals `[len(w) for w in greeting_words(name)]`, and its length always equals `greeting_word_count(name)`.

## Acceptance Criteria

### AC1: Return per-word lengths for simple and multi-word greetings

**Given** the valid names `Ada`, `Ada Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_word_lengths` with each name
**Then** `greeting_word_lengths("Ada")` returns `[6, 3]`
**And** `greeting_word_lengths("Ada Lovelace")` returns `[6, 3, 8]`
**And** `greeting_word_lengths("Agent 007")` returns `[6, 5, 3]`
**And** `type(result) is list` and every element is an `int`

### AC2: Split on any whitespace without producing empty words

**Given** the valid names `"Ada\tLee"`, `" Ada "`, and `"Ada  Lee"`
**When** a caller invokes `greeting_word_lengths` with each name
**Then** `greeting_word_lengths("Ada\tLee")` returns `[6, 3, 3]`
**And** `greeting_word_lengths(" Ada ")` returns `[6, 3]`
**And** `greeting_word_lengths("Ada  Lee")` returns `[6, 3, 3]`
**And** no result contains `0`

### AC3: Count code points without normalization

**Given** the valid names `"Zo\u00eb"` (precomposed), `"Zoe\u0308"` (decomposed), and `"Ada\U0001F600"` (a character outside the Basic Multilingual Plane)
**When** a caller invokes `greeting_word_lengths` with each name
**Then** they return `[6, 3]`, `[6, 4]`, and `[6, 4]` respectively

### AC4: Agree with the existing word helpers

**Given** the valid names `Ada`, `Ada Lovelace`, `Agent 007`, `O'Brien`, `"Ada\tLee"`, and `"Zoe\u0308"`
**When** a caller invokes `greeting_word_lengths` with each name
**Then** the result equals `[len(w) for w in greeting_words(name)]`
**And** `len(result)` equals `greeting_word_count(name)`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_word_lengths` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC6: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_word_lengths` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** the README example `greeting_word_lengths("Ada")` returns `[6, 3]`
**And** `"greeting_word_lengths"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the whitespace split rule, code-point lengths, in-order values, no normalization, use of the complete greeting, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_word_lengths(name: str) -> list[int]` that returns a new `list` of the code-point lengths of each `str.split()` word of `greet(name)`, in order, with no normalization | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_word_lengths` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Byte, UTF-16, or grapheme-cluster word lengths
- Stripping punctuation from words before measuring them
- Measuring the name alone instead of the complete greeting
- Aggregates such as longest word, shortest word, or average word length

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #332 | 2026-11-20 | Initial feature spec |
