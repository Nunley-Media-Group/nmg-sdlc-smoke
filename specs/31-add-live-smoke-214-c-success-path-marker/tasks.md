# Tasks: Add LIVE_SMOKE_214_C success-path marker

**Issue**: #31
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Files | Depends |
|------|-------|---------|
| T001 | `LIVE_SMOKE_214_C.txt` | None |

---

### T001: Create the exact-byte LIVE_SMOKE_214_C success-path marker

**File(s)**: `LIVE_SMOKE_214_C.txt`
**Type**: Create
**Depends**: None
**Acceptance**:
- [ ] Before this task runs, root `LIVE_SMOKE_214_C.txt` is absent; that absence is the expected success-path precondition and is not a failure.
- [ ] After this task, the file is at repository root.
- [ ] Its complete bytes equal `Buffer.from('LIVE_SMOKE_214_C\n', 'utf8')`.
- [ ] It has one final LF and contains no BOM, leading or trailing spaces, carriage return, or additional newline.
- [ ] No other tracked product file is modified, including `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, `LIVE_SMOKE_259_B.txt`, `README.md`, workflows, agents, extension commands, and `scripts/__tests__/`.
- [ ] Existing `cd scripts && npm test` still passes without a new contract test for this marker.

---

## Dependency Graph

```text
T001
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #31 | 2026-08-25 | Initial feature spec |
