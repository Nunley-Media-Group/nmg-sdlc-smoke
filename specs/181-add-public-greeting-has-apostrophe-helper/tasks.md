# Tasks: Add public greeting_has_apostrophe helper

**Issue**: #181
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/171-add-public-greeting-has-double-quote-helper/

## Implementation Tasks

### T001: Implement, export, and document the apostrophe query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_apostrophe(name: str) -> bool` returning `"'" in greet(name)` after `greeting_has_slash`; export it with a self-aliased package import and an `__all__` entry placed alphabetically before `greeting_has_ascii_asterisk`, without removing existing exports (AC1–AC4, FR1–FR3).
- In README Library, add the import, `greeting_has_apostrophe("O'Brien")  # True`, `greeting_has_apostrophe("Ada")  # False`, and `greeting_has_apostrophe("O’Brien")  # False` examples, and a prose line stating only literal `'` (U+0027) matches and invalid names inherit `greet`'s `ValueError("name must not be blank")` (AC4, FR3). Leave `greet` and `cli.py` unchanged.

### T002: Cover literal detection, lookalikes, and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import `greeting_has_apostrophe` from the package root; assert `greet("O'Brien") == "Hello, O'Brien"` and `greeting_has_apostrophe("O'Brien") is True` (AC1).
- Parameterize `"Ada"`, `"O\u2019Brien"`, `"O\u02bcBrien"`, and ``"O`Brien"``; assert each result `is False` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`; assert each raises `ValueError` matching `^name must not be blank$` (AC3). Run `python -m pytest tests/test_greet.py -k apostrophe`.

### T003: Exercise four independent AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_apostrophe_helper.feature`, `tests/features/steps/test_greeting_has_apostrophe_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Transfer the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature` without spec frontmatter or source comments; implement deterministic steps with a local `context` fixture and package-root imports following `tests/features/steps/test_greeting_has_double_quote_steps.py` (AC1–AC4).
- Assert exact greeting `Hello, O'Brien` and `True` identity (AC1); `False` identity for `Ada`, `O\u2019Brien`, `O\u02bcBrien`, and ``O`Brien`` with no literal `'` in each completed greeting (AC2); exact error `name must not be blank` for all four invalid names (AC3); `"greeting_has_apostrophe" in nmg_sdlc_smoke.__all__` and `True`/`False` for the README examples `O'Brien` and `Ada` (AC4). Run `python -m pytest tests/features/steps/test_greeting_has_apostrophe_steps.py` with four passing scenarios.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #181 | 2026-09-27 | Initial feature tasks |
