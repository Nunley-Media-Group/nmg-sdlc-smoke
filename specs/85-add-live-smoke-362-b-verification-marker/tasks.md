# Tasks: Add LIVE_SMOKE_362_B verification marker

**Issue**: #85
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| T001 | Add exact marker file | [ ] |
| T002 | Add unit and BDD coverage | [ ] |
| T003 | Run all verification gates | [ ] |

### T001: Add Exact Marker File

**File(s)**: `LIVE_SMOKE_362_B.txt`
**Acceptance**:
- [ ] File content is exactly `LIVE_SMOKE_362_B\n`.

### T002: Add Unit and BDD Coverage

**File(s)**: `tests/test_live_smoke_362_b_marker.py`, `tests/features/`
**Acceptance**:
- [ ] Unit coverage asserts exact regular-file content.
- [ ] AC1–AC3 have executable pytest-bdd coverage.

### T003: Run All Verification Gates

**Type**: Verify
**Acceptance**:
- [ ] Full pytest exits zero.
- [ ] Feature pytest exits zero.
- [ ] Ruff exits zero.
- [ ] Only the intended marker is a product change.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #85 | 2026-09-05 | Initial task plan |
