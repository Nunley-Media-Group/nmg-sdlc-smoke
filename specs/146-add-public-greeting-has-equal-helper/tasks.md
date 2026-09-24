# Tasks: Add public greeting_has_equal helper

**Issue**: #146
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement and expose the equals-sign query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_has_equal(name: str) -> bool` returning `"=" in greet(name)` and export it from the package root and `__all__`, without changing existing exports, `greet`, or the CLI (AC1–AC4, FR1–FR3).
- Show the public import, `True` and `False` examples, literal ASCII matching, and inherited invalid-name behavior in the README Library section without removing existing examples (AC1–AC3).

### T002: Prove public results and validation with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Import the public helper; check `greet("Ada=") == "Hello, Ada="` and `greeting_has_equal("Ada=") is True` (AC1); check `"Ada"` and `"Ada＝"` both return `False` (AC2).
- Parameterize `""`, `" "`, `None`, and `42` and check exact `ValueError("name must not be blank")` (AC3). Assert every preexisting public name listed in design is still importable; `greet("Ada")` and `greeting_has_hash("Ada#")` preserve their exact results (AC4). `python -m pytest tests/test_greet.py tests/test_cli.py` passes.

### T003: Prove each acceptance criterion through pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_equal_helper.feature`, `tests/features/steps/test_greeting_has_equal_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Materialize the four AC-linked scenarios from this spec's `feature.gherkin` into the executable feature, retaining unique `@SCN001`–`@SCN004` tags and omitting spec frontmatter and source comments. Follow `tests/features/steps/test_greeting_has_hash_steps.py` for deterministic package-root calls and cross-platform installed CLI discovery.
- Check exact greeting strings and Python boolean identities (AC1–AC2, including fullwidth lookalike), all four invalid values and their exact errors (AC3), and all preexisting public imports plus `greet("Ada")`, `greeting_has_hash("Ada#")`, and installed `nmg-smoke Ada` status 0/stdout `"Hello, Ada\n"`/empty stderr (AC4). `python -m pytest tests/features/steps/test_greeting_has_equal_steps.py` passes with four scenarios.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #146 | 2026-09-24 | Initial feature tasks |
