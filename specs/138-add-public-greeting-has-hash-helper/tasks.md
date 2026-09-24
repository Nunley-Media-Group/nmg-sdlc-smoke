# Tasks: Add public greeting_has_hash helper

**Issue**: #138
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement public hash predicate

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Return `"#" in greet(name)` from `greeting_has_hash(name: str) -> bool` and export it from the package (AC1, AC2, FR1).
- Propagate `greet`'s invalid-name `ValueError` without duplicating validation or changing existing greeting interfaces (AC3, AC4, FR2).

### T002: Cover public helper and preserved library behavior with pytest

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Assert the public import returns `True` for `Ada#`, `False` for `Ada`, and `ValueError("name must not be blank")` for `""`, `" "`, `None`, and `42` (AC1–AC3, FR3).
- Assert `greet("Ada") == "Hello, Ada"` and `greeting_has_question_mark("Ada?") is True` remain intact; the existing `tests/test_cli.py::test_cli_prints_greeting` retains the adapter contract (AC4, FR3).

### T003: Cover all acceptance outcomes with pytest-bdd

**File(s)**: `tests/features/add_public_greeting_has_hash_helper.feature`, `tests/features/steps/test_greeting_has_hash_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Implement one observable pytest-bdd scenario for each AC1–AC4 from `feature.gherkin` (copy executable Feature/scenario text without the spec metadata); cover all four invalid examples in AC3 (FR3).
- AC4 invokes the installed `nmg-smoke Ada` console script and checks exit 0, stdout exactly `"Hello, Ada\n"`, and no stderr, alongside the two preserved library results.

### T004: Document the helper in library usage

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_has_hash` to the Library import and show `greeting_has_hash("Ada#")  # True` and `greeting_has_hash("Ada")  # False`, preserving existing examples (FR4, AC1, AC2).

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #138 | 2026-09-24 | Initial feature tasks |
