# Tasks: Add --help to publish-approved-spec

**Issue**: #3
**Date**: 2026-08-20
**Status**: Approved
**Author**: write-spec
---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Implementation | 1 | [ ] |
| Testing | 1 | [ ] |
| **Total** | 2 | |

---

## Phase 1: Implementation

### T001: Add first-token --help to publish helper

**File(s)**: `scripts/publish-approved-spec.mjs`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `const USAGE` equals `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`
- [ ] `main()` writes `${USAGE}\n` to stdout and returns when `command === '--help'`
- [ ] The unknown-command `fail('invalid_arguments', …)` uses `{ detail: USAGE }`
- [ ] `prepare`, `commit-push`, `merge`, and `default-branch` branches are unchanged
- [ ] `-h` is not handled

**Notes**: Insert the `--help` check immediately after `const [command, ...rest] = argv;` and before the `prepare` check. Extra argv after `--help` is ignored.

---

## Phase 2: Testing

### T002: Cover --help and unchanged first tokens

**File(s)**: `scripts/__tests__/publish-approved-spec.test.mjs`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] A test runs `run(os.tmpdir(), ['--help'])`, expects `status === 0`, and expects stdout to contain the exact USAGE string
- [ ] A test runs `[]`, `['-h']`, `['nope']`, and `['prepare', '--help']` and expects each `status !== 0` and parsed JSON `{ ok: false, reasonCode: 'invalid_arguments' }`
- [ ] Existing prepare/commit-push/merge tests remain

---

## Dependency Graph

```
T001 ──▶ T002
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #3 | 2026-08-20 | Initial feature spec |
