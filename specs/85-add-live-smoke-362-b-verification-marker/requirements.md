# Requirements: Add LIVE_SMOKE_362_B verification marker

**Issue**: #85
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

---

## Acceptance Criteria

### AC1: Exact marker content

**Given** the issue is implemented
**When** `LIVE_SMOKE_362_B.txt` is read
**Then** its contents are exactly `LIVE_SMOKE_362_B` followed by one newline

### AC2: Existing verification remains green

**Given** the marker exists
**When** pytest, feature pytest, and Ruff run
**Then** each exits zero

### AC3: No unrelated product changes

**Given** the completed change
**When** its paths are inspected
**Then** the only product change is `LIVE_SMOKE_362_B.txt`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add root `LIVE_SMOKE_362_B.txt` with exact content and one newline. | Must |
| FR2 | Preserve existing runtime behavior and dependencies. | Must |
| FR3 | Add a unit test and executable pytest-bdd scenarios. | Must |
| FR4 | Pass pytest, feature pytest, and Ruff. | Must |

## Out of Scope

- Runtime, CLI, or dependency changes
- Additional markers

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #85 | 2026-09-05 | Initial feature spec |
