# Requirements: Add LIVE_SMOKE_362_A verification marker

**Issue**: #82
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## Acceptance Criteria

### AC1: Exact marker content

**Given** the issue is implemented
**When** `LIVE_SMOKE_362_A.txt` is read
**Then** its contents are exactly `LIVE_SMOKE_362_A` followed by one newline

### AC2: Existing verification remains green

**Given** the marker exists
**When** pytest, feature pytest, and Ruff run
**Then** each exits zero

### AC3: No unrelated product changes

**Given** the completed change
**When** its paths are inspected
**Then** the only product change is `LIVE_SMOKE_362_A.txt`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add root `LIVE_SMOKE_362_A.txt` with exact content and one newline. | Must |
| FR2 | Preserve all existing runtime behavior and dependencies. | Must |
| FR3 | Add a unit test for exact marker content. | Must |
| FR4 | Pass pytest, feature pytest, and Ruff. | Must |

## Out of Scope

- Runtime or CLI changes
- Dependency changes
- Additional markers

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #82 | 2026-09-04 | Initial feature spec |
