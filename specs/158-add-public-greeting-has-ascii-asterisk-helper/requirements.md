# Requirements: Add public greeting_has_ascii_asterisk helper

**Issue**: #158
**Date**: 2026-09-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/155-add-public-greeting-has-asterisk-helper/

## User Story

**As a** Python library caller
**I want** an explicitly ASCII-named asterisk predicate for a completed greeting
**So that** I can inspect the greeting through a self-describing public interface without changing it.

## Background

`greet(name)` produces `Hello, {name}` for valid names. Public predicates inspect literal punctuation in the completed greeting, but there is no `greeting_has_ascii_asterisk` export.

## Acceptance Criteria

### AC1: Detect an ASCII asterisk

**Given** a valid name `Ada*` and the public `nmg_sdlc_smoke` import
**When** `greeting_has_ascii_asterisk("Ada*")` is called
**Then** it returns the Python boolean `True`, since `greet("Ada*")` is `"Hello, Ada*"` and contains literal ASCII `*`.

### AC2: Report an absent asterisk

**Given** a valid name `Ada` and the public import
**When** `greeting_has_ascii_asterisk("Ada")` is called
**Then** it returns the Python boolean `False`, since `greet("Ada")` is `"Hello, Ada"`.

### AC3: Preserve invalid-name validation

**Given** invalid names `""`, `" \t\n"`, `None`, and `42`
**When** `greeting_has_ascii_asterisk` is called with each name
**Then** each call raises `ValueError` with the exact message `name must not be blank`, as `greet` does.

### AC4: Preserve existing public interfaces

**Given** the previously public package exports and the installed `nmg-smoke` console script
**When** the prior exports and `greeting_has_ascii_asterisk` are imported, `greet("Ada")` and `greeting_has_asterisk("Ada*")` are called, and `nmg-smoke Ada` is run
**Then** all prior exports remain importable, the library returns `"Hello, Ada"` and `True`, and the CLI exits 0 with stdout `"Hello, Ada\n"` and empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export a pure `greeting_has_ascii_asterisk(name: str) -> bool` from `nmg_sdlc_smoke`; report whether the completed `greet(name)` contains literal ASCII `*`. | Must |
| FR2 | Preserve `greet`'s invalid-name behavior and exact `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Add the helper without removing or changing existing public exports, `greet` behavior, or CLI behavior; add no CLI option or runtime dependency. | Must |

## Out of Scope

- New CLI options, changed greeting formatting, changes to `greeting_has_asterisk`, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #158 | 2026-09-25 | Initial feature spec |
