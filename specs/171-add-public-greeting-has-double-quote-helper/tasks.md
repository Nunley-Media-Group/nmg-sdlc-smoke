# Tasks: Add public greeting_has_double_quote helper

**Issue**: #171
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the double-quote query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_double_quote(name: str) -> bool` returning `'"' in greet(name)`; export it with a self-aliased package import and `__all__` member without removing existing exports (AC1–AC4, FR1–FR3).
- In README Library, show public import, `Ada"` true and `Ada` false examples, and inherited `ValueError("name must not be blank")` for invalid names (AC4, FR3).

### T002: Cover literal detection and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from package root; assert `greet('Ada"') == 'Hello, Ada"'`, `greeting_has_double_quote('Ada"') is True`, `greeting_has_double_quote("Ada") is False`, and `greeting_has_double_quote("Ada＂") is False` (AC1, AC2, AC4).
- Parameterize `""`, `" \t"`, `None`, and `42`; assert each raises `ValueError` with exact message `name must not be blank` (AC3). Run `python -m pytest tests/test_greet.py`.

### T003: Exercise four independent AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_double_quote_helper.feature`, `tests/features/steps/test_greeting_has_double_quote_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Transfer the four tagged observable scenarios from this spec's `feature.gherkin` to executable `.feature` without spec frontmatter or source comments; implement deterministic steps using package-root imports and the neighboring dollar-helper pattern (AC1–AC4).
- Assert exact greeting and boolean identity for `Ada"` (AC1), `False` for `Ada` and `Ada＂` (AC2), exact error for all four invalid names (AC3), and root import with documented true/false examples (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_double_quote_steps.py`; inspect README Library against AC4 without source-text tests.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #171 | 2026-09-26 | Initial feature tasks |
