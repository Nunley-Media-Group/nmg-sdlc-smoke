# Tasks: Add greeting_has_tilde library helper for review smoke

**Issue**: #131
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

### T001: Implement and export public tilde detector
**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- [ ] Add `greeting_has_tilde(name: str) -> bool` returning `"~" in greet(name)` and export through the package root and `__all__` (AC1, AC2).
- [ ] Preserve exact `greet` validation and document examples `"Ada~" -> True` and `"Ada" -> False` (AC3).

### T002: Prove public behavior in pytest
**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Assert completed greetings and bool identities for present and absent tildes, plus exact `ValueError` for empty, whitespace-only, `None` and integer inputs (AC1–AC3).

### T003: Cover each criterion in pytest-bdd
**File(s)**: `tests/features/add_greeting_has_tilde_library_helper.feature`, `tests/features/steps/test_greeting_has_tilde_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Translate `feature.gherkin` to three executable scenarios tagged `@SCN001`–`@SCN003`; bind positive, negative and invalid-name outcomes to the public import (FR3).

## Delivery
Complete review, verification, exact-head merge and closure of only #131; preserve plugin smoke invocation-bound delivery evidence.
