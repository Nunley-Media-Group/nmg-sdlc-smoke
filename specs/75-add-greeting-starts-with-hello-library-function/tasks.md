# Tasks: Add greeting_starts_with_hello library function

**Issue**: #75
**Date**: 2026-09-03
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| T001 | Add and export the pure helper | [ ] |
| T002 | Add unit and BDD coverage | [ ] |
| T003 | Document and verify behavior | [ ] |

### T001: Add and Export the Helper

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] The helper returns `greet(name).startswith("Hello, ")`.
- [ ] Existing exports remain present.
- [ ] Invalid-name errors propagate unchanged.
- [ ] `greet` and `cli.py` behavior remain unchanged.

### T002: Add Unit and BDD Coverage

**File(s)**: `tests/test_greet.py`, `tests/features/`, `tests/features/steps/`
**Type**: Modify and Create
**Depends**: T001
**Acceptance**:
- [ ] AC1–AC3 have executable pytest-bdd scenarios.
- [ ] Unit tests prove bool identity, export, and invalid-name behavior.
- [ ] Existing greeting and CLI regressions pass.

### T003: Document and Verify Behavior

**File(s)**: `README.md`
**Type**: Modify and Verify
**Depends**: T001, T002
**Acceptance**:
- [ ] README has one concise library example.
- [ ] Runtime dependencies remain zero.
- [ ] Full pytest, feature pytest, and Ruff pass.

Delivery evidence must explain alignment with `steering/manifest.json` and its registered managed steering runtime.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #75 | 2026-09-03 | Initial feature task plan |
