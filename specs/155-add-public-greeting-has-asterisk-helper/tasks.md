# Tasks: Add public greeting_has_asterisk helper

**Issue**: #155
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/152-add-public-greeting-has-backtick-library-helper/

## Implementation Tasks

### T001: Implement and expose the literal-asterisk query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_asterisk(name: str) -> bool` returning `"*" in greet(name)` and export it through the package-root import and `__all__` without removing existing public exports (AC1–AC4, FR1–FR4).
- Extend the README Library import/examples with `True` for `"Ada*"`, `False` for `"Ada"` and `"Ada∗"`, and the inherited invalid-name error. Leave `greet` and `cli.py` unchanged (AC5, FR4).

### T002: Test the public library behavior

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import the new public helper. Assert `greet("Ada*") == "Hello, Ada*"` and helper result `is True` (AC1); `greet("Ada") == "Hello, Ada"` and result `is False` (AC2); `greet("Ada∗") == "Hello, Ada∗"` and result `is False` (AC3).
- Parameterize `""`, `" \t\n"`, `None`, and `42` and assert each helper call raises `ValueError` with exactly `name must not be blank` (AC4). Preserve the existing `greet` and CLI tests (AC5). Run `python -m pytest tests/test_greet.py tests/test_cli.py` (FR5).

### T003: Exercise each criterion through pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_asterisk_helper.feature`, `tests/features/steps/test_greeting_has_asterisk_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Materialize this spec's five scenarios as a runnable feature with unique `@SCN001`–`@SCN005` tags, omitting the spec's frontmatter and source comments. Follow the local pytest-bdd fixture and installed-script lookup pattern in `tests/features/steps/test_greeting_has_backtick_steps.py`.
- Check exact completed greeting and Python boolean identity for ASCII U+002A (AC1), absent character (AC2), and U+2217 lookalike (AC3); check all four exact invalid-input errors (AC4); import the public helper, check `greet("Ada")`, and run the installed `nmg-smoke Ada`, asserting exit 0, stdout `"Hello, Ada\n"`, and empty stderr (AC5). Run `python -m pytest tests/features/steps/test_greeting_has_asterisk_steps.py` and require five passing scenarios (FR5).

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #155 | 2026-09-24 | Initial feature tasks |
