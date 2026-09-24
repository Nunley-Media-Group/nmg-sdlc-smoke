# Tasks: Add public greeting_has_backtick library helper

**Issue**: #152
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement and expose the literal-backtick query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_backtick(name: str) -> bool` returning `"\u0060" in greet(name)` and export it through the package-root import and `__all__`, retaining existing public exports; U+FF40 remains distinct (AC1–AC3, FR1–FR3).
- Add Library examples for a name ending in literal U+0060 yielding `True`, plain Ada and the U+FF40 lookalike variant yielding `False`, and the inherited invalid-name error to the README without removing existing examples (AC1–AC3). Leave `greet` and `cli.py` unchanged (AC4, FR4).

### T002: Test the public library behavior

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import the public helper and assert that a greeting with a name ending in U+0060 retains that exact ASCII character and returns Python `True` (AC1); assert both plain Ada and the U+FF40 variant produce their exact completed greetings and Python `False` (AC2).
- Parameterize `""`, `" \t\n"`, `None`, `42`; each helper call raises `ValueError` with exactly `name must not be blank` (AC3). Assert `greet("Ada") == "Hello, Ada"` (AC4). Run `python -m pytest tests/test_greet.py tests/test_cli.py` (AC1–AC4, FR5).

### T003: Exercise each criterion through pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_backtick_library_helper.feature`, `tests/features/steps/test_greeting_has_backtick_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Materialize this spec's four scenarios with unique `@SCN001`–`@SCN004` tags in the executable feature, omitting spec frontmatter and source comments; follow the installed-script lookup and context fixture pattern in `tests/features/steps/test_greeting_has_equal_steps.py`.
- Check completed greeting and Python boolean identity for literal U+0060 (AC1), exact greetings and false results for plain Ada and its U+FF40 variant (AC2), exact errors for all four invalid inputs (AC3), and `greet("Ada")` plus installed `nmg-smoke Ada` exit 0/stdout `"Hello, Ada\n"`/empty stderr (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_backtick_steps.py` with four passing scenarios (FR5).

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #152 | 2026-09-24 | Initial feature tasks |
