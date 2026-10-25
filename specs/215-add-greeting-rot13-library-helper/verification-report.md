# Verification Report: Add greeting_rot13 library helper

**Date**: 2026-10-24
**Issue**: #215
**Reviewer**: Claude (nmg-sdlc verify worker)
**Scope**: Implementation verification against spec

**Verification head**: 42533cb9bcf92e24afb1de67324e8e6bfc4911b3

---

## Executive Summary

The implementation commit `42533cb` ("feat: deliver issue #215") only changes `VERSION` (3.49.0 → 3.50.0) and `CHANGELOG.md`. None of the spec's work is in the tree. `greeting_rot13` is not in `src/nmg_sdlc_smoke/greet.py`, `nmg_sdlc_smoke/__init__.py`, `__all__`, or `README.md`, and the T002/T003 tests are missing. Every acceptance criterion fails.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 1 |
| Architecture (SOLID) | 3 |
| Security | 5 |
| Performance | 5 |
| Testability | 1 |
| Error Handling | 3 |
| **Overall** | 3.0 |

Only the existing code was scored for architecture; no new code exists to review.

### Implementation Status: Fail
**Total Issues**: 4

---

## Issue Scope

- Active issue: #215
- Spec: `specs/215-add-greeting-rot13-library-helper`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5]; FR [FR1, FR2, FR3]; tasks [T001, T002, T003]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":215,"specPath":"specs/215-add-greeting-rot13-library-helper","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5"],"functionalRequirements":["FR1","FR2","FR3"],"tasks":["T001","T002","T003"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Not complete
- PR evidence: Not required

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 215 --spec specs/215-add-greeting-rot13-library-helper --base main --controller-run-id 47f89399-a72e-4596-b452-160ef1c3909b`
- Artifact: `.nmg-sdlc/verification/215.json`, `ok: true`, `ceiling: null`
- Identity: head `42533cb9bcf92e24afb1de67324e8e6bfc4911b3`, steering `sha256:96bcc848…`, spec `sha256:f76d2582…`
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`. The manifest declares no project-specific validations, so `repository.nmg-sdlc-smoke` is not registered for this project.
- Note: the local `main` ref is one commit behind `origin/main` (it is missing #240), so the artifact's `changedPaths` includes #217 files. Compared with `origin/main`, the branch changes only `CHANGELOG.md` and `VERSION`.

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `greeting_rot13("Ada")` returns `Uryyb, Nqn` | Fail | `grep -rn rot13 src` finds nothing. `hasattr(nmg_sdlc_smoke, "greeting_rot13")` is `False`. |
| AC2 | Only ASCII letters are rotated | Fail | The helper does not exist. |
| AC3 | Applying ROT13 twice restores `greet(name)` | Fail | The helper does not exist. |
| AC4 | Invalid names raise `ValueError("name must not be blank")` | Fail | The helper does not exist. |
| AC5 | Exported, in `__all__`, README documented, CLI unchanged | Fail | `"greeting_rot13" in __all__` is `False` (`__all__` has 40 names). The README has no `greeting_rot13` import, example, or prose line. The CLI part passes: `nmg-smoke Ada` prints `Hello, Ada` and exits 0. |

| Scenario | Status | Evidence |
|----------|--------|----------|
| SCN001–SCN005 | Fail | Neither `tests/features/add_greeting_rot13_library_helper.feature` nor `tests/features/steps/test_greeting_rot13_steps.py` exists. |

| FR | Status |
|----|--------|
| FR1 | Fail: no `greeting_rot13` in `greet.py`, no `import codecs` |
| FR2 | Fail: the helper does not exist |
| FR3 | Fail: no export, no `__all__` entry, no README documentation |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Implement, export, and document `greeting_rot13` | Incomplete | `greet.py`, `__init__.py`, and `README.md` are unchanged. |
| T002 | pytest unit tests | Incomplete | `tests/test_greet.py` has no rot13 cases. |
| T003 | Five AC-linked pytest-bdd scenarios | Incomplete | The feature and step files are missing. |

The only changes are the release bookkeeping in `VERSION` and `CHANGELOG.md` (`[3.50.0]`, "Add greeting_rot13 library helper (#215)"). The CHANGELOG entry claims a feature that has not been delivered.

---

## Architecture Assessment

| Area | Score (1-5) | Notes |
|------|-------------|-------|
| SOLID Principles | 3 | Nothing new to assess. The existing `greet`/CLI separation is intact. |
| Security | 5 | No new surface. No runtime dependencies. |
| Performance | 5 | No change. |
| Testability | 1 | None of the required tests exist, so every AC is untested. |
| Error Handling | 3 | Nothing new to assess. `greet` validation is unchanged. |

---

## Test Results

Run in an isolated venv (Python 3.14.7) after `pip install -e ".[dev]"`:

| Command | Result |
|---------|--------|
| `python -m pytest` | 650 passed, 2 skipped |
| `python -m pytest tests/features` | 222 passed, 2 skipped |
| `python -m ruff check .` | All checks passed |
| `nmg-smoke Ada` | `Hello, Ada`, exit 0 |

These are only regression checks on existing behavior. None of them exercises #215.

Exercise testing: not applicable. This is not a plugin change; no `workflows/` or `agents/` files changed.

Smoke lifecycle: `repository.nmg-sdlc-smoke` is not declared in `steering/manifest.json` (`validations: []`), so this report has no registered smoke result.

---

## Fixes Applied

| Severity | Category | Location | Issue | Fix | Routing |
|----------|----------|----------|-------|-----|---------|
| — | — | — | None | Verify's publication scope only allows writing `verification-report.md`. Delivering T001–T003 is implementation work, not a small local fix. | — |

---

## Remaining Issues

| Severity | Category | Location | Issue | Reason Not Fixed |
|----------|----------|----------|-------|------------------|
| Critical | Spec compliance | `src/nmg_sdlc_smoke/greet.py` | `greeting_rot13` and `import codecs` are missing (T001, FR1, FR2) | Outside the verify scope. Route to implementation. |
| Critical | Spec compliance | `src/nmg_sdlc_smoke/__init__.py`, `README.md` | Export, `__all__` entry, and README import, example, and prose line are missing (T001, FR3) | Outside the verify scope. Route to implementation. |
| High | Testability | `tests/test_greet.py`, `tests/features/` | Unit tests and the SCN001–SCN005 feature and steps are missing (T002, T003) | Outside the verify scope. Route to implementation. |
| Medium | Release hygiene | `CHANGELOG.md`, `VERSION` | The 3.50.0 entry claims a feature that has not been delivered | Will be accurate once the implementation lands. |

---

## Recommendation

Major rework needed. Return to implementation for T001–T003, then run the full gate again at the new head.
