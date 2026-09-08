# Tasks: Add nmg-smoke braces flag

**Issue**: #105
**Date**: 2026-09-08
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

### T001: Add the opt-in outermost braces wrapper

**File(s)**: `src/nmg_sdlc_smoke/cli.py`, `tests/test_cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] Add long-only boolean --braces using the existing argparse pattern, disabled when absent.
- [ ] Wrap after all existing formatting including parentheses, before repeat/newline emission, adding only literal { and }.
- [ ] Preserve literal content, existing validation, library APIs, and absent-flag output bytes.
- [ ] Keep existing CLI behavior coverage; add only focused observable unit coverage for literal-content preservation where useful.

## Phase 2: BDD Testing

### T002: Add exactly two acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_braces_flag.feature`
**Type**: Create
**Depends**: T001
**Acceptance**:
- [ ] Translate feature.gherkin into executable Gherkin without Markdown metadata, retaining SCN001 and SCN002.
- [ ] Exactly two scenarios cover enabled outermost composition and absent/default preservation with the exact expected bytes in requirements.md.

### T003: Bind and verify both scenarios

**File(s)**: `tests/features/steps/test_braces_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Use existing pytest-bdd main/capsys conventions; keep scenarios independent and full-suite safe.
- [ ] Assert exact stdout, empty stderr, and exit 0 for every specified invocation, including separating and final LF behavior.
- [ ] Run python -m pytest, python -m pytest tests/features, and python -m ruff check . during implementation verification.

## Phase 3: Documentation

### T004: Document the optional outermost wrapper

**File(s)**: `README.md`, `CHANGELOG.md`, `VERSION` (delivery-owner only)
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Document --braces, outermost composition after parentheses, and byte-identical absent behavior without changing library documentation.
- [ ] Record the enhancement in CHANGELOG while preserving all released history.
- [ ] Implementation does not edit VERSION; the delivery owner alone selects and applies release version changes on the current major line.

## Dependency Graph

T001 -> T002 -> T003; T001 -> T004. No external issue dependencies.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #105 | 2026-09-08 | Initial feature spec |
