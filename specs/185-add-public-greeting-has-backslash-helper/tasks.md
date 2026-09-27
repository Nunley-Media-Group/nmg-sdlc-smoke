# Tasks: Add public greeting_has_backslash helper

**Issue**: #185
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the backslash query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_backslash(name: str) -> bool` returning `"\\" in greet(name)` and export it with a self-aliased package import and `__all__` member without removing existing exports (AC1–AC4, FR1–FR3).
- In README Library, show the public import, exact `greeting_has_backslash("Ada\\")  # True` and `greeting_has_backslash("Ada")  # False` examples, the U+005C-only match, and inherited invalid-name `ValueError("name must not be blank")` (AC4, FR3).

### T002: Cover the public query and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from the package root; assert `greet("Ada\\") == "Hello, Ada\\"` and `greeting_has_backslash("Ada\\") is True` (AC1, AC4).
- Parameterize `"Ada"`, `"Ada/"`, `"Ada\uff3c"`, and `"Ada\u2216"`, asserting `greeting_has_backslash(name) is False` for each (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`, asserting `ValueError` matching `^name must not be blank$` for each (AC3). Run `python -m pytest tests/test_greet.py`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_backslash_helper.feature`, `tests/features/steps/test_greeting_has_backslash_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four uniquely tagged scenarios in this spec's `feature.gherkin` into the executable `.feature` without frontmatter or source comments, and implement deterministic steps using public imports and the conventions of `tests/features/steps/test_greeting_has_slash_steps.py` (AC1–AC4).
- Assert the exact greeting `Hello, Ada\` and Python boolean identity `True` for `"Ada\\"` (AC1); `False` for each of `"Ada"`, `"Ada/"`, `"Ada\uff3c"`, `"Ada\u2216"` with no `\` in each greeting (AC2); exact `name must not be blank` for each invalid name (AC3); and `"greeting_has_backslash" in nmg_sdlc_smoke.__all__` plus package-root results `True` for `"Ada\\"` and `False` for `"Ada"` (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_backslash_steps.py`; inspect README Library against AC4 separately, without source-text tests.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #185 | 2026-09-27 | Initial feature tasks |
