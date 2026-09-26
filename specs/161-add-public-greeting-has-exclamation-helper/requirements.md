# Requirements: Add public greeting_has_exclamation helper

**Issue**: #161
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer using the Python greeting library
**I want** a public `greeting_has_exclamation(name)` helper
**So that** I can determine whether the completed greeting contains a literal exclamation mark

## Background

`greet(name)` returns `Hello, {name}` for a valid name and validates the input. Existing punctuation queries inspect the completed greeting; `greeting_ends_with_exclamation` instead appends a mark and returns a string. The new query inspects the original complete greeting without altering it.

## Acceptance Criteria

### AC1: Detect a literal exclamation mark

**Given** the installed public package and a valid name `Ada!`
**When** `greeting_has_exclamation("Ada!")` is called
**Then** it returns the Python boolean `True`, because `greet("Ada!")` is `"Hello, Ada!"` and contains literal `!`.

### AC2: Report absence of a literal exclamation mark

**Given** valid names `Ada` and `Ada！` (fullwidth punctuation)
**When** `greeting_has_exclamation` is called with each name through the public import
**Then** it returns the Python boolean `False` for both, because neither completed greeting contains literal `!`.

### AC3: Preserve name validation

**Given** invalid names `""`, `" "`, `None`, and `42`
**When** `greeting_has_exclamation` is called with each name
**Then** each call raises `ValueError` with the exact message `name must not be blank`, as `greet` does.

### AC4: Expose and document the helper

**Given** an installed package and its README Library section
**When** a caller imports `greeting_has_exclamation` from `nmg_sdlc_smoke` and follows the README examples
**Then** the public helper returns `True` for `Ada!` and `False` for `Ada`, and the README states its inherited invalid-name behavior.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_exclamation(name: str) -> bool` returning whether the complete `greet(name)` result contains literal `!`. | Must |
| FR2 | Export the helper from `nmg_sdlc_smoke` without changing existing exports. | Must |
| FR3 | Propagate `greet`'s `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. | Must |
| FR4 | Document the public import, true/false examples, and inherited validation in README's Library section. | Must |

## Out of Scope

- Changing `greet` output, CLI behavior, or the punctuation-appending helper; matching exclamation-like Unicode punctuation rather than literal `!`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #161 | 2026-09-26 | Initial feature spec |
