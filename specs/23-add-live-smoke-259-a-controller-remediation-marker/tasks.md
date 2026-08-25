# Tasks: Add LIVE_SMOKE_259_A controller remediation marker

**Issue**: #23
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Files | Depends |
|------|-------|---------|
| T001 | `LIVE_SMOKE_259_A.txt` | None |

---

### T001: Create the exact-byte controller-remediation marker

**File(s)**: `LIVE_SMOKE_259_A.txt`
**Type**: Create
**Depends**: None
**Acceptance**:
- [ ] The file is at repository root.
- [ ] Its complete bytes equal `Buffer.from('controller remediation smoke A\n', 'utf8')`.
- [ ] It has one final LF and contains no BOM, leading or trailing spaces, carriage return, or additional newline.
- [ ] No other tracked product file is modified, including `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `README.md`, workflows, agents, extension commands, and `scripts/__tests__/`.
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
| #23 | 2026-08-25 | Initial feature spec |
