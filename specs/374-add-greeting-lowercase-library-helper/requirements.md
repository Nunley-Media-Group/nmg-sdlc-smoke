# Requirements: Add greeting_lowercase library helper

**Issue**: #374
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_lowercase(name)` helper that returns the completed greeting converted to lower case
**So that** I can get a lower-case greeting from the library without re-implementing the greeting or calling the CLI `--lowercase` flag

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_lowercase` returns `greet(name).lower()`. It converts the complete greeting (not the name alone), including the `Hello, ` prefix. It uses Python's `str.lower()`, not `str.casefold()`, so `ß` stays `ß`. Characters without case, such as digits, punctuation, and whitespace, are unchanged, and no Unicode normalization is applied.

## Acceptance Criteria

### AC1: Lower-case a plain greeting

**Given** the valid names `Ada`, `ADA LOVELACE`, and `Agent 007`
**When** a caller invokes `greeting_lowercase` with each name
**Then** they return `"hello, ada"`, `"hello, ada lovelace"`, and `"hello, agent 007"` respectively
**And** `type(result) is str` for each result

### AC2: Apply str.lower() rather than case folding and keep uncased characters

**Given** the valid names `Straße`, `ÉMILE`, and `Ada\tBo` (containing a literal tab character)
**When** a caller invokes `greeting_lowercase` with each name
**Then** they return `"hello, straße"`, `"hello, émile"`, and `"hello, ada\tbo"` respectively
**And** for every valid name above the result equals `greet(name).lower()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_lowercase` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_lowercase` and follows the README example
**Then** the import succeeds and the README example `greeting_lowercase("Ada")` gives `"hello, ada"`
**And** `"greeting_lowercase"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README says that it applies `str.lower()` to the complete greeting, matches `nmg-smoke --lowercase` output without the trailing newline, and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_lowercase(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `greet(name).lower()` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_lowercase` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_lowercase` in the README Library section (import list, usage example, behavior sentence), following the other case helpers | Should |

## Out of Scope

- Any change to the `nmg-smoke --lowercase` CLI flag or other CLI behavior
- Any change to `greeting_casefold`, `greeting_uppercase`, `greeting_lowercase_count`, or other existing helpers
- Locale-specific lower-casing rules beyond Python's `str.lower()`

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #374 | 2026-11-25 | Initial feature spec |
