# Tasks: Add public greeting_has_exclamation_or_question helper

**Issue**: #163
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document the combined punctuation query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_exclamation_or_question(name: str) -> bool`: call `greet(name)` once and return whether its result contains literal `!` or `?`; propagate its existing invalid-name `ValueError` (AC1–AC4, FR1–FR2).
- Expose the helper through the package-root self-aliased import and `__all__` without removing existing exports. README Library shows the public import, `Ada!` and `Ada?` returning `True`, `Ada` returning `False`, and the inherited `ValueError("name must not be blank")` for invalid names (AC5, FR3).

### T002: Test the public query and validation with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import from the package root and assert Python boolean identity for `Ada!` → `True`, `Ada?` → `True`, `Ada` and `Ada！？` → `False`, and `Ada!?` → `True` (AC1–AC3, AC5).
- For each of `""`, `" \t"`, `None`, and `42`, assert `ValueError` with exact message `name must not be blank` (AC4). `python -m pytest tests/test_greet.py` passes.

### T003: Run five AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_has_exclamation_or_question_helper.feature`, `tests/features/steps/test_greeting_has_exclamation_or_question_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five distinct `@SCN001`–`@SCN005` scenarios from this spec's `feature.gherkin` to the executable `.feature`, without its frontmatter or source comments; implement steps using the public import and neighboring punctuation-step conventions (AC1–AC5).
- Assert exact boolean identity for `Ada!` (AC1), `Ada?` (AC2), all three AC3 names, exact errors for all AC4 invalid names, and public import/README example outcomes for AC5. `python -m pytest tests/features/steps/test_greeting_has_exclamation_or_question_steps.py` passes with five scenarios; inspect README's AC5 validation sentence directly rather than testing documentation source text.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #163 | 2026-09-26 | Initial feature tasks |
