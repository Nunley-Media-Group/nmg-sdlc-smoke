# Requirements: Add public greeting_has_double_quote helper

**Issue**: #171
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public predicate for a literal double quote in the completed greeting
**So that** I can query that greeting without duplicating the check.

## Background

`greet(name)` returns `Hello, {name}` for valid strings and raises `ValueError("name must not be blank")` for blank or non-string names. Existing literal-character predicates inspect the completed greeting. This predicate checks literal `"` without changing the greeting.

## Acceptance Criteria

### AC1: Detect a literal double quote

**Given** a valid name `Ada"`
**When** a caller invokes `greeting_has_double_quote('Ada"')`
**Then** it returns Python `True` because `greet('Ada"')` is `Hello, Ada"` and contains literal `"` (U+0022).

### AC2: Report absence of a literal double quote

**Given** valid names `Ada` and `Ada＂` (fullwidth quotation mark, U+FF02)
**When** a caller invokes `greeting_has_double_quote` with each name
**Then** it returns Python `False` for both because neither completed greeting contains literal `"` (U+0022).

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_has_double_quote` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Expose and document the helper

**Given** an installed `nmg_sdlc_smoke` package and its README Library section
**When** a caller imports `greeting_has_double_quote` from `nmg_sdlc_smoke` and follows the README examples
**Then** `greeting_has_double_quote('Ada"')` returns `True` and `greeting_has_double_quote("Ada")` returns `False`, and the README documents the inherited invalid-name error.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_double_quote(name: str) -> bool` returning whether the completed `greet(name)` contains literal `"` (U+0022). | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and document its public import, true/false examples, and inherited validation in README Library. | Must |

## Out of Scope

- Changing `greet` output or `nmg-smoke --quotes` CLI behavior; treating fullwidth `＂` as literal `"`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #171 | 2026-09-26 | Initial feature spec |
