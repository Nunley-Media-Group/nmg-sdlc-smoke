# Tasks: Add second serial lifecycle smoke marker

**Issue**: #12
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Files | Depends |
|------|-------|---------|
| T001 | `LIVE_SMOKE_B.txt` | None |
| T002 | `README.md` | T001 |
| T003 | `scripts/__tests__/live-smoke-b.test.mjs` | T001 |

---

### T001: Create the exact-byte second marker

**File(s)**: `LIVE_SMOKE_B.txt`
**Type**: Create
**Depends**: None
**Acceptance**:
- [ ] The file is at repository root.
- [ ] Its complete bytes equal `Buffer.from('smoke-b-213\n', 'utf8')`.
- [ ] It has one final LF and contains no BOM, spaces, carriage return, or additional newline.

### T002: Document the second serial lifecycle marker

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Under `## Verification Gates`, append exactly the sentence defined in `design.md`.
- [ ] The sentence identifies `LIVE_SMOKE_B.txt`, `smoke-b-213`, and the one-final-newline contract.
- [ ] The link target resolves to the root marker.
- [ ] No unrelated README content changes.

### T003: Add the deterministic exact-byte contract test

**File(s)**: `scripts/__tests__/live-smoke-b.test.mjs`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Use the exact test implementation from `design.md`, including the established `repoRoot` calculation.
- [ ] Read `LIVE_SMOKE_B.txt` without an encoding so the assertion compares raw `Buffer` values.
- [ ] `npm test -- --runTestsByPath __tests__/live-smoke-b.test.mjs` from `scripts/` exits zero for the canonical marker.
- [ ] The same focused test exits non-zero when the marker is missing, has changed text or extra bytes, lacks the final LF, or has an additional LF.
- [ ] Restore `LIVE_SMOKE_B.txt` to the canonical bytes after every negative probe.
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
| #12 | 2026-08-24 | Initial feature spec |
