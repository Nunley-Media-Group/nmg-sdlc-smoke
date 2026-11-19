# Requirements: Add greeting_initials library helper

**Issue**: #323
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/319-add-greeting-words-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_initials(name)` helper that returns the first character of each whitespace-separated word of the completed greeting
**So that** I can get a compact initials string for a greeting without re-implementing the greeting or its splitting rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper returns a `str` equal to `"".join(word[0] for word in greet(name).split())`. That is the first character of each word of the complete greeting, in order, with the original case preserved and no separator. It uses the same splitting rule as `greeting_words` and `greeting_word_count`, so `len(greeting_initials(name)) == greeting_word_count(name)` for every valid name. The first initial is always `H` from `Hello,`.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

`greeting_words` returns the greeting's words, but no helper returns their initials.

## Acceptance Criteria

### AC1: Return initials for single-word names

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_initials` with each name
**Then** the calls return the `str` values `"HA"` and `"HZ"` respectively

### AC2: Handle multi-word names, whitespace runs, and preserve case

**Given** the valid names `Ada Lovelace`, `Ada \t Lovelace`, and `ada lovelace`
**When** a caller invokes `greeting_initials` with each name
**Then** the calls return `"HAL"`, `"HAL"`, and `"Hal"` respectively
**And** each result length equals `greeting_word_count(name)`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_initials` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_initials` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_initials("Ada")` returns `"HA"`
**And** `"greeting_initials"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the case-preserving initials of the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_initials(name: str) -> str` returning `"".join(word[0] for word in greet(name).split())` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_initials` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, `greeting_words`, `greeting_word_count`, other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Uppercasing, lowercasing, or otherwise transforming the initials
- Separators or punctuation between initials (for example `H.A.`)
- Skipping leading punctuation within a word (a word starting with `'` contributes `'`)
- Initials of the name alone instead of the complete greeting
- Unicode normalization of names

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #323 | 2026-11-19 | Initial feature spec |
