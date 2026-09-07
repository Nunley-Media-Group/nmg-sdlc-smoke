# Tasks: Exact greeting suffix delivery fixture

**Issue**: #96
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## Summary
Three small implementation tasks; downstream review/verify/deliver retain normal stage ownership.

### T001: Add optional exact suffix rendering
**File(s)**: src/nmg_sdlc_smoke/cli.py
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] AC1 appends verbatim suffix after existing transformations and before repetition.
- [ ] AC2 preserves default/error output and provides argparse help.

### T002: Verify CLI behavior and BDD acceptance
**File(s)**: tests/test_cli.py; tests/features/exact_greeting_suffix.feature; tests/features/steps/test_exact_greeting_suffix_steps.py
**Type**: Modify/Create
**Depends**: T001
**Acceptance**:
- [ ] Two scenarios map AC1/AC2 and SCN001/SCN002 one-to-one using existing pytest-bdd conventions.
- [ ] Observable suffix/uppercase/prefix/repeat/no-newline composition and invalid-name boundaries are proven.
- [ ] Actual CLI smoke, full pytest, full BDD and Ruff pass in an isolated environment.

### T003: Document the fixture and publish implementation evidence
**File(s)**: README.md; CHANGELOG.md; VERSION only in delivery stage
**Type**: Modify
**Depends**: T001, T002
**Acceptance**:
- [ ] README shows one exact --suffix example and does not alter existing contracts.
- [ ] Scoped pending changelog, simplified implementation and clean commit/push evidence are ready for managed review.
- [ ] Normal downstream verification and exact-head merge/issue closure remain mandatory; implement does not open a PR or fabricate downstream proof.

## Change History

| Issue | Date | Summary |
|---|---|---|
| #96 | 2026-09-07 | Approved minimal fresh delivery fixture required to verify nmg-sdlc #372; not independent smoke backlog work |
