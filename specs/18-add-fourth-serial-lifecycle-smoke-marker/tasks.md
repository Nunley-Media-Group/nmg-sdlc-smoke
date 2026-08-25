# Tasks: Add fourth serial lifecycle smoke marker

**Issue**: #18
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Files | Depends |
|------|-------|---------|
| T001 | `LIVE_SMOKE_D.txt` | None |
| T002 | `README.md` | T001 |
| T003 | `scripts/__tests__/live-smoke-d.test.mjs` | T001, T002 |

---

### T001: Create the exact-byte fourth marker

**File(s)**: `LIVE_SMOKE_D.txt`
**Type**: Create
**Depends**: None
**Acceptance**:
- [ ] The file is at repository root.
- [ ] Its complete bytes equal `Buffer.from('LIVE_SMOKE_D\n', 'utf8')`.
- [ ] It has one final LF and contains no BOM, spaces, carriage return, or additional newline.

### T002: Document the fourth serial lifecycle marker

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Under `## Verification Gates`, append exactly the sentence defined in `design.md` after the existing lifecycle marker sentences.
- [ ] The sentence links `LIVE_SMOKE_D.txt`, identifies the fourth serial lifecycle smoke marker, and states the one-final-newline contract with token `LIVE_SMOKE_D`.
- [ ] The link target resolves to the root marker.
- [ ] No unrelated README content changes, including any existing marker sentence.

### T003: Add the deterministic bytes-and-README contract test

**File(s)**: `scripts/__tests__/live-smoke-d.test.mjs`
**Type**: Create
**Depends**: T001, T002
**Acceptance**:
- [ ] Use the exact test implementation from `design.md`, including the established `repoRoot` calculation and the README `toContain` of the documentation sentence.
- [ ] Read `LIVE_SMOKE_D.txt` without an encoding so the assertion compares raw `Buffer` values.
- [ ] `npm test -- --runTestsByPath __tests__/live-smoke-d.test.mjs` from `scripts/` exits zero for the canonical marker and README sentence.
- [ ] The same focused test exits non-zero when the marker is missing, has changed text or extra bytes, lacks the final LF, has an additional LF, or when README omits the D documentation sentence.
- [ ] Restore `LIVE_SMOKE_D.txt` and `README.md` to the canonical contents after every negative probe.
- [ ] `npm test` from `scripts/` passes with the canonical files restored.

---

## Dependency Graph

```text
T001 ──┬──▶ T002 ──▶ T003
       └─────────────▶ T003
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #18 | 2026-08-25 | Initial feature spec |
| #18 | 2026-08-25 | Spec revised before delivery |
