# Requirements: Add public greeting_has_underscore helper

**Issue**: #170
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public predicate for a literal underscore in the completed greeting
**So that** I can query the greeting without duplicating that check.

## Background

`greet(name)` returns `Hello, {name}` for valid strings and raises `ValueError("name must not be blank")` for blank or non-string names. Existing literal-character predicates query the completed greeting; this predicate checks literal `_` without changing the greeting.

## Acceptance Criteria

### AC1: Detect a literal underscore

**Given** a valid name `Ada_`
**When** a caller invokes `greeting_has_underscore("Ada_")`
**Then** it returns Python `True` because `greet("Ada_")` is `Hello, Ada_` and contains literal `_`.

### AC2: Report absence of a literal underscore

**Given** valid names `Ada` and `Ada＿` (fullwidth low line, U+FF3F)
**When** a caller invokes `greeting_has_underscore` with each name
**Then** it returns Python `False` for both because neither completed greeting contains literal `_` (U+005F).

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_has_underscore` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Expose and document the helper

**Given** an installed `nmg_sdlc_smoke` package and its README Library section
**When** a caller imports `greeting_has_underscore` from `nmg_sdlc_smoke` and follows the README examples
**Then** `greeting_has_underscore("Ada_")` returns `True` and `greeting_has_underscore("Ada")` returns `False`, and the README documents the inherited invalid-name error.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_underscore(name: str) -> bool` returning whether the completed `greet(name)` contains literal `_` (U+005F). | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and document its public import, true/false examples, and inherited validation in README Library. | Must |

## Out of Scope

- Changing `greet` output or `nmg-smoke` CLI behavior; treating fullwidth `＿` as literal `_`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #170 | 2026-09-26 | Initial feature spec |
