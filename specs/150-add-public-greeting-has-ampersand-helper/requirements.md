# Requirements: Add public greeting_has_ampersand helper

**Issue**: #150
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/146-add-public-greeting-has-equal-helper/

## User Story

**As a** Python library caller
**I want** to query whether a completed greeting contains a literal ASCII ampersand
**So that** I can inspect the greeting without changing it.

## Background

`greet(name)` produces `Hello, {name}` for valid names. Public predicates already inspect literal punctuation in the completed greeting, but there is no public ampersand predicate.

## Acceptance Criteria

### AC1: Detect an ASCII ampersand

**Given** a valid name `Ada&` and the public `nmg_sdlc_smoke` import
**When** `greeting_has_ampersand("Ada&")` is called
**Then** it returns the Python boolean `True`, since `greet("Ada&")` is `"Hello, Ada&"` and contains literal ASCII `&`.

### AC2: Report absence and reject a lookalike

**Given** valid names `Ada` and `Ada＆` (the latter contains fullwidth U+FF06 rather than ASCII `&`)
**When** `greeting_has_ampersand` is called through the public import with each name
**Then** it returns the Python boolean `False` for both, since neither completed greeting contains literal ASCII `&`.

### AC3: Preserve invalid-name validation

**Given** invalid names `""`, `" \t\n"`, `None`, and `42`
**When** `greeting_has_ampersand` is called with each name
**Then** each call raises `ValueError` with the exact message `name must not be blank`, as `greet` does.

### AC4: Preserve existing public interfaces

**Given** all previously public package exports and the installed `nmg-smoke` console script
**When** the prior exports and `greeting_has_ampersand` are imported, `greet("Ada")` and `greeting_has_equal("Ada=")` are called, and `nmg-smoke Ada` is run
**Then** all prior exports remain importable, the library returns `"Hello, Ada"` and `True`, and the CLI exits 0 with stdout `"Hello, Ada\n"` and empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export a pure `greeting_has_ampersand(name: str) -> bool` from `nmg_sdlc_smoke`; report whether the completed `greet(name)` contains literal ASCII `&`. | Must |
| FR2 | Preserve `greet`'s invalid-name behavior and exact `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Add the helper without removing or changing existing public exports, `greet` behavior, or CLI behavior; add no CLI option or runtime dependency. | Must |

## Out of Scope

- New CLI options, changed greeting formatting, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #150 | 2026-09-24 | Initial feature spec |
