# Remove history-dependent and recursive marker verification tests

**Issue**: #87
**Status**: Approved

## Problem

After squash delivery, marker tests classify VERSION and CHANGELOG.md as product changes and fail. Another test recursively runs the suite. Neither assertion describes marker behavior.

## Acceptance Criteria

- AC1: Exact marker bytes remain covered by unit and BDD tests.
- AC2: Marker tests do not invoke Git, network, or recursive verification commands.
- AC3: Ordinary pytest and Ruff verification pass after release metadata changes.

## Scope

Replace issue #82 SCN002 and SCN003 runtime tests with ordinary external CI verification; retain SCN001 and its unit regression. No product behavior changes.
