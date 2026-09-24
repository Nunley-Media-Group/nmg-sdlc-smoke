# Tasks: Add greeting_has_brace library helper

**Issue**: #141
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement the public brace predicate

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_brace(name: str) -> bool` returning `"{" in greet(name)` and export it from the package (AC1, AC2, FR1).
- Preserve `greet`'s error for invalid inputs, its formatting, and all existing public exports without duplicating validation (AC3, AC4, FR2, FR3).

### T002: Prove public outcomes with focused pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `test_greeting_has_brace_detects_literal_in_completed_greeting` for `Ada{` → `True`; `test_greeting_has_brace_reports_absence` for both `Ada` and `Ada}` → `False`; and `test_greeting_has_brace_preserves_validation`, parameterized over `""`, `" "`, `None`, and `42`, for exact `ValueError("name must not be blank")` (AC1–AC3, FR4).
- Add `test_greeting_has_brace_preserves_existing_public_behavior` asserting public `greet("Ada")`, `greeting_has_hash("Ada#")`, and `greeting_has_question_mark("Ada?")` still yield `Hello, Ada`, `True`, and `True` (AC4, FR3, FR4).

### T003: Prove all four ACs with pytest-bdd

**File(s)**: `tests/features/add_greeting_has_brace_library_helper.feature`, `tests/features/steps/test_greeting_has_brace_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the Feature and four independently tagged scenarios from this spec's `feature.gherkin` into the executable `.feature` without the metadata lines; register them with `scenarios("../add_greeting_has_brace_library_helper.feature")` and implement steps that exercise the public imports (AC1–AC4, FR4).
- For AC2 check both `Ada` and `Ada}`; for AC3 check all four invalid values and the exact exception text; for AC4 check all three preserved library results (FR2, FR3, FR4).

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #141 | 2026-09-24 | Initial feature tasks |
