# Requirements: Add greeting_has_percent library helper for recovery smoke

**Issue**: #135
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## User Story
**As a** Python library caller
**I want** a boolean query for a literal percent sign in a completed greeting
**So that** I can inspect greeting text without changing it.

## Acceptance Criteria
### AC1: Detect percent in a greeting
**Given** a valid name containing `%`
**When** `greeting_has_percent("Ada%")` is called through the public `nmg_sdlc_smoke` import
**Then** it returns Python `True` for `Hello, Ada%`.

### AC2: Report absent percent
**Given** a valid name without `%`
**When** `greeting_has_percent("Ada")` is called
**Then** it returns Python `False` for `Hello, Ada`.

### AC3: Preserve name validation
**Given** a blank, whitespace-only, or non-string name
**When** `greeting_has_percent` is called
**Then** it raises `ValueError("name must not be blank")` as `greet` does
**And** existing greeting, exports, and CLI behavior remain unchanged.

## Functional Requirements
| ID | Requirement | Priority |
|---|---|---|
| FR1 | Export a pure `greeting_has_percent(name: str) -> bool`, checking literal `%` membership in `greet(name)`. | Must |
| FR2 | Preserve existing `greet` validation and public APIs. | Must |
| FR3 | Cover present, absent, and invalid-name outcomes with pytest and three pytest-bdd scenarios plus README usage. | Must |

## Out of Scope
CLI options, greeting formatting, and detection of other punctuation.
