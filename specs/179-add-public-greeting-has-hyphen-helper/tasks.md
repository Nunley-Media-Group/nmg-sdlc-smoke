# Tasks: Add public greeting_has_hyphen helper

**Issue**: #179
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the hyphen query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_hyphen(name: str) -> bool` returning `"-" in greet(name)`; export it with a self-aliased package import and `__all__` member without removing existing exports (AC1–AC4, FR1–FR3).
- In README Library, show public import, `Mary-Jane` true and `Ada` false examples, the literal U+002D-only rule, and inherited `ValueError("name must not be blank")` for invalid names (AC4, FR3).

### T002: Cover literal detection and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from package root; assert `greet("Mary-Jane") == "Hello, Mary-Jane"`, `greeting_has_hyphen("Mary-Jane") is True`, and `greeting_has_hyphen(name) is False` for `"Ada"`, `"Ada\u2010"`, and `"Ada\u2013"` (AC1, AC2, AC4).
- Parameterize `""`, `" \t"`, `None`, and `42`; assert each raises `ValueError` with exact message `name must not be blank` (AC3). Run `python -m pytest tests/test_greet.py`.

### T003: Exercise four independent AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_hyphen_helper.feature`, `tests/features/steps/test_greeting_has_hyphen_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Transfer the four tagged observable scenarios from this spec's `feature.gherkin` to executable `.feature` without spec frontmatter or source comments; implement deterministic steps using package-root imports and the neighboring double-quote-helper pattern (AC1–AC4).
- Assert exact greeting and boolean identity for `Mary-Jane` (AC1), `False` for `Ada`, `Ada‐`, and `Ada–` (AC2), exact error for all four invalid names (AC3), and root import, `__all__` membership, and documented true/false examples (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_hyphen_steps.py`; inspect README Library against AC4 without source-text tests.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #179 | 2026-09-26 | Initial feature tasks |
