# Tasks: Add nmg-smoke --quotes flag for nmg-sdlc #379 verification

**Issue**: #109
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

## Summary

Three bounded delivery tasks. Review, verification, and delivery retain their normal stage ownership. Spec publication performs none of them.

### T001: Add optional quote wrapping

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] Add a long-only boolean `--quotes` argparse flag with an omitted/false default and no short alias.
- [ ] Wrap the fully composed message in literal double quotes after uppercase, prefix, parentheses, and braces processing and before repeat/newline output.
- [ ] Preserve current validation, repeat, newline, error, and library behavior when omitted.
- [ ] Add no dependency, module, or library API.

### T002: Verify both observable scenarios

**File(s)**: `tests/test_cli.py`, `tests/features/add_nmg_smoke_quotes_flag.feature`, `tests/features/steps/test_quotes_steps.py`
**Type**: Modify/Create
**Depends**: T001
**Acceptance**:
- [ ] `@SCN001` proves the exact quoted composed output, exit 0, and empty stderr.
- [ ] `@SCN002` proves omitted `--quotes` preserves exact default output, exit 0, and empty stderr.
- [ ] Exactly two BDD scenarios map one-to-one to AC1 and AC2 using existing pytest-bdd conventions.
- [ ] Focused CLI tests assert consumer-observable behavior without duplicating unrelated option cases.

### T003: Document and deliver the enhancement

**File(s)**: `README.md`, `CHANGELOG.md`, `VERSION` (delivery-owner only)
**Type**: Modify
**Depends**: T001, T002
**Acceptance**:
- [ ] README documents `--quotes` with the exact composed-output example while preserving existing CLI and library documentation.
- [ ] CHANGELOG records #109 under the normal pending enhancement section without rewriting released history.
- [ ] Delivery alone applies the normal 3.x VERSION bump; `pyproject.toml` continues reading VERSION dynamically.
- [ ] Implementation verification runs the actual CLI smoke, full pytest, feature pytest, and Ruff commands required by the repository.

## Execution Boundary

This approved package is the single nmg-sdlc #379 verification fixture. Do not implement during spec publication, run `/sdlc-execute`, open a feature PR, create another fixture, or change existing smoke issues/specs/backlog.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #109 | 2026-09-13 | Initial feature tasks for the single nmg-sdlc #379 verification fixture |
