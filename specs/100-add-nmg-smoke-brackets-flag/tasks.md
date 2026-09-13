# Tasks: Add nmg-smoke --brackets flag

**Issue**: #100
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| CLI | 1 | [ ] |
| BDD | 1 | [ ] |
| Documentation and verification | 1 | [ ] |
| **Total** | **3** | |

## CLI

### T001: Add opt-in composed-greeting brackets

**File(s)**: src/nmg_sdlc_smoke/cli.py
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] --brackets is a long boolean option that wraps the message after uppercase and prefix composition and before the existing repeat/newline output.
- [ ] Contents receive no additional transformation or escaping; omitted flag, library APIs, validation, repeat, and newline semantics remain unchanged.

## BDD

### T002: Cover enabled composition and omitted preservation

**File(s)**: tests/features/add_nmg_smoke_brackets_flag.feature; tests/features/steps/test_brackets_steps.py
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Exactly two scenarios implement AC1 and AC2 from feature.gherkin, preserving stable @SCN001 and @SCN002 tags.
- [ ] All four commands assert exact stdout, empty stderr, and exit 0 through the real CLI using existing pytest-bdd conventions.
- [ ] Existing CLI validation coverage remains intact; reuse existing step helpers where appropriate rather than introducing a new harness.

## Documentation and Verification

### T003: Document the flag and verify delivery behavior

**File(s)**: README.md; CHANGELOG.md; VERSION (delivery owner only)
**Type**: Modify
**Depends**: T002
**Acceptance**:
- [ ] README describes --brackets and its composition order with a literal example; library documentation is unchanged.
- [ ] CHANGELOG records the enhancement while preserving released history; any VERSION change is owned by delivery and remains on the 3.x line with pyproject.toml still dynamically reading VERSION.
- [ ] python -m pytest, python -m pytest tests/features, and python -m ruff check . pass with recorded outcomes.
- [ ] Actual installed nmg-smoke commands from both criteria produce the specified stdout, stderr, and exit status.

## Execution Boundary

These tasks are for the authorized delivery owner, not this spec-authoring clone. Publication writes only this singular four-file approved package. No stopped queue, additional issue, provider safety approval, or execution is part of publication.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #100 | 2026-09-07 | Initial feature spec |
