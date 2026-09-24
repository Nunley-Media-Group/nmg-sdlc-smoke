# Requirements: Add public greeting_has_plus library helper

**Issue**: #144
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** to ask whether a completed greeting contains a literal `+`
**So that** I can inspect the greeting without changing its text.

## Background

`greet(name)` returns `Hello, {name}` for valid names. Existing pure character predicates, including the public `greeting_has_hash`, inspect the completed greeting and propagate `greet`'s name validation.

## Acceptance Criteria

### AC1: Detect a literal plus in the completed greeting

**Given** the public `nmg_sdlc_smoke` library and the valid name `Ada+`
**When** `greeting_has_plus("Ada+")` is called
**Then** it returns the Python boolean `True` because `greet("Ada+")` is `Hello, Ada+`.

### AC2: Report absence of a literal plus

**Given** the public library and the valid name `Ada`
**When** `greeting_has_plus("Ada")` is called
**Then** it returns the Python boolean `False` because `greet("Ada")` is `Hello, Ada` and contains no `+`.

### AC3: Preserve greeting name validation

**Given** each invalid name `""`, `" \t\n"`, `None`, or `42`
**When** `greeting_has_plus` is called with that name
**Then** it raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Preserve existing public exports and behavior

**Given** the public package with the new helper available
**When** a caller imports the existing public exports and invokes `greet("Ada")` and `greeting_has_hash("Ada#")`
**Then** all prior exports remain importable and the observed results remain `Hello, Ada` and `True` respectively.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Expose `greeting_has_plus(name: str) -> bool` from `nmg_sdlc_smoke`; report whether the complete `greet(name)` contains literal ASCII `+`. | Must |
| FR2 | Propagate the existing invalid-name `ValueError("name must not be blank")` and leave `greet` formatting unchanged. | Must |
| FR3 | Preserve all existing public exports and their behavior. | Must |
| FR4 | Cover presence, absence, invalid inputs, and preserved exports with focused pytest and pytest-bdd acceptance. | Must |

## Out of Scope

- New CLI options, greeting formatting changes, and detection of other characters.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #144 | 2026-09-24 | Initial feature spec |
