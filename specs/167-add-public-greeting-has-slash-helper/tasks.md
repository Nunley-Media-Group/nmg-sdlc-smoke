# Tasks: Add public greeting_has_slash helper

**Issue**: #167
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the slash query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_slash(name: str) -> bool` returning `"/" in greet(name)` and export it with a self-aliased package import and `__all__` member without removing existing exports (AC1–AC4, FR1–FR3).
- In README Library, show the public import, exact `Ada/` true and `Ada` false examples, and inherited invalid-name `ValueError("name must not be blank")` (AC4, FR3).

### T002: Cover the public query and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from the package root; assert `greeting_has_slash("Ada/") is True`, `greet("Ada/") == "Hello, Ada/"`, `greeting_has_slash("Ada") is False`, and `greeting_has_slash("Ada／") is False` (AC1, AC2, AC4).
- Parameterize `""`, `" \t"`, `None`, and `42`, asserting exact `ValueError("name must not be blank")` for each (AC3). Run `python -m pytest tests/test_greet.py`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_slash_helper.feature`, `tests/features/steps/test_greeting_has_slash_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four uniquely tagged scenarios in this spec's `feature.gherkin` into the executable `.feature` without frontmatter or source comments, and implement deterministic steps using public imports and neighboring punctuation-helper conventions (AC1–AC4).
- Assert exact greeting and Python boolean identity for `Ada/` (AC1), both absent cases including `Ada／` (AC2), each invalid name and exact error (AC3), and package-root import returning true/false for README examples (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_slash_steps.py`; inspect README Library against AC4 separately, without source-text tests.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #167 | 2026-09-26 | Initial feature tasks |
