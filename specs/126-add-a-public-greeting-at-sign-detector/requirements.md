# Requirements: Add a public greeting at-sign detector

**Issue**: #126
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** a public boolean query for a literal `@` in a completed greeting
**So that** I can inspect greeting text without changing it.

## Background

`nmg_sdlc_smoke` exports `greet(name)` and literal-punctuation queries for `:` and `;`. `greet` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.

## Acceptance Criteria

### AC1: Detect a literal at sign

**Given** the installed library and a valid name containing `@`
**When** `greeting_has_at_sign("Ada@")` is called through the public `nmg_sdlc_smoke` import
**Then** it returns the Python bool `True` for the completed greeting `Hello, Ada@`.

### AC2: Report an absent at sign

**Given** the installed library and a valid name without `@`
**When** `greeting_has_at_sign("Ada")` is called through the public `nmg_sdlc_smoke` import
**Then** it returns the Python bool `False` for the completed greeting `Hello, Ada`.

### AC3: Preserve name validation

**Given** an empty, whitespace-only, or non-string name
**When** `greeting_has_at_sign` is called with that name
**Then** it raises `ValueError("name must not be blank")` as `greet` does.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export a pure `greeting_has_at_sign(name: str) -> bool` from `nmg_sdlc_smoke` that reports literal `@` membership in the completed `greet(name)` text. | Must |
| FR2 | Preserve `greet` validation for invalid names and leave existing greeting and CLI behavior unchanged. | Must |
| FR3 | Independently cover positive, negative, and invalid-name outcomes with pytest tests and three separate pytest-bdd scenarios. | Must |

## Out of Scope

- CLI options, greeting text changes, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #126 | 2026-09-23 | Initial feature spec |
