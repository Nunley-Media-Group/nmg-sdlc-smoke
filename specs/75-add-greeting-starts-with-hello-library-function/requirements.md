# Requirements: Add greeting_starts_with_hello library function

**Issue**: #75
**Date**: 2026-09-03
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a `greeting_starts_with_hello(name)` library helper
**So that** callers can verify the existing greeting prefix without changing `greet` or the CLI

## Background

The package exposes `greet(name)` and small pure derived helpers. The new helper must delegate validation to `greet` and return `greet(name).startswith("Hello, ")` as a Python bool.

## Acceptance Criteria

### AC1: Valid greeting reports the expected prefix

**Given** the library is importable
**When** `greeting_starts_with_hello("Ada")` is called
**Then** it returns the Python bool `True`
**And** the value equals `greet("Ada").startswith("Hello, ")`

### AC2: Existing validation is preserved

**Given** the library is importable
**When** the helper receives a blank, whitespace-only, or non-string name
**Then** it raises the existing `ValueError("name must not be blank")` from `greet`

### AC3: Existing public behavior is unchanged

**Given** the distribution is installed
**When** `greet("Ada")` or `nmg-smoke Ada` is used
**Then** both retain their existing output and error behavior

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Implement `greeting_starts_with_hello(name)` as `greet(name).startswith("Hello, ")`. | Must |
| FR2 | Export the helper without removing existing public names. | Must |
| FR3 | Cover every acceptance criterion with unit and pytest-bdd tests. | Must |
| FR4 | Keep zero runtime dependencies and pass pytest, feature pytest, and Ruff. | Must |
| FR5 | Add one concise README library example. | Should |

## Out of Scope

- Changing `greet` or CLI behavior
- Adding CLI flags or runtime dependencies
- Bumping `VERSION`

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #75 | 2026-09-03 | Initial feature spec |
