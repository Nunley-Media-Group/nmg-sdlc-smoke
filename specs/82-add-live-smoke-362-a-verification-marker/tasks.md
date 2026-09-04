# Tasks: Add LIVE_SMOKE_362_A verification marker

**Issue**: #82
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| T001 | Add exact marker file | [ ] |
| T002 | Add exact-content unit test | [ ] |
| T003 | Run all verification gates | [ ] |

### T001: Add Exact Marker File

**File(s)**: `LIVE_SMOKE_362_A.txt`
**Acceptance**:
- [ ] The file is regular and contains exactly `LIVE_SMOKE_362_A\n`.

### T002: Add Exact-content Unit Test

**File(s)**: `tests/test_live_smoke_marker.py`
**Acceptance**:
- [ ] A unit test reads the root marker and asserts exact content.

### T003: Run All Verification Gates

**Type**: Verify
**Acceptance**:
- [ ] `python -m pytest` exits zero.
- [ ] `python -m pytest tests/features` exits zero.
- [ ] `python -m ruff check .` exits zero.
- [ ] No unrelated product path changes.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #82 | 2026-09-04 | Initial task plan |
