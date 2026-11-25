# Requirements: Add greeting_uppercase library helper

**Issue**: #371
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_uppercase(name)` helper that returns the completed greeting converted to upper case
**So that** I can get an upper-case greeting from the library without re-implementing the greeting or calling the CLI `--uppercase` flag

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_uppercase` returns `greet(name).upper()`. It converts the complete greeting (not the name alone), including the `Hello, ` prefix. It uses Python's full Unicode upper-casing, so characters whose upper-case form is longer expand (for example `ß` becomes `SS`). Characters without case, such as digits, punctuation, and whitespace, are unchanged, and no Unicode normalization is applied.

## Acceptance Criteria

### AC1: Upper-case a plain greeting

**Given** the valid names `Ada`, `ada lovelace`, and `Agent 007`
**When** a caller invokes `greeting_uppercase` with each name
**Then** they return `"HELLO, ADA"`, `"HELLO, ADA LOVELACE"`, and `"HELLO, AGENT 007"` respectively
**And** `type(result) is str` for each result

### AC2: Apply full Unicode upper-casing and keep uncased characters

**Given** the valid names `straße`, `émile`, and `Ada\tBo` (containing a literal tab character)
**When** a caller invokes `greeting_uppercase` with each name
**Then** they return `"HELLO, STRASSE"`, `"HELLO, ÉMILE"`, and `"HELLO, ADA\tBO"` respectively
**And** for every valid name above the result equals `greet(name).upper()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_uppercase` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_uppercase` and follows the README example
**Then** the import succeeds and the README example `greeting_uppercase("Ada")` gives `"HELLO, ADA"`
**And** `"greeting_uppercase"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents that it applies `str.upper()` to the complete greeting and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_uppercase(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `greet(name).upper()` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_uppercase` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_uppercase` in the README Library section (import list, usage example, behavior sentence) consistent with the other case helpers | Should |

## Out of Scope

- Any change to the `nmg-smoke --uppercase` CLI flag or other CLI behavior
- A `greeting_lowercase` helper or any other new case transform
- Locale-specific upper-casing rules beyond Python's `str.upper()`
- Changes to `greet`, `greeting_capitalize`, `greeting_uppercase_count`, or other existing helpers

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #371 | 2026-11-25 | Initial feature spec |
