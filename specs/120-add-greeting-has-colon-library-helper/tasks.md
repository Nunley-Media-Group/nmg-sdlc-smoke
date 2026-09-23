# Tasks: Add greeting_has_colon library helper

**Issue**: #120
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document colon detection

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_colon(name: str) -> bool` returning `":" in greet(name)` and export it through the package root and `__all__` (AC1, AC2, FR1).
- Invalid names propagate `greet`'s exact `ValueError("name must not be blank")` without changing `greet` or CLI behavior (AC3, FR2).
- Add the helper to README's library import/examples, showing `greeting_has_colon("Ada:")  # True` and `greeting_has_colon("Ada")  # False`, and say it checks literal `:` in the complete greeting with the same invalid-name validation as `greet` (AC1–AC3, FR4).

### T002: Cover helper results and validation with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import the package-root helper; assert `greet("Ada:") == "Hello, Ada:"` and `greeting_has_colon("Ada:") is True` (AC1), and `greet("Ada") == "Hello, Ada"` and `greeting_has_colon("Ada") is False` (AC2).
- For `""`, `" \t\n"`, `None`, and `42`, assert `ValueError` with exact message `name must not be blank` (AC3); `python -m pytest tests/test_greet.py` passes (FR3).

### T003: Exercise each acceptance criterion through pytest-bdd

**File(s)**: `tests/features/add_greeting_has_colon_library_helper.feature`, `tests/features/steps/test_greeting_has_colon_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Convert this spec's `feature.gherkin` into executable pytest-bdd Gherkin at the named feature path, omitting spec metadata and comments; preserve three independent scenarios and unique `@SCN001` through `@SCN003` tags corresponding to AC1–AC3.
- Bind steps following `tests/features/steps/test_greeting_has_semicolon_steps.py`: test package-level `greeting_has_colon` on `"Ada:"` and `"Ada"`, with their exact complete greeting strings and Python bool identities; for `""`, `" \t\n"`, `None`, and `42`, check each exact `ValueError` text (AC1–AC3, FR3).
- `python -m pytest tests/features/steps/test_greeting_has_colon_steps.py` passes with three scenarios; no other issue spec is edited.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #120 | 2026-09-22 | Initial feature tasks |
