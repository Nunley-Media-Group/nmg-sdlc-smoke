# Requirements: Add greeting_has_brace library helper

**Issue**: #141
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer using the public greeting library
**I want** to ask whether a completed greeting contains a literal opening brace
**So that** I can distinguish that character without altering greeting output.

## Background

`greet(name)` returns `Hello, ` followed by a valid name; existing punctuation predicates inspect that completed string. The new public query reports membership of the literal opening brace `{` as a boolean, using the same name validation.

## Acceptance Criteria

### AC1: Detect an opening brace

**Given** the public `nmg_sdlc_smoke` library and valid name `Ada{`
**When** `greeting_has_brace("Ada{")` is called
**Then** it returns `True` because `greet("Ada{")` is `Hello, Ada{`.

### AC2: Report absence of the literal opening brace

**Given** valid names `Ada` and `Ada}`
**When** `greeting_has_brace` is called with each name
**Then** both results are `False`; a closing brace alone does not match `{`.

### AC3: Preserve name validation

**Given** an empty, whitespace-only, or non-string name (`""`, `" "`, `None`, or `42`)
**When** `greeting_has_brace(name)` is called
**Then** each call raises `ValueError("name must not be blank")`, as `greet(name)` does.

### AC4: Preserve existing public behavior

**Given** the new helper is importable alongside existing package exports
**When** a caller invokes `greet("Ada")`, `greeting_has_hash("Ada#")`, and `greeting_has_question_mark("Ada?")`
**Then** the respective results remain `Hello, Ada`, `True`, and `True`.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Expose a pure `greeting_has_brace(name: str) -> bool` from `nmg_sdlc_smoke` that reports whether the completed `greet(name)` contains a literal `{`. | Must |
| FR2 | Propagate `greet`'s invalid-name `ValueError("name must not be blank")` without changing `greet` or its formatting. | Must |
| FR3 | Preserve existing public exports and their behavior. | Must |
| FR4 | Cover presence, absence (including a closing brace alone), invalid inputs, and preserved exports with focused pytest and pytest-bdd scenarios. | Must |

## Out of Scope

- Changes to the console script, greeting formatting, or other public helpers.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #141 | 2026-09-24 | Initial feature spec |
