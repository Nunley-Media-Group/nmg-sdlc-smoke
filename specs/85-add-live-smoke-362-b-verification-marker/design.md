# Design: Add LIVE_SMOKE_362_B verification marker

**Issue**: #85
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

---

## Overview

Add root regular file `LIVE_SMOKE_362_B.txt` containing exactly `LIVE_SMOKE_362_B\n`. Add a focused unit test and executable pytest-bdd scenarios for exact content, existing verification, and isolated product paths. No package, CLI, dependency, steering, or version behavior changes.

## Changes

| File | Change |
|------|--------|
| `LIVE_SMOKE_362_B.txt` | Add exact marker payload. |
| `tests/test_live_smoke_362_b_marker.py` | Assert exact regular-file content. |
| `tests/features/` | Execute AC1–AC3 without recursive verification. |

## Risks

| Risk | Mitigation |
|------|------------|
| Wrong payload | Exact text and byte assertions. |
| Recursive meta-test | Parent verification supplies full-gate evidence; BDD checks observable marker and path isolation. |

## Steering Alignment

The marker is a deterministic stack-neutral lifecycle probe. Existing Python runtime boundaries remain unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #85 | 2026-09-05 | Initial feature design |
