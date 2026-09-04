# Tasks: Add greeting_ends_with_exclamation library function

**Issue**: #79
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| T001 | Add and export the helper | [ ] |
| T002 | Add unit and BDD coverage | [ ] |
| T003 | Document and verify behavior | [ ] |

### T001: Add and Export the Helper

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] The helper returns `greet(name)` followed by exactly one exclamation mark.
- [ ] Valid names are preserved byte-for-byte.
- [ ] Existing exports remain present.
- [ ] Invalid-name errors propagate unchanged.
- [ ] `greet` and `cli.py` behavior remain unchanged.

### T002: Add Unit and BDD Coverage

**File(s)**: `tests/test_greet.py`, `tests/features/`, `tests/features/steps/`
**Type**: Modify and Create
**Depends**: T001
**Acceptance**:
- [ ] AC1–AC4 have executable pytest-bdd scenarios.
- [ ] Unit tests prove exact output, public export, whitespace preservation, and invalid-name behavior.
- [ ] Existing greeting and CLI regressions pass.

### T003: Document and Verify Behavior

**File(s)**: `README.md`
**Type**: Modify and Verify
**Depends**: T001, T002
**Acceptance**:
- [ ] README has one concise library example.
- [ ] Runtime dependencies remain zero and `VERSION` is unchanged.
- [ ] Full pytest, feature pytest, and Ruff pass.

Delivery evidence must explain alignment with `steering/manifest.json` and its registered managed steering runtime.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #79 | 2026-09-04 | Initial feature task plan |
