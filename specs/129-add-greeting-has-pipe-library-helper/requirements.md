# Requirements: Add greeting_has_pipe library helper for verified smoke

**Issue**: #129
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## User Story
**As a** Python library caller
**I want** a public boolean query for a literal pipe in a completed greeting
**So that** I can inspect greeting text without changing it.

## Acceptance Criteria
### AC1: Detect a literal pipe
**Given** a valid name containing `|`
**When** `greeting_has_pipe("Ada|")` is called through the public `nmg_sdlc_smoke` import
**Then** it returns Python `True` for the completed greeting `Hello, Ada|`.

### AC2: Report an absent pipe
**Given** a valid name without `|`
**When** `greeting_has_pipe("Ada")` is called
**Then** it returns Python `False` for the completed greeting `Hello, Ada`.

### AC3: Preserve name validation
**Given** an empty, whitespace-only, or non-string name
**When** `greeting_has_pipe` is called
**Then** it raises `ValueError("name must not be blank")` as `greet` does.

## Functional Requirements
| ID | Requirement | Priority |
|---|---|---|
| FR1 | Export a pure `greeting_has_pipe(name: str) -> bool` from `nmg_sdlc_smoke`, checking literal `|` membership in `greet(name)`. | Must |
| FR2 | Preserve `greet` validation, all existing helpers and CLI behavior. | Must |
| FR3 | Cover positive, negative, and invalid-name outcomes with pytest and three pytest-bdd scenarios. | Must |

## Out of Scope
- CLI options, greeting formatting, and detection of other punctuation.
