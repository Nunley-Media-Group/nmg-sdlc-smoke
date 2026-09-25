# Requirements: Add public greeting_has_asterisk helper

**Issue**: #155
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/152-add-public-greeting-has-backtick-library-helper/

## User Story

**As a** Python library caller
**I want** to query whether a completed greeting contains a literal ASCII asterisk
**So that** I can inspect the greeting without changing its text.

## Background

`greet(name)` returns `"Hello, {name}"` for valid names and raises `ValueError("name must not be blank")` for blank, whitespace-only, or non-string names. Public literal-character helpers such as `greeting_has_backtick` inspect completed greetings; an asterisk helper is not available.

## Acceptance Criteria

### AC1: Detect a literal ASCII asterisk

**Given** the public `nmg_sdlc_smoke` import and valid name `"Ada*"`
**When** `greeting_has_asterisk("Ada*")` is called
**Then** it returns the Python boolean `True` because `greet("Ada*")` is `"Hello, Ada*"` and contains U+002A.

### AC2: Report an absent asterisk

**Given** the public import and valid name `"Ada"`
**When** `greeting_has_asterisk("Ada")` is called
**Then** it returns the Python boolean `False` because `greet("Ada")` is `"Hello, Ada"` and contains no U+002A.

### AC3: Distinguish a Unicode lookalike

**Given** the public import and valid name `"Ada∗"` containing U+2217 ASTERISK OPERATOR
**When** `greeting_has_asterisk("Ada∗")` is called
**Then** it returns the Python boolean `False`; `greet("Ada∗")` is `"Hello, Ada∗"` and U+2217 is not treated as U+002A.

### AC4: Inherit invalid-name behavior

**Given** each invalid name `""`, `" \t\n"`, `None`, and `42`
**When** `greeting_has_asterisk(name)` is called for each
**Then** each raises `ValueError` with the exact message `name must not be blank`, as `greet(name)` does.

### AC5: Preserve greeting and CLI output

**Given** the new public helper and the installed `nmg-smoke` console script
**When** a caller imports `greeting_has_asterisk`, evaluates `greet("Ada")`, and runs `nmg-smoke Ada`
**Then** the import succeeds, `greet("Ada")` remains `"Hello, Ada"`, and the CLI exits 0 with stdout `"Hello, Ada\n"` and empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export a pure `greeting_has_asterisk(name: str) -> bool` from `nmg_sdlc_smoke`; return whether the exact completed `greet(name)` contains literal ASCII asterisk U+002A. | Must |
| FR2 | Compare literal characters without normalization; U+2217 ASTERISK OPERATOR must not match U+002A. | Must |
| FR3 | Propagate `greet`'s exact `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. | Must |
| FR4 | Preserve existing `greet` results and `nmg-smoke` output; do not remove existing public exports. | Must |
| FR5 | Prove positive, absent, lookalike, and invalid input cases with deterministic unit and pytest-bdd cases, including the unchanged greeting and CLI output. | Must |

## Out of Scope

- New CLI flags or output transformations, changed greeting formatting, and detection of other characters.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #155 | 2026-09-24 | Initial feature spec |
