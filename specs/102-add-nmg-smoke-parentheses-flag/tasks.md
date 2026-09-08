# Tasks: Add nmg-smoke parentheses flag

**Issue**: #102
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| CLI | 1 | [ ] |
| BDD Testing | 2 | [ ] |
| Documentation | 1 | [ ] |
| **Total** | **4** | |

## Phase 1: CLI Implementation

### T001: Add the opt-in composed-message wrapper

**File(s)**: `src/nmg_sdlc_smoke/cli.py`, `tests/test_cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] Add long-only boolean --parentheses using the existing argparse pattern, disabled when absent.
- [ ] Wrap the fully composed message after uppercase/prefix and before repeat/newline emission, adding only literal ( and ).
- [ ] Preserve all content without escaping or extra transformation, existing validation, library APIs, and absent-flag output bytes.
- [ ] Keep existing CLI tests; add only focused observable unit coverage where useful for literal content preservation.

## Phase 2: BDD Testing

### T002: Add exactly two acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_parentheses_flag.feature`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Translate feature.gherkin into executable Gherkin, omitting Markdown metadata but retaining SCN001 and SCN002.
- [ ] Exactly two scenarios cover enabled composition and absent/default preservation, with the exact expected bytes from requirements.md.

### T003: Bind and verify the two scenarios

**File(s)**: `tests/features/steps/test_parentheses_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Follow existing pytest-bdd main/capsys step conventions; keep scenarios independent and full-suite safe.
- [ ] Assert exit status 0, empty stderr, and exact stdout including separating and final LF behavior for all specified invocations.
- [ ] Run python -m pytest, python -m pytest tests/features, and python -m ruff check . during implementation verification.

## Phase 3: Documentation

### T004: Document the optional wrapper

**File(s)**: `README.md`, `CHANGELOG.md`, `VERSION` (delivery-owner only)
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Document --parentheses, composition order, and unchanged default behavior in the CLI documentation without changing library documentation.
- [ ] Record the enhancement in CHANGELOG while preserving released history.
- [ ] Implementation does not edit VERSION; the delivery owner alone selects and applies release version changes on the current major line.

## Dependency Graph

T001 -> T002 -> T003; T001 -> T004. No external issue dependencies.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #102 | 2026-09-07 | Initial feature spec |
