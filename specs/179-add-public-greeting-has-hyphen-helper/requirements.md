# Requirements: Add public greeting_has_hyphen helper

**Issue**: #179
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public predicate for a literal hyphen-minus in the completed greeting
**So that** I can query that greeting without duplicating the check.

## Background

`greet(name)` returns `Hello, {name}` for valid strings and raises `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. Existing literal-character predicates such as `greeting_has_slash`, `greeting_has_underscore`, and `greeting_has_double_quote` query the completed greeting; this predicate checks literal `-` (U+002D) without changing the greeting.

## Acceptance Criteria

### AC1: Detect a literal hyphen-minus

**Given** a valid name `Mary-Jane`
**When** a caller invokes `greeting_has_hyphen("Mary-Jane")`
**Then** it returns Python `True` because `greet("Mary-Jane")` is `Hello, Mary-Jane` and contains literal `-` (U+002D).

### AC2: Report absence of a literal hyphen-minus

**Given** valid names `Ada`, `Ada‐` (hyphen, U+2010), and `Ada–` (en dash, U+2013)
**When** a caller invokes `greeting_has_hyphen` with each name
**Then** it returns Python `False` for all three because none of the completed greetings contains literal `-` (U+002D).

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_has_hyphen` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Expose and document the helper

**Given** an installed `nmg_sdlc_smoke` package and its README Library section
**When** a caller imports `greeting_has_hyphen` from `nmg_sdlc_smoke` and follows the README examples
**Then** `greeting_has_hyphen("Mary-Jane")` returns `True` and `greeting_has_hyphen("Ada")` returns `False`, `greeting_has_hyphen` is listed in `nmg_sdlc_smoke.__all__`, and the README documents the inherited invalid-name error.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_hyphen(name: str) -> bool` returning whether the completed `greet(name)` contains literal `-` (U+002D). | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke`, list it in `__all__`, and document its public import, true/false examples, and inherited validation in README Library. | Must |

## Out of Scope

- Changing `greet` output or `nmg-smoke` CLI behavior; treating Unicode dashes such as `‐` (U+2010), `–` (U+2013), `—` (U+2014), or `−` (U+2212) as literal `-`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #179 | 2026-09-26 | Initial feature spec |
