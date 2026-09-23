# Tasks: Add greeting_has_digit helper

**Issue**: #115
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

### T001: Implement and export digit detection
**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] AC1 and AC2 pass; existing exports and CLI behavior remain unchanged.

### T002: Verify and document observable behavior
**File(s)**: `tests/test_greet.py`, `tests/features/`, `README.md`
**Type**: Modify/Create
**Depends**: T001
**Acceptance**:
- [ ] Independent pytest-bdd scenarios cover AC1-AC3 with deterministic outcomes.
- [ ] python -m pytest, python -m pytest tests/features, and python -m ruff check . pass.
- [ ] README includes greeting_has_digit examples without changing existing usage.
