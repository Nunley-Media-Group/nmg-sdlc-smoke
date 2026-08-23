# Requirements: Add execute startup retry smoke marker

**Issue**: #9
**Date**: 2026-08-22
**Status**: Approved
**Author**: NMG

---

## Acceptance Criteria

### AC1: Add the smoke marker

Given the disposable repository
When issue #9 is implemented
Then `EXECUTE_SMOKE.md` exists at the repository root
And its exact content is `Execute startup retry smoke completed.` followed by a newline.
