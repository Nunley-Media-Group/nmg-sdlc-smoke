# Requirements: Add greeting_words library helper

**Issue**: #319
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/93-add-greeting-word-count-lifecycle-fixture/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_words(name)` helper that returns the whitespace-separated words of the completed greeting
**So that** I can work with the greeting's individual words without re-implementing the greeting or its splitting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper returns a new `list[str]` equal to `greet(name).split()`: the complete greeting split on runs of any whitespace, with no empty items. This is the same splitting rule `greeting_word_count` uses, so `len(greeting_words(name)) == greeting_word_count(name)` for every valid name. Punctuation stays attached, so the first word is always `Hello,`.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

`greeting_word_count` returns how many words the greeting has, but no helper returns the words themselves.

## Acceptance Criteria

### AC1: Return the greeting's words for single-word names

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_words` with each name
**Then** the calls return the `list[str]` values `["Hello,", "Ada"]` and `["Hello,", "Zoë"]` respectively
**And** each result equals `greet(name).split()`

### AC2: Split multi-word names on any whitespace run

**Given** the valid names `Ada Lovelace` and `Ada \t Lovelace`
**When** a caller invokes `greeting_words` with each name
**Then** both calls return `["Hello,", "Ada", "Lovelace"]`
**And** each result length equals `greeting_word_count(name)`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_words` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_words` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_words("Ada")` returns `["Hello,", "Ada"]`
**And** `"greeting_words"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the word list of the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_words(name: str) -> list[str]` returning a new list equal to `greet(name).split()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_words` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, `greeting_word_count`, other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Splitting on custom separators or stripping punctuation from words (the first word stays `Hello,`)
- Words of the name alone instead of the complete greeting
- Unicode normalization of names

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #319 | 2026-11-15 | Initial feature spec |
