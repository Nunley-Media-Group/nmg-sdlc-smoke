# Tasks: Add LIVE_SMOKE_A lifecycle verification marker

**Issue**: #11
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Files | Depends |
|------|-------|---------|
| T001 | `LIVE_SMOKE_A.txt` | None |
| T002 | `README.md` | T001 |
| T003 | `scripts/__tests__/live-smoke-a.test.mjs` | T001 |

---

### T001: Create the exact-byte lifecycle marker

**File(s)**: `LIVE_SMOKE_A.txt`
**Type**: Create
**Depends**: None
**Acceptance**:
- [ ] The file is at repository root.
- [ ] Its complete bytes equal `Buffer.from('smoke-a-213\n', 'utf8')`.
- [ ] It has one final LF and contains no BOM, spaces, carriage return, or additional newline.

### T002: Document the lifecycle marker

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Under `## Verification Gates`, append exactly the sentence defined in `design.md`.
- [ ] The link target resolves to the root marker.
- [ ] No unrelated README content changes.

### T003: Add the deterministic exact-byte contract test

**File(s)**: `scripts/__tests__/live-smoke-a.test.mjs`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Use the exact test implementation from `design.md`, including the established `repoRoot` calculation.
- [ ] Read `LIVE_SMOKE_A.txt` without an encoding so the assertion compares raw `Buffer` values.
- [ ] `npm test -- --runTestsByPath __tests__/live-smoke-a.test.mjs` from `scripts/` passes for the canonical marker.
- [ ] The same targeted test exits non-zero when the marker is missing, lacks the final LF, has an extra LF, contains a BOM, or has any changed byte.
- [ ] `npm test` from `scripts/` passes with the canonical marker restored.

---

## Dependency Graph

```text
T001 ──┬──▶ T002
       └──▶ T003
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #11 | 2026-08-24 | Initial feature spec |
