# Tasks: Add greeting_has_caret library helper for recovery smoke

**Issue**: #133
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

### T001: Implement and export literal caret query

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Acceptance**:
- [ ] Return `True` for a completed greeting containing `^` and `False` otherwise (AC1, AC2).
- [ ] Reuse `greet` validation and preserve existing exports and CLI behavior (AC3).

### T002: Verify acceptance behavior and document usage

**File(s)**: `tests/test_greet.py`, `tests/features/`, `README.md`
**Type**: Modify/Create
**Acceptance**:
- [ ] Add deterministic pytest coverage and three independent pytest-bdd scenarios for present, absent, and invalid names (AC1–AC3).
- [ ] Document the public helper and run `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` with passing results (AC1–AC3).
