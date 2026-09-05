# Tasks: Add casefolded greeting helper

**Issue**: #90
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

### T001: Implement and export casefolded greeting
**File(s)**: src/nmg_sdlc_smoke/greet.py, src/nmg_sdlc_smoke/__init__.py
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] AC1 and AC2 pass; all existing exports remain.

### T002: Verify consumer contract and document usage
**File(s)**: tests/test_greet.py, tests/features/, README.md
**Type**: Modify/Create
**Depends**: T001
**Acceptance**:
- [ ] Independent pytest-bdd scenarios cover AC1-AC3.
- [ ] python -m pytest, python -m pytest tests/features, python -m ruff check . pass.
- [ ] README includes greeting_casefold Unicode example while preserving existing behavior documentation.
