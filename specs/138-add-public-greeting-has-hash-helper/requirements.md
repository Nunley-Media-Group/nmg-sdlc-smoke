# Requirements: Add public greeting_has_hash helper

**Issue**: #138
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer using the installable Python smoke library
**I want** a public `greeting_has_hash(name)` query
**So that** I can determine whether a completed greeting contains a literal `#` without changing the greeting or CLI contract.

## Background

`greet(name)` returns `Hello, {name}` for a valid name; the public punctuation helpers inspect the completed greeting. This additive query reports literal hash membership as a Python boolean and uses the same name validation.

## Acceptance Criteria

### AC1: Detect a literal hash

**Given** a valid name `Ada#` and the public `nmg_sdlc_smoke` import
**When** `greeting_has_hash("Ada#")` is called
**Then** it returns the boolean `True` because `greet("Ada#")` is `Hello, Ada#` and contains a literal `#`.

### AC2: Report hash absence

**Given** a valid name `Ada` and the public `nmg_sdlc_smoke` import
**When** `greeting_has_hash("Ada")` is called
**Then** it returns the boolean `False` because `greet("Ada")` is `Hello, Ada` and contains no literal `#`.

### AC3: Preserve greet validation

**Given** an empty, whitespace-only, or non-string name (`""`, `" "`, `None`, or `42`)
**When** `greeting_has_hash(name)` is called
**Then** each call raises `ValueError("name must not be blank")`, consistent with `greet(name)`.

### AC4: Preserve existing greeting interfaces

**Given** the new helper is available
**When** a caller invokes `greet("Ada")`, `greeting_has_question_mark("Ada?")`, and `nmg-smoke Ada`
**Then** the respective results remain `Hello, Ada`, `True`, and stdout `Hello, Ada` followed by one newline with a successful CLI exit.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Expose `greeting_has_hash(name: str) -> bool` through the public `nmg_sdlc_smoke` package; report whether the complete `greet(name)` contains a literal `#`. | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Cover AC1–AC4 with focused pytest and pytest-bdd checks. | Must |
| FR4 | Show the public import and `True`/`False` examples in the README library section. | Must |

## Out of Scope

- New CLI flags or output modes; changes to `greet` formatting or other public helpers.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #138 | 2026-09-24 | Initial feature spec |
