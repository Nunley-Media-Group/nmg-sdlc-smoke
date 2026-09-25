# Tasks: Add public greeting_has_ascii_asterisk helper

**Issue**: #158
**Date**: 2026-09-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/155-add-public-greeting-has-asterisk-helper/

## Implementation Tasks

### T001: Implement and expose the ASCII asterisk query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add pure `greeting_has_ascii_asterisk(name: str) -> bool` returning `"*" in greet(name)` and export it at package root and in `__all__`, preserving existing exports, `greet`, and the CLI (AC1–AC4, FR1–FR3).
- Show public import, `True` and `False` examples, and inherited invalid-name behavior in the README Library section alongside existing examples (AC1–AC3).

### T002: Prove public results and validation with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import the public helper and assert `greet("Ada*") == "Hello, Ada*"` and `greeting_has_ascii_asterisk("Ada*") is True` (AC1); assert `"Ada"` returns Python `False` (AC2).
- Parameterize `""`, `" \t\n"`, `None`, and `42` to assert exact `ValueError("name must not be blank")` (AC3); check the preexisting public exports listed in design remain importable and `greet("Ada")` and `greeting_has_asterisk("Ada*")` retain exact results (AC4). `python -m pytest tests/test_greet.py tests/test_cli.py` passes.

### T003: Prove every acceptance criterion with pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_ascii_asterisk_helper.feature`, `tests/features/steps/test_greeting_has_ascii_asterisk_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Materialize this spec's four AC-linked scenarios in the executable feature, preserving distinct `@SCN001`–`@SCN004` tags but omitting spec frontmatter and source comments; bind them to deterministic package-root steps (AC1–AC4).
- Check the completed greeting and Python boolean identity for ASCII `*` (AC1), `Ada` absence (AC2), all four invalid values and exact errors (AC3), every prior public export and installed cross-platform `nmg-smoke Ada` exit 0/stdout `"Hello, Ada\n"`/empty stderr with `greet("Ada")` and `greeting_has_asterisk("Ada*")` preserved (AC4). `python -m pytest tests/features/steps/test_greeting_has_ascii_asterisk_steps.py` passes with four scenarios.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #158 | 2026-09-25 | Initial feature tasks |
