# Requirements: Add greeting_titlecase library helper

**Issue**: #353
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_titlecase(name)` helper that returns the complete greeting title-cased
**So that** I can get the same title-cased greeting that `nmg-smoke --titlecase` prints without reimplementing it

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_titlecase` returns one `str`: Python `str.title()` applied to the complete greeting (not the name alone). Each run of letters starts with an uppercase character, and the rest of the run is lowercase. A letter that follows a digit or an apostrophe also starts a new run. Whitespace is kept unchanged, and no Unicode normalization is applied.

## Acceptance Criteria

### AC1: Title-case single- and multi-word names

**Given** the valid names `ada`, `ADA LOVELACE`, and `ada lovelace`
**When** a caller invokes `greeting_titlecase` with each name
**Then** they return `"Hello, Ada"`, `"Hello, Ada Lovelace"`, and `"Hello, Ada Lovelace"` respectively
**And** `type(result) is str` for each result

### AC2: Follow str.title() rules for apostrophes, digits, and non-ASCII letters

**Given** the valid names `"o'brien"`, `"agent 007x"`, and `"åsa"`
**When** a caller invokes `greeting_titlecase` with each name
**Then** they return `"Hello, O'Brien"`, `"Hello, Agent 007X"`, and `"Hello, Åsa"` respectively

### AC3: Agree with greet and the CLI flag

**Given** the valid names `ada`, `ADA LOVELACE`, `"o'brien"`, and `"Ada\tLovelace"`
**When** a caller invokes `greeting_titlecase` with each name
**Then** the result equals `greet(name).title()`
**And** for `ada` it equals the stdout of `nmg-smoke --titlecase ada` without the trailing newline

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_titlecase` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC5: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_titlecase` and follows the README example
**Then** the import succeeds and the README example `greeting_titlecase("ada lovelace")` prints `Hello, Ada Lovelace`
**And** `"greeting_titlecase"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the `str.title()` rule and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_titlecase(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `greet(name).title()` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_titlecase` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_titlecase` in the README Library section (import list, usage example, behavior sentence) consistent with the other case helpers | Should |

## Out of Scope

- Changes to the `nmg-smoke --titlecase` flag or any other CLI behavior
- Changes to `greet`, `greeting_is_title`, `greeting_casefold`, `greeting_swapcase`, or other existing helpers
- Separate `greeting_uppercase` or `greeting_lowercase` library helpers
- Smarter title-casing than `str.title()` (for example, keeping `McAdam` or lowercasing letters after apostrophes)

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #353 | 2026-11-23 | Initial feature spec |
