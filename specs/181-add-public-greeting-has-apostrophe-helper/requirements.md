# Requirements: Add public greeting_has_apostrophe helper

**Issue**: #181
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/171-add-public-greeting-has-double-quote-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public predicate for a literal ASCII apostrophe in the completed greeting
**So that** I can query that greeting without duplicating the check.

## Background

`greet(name)` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. The package already exports literal-character predicates over the completed greeting, such as `greeting_has_slash`, `greeting_has_underscore`, `greeting_has_double_quote`, and `greeting_has_backtick`, each documented in the README Library section with its public import, true/false examples, and inherited validation. No apostrophe predicate exists.

## Acceptance Criteria

### AC1: Detect a literal apostrophe

**Given** a valid name `O'Brien`
**When** a caller invokes `greeting_has_apostrophe("O'Brien")`
**Then** it returns Python `True` because the completed greeting `Hello, O'Brien` contains a literal `'` (U+0027).

### AC2: Report absence of a literal apostrophe

**Given** valid names `Ada`, `O’Brien` (right single quotation mark, U+2019), `OʼBrien` (modifier letter apostrophe, U+02BC), and ``O`Brien`` (grave accent, U+0060)
**When** a caller invokes `greeting_has_apostrophe` with each name
**Then** it returns Python `False` for all four because none of the completed greetings contains a literal `'` (U+0027).

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_has_apostrophe` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_has_apostrophe` from `nmg_sdlc_smoke` and follows the README examples
**Then** `greeting_has_apostrophe("O'Brien")` returns `True`, `greeting_has_apostrophe("Ada")` returns `False`, `greeting_has_apostrophe` appears in `nmg_sdlc_smoke.__all__`, and the README documents the inherited invalid-name error.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_apostrophe(name: str) -> bool`, which returns whether the completed `greet(name)` contains a literal `'` (U+0027). | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and document its public import, true/false examples, and inherited validation in the README Library section. | Must |

## Out of Scope

- Changing `greet` output or any `nmg-smoke` CLI option.
- Treating `’` (U+2019), `‘` (U+2018), `ʼ` (U+02BC), `` ` `` (U+0060), or `′` (U+2032) as a literal `'`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #181 | 2026-09-27 | Initial feature spec |
