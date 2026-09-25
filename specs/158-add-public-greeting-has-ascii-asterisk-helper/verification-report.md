# Verification Report: Add public greeting_has_ascii_asterisk helper

**Date**: 2026-09-25
**Issue**: #158
**Reviewer**: Codex
**Scope**: Implementation verification against spec
**Verification head**: d649006230ecfd153b3bcb2924dd1ec7e31c6b4d

---

## Executive Summary

The branch `158-add-public-greeting-has-ascii-asterisk-helper` has no implementation. Its head `d649006` is the spec-approval commit, which is also `origin/main`, so `git diff main...HEAD` is empty. `greeting_has_ascii_asterisk` does not exist in `src/`, `tests/`, or `README.md`. None of the tasks T001–T003 were done, and none of the ACs AC1–AC4 are met.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 1 |
| Architecture (SOLID) | N/A (no changed code) |
| Security | N/A (no changed code) |
| Performance | N/A (no changed code) |
| Testability | 1 |
| Error Handling | N/A (no changed code) |
| **Overall** | 1.0 (scored areas only) |

### Implementation Status: Fail
**Total Issues**: 3

---

## Issue Scope

- Active issue: #158
- Spec: `specs/158-add-public-greeting-has-ascii-asterisk-helper`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4]; FR [FR1, FR2, FR3]; tasks [T001, T002, T003]; scenarios [SCN001, SCN002, SCN003, SCN004]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":158,"specPath":"specs/158-add-public-greeting-has-ascii-asterisk-helper","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4"],"functionalRequirements":["FR1","FR2","FR3"],"tasks":["T001","T002","T003"],"scenarios":["SCN001","SCN002","SCN003","SCN004"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Not complete
- PR evidence: Not required

---

## Deterministic Steering Artifact and Ceiling

- Command: `sdlc-verify-steering.mjs --project . --issue 158 --spec specs/158-add-public-greeting-has-ascii-asterisk-helper --base main --controller-run-id f71d921f-7582-4e4c-a3f9-56d24bead574`
- Artifact: `.omp/sdlc/verification/158.json`. Head `d649006230ecfd153b3bcb2924dd1ec7e31c6b4d`, `ceiling: null`, `changedPaths: []`.
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`. `steering/manifest.json` registers no project-specific validations, so no `repository.nmg-sdlc-smoke` / `project.nmg-sdlc-smoke` provider is declared.
- The steering gate does not cap the status, but because nothing was implemented, the status is Fail.

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `greeting_has_ascii_asterisk("Ada*")` returns `True` | Fail | Symbol missing: `hasattr(nmg_sdlc_smoke, "greeting_has_ascii_asterisk")` returned `False` in an isolated venv. |
| AC2 | `greeting_has_ascii_asterisk("Ada")` returns `False` | Fail | Symbol missing (same evidence as AC1). |
| AC3 | Invalid names raise `ValueError("name must not be blank")` | Fail | Symbol missing, so the helper cannot be called. |
| AC4 | Prior exports, `greet`, `greeting_has_asterisk`, and the CLI are preserved; the new export is importable | Fail | Prior interfaces still work because the code did not change: the full suite passes. The new export required by the AC does not exist. |

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Implement and expose the ASCII asterisk query | Incomplete | `src/nmg_sdlc_smoke/greet.py`, `__init__.py`, and `README.md` are unchanged from main. |
| T002 | Prove public results and validation with pytest | Incomplete | `tests/test_greet.py` has no `greeting_has_ascii_asterisk` tests. |
| T003 | Prove every AC with pytest-bdd | Incomplete | `tests/features/add_public_greeting_has_ascii_asterisk_helper.feature` and `tests/features/steps/test_greeting_has_ascii_asterisk_steps.py` do not exist. |

---

## Architecture Assessment

There is no changed code to score for SOLID, security, performance, or error handling. The existing layer boundaries still hold: the library is pure, and the CLI is a thin adapter over it. Testability is scored 1 because none of the required tests exist.

---

## Test Coverage

### BDD Scenarios

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 / SCN001 | No | No | No |
| AC2 / SCN002 | No | No | No |
| AC3 / SCN003 | No | No | No |
| AC4 / SCN004 | No | No | No |

### Registered commands (isolated venv, `pip install -e ".[dev]"`)

- `python -m pytest`: 303 passed, 2 skipped
- `python -m pytest tests/features`: 116 passed, 2 skipped
- `python -m ruff check .`: All checks passed

These passes cover only existing behavior. None of them exercise #158.

---

## Fixes Applied

None. The publication scope for the verify step allows writing only `verification-report.md`, and adding the missing feature is implementation work, not a local verification fix.

## Remaining Issues

### Critical Issues

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | Spec Compliance |
| **Location** | `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md` |
| **Issue** | T001 is not implemented: `greeting_has_ascii_asterisk` does not exist and is not exported. |
| **Impact** | AC1–AC4 and FR1–FR3 are not met. |
| **Reason Not Fixed** | This is implementation scope, and the verify publication scope does not allow writing these files. |

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | Testing |
| **Location** | `tests/test_greet.py` |
| **Issue** | T002 unit tests are missing. |
| **Impact** | There is no unit evidence for AC1–AC4. |
| **Reason Not Fixed** | This is implementation scope. |

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | Testing |
| **Location** | `tests/features/` |
| **Issue** | T003 pytest-bdd feature and step files for SCN001–SCN004 are missing. |
| **Impact** | There is no acceptance evidence. |
| **Reason Not Fixed** | This is implementation scope. |

---

## Recommendations Summary

### Before PR (Must)
- [ ] Implement T001–T003 on this branch, then run the full verification gate again at the new head.

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/greet.py` | 1 | Helper missing |
| `src/nmg_sdlc_smoke/__init__.py` | 1 | Export missing |
| `tests/test_greet.py` | 1 | Tests missing |
| `tests/features/` | 1 | Feature and steps missing |

---

## Recommendation

**Major rework needed**

The branch has no implementation for #158. Route it back to implementation.
