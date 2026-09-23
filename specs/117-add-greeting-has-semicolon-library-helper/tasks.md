# Tasks: Add greeting_has_semicolon library helper

**Issue**: #117
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement and export semicolon detection

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_semicolon(name: str) -> bool` returning `";" in greet(name)` and export it through the package root and `__all__` (AC1, AC2, FR1).
- Invalid names propagate `greet`'s exact `ValueError("name must not be blank")`; do not change `greet`, CLI, or existing exports (AC3, AC4, FR2).

### T002: Cover helper results and validation

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Assert package-level `greeting_has_semicolon("Ada;") is True` and `greeting_has_semicolon("Ada") is False`, checking the complete greeting's corresponding text (AC1, AC2).
- For `""`, `" \t\n"`, `None`, and `42`, assert `ValueError` with exact message `name must not be blank` (AC3); `python -m pytest tests/test_greet.py` passes.

### T003: Exercise each acceptance criterion through pytest-bdd

**File(s)**: `tests/features/add_greeting_has_semicolon_library_helper.feature`, `tests/features/steps/test_greeting_has_semicolon_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Convert `feature.gherkin` to executable pytest-bdd Gherkin in the named test feature (omit spec metadata comments/frontmatter); bind one distinct scenario per AC, with `@SCN001` through `@SCN004` and matching steps (AC1–AC4).
- In AC3 check each invalid category against exact `ValueError` text. In AC4 invoke the installed `nmg-smoke` console script with `Ada` and assert exit 0, stdout `Hello, Ada\n`, empty stderr; assert `greet("Ada") == "Hello, Ada"` and all previously exported package helpers (`greet`, `greet_many`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello`, `greeting_word_count`) remain importable (AC4, FR2).
- `python -m pytest tests/features` passes with four new scenarios; this task does not edit other issue specs.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #117 | 2026-09-22 | Initial feature tasks |
