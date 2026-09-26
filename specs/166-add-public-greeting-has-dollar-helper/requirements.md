# Requirements: Add public greeting_has_dollar helper

**Issue**: #166
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer using the Python greeting library
**I want** a public boolean helper to detect literal `$` in a completed greeting
**So that** I can query that property without parsing or changing the greeting

## Background

`greet(name)` returns `Hello, {name}` for valid strings and raises `ValueError("name must not be blank")` for blank or non-string names. Existing punctuation predicates query the complete greeting. The new predicate checks literal `$` without altering the greeting.

## Acceptance Criteria

### AC1: Detect a literal dollar sign

**Given** a valid name `Ada$` and the public greeting library
**When** `greeting_has_dollar("Ada$")` is called
**Then** it returns Python `True` because `greet("Ada$")` is `Hello, Ada$` and contains literal `$`.

### AC2: Report absence of a literal dollar sign

**Given** valid names `Ada` and `Ada＄` (fullwidth dollar sign)
**When** `greeting_has_dollar` is called with each name
**Then** it returns Python `False` for both because neither completed greeting contains literal `$`.

### AC3: Preserve name validation

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** `greeting_has_dollar` is called with each name
**Then** each call raises `ValueError` with the exact message `name must not be blank`, as `greet` does.

### AC4: Expose and document the helper

**Given** an installed `nmg_sdlc_smoke` package and its README Library section
**When** a caller imports `greeting_has_dollar` from `nmg_sdlc_smoke` and follows the README examples
**Then** the public helper returns `True` for `Ada$` and `False` for `Ada`, and the README states its inherited invalid-name behavior.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_dollar(name: str) -> bool` returning whether the complete `greet(name)` result contains literal `$`. | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and document its public import, true/false examples, and inherited validation in README's Library section. | Must |

## Out of Scope

- Changing `greet` output or `nmg-smoke` CLI behavior; matching fullwidth `＄` as literal `$`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #166 | 2026-09-26 | Initial feature spec |
