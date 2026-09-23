# Requirements: Add greeting_has_semicolon library helper

**Issue**: #117
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** to ask whether a completed greeting contains a semicolon
**So that** I can inspect that greeting without changing its text.

## Background

The public package exposes `greet(name)` and derived pure helpers. `greet` returns `Hello, {name}` for non-blank strings and rejects blank, whitespace-only, or non-string names with `ValueError("name must not be blank")`. The new helper reports a property of that complete greeting.

## Acceptance Criteria

### AC1: Detect a literal semicolon

**Given** the installed library and a valid name containing `;`
**When** `greeting_has_semicolon("Ada;")` is called
**Then** it returns the Python bool `True`, because `greet("Ada;")` is `Hello, Ada;` and contains literal `;`.

### AC2: Report absence of a semicolon

**Given** the installed library and a valid name without `;`
**When** `greeting_has_semicolon("Ada")` is called
**Then** it returns the Python bool `False`, because `greet("Ada")` is `Hello, Ada` and contains no `;`.

### AC3: Preserve name validation

**Given** an empty, whitespace-only, or non-string name
**When** `greeting_has_semicolon` is called
**Then** it raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Preserve existing greeting and CLI behavior

**Given** the installed package
**When** `greet("Ada")` and `nmg-smoke Ada` run
**Then** the library result is `Hello, Ada`, the CLI exits 0 with stdout `Hello, Ada` followed by exactly one newline and empty stderr, and all existing public helper imports remain available.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export `greeting_has_semicolon(name: str) -> bool` from `nmg_sdlc_smoke`; return whether the complete `greet(name)` text contains literal ASCII `;`. | Must |
| FR2 | Use `greet` validation for the helper; preserve the current greeting, CLI behavior, and existing public helper imports. | Must |

## Out of Scope

- New CLI options, greeting text changes, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #117 | 2026-09-22 | Initial feature spec |
