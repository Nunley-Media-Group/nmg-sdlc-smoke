# Requirements: Add greeting_has_colon library helper

**Issue**: #120
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** to ask whether a completed greeting contains a literal colon
**So that** I can inspect that greeting without changing its text.

## Background

`nmg_sdlc_smoke` exports `greet(name)` and pure helpers derived from its completed text, including `greeting_has_semicolon(name)`. `greet` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for empty, whitespace-only, or non-string names.

## Acceptance Criteria

### AC1: Detect a literal colon

**Given** the installed library and a valid name containing `:`
**When** `greeting_has_colon("Ada:")` is called
**Then** it returns the Python bool `True`, because the completed greeting is `Hello, Ada:`.

### AC2: Report absence of a colon

**Given** the installed library and a valid name without `:`
**When** `greeting_has_colon("Ada")` is called
**Then** it returns the Python bool `False`, because the completed greeting is `Hello, Ada`.

### AC3: Preserve name validation

**Given** an empty, whitespace-only, or non-string name
**When** `greeting_has_colon` is called
**Then** it raises `ValueError("name must not be blank")`, as `greet` does.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export `greeting_has_colon(name: str) -> bool` from `nmg_sdlc_smoke`; return whether the complete `greet(name)` text contains literal ASCII `:`. | Must |
| FR2 | Inherit `greet` validation without changing `greet` or existing CLI behavior. | Must |
| FR3 | Add deterministic pytest and pytest-bdd coverage for the true, false, and invalid-name outcomes. | Must |
| FR4 | Document the exported helper, its boolean result, and shared invalid-name behavior in `README.md`. | Must |

## Out of Scope

- New CLI options, greeting text changes, and detecting punctuation other than the colon.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #120 | 2026-09-22 | Initial feature spec |
