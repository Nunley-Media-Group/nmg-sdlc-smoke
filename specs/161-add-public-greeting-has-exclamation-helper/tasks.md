# Tasks: Add public greeting_has_exclamation helper

**Issue**: #161
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the exclamation query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_exclamation(name: str) -> bool` returning `"!" in greet(name)` and export it through the package root and `__all__`, leaving prior exports and the punctuation-appending helper intact (AC1–AC4, FR1–FR3).
- In README Library, show the public import, both exact boolean examples, and a sentence that it checks literal `!` in the completed greeting and inherits `greet`'s `ValueError("name must not be blank")` (AC4, FR4).

### T002: Cover the public query and invalid names with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- From the package-root import, assert `greeting_has_exclamation("Ada!") is True` and `greet("Ada!") == "Hello, Ada!"` (AC1); assert `greeting_has_exclamation("Ada") is False` and `greeting_has_exclamation("Ada！") is False` (AC2, AC4).
- Parameterize `""`, `" "`, `None`, `42` and assert exact `ValueError("name must not be blank")` for each (AC3); existing exported-helper tests continue passing (FR2). `python -m pytest tests/test_greet.py` passes.

### T003: Execute four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_exclamation_helper.feature`, `tests/features/steps/test_greeting_has_exclamation_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four uniquely tagged scenarios in this spec's `feature.gherkin` into the executable `.feature`, omitting its metadata and source comments; implement deterministic steps using the public package import and the neighboring punctuation-helper step conventions (AC1–AC4).
- Assert the exact completed greeting and Python boolean identity for `Ada!` (AC1), both false inputs including fullwidth punctuation (AC2), each invalid input and exact error (AC3), and the documented package import/true/false examples (AC4). `python -m pytest tests/features/steps/test_greeting_has_exclamation_steps.py` passes with four scenarios; inspect the README Library addition against AC4 separately, without testing source text.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #161 | 2026-09-26 | Initial feature tasks |
