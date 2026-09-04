# Design: Add LIVE_SMOKE_362_A verification marker

**Issue**: #82
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## Overview

Add repository-root regular file `LIVE_SMOKE_362_A.txt` containing exactly:

```text
LIVE_SMOKE_362_A
```

Add a unit test that reads the file as UTF-8 and asserts the exact string including its single trailing newline. No Python package, CLI, dependency, steering, or version behavior changes.

## Changes

| File | Change |
|------|--------|
| `LIVE_SMOKE_362_A.txt` | Add exact marker payload. |
| `tests/test_live_smoke_marker.py` | Assert the exact regular-file content. |

## Risks

| Risk | Mitigation |
|------|------------|
| Wrong newline or text | Exact unit assertion. |
| Unrelated behavior changes | Restrict product diff to the marker. |

## Steering Alignment

The marker is a deterministic, stack-neutral lifecycle probe. Existing Python verification and package boundaries remain unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #82 | 2026-09-04 | Initial feature design |
