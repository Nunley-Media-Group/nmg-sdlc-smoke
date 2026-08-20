# Tasks: Add --help to publish-approved-spec

**Issue**: #1
**Date**: 2026-08-20
**Status**: Approved
**Author**: Rich Nunley

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Implementation | 1 | [ ] |
| Testing | 1 | [ ] |
| **Total** | 2 | |

---

## Phase 1: Implementation

### T001: Add first-argument --help in main()

**File(s)**: `scripts/publish-approved-spec.mjs`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `main()` treats `command === '--help'` before the four subcommand checks
- [ ] That branch writes exactly `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...\n` to stdout via `process.stdout.write`
- [ ] That branch calls `process.exit(0)` and does not call `fail()` or `ok()`
- [ ] Remaining argv after `--help` is ignored
- [ ] `-h` is not added
- [ ] The invalid-arguments `detail` string is unchanged
- [ ] `prepare`, `commit-push`, `merge`, and `default-branch` dispatch is unchanged

**Notes**: Insert the `--help` `if` immediately after `const [command, ...rest] = argv;`. Do not extract a new CLI parser.

---

## Phase 2: Testing

### T002: Cover --help success and unrecognized first arguments

**File(s)**: `scripts/__tests__/publish-approved-spec.test.mjs`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] A test runs the script with first argument `--help` and asserts `status === 0`, stdout includes `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`, and stdout is not an object with `ok: false` and `reasonCode: 'invalid_arguments'`
- [ ] A test runs the script with an unrecognized first argument (use `not-a-command`) and asserts `status === 1` and parsed stdout `{ ok: false, reasonCode: 'invalid_arguments' }` whose `detail` contains that same usage line
- [ ] Existing prepare / commit-push / merge tests remain and still pass

**Notes**: Reuse `run()` and `parse()`. Help and invalid-first-arg cases may use `process.cwd()`; they must not require `makeRepo()`.

---

## Dependency Graph

```
T001 ──▶ T002
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #1 | 2026-08-20 | Initial feature spec |
