# Requirements: Add greeting_ends_with_exclamation library function

**Issue**: #79
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a public `greeting_ends_with_exclamation(name)` library function
**So that** callers can obtain the existing greeting with one trailing exclamation mark

## Acceptance Criteria

### AC1: Append one exclamation mark

**Given** the installed package is importable
**When** `greeting_ends_with_exclamation("Ada")` is called
**Then** it returns exactly `Hello, Ada!`

### AC2: Preserve valid names

**Given** a valid name contains leading and trailing spaces
**When** the helper is called with that name
**Then** every name character is preserved before the final exclamation mark

### AC3: Preserve validation

**Given** the helper is imported from the public package
**When** it receives a blank, whitespace-only, or non-string name
**Then** it propagates `ValueError("name must not be blank")` from `greet`

### AC4: Preserve existing behavior

**Given** the distribution is installed
**When** `greet("Ada")` and `nmg-smoke Ada` are used
**Then** their existing return value, output, and exit status are unchanged

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Return `greet(name) + "!"` for valid names. | Must |
| FR2 | Preserve every character of a valid name. | Must |
| FR3 | Export the helper without removing existing public names. | Must |
| FR4 | Preserve existing validation and CLI behavior. | Must |
| FR5 | Cover every acceptance criterion with unit and pytest-bdd tests. | Must |
| FR6 | Add one concise README library example. | Should |
| FR7 | Add no runtime dependency and leave `VERSION` unchanged. | Must |

## Out of Scope

- Changing `greet`, its validation, or the CLI
- Configurable punctuation
- Runtime dependencies or version changes

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #79 | 2026-09-04 | Initial feature spec |
