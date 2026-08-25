# Requirements: Add LIVE_SMOKE_214_A managed steering verification marker

**Issue**: #30
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

## Acceptance Criteria

### AC1: Marker exists after implementation

**Given** the issue has been implemented
**When** root `LIVE_SMOKE_214_A.txt` is read
**Then** its complete UTF-8 bytes are `LIVE_SMOKE_214_A` followed by exactly one LF

### AC2: Pre-implementation absence is expected

**Given** implementation has not started
**When** the marker path is inspected
**Then** absence is the expected success-path precondition and is not a failure

### AC3: Existing verification remains green

**Given** the marker is implemented
**When** `cd scripts && npm test -- --runInBand` runs
**Then** the suite passes and unrelated product behavior remains unchanged

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add root `LIVE_SMOKE_214_A.txt` with UTF-8 `LIVE_SMOKE_214_A` plus one LF. | Must |
| FR2 | Preserve unrelated product behavior and existing verification. | Must |
| FR3 | Treat pre-implementation absence as expected. | Must |

## Out of Scope

- nmg-sdlc source or workflow changes
- Additional smoke issues or markers
