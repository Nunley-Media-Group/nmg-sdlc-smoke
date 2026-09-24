# Tasks: Add greeting_has_pipe library helper for verified smoke

**Issue**: #129
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

### T001: Implement and export public pipe detector
**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- [ ] Add `greeting_has_pipe(name: str) -> bool` returning `"|" in greet(name)` and export through the package root and `__all__` (AC1, AC2).
- [ ] Preserve exact `greet` validation for invalid names; document examples `"Ada|" -> True` and `"Ada" -> False` (AC3).

### T002: Prove public behavior in pytest
**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Assert the completed greeting and bool identity for present and absent pipes, plus exact `ValueError` for `""`, whitespace-only, `None` and integer inputs (AC1–AC3).

### T003: Cover each acceptance criterion in pytest-bdd
**File(s)**: `tests/features/add_greeting_has_pipe_library_helper.feature`, `tests/features/steps/test_greeting_has_pipe_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Translate `feature.gherkin` to three distinct executable scenarios tagged `@SCN001`–`@SCN003`; bind positive, negative and invalid-name outcomes to the public import (FR3).

## Delivery
Complete review, verification, exact-head merge and closure of only #129; preserve the plugin smoke run's invocation-bound delivery evidence.
