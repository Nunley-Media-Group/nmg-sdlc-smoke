# Tasks: Ignore the nmg-sdlc v4 runtime directory .nmg-sdlc/

**Issue**: #219
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Swap the runtime ignore rule

**File(s)**: `.gitignore`
**Type**: Modify
**Depends**: none
**Acceptance**:
- `.omp/sdlc/` is replaced in place by `.nmg-sdlc/`; every other rule is unchanged (AC1, FR1)

### T002: Record the change

**File(s)**: `CHANGELOG.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- `CHANGELOG.md` records the change under `[Unreleased]`
