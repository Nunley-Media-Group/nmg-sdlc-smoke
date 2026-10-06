# Verification Report: Add nmg-smoke --titlecase flag

**Date**: 2026-10-06
**Issue**: #194
**Reviewer**: Codex
**Scope**: Implementation verification against spec

**Verification head**: fd95df05be4595f86a6c8ef19d3fa833990a6472

---

## Executive Summary

Branch `194-add-nmg-smoke-titlecase-flag` contains no implementation for #194. The verified head `fd95df0` (`docs: approve spec for #194 (#195)`) is identical to `main` and `origin/main`. `git diff main...HEAD` is empty, and the steering runner reports `changedPaths: []`. `--titlecase` does not appear in `src/`, `tests/`, `README.md`, or `CHANGELOG.md`. The installed console script rejects the flag with `nmg-smoke: error: unrecognized arguments: --titlecase` (exit 2). AC1–AC5 fail. AC6 is partial: the four existing outputs are preserved, but `--help` does not list `--titlecase`. Tasks T001–T004 are not done. The required steering checks pass, but only because they cover the existing behavior. No new behavior exists to test. Implementation is outside this verify run's publication scope, which allows writes only to this report, so the gap is not fixed here and routes back to implementation.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 1 |
| Architecture (SOLID) | 5 |
| Security | 5 |
| Performance | 5 |
| Testability | 1 |
| Error Handling | 3 |
| **Overall** | 3.3 |

### Implementation Status: Fail
**Total Issues**: 4 (1 Critical, 3 High)

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 194 --spec specs/194-add-nmg-smoke-titlecase-flag --base main --controller-run-id 3c9d46bf-6ac5-42ab-8926-154aa076f274`
- Artifact: `.omp/sdlc/verification/194.json` (`ok: true`)
- Identity: head `fd95df05be4595f86a6c8ef19d3fa833990a6472`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:da6f742ecae3dc5941d84a3f1dca0c7452fb74d74cc3832218f3ef38ee401094`
- Ceiling: `null`
- Coverage: declared 0, recorded 0, complete `true`; missing/duplicate/unknown are all empty
- `steering/manifest.json` registers `validations: []`. `repository.nmg-sdlc-smoke` and `project.nmg-sdlc-smoke` are not declared, so no real smoke lifecycle evidence is required.
- Changed paths vs `main`: none

---

## Issue Scope

- Active issue: #194
- Spec: `specs/194-add-nmg-smoke-titlecase-flag`
- Manifest: implicit single issue
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002, T003, T004]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":194,"specPath":"specs/194-add-nmg-smoke-titlecase-flag","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002","T003","T004"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Not complete
- PR evidence: Not required

---

## Acceptance Criteria Verification

All probes were run against the installed `nmg-smoke` from an isolated `pip install -e ".[dev]"` environment at the verification head.

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `nmg-smoke --titlecase ada` prints `Hello, Ada\n`, exit 0 | Fail | Exit 2, empty stdout, stderr `nmg-smoke: error: unrecognized arguments: --titlecase`. `src/nmg_sdlc_smoke/cli.py:20-23` registers only `--uppercase`, `--lowercase`, and `--swapcase` in the `case` group. |
| AC2 | `str.title()` semantics for `"ADA LOVELACE"`, `"o'neil"`, `åsa` | Fail | `nmg-smoke --titlecase "ADA LOVELACE"` → exit 2, `unrecognized arguments: --titlecase`. There is no `.title()` branch in `cli.py:39-44`. |
| AC3 | Composes with `--prefix`, `--quotes`, `--repeat`, `--no-newline` | Fail | `nmg-smoke --titlecase --prefix 'ok: ' --quotes --repeat 2 --no-newline ADA` → exit 2, empty stdout, `unrecognized arguments: --titlecase`. |
| AC4 | Combining with another case flag exits 2 with `not allowed with argument` | Fail | `--titlecase --uppercase Ada` and `--swapcase --titlecase Ada` exit 2, but stderr says `unrecognized arguments: --titlecase`, not `not allowed with argument`. The exit code matches only by accident. Mutual exclusion is not implemented. |
| AC5 | `nmg-smoke --titlecase " "` exits 1 with `name must not be blank` | Fail | Exit 2 with `unrecognized arguments: --titlecase`. Argument parsing fails before `greet` runs. |
| AC6 | Default/`--uppercase`/`--lowercase`/`--swapcase` output preserved; `--help` lists `--titlecase` | Partial | `Hello, Ada`, `HELLO, ADA`, `hello, ada`, and `hELLO, aDA` print as expected (FR4 holds trivially because nothing changed). Usage shows `[--uppercase \| --lowercase \| --swapcase]`, and `nmg-smoke --help \| grep -c titlecase` → `0`. |

### Functional Requirements

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Fail | No `--titlecase` argument or `str.title()` call in `src/nmg_sdlc_smoke/cli.py`. |
| FR2 | Fail | No title-casing stage exists. |
| FR3 | Fail | `--titlecase` is not in the `case` mutually exclusive group. |
| FR4 | Pass | Output without `--titlecase` is byte-identical (no source change; existing suites pass). |
| FR5 | Fail | `README.md` CLI section documents `--swapcase` at lines 156-165 and has no `--titlecase` entry. |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add the mutually exclusive `--titlecase` flag | Incomplete | `src/nmg_sdlc_smoke/cli.py` is unchanged from `main`. |
| T002 | Add focused CLI unit tests | Incomplete | `tests/test_cli.py` has no `--titlecase` tests. |
| T003 | Add pytest-bdd acceptance scenarios | Incomplete | `tests/features/add_nmg_smoke_titlecase_flag.feature` and `tests/features/steps/test_titlecase_steps.py` do not exist. |
| T004 | Document `--titlecase` in the README | Incomplete | No README change. |

