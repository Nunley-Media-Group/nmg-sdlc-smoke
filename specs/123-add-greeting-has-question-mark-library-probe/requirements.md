# Requirements: Add greeting_has_question_mark library probe

**Issue**: #123
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## User Story

As an nmg-sdlc maintainer exercising merged plugin #413, I want one fresh, bounded Python greeting query to verify approved-spec → execute → exact-head merge delivery through a real install. This is a disposable plugin smoke fixture, not a repair of the smoke application's backlog.

## Acceptance Criteria

### AC1: Detect a question mark
Given a valid name containing `?`, when `greeting_has_question_mark(name)` is imported from `nmg_sdlc_smoke` and called, then it returns `True`.

### AC2: Distinguish a name without a question mark
Given a valid name without `?`, when the public helper is called, then it returns `False`.

### AC3: Preserve existing validation
Given a blank, whitespace-only, or non-string name, when the helper is called, then it raises the existing `ValueError("name must not be blank")` from `greet`.

## Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR1 | Export a pure typed `greeting_has_question_mark(name: str) -> bool` through the public library API and reuse `greet` validation. | Must |
| FR2 | Cover positive, negative, and invalid input in independent pytest-bdd scenarios, plus focused unit tests. | Must |

## Scope and stop rule

Only `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `tests/test_greet.py`, `tests/features/`, documentation, and normal workflow-owned version/changelog/verification artifacts are in scope. No CLI, infrastructure, unrelated issue, or assertion weakening. This is one #413 smoke attempt. An unchanged failure or unrelated application defect stops the experiment; no replacement issue or retry without a concrete changed plugin fix/hypothesis.
