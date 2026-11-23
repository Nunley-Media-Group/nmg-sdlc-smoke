# Requirements: Add greeting_capitalize library helper

**Issue**: #365
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_capitalize(name)` helper that returns the completed greeting with only its first character uppercased and every other character lowercased
**So that** I can get a sentence-case greeting without re-implementing the greeting or the case rule

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_capitalize` returns `str.capitalize()` of the complete greeting (not the name alone), including the `Hello, ` prefix. Because the greeting always starts with `H`, the result is always `Hello, ` followed by the name lowercased with Python's `str.lower()` rules. Uncased characters (punctuation, digits, whitespace) are unchanged, and no Unicode normalization is applied.

## Acceptance Criteria

### AC1: Lowercase everything after the first character

**Given** the valid names `Ada`, `Ada Lovelace`, `ADA`, and `ada lovelace`
**When** a caller invokes `greeting_capitalize` with each name
**Then** they return `Hello, ada`, `Hello, ada lovelace`, `Hello, ada`, and `Hello, ada lovelace` respectively
**And** each result is a `str`

### AC2: Leave uncased characters and non-ASCII letters to str.capitalize

**Given** the valid names `O'BRIEN-SMITH`, `Ada 42`, `\N{LATIN CAPITAL LETTER E WITH ACUTE}MILE`, and `" Ada "`
**When** a caller invokes `greeting_capitalize` with each name
**Then** they return `Hello, o'brien-smith`, `Hello, ada 42`, `Hello, \N{LATIN SMALL LETTER E WITH ACUTE}mile`, and `Hello,  ada ` respectively
**And** for every name above the result equals `greet(name).capitalize()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_capitalize` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_capitalize` and follows the README example
**Then** the import succeeds and the README example `greeting_capitalize("Ada Lovelace")` gives `Hello, ada lovelace`
**And** `"greeting_capitalize"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents that it applies `str.capitalize()` to the complete greeting, applies no Unicode normalization, and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_capitalize(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `greet(name).capitalize()` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_capitalize` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_capitalize` in the README Library section (import list, usage example, behavior sentence) consistent with the other case helpers | Should |

## Out of Scope

- A new `nmg-smoke --capitalize` CLI flag or any CLI change
- Changes to `greet`, `greeting_casefold`, `greeting_swapcase`, `greeting_titlecase`, or other existing helpers
- Unicode normalization of the result

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #365 | 2026-11-23 | Initial feature spec |
