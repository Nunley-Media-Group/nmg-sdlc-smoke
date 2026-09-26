# Requirements: Add public greeting_has_exclamation_or_question helper

**Issue**: #163
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer using the Python greeting library
**I want** a public helper that reports whether a completed greeting contains a literal exclamation mark or question mark
**So that** I can check either punctuation mark with one boolean call

## Background

`greet(name)` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for invalid names. `greeting_has_question_mark` checks literal `?`; `greeting_ends_with_exclamation` appends `!` rather than querying the unmodified greeting. No public helper checks either mark in one call.

## Acceptance Criteria

### AC1: Detect an exclamation mark

**Given** an installed public package and valid name `Ada!`
**When** I call `greeting_has_exclamation_or_question("Ada!")`
**Then** it returns Python `True` because `greet("Ada!")` contains literal `!`.

### AC2: Detect a question mark

**Given** an installed public package and valid name `Ada?`
**When** I call `greeting_has_exclamation_or_question("Ada?")`
**Then** it returns Python `True` because `greet("Ada?")` contains literal `?`.

### AC3: Report absence and combined presence

**Given** valid names `Ada`, `Ada！？` (fullwidth marks), and `Ada!?`
**When** I call the helper with each name
**Then** it returns Python `False`, `False`, and `True` respectively, based on literal `!` or `?` in each completed greeting.

### AC4: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** I call the helper with each name
**Then** every call raises `ValueError` with exact message `name must not be blank`.

### AC5: Expose and document the helper

**Given** the installed package and README Library section
**When** I import `greeting_has_exclamation_or_question` from `nmg_sdlc_smoke` and follow its README examples
**Then** the public helper returns `True` for `Ada!` and `Ada?`, `False` for `Ada`, and README states the inherited invalid-name behavior.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_exclamation_or_question(name: str) -> bool` returning whether `greet(name)` contains literal `!` or `?`. | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and document its public import, examples, and validation in README's Library section. | Must |

## Out of Scope

- Changing `greet` or CLI output, appending punctuation, or matching lookalike Unicode punctuation instead of literal `!` and `?`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #163 | 2026-09-26 | Initial feature spec |
