# Tasks: Add a public greeting at-sign detector

**Issue**: #126
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document at-sign detection

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_at_sign(name: str) -> bool` returning `"@" in greet(name)` and export it via the package root and `__all__` (AC1, AC2, FR1).
- Invalid names propagate the exact `ValueError("name must not be blank")` without changing `greet`, the other punctuation helpers, or CLI behavior (AC3, FR2).
- Add the import and examples `greeting_has_at_sign("Ada@")  # True` and `greeting_has_at_sign("Ada")  # False` to README's library section; describe literal `@` detection in completed greeting text and shared `greet` validation (AC1–AC3).

### T002: Cover public results and validation with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from the package root; in separate tests assert `greet("Ada@") == "Hello, Ada@"` and `greeting_has_at_sign("Ada@") is True` (AC1), and `greet("Ada") == "Hello, Ada"` and `greeting_has_at_sign("Ada") is False` (AC2).
- In a third parametrized test, assert `ValueError` with exact message `name must not be blank` for `""`, `" \t\n"`, `None`, and `42` (AC3); `python -m pytest tests/test_greet.py -k greeting_has_at_sign` passes (FR3).

### T003: Exercise each acceptance criterion through pytest-bdd

**File(s)**: `tests/features/add_greeting_has_at_sign_library_helper.feature`, `tests/features/steps/test_greeting_has_at_sign_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Convert this spec's `feature.gherkin` to the executable feature path, omitting the spec metadata and source comments; preserve the three distinct AC1–AC3 scenarios and unique `@SCN001` through `@SCN003` tags.
- Bind steps following `tests/features/steps/test_greeting_has_colon_steps.py`: call the public helper with `"Ada@"` and `"Ada"`, assert exact completed greetings and Python bool identities; for `""`, `" \t\n"`, `None`, and `42`, assert each exact `ValueError` message (AC1–AC3, FR3).
- `python -m pytest tests/features/steps/test_greeting_has_at_sign_steps.py` passes with three scenarios.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #126 | 2026-09-23 | Initial feature tasks |
