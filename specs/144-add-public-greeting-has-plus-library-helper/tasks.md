# Tasks: Add public greeting_has_plus library helper

**Issue**: #144
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement public plus predicate

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Return `"+" in greet(name)` from `greeting_has_plus(name: str) -> bool`, importing it from the package and adding it to `__all__` (AC1, AC2, FR1).
- Propagate `greet`'s invalid-name `ValueError` without duplicate validation; retain the original greeting format and all existing package exports (AC3, AC4, FR2, FR3).

### T002: Verify public helper and preserved behavior with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Assert the public import returns `True` for `Ada+`, `False` for `Ada`, and exact `ValueError("name must not be blank")` for `""`, `" \t\n"`, `None`, and `42` (AC1–AC3, FR4).
- Keep/import every original `__all__` symbol and verify `greet("Ada") == "Hello, Ada"` and `greeting_has_hash("Ada#") is True`; run the existing suite for prior helper behavior (AC4, FR3, FR4).

### T003: Verify each acceptance criterion with pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_plus_library_helper.feature`, `tests/features/steps/test_greeting_has_plus_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Implement one observable scenario per AC1–AC4 from `feature.gherkin`; copy executable Feature and scenario text but omit spec metadata, and cover all four invalid examples in AC3 (FR4).
- AC4 imports all prior public exports and checks `greet("Ada") == "Hello, Ada"` and `greeting_has_hash("Ada#") is True` without changing or invoking the CLI.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #144 | 2026-09-24 | Initial feature tasks |