---

## Architecture Assessment

There is no implementation diff to review. The scores below apply to the unchanged CLI and library at the verification head. They are not a judgment of a #194 implementation.

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | `greet.py` stays pure, and `cli.py` stays a thin argparse adapter. |
| Open/Closed | 5 | The existing `case` group plus `if/elif` casing step is the approved extension point for the new flag (design.md). |
| Liskov Substitution | 5 | Not applicable; no class hierarchies. |
| Interface Segregation | 5 | Public library API unchanged. |
| Dependency Inversion | 5 | The CLI depends on the library only; no reverse dependency. |

### Layer Separation

The library does not import the CLI, tests, or repository layout. This boundary is unchanged.

### Dependency Flow

`cli.main` → `greet`. There are no runtime dependencies (`pyproject.toml` unchanged).

---

## Security Assessment

No new input surface, because nothing changed. Existing CLI input is limited to argparse values and `greet` validation.

- [x] Authentication: N/A (local CLI)
- [x] Authorization: N/A
- [x] Input validation: blank names are still rejected by `greet` (exit 1)
- [x] Injection prevention: no shell, eval, or file I/O on user input
- [x] Data protection: N/A

---

## Performance Assessment

- [x] Async patterns: N/A
- [x] Caching: N/A
- [x] Resource management: no files or sockets opened
- [x] Query optimization: N/A

---

## Test Coverage

### BDD Scenarios

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 (SCN001) | No | No | No |
| AC2 (SCN002) | No | No | No |
| AC3 (SCN003) | No | No | No |
| AC4 (SCN004) | No | No | No |
| AC5 (SCN005) | No | No | No |
| AC6 (SCN006) | No | No | No |

### Coverage Summary

- Feature files: 0 of 6 approved #194 scenarios present
- Step definitions: Missing
- Unit tests: 0 `--titlecase` tests

### Required Steering Checks (technology steering)

| Command | Result |
|---------|--------|
| `python -m pip install -e ".[dev]"` (isolated venv) | Pass |
| `python -m pytest` | Pass — 447 passed, 2 skipped |
| `python -m pytest tests/features` | Pass — 165 passed, 2 skipped |
| `python -m ruff check .` | Pass — `All checks passed!` |

These passes show only that existing behavior is intact. None of these tests exercises #194 behavior.

---

## Exercise Test Results

| Field | Value |
|-------|-------|
| **Reason** | Not applicable: this is a Python CLI host, not a plugin change (no `workflows/` or `agents/` diff). |
| **Recommendation** | None |

---

## Fixes Applied

None. The verify publication scope permits writes only to `specs/194-add-nmg-smoke-titlecase-flag/verification-report.md`. The missing feature is implementation work, not a safe local verification fix.

## Remaining Issues

### Critical Issues

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | Architecture |
| **Location** | `src/nmg_sdlc_smoke/cli.py:20-44` |
| **Issue** | `--titlecase` is not implemented: it is missing from the `case` group and there is no `message.title()` branch (T001; AC1–AC5; FR1–FR3). |
| **Impact** | Every `--titlecase` invocation exits 2 with `unrecognized arguments`. |
| **Reason Not Fixed** | Implementation is outside the verify publication scope; routes to implementation. |

### High Priority

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Testing |
| **Location** | `tests/test_cli.py` |
| **Issue** | T002 unit tests are absent. |
| **Impact** | No regression protection for AC1–AC6. |
| **Reason Not Fixed** | Depends on T001; outside verify scope. |

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Testing |
| **Location** | `tests/features/add_nmg_smoke_titlecase_flag.feature`, `tests/features/steps/test_titlecase_steps.py` |
| **Issue** | T003 pytest-bdd scenarios SCN001–SCN006 are absent. |
| **Impact** | Approved acceptance criteria have no executable scenarios, which violates technology steering. |
| **Reason Not Fixed** | Depends on T001; outside verify scope. |

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Architecture |
| **Location** | `README.md` (CLI section after `--swapcase`, lines 156-165) |
| **Issue** | T004 / FR5 documentation is absent. |
| **Impact** | The user-facing flag would be undocumented. |
| **Reason Not Fixed** | Depends on T001; outside verify scope. |

### Medium Priority
None.

### Low Priority
None.

---

## Positive Observations

- The approved spec, design, and tasks are precise and mirror the #191 `--swapcase` pattern, so implementation is a small, well-bounded change.
- Existing behavior and all required checks are green at the verification head.

---

## Recommendations Summary

### Before PR (Must)
- [ ] Implement T001–T004 per `specs/194-add-nmg-smoke-titlecase-flag/tasks.md`.
- [ ] Re-run the full registered gate and fresh verification at the new implementation head.

### Short Term (Should)
- None

### Long Term (Could)
- None

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/cli.py` | 1 | No `--titlecase` |
| `tests/test_cli.py` | 1 | No `--titlecase` tests |
| `tests/features/` | 1 | No #194 feature or steps |
| `README.md` | 1 | No `--titlecase` docs |
| `steering/manifest.json` | 0 | `validations: []` |

---

## Recommendation

**Major rework needed**

The branch head equals `main`, and no #194 deliverable exists. Status is **Fail**. Return to implementation, then run the full verification again at the new head.
