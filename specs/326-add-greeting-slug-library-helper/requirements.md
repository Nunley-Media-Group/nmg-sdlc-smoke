# Requirements: Add greeting_slug library helper

**Issue**: #326
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_slug(name)` helper that returns a lowercase ASCII, hyphen-separated slug of the completed greeting
**So that** I can use a greeting as a URL- or filename-safe identifier without re-implementing the greeting or the slug rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_slug` builds a `str` from the complete greeting (not the name alone) in four steps:

1. Apply Unicode NFKD normalization and remove combining marks, so accented letters become their ASCII base (`ë` → `e`) and compatibility forms fold (fullwidth `Ａ` → `A`).
2. Lowercase the result.
3. Replace every run of one or more characters that are not ASCII `a`–`z` or `0`–`9` with a single `-`.
4. Remove leading and trailing `-`.

Characters with no ASCII base after step 1 (for example `李`) act as separators. Because every greeting starts with `Hello`, the result is never empty and always starts with `hello`.

Each public helper has a definition in `src/nmg_sdlc_smoke/greet.py`, a self-aliased re-export from `nmg_sdlc_smoke`, an entry in `nmg_sdlc_smoke.__all__`, and a README Library entry with an import, example results, and a prose contract line. No existing helper returns a slug.

## Acceptance Criteria

### AC1: Slug simple and multi-word names

**Given** the valid names `Ada`, `Ada Lovelace`, `Ada \t Lovelace`, and `Agent 007`
**When** a caller invokes `greeting_slug` with each name
**Then** the calls return the `str` values `"hello-ada"`, `"hello-ada-lovelace"`, `"hello-ada-lovelace"`, and `"hello-agent-007"` respectively

### AC2: Collapse punctuation and trim edge separators

**Given** the valid names `O'Brien`, `Ada!!`, `--Ada--`, and `Ada_Lovelace`
**When** a caller invokes `greeting_slug` with each name
**Then** the calls return `"hello-o-brien"`, `"hello-ada"`, `"hello-ada"`, and `"hello-ada-lovelace"` respectively
**And** no result contains `--` or starts or ends with `-`

### AC3: Transliterate accents and separate non-ASCII letters

**Given** the valid names `Zoë` (precomposed U+00EB), `ÉMILE`, `Ａda` (fullwidth U+FF21), and `Ada李Lee`
**When** a caller invokes `greeting_slug` with each name
**Then** the calls return `"hello-zoe"`, `"hello-emile"`, `"hello-ada"`, and `"hello-ada-lee"` respectively
**And** every result matches the pattern `^[a-z0-9]+(-[a-z0-9]+)*$`

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_slug` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC5: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_slug` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_slug("Ada Lovelace")` returns `"hello-ada-lovelace"`
**And** `"greeting_slug"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the NFKD transliteration, lowercasing, single-hyphen separator rule, edge trimming, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_slug(name: str) -> str` that applies NFKD and drops combining marks, lowercases, replaces each run of characters outside `[a-z0-9]` with one `-`, and trims edge `-` from `greet(name)` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_slug` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, other existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- A configurable separator, maximum length, or case option
- Transliterating characters with no NFKD ASCII base (for example `李` → `li` or `ß` → `ss`); they act as separators
- Slugging the name alone instead of the complete greeting

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #326 | 2026-11-19 | Initial feature spec |
