# Requirements: Add public greeting_has_equal helper

**Issue**: #146
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** to query whether a completed greeting contains a literal ASCII equals sign
**So that** I can inspect the greeting without changing it.

## Background

`greet(name)` produces `Hello, {name}` for valid names, and the public punctuation queries inspect that completed string. A corresponding query for the literal ASCII `=` is not yet exported.

## Acceptance Criteria

### AC1: Detect a literal equals sign

**Given** a valid name `Ada=` and the public `nmg_sdlc_smoke` import
**When** `greeting_has_equal("Ada=")` is called
**Then** it returns the Python boolean `True` because `greet("Ada=")` is `"Hello, Ada="` and contains literal ASCII `=`.

### AC2: Report equals-sign absence

**Given** valid names `Ada` and `Ada＝` (the latter contains a fullwidth equals sign)
**When** `greeting_has_equal` is called with each name through the public import
**Then** it returns the Python boolean `False` for both: `greet("Ada")` is `"Hello, Ada"` and neither completed greeting contains ASCII `=`.

### AC3: Preserve name validation

**Given** invalid names `""`, `" "`, `None`, and `42`
**When** `greeting_has_equal(name)` is called for each
**Then** each call raises `ValueError` with the exact message `name must not be blank`, as `greet(name)` does.

### AC4: Preserve the existing public interface

**Given** the previously public package exports and the installed `nmg-smoke` console script
**When** those exports and the new helper are imported, `greet("Ada")` and `greeting_has_hash("Ada#")` are called, and `nmg-smoke Ada` is run
**Then** all previously public exports remain importable, the library calls return `"Hello, Ada"` and `True`, and the CLI exits 0 with stdout `"Hello, Ada\n"` and empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export a pure `greeting_has_equal(name: str) -> bool` from `nmg_sdlc_smoke`; return whether the completed `greet(name)` contains literal ASCII `=`. | Must |
| FR2 | Propagate `greet`'s exact `ValueError("name must not be blank")` for blank, whitespace-only, and non-string input. | Must |
| FR3 | Add the helper without removing or altering existing public exports, `greet` behavior, or CLI behavior. | Must |

## Out of Scope

- New CLI options, changed greeting formatting, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #146 | 2026-09-24 | Initial feature spec |
